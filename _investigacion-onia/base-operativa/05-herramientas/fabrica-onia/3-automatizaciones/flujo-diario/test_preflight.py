"""RPC/control de admisión con procesos sintéticos; jamás lanza sesiones Codex."""
import copy
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import Mock, patch

import preflight as p
import motor
import comun
from adaptador_harness import LocalHarness, task_id
import test_flujo as fixture

NOW = datetime.now(timezone.utc)
STAMP = NOW.isoformat()
ACCOUNT = {'account': {'type': 'chatgpt', 'email': 'PRIVATE@example.invalid', 'planType': 'pro'}, 'requiresOpenaiAuth': True}
BUCKET = {'limitId': 'codex', 'primary': {'usedPercent': 95, 'windowDurationMins': 300,
          'resetsAt': int(NOW.timestamp())+86400}, 'secondary': {'usedPercent': 99,
          'windowDurationMins': 10080, 'resetsAt': int(NOW.timestamp())+864000},
          'rateLimitReachedType': None, 'spendControlReached': False}
QUOTA = {'ordinaryUsageAllowed': True, 'rateLimits': BUCKET, 'rateLimitsByLimitId': {'codex': BUCKET},
         'accountId': 'PRIVATE_ACCOUNT', 'rateLimitResetCredits': {'credits': ['PRIVATE_RESET']}}


def valid():
    return p.validate(copy.deepcopy(ACCOUNT), copy.deepcopy(QUOTA), STAMP, STAMP)


class ValidationTests(unittest.TestCase):
    def test_incluido_sin_reserva_90_y_salida_saneada(self):
        snapshot = valid()
        self.assertTrue(snapshot['permitido'])
        self.assertEqual(snapshot['limites']['secondary']['usedPercent'], 99)
        self.assertNotIn('PRIVATE', json.dumps(snapshot))
        self.assertNotIn('credits', json.dumps(snapshot))

    def test_cuota_agotada_y_backend_no_autoriza_creditos(self):
        cases = []
        for key in ('primary', 'secondary'):
            q = copy.deepcopy(QUOTA)
            q['rateLimitsByLimitId']['codex'][key]['usedPercent'] = 100
            cases.append(q)
        for key, value in [('ordinaryUsageAllowed', False)]:
            q = copy.deepcopy(QUOTA);q[key] = value;cases.append(q)
        for key, value in [('spendControlReached', True), ('rateLimitReachedType', 'rate_limit_reached')]:
            q = copy.deepcopy(QUOTA);q['rateLimitsByLimitId']['codex'][key] = value;cases.append(q)
        for q in cases:
            q['rateLimits']['credits'] = {'hasCredits': True, 'unlimited': True, 'balance': '99999'}
            with self.subTest(q=q), self.assertRaisesRegex(p.PreflightError, 'CUOTA_AGOTADA'):
                p.validate(ACCOUNT, q, STAMP, STAMP)

    def test_permiso_incluido_desconocido_no_se_infiere_de_porcentajes(self):
        for value in (None, 'true', 1, [], {}):
            q = copy.deepcopy(QUOTA);q['ordinaryUsageAllowed'] = value
            with self.subTest(value=value), self.assertRaises(p.PreflightError):
                p.validate(ACCOUNT, q, STAMP, STAMP)
        q = copy.deepcopy(QUOTA);del q['ordinaryUsageAllowed']
        with self.assertRaisesRegex(p.PreflightError, 'CUOTA_PERMISO_DESCONOCIDO'):
            p.validate(ACCOUNT, q, STAMP, STAMP)

    def test_tipos_invalidos_rangos_nan_y_ventanas_sin_datos(self):
        for field, values in [('usedPercent', [True, False, 95.0, '95', -1, 101, None, float('nan'), float('inf')]),
                              ('windowDurationMins', [True, 0, -1, '300', 300.0, None]),
                              ('resetsAt', [True, 0, -1, '123', 123.0, None])]:
            for value in values:
                q = copy.deepcopy(QUOTA);q['rateLimitsByLimitId']['codex']['primary'][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(p.PreflightError):
                    p.validate(ACCOUNT, q, STAMP, STAMP)
        q = copy.deepcopy(QUOTA)
        q['rateLimitsByLimitId']['codex'].update(primary=None, secondary=None)
        with self.assertRaisesRegex(p.PreflightError, 'CUOTA_CODEX_DESCONOCIDA'):
            p.validate(ACCOUNT, q, STAMP, STAMP)

    def test_reset_pasado_no_se_convierte_en_renovacion(self):
        q = copy.deepcopy(QUOTA)
        q['rateLimitsByLimitId']['codex']['primary']['resetsAt'] = int(NOW.timestamp())-1
        with self.assertRaisesRegex(p.PreflightError, 'CUOTA_VENTANA_VENCIDA'):
            p.validate(ACCOUNT, q, STAMP, STAMP)

    def test_login_incluido_y_plan_requeridos(self):
        for identity in (None, {}, {'type': 'apiKey'}, {'type': 'amazonBedrock'},
                         {'type': 'chatgpt', 'planType': 'unknown'},
                         {'type': 'chatgpt', 'planType': 'self_serve_business_usage_based'}):
            account = {**ACCOUNT, 'account': identity}
            with self.subTest(identity=identity), self.assertRaises(p.PreflightError):
                p.validate(account, QUOTA, STAMP, STAMP)
        for value in (False, None, 'true', 1):
            with self.subTest(value=value), self.assertRaises(p.PreflightError):
                p.validate({**ACCOUNT, 'requiresOpenaiAuth': value}, QUOTA, STAMP, STAMP)

    def test_bucket_global_y_compatibilidad_sin_mapa(self):
        q = copy.deepcopy(QUOTA);q.pop('rateLimitsByLimitId')
        self.assertTrue(p.validate(ACCOUNT, q, STAMP, STAMP)['permitido'])
        for buckets in ({}, [], {'other': BUCKET}, {'codex': []}):
            q = {**QUOTA, 'rateLimitsByLimitId': buckets}
            with self.subTest(buckets=buckets), self.assertRaises(p.PreflightError):
                p.validate(ACCOUNT, q, STAMP, STAMP)


SCRIPT = r'''
import json,sys,time
account=json.loads(sys.argv[1]);quota=json.loads(sys.argv[2]);mode=sys.argv[3]
for line in sys.stdin:
 request=json.loads(line)
 method=request['method']
 assert method in ('initialize','initialized','account/read','account/rateLimits/read')
 if method=='initialized': continue
 if method=='account/read': assert request['params']=={'refreshToken':False}
 if method=='account/rateLimits/read': assert request['params']=={'excludeResetCreditDetails':True}
 if mode=='partial':
  sys.stdout.write('{');sys.stdout.flush();time.sleep(60)
 if mode=='oversize':
  sys.stdout.write('x'*600000+'\n');sys.stdout.flush();time.sleep(60)
 if mode=='error':
  print(json.dumps({'id':request['id'],'error':{'message':'PRIVATE TOKEN ERROR'}}),flush=True);continue
 if mode=='wrong-id':
  print(json.dumps({'id':True,'result':{}}),flush=True);continue
 if mode=='bad-json':
  print('not-json PRIVATE',flush=True);continue
 if mode=='nan':
  print('{"id":1,"result":{"x":NaN}}',flush=True);continue
 if mode=='duplicate':
  print('{"id":1,"id":1,"result":{}}',flush=True);continue
 print(json.dumps({'method':'test/notification','params':{'secret':'PRIVATE'}}),flush=True)
 print(json.dumps({'id':request['id'],'result':account if method=='account/read' else quota if method=='account/rateLimits/read' else {}}),flush=True)
 if method=='account/rateLimits/read':time.sleep(60)
'''


class RPCTests(unittest.TestCase):
    def run_rpc(self, mode='ok', timeout=1):
        processes, calls = [], []
        def factory(command, **kwargs):
            calls.append((command, kwargs))
            process = subprocess.Popen([sys.executable, '-u', '-c', SCRIPT, json.dumps(ACCOUNT), json.dumps(QUOTA), mode], **kwargs)
            processes.append(process)
            return process
        try:
            return p.read_live(timeout=timeout, process_factory=factory), calls
        finally:
            self.assertTrue(all(proc.poll() is not None for proc in processes), 'Cada RPC debe salir sin daemon')

    def test_transporte_efimero_solo_lecturas_y_sin_api_env(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY':'PRIVATE','CODEX_API_KEY':'PRIVATE','OPENAI_BASE_URL':'PRIVATE','CODEX_ACCESS_TOKEN':'PRIVATE'}):
            snapshot, calls = self.run_rpc()
        self.assertTrue(snapshot['permitido'])
        self.assertEqual(calls[0][0], list(p.COMMAND))
        self.assertNotIn('exec', calls[0][0])
        for name in ('OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL','CODEX_ACCESS_TOKEN'):
            self.assertNotIn(name, calls[0][1]['env'])
        self.assertEqual(calls[0][1]['stderr'], subprocess.DEVNULL)

    def test_cada_lectura_es_nueva_no_reutiliza_cache(self):
        a, _ = self.run_rpc();b, _ = self.run_rpc()
        self.assertGreater(datetime.fromisoformat(b['iniciada']), datetime.fromisoformat(a['completada']))

    def test_timeout_total_tambien_en_linea_parcial_y_cierra_proceso(self):
        started = time.monotonic()
        with self.assertRaisesRegex(p.PreflightError, 'PREFLIGHT_TIMEOUT'):
            self.run_rpc('partial', timeout=0.08)
        self.assertLess(time.monotonic()-started, 1.5)

    def test_fallo_rpc_tipos_invalidos_y_exceso_sin_filtrar_payload(self):
        for mode in ('error','bad-json','wrong-id','oversize','nan','duplicate'):
            with self.subTest(mode=mode):
                with self.assertRaises(p.PreflightError) as error:
                    self.run_rpc(mode)
                self.assertNotIn('PRIVATE', str(error.exception))

    def test_fallo_de_arranque_saneado(self):
        with self.assertRaisesRegex(p.PreflightError, 'PREFLIGHT_RPC_FALLIDO'):
            p.read_live(process_factory=Mock(side_effect=OSError('PRIVATE config')))


class AdmissionTests(unittest.TestCase):
    def adapter(self):
        adapter = LocalHarness.__new__(LocalHarness)
        adapter.base = comun.BASE
        adapter.operation = Path('/tmp/no-usada')
        adapter.sessions = types.SimpleNamespace(launch=Mock(), close=Mock(), collect_review=Mock())
        adapter.preflight = Mock(return_value=valid())
        request = motor.make_request(fixture.DAY, [], fixture.STAMP, True)
        _, actor, route = adapter.scope(request)
        before = {'exists': True,'revision':7,'binding':'SCOPE','goal':adapter.goal(request),
                  'actor':actor,'routes':[route],'sessions':[],'occupied':0}
        adapter.query = Mock(return_value=copy.deepcopy(before))
        return adapter, request, before

    def test_lanzar_y_revisar_comprueban_cada_vez_antes_del_modelo(self):
        adapter, request, row = self.adapter()
        for op in ('lanzar', 'revisar'):
            receipt = adapter.invoke(op, request, row, Path('/tmp/no-se-lee'))
            self.assertTrue(receipt['preflight']['permitido'])
        self.assertEqual(adapter.preflight.call_count, 2)
        self.assertEqual(adapter.sessions.launch.call_count, 2)
        self.assertTrue(adapter.sessions.launch.call_args.kwargs['auth_chatgpt'])
        self.assertEqual(adapter.sessions.launch.call_args.kwargs['subagents'], 0)

    def test_cuota_agotada_rpc_tipos_y_timeout_nunca_lanzan(self):
        for code in ('CUOTA_AGOTADA','LOGIN_CHATGPT_REQUERIDO','PREFLIGHT_RPC_FALLIDO','PREFLIGHT_DATOS_INVALIDOS','PREFLIGHT_TIMEOUT'):
            for op in ('lanzar','revisar'):
                adapter, request, row = self.adapter()
                adapter.preflight.side_effect = p.PreflightError(code)
                with self.subTest(code=code,op=op), self.assertRaisesRegex(p.PreflightError,code):
                    adapter.invoke(op,request,row,Path('/tmp/no-se-lee'))
                adapter.sessions.launch.assert_not_called()

    def test_cerrar_recoger_no_consultan_cuota_aunque_este_agotada(self):
        adapter, request, row = self.adapter()
        adapter.preflight.side_effect = p.PreflightError('CUOTA_AGOTADA')
        adapter.invoke('cerrar',request,row,Path('/tmp/no-se-lee'))
        adapter.invoke('recoger',request,row,Path('/tmp/no-se-lee'))
        adapter.preflight.assert_not_called()
        adapter.sessions.close.assert_called_once()
        adapter.sessions.collect_review.assert_called_once()

    def test_motor_no_deja_despacho_incierto_por_fallo_previo_y_reintenta_lectura(self):
        class Guarded(fixture.FakeHarness):
            def invoke(self,op,*args):
                if op in {'lanzar','revisar'}:
                    guard()
                return super().invoke(op,*args)
        guard = Mock(side_effect=p.PreflightError('CUOTA_AGOTADA'))
        with tempfile.TemporaryDirectory(prefix='onia-admission-',dir='/tmp') as tmp:
            fake = Guarded();engine = motor.Engine(Path(tmp),fake,clock=lambda:fixture.STAMP)
            self.addCleanup(engine.store.close)
            step = lambda provider=True:engine.step('reconciliar',authorized_id=task_id(fixture.DAY),provider=provider)
            engine.step('entrada',fixture.report(),task_id(fixture.DAY),True)
            view = step()
            self.assertEqual(view['ciclos'][0]['error'],'CUOTA_AGOTADA')
            self.assertEqual(engine.store.get('efecto',task_id(fixture.DAY)+':lanzar')['fase'],'preparado')
            self.assertEqual(fake.calls,['registrar'])
            guard.side_effect=None;guard.return_value=valid()
            step();fake.finish();step(False)  # cerrar sin cuota/proveedor
            guard.side_effect=p.PreflightError('PREFLIGHT_TIMEOUT')
            view=step()
            self.assertEqual(view['ciclos'][0]['error'],'PREFLIGHT_TIMEOUT')
            self.assertEqual(fake.calls.count('lanzar'),1)
            guard.side_effect=None;step();fake.finish()
            step(False)  # recoger aunque proveedor no esté disponible
            final=step(False)
            self.assertEqual(final['ciclos'][0]['fase'],'para_revision_editorial')
            self.assertEqual(fake.calls,['registrar','lanzar','cerrar','revisar','recoger'])


if __name__ == '__main__':
    unittest.main()
