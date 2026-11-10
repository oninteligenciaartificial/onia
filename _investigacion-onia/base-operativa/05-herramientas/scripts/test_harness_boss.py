"""Puente con repos temporales, Codex sintético y HTTP simulado. Sin servicios reales."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

import harness
import harness_boss as boss
import harness_retorno as retorno
import trabajo
import test_harness_sesiones


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_harness_sesiones.SessionTests(methodName='runTest')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.base, self.repo, self.op = self.fixture.base, self.fixture.repo, self.fixture.op
        self.root = self.op / 'puente-boss'
        self.root.mkdir(parents=True, mode=0o700)
        harness.prepare(self.base, 'toy', 'desarrollo', 'Juguete', 'Texto', 'Comprobable', shared=True)
        self.row = trabajo.assign(self.base, 'toy', 1, 'executor', ['salidas/toy'])
        self.config = {'base': str(self.base), 'operacion': str(self.op), 'privado': str(self.root),
                       'lectura_ids': ['toy'], 'pausado': False}
        self.grant = {'id': 'toy', 'revocado': False, 'vence': '2099-01-01T00:00:00+00:00',
                      'binding': boss.binding(self.row), 'autorizacion_sergio': 'fixture',
                      'actor': 'executor', 'revisor': 'reviewer', 'modelo': 'gpt-6.1-sol',
                      'esfuerzo': 'low', 'max_intentos': 3,
                      'operaciones': sorted(boss.WRITE), 'resultado_cierre': 'Juguete publicado',
                      'comprobacion_cierre': 'fixture'}
        self.save_grant()
        self.fixture.git('add', '.')
        self.fixture.git('commit', '-m', 'tarea preparada')
        self.fixture.git('push', 'origin', 'master')

    def save_grant(self):
        boss.private_write(self.root / 'permisos/toy.json', self.grant)

    def req(self, op='ejecutar', nonce='solicitud-1'):
        return {'version': 1, 'operacion': op, 'id': 'toy', 'solicitud': nonce,
                'revision_esperada': trabajo.read_task(self.base, 'toy')['revision']}

    def close_fixture(self):
        folder = self.base / '04-operacion-agentes/evidencias/toy'
        folder.mkdir(parents=True)
        file = folder / 'entrega.md'
        file.write_text('Evidencia ficticia.\n')
        row = trabajo.update(self.base, 'toy', 'para_revision', 'Texto', 'Comprobado', 'Revisar',
                             [str(file.relative_to(self.base))], revision=2, verification='correcta', actor='executor')
        self.row = trabajo.mutate(self.base, 'toy', row['revision'],
            lambda d: dict(d, cierre={'commit': self.fixture.git('rev-parse', 'HEAD'), 'dry_run': False}), actor='executor')
        return self.row

    def secret(self):
        boss.private_write(self.root / 'webhook.json', {'url': 'https://example.invalid/hook',
                                                        'clave': 'test-secret-not-a-real-key'})

    def test_read_has_no_mutations_or_private_fields(self):
        files = list(self.base.rglob('*')) + list(self.root.rglob('*'))
        before = {str(p): p.read_bytes() for p in files if p.is_file()}
        result = boss.handle(self.config, {'version': 1, 'operacion': 'consultar', 'id': 'toy'})
        after = {str(p): p.read_bytes() for p in files if p.is_file()}
        self.assertEqual(before, after)
        self.assertNotIn('resultado', result['tarea'])
        self.assertNotIn(str(self.op), json.dumps(result))

    def test_bad_commands_paths_and_extra_fields(self):
        for data in [dict(self.req(), operacion='shell'), dict(self.req(), id='../toy'),
                     dict(self.req(), base='/tmp'), dict(self.req(), revision_esperada=True)]:
            with self.subTest(data=data), self.assertRaises(boss.Rejected):
                boss.handle(self.config, data)

    def test_config_ids_must_be_list(self):
        with self.assertRaises(boss.Rejected):
            boss.handle(dict(self.config, lectura_ids='toy-other'), self.req())

    def test_no_grant_no_launch(self):
        with patch.object(boss, 'private_read', side_effect=FileNotFoundError), patch.object(boss.sessions, 'launch') as launch:
            with self.assertRaises(FileNotFoundError): boss.handle(self.config, self.req())
            launch.assert_not_called()

    def test_expired_revoked_scope_and_model(self):
        for change in [{'vence': '2000-01-01T00:00:00+00:00'}, {'revocado': True},
                       {'binding': 'changed'}, {'modelo': 'other'}, {'operaciones': 'ejecutar'}]:
            with self.subTest(change=change), patch.object(boss, 'private_read', return_value=dict(self.grant, **change)):
                with self.assertRaises(boss.Rejected):boss.authorize(self.root, self.req(), self.row)

    def test_review_cannot_fall_back_to_executor(self):
        for reviewer in [None, '', 'executor']:
            self.grant['revisor'] = reviewer; self.save_grant()
            with patch.object(boss.sessions, 'launch') as launch, self.assertRaises(boss.Rejected):
                boss.handle(self.config, self.req('revisar'))
            launch.assert_not_called()

    def test_duplicate_request_launches_once(self):
        request = self.req()
        with patch.object(boss.sessions, 'launch') as launch:
            first = boss.handle(self.config, request)
            second = boss.handle(self.config, request)
            self.assertTrue(first['ok']); self.assertTrue(second['repetida'])
            self.assertEqual(launch.call_count, 1)
            self.assertTrue(launch.call_args.kwargs['auth_chatgpt'])
            self.assertEqual(launch.call_args.kwargs['subagents'], 0)

    def test_same_nonce_different_request_rejected(self):
        with patch.object(boss.sessions, 'launch'):
            boss.handle(self.config, self.req())
            with self.assertRaises(boss.Rejected):boss.handle(self.config, self.req('reanudar'))

    def test_uncertain_blocks_new_nonce_for_same_task(self):
        with patch.object(boss.sessions, 'launch', side_effect=RuntimeError('SECRET')) as launch:
            for nonce in ['one', 'two']:
                with self.assertRaisesRegex(boss.Rejected, 'conciliacion_necesaria'):
                    boss.handle(self.config, self.req(nonce=nonce))
            self.assertEqual(launch.call_count, 1)

    def test_stale_revision_does_not_launch(self):
        with patch.object(boss.sessions, 'launch') as launch, self.assertRaises(ValueError):
            boss.handle(self.config, dict(self.req(), revision_esperada=1))
        launch.assert_not_called()

    def test_pause_and_attempt_limits(self):
        with self.assertRaises(boss.Rejected):boss.handle(dict(self.config, pausado=True), self.req())
        with self.assertRaises(boss.Rejected):
            boss.invoke(self.config, self.req(), dict(self.row, sesiones=[{}, {}, {}]), self.grant)

    def test_private_files_reject_symlink_and_bad_mode(self):
        file = self.root / 'permisos/toy.json'
        file.chmod(0o644)
        with self.assertRaises(boss.Rejected):boss.private_read(file)
        link = self.root / 'link'; link.symlink_to(file)
        with self.assertRaises(boss.Rejected):boss.private_read(link)

    def test_non_command_ssh_rejected(self):
        with patch.dict('os.environ', {'SSH_ORIGINAL_COMMAND': 'cat ~/.codex/auth.json'}):
            with patch('builtins.print') as output:
                self.assertEqual(boss.serve(self.root / 'absent.json'), 2)
            self.assertNotIn('auth.json', str(output.call_args))

    def test_publisher_keeps_user_index_and_unrelated_edits(self):
        self.close_fixture()
        unrelated = self.repo / 'unrelated.txt'; unrelated.write_text('personal')
        self.fixture.git('add', 'unrelated.txt')
        index = self.repo / '.git/index'; before = index.read_bytes()
        commit = retorno.publish(self.config, self.row)
        self.assertEqual(before, index.read_bytes())
        self.assertEqual(unrelated.read_text(), 'personal')
        self.assertEqual(self.fixture.git('ls-tree', commit, '--', 'unrelated.txt'), '')
        relative = trabajo.task_path(self.base, 'toy').relative_to(self.repo).as_posix()
        self.assertEqual(json.loads(self.fixture.git('show', commit + ':' + relative))['revision'], self.row['revision'])

    def test_remote_same_revision_changed_rejected(self):
        self.close_fixture(); retorno.publish(self.config, self.row)
        path = trabajo.task_path(self.base, 'toy')
        data = json.loads(path.read_text()); data['resultado'] = 'changed at same revision'
        path.write_text(json.dumps(data))
        with self.assertRaises(boss.Rejected):retorno.publish(self.config, data)

    def test_remote_newer_revision_not_rolled_back(self):
        self.close_fixture(); old = dict(self.row)
        newer = trabajo.mutate(self.base, 'toy', old['revision'], lambda d: dict(d, resultado='avance'), actor='executor')
        retorno.publish(self.config, newer)
        trabajo.task_path(self.base, 'toy').write_text(json.dumps(old))
        with self.assertRaisesRegex(boss.Rejected, 'no_retroceder'):retorno.publish(self.config, old)

    def test_remote_immutable_evidence_not_overwritten(self):
        self.close_fixture(); commit = retorno.publish(self.config, self.row)
        path = '04-operacion-agentes/evidencias/toy/entrega.md'
        file = self.base / path; file.write_text('other bytes')
        data = trabajo.read_task(self.base, 'toy')
        data['evidencias'] = [trabajo.evidence(self.base, path, True)]
        data['revision'] += 1
        trabajo.task_path(self.base, 'toy').write_text(json.dumps(data))
        with self.assertRaisesRegex(boss.Rejected, 'inmutable'):retorno.publish(self.config, data)

    def test_http_after_publication_and_deduplicated(self):
        self.close_fixture(); self.secret()
        sender = Mock(return_value=True)
        result = retorno.deliver(self.config, 'toy', sender=sender)
        self.assertEqual(result['estado_envio'], 'recibido_http'); self.assertFalse(result['acuse_boss'])
        self.assertEqual(set(sender.call_args.args[1]), {'id', 'revision', 'estado', 'commit'})
        commit = sender.call_args.args[1]['commit']
        self.assertEqual(self.fixture.git('ls-remote', 'origin', 'refs/heads/master').split()[0], commit)
        retorno.deliver(self.config, 'toy', sender=sender)
        self.assertEqual(sender.call_count, 1)

    def test_missing_config_never_sends(self):
        self.close_fixture(); sender = Mock()
        self.assertEqual(retorno.deliver(self.config, 'toy', sender=sender)['estado_envio'], 'pendiente_configuracion')
        sender.assert_not_called()

    def test_http_timeout_not_retried(self):
        self.close_fixture(); self.secret(); sender = Mock(side_effect=TimeoutError('SECRET'))
        self.assertEqual(retorno.deliver(self.config, 'toy', sender=sender)['estado_envio'], 'incierto')
        retorno.deliver(self.config, 'toy', sender=sender)
        self.assertEqual(sender.call_count, 1)

    def test_changed_snapshot_rejected_before_publish(self):
        self.close_fixture()
        with patch.object(retorno, 'publish') as publish, self.assertRaises(boss.Rejected):
            retorno.deliver(self.config, 'toy', expected_revision=1)
        publish.assert_not_called()

    def test_no_webhook_before_remote_publication(self):
        self.close_fixture(); self.secret(); sender = Mock()
        with patch.object(retorno, 'publish', side_effect=ValueError('private remote')):
            result = retorno.deliver(self.config, 'toy', sender=sender)
        self.assertEqual(result['estado_envio'], 'pendiente_publicacion'); sender.assert_not_called()

    def test_secret_validation_and_redirect_rejection(self):
        for url in ['http://example.invalid/x', 'https://user:pass@example.invalid/x', 'https://example.invalid:444/x']:
            with self.assertRaises(boss.Rejected):retorno.validate_secret({'url': url, 'clave': 'x' * 20})
        self.assertIsNone(retorno.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.invalid'))

    def test_git_fsmonitor_hook_disabled(self):
        marker = self.repo / 'hook-ran'
        self.fixture.git('config', 'core.fsmonitor', 'touch ' + str(marker))
        self.fixture.git('status', '--porcelain')
        self.assertFalse(marker.exists())

    def test_git_filters_disabled_for_status(self):
        marker = self.repo / 'filter-ran'
        script = self.repo / 'filter.sh'
        script.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\ncat\n')
        script.chmod(0o700)
        (self.repo / '.gitattributes').write_text('filtered.txt filter=probe\n')
        target = self.repo / 'filtered.txt'; target.write_text('one\n')
        self.fixture.git('add', '.gitattributes', 'filtered.txt')
        self.fixture.git('commit', '-m', 'filter fixture')
        self.fixture.git('config', 'filter.probe.clean', str(script))
        self.fixture.git('config', 'filter.probe.required', 'true')
        target.write_text('two\n')
        self.fixture.git('status', '--porcelain')
        self.assertFalse(marker.exists())
        # Positive control: raw Git really invokes the same filter.
        subprocess.run(['git', '-C', str(self.repo), 'status', '--porcelain'], check=True, capture_output=True)
        self.assertTrue(marker.exists())

    def test_git_keeps_coordinator_ssh_identity(self):
        self.fixture.git('config', 'core.sshCommand', '/usr/bin/ssh -i dedicated-key')
        self.assertEqual(self.fixture.git('config', '--get', 'core.sshCommand'),
                         '/usr/bin/ssh -i dedicated-key')

    def test_submodule_in_index_rejected_before_status(self):
        commit = self.fixture.git('rev-parse', 'HEAD')
        self.fixture.git('update-index', '--add', '--cacheinfo', '160000,' + commit + ',unreviewed-module')
        with self.assertRaisesRegex(ValueError, 'Submódulos fuera'):
            boss.sessions.validate_retained_worktree(self.repo, commit)

    def test_pause_reloaded_after_lock(self):
        config_path = self.root / 'config.json'
        boss.private_write(config_path, dict(self.config, pausado=True))
        with patch.object(boss.sessions, 'launch') as launch, self.assertRaisesRegex(boss.Rejected, 'puente_pausado'):
            boss.handle(self.config, self.req(), config_path=config_path)
        launch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
