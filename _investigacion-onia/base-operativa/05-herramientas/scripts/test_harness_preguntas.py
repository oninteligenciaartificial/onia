"""Consultas: repo Git temporal, concurrencia y procesos falsos; sin servicios/LLM."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

import harness_boss as boss
import harness_preguntas as q
import harness_sesiones as sessions
import test_harness_boss as fixtures


class QuestionTests(unittest.TestCase):
    def setUp(self):
        self.bridge=fixtures.BridgeTests(methodName='runTest');self.bridge.setUp()
        self.addCleanup(self.bridge.doCleanups)
        self.config=dict(self.bridge.config,preguntar_habilitado=True)
        self.base=self.bridge.base;self.root=self.bridge.root
        self.config_path=self.root/'config.json';boss.private_write(self.config_path,self.config)
        self.repo=self.bridge.repo
        # Fixture base uses the production layout.
        self.assertEqual(self.base,self.repo/q.BASE)
        for name in q.MANDATORY:
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('Contexto de prueba. Nombre final: Taller de prueba.\n')
        self.bridge.fixture.git('add','.');self.bridge.fixture.git('commit','-m','contexto pregunta')
        self.bridge.fixture.git('push','origin','master')
        self.patch=patch.object(q.delegation,'quota_snapshot',return_value={'used_percent':20,'fecha':'fixture'})
        self.patch.start();self.addCleanup(self.patch.stop)

    def request(self,ident='pregunta-1',text='¿Cuál es el nombre final?'):
        return {'version':1,'operacion':'preguntar','id_pregunta':ident,'texto':text}

    def fake(self,config,folder,prompt,deadline,slot):
        self.assertIn('Taller de prueba',prompt)
        self.assertEqual(sessions.question_slots(Path(config['operacion'])),1)
        return {'respuesta':'Nombre: Taller de prueba.','modelo_observado':None}

    def handle(self,req=None,runner=None):
        return q.handle(self.config,boss.request(req or self.request()),self.config_path,runner=runner or self.fake)

    def test_roundtrip_repeat_log_no_repo_write_and_slot_released(self):
        before=self.bridge.fixture.git('status','--porcelain')
        a=self.handle();b=self.handle(runner=lambda *a: self.fail('no relanzar'))
        self.assertTrue(a['ok']);self.assertTrue(b['repetida'])
        self.assertEqual(a['respuesta'],b['respuesta'])
        self.assertEqual(before,self.bridge.fixture.git('status','--porcelain'))
        log=boss.private_read(self.root/'preguntas/pregunta-1/registro.json')
        self.assertEqual(log['texto'],self.request()['texto'])
        self.assertEqual(log['respuesta']['respuesta'],a['respuesta'])
        self.assertEqual(sessions.question_slots(Path(self.config['operacion'])),0)

    def test_trial_question_is_tagged_and_stop_before_runner_blocks(self):
        import harness_ensayo as trial
        from test_harness_ensayo import install_trial
        op = Path(self.config['operacion'])
        value = install_trial(op, self.base, ['pregunta-1', 'pregunta-2'])
        def answer(config, folder, prompt, deadline, slot):
            current = boss.private_read(slot)
            self.assertEqual(current['ensayo_sha256'], trial.digest(value))
            self.assertEqual(current['base'], str(self.base))
            return self.fake(config, folder, prompt, deadline, slot)
        self.assertTrue(self.handle(runner=answer)['ok'])
        with patch.object(q, 'context', side_effect=lambda *_:
                          (boss.private_write(op / trial.DIRECTORY / 'STOP', {'motivo': 'prueba'})
                           or ('a' * 40, [], 'contexto'))):
            with patch.object(q, 'answer') as runner:
                result = self.handle(req=self.request('pregunta-2'), runner=runner)
                self.assertFalse(result['ok'])
                runner.assert_not_called()

    def test_bridge_dispatch_and_schema(self):
        with patch.object(q,'handle',return_value={'ok':True}) as call:
            self.assertTrue(boss.handle(self.config,self.request(),config_path=self.config_path)['ok'])
            call.assert_called_once()
        for change in [{'id_pregunta':'../../bad'},{'texto':''},{'texto':'a'*2001},{'modelo':'otro'},
                       {'texto':'ghp_'+'x'*24},{'version':True}]:
            with self.subTest(change=change),self.assertRaises(boss.Rejected):boss.request(self.request()|change)

    def test_same_id_different_text_rejected(self):
        self.handle()
        with self.assertRaisesRegex(boss.Rejected,'reutilizado'):self.handle(self.request(text='Otra cosa'))

    def test_daily_limit_includes_failed_and_uses_local_day(self):
        for i in range(20):boss.private_write(self.root/f'preguntas/old-{i}/registro.json',{'dia':q.day(),'estado':'fallida'})
        with self.assertRaisesRegex(boss.Rejected,'20_preguntas'):self.handle()
        with patch.object(q,'day',return_value='2099-01-01'):self.assertTrue(self.handle()['ok'])

    def test_quota_pause_and_opt_in_fail_closed(self):
        for change in [{'pausado':True},{'preguntar_habilitado':False}]:
            boss.private_write(self.config_path,self.config|change)
            with self.assertRaisesRegex(boss.Rejected,'no_habilitado'):self.handle()
        boss.private_write(self.config_path,self.config)
        with patch.object(q.delegation,'quota_snapshot',return_value={'used_percent':90}):
            with self.assertRaisesRegex(boss.Rejected,'tope_cuota'):self.handle()
        self.assertFalse((self.root/'preguntas/pregunta-1/registro.json').exists())

    def test_question_uses_private_quota_policy_and_blocks_at_limit(self):
        boss.private_write(self.config_path,self.config|{'politica_cuota':{
            'max_usado':95,'autorizacion_sergio':'fixture explícito, no permiso real'}})
        with patch.object(q.delegation,'quota_snapshot',return_value={'used_percent':94}):
            self.assertTrue(self.handle()['ok'])
        with patch.object(q.delegation,'quota_snapshot',return_value={'used_percent':95}):
            with self.assertRaisesRegex(boss.Rejected,'tope_cuota_configurado'):
                self.handle(self.request(ident='pregunta-bloqueada'))
        self.assertFalse((self.root/'preguntas/pregunta-bloqueada/registro.json').exists())

    def test_shared_capacity_and_stale_pid(self):
        op=Path(self.config['operacion'])
        for i in range(3):boss.private_write(op/f'preguntas-slots/q-{i}.json',{'estado':'respondiendo','vence':time.time()+30})
        with self.assertRaisesRegex(ValueError,'Máximo 3'):self.handle()
        with self.assertRaisesRegex(ValueError,'Máximo 3'):sessions.check_capacity([], 'real-task',self.base,[],'revisor',root=op)
        for i in range(3):boss.private_write(op/f'preguntas-slots/q-{i}.json',{'estado':'cerrada','vence':time.time()+30})
        self.assertEqual(sessions.question_slots(op),0)
        boss.private_write(op/'preguntas-slots/stale.json',{'estado':'respondiendo','pid':os.getpid(),'pid_inicio':'not-the-start','vence':0})
        self.assertEqual(sessions.question_slots(op),0)
        boss.private_write(op/'preguntas-slots/live.json',{'estado':'respondiendo','pid':os.getpid(),'pid_inicio':sessions.process_start(os.getpid()),'vence':0})
        self.assertEqual(sessions.question_slots(op),1)

    def test_timeout_cached_no_automatic_retry(self):
        def slow(*a):raise boss.Rejected('pregunta_timeout')
        r=self.handle(runner=slow);self.assertEqual(r['error'],'pregunta_timeout')
        r2=self.handle(runner=lambda *a:self.fail('no retry'));self.assertTrue(r2['repetida'])
        self.assertEqual(sessions.question_slots(Path(self.config['operacion'])),0)

    def test_context_only_published_regular_allowed_files(self):
        excluded=[q.BASE+'privado/secret.md',q.BASE+'04-operacion-agentes/auth.json']
        for name in excluded:
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('SECRET-CANARY')
        link=self.repo/(q.BASE+'04-operacion-agentes/link.md');link.symlink_to('/etc/passwd')
        safe=self.repo/(q.BASE+'04-operacion-agentes/SESIONES.md');safe.write_text('nombre final\nBearer '+'a'*30)
        self.bridge.fixture.git('add','.');self.bridge.fixture.git('commit','-m','sources');self.bridge.fixture.git('push','origin','master')
        (self.repo/q.MANDATORY[0]).write_text('DIRTY-CANARY')
        commit,names,text=q.context(self.config,'nombre final',time.monotonic()+20)
        self.assertNotIn('SECRET-CANARY',text);self.assertNotIn('DIRTY-CANARY',text)
        self.assertNotIn('a'*30,text);self.assertNotIn(str(link.relative_to(self.repo)),names)
        self.assertEqual(names[:4],q.MANDATORY)

    def test_command_and_environment_no_model_control_or_inherited_secrets(self):
        cmd=q.command(self.root,self.root/'empty');env=q.environment(self.root)
        self.assertIn('--ignore-user-config',cmd);self.assertIn('--ephemeral',cmd)
        self.assertIn('model_reasoning_effort="low"',cmd);self.assertIn('gpt-6.1-sol',cmd)
        self.assertIn('permissions.pregunta.network.enabled=false',cmd)
        for x in ['shell_tool','apps','plugins','multi_agent','hooks','view_image']:
            self.assertIn(x,cmd)
        self.assertNotIn('OPENAI_API_KEY',env);self.assertNotIn('SSH_AUTH_SOCK',env)
        self.assertEqual(env['HOME'],str(self.root))

    def test_extract_rejects_tool_calls_and_sanitizes_output(self):
        with self.assertRaisesRegex(boss.Rejected,'herramienta'):
            q.extract(json.dumps({'item':{'type':'command_execution'}}),'')
        with self.assertRaisesRegex(boss.Rejected,'excesiva'):
            q.extract(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'a'*12001}})+'\n'+json.dumps({'type':'turn.completed'}),'')
        good=q.extract(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'Bearer '+'a'*30}})+'\n'+json.dumps({'type':'turn.completed'}),'model: gpt-6.1-sol\n')
        self.assertNotIn('a'*30,good['respuesta']);self.assertIsNone(good['modelo_observado'])

    def test_busy_bridge_rejected_without_wait_or_reservation(self):
        with boss.locked(self.root):
            start=time.monotonic()
            with self.assertRaisesRegex(boss.Rejected,'ocupado'):self.handle()
            self.assertLess(time.monotonic()-start,1)

    def test_required_context_invalid_utf8_fails_closed(self):
        (self.repo/q.MANDATORY[0]).write_bytes(b'\xff\xfe')
        self.bridge.fixture.git('add','.');self.bridge.fixture.git('commit','-m','invalid context');self.bridge.fixture.git('push','origin','master')
        r=self.handle();self.assertEqual(r['error'],'contexto_obligatorio_invalido')

    def test_json_secret_and_error_message_never_returned(self):
        secret='fictional-value-for-test-only'
        self.assertNotIn(secret,q.clean('"access_token": "'+secret+'"'))
        with self.assertRaisesRegex(boss.Rejected,'^runtime_respuesta_fallida$'):
            q.extract(json.dumps({'item':{'type':'error','message':secret}}),'')
        with self.assertRaisesRegex(boss.Rejected,'vacia'):
            q.extract(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'partial'}}),'')

    def test_cannot_write_capacity_or_counter_while_in_flight(self):
        def nested(config,folder,prompt,deadline,slot):
            with self.assertRaisesRegex(boss.Rejected,'en_curso_o_incierta'):self.handle()
            synthetic=[(self.base,{'id':str(i),'sesiones':[{'rol':'revisor','dry_run':True,'estado':'simulada'}]}) for i in range(2)]
            with self.assertRaisesRegex(ValueError,'Máximo 3'):
                sessions.check_capacity(synthetic,'another',self.base,[],'ejecutor',root=Path(config['operacion']))
            return {'respuesta':'final'}
        self.assertTrue(self.handle(runner=nested)['ok'])


    def test_supervisor_gate_and_kill_group_on_timeout(self):
        # Fake Codex process would leave a child if only its parent were terminated.
        home=self.root/'fake-home';home.mkdir();(home/'empty').mkdir()
        fake=self.root/'fake-bin';fake.mkdir();exe=fake/'codex'
        pidfile=home/'child.pid'
        exe.write_text('#!/usr/bin/python3\nimport subprocess,time\np=subprocess.Popen(["/usr/bin/sleep","30"])\nopen('+repr(str(pidfile))+',"w").write(str(p.pid))\ntime.sleep(30)\n');exe.chmod(0o700)
        # A wrapper patches only environment routing, retaining production supervisor logic.
        script=self.root/'worker.py';script.write_text('import sys\nsys.path.insert(0,'+repr(str(Path(q.__file__).parent))+')\nimport harness_preguntas as q\noldcmd=q.command\nq.command=lambda h,c: ['+repr(str(exe))+']+oldcmd(h,c)[1:]\nq.environment=lambda h: {"PATH":'+repr(str(fake))+',"HOME":str(h)}\nq.worker()\n')
        proc=subprocess.Popen([sys.executable,str(script)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,start_new_session=True)
        self.addCleanup(lambda:proc.poll() is None and os.killpg(proc.pid,9))
        time.sleep(.1);self.assertFalse(pidfile.exists()) # no input gate, no Codex
        data={'pid':proc.pid,'parent':os.getpid(),'parent_start':sessions.process_start(os.getpid()),'deadline':time.monotonic()+.5,'home':str(home),'prompt':'fixture'}
        out,_=proc.communicate((json.dumps(data)+'\n').encode(),timeout=4)
        self.assertIn('timeout',json.loads(out)['error']);self.assertIsNotNone(proc.returncode)
        if pidfile.exists():
            child=int(pidfile.read_text())
            for _ in range(30):
                if sessions.process_start(child) is None:break
                time.sleep(.02)
            self.assertIsNone(sessions.process_start(child))


if __name__=='__main__':unittest.main()
