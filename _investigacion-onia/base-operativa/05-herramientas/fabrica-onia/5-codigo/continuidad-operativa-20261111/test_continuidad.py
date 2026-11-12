"""Pruebas sin Codex real: mismas API, journals, cupos y Git local del harness."""
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import uuid

import continuidad as app
import instalar

REPO = app.HERE.parents[5]
sys.path.insert(0, str(REPO / app.SCRIPTS))
import harness_lote as lote
import harness_sesiones as sessions
import test_harness_lote as fixtures


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = {}
        self.entries = []
        for n, ident in enumerate(('primero', 'segundo')):
            fixture = fixtures.BatchTests()
            fixture.setUp()
            self.addCleanup(fixture.doCleanups)
            fixture.manifest['id'] = ident
            fixture.manifest['tareas'] = fixture.manifest['tareas'][:1]
            fixture.save()
            fixture.adapter.quota = lambda f=fixture: dict(fecha='2026-11-11T20:00:00Z',
                proveedor='openai-chatgpt-incluido', disponible=True, saldo_extra_autorizado=False,
                restante_porcentaje=100, reinicio_mas_proximo=f.now + 3600)
            self.fixtures[ident] = fixture
            self.entries.append(dict(id=ident, orden=n * 10, habilitado=True,
                manifiesto=str(fixture.path), manifiesto_sha256=lote.digest(fixture.manifest),
                operacion=str(fixture.op), observaciones=None, limite_segundos=5))
        self.config = dict(schema=1, lotes=self.entries)

    def step(self, entry):
        f = self.fixtures[entry['id']]
        return app.step(entry, lote, adapter=f.adapter, clock=lambda: f.now)

    def executor(self, command, timeout):
        ident = command[command.index('--uno') + 1]
        return self.step(next(e for e in self.entries if e['id'] == ident))

    def run_once(self):
        return app.run(self.config, REPO, Path('/synthetic/lista.json'), executor=self.executor)

    def test_two_lots_order_and_at_most_one_step_per_lot(self):
        self.config['lotes'] = list(reversed(self.entries))
        report = self.run_once()
        self.assertEqual([e['id'] for e in report['lotes']], ['primero', 'segundo'])
        self.assertEqual(report['avanzados'], 2)
        for f in self.fixtures.values():
            self.assertEqual(f.adapter.calls, [('lanzar', 'uno')])
            f.adapter.rows['uno']['sesiones'][0].update(
                pid=os.getpid(), pid_inicio=sessions.process_start(os.getpid()))
        again = self.run_once()
        self.assertEqual(again['avanzados'], 0)
        self.assertTrue(all(r['resultado'] == 'sin_avance' for r in again['lotes']))
        self.assertIn('esperar sesión existente', json.dumps(again, ensure_ascii=False))
        self.assertTrue(all(len(f.adapter.calls) == 1 for f in self.fixtures.values()))

    def test_stop_expired_disabled_and_hash_mismatch_do_not_starve_other_lot(self):
        first = self.fixtures['primero']
        for mode in ('stop', 'expired', 'disabled', 'hash', 'missing'):
            with self.subTest(mode=mode):
                manifest = deepcopy(first.manifest)
                if mode == 'stop':
                    first.dispatcher().revoke('Parada sintética')
                elif mode == 'expired':
                    first.manifest['hasta'] = '2026-11-11T19:59:00Z'
                    first.save()
                    self.entries[0]['manifiesto_sha256'] = lote.digest(first.manifest)
                elif mode == 'disabled':
                    self.entries[0]['habilitado'] = False
                elif mode == 'hash':
                    self.entries[0]['manifiesto_sha256'] = '0' * 64
                else:
                    self.entries[0]['manifiesto'] += '.missing'
                result = self.run_once()
                self.assertNotEqual(result['lotes'][0]['resultado'], 'avanzado')
                self.assertFalse(first.adapter.calls)
                # El segundo avanza una vez y las demás pasadas ven esa sesión.
                self.assertEqual(len(self.fixtures['segundo'].adapter.calls), 1)
                stop = first.dispatcher().stop
                if stop.exists():
                    stop.unlink()  # sólo fixture sintética, nunca operación real
                first.manifest = manifest
                first.save()
                self.entries[0].update(habilitado=True, manifiesto=str(first.path),
                                       manifiesto_sha256=lote.digest(first.manifest))

    def test_quota_three_global_slots_and_no_secret_in_report(self):
        first = self.fixtures['primero']
        original = first.adapter.quota
        first.adapter.quota = lambda: dict(original(), restante_porcentaje=0)
        result = self.run_once()
        self.assertEqual(result['avanzados'], 1)
        self.assertIn('cuota_o_autenticacion', json.dumps(result))
        first.adapter.quota = original
        live = dict(pid=os.getpid(), pid_inicio=sessions.process_start(os.getpid()),
                    estado='ejecutando', rol='ejecutor', rutas=['otra'], dry_run=False)
        for n in range(3):
            first.adapter.rows['externa-' + str(n)] = dict(id='externa-' + str(n), sesiones=[live])
        self.assertIn('tres_cupos_ocupados', json.dumps(self.run_once()))
        first.adapter.capacity = lambda *a: (_ for _ in ()).throw(ValueError('secret://TOKEN_PRIVADO'))
        result = self.run_once()
        self.assertNotIn('TOKEN_PRIVADO', json.dumps(result))
        self.assertIn('control_canonico', json.dumps(result))
        self.assertFalse(first.adapter.calls)

    def test_crash_after_effect_reuses_journal_sid_without_duplicate(self):
        first = self.fixtures['primero']
        first.adapter.after = lambda: (_ for _ in ()).throw(fixtures.Crash())
        with self.assertRaises(fixtures.Crash):
            self.step(self.entries[0])
        sid = first.adapter.rows['uno']['sesiones'][0]['session_id']
        first.adapter.after = None
        result = self.run_once()
        self.assertEqual(result['lotes'][0]['resultado'], 'sin_avance')
        self.assertEqual(first.adapter.calls, [('lanzar', 'uno')])
        self.assertEqual(first.adapter.rows['uno']['sesiones'][0]['session_id'], sid)
        self.assertTrue(any(e.get('recuperado') for e in first.dispatcher().events()))

    def test_fresh_observations_close_then_collect_once_stale_waits(self):
        f = self.fixtures['primero']
        self.step(self.entries[0])
        f.finish()
        result = self.step(self.entries[0])
        self.assertIn('evidencia_coordinadora', json.dumps(result))
        self.entries[0]['observaciones'] = str(f.observation_path)
        f.save(cierres={'uno': dict(commit='b' * 40, verificacion='correcta',
                                   resultado='Artefacto esperado cotejado', comprobacion='Fixture exacta')})
        obs = json.loads(f.observation_path.read_text())
        obs['fecha'] = '2026-11-11T19:55:00Z'
        f.observation_path.write_text(json.dumps(obs))
        self.assertEqual(self.step(self.entries[0])['resultado'], 'sin_avance')
        obs['fecha'] = '2026-11-11T20:00:00Z'
        f.observation_path.write_text(json.dumps(obs))
        self.assertEqual(self.step(self.entries[0])['avances'][0]['op'], 'cerrar')
        self.assertEqual(self.step(self.entries[0])['avances'][0]['op'], 'revisar')
        f.finish()
        self.assertEqual(self.step(self.entries[0])['avances'][0]['op'], 'recoger')
        again = self.step(self.entries[0])
        self.assertEqual(again['resultado'], 'sin_avance')
        self.assertIn('decidir aceptación', json.dumps(again, ensure_ascii=False))
        self.assertEqual(f.adapter.calls.count(('cerrar', 'uno')), 1)
        self.assertEqual(f.adapter.calls.count(('recoger', 'uno')), 1)
        self.assertNotIn(('aceptar', 'uno'), f.adapter.calls)

    def test_timeout_and_worker_error_continue_other_lots(self):
        def execute(command, timeout):
            if command[command.index('--uno') + 1] == 'primero':
                return app.execute([sys.executable, '-c', 'import time; time.sleep(10)'], 0.05)
            return self.executor(command, timeout)
        report = app.run(self.config, REPO, Path('/synthetic/lista.json'), executor=execute)
        self.assertEqual(report['lotes'][0]['resultado'], 'limite_de_tiempo')
        self.assertEqual(report['lotes'][1]['resultado'], 'avanzado')
        self.assertEqual(app.execute([sys.executable, '-c', 'print("SECRET"); exit(1)'], 2)['fallo'],
                         'worker_fallido')
        self.assertEqual(app.run(dict(schema=1, lotes=[]), REPO, Path('/x'))['resultado'], 'sin_lotes')

    def test_disappearing_process_blocks_only_one_pass_not_other_lots(self):
        f = self.fixtures['primero']
        original = f.adapter.reconcile
        f.adapter.reconcile = lambda *a: (_ for _ in ()).throw(ProcessLookupError('proceso terminado'))
        result = self.run_once()
        self.assertEqual(result['lotes'][0]['resultado'], 'bloqueado')
        self.assertEqual(result['lotes'][1]['resultado'], 'avanzado')
        self.assertFalse(f.dispatcher().events())
        f.adapter.reconcile = original
        self.assertEqual(self.run_once()['lotes'][0]['resultado'], 'avanzado')
        self.assertEqual(f.adapter.calls, [('lanzar', 'uno')])

    def test_list_contract_rejects_duplicate_wrong_operation_and_unbounded(self):
        entry = deepcopy(self.entries[0])
        entry['operacion'] = str(self.fixtures['primero'].op)
        config = dict(schema=1, lotes=[entry])
        path = self.fixtures['primero'].root / 'lista.json'
        def check(value):
            path.write_text(json.dumps(value))
            return app.load(path, operation=entry['operacion'])
        self.assertEqual(check(config), config)
        for mutation in (dict(lotes=[entry, entry]),
                         dict(lotes=[dict(entry, limite_segundos=121)]),
                         dict(lotes=[dict(entry, orden=True)]),
                         dict(lotes=[dict(entry, operacion='/other')]),
                         dict(lotes=[dict(entry, manifiesto_sha256='bad')])):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check(dict(config, **mutation))
        too_long = [dict(entry, id='lote-' + str(n), orden=n, manifiesto='/tmp/lote-' + str(n),
                         limite_segundos=120) for n in range(5)]
        with self.assertRaises(ValueError):
            check(dict(config, lotes=too_long))

    def test_worker_rejects_changed_list_before_opening_manifest(self):
        entry = dict(self.entries[0], operacion=str(Path.home() / 'operacion'),
                     manifiesto='/tmp/manifiesto-inexistente-para-esta-prueba.json')
        path = self.fixtures['primero'].root / 'lista.json'
        path.write_text(json.dumps(dict(schema=1, lotes=[entry])))
        result = subprocess.run([sys.executable, '-B', str(app.HERE / 'continuidad.py'),
            '--repo', str(REPO), '--lista', str(path), '--uno', entry['id'],
            '--lista-sha256', '0' * 64], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['resultado'], 'bloqueado')
        self.assertEqual(result.stderr, '')
        self.assertFalse(self.fixtures['primero'].op.exists())


class NativeRouteTests(unittest.TestCase):
    def test_real_api_local_git_expected_artifact_and_collect(self):
        from test_harness_sesiones import SessionTests
        f = SessionTests()
        f.setUp()
        self.addCleanup(f.doCleanups)
        f.prepare('uno')
        row = f.row('uno')
        adapter = lote.LocalHarness.__new__(lote.LocalHarness)
        adapter.base, adapter.operation, adapter.repo = f.base, f.op, f.repo
        adapter.provider = lambda: True
        now = lote.timestamp('2026-11-11T20:00:00Z')
        adapter.quota = lambda: dict(fecha='2026-11-11T20:00:00Z',
            proveedor='openai-chatgpt-incluido', disponible=True, saldo_extra_autorizado=False,
            restante_porcentaje=100, reinicio_mas_proximo=now + 3600)
        task = dict(id='uno', actor='executor', revisor='reviewer', criterio='Artefacto esperado cotejado',
            rutas=row['asignacion']['rutas'], briefing_sha256=row['briefing']['sha256'],
            operaciones=sorted(lote.OPS), depende_de=[],
            perfiles={r: dict(modelo='gpt-6.1-sol', esfuerzo='high') for r in ('ejecutor', 'revisor')},
            intentos_maximos={'ejecutor': 1, 'revisor': 1})
        manifest = dict(schema=1, id='sintetico', habilitado=True, autorizacion='Sólo prueba',
            desde='2026-11-11T19:00:00Z', hasta='2026-11-11T21:00:00Z', base=str(f.base),
            operacion=str(f.op), repositorio=str(f.repo), proveedor='openai-chatgpt-incluido',
            cuota_minima_porcentaje=1, tareas=[task])
        path, obs = f.root / 'lote.json', f.root / 'obs.json'
        path.write_text(json.dumps(manifest))
        entry = dict(id='sintetico', habilitado=True, operacion=str(f.op), manifiesto=str(path),
                     manifiesto_sha256=lote.digest(manifest), observaciones=None)
        def step():
            return app.step(entry, lote, adapter=adapter, clock=lambda: now)
        self.assertEqual(step()['avances'][0]['op'], 'lanzar')
        f.wait_finished('uno')
        self.assertEqual(step()['resultado'], 'sin_avance')
        commit = f.deliver('uno')
        # deliver crea archivo esperado, commit y push contra un remoto temporal local.
        worktree = Path(f.row('uno')['sesiones'][0]['worktree'])
        self.assertEqual(f.git('show', commit + ':_investigacion-onia/base-operativa/salidas/uno',
                               repo=worktree), 'Entrega de juguete')
        obs.write_text(json.dumps(dict(manifiesto_sha256=lote.digest(manifest),
            fecha='2026-11-11T20:00:00Z', cierres={'uno': dict(commit=commit, verificacion='correcta',
            resultado='Artefacto sintético publicado', comprobacion='Contenido esperado y diff local cotejados')})))
        entry['observaciones'] = str(obs)
        self.assertEqual(step()['avances'][0]['op'], 'cerrar')
        self.assertEqual(step()['avances'][0]['op'], 'revisar')
        f.wait_finished('uno')
        self.assertEqual(step()['avances'][0]['op'], 'recoger')
        self.assertTrue(lote.current_review(f.row('uno')))
        self.assertEqual(step()['resultado'], 'sin_avance')
        self.assertEqual(len(f.row('uno')['sesiones']), 2)


class UnitTests(unittest.TestCase):
    def test_install_cli_is_idempotent_and_empty_pass_is_visible(self):
        with tempfile.TemporaryDirectory(prefix='onia-install-') as folder:
            root = Path(folder)
            config = root / 'lista.json'
            config.write_text('{"schema":1,"lotes":[]}')
            command = [sys.executable, '-B', str(app.HERE / 'instalar.py'), '--repo', str(REPO),
                       '--lista', str(config), '--destino', str(root / 'units'), '--codex-bin', '/usr/bin']
            for _ in range(2):
                installed = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(len(list((root / 'units').iterdir())), 2)
            passed = subprocess.run([sys.executable, '-B', str(app.HERE / 'continuidad.py'),
                '--repo', str(REPO), '--lista', str(config)], capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertEqual(json.loads(passed.stdout), {'resultado': 'sin_lotes', 'avanzados': 0})
            # Rechazar sobreescritura accidental de una unidad existente diferente.
            (root / 'units/onia-continuidad.timer').write_text('unidad ajena')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_transient_user_service_preserves_synthetic_supervisor(self):
        probe = subprocess.run(['systemctl', '--user', 'show-environment'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if probe.returncode:
            self.skipTest('Sin acceso a systemd de usuario; verify se prueba por separado.')
        with tempfile.TemporaryDirectory(prefix='onia-unit-') as folder:
            marker = Path(folder) / 'supervisor-finalizado'
            child_code = 'import time,pathlib; time.sleep(0.4); pathlib.Path(' + repr(str(marker)) + ').write_text("ok")'
            parent_code = 'import subprocess,sys; subprocess.Popen([sys.executable,"-c",' + repr(child_code) + '],start_new_session=True)'
            unit = 'onia-continuidad-prueba-' + uuid.uuid4().hex[:12]
            try:
                result = subprocess.run(['systemd-run', '--user', '--quiet', '--wait', '--collect',
                    '--unit=' + unit, '--property=Type=oneshot', '--property=KillMode=process',
                    sys.executable, '-c', parent_code], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                deadline = time.monotonic() + 3
                while not marker.exists() and time.monotonic() < deadline:
                    time.sleep(0.03)
                self.assertEqual(marker.read_text(), 'ok')
            finally:
                # Sólo la unidad transitoria de esta prueba; nunca servicios ajenos.
                subprocess.run(['systemctl', '--user', 'stop', unit],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_units_render_reproducibly_and_are_verified_without_activation(self):
        units = instalar.render(REPO, Path('/tmp/lista.json'), Path('/usr/bin'))
        self.assertEqual(units, instalar.render(REPO, Path('/tmp/lista.json'), Path('/usr/bin')))
        with tempfile.TemporaryDirectory() as folder:
            paths = []
            for name, body in units.items():
                path = Path(folder) / name
                path.write_text(body)
                paths.append(str(path))
            result = subprocess.run(['systemd-analyze', '--user', 'verify', *paths],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Persistent=true', units['onia-continuidad.timer'])
        self.assertIn('KillMode=process', units['onia-continuidad.service'])
        with self.assertRaises(ValueError):
            instalar.render(REPO, Path('/tmp/$UNSAFE'), Path('/usr/bin'))


if __name__ == '__main__':
    unittest.main()
