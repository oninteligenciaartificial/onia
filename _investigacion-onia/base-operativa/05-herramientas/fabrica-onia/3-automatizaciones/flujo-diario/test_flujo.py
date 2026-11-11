"""Ensayos SINTÉTICOS; ningún test llama Codex, APIs pagadas ni un harness real."""
import copy
from datetime import datetime
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

import comun
from comun import GENERATOR, digest, read_json
import fuentes
import motor
from adaptador_harness import LocalHarness, task_id

STAMP = '2026-11-11T18:30:00+00:00'
DAY = '2026-11-11'
URL = 'https://www.anthropic.com/news/ensayo-sintetico-fechado'
HTML = b'<html><head><title>ENSAYO</title><meta property="article:published_time" content="2026-11-11T00:00:00Z"></head><body><h1>ENSAYO SINTETICO</h1><time datetime="2026-11-11">Nov 11, 2026</time></body></html>'


def report():
    return fuentes.collect([URL], transport=lambda _: HTML, clock=lambda: STAMP)


def fixture(request):
    """Reutilizar textos FIJOS sólo para probar ensamblado, sin presentarlos como modelo nuevo."""
    g = motor.g
    brief = g.load(GENERATOR / 'entradas/brief.json')
    sources = g.load(GENERATOR / 'entradas/fuentes.json')
    draft = g.load(GENERATOR / 'entradas/redaccion-r1.json')
    brief['fecha_tanda'], brief['generado'] = request['dia'], request['creado']
    for i, candidate in enumerate(brief['candidatas'], 1):
        candidate['idea'] = 'Idea SINTÉTICA fija número ' + str(i)
    for i in range(len(brief['candidatas']) + 1, 21):
        brief['candidatas'].append({'id': f'I{i:02}', 'idea': f'ENSAYO {i}', 'decision': 'descartada', 'motivo': 'Dato sintético para validar contrato'})
    # Nada de los ejemplos web anteriores se trata como noticia nueva.
    sources['items'] = [s for s in sources['items'] if s['tipo'] == 'local']
    for row in sources['items']:
        row['consultada'] = request['creado']
    row = draft['guiones'][2]
    row.update(slot='evergreen', motivo_evergreen='ENSAYO SINTÉTICO: no validar hechos con una fixture.',
               fuentes=['D11', 'CEREBRO'], tipo_evidencia='ejemplo_ficticio', apertura='ENSAYO SINTÉTICO para revisar una agenda.',
               guion_hablado='ENSAYO SINTÉTICO para revisar una agenda. ' + 'Contá las tareas y revisá sus límites antes de usar la propuesta. '*5 + row['cta'])
    draft['autor']['nota'] = 'FI XTURE SINTÉTICA aportada; no generación por modelo real.'
    return brief, sources, draft


class FakeHarness:
    """Doble controlado del registro canónico, fuera del motor y sin persistir otra tarea real."""
    goal = staticmethod(LocalHarness.goal)
    check_scope = LocalHarness.check_scope
    scope = staticmethod(LocalHarness.scope)

    def __init__(self):
        self.row = {'exists': False, 'occupied': 0}
        self.calls = []
        self.input = None
        self.result_data = None
        self.fail = False

    def query(self, _):
        return copy.deepcopy(self.row)

    def invoke(self, op, request, before, path):
        self.calls.append(op)
        if self.fail:
            raise ValueError('untrusted SECRET exception')
        self.input = request
        ident, actor, route = self.scope(request)
        if op == 'registrar':
            self.row.update(exists=True, revision=1, state='preparado', sessions=[], actor=actor,
                            routes=[route], goal=self.goal(request), binding='SCOPE', commit=None, review={})
        else:
            assert before['revision'] == self.row['revision']
            self.row['revision'] += 1
            if op in {'lanzar', 'revisar'}:
                self.row['sessions'].append({'role': 'ejecutor' if op == 'lanzar' else 'revisor',
                    'alive': True, 'finished': False, 'rc': None, 'sid': 'sid-' + op})
            elif op == 'cerrar':
                self.row.update(commit='a'*40, state='para_revision')
            elif op == 'recoger':
                self.row['review'] = {'verdict': 'bueno', 'commit': self.row['commit']}

    def finish(self):
        self.row['sessions'][-1].update(alive=False, finished=True, rc=0)

    def result(self, request):
        return copy.deepcopy(self.result_data or fixture(request))


class Crash(BaseException):
    pass


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='onia-flujo-test-')
        self.root = Path(self.tmp.name)
        self.fake = FakeHarness()
        self.clock = lambda: STAMP
        self.engine = motor.Engine(self.root, self.fake, clock=self.clock)
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(lambda: self.engine.store.close())

    def step(self, report_value=None, trigger='reconciliar', authorized=True, provider=True):
        return self.engine.step(trigger, report_value,
            task_id(DAY) if authorized else None, provider)

    def register_launch(self):
        self.step(report(), 'entrada')
        self.step()
        self.assertEqual(self.fake.calls, ['registrar', 'lanzar'])

    def complete(self):
        self.register_launch()
        self.fake.finish()
        self.step()  # cerrar
        self.step()  # ensamblar + revisar
        self.fake.finish()
        self.step()  # recoger
        return self.step()  # observar dictamen

    def test_ciclo_completo_y_evento_duplicado(self):
        view = self.complete()
        cycle = view['ciclos'][0]
        self.assertEqual(cycle['fase'], 'para_revision_editorial')
        self.assertEqual(cycle['harness']['commit'], 'a'*40)
        self.assertEqual(len(cycle['resultado']['piezas']), 5)
        self.assertTrue(cycle['resultado']['sintetico'])
        self.assertEqual(self.fake.calls, ['registrar', 'lanzar', 'cerrar', 'revisar', 'recoger'])
        before = copy.deepcopy(cycle['resultado'])
        self.step(report(), 'entrada')
        self.assertEqual(len(self.engine.store.rows('ciclo')), 1)
        self.assertEqual(len(self.engine.store.rows('noticia')), 1)
        self.assertEqual(self.engine.projection()['ciclos'][0]['resultado'], before)
        self.assertEqual(self.fake.calls.count('lanzar'), 1)

    def test_caida_antes_despacho_reanuda_una_vez(self):
        self.step(report(), 'entrada')
        def crash(stage, op):
            if stage == 'antes_despacho' and op == 'lanzar':
                raise Crash()
        self.engine.hook = crash
        with self.assertRaises(Crash):
            self.step()
        self.restart()
        self.step()
        self.assertEqual(self.fake.calls.count('lanzar'), 1)

    def test_caida_despues_despacho_concilia_sid(self):
        self.step(report(), 'entrada')
        def crash(stage, op):
            if stage == 'despues_despacho' and op == 'lanzar':
                raise Crash()
        self.engine.hook = crash
        with self.assertRaises(Crash):
            self.step()
        self.restart()
        self.step()
        self.assertEqual(self.fake.calls.count('lanzar'), 1)
        self.assertEqual(self.engine.projection()['ciclos'][0]['fase'], 'redaccion_en_curso')

    def restart(self):
        self.engine.store.close()
        self.engine = motor.Engine(self.root, self.fake, clock=self.clock)

    def test_envio_incierto_no_reintenta_ni_filtra_excepcion(self):
        self.step(report(), 'entrada')
        self.fake.fail = True
        self.step()
        self.fake.fail = False
        self.step()
        self.assertEqual(self.fake.calls.count('lanzar'), 1)
        view = self.engine.projection()
        self.assertEqual(view['ciclos'][0]['error'], 'CONCILIACION_NECESARIA')
        self.assertNotIn('SECRET', json.dumps(view))

    def test_tres_cupos_y_falta_modelo_o_permiso(self):
        view = self.step(report(), 'entrada', provider=False)
        self.assertEqual(view['ciclos'][0]['error'], 'MODELO_NO_DISPONIBLE')
        self.assertEqual(self.fake.calls, [])
        view = self.step(authorized=False)
        self.assertEqual(view['ciclos'][0]['error'], 'AUTORIZACION_PENDIENTE')
        self.step()
        self.fake.row['occupied'] = 3
        self.step()
        self.assertEqual(self.fake.calls, ['registrar'])
        self.assertEqual(self.engine.projection()['ciclos'][0]['error'], 'TRES_CUPOS_OCUPADOS')

    def test_error_fuente_conserva_exito_y_resultado(self):
        before = self.complete()
        bad = report()
        bad.update(consulta='2026-11-11T19:00:00+00:00', items=[], errores=[{'codigo': 'LECTURA_FALLIDA', 'url': URL}])
        after = self.step(bad, 'entrada')
        self.assertEqual(after['fuente_ultimo_exito'], before['fuente_ultimo_exito'])
        self.assertEqual(after['ciclos'][0]['resultado'], before['ciclos'][0]['resultado'])
        self.assertTrue(any(e['codigo'] == 'LECTURA_FALLIDA' for e in after['errores']))

    def test_cambio_dia_la_paz_no_utc(self):
        self.engine.clock = lambda: '2026-11-12T03:59:59+00:00'
        self.step(report(), 'entrada', authorized=False)
        self.assertEqual([c['dia'] for c in self.engine.projection()['ciclos']], [DAY])
        self.engine.clock = lambda: '2026-11-12T04:00:00+00:00'
        self.step(report(), 'entrada', authorized=False)  # misma noticia no inicia otro trabajo
        self.assertEqual(len(self.engine.store.rows('ciclo')), 1)
        self.step(trigger='horario', authorized=False)
        self.assertEqual([c['dia'] for c in self.engine.projection()['ciclos']], [DAY, '2026-11-12'])

    def test_fuente_caida_no_es_evergreen_ni_sin_novedades(self):
        bad = report()
        bad.update(items=[], errores=[{'codigo': 'FALLO_FUENTE', 'url': URL}])
        self.step(bad, 'horario')
        self.assertEqual(self.engine.store.rows('ciclo'), [])
        self.assertIsNone(self.engine.projection()['fuente_ultimo_exito'])

    def test_resultado_invalido_no_sobrepone_original(self):
        self.complete()
        cycle = self.engine.store.get('ciclo', DAY)
        request = self.fake.input
        before = self.engine.projection()['ciclos'][0]['resultado']
        brief, sources, draft = fixture(request)
        brief['candidatas'].pop()
        with self.assertRaises(ValueError):
            self.engine.accept_result(cycle, request, brief, sources, draft)
        after = self.engine.projection()['ciclos'][0]
        self.assertEqual(after['error'], 'RESULTADO_INVALIDO')
        self.assertEqual(after['resultado'], before)

    def test_correccion_versionada_conserva_original_aprobado_o_grabado(self):
        self.complete()
        cycle = self.engine.store.get('ciclo', DAY)
        before = self.engine.projection()['ciclos'][0]['resultado']
        brief, sources, draft = fixture(self.fake.input)
        corrections = {'schema': 'onia-correcciones-v1', 'entrada_sha256': motor.g.fingerprint(draft),
            'version_base': 'r1', 'version_nueva': 'r2', 'reglas': [{'id': 'C1', 'motivo': 'ENSAYO',
            'piezas': ['T01'], 'campos': ['pendientes'], 'antes': draft['guiones'][0]['pendientes'], 'despues': 'Pendiente de ensayo humano revisado.'}]}
        original_files = {str(p): p.read_bytes() for p in (self.root/'v3').rglob('*') if p.is_file()}
        self.engine.accept_result(cycle, self.fake.input, brief, sources, draft, corrections)
        self.assertEqual(self.engine.store.get('resultado', before['huella']), before)
        self.assertTrue(all(Path(p).read_bytes() == raw for p, raw in original_files.items()))
        self.assertEqual(len(list((self.root/'v3').glob('guiones-*'))), 2)
        self.assertEqual(self.engine.projection()['ciclos'][0]['resultado']['version'], 'r2')
        self.assertIsNone(self.engine.projection()['ciclos'][0]['revision_tecnica'])
        self.step()
        self.assertEqual(self.engine.projection()['ciclos'][0]['fase'], 'correccion_pendiente_revision')

    def test_recupera_caida_despues_ensamblado_y_rechaza_salida_alterada(self):
        self.complete()
        cycle = self.engine.store.get('ciclo', DAY)
        brief, sources, draft = fixture(self.fake.input)
        self.engine.accept_result(cycle, self.fake.input, brief, sources, draft)
        path = next((self.root/'v3').glob('*/T01.md'))
        path.write_text('alterado')
        with self.assertRaises(ValueError):
            self.engine.accept_result(cycle, self.fake.input, brief, sources, draft)

    def test_revision_con_cambios_no_lanza_correcion_automatica(self):
        self.complete()
        cycle = self.engine.store.get('ciclo', DAY)
        cycle['fase'] = 'revision_tecnica_en_curso'
        self.engine.store.put('ciclo', DAY, cycle)
        self.fake.row['review']['verdict'] = 'cambios'
        self.step()
        self.step()
        self.assertEqual(self.engine.projection()['ciclos'][0]['fase'], 'correccion_pendiente')
        self.assertEqual(self.fake.calls.count('lanzar'), 1)
        self.assertEqual(len(self.fake.calls), 5)

    def test_revision_obsoleta_o_alcance_cambiado_bloquea(self):
        self.register_launch()
        self.fake.row['routes'] = ['otra/ruta']
        self.step()
        self.assertEqual(self.engine.projection()['ciclos'][0]['error'], 'CONCILIACION_NECESARIA')
        self.assertEqual(len(self.fake.calls), 2)

    def test_fallo_publicacion_conserva_export_anterior(self):
        self.complete()
        before = (self.root/'panel.json').read_bytes()
        with patch.object(motor, 'atomic', side_effect=OSError('fallo simulado')):
            with self.assertRaises(OSError):
                self.step()
        self.assertEqual((self.root/'panel.json').read_bytes(), before)



    def test_noticia_invalida_visible_sin_exito_inventado(self):
        bad = fuentes.collect([URL], transport=lambda _: b'<h1>Sin fecha</h1>', clock=lambda: STAMP)
        view = self.step(bad, 'entrada')
        self.assertIsNone(view['fuente_ultimo_exito'])
        self.assertEqual(view['ciclos'], [])
        self.assertEqual(view['errores'][0]['codigo'], 'NOTICIA_INVALIDA_O_FUENTE_CAIDA')

    def test_pedido_derivado_ausente_se_recupera_desde_journal(self):
        self.step(report(), 'entrada')
        path = next((self.root/'pedidos').glob('*.json'))
        before = path.read_bytes()
        path.unlink()
        self.restart()
        self.step()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.fake.calls.count('lanzar'), 1)

    def test_candidato_sin_critica_o_fuente_de_otro_pedido_rechazado(self):
        request = motor.make_request(DAY, report()['items'], STAMP, True)
        brief, sources, draft = fixture(request)
        brief['hipotesis_editoriales'] = []
        with self.assertRaises(ValueError):
            motor.validate_result(request, brief, sources, draft)
        brief, sources, draft = fixture(request)
        sources['items'].append({'tipo': 'web_primaria', 'url': 'https://www.anthropic.com/news/otra'})
        with self.assertRaises(ValueError):
            motor.validate_result(request, brief, sources, draft)

    def test_bloqueo_global_por_mismo_directorio(self):
        with comun.locked(self.root):
            with self.assertRaises(BlockingIOError):
                with comun.locked(self.root):
                    self.fail('No debe entrar dos veces')

    def test_intencion_de_pedido_se_recupera_tras_corte_antes_de_archivo(self):
        with patch.object(motor, 'immutable', side_effect=OSError('corte')):
            with self.assertRaises(OSError):
                self.step(report(), 'entrada')
        self.restart()
        self.step(report(), 'entrada')
        self.assertEqual(len(self.engine.store.rows('ciclo')), 1)
        self.assertEqual(self.fake.calls, ['registrar'])

    def test_revision_obsoleta_no_se_aplica(self):
        self.complete()
        cycle = self.engine.store.get('ciclo', DAY)
        cycle['fase'] = 'revision_tecnica_en_curso'
        self.engine.store.put('ciclo', DAY, cycle)
        self.fake.row['review']['commit'] = 'b'*40
        self.step()
        self.assertEqual(self.engine.projection()['ciclos'][0]['error'], 'CONCILIACION_NECESARIA')


class SourcesTests(unittest.TestCase):
    def test_metadatos_reales_precision_dia_y_rechazos(self):
        article = fuentes.article(HTML, URL, STAMP)
        self.assertEqual(article['publicada'], DAY)
        self.assertEqual(article['precision'], 'dia')
        for html in (b'<h1>Challenge</h1>', HTML.replace(b'Nov 11', b'Nov 10'), HTML.replace(b'2026-11-11T', b'2027-11-11T')):
            with self.assertRaises(ValueError):
                fuentes.article(html, URL, STAMP)
        for url in ('http://www.anthropic.com/news/x', 'https://evil.test/news/x', URL+'?token=PRIVATE', 'https://www.anthropic.com@evil.test/news/x', URL+'/../../private'):
            with self.assertRaises(ValueError):
                fuentes.canonical(url)

    def test_indice_rotacion_limites_y_no_redirecciones(self):
        calls = []
        index = '<h1>News</h1>' + ''.join(f'<a href="/news/a-{i}">x</a>' for i in range(30)) + '<a href="https://evil.test/x">x</a>'
        def transport(url):
            calls.append(url)
            return index.encode() if url == fuentes.INDEX else HTML
        first = fuentes.collect(transport=transport, clock=lambda: STAMP)
        self.assertEqual(len(calls), 4)
        self.assertEqual(len(first['items']), 3)
        second = fuentes.collect(transport=transport, cursor=first['cursor'], clock=lambda: STAMP)
        self.assertNotEqual(first['items'][0]['url'], second['items'][0]['url'])
        with self.assertRaises(comun.lector.Rejected):
            comun.lector.NoRedirect().redirect_request(None, None, 302, None, None, 'https://evil.test')

    def test_error_no_se_convierte_en_lista_vacia_exitosa(self):
        def broken(_):
            raise TimeoutError('secret')
        result = fuentes.collect([URL], transport=broken, clock=lambda: STAMP)
        self.assertEqual(result['items'], [])
        self.assertTrue(result['errores'])
        self.assertNotIn('secret', json.dumps(result))


class AdapterTests(unittest.TestCase):
    def test_api_existente_con_revision_subagentes_cero_y_sin_shell(self):
        adapter = LocalHarness.__new__(LocalHarness)
        adapter.base, adapter.operation = Path('/tmp/coordinador-no-usado'), Path('/tmp/operacion-no-usada')
        adapter.sessions = types.SimpleNamespace(launch=Mock(), close=Mock(), collect_review=Mock())
        request = motor.make_request(DAY, [], STAMP, True)
        _, actor, route = adapter.scope(request)
        before = {'exists': True, 'revision': 7, 'binding': 'SCOPE', 'goal': adapter.goal(request),
                  'actor': actor, 'routes': [route], 'sessions': [], 'occupied': 2}
        adapter.query = Mock(return_value=copy.deepcopy(before))
        with patch.object(Path, 'read_bytes', return_value=(comun.BASE/'05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md').read_bytes()):
            adapter.invoke('lanzar', request, before, Path('/tmp/no-se-lee'))
        self.assertEqual(adapter.sessions.launch.call_args.kwargs, {'approved': True, 'reviewer': None,
            'model': 'gpt-6.1-sol', 'effort': 'high', 'auth_chatgpt': True, 'subagents': 0})
        adapter.invoke('cerrar', request, before, Path('/tmp/no-se-lee'))
        self.assertTrue(adapter.sessions.close.call_args.kwargs['retain_worktree'])
        adapter.invoke('revisar', request, before, Path('/tmp/no-se-lee'))
        self.assertNotEqual(adapter.sessions.launch.call_args.kwargs['reviewer'], actor)
        adapter.invoke('recoger', request, before, Path('/tmp/no-se-lee'))
        self.assertEqual(adapter.sessions.collect_review.call_count, 1)
        with self.assertRaises(ValueError):
            adapter.invoke('shell', request, before, Path('/tmp/no-se-lee'))
        adapter.query.return_value['revision'] = 8
        with self.assertRaises(ValueError):
            adapter.invoke('lanzar', request, before, Path('/tmp/no-se-lee'))


    def test_registrar_preparar_y_asignar_en_api_unica(self):
        adapter = LocalHarness.__new__(LocalHarness)
        adapter.base = Path('/tmp/coordinador-no-usado')
        request = motor.make_request(DAY, [], STAMP, True)
        ident, actor, route = adapter.scope(request)
        row = {'objetivo': adapter.goal(request), 'revision': 1, 'asignacion': None}
        adapter.harness = types.SimpleNamespace(prepare=Mock())
        adapter.trabajo = types.SimpleNamespace(read_task=Mock(return_value=row), assign=Mock())
        adapter.query = Mock(side_effect=[{'exists': False}, {'exists': True, 'goal': row['objetivo'], 'routes': [route], 'actor': actor}])
        adapter.invoke('registrar', request, {'exists': False}, Path('/tmp/pedido-no-se-lee'))
        self.assertEqual(adapter.harness.prepare.call_count, 1)
        self.assertFalse(adapter.harness.prepare.call_args.kwargs['shared'])
        adapter.trabajo.assign.assert_called_once_with(adapter.base, ident, 1, actor, [route])

    def test_programacion_deshabilitada_y_hora_pendiente(self):
        import programacion
        config = comun.read_json(comun.HERE/'config.ejemplo.json')
        self.assertFalse(programacion.plan(config)['habilitada'])
        self.assertIsNone(programacion.plan(config)['hora_tanda'])
        config['habilitada'] = True
        with self.assertRaises(ValueError):
            programacion.plan(config)

    def test_generador_privado_rechaza_raiz_publica_y_respeta_dia_la_paz(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'v3'
            root.mkdir(mode=0o755)
            with self.assertRaises(ValueError):
                motor.g.target_path(root/'r1', root)
            root.chmod(0o700)
            request = motor.make_request('2026-11-10', [], '2026-11-11T03:30:00+00:00', True)
            brief, sources, draft = fixture(request)
            motor.g.build(brief, sources, draft, None, root/'r1', output_root=root)
            self.assertTrue((root/'r1/redaccion-original.json').is_file())
            self.assertEqual(comun.read_json(root/'r1/estado-fabrica.json')['schema'], 'onia-fabrica-estado-privado-v1')

    def test_raiz_privada_no_git_no_enlaces_y_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'link').symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                comun.private_root(root/'link'/'datos')
            with self.assertRaises(ValueError):
                comun.private_root(comun.REPO/'privado-no-crear')
            with self.assertRaises(ValueError):
                motor.g.target_path(root/'escape', root/'v3')


if __name__ == '__main__':
    unittest.main()
