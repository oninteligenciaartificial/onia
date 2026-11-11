"""Regresiones de revisión y lectura de contrato. Datos privados de ensayo en /tmp."""
import base64
import copy
import http.client
from http.server import HTTPServer
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

import acceso
import cerebro
import lector
import operacion as op
import servidor
import vistas_cerebro
from test_operacion import Forms


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='onia-cerebro-sintetico-')
        self.addCleanup(self.tmp.cleanup)
        self.app = servidor.Application(self.tmp.name)
        self.http = HTTPServer(('127.0.0.1',0),servidor.handler_for(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever,kwargs={'poll_interval':0.01})
        self.thread.start()
        self.addCleanup(self.stop)

    def stop(self):
        self.http.shutdown()
        self.thread.join(timeout=5)
        self.http.server_close()

    def request(self, method='GET', path='/', fields=None, origin='local', headers=None):
        port = self.http.server_port
        values = {'Content-Type':'application/x-www-form-urlencoded'}
        if origin is not None:
            values['Origin'] = f'http://127.0.0.1:{port}' if origin=='local' else origin
        values.update(headers or {})
        conn = http.client.HTTPConnection('127.0.0.1',port,timeout=15)
        conn.request(method,path,urlencode(fields).encode() if fields else None,values)
        response = conn.getresponse()
        result = response.status,dict(response.getheaders()),response.read().decode()
        conn.close()
        return result

    def fields(self):
        fields = Forms(self.request()[2]).forms[0]
        return {**fields,'motivo':'ENSAYO SINTÉTICO de acción evaluable','correccion':'Nueva pieza de ensayo local con criterio comprobable.','alcance':'pieza'}

    def action_fields(self, fields, version='1'):
        return {key:fields[key] for key in ('csrf','target','source_hash')} | {'version':version}

    def test_source_documents_and_correction_from_all_sections(self):
        model = self.app.model()
        self.assertEqual(len(model['conocimiento']['fuentes']),5)
        self.assertTrue(any(name=='Precio del grupo' for name,_ in model['conocimiento']['decisiones']))
        self.assertTrue(model['conocimiento']['reglas'])
        for key in model['context_targets'].values():
            status,_,html = self.request(path='/?objetivo='+key+'#correcciones')
            self.assertEqual(status,200)
            self.assertIn(model['targets'][key]['nombre'],html)
            self.assertIn('name="alcance"',html)
        self.assertEqual(self.request(path='/?objetivo=../../privado')[0],400)
        private_id=lector.sha('privado/contexto.md'.encode())[:24]
        self.assertEqual(self.request(path='/documento?id='+private_id)[0],400)

    def test_double_submission_idempotent_conflicting_payload_rejected(self):
        fields=self.fields()
        self.assertEqual(self.request('POST','/revision',fields)[0],303)
        self.assertEqual(self.request('POST','/revision',fields)[0],303)
        self.assertEqual(len(self.app.reviews.history(fields['target'])),1)
        restarted=servidor.Application(self.tmp.name)
        retry={key:[value] for key,value in fields.items()}
        retry['csrf']=[restarted.csrf]
        self.assertEqual(restarted.save(retry),fields['target'])
        self.assertEqual(len(restarted.reviews.history(fields['target'])),1)
        self.assertEqual(self.request('POST','/revision',{**fields,'correccion':'Otra propuesta con ID reutilizado'})[0],409)
        stale={**fields,'solicitud_id':'a'*64}
        self.assertEqual(self.request('POST','/revision',stale)[0],409)

    def test_apply_creates_private_version_once_restart_and_recorrect(self):
        fields=self.fields()
        original=(lector.BASE/op.HISTORIC_TANDA).read_bytes()
        self.assertEqual(self.request('POST','/revision',fields)[0],303)
        self.assertEqual(self.app.corrections.versions(),[])
        action=self.action_fields(fields)
        status,headers,_=self.request('POST','/aplicar',action)
        self.assertEqual(status,303)
        self.assertEqual(self.request('POST','/aplicar',action)[0],303)
        status,_,html=self.request(path=headers['Location'])
        self.assertEqual(status,200)
        self.assertIn('pendiente de revisión',html)
        self.assertIn(fields['correccion'],html)
        self.assertIn('Original conservado',html)
        restarted=servidor.Application(self.tmp.name)
        self.assertEqual(len(restarted.corrections.versions()),1)
        model=restarted.model()
        key=model['versiones_locales'][0]['target_local']
        item=model['targets'][key]
        restarted.save({'csrf':[restarted.csrf],'target':[key],'source_hash':[item['huella_revision']],
                        'version':['0'],'motivo':['ENSAYO siguiente versión'],'correccion':['Segunda pieza local de ensayo.']})
        restarted.corrections.apply(item,1)
        self.assertEqual(len(restarted.corrections.versions()),2)
        self.assertEqual((lector.BASE/op.HISTORIC_TANDA).read_bytes(),original)

    def test_obsolete_observation_and_tampered_source_cannot_apply(self):
        fields=self.fields()
        self.request('POST','/revision',fields)
        next_fields=self.fields()
        next_fields['correccion']='Nueva propuesta pendiente para el mismo texto.'
        self.assertEqual(self.request('POST','/revision',next_fields)[0],303)
        self.assertEqual(self.request('POST','/aplicar',self.action_fields(fields))[0],409)
        self.assertEqual(self.request('POST','/aplicar',{**self.action_fields(fields,'2'),'source_hash':'wrong'})[0],409)
        self.assertEqual(self.app.corrections.versions(),[])

    def test_canonical_and_llm_export_request_never_marked_applied(self):
        model=self.app.model()
        key=model['context_targets']['calendario']
        fields=Forms(self.request(path='/?objetivo='+key)[2]).forms[-1]
        fields.update(motivo='ENSAYO cambio propuesto de precio',correccion='Proponer nueva decisión comercial.',alcance='canonico')
        self.assertEqual(self.request('POST','/revision',fields)[0],303)
        self.assertEqual(self.request('POST','/aplicar',self.action_fields(fields))[0],409)
        status,headers,_=self.request('POST','/solicitar',self.action_fields(fields))
        self.assertEqual(status,303)
        again=self.request('POST','/solicitar',self.action_fields(fields))
        self.assertEqual(again[1]['Location'],headers['Location'])
        payload=json.loads(self.request(path=headers['Location'])[2])
        self.assertEqual(payload['schema'],'onia-solicitud-correccion-v1')
        self.assertEqual(payload['estado'],'pendiente_coordinacion')
        self.assertIn(op.DECISIONS,payload['dependencias'])
        self.assertEqual(self.app.corrections.versions(),[])

    def test_malicious_text_stays_escaped_after_application(self):
        fields=self.fields()
        fields['correccion']='<script>alert(1)</script><img src=x onerror=alert(1)>'
        self.assertEqual(self.request('POST','/revision',fields)[0],303)
        status,headers,_=self.request('POST','/aplicar',self.action_fields(fields))
        self.assertEqual(status,303)
        html=self.request(path=headers['Location'])[2]
        self.assertNotIn('<script',html)
        self.assertNotIn('<img',html)
        self.assertIn('&lt;script',html)

    def test_new_mutations_keep_csrf_and_origin_guards(self):
        fields=self.fields()
        self.request('POST','/revision',fields)
        action=self.action_fields(fields)
        for path in ('/aplicar','/solicitar'):
            for origin in (None,'null','*','https://evil.invalid'):
                self.assertEqual(self.request('POST',path,action,origin=origin)[0],403)
            self.assertEqual(self.request('POST',path,{**action,'csrf':'wrong'})[0],409)
        self.assertEqual(self.app.corrections.versions(),[])

    def test_legacy_database_migrates_without_losing_rows(self):
        legacy=Path(self.tmp.name)/'legacy'
        legacy.mkdir()
        with sqlite3.connect(legacy/'revisiones.sqlite3') as db:
            db.execute('CREATE TABLE revisiones(target TEXT, version INTEGER, fecha TEXT, motivo TEXT, correccion TEXT, estado TEXT, fuente TEXT, sha256_fuente TEXT, original TEXT, PRIMARY KEY(target,version))')
            db.execute('INSERT INTO revisiones VALUES (?,?,?,?,?,?,?,?,?)',('legacy',1,'2026-11-11','motivo','propuesta','pendiente','fuente','sha','{}'))
        reviews=op.Reviews(legacy)
        self.assertEqual(reviews.history('legacy')[0]['correccion'],'propuesta')
        self.assertEqual(reviews.history('legacy')[0]['alcance'],'pieza')


class PrivateAccessTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='onia-acceso-sintetico-')
        self.addCleanup(self.tmp.cleanup)
        self.config=Path(self.tmp.name)/'acceso.json'
        self.password='ENSAYO-'+ 'x'*32
        acceso.create(self.config,'https://panel.example.invalid','ensayo',self.password)
        self.app=servidor.Application(Path(self.tmp.name)/'datos',access_path=self.config)
        self.http=HTTPServer(('127.0.0.1',0),servidor.handler_for(self.app))
        self.thread=threading.Thread(target=self.http.serve_forever,kwargs={'poll_interval':0.01})
        self.thread.start()
        self.addCleanup(self.stop)
        self.authorization='Basic '+base64.b64encode(('ensayo:'+self.password).encode()).decode()

    def stop(self):
        self.http.shutdown()
        self.thread.join(timeout=5)
        self.http.server_close()

    def request(self,path='/',auth=True,host='panel.example.invalid',extra=None):
        headers={'Host':host}
        if auth:headers['Authorization']=self.authorization
        headers.update(extra or {})
        conn=http.client.HTTPConnection('127.0.0.1',self.http.server_port,timeout=10)
        conn.request('GET',path,headers=headers)
        response=conn.getresponse()
        result=response.status,response.read().decode()
        conn.close()
        return result

    def test_explicit_external_host_auth_and_no_forwarded_trust(self):
        self.assertEqual(self.request()[0],200)
        self.assertEqual(self.request(auth=False)[0],401)
        self.assertEqual(self.request(extra={'Authorization':'Basic !!!'})[0],401)
        self.assertEqual(self.request(host='evil.invalid',extra={'X-Forwarded-Host':'panel.example.invalid','X-Forwarded-For':'127.0.0.1'})[0],403)
        self.assertEqual(self.request(host=f'127.0.0.1:{self.http.server_port}')[0],403)
        self.assertNotIn(self.password,self.request()[1])
        self.assertEqual(self.request('/solicitud?id=unknown',auth=False)[0],401)
        self.assertEqual(self.request('/documento?id=unknown',auth=False)[0],401)

    def test_credential_permissions_symlinks_and_http_origin_rejected(self):
        os.chmod(self.config,0o644)
        with self.assertRaises(ValueError):acceso.Access(self.config)
        os.chmod(self.config,0o600)
        linked=Path(self.tmp.name)/'link.json'
        linked.symlink_to(self.config)
        with self.assertRaises(ValueError):acceso.Access(linked)
        with self.assertRaises(ValueError):acceso.origin('http://panel.example.invalid')
        with self.assertRaises(ValueError):acceso.origin('https://user:password@panel.example.invalid')
        with self.assertRaises(ValueError):acceso.private_file(lector.ROOT/'secret.json')

    def test_external_post_requires_configured_origin_and_auth(self):
        model=self.app.model()
        key=model['tanda']['guiones'][0]['target']
        fields={'csrf':self.app.csrf,'target':key,'source_hash':model['targets'][key]['huella_revision'],
                'version':'0','motivo':'ENSAYO proxy privado','correccion':'Propuesta local pendiente.'}
        def post(origin,authorized):
            conn=http.client.HTTPConnection('127.0.0.1',self.http.server_port,timeout=10)
            headers={'Host':'panel.example.invalid','Origin':origin,'Content-Type':'application/x-www-form-urlencoded'}
            if authorized:headers['Authorization']=self.authorization
            conn.request('POST','/revision',urlencode(fields),headers)
            response=conn.getresponse()
            status=response.status
            response.read()
            conn.close()
            return status
        self.assertEqual(post('http://127.0.0.1',True),403)
        self.assertEqual(post('https://panel.example.invalid',False),401)
        self.assertEqual(post('https://panel.example.invalid',True),303)


class StrategyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.commit='19e2d7dc71db6c00c4e5c1e60239b9419b4f7bed'
        cls.prefix='_investigacion-onia/base-operativa/'
        result=subprocess.run(['git','cat-file','-e',cls.commit],capture_output=True)
        if result.returncode:
            raise unittest.SkipTest('Entrega publicada del productor todavía no disponible en los objetos de este checkout')

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='onia-estrategias-contrato-')
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        folder=self.prefix+cerebro.STRATEGY_ROOT
        files=subprocess.check_output(['git','ls-tree','-r','--name-only',self.commit,'--',folder],text=True).splitlines()
        for name in files:self.copy_source(name)
        sources=json.loads((self.base/cerebro.STRATEGY_ROOT/'fuentes.json').read_text())
        for row in sources['fuentes']:self.copy_source(self.prefix+row['ruta'])
        self.original=json.loads((self.base/cerebro.STRATEGY_INDEX).read_text())
        self.model={'documents':{},'targets':{},'clases':[('clase',row['inicio']) for row in self.original['workshop']['clases']]}
        self.patch=patch.object(op,'BASE',self.base)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def copy_source(self,name):
        path=self.base/name.removeprefix(self.prefix)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(subprocess.check_output(['git','show',self.commit+':'+name]))

    def test_published_export_valid_future_proposals_and_source_hashes(self):
        result=cerebro.strategies(self.model)
        self.assertEqual(result['actual'],'workshop-claude-20261113')
        self.assertEqual(len(result['estrategias']),4)
        self.assertEqual(len(result['estrategias'][0]['piezas']),10)
        self.assertTrue(all(row['propuesta_futura'] for row in result['estrategias'][1:]))
        self.assertEqual(result['metricas_reales']['ingresos_cobrados_Bs'],None)
        self.assertFalse(any('BITACORA' in row['ruta'] for row in self.model['documents'].values()))

    def test_absent_invalid_and_schema_reference_rejected(self):
        path=self.base/cerebro.STRATEGY_INDEX
        path.write_text('{invalid')
        with self.assertRaises(ValueError):cerebro.strategies(self.model)
        path.unlink()
        with self.assertRaises((OSError,ValueError)):cerebro.strategies(self.model)
        path.write_text(json.dumps(self.original))
        (self.base/cerebro.STRATEGY_ROOT/'estrategias.schema.json').write_text('{"$ref":"https://evil.invalid/schema"}')
        with self.assertRaises(ValueError):cerebro.strategies(self.model)

    def test_changed_business_source_path_escape_and_fake_approval_rejected(self):
        path=self.base/cerebro.STRATEGY_INDEX
        for modification in ('price','path','approval'):
            data=copy.deepcopy(self.original)
            if modification=='price':data['workshop']['precio_grupo_Bs']=60
            if modification=='path':data['workshop']['documento']='privado/contexto.md'
            if modification=='approval':data['workshop']['piezas'][0]['revision_editorial']='aprobado'
            path.write_text(json.dumps(data))
            with self.subTest(case=modification),self.assertRaises(ValueError):cerebro.strategies(self.model)
        path.write_text(json.dumps(self.original))
        decision=self.base/op.DECISIONS
        decision.write_bytes(decision.read_bytes()+b'\nENSAYO DE CAMBIO EN COPIA TEMPORAL')
        with self.assertRaises(ValueError):cerebro.strategies(self.model)

    def test_strategy_piece_malicious_text_is_inert_in_view(self):
        data=copy.deepcopy(self.original)
        piece=data['workshop']['piezas'][0]
        piece['contenido']+='\n<script>alert(1)</script><img src=x onerror=alert(1)>'
        path=self.base/cerebro.STRATEGY_INDEX
        path.write_text(json.dumps(data))
        document=self.base/piece['documento']
        document.write_text(document.read_text()+'\n'+piece['contenido'])
        self.model['estrategias']=cerebro.strategies(self.model)
        html=vistas_cerebro.strategies(self.model)
        self.assertNotIn('<script',html)
        self.assertNotIn('<img',html)
        self.assertIn('&lt;script',html)


if __name__=='__main__':
    unittest.main(verbosity=2)
