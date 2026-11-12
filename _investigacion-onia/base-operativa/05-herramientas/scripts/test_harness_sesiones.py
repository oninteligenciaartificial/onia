"""Tests con Git local y ejecutable sintético. Nunca invocan Codex real ni la red."""
import json
import os
import signal
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


INTERRUPTION_FAKE = r'''#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, time, uuid
from pathlib import Path
args = sys.argv[1:]
sys.stdin.read()
sid = args[args.index('resume') + 1] if 'resume' in args else str(uuid.uuid4())
print(json.dumps({'type': 'thread.started', 'thread_id': sid}), flush=True)
def git(*arguments):
    return subprocess.check_output(['git', '--no-optional-locks', *arguments], text=True).strip()
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
folder = Path('_investigacion-onia/base-operativa/salidas/toy')
checkpoint, note, result = (folder / name for name in ('checkpoint.json', 'nota.txt', 'resultado.json'))
marker = Path(os.environ['HARNESS_TEST_INTERRUPTION_MARKER'])
index = Path(git('rev-parse', '--git-path', 'index'))
if 'resume' not in args:
    folder.mkdir(parents=True)
    checkpoint.write_text('{"valores":[2,3,5]}\n')
    note.write_text('Nota sin seguimiento que debe conservarse.\n')
    git('add', '--', str(checkpoint))
    receipt = {'head': git('rev-parse', 'HEAD'), 'index': sha(index),
               'checkpoint': sha(checkpoint), 'note': sha(note)}
    temporary = marker.with_suffix('.tmp')
    temporary.write_text(json.dumps(receipt))
    os.replace(temporary, marker)
    # Espera acotada, sin hijos lectores ni operaciones Git en curso.
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        time.sleep(0.02)
    sys.exit(8)
receipt = json.loads(marker.read_text())
assert sha(checkpoint) == receipt['checkpoint'] and sha(note) == receipt['note']
branch = git('branch', '--show-current')
if git('rev-parse', 'HEAD') == receipt['head']:
    assert sha(index) == receipt['index'], 'Se alteró el índice antes de retomar'
    values = json.loads(checkpoint.read_text())['valores']
    result.write_text(json.dumps({'total': sum(values), 'cantidad': len(values)}) + '\n')
    git('add', '--', str(checkpoint), str(note), str(result))
    git('commit', '-m', 'entrega única tras interrupción sintética')
    git('push', 'origin', 'HEAD:refs/heads/' + branch)
    print(json.dumps({'type': 'fake.resumed_and_published'}), flush=True)
else:
    assert json.loads(result.read_text()) == {'total': 10, 'cantidad': 3}
    print(json.dumps({'type': 'fake.already_published'}), flush=True)
head = git('rev-parse', 'HEAD')
assert git('rev-list', '--count', receipt['head'] + '..HEAD') == '1'
assert git('ls-remote', 'origin', 'refs/heads/' + branch).split()[0] == head
assert not git('status', '--porcelain')
print(json.dumps({'type': 'turn.completed'}), flush=True)
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
            # Los ensayos siguientes alteran archivos/estado como si no quedara
            # ningún proceso. alive() ya separa sesión de supervisor publicando.
            supervisor_alive = (session.get('supervisor_pid') and session.get('supervisor_inicio')
                                and sessions.process_start(session['supervisor_pid']) == session['supervisor_inicio'])
            if session['estado'] not in sessions.ACTIVE and not sessions.alive(session) and not supervisor_alive:
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

    def close(self, ident='toy', dry=False, *, retain_worktree=False):
        return sessions.close(self.base, ident, self.op, self.row(ident)['revision'], 'executor',
                              'Entrega lista', 'Prueba sintética correcta', dry,
                              retain_worktree=retain_worktree)

    def test_trial_four_synthetic_launches_fifth_blocked_and_sigterm(self):
        import harness_ensayo as trial
        from test_harness_ensayo import install_trial, write_state
        ids = ['ensayo-' + str(i) for i in range(5)]
        for ident in ids:
            self.prepare(ident)
        value = install_trial(self.op, self.base, ids)
        release = self.root / 'release-trial'
        try:
            with patch.dict(os.environ, {'HARNESS_TEST_RELEASE': str(release)}):
                for ident in ids[:4]:
                    write_state(self.op, value)
                    self.launch(ident, model='gpt-6.1-sol', effort='high', auth_chatgpt=True, subagents=0)
                with self.assertRaisesRegex(ValueError, 'Máximo 4'):
                    self.launch(ids[4], model='gpt-6.1-sol', effort='high', auth_chatgpt=True)
                self.assertEqual(len(trial.live_sessions(sessions.indexed_rows(self.op, self.base))), 4)
                for ident in ids[:4]:
                    self.assertEqual(self.row(ident)['sesiones'][-1]['ensayo_sha256'], trial.digest(value))
                result = trial.stop(self.op)
                self.assertEqual(result['estado'], 'parado')
        finally:
            release.touch()
            for ident in ids[:4]:
                if self.row(ident).get('sesiones'):
                    self.wait_finished(ident)
        self.assertTrue(all(Path(self.row(i)['sesiones'][0]['worktree']).exists() for i in ids[:4]))
        self.assertTrue(all(Path(self.row(i)['sesiones'][0]['log']).exists() for i in ids[:4]))

    def test_trial_enforces_model_auth_and_no_children_before_creating_worktree(self):
        from test_harness_ensayo import install_trial
        self.prepare()
        install_trial(self.op, self.base, ['toy'])
        for options in [{'model': 'otro', 'effort': 'high', 'auth_chatgpt': True},
                        {'model': 'gpt-6.1-sol', 'effort': 'low', 'auth_chatgpt': True},
                        {'model': 'gpt-6.1-sol', 'effort': 'high', 'subagents': 1, 'auth_chatgpt': True},
                        {'model': 'gpt-6.1-sol', 'effort': 'high'}]:
            with self.subTest(options=options), self.assertRaisesRegex(ValueError, 'Sol high'):
                self.launch(**options)
        self.assertFalse((self.op / 'git/toy.git').exists())

    def test_trial_revalidates_after_git_and_before_registration(self):
        import harness_ensayo as trial
        from test_harness_ensayo import install_trial
        self.prepare()
        install_trial(self.op, self.base, ['toy'])
        with patch.object(trial, 'revalidate', side_effect=ValueError('ensayo_STOP')), \
                patch.object(sessions.subprocess, 'Popen') as popen:
            # Reutiliza el camino simulado sólo para evitar Git en esta comprobación.
            with patch.object(sessions, 'repo_for', return_value=self.repo), \
                    patch.object(sessions, 'create_private_git', return_value=(self.op / 'git/toy.git', 'a' * 40)), \
                    patch.object(sessions, 'validate_private_git'), patch.object(sessions, 'link_skills'):
                with self.assertRaisesRegex(ValueError, 'STOP'):
                    self.launch(model='gpt-6.1-sol', effort='high', auth_chatgpt=True)
            self.assertFalse(self.row().get('sesiones'))
            popen.assert_not_called()

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

    def test_sigterm_resume_preserves_staged_untracked_and_single_publication(self):
        self.prepare()
        (self.fakebin / 'codex').write_text(INTERRUPTION_FAKE)
        marker = self.root / 'checkpoint-ready.json'
        with patch.dict(os.environ, {'HARNESS_TEST_INTERRUPTION_MARKER': str(marker)}):
            self.launch()
            # Siempre terminar sólo el proceso de esta fixture si falla una aserción.
            def finish_fixture():
                session = self.row()['sesiones'][-1]
                if (session['pid'] and session['pid_inicio'] and
                        sessions.process_start(session['pid']) == session['pid_inicio']):
                    os.kill(session['pid'], signal.SIGTERM)
                self.wait_finished()
            self.addCleanup(finish_fixture)
            deadline = time.monotonic() + 6
            while not (marker.exists() and self.row()['sesiones'][0]['session_id']):
                self.assertLess(time.monotonic(), deadline, 'El fake no preparó su checkpoint')
                time.sleep(0.02)
            first = self.row()['sesiones'][0]
            worktree = Path(first['worktree'])
            folder = worktree / '_investigacion-onia/base-operativa/salidas/toy'
            index = Path(first['git_dir']) / 'index'
            def snapshot():
                return {'checkpoint': (folder / 'checkpoint.json').read_bytes(),
                        'note': (folder / 'nota.txt').read_bytes(), 'index': index.read_bytes(),
                        'head': self.git('rev-parse', 'HEAD', repo=worktree),
                        'staged': self.git('ls-files', '--stage', repo=worktree),
                        'status': self.git('--no-optional-locks', 'status', '--porcelain',
                                           '--untracked-files=all', repo=worktree)}
            before = snapshot()
            prefix = '_investigacion-onia/base-operativa/salidas/toy/'
            self.assertIn('A  ' + prefix + 'checkpoint.json', before['status'])
            self.assertIn('?? ' + prefix + 'nota.txt', before['status'])
            self.assertEqual(before['head'], first['commit_base'])
            self.assertEqual(self.git('rev-list', '--count', first['commit_base'] + '..HEAD', repo=worktree), '0')
            self.assertEqual(sessions.process_start(first['pid']), first['pid_inicio'])
            # No señalar grupos ni al supervisor: únicamente el Codex falso del test.
            os.kill(first['pid'], signal.SIGTERM)
            failed = self.wait_finished()
            self.assertEqual(failed['estado'], 'en_espera')
            self.assertEqual(failed['sesiones'][0]['estado'], 'fallida')
            self.assertEqual(failed['sesiones'][0]['rc'], -signal.SIGTERM)
            self.assertFalse(sessions.alive(failed['sesiones'][0]))
            self.assertNotEqual(sessions.process_start(first['supervisor_pid']), first['supervisor_inicio'])
            self.assertEqual(snapshot(), before)
            resumed = self.launch(resume=True)
            self.assertEqual(resumed['comando'][-3:], ['resume', first['session_id'], '-'])
            row = self.wait_finished()
            self.assertEqual(row['sesiones'][1]['rc'], 0)
            self.assertEqual(row['sesiones'][1]['session_id'], first['session_id'])
            self.assertEqual((folder / 'checkpoint.json').read_bytes(), before['checkpoint'])
            self.assertEqual((folder / 'nota.txt').read_bytes(), before['note'])
            self.assertEqual(json.loads((folder / 'resultado.json').read_text()), {'total': 10, 'cantidad': 3})
            commit = self.git('rev-parse', 'HEAD', repo=worktree)
            self.assertNotEqual(commit, before['head'])
            self.assertEqual(self.git('rev-parse', first['rama'], repo=self.remote), commit)
            self.assertEqual(self.git('rev-list', '--count', first['commit_base'] + '..HEAD', repo=worktree), '1')
            published_index = index.read_bytes()
            # Un tercer turno comprueba una entrega ya publicada sin crear otro commit.
            self.launch(resume=True)
            row = self.wait_finished()
            self.assertEqual(row['sesiones'][2]['rc'], 0)
            self.assertEqual(row['sesiones'][2]['session_id'], first['session_id'])
            self.assertEqual(self.git('rev-parse', 'HEAD', repo=worktree), commit)
            self.assertEqual(self.git('rev-parse', first['rama'], repo=self.remote), commit)
            self.assertEqual(self.git('rev-list', '--count', first['commit_base'] + '..HEAD', repo=worktree), '1')
            self.assertEqual(index.read_bytes(), published_index)
            events = [json.loads(line) for line in Path(first['log']).read_text().splitlines()]
            self.assertEqual([e['thread_id'] for e in events if e['type'] == 'thread.started'],
                             [first['session_id']] * 3)
            self.assertEqual(sum(e['type'] == 'fake.resumed_and_published' for e in events), 1)
            self.assertEqual(sum(e['type'] == 'fake.already_published' for e in events), 1)

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

    def test_preserve_executor_and_reviewer_worktrees_without_sharing_private_files(self):
        self.prepare()
        self.launch()
        executor = self.wait_finished()['sesiones'][0]
        commit = self.deliver()
        worktree = Path(executor['worktree'])
        local_files = {'captura.bin': b'captura privada', '.agents/cache.bin': b'cache privada'}
        for name, content in local_files.items():
            (worktree / name).write_bytes(content)

        # Ambos estados del índice deben impedir el cierre, aunque se conserve el checkout.
        (worktree / '.gitignore').write_text('cambio sin publicar\n')
        with self.assertRaisesRegex(ValueError, 'cambios versionados'):
            self.close(retain_worktree=True)
        self.git('add', '.gitignore', repo=worktree)
        with self.assertRaisesRegex(ValueError, 'cambios versionados'):
            self.close(retain_worktree=True)
        self.assertEqual(self.row()['estado'], 'en_curso')
        self.git('restore', '--source=HEAD', '--staged', '--worktree', '.gitignore', repo=worktree)

        cli = [sys.executable, str(Path(harness.__file__)), '--base', str(self.base), '--operacion', str(self.op)]

        def call(*args):
            completed = subprocess.run(cli + list(args) + ['--revision-esperada', str(self.row()['revision']),
                                                           '--conservar-worktree'], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

        call('cerrar', 'toy', '--actor', 'executor', '--resultado', 'Entrega lista',
             '--comprobacion', 'Prueba sintética correcta')
        closure = self.row()['cierre']
        self.assertEqual(closure['commit'], commit)
        self.assertTrue(closure['worktree_conservado'])
        closure_receipt = (self.base / closure['evidencia']['archivo']).read_text()
        self.assertTrue(json.loads(closure_receipt)['worktree_conservado'])
        for name, content in local_files.items():
            self.assertNotIn(name, closure_receipt)
            self.assertEqual((worktree / name).read_bytes(), content)
        self.assertEqual(self.git('rev-parse', 'HEAD', repo=worktree), commit)

        self.launch(reviewer='reviewer')
        reviewer = self.wait_finished()['sesiones'][-1]
        snapshot = Path(reviewer['worktree'])
        self.assertNotEqual(snapshot, worktree)
        self.assertEqual(self.git('rev-parse', 'HEAD', repo=snapshot), commit)
        for name in local_files:
            self.assertFalse((snapshot / name).exists())
        scratch = snapshot / '.agents/revision.bin'
        scratch.write_bytes(b'archivo local de prueba')
        self.git('switch', '--detach', executor['commit_base'], repo=snapshot)
        with self.assertRaisesRegex(ValueError, 'HEAD del worktree'):
            sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'], retain_worktree=True)
        self.assertIsNone(self.row()['revision_independiente'])
        self.git('switch', '--detach', commit, repo=snapshot)

        call('revisar', 'toy', '--recoger')
        row = self.row()
        review = row['revision_independiente']
        review_receipt = json.loads((self.base / review['evidencia']['archivo']).read_text())
        self.assertTrue(review['worktree_conservado'])
        self.assertTrue(review_receipt['worktree_conservado'])
        sessions.collect_review(self.base, 'toy', self.op, row['revision'])
        self.assertEqual(self.row()['revision'], row['revision'])
        self.assertEqual(scratch.read_bytes(), b'archivo local de prueba')
        self.assertEqual(trabajo.accept(self.base, 'toy', row['revision'], 'reviewer', 'Verificado')['estado'],
                         'aceptado')

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

    def test_subagents_default_off_and_invalid_before_mutation(self):
        self.prepare()
        for value in (-1, 3, True, '1'):
            with self.assertRaisesRegex(ValueError, 'Subagentes'):
                self.launch(dry=True, subagents=value)
        self.assertNotIn('sesiones', self.row())
        cmd = self.launch(dry=True)['comando']
        self.assertIn('agents.enabled=false', cmd)
        self.assertIn('features.multi_agent=false', cmd)
        self.assertIn('features.multi_agent_v2=false', cmd)
        self.assertFalse(any('max_concurrent_threads' in arg for arg in cmd))

    def test_subagents_limit_persists_resume_and_reviewer_is_independent(self):
        self.prepare()
        launched = self.launch(subagents=1, model='gpt-6.1-sol', effort='high')
        self.assertIn('agents.max_concurrent_threads_per_session=1', launched['comando'])
        self.assertIn('agents.max_depth=1', launched['comando'])
        self.assertIn('agents.default_subagent_model="gpt-6.1-sol"', launched['comando'])
        self.assertIn('agents.default_subagent_reasoning_effort="high"', launched['comando'])
        first = self.wait_finished()['sesiones'][-1]
        resumed = self.launch(resume=True)
        self.assertIn('agents.enabled=true', resumed['comando'])
        second = self.wait_finished()['sesiones'][-1]
        self.assertEqual(second['subagentes_maximos'], 1)
        self.assertEqual(second['session_id'], first['session_id'])
        disabled = self.launch(resume=True, subagents=0)
        self.assertIn('agents.enabled=false', disabled['comando'])
        self.assertEqual(self.wait_finished()['sesiones'][-1]['subagentes_maximos'], 0)
        self.deliver()
        self.close()
        with self.assertRaisesRegex(ValueError, 'no delega'):
            self.launch(reviewer='reviewer', subagents=1)
        reviewed = self.launch(reviewer='reviewer', model='gpt-6.1-sol', effort='ultra')
        self.assertIn('agents.enabled=false', reviewed['comando'])
        self.assertIn('model_reasoning_effort="ultra"', reviewed['comando'])
        self.wait_finished()
        self.assertEqual(self.row()['sesiones'][-1]['subagentes_maximos'], 0)
        invalid = json.loads(json.dumps(self.row()))
        invalid['sesiones'][-1]['subagentes_maximos'] = 1
        with self.assertRaisesRegex(ValueError, 'subagentes'):
            trabajo.validate_sessions(invalid)

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

    def test_changes_review_reaches_resumed_executor_after_worktree_removed(self):
        self.prepare()
        self.launch()
        first = self.wait_finished()['sesiones'][0]
        commit = self.deliver()
        self.close()
        with patch.dict(os.environ, {'HARNESS_TEST_VERDICT': 'cambios'}):
            self.launch(reviewer='reviewer')
            self.wait_finished()
        sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'])
        row = self.row()
        self.assertEqual(row['revision_independiente']['veredicto'], 'cambios')
        self.assertFalse(Path(first['worktree']).exists())
        trabajo.update(self.base, 'toy', 'en_curso', 'Corregir según revisión',
                       'Veredicto recogido', 'Añadir detalle faltante', [],
                       revision=row['revision'], actor='executor')
        self.assertIsNone(self.row()['revision_independiente'])
        self.launch(resume=True)
        resumed = self.wait_finished()['sesiones'][-1]
        prompt = Path(resumed['briefing']).read_text()
        self.assertIn('ÚLTIMO VEREDICTO INDEPENDIENTE', prompt)
        self.assertIn('"veredicto": "cambios"', prompt)
        self.assertIn(commit, prompt)
        self.assertIn('Añadir detalle faltante', prompt)
        self.assertEqual(resumed['session_id'], first['session_id'])
        wt = Path(resumed['worktree'])
        (wt / '_investigacion-onia/base-operativa/salidas/toy').write_text('Entrega corregida\n')
        self.git('add', '.', repo=wt)
        self.git('commit', '-m', 'corrección sintética', repo=wt)
        self.git('push', 'origin', 'codex/ws-toy', repo=wt)
        self.close()
        self.launch(reviewer='reviewer-2')
        self.wait_finished()
        sessions.collect_review(self.base, 'toy', self.op, self.row()['revision'])
        accepted = trabajo.accept(self.base, 'toy', self.row()['revision'], 'reviewer-2', 'Corrección comprobada')
        self.assertEqual(accepted['estado'], 'aceptado')
        self.assertEqual(len(accepted['evidencias_revision']), 2)

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
