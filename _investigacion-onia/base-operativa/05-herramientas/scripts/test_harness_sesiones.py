"""Tests con Git local y ejecutable sintético. Nunca invocan Codex real ni la red."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import harness
import harness_sesiones as sessions
import trabajo

FAKE = '''#!/usr/bin/env python3
import json, os, re, subprocess, sys, time, uuid
from pathlib import Path
args = sys.argv[1:]
prompt = sys.stdin.read()
sid = args[args.index('resume') + 1] if 'resume' in args else str(uuid.uuid4())
print(json.dumps({'type': 'thread.started', 'thread_id': sid}), flush=True)
time.sleep(float(os.environ.get('HARNESS_TEST_SLEEP', '0.1')))
release = os.environ.get('HARNESS_TEST_RELEASE')
deadline = time.monotonic() + 10
while release and not os.path.exists(release):
    if time.monotonic() > deadline:
        sys.exit(8)
    time.sleep(0.02)
if os.environ.get('HARNESS_TEST_GIT_DELIVERY') and '--output-last-message' not in args:
    ident = os.environ['HARNESS_TEST_GIT_DELIVERY']
    delivery = Path('_investigacion-onia/base-operativa/salidas') / ident
    delivery.parent.mkdir(parents=True, exist_ok=True)
    delivery.write_text('Entrega creada y publicada por el ejecutor falso\\n')
    def git(*arguments):
        return subprocess.check_output(['git', *arguments], text=True).strip()
    branch = git('branch', '--show-current')
    git('add', str(delivery))
    git('commit', '-m', 'entrega autónoma sintética')
    git('push', 'origin', branch)
    print(json.dumps({'type': 'fake.git_published', 'commit': git('rev-parse', 'HEAD')}), flush=True)
if '--output-last-message' in args:
    commit = re.search(r'Commit a revisar: ([0-9a-f]+)', prompt).group(1)
    with open(args[args.index('--output-last-message') + 1], 'w') as f:
        json.dump({'veredicto': os.environ.get('HARNESS_TEST_VERDICT', 'bueno'), 'commit': commit,
                   'criterio': 'Entrega sintética cotejada con aceptación'}, f)
print(json.dumps({'type': 'turn.failed' if os.environ.get('HARNESS_TEST_FAIL') else 'turn.completed'}), flush=True)
sys.exit(7 if os.environ.get('HARNESS_TEST_FAIL') else 0)
'''


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='test-harness-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.base = self.repo / '_investigacion-onia/base-operativa'
        self.base.mkdir(parents=True)
        self.op = self.root / 'operacion'
        data = harness.manifest(harness.BASE)
        paths = [data['reglas'], '04-operacion-agentes/boss-memoria.md', *data['contexto_comun'],
                 *data['archivos_cloud'], *data['skills'].values()]
        for route in data['areas'].values():
            paths.extend(route['contexto'])
        for relative in paths:
            file = self.base / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text('Fixture sintética, sin permisos externos.\n')
        (self.base / '04-operacion-agentes/orquestacion.json').write_text(json.dumps(data))
        (self.repo / 'AGENTS.md').write_text('Fixture de reglas.\n')
        (self.repo / '.gitignore').write_text('.agents/\n**/operacion/\n')
        self.git('init', '-b', 'master')
        self.git('config', 'user.name', 'Test harness')
        self.git('config', 'user.email', 'harness@example.invalid')
        self.git('add', '.')
        self.git('commit', '-m', 'fixture base')
        self.remote = self.root / 'origin.git'
        subprocess.run(['git', 'init', '--bare', str(self.remote)], check=True, capture_output=True)
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-u', 'origin', 'master')
        self.fakebin = self.root / 'fakebin'
        self.fakebin.mkdir()
        fake = self.fakebin / 'codex'
        fake.write_text(FAKE)
        fake.chmod(0o700)
        self.env_patch = patch.dict(os.environ, {'PATH': str(self.fakebin) + ':' + os.environ['PATH']})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

    def git(self, *args, repo=None):
        return sessions.git(repo or self.repo, *args)

    def prepare(self, ident='toy', route=None):
        harness.prepare(self.base, ident, 'desarrollo', 'Probar juguete', 'Archivo sintético', 'Texto comprobable')
        return trabajo.assign(self.base, ident, 1, 'executor', [route or ('salidas/' + ident)])

    def row(self, ident='toy'):
        return trabajo.read_task(self.base, ident)

    def launch(self, ident='toy', dry=False, **kwargs):
        return sessions.launch(self.base, ident, self.op, self.row(ident)['revision'], 'executor',
                               approved=True, dry_run=dry, **kwargs)

    def wait_finished(self, ident='toy'):
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            row = self.row(ident)
            session = row['sesiones'][-1]
            if session['estado'] not in sessions.ACTIVE and not sessions.alive(session):
                return row
            time.sleep(0.05)
        self.fail('El proceso sintético no terminó: ' + str(row))

    def deliver(self, ident='toy', push=True):
        row = self.row(ident)
        worktree = Path(row['sesiones'][0]['worktree'])
        path = worktree / '_investigacion-onia/base-operativa/salidas' / ident
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Entrega de juguete\n')
        self.git('add', str(path), repo=worktree)
        self.git('commit', '-m', 'entrega sintética', repo=worktree)
        commit = self.git('rev-parse', 'HEAD', repo=worktree)
        if push:
            self.git('push', 'origin', 'codex/ws-' + ident, repo=worktree)
        return commit

    def close(self, ident='toy', dry=False):
        return sessions.close(self.base, ident, self.op, self.row(ident)['revision'], 'executor',
                              'Entrega lista', 'Prueba sintética correcta', dry)

    def test_dry_run_entire_flow_and_fourth_rejected_without_subprocess(self):
        for i in range(4):
            self.prepare('toy-' + str(i))
        # Nunca fetch, worktree ni Popen; repo_for se sustituye por la fixture.
        with patch.object(sessions.subprocess, 'Popen') as popen, patch.object(sessions, 'repo_for', return_value=self.repo):
            for i in range(3):
                self.launch('toy-' + str(i), dry=True)
            with self.assertRaisesRegex(ValueError, 'Máximo 3'):
                self.launch('toy-3', dry=True)
            state = sessions.status(self.base, self.op, True)
            self.assertEqual(sum(s['viva_simulada'] for s in state['sesiones']), 3)
            self.close('toy-0', dry=True)
            self.launch('toy-3', dry=True)
            popen.assert_not_called()
        self.assertEqual(self.row('toy-0')['estado'], 'para_revision')
        self.assertFalse((self.op / 'sesiones.tsv').exists())
        self.assertTrue((self.op / 'harness-dry-run/sesiones.tsv').exists())
        self.assertFalse((self.root / 'onia-ws-toy-0').exists())
        with self.assertRaisesRegex(ValueError, 'veredicto bueno'):
            trabajo.accept(self.base, 'toy-0', self.row('toy-0')['revision'], 'reviewer', 'Simulación')

    def test_permission_assignment_revision_and_dry_real_separation(self):
        self.prepare()
        with self.assertRaisesRegex(ValueError, 'sí de Sergio'):
            sessions.launch(self.base, 'toy', self.op, 2, 'executor')
        with self.assertRaisesRegex(ValueError, 'Revisión'):
            sessions.launch(self.base, 'toy', self.op, 1, 'executor', dry_run=True)
        self.launch(dry=True)
        with self.assertRaisesRegex(ValueError, 'No mezclar'):
            self.launch(resume=True)
        with self.assertRaisesRegex(ValueError, 'session id|viva'):
            self.launch(dry=True, resume=True)

    def test_supervised_fake_process_log_tsv_and_resume_same_thread(self):
        self.prepare()
        with patch.dict(os.environ, {'HARNESS_TEST_FAIL': '1'}):
            self.launch()
            row = self.wait_finished()
        first = row['sesiones'][0]
        self.assertEqual(first['rc'], 7)
        self.assertEqual(row['estado'], 'en_espera')
        self.assertTrue(first['pid'])
        self.assertTrue(first['session_id'])
        with self.assertRaisesRegex(ValueError, 'reanudar'):
            self.launch()
        resumed = self.launch(resume=True)
        self.assertIn('resume', resumed['comando'])
        row = self.wait_finished()
        self.assertEqual(row['sesiones'][1]['session_id'], first['session_id'])
        self.assertEqual(row['sesiones'][1]['rc'], 0)
        self.assertEqual(row['sesiones'][1]['git_repo'], first['git_repo'])
        self.assertEqual(row['sesiones'][1]['git_dir'], first['git_dir'])
        state = sessions.status(self.base, self.op)
        self.assertEqual(state['sesiones'][-1]['ultimo_evento'], 'turn.completed')
        self.assertFalse(state['sesiones'][-1]['pid_vivo'])
        self.assertIn(first['session_id'], (self.op / 'sesiones.tsv').read_text())
        self.assertEqual(Path(first['log']).read_text().count('thread.started'), 2)

    def test_close_requires_published_new_commit_preserves_branch_and_review_gates_accept(self):
        self.prepare()
        self.launch()
        self.wait_finished()
        with self.assertRaisesRegex(ValueError, 'commit de entrega'):
            self.close()
        commit = self.deliver(push=False)
        with self.assertRaisesRegex(ValueError, 'no está en origin'):
            self.close()
        self.assertEqual(self.row()['estado'], 'en_curso')
        worktree = Path(self.row()['sesiones'][0]['worktree'])
        self.assertTrue(worktree.exists())
        self.git('push', 'origin', 'codex/ws-toy', repo=worktree)
        self.close()
        self.assertFalse(worktree.exists())
        self.assertEqual(self.git('rev-parse', 'codex/ws-toy', repo=Path(self.row()['sesiones'][0]['git_repo'])), commit)
        with self.assertRaisesRegex(ValueError, 'veredicto bueno'):
            trabajo.accept(self.base, 'toy', self.row()['revision'], 'reviewer', 'Sin revisión')
        with self.assertRaisesRegex(ValueError, 'distinto'):
            self.launch(reviewer='executor')
        self.launch(reviewer='reviewer')
        self.wait_finished()
        row = sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'])['tarea']
        self.assertEqual(row['revision_independiente']['veredicto'], 'bueno')
        self.assertNotEqual(row['sesiones'][0]['session_id'], row['revision_independiente']['session_id'])
        accepted = trabajo.accept(self.base, 'toy', row['revision'], 'reviewer', 'Prueba completa')
        self.assertEqual(accepted['estado'], 'aceptado')

    def test_dirty_and_ignored_worktree_cannot_be_removed(self):
        self.prepare()
        self.launch()
        self.wait_finished()
        self.deliver()
        worktree = Path(self.row()['sesiones'][0]['worktree'])
        (worktree / 'keep.txt').write_text('No borrar')
        with self.assertRaisesRegex(ValueError, 'con cambios'):
            self.close()
        self.assertTrue((worktree / 'keep.txt').exists())
        # Guardar el archivo como entrega antes de probar un ignorado.
        self.git('add', 'keep.txt', repo=worktree)
        self.git('commit', '-m', 'guardar archivo', repo=worktree)
        self.git('push', 'origin', 'codex/ws-toy', repo=worktree)
        ignored = worktree / '.agents/keep.bin'
        ignored.write_bytes(b'preservar')
        with self.assertRaisesRegex(ValueError, 'ignorados'):
            self.close()
        self.assertTrue(ignored.exists())

    def test_live_process_blocks_fourth_close_and_resume(self):
        for i in range(4):
            self.prepare('toy-' + str(i))
        release = self.root / 'release-fake'
        with patch.dict(os.environ, {'HARNESS_TEST_RELEASE': str(release)}):
            for i in range(3):
                self.launch('toy-' + str(i))
            try:
                deadline = time.monotonic() + 5
                while not all(self.row('toy-' + str(i))['sesiones'][0]['session_id'] for i in range(3)):
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(0.02)
                sessions.status(self.base, self.op)
                with self.assertRaisesRegex(ValueError, 'Máximo 3'):
                    self.launch('toy-3')
                with self.assertRaisesRegex(ValueError, 'viva'):
                    self.close('toy-0')
                with self.assertRaisesRegex(ValueError, 'viva'):
                    self.launch('toy-0', resume=True)
            finally:
                release.touch()
                for i in range(3):
                    self.wait_finished('toy-' + str(i))

    def test_cross_checkout_collision_and_index_reconstruction(self):
        self.prepare(route='salidas/shared')
        self.launch(dry=True)
        other = self.root / 'other-base'
        other.mkdir()
        # Copia de fixtures; un segundo coordinador tiene su propio registro canónico.
        import shutil
        for name in ('04-operacion-agentes', '00-MAPA', '05-herramientas', '01-negocio', '06-plataforma', '02-contenido'):
            if (self.base / name).exists():
                shutil.copytree(self.base / name, other / name)
        harness.prepare(other, 'collision', 'desarrollo', 'Objetivo', 'Entrega', 'Criterio')
        trabajo.assign(other, 'collision', 1, 'second', ['SALIDAS/shared/file.txt'])
        with self.assertRaisesRegex(ValueError, 'Colisión'):
            sessions.launch(other, 'collision', self.op, 2, 'second', dry_run=True)
        # TSV atrasado se reconstruye desde la autoridad canónica.
        (self.op / 'harness-dry-run/sesiones.tsv').write_text('\t'.join(sessions.FIELDS) + '\n')
        self.assertEqual(len(sessions.status(self.base, self.op, True)['sesiones']), 1)

    def test_pid_reuse_and_partial_jsonl_fail_closed(self):
        self.assertFalse(sessions.alive({'pid': os.getpid(), 'pid_inicio': 'otro-boot:1'}))
        self.assertTrue(sessions.alive({'pid': os.getpid(), 'pid_inicio': sessions.process_start(os.getpid())}))
        log = self.root / 'partial.jsonl'
        log.write_text('stderr accidental\n{"type":"thread.started","thread_id":"invalid"}\n{"type":"turn.completed"}\n{"type":')
        found = sessions.scan_log(log)
        self.assertEqual(found['ultimo_evento'], 'turn.completed')
        self.assertIsNone(found['session_id'])

    def test_skill_links_idempotent_and_preserve_foreign_files(self):
        first = sessions.link_skills(self.repo, self.base)
        self.assertEqual(first, sessions.link_skills(self.repo, self.base))
        self.assertEqual(len(first['skills']), 9)
        link = self.repo / '.agents/skills' / first['skills'][0]
        link.unlink()  # Sólo fixture propia.
        link.mkdir()
        with self.assertRaisesRegex(ValueError, 'no se reemplazó'):
            sessions.link_skills(self.repo, self.base)
        self.assertTrue(link.is_dir())

    def test_review_bad_stale_and_corrupt_verdict_never_accept(self):
        self.prepare()
        self.launch()
        self.wait_finished()
        self.deliver()
        self.close()
        with patch.dict(os.environ, {'HARNESS_TEST_VERDICT': 'cambios'}):
            self.launch(reviewer='reviewer')
            self.wait_finished()
        row = sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'])['tarea']
        with self.assertRaisesRegex(ValueError, 'veredicto bueno'):
            trabajo.accept(self.base, 'toy', row['revision'], 'reviewer', 'No pasa')
        self.launch(reviewer='reviewer')
        self.wait_finished()
        row = sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'])['tarea']
        original = trabajo.task_path(self.base, 'toy').read_bytes()
        changed = dict(self.row(), resultado='Otra entrega')
        trabajo.atomic_json(trabajo.task_path(self.base, 'toy'), changed)
        with self.assertRaisesRegex(ValueError, 'veredicto bueno'):
            trabajo.accept(self.base, 'toy', changed['revision'], 'reviewer', 'Revisión vieja')
        trabajo.task_path(self.base, 'toy').write_bytes(original)
        (self.base / row['revision_independiente']['evidencia']['archivo']).write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Evidencia cambió'):
            trabajo.accept(self.base, 'toy', row['revision'], 'reviewer', 'Corrupto')

    def test_command_contract_and_readonly_reviewer(self):
        session = {'rol': 'ejecutor', 'worktree': '/tmp/example', 'reanuda': 'abc'}
        cmd = sessions.command(session)
        self.assertEqual(cmd[:7], ['codex', '-a', 'never', '-c', 'sandbox_workspace_write.network_access=true', 'exec', '--json'])
        self.assertLess(cmd.index('--sandbox'), cmd.index('resume'))
        self.assertEqual(cmd[-3:], ['resume', 'abc', '-'])
        session.update(rol='revisor', reanuda=None, schema='/tmp/schema', veredicto_archivo='/tmp/verdict')
        cmd = sessions.command(session)
        self.assertIn('read-only', cmd)
        self.assertIn('--ignore-user-config', cmd)
        self.assertNotIn('resume', cmd)

    def test_parallel_cli_launches_enforce_limit_under_one_lock(self):
        for i in range(4):
            self.prepare('parallel-' + str(i))
        cli = [sys.executable, str(Path(harness.__file__)), '--base', str(self.base), '--operacion', str(self.op)]
        processes = [subprocess.Popen(cli + ['lanzar', 'parallel-' + str(i), '--revision-esperada', '2',
                     '--actor', 'executor', '--dry-run'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                     for i in range(4)]
        outputs = [p.communicate(timeout=15) for p in processes]
        self.assertEqual(sorted(p.returncode for p in processes), [0, 0, 0, 2], outputs)
        self.assertEqual(len(sessions.status(self.base, self.op, True)['sesiones']), 3)

    def test_reconciliation_recovers_abandoned_process_from_log(self):
        self.prepare()
        self.launch()
        self.wait_finished()
        sid = self.row()['sesiones'][0]['session_id']
        def abandoned(row):
            row['sesiones'][0].update(estado='ejecutando', session_id=None, rc=None)
            return row
        sessions.change(self.base, 'toy', abandoned)
        state = sessions.status(self.base, self.op)
        self.assertEqual(state['sesiones'][0]['estado_sesion'], 'interrumpida')
        self.assertEqual(state['sesiones'][0]['session_id'], sid)
        self.assertEqual(self.row()['estado'], 'en_espera')
        self.launch(resume=True)
        self.wait_finished()
        self.assertEqual(self.row()['sesiones'][-1]['session_id'], sid)

    def test_remote_failure_leaves_task_and_worktree_open(self):
        self.prepare()
        self.launch()
        self.wait_finished()
        self.deliver()
        real_git = sessions.git
        def fail_fetch(repo, *args):
            if args[0] == 'fetch':
                raise ValueError('fetch simulado fallido')
            return real_git(repo, *args)
        with patch.object(sessions, 'git', side_effect=fail_fetch):
            with self.assertRaisesRegex(ValueError, 'fetch simulado'):
                self.close()
        self.assertEqual(self.row()['estado'], 'en_curso')
        self.assertTrue(Path(self.row()['sesiones'][0]['worktree']).exists())

    def test_symlinked_operation_and_log_preserve_target(self):
        self.prepare()
        target = self.root / 'target'
        target.mkdir()
        self.op.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'enlace'):
            self.launch(dry=True)
        self.assertEqual(list(target.iterdir()), [])

    def test_explicit_runtime_and_chatgpt_auth_do_not_inherit_api_credentials(self):
        self.prepare()
        result = self.launch(dry=True, model='gpt-6.1-sol', effort='low', auth_chatgpt=True)
        command = result['comando']
        self.assertIn('gpt-6.1-sol', command)
        self.assertIn('model_reasoning_effort="low"', command)
        self.assertIn('forced_login_method="chatgpt"', command)
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'fixture', 'CODEX_API_KEY': 'fixture', 'OPENAI_BASE_URL': 'fixture'}):
            child_env = sessions.child_environment(self.row()['sesiones'][0])
            self.assertNotIn('OPENAI_API_KEY', child_env)
            self.assertNotIn('CODEX_API_KEY', child_env)
            self.assertNotIn('OPENAI_BASE_URL', child_env)
            self.assertEqual(os.environ['OPENAI_API_KEY'], 'fixture')
        self.assertEqual(self.row()['sesiones'][0]['esfuerzo'], 'low')

    def test_close_fetches_task_branch_when_clone_tracks_only_master(self):
        self.git('config', '--unset-all', 'remote.origin.fetch')
        self.git('config', '--add', 'remote.origin.fetch', '+refs/heads/master:refs/remotes/origin/master')
        self.prepare()
        self.launch()
        self.wait_finished()
        commit = self.deliver()
        result = self.close()
        self.assertEqual(result['tarea']['cierre']['commit'], commit)
        self.assertIn('origin/codex/ws-toy', result['tarea']['cierre']['ramas_origin'])

    def test_private_owners_and_fake_executor_commit_push_preserve_coordinator(self):
        self.prepare('other')
        self.launch('other')
        other = self.wait_finished('other')['sesiones'][0]
        self.prepare()
        main_refs = self.git('show-ref')
        main_index = (self.repo / '.git/index').read_bytes()
        with patch.dict(os.environ, {'HARNESS_TEST_GIT_DELIVERY': 'toy'}):
            self.launch()
            row = self.wait_finished()
        session = row['sesiones'][0]
        self.assertEqual(session['rc'], 0)
        owner = Path(session['git_repo'])
        self.assertNotEqual(owner, Path(other['git_repo']))
        self.assertNotEqual(owner, self.repo / '.git')
        self.assertEqual(self.git('rev-parse', '--path-format=absolute', '--git-common-dir',
                                  repo=Path(session['worktree'])), str(owner))
        commit = self.git('rev-parse', 'codex/ws-toy', repo=owner)
        self.assertNotEqual(commit, session['commit_base'])
        self.assertEqual(self.git('rev-parse', 'codex/ws-toy', repo=self.remote), commit)
        self.assertEqual(self.git('rev-parse', 'codex/ws-other', repo=Path(other['git_repo'])), other['commit_base'])
        self.assertEqual(self.git('show-ref'), main_refs)
        self.assertEqual((self.repo / '.git/index').read_bytes(), main_index)
        self.assertFalse((owner / 'objects/info/alternates').exists())
        with self.assertRaises(ValueError):
            self.git('rev-parse', '--verify', 'refs/heads/codex/ws-toy')
        self.close()
        self.assertEqual(self.git('rev-parse', 'origin/codex/ws-toy'), commit)
        self.assertEqual(self.git('rev-parse', 'codex/ws-toy', repo=owner), commit)
        self.assertTrue(owner.is_dir())
        self.assertFalse(Path(session['worktree']).exists())

    def test_resume_restores_worktree_from_same_private_owner(self):
        self.prepare()
        self.launch()
        first = self.wait_finished()['sesiones'][0]
        self.git('worktree', 'remove', first['worktree'], repo=Path(first['git_repo']))
        self.launch(resume=True)
        resumed = self.wait_finished()['sesiones'][-1]
        self.assertEqual(resumed['session_id'], first['session_id'])
        self.assertEqual(resumed['git_repo'], first['git_repo'])
        self.assertEqual(resumed['git_dir'], first['git_dir'])
        self.assertEqual(self.git('rev-parse', 'HEAD', repo=Path(first['worktree'])), first['commit_base'])

    def test_private_git_rejects_changed_owner_directory_and_alternates(self):
        self.prepare()
        self.launch()
        session = self.wait_finished()['sesiones'][0]
        owner = Path(session['git_repo'])
        self.assertEqual(sessions.validate_private_git(session, 'toy'), owner)
        for key, value in (('git_repo', str(self.repo / '.git')),
                           ('git_dir', str(self.repo / '.git'))):
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, 'inválidos'):
                sessions.validate_private_git(dict(session, **{key: value}), 'toy')
        alternates = owner / 'objects/info/alternates'
        alternates.write_text(str(self.repo / '.git/objects') + '\n')
        with self.assertRaisesRegex(ValueError, 'otro repositorio'):
            sessions.validate_private_git(session, 'toy')

    def test_private_git_rejects_symlinked_metadata_without_touching_target(self):
        self.prepare()
        self.launch()
        session = self.wait_finished()['sesiones'][0]
        owner = Path(session['git_repo'])
        original_config = (owner / 'config').read_bytes()
        for name in ('config', 'objects', 'refs', 'worktrees'):
            with self.subTest(path=name):
                path = owner / name
                preserved = owner / (name + '.fixture-original')
                path.rename(preserved)
                path.symlink_to(preserved, target_is_directory=preserved.is_dir())
                try:
                    with self.assertRaisesRegex(ValueError, 'enlace'):
                        sessions.validate_private_git(session, 'toy')
                finally:
                    path.unlink()  # Enlace creado exclusivamente en esta fixture.
                    preserved.rename(path)
        self.assertEqual((owner / 'config').read_bytes(), original_config)

    def test_private_git_rejects_worktree_symlink_with_same_basename(self):
        self.prepare()
        self.launch()
        session = self.wait_finished()['sesiones'][0]
        original = Path(session['worktree'])
        alias = self.root / 'alias' / original.name
        alias.parent.mkdir()
        alias.symlink_to(original, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'enlace'):
            sessions.validate_private_git(dict(session, worktree=str(alias)), 'toy')
        self.assertTrue(original.is_dir())

    def test_git_and_child_environment_ignore_inherited_git_redirections(self):
        expected = self.git('rev-parse', 'HEAD')
        injected = {'GIT_DIR': '/fixture/foreign', 'GIT_COMMON_DIR': '/fixture/common',
                    'GIT_WORK_TREE': '/fixture/worktree', 'GIT_INDEX_FILE': '/fixture/index',
                    'GIT_OBJECT_DIRECTORY': '/fixture/objects',
                    'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.bare',
                    'GIT_CONFIG_VALUE_0': 'true'}
        with patch.dict(os.environ, injected):
            self.assertEqual(self.git('rev-parse', 'HEAD'), expected)
            environment = sessions.child_environment({'auth_chatgpt': True})
            self.assertFalse(any(k.startswith('GIT_') for k in environment))
            self.assertEqual(os.environ['GIT_DIR'], injected['GIT_DIR'])
            self.assertEqual(environment['PATH'], os.environ['PATH'])

    def test_private_profile_grants_only_own_metadata_and_reviewer_stays_readonly(self):
        self.prepare()
        self.launch(dry=True)
        session = self.row()['sesiones'][0]
        cmd = sessions.command(session)
        self.assertNotIn('--sandbox', cmd)
        self.assertIn('--ignore-user-config', cmd)
        self.assertIn('default_permissions="harness-git"', cmd)
        self.assertIn('permissions.harness-git.extends=":workspace"', cmd)
        self.assertFalse(any('sandbox_workspace_write' in part for part in cmd))
        permissions = next(part for part in cmd if part.startswith('permissions.harness-git.filesystem='))
        self.assertIn(json.dumps(session['git_repo']) + ' = "write"', permissions)
        self.assertIn(json.dumps(session['git_dir']) + ' = "write"', permissions)
        self.assertEqual(permissions.count(' = "write"'), 2)
        self.assertNotIn(str(self.repo / '.git'), permissions)
        reviewer = dict(session, rol='revisor', schema='/tmp/schema', veredicto_archivo='/tmp/verdict')
        review_cmd = sessions.command(reviewer)
        self.assertIn('read-only', review_cmd)
        self.assertNotIn('default_permissions="harness-git"', review_cmd)
        self.assertFalse(any('permissions.harness-git' in part for part in review_cmd))

    def test_legacy_shared_worktree_can_resume_and_close_without_migration(self):
        self.prepare()
        def legacy_create(repo, root, ident, branch, worktree):
            self.git('fetch', 'origin')
            start = self.git('rev-parse', 'origin/master')
            self.git('worktree', 'add', '-b', branch, str(worktree), start)
            return None, start
        with patch.object(sessions, 'create_private_git', side_effect=legacy_create):
            self.launch()
            first = self.wait_finished()['sesiones'][0]
        self.assertNotIn('git_repo', first)
        resumed = self.launch(resume=True)
        self.assertIn('workspace-write', resumed['comando'])
        last = self.wait_finished()['sesiones'][-1]
        self.assertEqual(last['session_id'], first['session_id'])
        self.assertNotIn('git_repo', last)
        commit = self.deliver()
        self.close()
        self.assertEqual(self.git('rev-parse', 'codex/ws-toy'), commit)
        self.assertFalse(Path(first['worktree']).exists())

    def test_task_schema_rejects_partial_relative_or_reviewer_git_permissions(self):
        self.prepare()
        self.launch(dry=True)
        row = self.row()
        variants = ({'perfil_permisos': 'otro'}, {'rol': 'revisor'},
                    {'git_repo': 'relative.git'}, {'git_dir': 'relative.git'},
                    {'git_repo': None}, {'git_dir': None})
        for fields in variants:
            changed = dict(row, sesiones=[dict(row['sesiones'][0], **fields)])
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                trabajo.validate_sessions(changed)
        legacy = dict(row['sesiones'][0])
        for key in ('git_repo', 'git_dir', 'perfil_permisos'):
            legacy.pop(key)
        trabajo.validate_sessions(dict(row, sesiones=[legacy]))

    def test_cli_dry_run_from_prepare_to_close(self):
        cli = [sys.executable, str(Path(harness.__file__)), '--base', str(self.base), '--operacion', str(self.op)]
        def call(*args, rc=0):
            result = subprocess.run(cli + list(args), capture_output=True, text=True)
            self.assertEqual(result.returncode, rc, result.stdout + result.stderr)
            return json.loads(result.stdout)
        call('preparar', 'cli-toy', '--area', 'desarrollo', '--objetivo', 'Juguete', '--entregable', 'Ficticio', '--aceptacion', 'Simulado')
        call('asignar', 'cli-toy', '--revision-esperada', '1', '--responsable', 'executor', '--ruta', 'salidas/cli-toy')
        call('lanzar', 'cli-toy', '--revision-esperada', '2', '--actor', 'executor', '--dry-run')
        state = call('estado', '--dry-run')
        self.assertTrue(state['sesiones'][0]['viva_simulada'])
        row = call('cerrar', 'cli-toy', '--revision-esperada', '3', '--actor', 'executor', '--resultado', 'Ficticio', '--comprobacion', 'Simulado', '--dry-run')['tarea']
        self.assertEqual(row['estado'], 'para_revision')
        for i in range(4):
            ident = 'cli-' + str(i)
            call('preparar', ident, '--area', 'desarrollo', '--objetivo', 'Juguete', '--entregable', 'Ficticio', '--aceptacion', 'Simulado')
            call('asignar', ident, '--revision-esperada', '1', '--responsable', 'executor', '--ruta', 'salidas/' + ident)
            result = call('lanzar', ident, '--revision-esperada', '2', '--actor', 'executor', '--dry-run', rc=2 if i == 3 else 0)
            if i == 3:
                self.assertIn('Máximo 3', result['error'])


if __name__ == '__main__':
    unittest.main()
