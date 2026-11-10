"""Delegación con Git temporal, sin Codex ni solicitudes externas."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import harness_boss as boss
import harness_delegacion as delegated
import harness_retorno as retorno
import trabajo
import test_harness_boss as fixtures


class DelegationTests(unittest.TestCase):
    def setUp(self):
        self.bridge = fixtures.BridgeTests(methodName='runTest')
        self.bridge.setUp()
        self.addCleanup(self.bridge.doCleanups)
        self.base, self.root = self.bridge.base, self.bridge.root
        self.config = dict(self.bridge.config, delegacion_fabricas={
            'activa': True, 'autorizacion_sergio': 'fixture sin producción',
            'fabricas': list(delegated.FACTORIES), 'avisos_fin':True})
        self.config_path = self.root/'config.json'
        boss.private_write(self.config_path, self.config)
        self.source = '04-operacion-agentes/pendientes/pedido-fixture.md'
        path = self.base/self.source
        path.parent.mkdir(parents=True, exist_ok=True)
        self.source_text = 'Pedido ficticio.\n```onia-pedido-v1\n' + json.dumps({k:v for k,v in self.request().items() if k in {'id','fabrica','objetivo','entregable','aceptacion','esfuerzo'}}) + '\n```\n'
        path.write_text(self.source_text)
        self.bridge.fixture.git('add', '.')
        self.bridge.fixture.git('commit', '-m', 'pedido ficticio')
        self.bridge.fixture.git('push', 'origin', 'master')

    def request(self, ident='fabrica-codigo-prueba', nonce='alta-1'):
        return {'version':1, 'operacion':'registrar', 'id':ident, 'solicitud':nonce,
                'fabrica':'codigo', 'objetivo':'Comprobar un texto', 'entregable':'Texto y evidencia',
                'aceptacion':'Un texto correcto', 'pedido':self.source, 'esfuerzo':'low'}

    def handle(self, req):
        return boss.handle(self.config, req, config_path=self.config_path)

    def test_register_publish_scope_grant_and_duplicate_without_launch(self):
        with patch.object(boss.sessions, 'launch') as launch:
            response = self.handle(self.request())
            duplicate = self.handle(self.request())
            launch.assert_not_called()
        self.assertTrue(response['ok']); self.assertTrue(duplicate['repetida'])
        row = trabajo.read_task(self.base, response['tarea']['id'])
        self.assertEqual(row['revision'], 3)
        self.assertEqual(row['asignacion']['rutas'],[
            '05-herramientas/fabrica-onia/5-codigo/trabajos/fabrica-codigo-prueba'])
        grant = boss.private_read(self.root/'permisos/fabrica-codigo-prueba.json')
        self.assertEqual(grant['modelo'], 'gpt-6.1-sol');self.assertEqual(grant['max_intentos'],2)
        self.assertNotEqual(grant['actor'], grant['revisor'])
        conf = boss.private_read(self.config_path)
        self.assertIn(row['id'], conf['lectura_ids']);self.assertIn(row['id'],conf['avisos_fin_ids'])
        published = retorno.git(self.bridge.repo, 'show', response['commit']+':'+str(trabajo.task_path(self.base,row['id']).relative_to(self.bridge.repo)))
        self.assertEqual(json.loads(published), row)

    def test_invalid_scope_model_source_extra_fields_and_secret_refused(self):
        changes = [{'fabrica':'root'}, {'esfuerzo':'ultra'}, {'modelo':'otro'}, {'rutas':['/etc']},
                   {'pedido':'../../secret.md'}, {'pedido':'04-operacion-agentes/boss-memoria.md'},
                   {'id':'conexion-boss-piloto-20261110'}, {'objetivo':'ghp_'+'x'*24}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises((boss.Rejected, ValueError)):
                self.handle(self.request()|change)
        self.assertFalse((self.root/'altas').exists())

    def test_disabled_or_paused_policy_rejected(self):
        for change in ({'pausado':True}, {'delegacion_fabricas':{'activa':False}}):
            boss.private_write(self.config_path,self.config|change)
            with self.assertRaises(boss.Rejected):self.handle(self.request())

    def test_publication_failure_retry_same_nonce_without_recreating_task(self):
        with patch.object(retorno,'publish',side_effect=RuntimeError('synthetic')):
            result = self.handle(self.request())
        self.assertEqual(result['error'],'registro_pendiente_publicacion')
        self.assertFalse((self.root/'permisos/fabrica-codigo-prueba.json').exists())
        with patch.object(delegated.harness,'prepare',side_effect=AssertionError('no repetir')):
            result = self.handle(self.request())
        self.assertTrue(result['ok']);self.assertEqual(result['tarea']['revision'],3)

    def test_registration_after_six_attempts_preserves_audit_and_deduplicates(self):
        from datetime import datetime,timezone
        stamp = datetime.now(timezone.utc)
        originals = {}
        for i in range(6):
            path = self.root/'altas'/f'fixture-{i}.json'
            boss.private_write(path,{'fecha_dia':stamp.date().isoformat()})
            originals[path] = path.read_bytes()
        with patch.object(boss.sessions, 'launch') as launch, \
             patch.object(delegated, 'datetime', wraps=datetime) as clock:
            clock.now.return_value = stamp
            response = self.handle(self.request())
            duplicate = self.handle(self.request())
            launch.assert_not_called()
        self.assertTrue(response['ok']); self.assertTrue(duplicate['repetida'])
        self.assertEqual(response['commit'], duplicate['commit'])
        self.assertEqual(len(list((self.root/'altas').glob('*.json'))), 7)
        for path, content in originals.items():
            self.assertEqual(path.read_bytes(), content)
        with self.assertRaisesRegex(boss.Rejected, 'id_existente'):
            self.handle(self.request(nonce='otra-alta'))
        self.assertEqual(len(list((self.root/'altas').glob('*.json'))), 7)

    def test_eight_published_registrations_same_day_without_launch_or_quota_call(self):
        from datetime import datetime,timezone
        stamp = datetime.now(timezone.utc)
        requests = []
        for i in range(8):
            req = self.request(ident=f'fabrica-codigo-lote-{i}', nonce=f'alta-lote-{i}')
            req['pedido'] = f'04-operacion-agentes/pendientes/pedido-lote-{i}.md'
            spec = {k:req[k] for k in ('id','fabrica','objetivo','entregable','aceptacion','esfuerzo')}
            (self.base/req['pedido']).write_text('```onia-pedido-v1\n'+json.dumps(spec)+'\n```\n')
            requests.append(req)
        self.bridge.fixture.git('add', '.')
        self.bridge.fixture.git('commit', '-m', 'ocho pedidos ficticios')
        self.bridge.fixture.git('push', 'origin', 'master')
        ids = []
        with patch.object(boss.sessions, 'launch') as launch, \
             patch.object(delegated, 'quota_snapshot', side_effect=AssertionError('registrar no lanza')), \
             patch.object(delegated, 'datetime', wraps=datetime) as clock:
            clock.now.return_value = stamp
            for req in requests:
                ident = req['id']
                response = self.handle(req)
                self.assertTrue(response['ok'])
                row = trabajo.read_task(self.base, ident)
                self.assertEqual(row['estado'], 'preparado')
                self.assertFalse(row.get('sesiones'))
                audit = boss.private_read(self.root/'altas'/(ident+'.json'))
                self.assertEqual(audit['fecha_dia'], stamp.date().isoformat())
                self.assertEqual(audit['solicitud'], req['solicitud'])
                published = retorno.git(self.bridge.repo, 'show', response['commit']+':'+str(trabajo.task_path(self.base,ident).relative_to(self.bridge.repo)))
                self.assertEqual(json.loads(published), row)
                ids.append(ident)
            launch.assert_not_called()
        self.assertEqual(len(set(ids)), 8)
        self.assertEqual(len(list((self.root/'altas').glob('*.json'))), 8)

    def test_changed_source_and_nonce_are_not_accepted(self):
        (self.base/self.source).write_text('cambio no publicado')
        with self.assertRaisesRegex(boss.Rejected,'pedido_local_no_coincide'):
            self.handle(self.request())
        (self.base/self.source).write_text(self.source_text)
        self.handle(self.request())
        with self.assertRaisesRegex(boss.Rejected,'solicitud_reutilizada'):
            self.handle(self.request()|{'objetivo':'otro'})

    def test_renew_preserves_binding_attempt_limit_and_rejects_revocation(self):
        self.handle(self.request())
        req={'version':1,'operacion':'habilitar','id':'fabrica-codigo-prueba','solicitud':'renovar-1','revision_esperada':3}
        result=self.handle(req); self.assertEqual(result['permiso']['max_intentos'],2)
        path=self.root/'permisos/fabrica-codigo-prueba.json'
        old=boss.private_read(path);boss.private_write(path,old|{'revocado':True})
        with self.assertRaisesRegex(boss.Rejected,'revocado'):
            self.handle(req|{'solicitud':'renovar-2'})

    def test_quota_and_policy_gates_precede_launch_and_journal(self):
        self.handle(self.request())
        config=boss.private_read(self.config_path)
        req={'version':1,'operacion':'ejecutar','id':'fabrica-codigo-prueba','solicitud':'run-1','revision_esperada':3}
        for quota in (90,100):
            with patch.object(delegated,'quota_snapshot',return_value={'used_percent':quota}), \
                 patch.object(boss.sessions,'launch') as launch, self.assertRaisesRegex(boss.Rejected,'tope_cuota'):
                boss.handle(config,req,config_path=self.config_path)
            launch.assert_not_called()
        self.assertFalse((self.root/'barreras/fabrica-codigo-prueba.json').exists())
        with patch.object(delegated,'quota_snapshot',return_value={'used_percent':81}), \
             patch.object(boss.sessions,'launch') as launch:
            self.assertTrue(boss.handle(config,req,config_path=self.config_path)['ok'])
            self.assertEqual(launch.call_args.kwargs['subagents'],0)
            self.assertEqual(launch.call_args.kwargs['model'],'gpt-6.1-sol')

    def test_reserved_id_survives_crash_before_create(self):
        with patch.object(delegated.harness,'prepare',side_effect=RuntimeError('crash')), self.assertRaises(RuntimeError):
            self.handle(self.request())
        old=boss.private_read(self.root/'altas/fabrica-codigo-prueba.json')
        with self.assertRaisesRegex(boss.Rejected,'id_reservado'):
            self.handle(self.request(nonce='otro-nonce'))
        self.assertEqual(boss.private_read(self.root/'altas/fabrica-codigo-prueba.json'),old)

    def test_pending_renewal_cannot_undo_revocation_or_scope_reduction(self):
        self.handle(self.request())
        req={'version':1,'operacion':'habilitar','id':'fabrica-codigo-prueba','solicitud':'renovar-1','revision_esperada':3}
        with patch.object(retorno,'publish',side_effect=RuntimeError('sin Git')):
            self.assertFalse(self.handle(req)['ok'])
        path=self.root/'permisos/fabrica-codigo-prueba.json'
        old=boss.private_read(path)
        boss.private_write(path,old|{'revocado':True})
        with self.assertRaisesRegex(boss.Rejected,'revocado'):
            self.handle(req)
        self.assertTrue(boss.private_read(path)['revocado'])
        boss.private_write(path,old|{'operaciones':['recoger'],'max_intentos':1})
        self.assertTrue(self.handle(req)['ok'])
        self.assertEqual(boss.private_read(path)['operaciones'],['recoger'])
        self.assertEqual(boss.private_read(path)['max_intentos'],1)

    def test_request_must_match_frozen_published_spec(self):
        with self.assertRaisesRegex(boss.Rejected,'solicitud_distinta'):
            self.handle(self.request()|{'objetivo':'otro encargo'})
        self.handle(self.request())
        row=trabajo.read_task(self.base,'fabrica-codigo-prueba')
        path=self.base/row['evidencias'][0]['archivo']
        path.write_text('modificado')
        with self.assertRaisesRegex(ValueError,'Evidencia cambió'):
            trabajo.verify(self.base,row)

    def test_quota_reader_requires_real_event_shape_and_freshness(self):
        from datetime import datetime,timedelta,timezone
        home=self.bridge.op/'quota-home'; folder=home/'.codex/sessions';folder.mkdir(parents=True)
        path=folder/'synthetic.jsonl'
        def event(stamp,kind='event_msg', payload_kind='token_count', limit='codex'):
            return {'timestamp':stamp.isoformat(),'type':kind,'payload':{'type':payload_kind,'rate_limits':{
                'limit_id':limit,'primary':{'used_percent':81,'window_minutes':10080}}}}
        now=datetime.now(timezone.utc)
        with patch.object(Path,'home',return_value=home):
            for item in (event(now,kind='item'),event(now,payload_kind='message'),event(now,limit='other')):
                path.write_text(json.dumps(item)+'\n')
                with self.assertRaisesRegex(boss.Rejected,'cuota_no_comprobada'):delegated.quota_snapshot()
            path.write_text(json.dumps(event(now-timedelta(hours=3)))+'\n')
            with self.assertRaisesRegex(boss.Rejected,'cuota_desactualizada'):delegated.quota_snapshot()
            path.write_text(json.dumps(event(now))+'\n')
            self.assertEqual(delegated.quota_snapshot()['used_percent'],81)

    def test_product_rename_from_outside_route_refused(self):
        self.handle(self.request())
        row=trabajo.read_task(self.base,'fabrica-codigo-prueba')
        grant=boss.private_read(self.root/'permisos/fabrica-codigo-prueba.json')
        original=self.bridge.repo/'outside.txt';original.write_text('base')
        self.bridge.fixture.git('add','outside.txt');self.bridge.fixture.git('commit','-m','base')
        base_commit=self.bridge.fixture.git('rev-parse','HEAD')
        destination=self.base/row['asignacion']['rutas'][0]/'inside.txt';destination.parent.mkdir(parents=True)
        self.bridge.fixture.git('mv',str(original),str(destination))
        self.bridge.fixture.git('commit','-m','rename')
        commit=self.bridge.fixture.git('rev-parse','HEAD')
        session={'worktree':str(self.bridge.repo),'commit_base':base_commit}
        with patch.object(boss.sessions,'validate_private_git'), self.assertRaisesRegex(boss.Rejected,'entrega_fuera_de_rutas'):
            delegated.check_product_scope(self.config,row,grant,session,commit)

    def test_renewal_does_not_restore_allowlists_or_global_notifications(self):
        self.handle(self.request())
        config=boss.private_read(self.config_path)
        config['lectura_ids']=[];config['avisos_fin_ids']=[];config['avisar_fin_sesion']=False
        boss.private_write(self.config_path,config)
        self.handle({'version':1,'operacion':'habilitar','id':'fabrica-codigo-prueba','solicitud':'renovar-1','revision_esperada':3})
        after=boss.private_read(self.config_path)
        self.assertEqual(after['lectura_ids'],[]);self.assertEqual(after['avisos_fin_ids'],[])
        self.assertIs(after['avisar_fin_sesion'],False)



if __name__ == '__main__':
    unittest.main()
