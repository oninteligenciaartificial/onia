"""Dobles de fallos y prueba de contrato con Git local y ejecutable sintético."""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import uuid

import harness_lote as lote
import harness_sesiones as sessions
import trabajo


class Crash(BaseException):
    pass


class MemoryHarness:
    def __init__(self, rows, operation):
        self.rows = rows
        self.operation = operation
        self.calls = []
        self.provider_ok = True
        self.commits = set()
        self.failure = None
        self.before = None
        self.after = None

    def row(self, ident):
        return deepcopy(self.rows[ident])

    def reconcile(self, ids):
        pass

    def reservations(self):
        return list(self.rows.values())

    def integrated(self, commit, refresh=False):
        return commit in self.commits

    def provider(self):
        return self.provider_ok

    def capacity(self, task, role):
        sessions.check_capacity([(None, r) for r in self.rows.values()], task['id'], None,
                                task['rutas'], role)

    def invoke(self, op, task, row, observation):
        if self.before:
            self.before()
        self.calls.append((op, task['id']))
        if self.failure:
            raise self.failure
        current = self.rows[task['id']]
        trabajo.expected(current, row['revision'])
        if op in lote.DISPATCH:
            role = 'revisor' if op == 'revisar' else 'ejecutor'
            sessions.check_capacity([(None, r) for r in self.rows.values()], task['id'], None,
                                    task['rutas'], role)
            session = dict(intento=len(current['sesiones']) + 1, rol=role,
                           session_id=str(uuid.uuid4()), estado='ejecutando', rc=None,
                           responsable=task['revisor'] if role == 'revisor' else task['actor'],
                           operacion=str(self.operation), dry_run=False,
                           subagentes_maximos=0 if role == 'revisor' else task.get('subagentes_maximos', 0),
                           auth_chatgpt=True,
                           modelo=task['perfiles'][role]['modelo'], esfuerzo=task['perfiles'][role]['esfuerzo'],
                           rutas=task['rutas'], commit_base=(current.get('cierre') or {}).get('commit', 'a' * 40),
                           entrega_sha256=trabajo.delivery_digest(current) if role == 'revisor' else None,
                           reanuda=task.get('reanudar_sid') if op == 'reanudar' else None)
            if op == 'reanudar':
                session['session_id'] = task['reanudar_sid']
            current['sesiones'].append(session)
            if role == 'ejecutor':
                current['estado'] = 'en_curso'
        elif op == 'cerrar':
            current['cierre'] = {'commit': observation['cierres'][task['id']]['commit']}
            current['estado'] = 'para_revision'
        else:
            session = current['sesiones'][-1]
            current['revision_independiente'] = dict(veredicto='bueno', commit=current['cierre']['commit'],
                session_id=session['session_id'], revisor=session['responsable'],
                entrega_sha256=trabajo.delivery_digest(current))
        current['revision'] += 1
        if self.after:
            self.after()


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='test-lote-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.op = self.root / 'operacion'
        self.base = self.root / 'repo/base'
        self.base.mkdir(parents=True)
        self.now = lote.timestamp('2026-11-11T20:00:00Z')
        self.manifest = dict(schema=1, id='lote-prueba', habilitado=True,
            autorizacion='Autorización sintética para prueba local',
            desde='2026-11-11T19:00:00Z', hasta='2026-11-11T21:00:00Z',
            base=str(self.base), repositorio=str(self.root / 'repo'), operacion=str(self.op),
            proveedor='openai-chatgpt-incluido', cuota_minima_porcentaje=1,
            tareas=[self.task('uno'), self.task('dos')])
        self.path = self.root / 'lote.json'
        rows = {t['id']: dict(id=t['id'], schema=2, revision=2, estado='preparado',
            objetivo=t['id'], resultado='', comprobacion='', verificacion='pendiente', evidencias=[],
            briefing={'sha256': t['briefing_sha256']},
            asignacion={'responsable': t['actor'], 'rutas': t['rutas']}, sesiones=[])
            for t in self.manifest['tareas']}
        self.adapter = MemoryHarness(rows, self.op)
        self.observation_path = self.root / 'observaciones.json'
        self.save()

    def task(self, ident):
        return dict(id=ident, actor='executor-' + ident, revisor='reviewer-' + ident,
                    criterio='Criterios sintéticos comprobados', briefing_sha256='a' * 64,
                    rutas=['salidas/' + ident], depende_de=[],
                    operaciones=sorted(lote.OPS),
                    perfiles={role: dict(modelo='gpt-6.1-sol', esfuerzo='high') for role in ('ejecutor', 'revisor')},
                    intentos_maximos={'ejecutor': 3, 'revisor': 2})

    def save(self, **observation):
        self.path.write_text(json.dumps(self.manifest))
        obs = dict(manifiesto_sha256=lote.digest(self.manifest), fecha='2026-11-11T20:00:00Z',
                   proveedor='openai-chatgpt-incluido', disponible=True,
                   saldo_extra_autorizado=False, restante_porcentaje=100)
        obs.update(observation)
        self.observation_path.write_text(json.dumps(obs))

    def dispatcher(self, **kwargs):
        return lote.Dispatcher(self.path, self.op, lote.digest(self.manifest),
                               adapter=self.adapter, clock=lambda: self.now, **kwargs)

    def tick(self):
        return self.dispatcher().tick(self.observation_path)

    def finish(self, ident='uno'):
        self.adapter.rows[ident]['sesiones'][-1].update(estado='finalizada', rc=0)

    def review_ready(self, ident='uno'):
        task = next(t for t in self.manifest['tareas'] if t['id'] == ident)
        row = self.adapter.row(ident)
        self.adapter.invoke('lanzar', task, row, {})
        self.finish(ident)
        self.adapter.rows[ident].update(estado='para_revision', cierre={'commit': 'b' * 40})
        self.adapter.calls.clear()

    def assert_blocked(self, result, text):
        self.assertIn(text, json.dumps(result, ensure_ascii=False))

    def test_plan_has_no_effects_or_operation_directory(self):
        before = deepcopy(self.adapter.rows)
        self.assertEqual(len(self.dispatcher().plan()['tareas']), 2)
        self.assertFalse(self.op.exists())
        self.assertEqual(before, self.adapter.rows)

    def test_finite_tick_and_duplicate_executor(self):
        self.tick()
        self.assertEqual(len(self.adapter.calls), 1)
        self.tick()
        self.assertEqual(self.adapter.calls, [('lanzar', 'dos'), ('lanzar', 'uno')])
        self.tick()
        self.assertEqual(len(self.adapter.calls), 2)

    def test_reviewer_has_priority_and_pending_review_is_collected_once(self):
        self.review_ready()
        self.tick()
        self.assertEqual(self.adapter.calls, [('revisar', 'uno')])
        self.finish()
        self.tick()
        self.assertEqual(self.adapter.calls[-1], ('recoger', 'uno'))
        self.tick()
        self.assertEqual(self.adapter.calls.count(('revisar', 'uno')), 1)
        self.assertEqual(self.adapter.calls.count(('recoger', 'uno')), 1)

    def test_finished_executor_requires_attestation_then_closes(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.tick()
        self.finish()
        result = self.tick()
        self.assert_blocked(result, 'comprobación explícita')
        self.save(cierres={'uno': dict(commit='b' * 40, verificacion='correcta',
                                      resultado='Prueba ejecutada', comprobacion='Salida cotejada')})
        self.tick()
        self.assertEqual(self.adapter.calls[-1], ('cerrar', 'uno'))

    def test_stale_review_blocks_only_its_task(self):
        self.review_ready()
        row = self.adapter.rows['uno']
        row['revision_independiente'] = dict(veredicto='bueno', commit='c' * 40, entrega_sha256='x')
        result = self.tick()
        self.assert_blocked(result, 'Revisión obsoleta')
        self.assertIn(('lanzar', 'dos'), self.adapter.calls)

    def test_route_reservation_blocks_without_process(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.adapter.rows['externa'] = dict(id='externa', asignacion={'rutas': ['salidas/uno/hijo']}, sesiones=[])
        result = self.tick()
        self.assert_blocked(result, 'Conflicto con reserva')
        self.assertNotIn(('lanzar', 'uno'), self.adapter.calls)

    def test_quota_provider_and_stale_observation(self):
        for update in ({'restante_porcentaje': 0}, {'restante_porcentaje': None},
                       {'proveedor': 'api-pagada'}, {'saldo_extra_autorizado': True},
                       {'disponible': False}, {'fecha': '2026-11-11T19:00:00Z'},
                       {'fecha': '2026-11-11T20:00:01Z'}):
            with self.subTest(update=update):
                self.save(**update)
                self.tick()
                self.assertFalse(self.adapter.calls)
        self.save()
        self.adapter.provider_ok = False
        self.assert_blocked(self.tick(), 'Autenticación ChatGPT')
        self.assertFalse(self.adapter.calls)

    def test_quota_expires_during_provider_check_does_not_dispatch(self):
        self.now += 115
        def slow_provider():
            self.now += 10
            return True
        self.adapter.provider = slow_provider
        result = self.tick()
        self.assertIn('caducada', json.dumps(result, ensure_ascii=False))
        self.assertFalse(self.adapter.calls)

    def test_failed_executor_with_verified_delivery_closes_without_retry(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.tick()
        row = self.adapter.rows['uno']
        row['sesiones'][-1].update(estado='fallida', rc=1)
        self.adapter.calls.clear()
        self.save(cierres={'uno': dict(commit='b' * 40, verificacion='correcta',
                  resultado='Entrega publicada antes del fallo', comprobacion='Commit comprobado')})
        self.tick()
        self.assertEqual(self.adapter.calls, [('cerrar', 'uno')])
        self.assertEqual(row['estado'], 'para_revision')
        self.assertEqual(len(row['sesiones']), 1)

    def test_missing_quota_still_allows_collect(self):
        self.review_ready()
        self.tick()
        self.finish()
        self.save(restante_porcentaje=0)
        self.tick()
        self.assertEqual(self.adapter.calls[-1], ('recoger', 'uno'))

    def test_recurring_tick_refreshes_quota_and_ignores_stale_attestation(self):
        self.save(fecha='2026-11-11T19:00:00Z', restante_porcentaje=100,
                  cierres={'uno': dict(commit='b' * 40, verificacion='correcta')})
        readings = []

        def quota():
            readings.append(self.now)
            return lote.codex_quota({'rateLimits': {'limitId': 'codex', 'primary': {
                'usedPercent': 95 if len(readings) == 1 else 100, 'resetsAt': int(self.now) + 60}}}, self.now)

        self.adapter.quota = quota
        first = self.dispatcher().tick(self.observation_path, refresh_quota=True)
        self.assertEqual(first['resultado'], 'avanzado')
        intent = next(e for e in self.dispatcher().events() if e['tipo'] == 'intencion')
        self.assertEqual(intent['cuota']['restante_porcentaje'], 5)
        self.assertEqual(intent['cuota']['fuente'], 'account/rateLimits/read')
        self.now += 30
        second = self.dispatcher().tick(self.observation_path, refresh_quota=True)
        self.assert_blocked(second, 'Cuota insuficiente')
        self.assertEqual(len(self.adapter.calls), 1)
        self.assertEqual(len(readings), 2)

    def test_recurring_collect_without_quota_or_observation_file(self):
        self.review_ready()
        self.tick()
        self.finish()
        self.adapter.quota = lambda: self.fail('Recoger no necesita consulta al proveedor.')
        self.dispatcher().tick(refresh_quota=True)
        self.assertEqual(self.adapter.calls[-1], ('recoger', 'uno'))

    def test_live_quota_reset_during_preflight_blocks_launch(self):
        self.adapter.quota = lambda: lote.codex_quota({'rateLimits': {'limitId': 'codex',
            'primary': {'usedPercent': 50, 'resetsAt': int(self.now) + 1}}}, self.now)

        def slow_provider():
            self.now += 2
            return True

        self.adapter.provider = slow_provider
        result = self.dispatcher().tick(refresh_quota=True)
        self.assert_blocked(result, 'Cuota de Codex caducada')
        self.assertFalse(self.adapter.calls)
        self.assertFalse(self.dispatcher().events())

    def test_quota_rpc_uses_only_read_only_methods_and_tightest_window(self):
        binary = self.root / 'codex'
        binary.write_text("""#!/usr/bin/env python3
import json
import os
import sys
import time

assert sys.argv[1:4] == ['app-server', '--listen', 'stdio://']
assert not {'OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL'} & set(os.environ)
for method in ('initialize', 'initialized', 'account/rateLimits/read'):
    request = json.loads(sys.stdin.readline())
    assert request['method'] == method
    if 'id' in request:
        reset = int(time.time()) + 120
        limits = {'limitId': 'codex', 'primary': {'usedPercent': 55, 'resetsAt': reset},
                  'secondary': {'usedPercent': 95, 'resetsAt': reset + 20}}
        result = {'rateLimitsByLimitId': {'codex': limits}} if method != 'initialize' else {}
        print(json.dumps({'id': request['id'], 'result': result}), flush=True)
""")
        binary.chmod(0o700)
        with patch.dict(os.environ, {'PATH': str(self.root) + os.pathsep + os.environ['PATH'],
                                     'OPENAI_API_KEY': 'synthetic', 'CODEX_API_KEY': 'synthetic',
                                     'OPENAI_BASE_URL': 'https://example.invalid'}):
            quota = lote.read_codex_quota()
        self.assertEqual(quota['restante_porcentaje'], 5)
        self.assertTrue(quota['disponible'])
        self.assertFalse(quota['saldo_extra_autorizado'])

    def test_disabled_expired_bad_hash_and_revocation(self):
        self.manifest['habilitado'] = False
        self.save()
        with self.assertRaisesRegex(ValueError, 'deshabilitada'):
            self.tick()
        self.manifest['habilitado'] = True
        self.save()
        self.now += 3600
        with self.assertRaisesRegex(ValueError, 'vigencia'):
            self.tick()
        self.now -= 3600
        dispatcher = self.dispatcher()
        dispatcher.approval = 'f' * 64
        with self.assertRaisesRegex(ValueError, 'SHA256 aprobado'):
            dispatcher.tick(self.observation_path)
        dispatcher.revoke('STOP de prueba')
        with self.assertRaisesRegex(ValueError, 'revocado'):
            self.tick()
        self.assertFalse(self.adapter.calls)

    def test_revocation_during_preflight_stops_effect(self):
        dispatcher = self.dispatcher()
        def revoke():
            dispatcher.revoke('STOP entre consulta y efecto')
            return True
        self.adapter.provider = revoke
        dispatcher.tick(self.observation_path)
        self.assertFalse(self.adapter.calls)

    def test_crash_before_dispatch_is_uncertain_then_explicitly_recoverable(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.adapter.before = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.before = None
        result = self.tick()
        self.assert_blocked(result, 'Intención incierta')
        self.assertNotIn(('lanzar', 'uno'), self.adapter.calls)
        intent = next(e for e in self.dispatcher().events() if e['tipo'] == 'intencion')
        self.resolve(intent)
        self.tick()
        self.assertEqual(self.adapter.calls.count(('lanzar', 'uno')), 1)

    def resolve(self, intent):
        revision = self.adapter.row(intent['id'])['revision']
        path = self.root / 'conciliacion.json'
        path.write_text(json.dumps(dict(clave=intent['clave'], revision=revision,
            sin_efecto_comprobado=True, comprobacion='Procesos, logs y worktree inspeccionados en doble')))
        self.dispatcher().resolve_no_effect(intent['clave'], revision, path)

    def test_crash_after_dispatch_reconciles_sid_without_redispatch(self):
        self.manifest['tareas'] = self.manifest['tareas'][:1]
        self.manifest['tareas'][0]['subagentes_maximos'] = 1
        self.save()
        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        original = self.adapter.calls[0]
        session = deepcopy(self.adapter.rows['uno']['sesiones'][0])
        intent = next(e for e in self.dispatcher().events() if e['tipo'] == 'intencion')
        self.assertEqual(intent['subagentes_maximos'], 1)
        self.assertEqual(session['subagentes_maximos'], 1)
        self.adapter.after = None
        self.tick()
        self.assertEqual(self.adapter.calls.count(original), 1)
        self.assertEqual(self.adapter.rows['uno']['sesiones'], [session])
        effect, = [e for e in self.dispatcher().events() if e['tipo'] == 'efecto']
        self.assertTrue(effect['recuperado'])
        self.assertEqual(effect['clave'], intent['clave'])
        self.assertEqual(effect['despues']['sesiones'][0]['session_id'], session['session_id'])
        self.assertEqual(effect['despues']['sesiones'][0]['intento'], session['intento'])
        self.assertEqual(effect['despues']['sesiones'][0]['subagentes_maximos'], 1)

    def test_recovery_rejects_changed_subagents_even_after_manifest_reapproval(self):
        self.manifest['tareas'] = self.manifest['tareas'][:1]
        self.manifest['tareas'][0]['subagentes_maximos'] = 1
        self.save()
        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.after = None
        self.manifest['tareas'][0]['subagentes_maximos'] = 2
        self.adapter.rows['uno']['sesiones'][0]['subagentes_maximos'] = 2
        self.save()
        self.assert_blocked(self.tick(), 'Intención incierta')
        self.assertEqual(len(self.adapter.calls), 1)
        self.assertFalse(any(e['tipo'] == 'efecto' for e in self.dispatcher().events()))

    def test_legacy_intent_and_session_without_subagents_recover_as_zero(self):
        self.manifest['tareas'] = self.manifest['tareas'][:1]
        self.save()
        dispatcher = self.dispatcher()
        append = dispatcher.append

        def legacy_append(kind, **values):
            values.pop('subagentes_maximos', None)
            return append(kind, **values)

        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with patch.object(dispatcher, 'append', side_effect=legacy_append), self.assertRaises(Crash):
            dispatcher.tick(self.observation_path)
        self.adapter.after = None
        session = self.adapter.rows['uno']['sesiones'][0]
        session.pop('subagentes_maximos')
        # Una intención histórica sin límite nunca acredita un hijo.
        session['subagentes_maximos'] = 1
        self.assert_blocked(self.tick(), 'Intención incierta')
        session.pop('subagentes_maximos')
        self.tick()
        effect, = [e for e in self.dispatcher().events() if e['tipo'] == 'efecto']
        self.assertEqual(effect['despues']['sesiones'][0]['subagentes_maximos'], 0)
        self.assertEqual(len(self.adapter.calls), 1)

    def test_crash_after_collect_reconciles_exact_commit(self):
        self.review_ready()
        self.tick()
        self.finish()
        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.after = None
        self.tick()
        self.assertEqual(self.adapter.calls.count(('recoger', 'uno')), 1)

    def test_unknown_sid_remains_pending_without_duplicate(self):
        self.tick()
        ident = self.adapter.calls[0][1]
        # Reabrir la ventana entre registro del intento y thread.started.
        row = self.adapter.rows[ident]
        row['sesiones'][-1]['session_id'] = None
        events = self.dispatcher().events()
        # Crear otra intención que representa el mismo límite antes del efecto.
        intent = next(e for e in events if e['tipo'] == 'intencion')
        intent = {k: v for k, v in intent.items() if k not in {'tipo', 'fecha', 'anterior', 'manifiesto_sha256'}}
        intent['clave'] = 'sin-sid'
        self.dispatcher().append('intencion', **intent)
        result = self.tick()
        self.assert_blocked(result, 'Intención incierta')
        self.assertEqual(self.adapter.calls.count(('lanzar', ident)), 1)

    def test_two_failures_stop_task_and_allow_independent_progress(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.adapter.failure = ValueError('Fallo sintético antes del efecto')
        self.tick()
        for intent in [e for e in self.dispatcher().events() if e['tipo'] == 'intencion']:
            self.resolve(intent)
        self.tick()
        pending = [e for e in self.dispatcher().events() if e['tipo'] == 'intencion'][-2:]
        for intent in pending:
            self.resolve(intent)
        self.adapter.failure = None
        self.assert_blocked(self.tick(), 'Dos fallos sin progreso')
        self.assertEqual(len(self.adapter.calls), 4)

    def test_invalid_manifest_graph_and_duplicate_ids(self):
        for change in ('duplicate', 'missing', 'cycle', 'profile'):
            manifest = deepcopy(self.manifest)
            if change == 'duplicate':
                manifest['tareas'].append(manifest['tareas'][0])
            elif change == 'missing':
                manifest['tareas'][0]['depende_de'] = [{'id': 'ausente', 'commit': 'a' * 40}]
            elif change == 'cycle':
                for task, other in zip(manifest['tareas'], reversed(manifest['tareas'])):
                    task['depende_de'] = [{'id': other['id'], 'commit': 'a' * 40}]
            else:
                manifest['tareas'][0]['perfiles']['ejecutor']['esfuerzo'] = 'ultra'
            with self.subTest(change=change), self.assertRaises(ValueError):
                lote.validate_manifest(manifest)

    def test_manifest_subagents_are_optional_strict_integers_zero_to_two(self):
        original = deepcopy(self.manifest)
        old_hash = lote.digest(self.manifest)
        lote.validate_manifest(self.manifest)
        self.assertEqual(self.manifest, original)
        self.assertEqual(lote.digest(self.manifest), old_hash)
        for value in (0, 1, 2):
            with self.subTest(valid=value):
                manifest = deepcopy(original)
                manifest['tareas'][0]['subagentes_maximos'] = value
                lote.validate_manifest(manifest)
        for value in (True, False, -1, 3, 1.0, '1', None, [], {}):
            with self.subTest(invalid=value), self.assertRaisesRegex(ValueError, 'Subagentes máximos'):
                manifest = deepcopy(original)
                manifest['tareas'][0]['subagentes_maximos'] = value
                lote.validate_manifest(manifest)

    def test_changed_scope_blocks_only_affected_task(self):
        self.adapter.rows['uno']['briefing']['sha256'] = 'c' * 64
        result = self.tick()
        self.assert_blocked(result, 'Alcance canónico distinto')
        self.assertEqual(self.adapter.calls, [('lanzar', 'dos')])

    def test_lock_and_truncated_journal_preserve_bytes(self):
        with lote.batch_lock(self.op), self.assertRaisesRegex(ValueError, 'activa'):
            self.tick()
        dispatcher = self.dispatcher()
        dispatcher.folder.mkdir(parents=True)
        dispatcher.journal.write_bytes(b'{"tipo":')
        with self.assertRaisesRegex(ValueError, 'truncado'):
            self.tick()
        self.assertEqual(dispatcher.journal.read_bytes(), b'{"tipo":')

    def test_resume_needs_same_sid_and_auxiliary_process_attestation(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.manifest['tareas'][0]['subagentes_maximos'] = 2
        self.save()
        self.tick()
        row = self.adapter.rows['uno']
        row['estado'] = 'en_espera'
        row['sesiones'][-1].update(estado='fallida', rc=1)
        sid = row['sesiones'][-1]['session_id']
        self.assert_blocked(self.tick(), 'Retoma requiere SID')
        self.manifest['tareas'][0]['reanudar_sid'] = sid
        self.save()
        self.assert_blocked(self.tick(), 'procesos auxiliares')
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        self.tick()
        self.assertEqual(self.adapter.calls[-1], ('reanudar', 'uno'))
        self.assertEqual(self.adapter.rows['uno']['sesiones'][-1]['session_id'], sid)
        self.assertEqual([s['subagentes_maximos'] for s in row['sesiones']], [2, 2])
        self.assertTrue(any(e['tipo'] == 'efecto' and e['op'] == 'reanudar'
                            for e in self.dispatcher().events()))

    def test_reviewer_stays_zero_and_recovery_rejects_a_child(self):
        self.manifest['tareas'] = self.manifest['tareas'][:1]
        self.manifest['tareas'][0]['subagentes_maximos'] = 2
        self.save()
        self.review_ready()
        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.after = None
        row = self.adapter.rows['uno']
        self.assertEqual([s['subagentes_maximos'] for s in row['sesiones']], [2, 0])
        intent = next(e for e in self.dispatcher().events() if e['tipo'] == 'intencion')
        self.assertEqual(intent['subagentes_maximos'], 0)
        row['sesiones'][-1]['subagentes_maximos'] = 1
        self.assert_blocked(self.tick(), 'Intención incierta')
        row['sesiones'][-1]['subagentes_maximos'] = 0
        self.tick()
        self.assertEqual(self.adapter.calls.count(('revisar', 'uno')), 1)
        self.assertTrue(any(e['tipo'] == 'efecto' and e['op'] == 'revisar'
                            for e in self.dispatcher().events()))

    def test_changes_review_reopen_resume_reconciles_executor_sid(self):
        self.manifest['tareas'][0]['subagentes_maximos'] = 1
        self.save()
        self.review_ready()
        self.tick()
        self.finish()
        self.tick()
        row = self.adapter.rows['uno']
        row['revision_independiente']['veredicto'] = 'cambios'
        writer = next(s for s in row['sesiones'] if s['rol'] == 'ejecutor')
        writer['estado'] = 'cerrada'
        sid = writer['session_id']
        reviewer_sid = row['sesiones'][-1]['session_id']
        self.assertNotEqual(sid, reviewer_sid)
        row.update(estado='en_espera', cierre=None, revision_independiente=None)
        task = self.manifest['tareas'][0]
        task.update(reanudar_sid=sid, prioridad=10)
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        def crash_after_effect():
            raise Crash()
        self.adapter.after = crash_after_effect
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.after = None
        restored = self.dispatcher()
        unresolved = restored.recover({i: self.adapter.row(i) for i in self.adapter.rows})
        self.assertEqual(unresolved, {})
        resumed = [e for e in restored.events() if e.get('op') == 'reanudar']
        self.assertEqual(resumed[0]['sid'], sid)
        self.assertTrue(any(e['tipo'] == 'efecto' and e.get('recuperado') for e in resumed))
        self.assertEqual(self.adapter.calls.count(('reanudar', 'uno')), 1)
        self.assertEqual(row['sesiones'][-1]['subagentes_maximos'], 1)

    def test_attempt_budget_and_global_three_slots(self):
        self.review_ready()
        self.manifest['tareas'][0]['intentos_maximos']['revisor'] = 1
        self.save()
        self.tick()
        self.finish()
        self.tick()
        # Un veredicto existente impide volver a revisar aunque quede cupo.
        self.tick()
        self.assertEqual(self.adapter.calls.count(('revisar', 'uno')), 1)
        live = dict(pid=os.getpid(), pid_inicio=sessions.process_start(os.getpid()), estado='ejecutando',
                    rol='ejecutor', rutas=['otra'], dry_run=False)
        rows = [(None, dict(id=str(i), sesiones=[live])) for i in range(3)]
        with self.assertRaisesRegex(ValueError, 'Máximo 3'):
            sessions.check_capacity(rows, 'cuarta', None, ['cuarta'], 'revisor')

    def test_exhausted_resume_budget_does_not_create_resume_intent(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.manifest['tareas'][0]['intentos_maximos']['ejecutor'] = 1
        self.save()
        self.tick()
        row = self.adapter.rows['uno']
        row['estado'] = 'en_espera'
        row['sesiones'][-1].update(estado='fallida', rc=1)
        sid = row['sesiones'][-1]['session_id']
        self.manifest['tareas'][0]['reanudar_sid'] = sid
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        self.assert_blocked(self.tick(), 'Presupuesto de intentos agotado')
        self.assertNotIn(('reanudar', 'uno'), self.adapter.calls)

    def test_full_capacity_does_not_record_dispatch_intent(self):
        self.adapter.capacity = lambda task, role: (_ for _ in ()).throw(ValueError('Máximo 3 sesiones vivas'))
        result = self.tick()
        self.assert_blocked(result, 'Máximo 3')
        self.assertFalse(self.adapter.calls)
        self.assertFalse(self.dispatcher().events())

    def test_dependency_needs_exact_review_acceptance_and_remote_integration(self):
        self.review_ready('dos')
        self.adapter.rows['dos']['revision_independiente'] = dict(veredicto='bueno', commit='b' * 40,
            session_id='revisor-distinto', revisor='reviewer-dos',
            entrega_sha256=trabajo.delivery_digest(self.adapter.rows['dos']))
        self.adapter.rows['dos'].update(estado='aceptado', aceptacion={'revisor': 'reviewer-dos'})
        self.manifest['tareas'][0]['depende_de'] = [{'id': 'dos', 'commit': 'b' * 40}]
        self.save()
        self.assert_blocked(self.tick(), 'pendiente en origin/master')
        self.assertFalse(self.adapter.calls)
        self.adapter.commits.add('b' * 40)
        self.tick()
        self.assertEqual(self.adapter.calls, [('lanzar', 'uno')])

    def test_crash_after_close_reconciles_commit_without_second_close(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.tick()
        self.finish()
        self.save(cierres={'uno': dict(commit='b' * 40, resultado='Entregado',
            comprobacion='Comprobado en fixture', verificacion='correcta')})
        self.adapter.after = lambda: (_ for _ in ()).throw(Crash())
        with self.assertRaises(Crash):
            self.tick()
        self.adapter.after = None
        self.tick()
        self.assertEqual(self.adapter.calls.count(('cerrar', 'uno')), 1)
        self.assertIn(('revisar', 'uno'), self.adapter.calls)

    def test_failed_reviewer_retry_needs_explicit_attempt_and_checkpoint(self):
        self.review_ready()
        self.tick()
        row = self.adapter.rows['uno']
        last = row['sesiones'][-1]
        last.update(estado='fallida', rc=1)
        self.assert_blocked(self.tick(), 'Revisor sin finalización correcta')
        self.manifest['tareas'][0]['reintentar_revision_intento'] = last['intento']
        self.save()
        self.assert_blocked(self.tick(), 'conciliación de la revisión fallida')
        self.save(revisiones={'uno': dict(intento=last['intento'], revision=row['revision'], auxiliares_terminados=True)})
        self.tick()
        self.assertEqual(self.adapter.calls.count(('revisar', 'uno')), 2)
        self.assertNotEqual(row['sesiones'][-1]['session_id'], last['session_id'])

    def test_two_failed_sessions_do_not_count_new_attempts_as_product_progress(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.tick()
        row = self.adapter.rows['uno']
        row.update(estado='en_espera')
        row['sesiones'][-1].update(estado='fallida', rc=1)
        sid = row['sesiones'][-1]['session_id']
        self.manifest['tareas'][0]['reanudar_sid'] = sid
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        self.tick()
        row['sesiones'][-1].update(estado='fallida', rc=1)
        row['estado'] = 'en_espera'
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        result = self.tick()
        self.assert_blocked(result, 'Dos fallos sin progreso')
        self.assertEqual(self.adapter.calls.count(('reanudar', 'uno')), 1)
        self.assertIn(('lanzar', 'dos'), self.adapter.calls)

    def test_dispatch_exception_and_failed_process_count_as_one_failure(self):
        self.manifest['tareas'][0]['prioridad'] = 10
        self.save()
        self.adapter.after = lambda: (_ for _ in ()).throw(ValueError('Fallo tras registrar sesión'))
        self.tick()
        self.adapter.after = None
        row = self.adapter.rows['uno']
        row.update(estado='en_espera')
        row['sesiones'][-1].update(estado='fallida', rc=1)
        sid = row['sesiones'][-1]['session_id']
        self.manifest['tareas'][0]['reanudar_sid'] = sid
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        self.tick()
        self.assertIn(('reanudar', 'uno'), self.adapter.calls)
        self.assertFalse(any(e['tipo'] == 'fallo_sesion' and e['id'] == 'uno' for e in self.dispatcher().events()))

    def test_failure_before_effect_and_later_failed_process_are_distinct_failures(self):
        self.manifest['tareas'] = self.manifest['tareas'][:1]
        self.save()
        self.adapter.failure = ValueError('Fallo anterior al efecto')
        self.tick()
        self.resolve(next(e for e in self.dispatcher().events() if e['tipo'] == 'intencion'))
        self.adapter.failure = None
        self.tick()
        row = self.adapter.rows['uno']
        row.update(estado='en_espera')
        row['sesiones'][-1].update(estado='fallida', rc=1)
        sid = row['sesiones'][-1]['session_id']
        self.manifest['tareas'][0]['reanudar_sid'] = sid
        self.save(retomas={'uno': dict(sid=sid, revision=row['revision'], auxiliares_terminados=True)})
        self.assert_blocked(self.tick(), 'Dos fallos sin progreso')
        self.assertNotIn(('reanudar', 'uno'), self.adapter.calls)

    def test_close_validator_rejects_other_commit_and_paths(self):
        adapter = lote.LocalHarness.__new__(lote.LocalHarness)
        adapter.base, adapter.operation, adapter.repo = self.base, self.op, self.root / 'repo'
        task = self.manifest['tareas'][0]
        row = self.adapter.row('uno')
        observation = {'cierres': {'uno': dict(commit='b' * 40, resultado='Resultado', comprobacion='Comprobación')}}
        def close(*args, commit_validator, **kwargs):
            commit_validator(row, {'commit_base': 'a' * 40}, 'b' * 40)
        with patch.object(sessions, 'close', side_effect=close), patch.object(sessions, 'git', return_value='base/salidas/unotro'):
            with self.assertRaisesRegex(ValueError, 'fuera de rutas'):
                adapter.invoke('cerrar', task, row, observation)
        observation['cierres']['uno']['commit'] = 'c' * 40
        with patch.object(sessions, 'close', side_effect=close):
            with self.assertRaisesRegex(ValueError, 'otro commit'):
                adapter.invoke('cerrar', task, row, observation)

    def test_local_adapter_passes_subagents_on_launch_resume_and_zero_on_review(self):
        adapter = lote.LocalHarness.__new__(lote.LocalHarness)
        adapter.base, adapter.operation = self.base, self.op
        task = self.manifest['tareas'][0]
        row = self.adapter.row('uno')
        for limit in (None, 0, 1, 2):
            if limit is not None:
                task['subagentes_maximos'] = limit
            for op in ('lanzar', 'reanudar', 'revisar'):
                with self.subTest(limit=limit, op=op), patch.object(sessions, 'launch') as launch:
                    adapter.invoke(op, task, row, {})
                    kwargs = launch.call_args.kwargs
                    self.assertEqual(kwargs['subagents'], 0 if op == 'revisar' else limit or 0)
                    self.assertEqual(kwargs['resume'], op == 'reanudar')
                    self.assertEqual(kwargs['reviewer'], task['revisor'] if op == 'revisar' else None)
                    self.assertIs(kwargs['approved'], True)
                    self.assertIs(kwargs['auth_chatgpt'], True)

    def test_provider_probe_uses_chatgpt_without_inherited_api_keys(self):
        adapter = lote.LocalHarness.__new__(lote.LocalHarness)
        result = SimpleNamespace(returncode=0, stdout='Logged in using ChatGPT', stderr='')
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'synthetic', 'CODEX_API_KEY': 'synthetic',
                                     'OPENAI_BASE_URL': 'https://example.invalid'}), \
                patch.object(lote.subprocess, 'run', return_value=result) as run:
            self.assertTrue(adapter.provider())
            self.assertEqual(run.call_args.args[0], ['codex', 'login', 'status'])
            env = run.call_args.kwargs['env']
            self.assertFalse({'OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL'} & set(env))
        result.stdout = 'Logged in using an API key'
        with patch.object(lote.subprocess, 'run', return_value=result):
            self.assertFalse(adapter.provider())


class NativeApiTests(unittest.TestCase):
    def test_local_git_executor_close_review_accept_integrate_and_dependency(self):
        # Reusar fixtures del harness. Sólo el binario sintético de esa suite se inicia.
        from test_harness_sesiones import SessionTests
        fixture = SessionTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        row = fixture.prepare('uno')
        fixture.prepare('dos')
        adapter = lote.LocalHarness.__new__(lote.LocalHarness)
        adapter.base, adapter.operation, adapter.repo = fixture.base, fixture.op, fixture.repo
        adapter.provider = lambda: True
        tasks = []
        for ident in ('uno', 'dos'):
            current = fixture.row(ident)
            tasks.append(dict(id=ident, actor='executor', revisor='reviewer', criterio='Entrega sintética cotejada',
                rutas=current['asignacion']['rutas'], briefing_sha256=current['briefing']['sha256'],
                operaciones=sorted(lote.OPS), depende_de=[],
                perfiles={r: dict(modelo='gpt-6.1-sol', esfuerzo='high') for r in ('ejecutor', 'revisor')},
                intentos_maximos={'ejecutor': 2, 'revisor': 1}))
        tasks[0]['prioridad'] = 10
        tasks[0]['subagentes_maximos'] = 1
        manifest = dict(schema=1, id='nativo', habilitado=True, autorizacion='Fixture local autorizada',
            desde='2026-11-11T19:00:00Z', hasta='2026-11-11T21:00:00Z', base=str(fixture.base),
            operacion=str(fixture.op), repositorio=str(fixture.repo), proveedor='openai-chatgpt-incluido',
            cuota_minima_porcentaje=1, tareas=tasks)
        manifest_path = fixture.root / 'lote.json'
        obs_path = fixture.root / 'observaciones.json'
        observation = dict(fecha='2026-11-11T20:00:00Z', disponible=True, saldo_extra_autorizado=False,
                           proveedor=manifest['proveedor'], restante_porcentaje=100)

        def dispatcher():
            manifest_path.write_text(json.dumps(manifest))
            observation['manifiesto_sha256'] = lote.digest(manifest)
            obs_path.write_text(json.dumps(observation))
            return lote.Dispatcher(manifest_path, fixture.op, lote.digest(manifest), adapter=adapter,
                                   clock=lambda: lote.timestamp(observation['fecha']))

        invoke = adapter.invoke

        def crash_after_launch(op, *args):
            invoke(op, *args)
            raise Crash()

        with patch.object(adapter, 'invoke', side_effect=crash_after_launch), self.assertRaises(Crash):
            dispatcher().tick(obs_path)
        fixture.wait_finished('uno')
        original = fixture.row('uno')['sesiones'][0]
        self.assertEqual(original['subagentes_maximos'], 1)
        restored = dispatcher()
        self.assertEqual(restored.recover({'uno': fixture.row('uno')}), {})
        effect, = [e for e in restored.events() if e['tipo'] == 'efecto']
        self.assertEqual(effect['despues']['sesiones'][0]['session_id'], original['session_id'])
        self.assertEqual(effect['despues']['sesiones'][0]['intento'], original['intento'])
        self.assertEqual(len(fixture.row('uno')['sesiones']), 1)
        commit = fixture.deliver('uno')
        observation['cierres'] = {'uno': dict(commit=commit, resultado='Entrega sintética publicada',
            comprobacion='Archivo leído y Git limpio en fixture', verificacion='correcta')}
        dispatcher().tick(obs_path)
        self.assertEqual(fixture.row('uno')['cierre']['commit'], commit)
        dispatcher().tick(obs_path)
        fixture.wait_finished('uno')
        dispatcher().tick(obs_path)
        reviewed = fixture.row('uno')
        self.assertEqual([s['subagentes_maximos'] for s in reviewed['sesiones']], [1, 0])
        self.assertTrue(lote.current_review(reviewed))
        # Aceptación e integración son acciones explícitas de la coordinadora.
        trabajo.accept(fixture.base, 'uno', reviewed['revision'], 'reviewer', 'Fixture cotejada')
        accepted = fixture.row('uno')
        trabajo.assign(fixture.base, 'uno', accepted['revision'], actor='executor', release=True)
        fixture.git('merge', '--ff-only', commit)
        fixture.git('push', 'origin', 'master')
        tasks[1]['depende_de'] = [{'id': 'uno', 'commit': commit}]
        dispatcher().tick(obs_path)
        fixture.wait_finished('dos')
        self.assertEqual(len(fixture.row('uno')['sesiones']), 2)
        self.assertEqual(len(fixture.row('dos')['sesiones']), 1)
        self.assertTrue(adapter.integrated(commit, refresh=True))
        self.assertTrue(Path(row['briefing']['archivo']).name.endswith('.md'))


if __name__ == '__main__':
    unittest.main()
