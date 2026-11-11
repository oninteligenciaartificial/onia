"""Pruebas locales con fixture SINTÉTICO. Sin red externa ni mutaciones del harness."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import http.client
from http.server import HTTPServer
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

import lector
import operacion
import panel
import servidor

FIXTURE = operacion.PANEL_ROOT + '/fixtures/tarea-sintetica/estado-fabrica.json'


class Forms(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.forms = []
        self.capture_review = False
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'form':
            self.capture_review = attrs.get('method') == 'post' and attrs.get('action') == '/revision'
            if self.capture_review:
                self.forms.append({})
        if tag == 'input' and attrs.get('type') == 'hidden' and self.capture_review:
            self.forms[-1][attrs['name']] = attrs.get('value', '')

    def handle_endtag(self, tag):
        if tag == 'form':
            self.capture_review = False


class ContractTests(unittest.TestCase):
    def test_own_delivery_export_and_fixture_together(self):
        model = operacion.build([operacion.PANEL_ROOT + '/estado-fabrica.json', FIXTURE])
        self.assertEqual(model['errores'], [])
        self.assertEqual(model['exports_panel'][0]['id'], 'cerebro-panel-usable-20261109')

    def test_six_factories_pending_and_fixture_explicit(self):
        model = operacion.build([FIXTURE])
        self.assertEqual(len(model['fabricas']), 6)
        self.assertEqual(model['errores'], [])
        self.assertTrue(model['fabricas'][0]['exports'][0]['sintetico'])
        self.assertTrue(all(row['exports'] == [] for row in model['fabricas'][1:]))
        html = panel.render(model['tanda'], model)
        self.assertIn('ENSAYO SINTÉTICO', html)
        self.assertIn('horarios sustituidos', html)
        self.assertEqual([row[1] for row in model['clases']], ['2026-11-13T20:00:00-04:00', '2026-11-14T14:00:00-04:00', '2026-11-16T20:00:00-04:00'])
        self.assertIn("form-action 'none'", html)
        self.assertNotIn('<form', html)

    def test_export_invalid_types_states_dates_and_paths(self):
        original = json.loads((lector.BASE / FIXTURE).read_text())
        invalid = [[], {**original, 'schema': 'other'}, {**original, 'estado': 'aceptado'},
                   {**original, 'generado': '2026-11-11T12:00:00'}, {**original, 'pasos': None},
                   {**original, 'fuente': 'privado/contexto.md'},
                   {**original, 'fuente': 'https://example.invalid/file'},
                   {**original, 'fabrica': 'edicion'},
                   {**original, 'pasos': original['pasos'] * 2},
                   {**original, 'pendientes': [{'motivo': 'falta responsable'}]},
                   {**original, 'entregables': [{'nombre': 'escape', 'ruta': operacion.PRODUCERS['whatsapp'] + '/README.md'}]}]
        for data in invalid:
            with self.subTest(data=str(data)[:60]), patch.object(operacion, 'read_relative', return_value=json.dumps(data).encode()):
                with self.assertRaises((ValueError, TypeError)):
                    operacion.load_export(FIXTURE, {}, {})

    def test_bad_export_does_not_authorize_partial_targets(self):
        data = json.loads((lector.BASE / FIXTURE).read_text())
        data['pendientes'] = [{}]
        read = operacion.read_relative
        def source(value, roots):
            return json.dumps(data).encode() if value == FIXTURE else read(value, roots)
        with patch.object(operacion, 'read_relative', side_effect=source):
            model = operacion.build([FIXTURE])
        self.assertEqual(len(model['errores']), 1)
        self.assertEqual(len(model['targets']), 5)  # Sólo la tanda real.
        self.assertFalse(any('/fixtures/' in d['ruta'] for d in model['documents'].values()))

    def test_duplicate_path_and_missing_export_visible(self):
        model = operacion.build([FIXTURE, FIXTURE, operacion.PRODUCERS['whatsapp'] + '/ausente/estado-fabrica.json'])
        self.assertEqual(len(model['errores']), 2)
        self.assertEqual(len(model['targets']), 9)

    def test_routes_reject_traversal_absolute_private_url_and_symlinks(self):
        with tempfile.TemporaryDirectory(prefix='onia-rutas-') as tmp, patch.object(operacion, 'BASE', Path(tmp)):
            base = Path(tmp)
            (base / 'permitido').mkdir()
            (base / 'permitido' / 'link').symlink_to('/tmp', target_is_directory=True)
            for path in ('/etc/passwd', 'permitido/../secreto', 'permitido//archivo', 'permitido/./archivo',
                         'https://example.invalid', 'permitido/privado/a.md', 'permitido/link/a.md',
                         'permitido/a.md?token=x', 'permitido\\a.md', 'permitido/.git/config'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    operacion.relative_path(path, ['permitido'])

    def test_future_producer_export_with_exact_contract(self):
        data = json.loads((lector.BASE / FIXTURE).read_text())
        with tempfile.TemporaryDirectory(prefix='onia-export-') as tmp, patch.object(operacion, 'BASE', Path(tmp)):
            root = operacion.PRODUCERS['guiones'] + '/salida/ensayo'
            directory = Path(tmp) / root
            directory.mkdir(parents=True)
            data['fuente'] = root + '/informe.md'
            data['pasos'] = [{'id': 'paso', 'nombre': 'Evaluar', 'estado': 'completado', 'evidencias': [data['fuente']]}]
            data['entregables'] = [{'nombre': 'Resultado', 'ruta': data['fuente']}]
            (directory / 'informe.md').write_text('ENSAYO SINTÉTICO en /tmp')
            (directory / 'estado-fabrica.json').write_text(json.dumps(data))
            exports, targets = {}, {}
            result = operacion.load_export(root + '/estado-fabrica.json', exports, targets)
            self.assertFalse(result['sintetico'])  # La etiqueta se deriva de la ruta de fixtures del panel.
            self.assertEqual(len(targets), 2)
            self.assertTrue(any('texto' in row['original'] for row in targets.values()))

    def test_missing_tanda_visible_and_existing_reader_usable(self):
        model = operacion.build(tanda_path=operacion.PRODUCERS['guiones'] + '/ausente/guiones-panel.json')
        self.assertIsNone(model['tanda'])
        self.assertEqual(len(model['errores']), 1)
        self.assertEqual(model['targets'], {})

    def test_brain_reuses_existing_validation_and_filters(self):
        result = operacion.brain('revision', 'workshop')
        self.assertGreater(result['cantidad'], 0)
        self.assertTrue(all('ficha' in item and 'pasaje' in item for item in result['resultados']))
        self.assertEqual(operacion.brain('tributacion', '')['cantidad'], 0)
        with self.assertRaises(ValueError):
            operacion.brain('oferta', 'aceptar')

    def test_xss_escaped_in_export_and_static_html(self):
        data = json.loads((lector.BASE / FIXTURE).read_text())
        data['pasos'][0]['nombre'] = '<img src=x onerror=alert(1)>'
        read = operacion.read_relative
        with patch.object(operacion, 'read_relative', side_effect=lambda p, roots: json.dumps(data).encode() if p == FIXTURE else read(p, roots)):
            model = operacion.build([FIXTURE])
        html = panel.render(model['tanda'], model)
        self.assertIn('&lt;img', html)
        self.assertNotIn('<img', html)
        self.assertNotIn('<script', html)


class LocalFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='onia-revision-sintetica-')
        self.start()

    def start(self):
        self.app = servidor.Application(self.tmp.name, [FIXTURE])
        self.http = HTTPServer(('127.0.0.1', 0), servidor.handler_for(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever, kwargs={'poll_interval': 0.02})
        self.thread.start()

    def stop(self):
        self.http.shutdown()
        self.thread.join(timeout=5)
        self.http.server_close()

    def tearDown(self):
        self.stop()
        self.tmp.cleanup()

    def request(self, method='GET', path='/', fields=None, headers=None, raw=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.http.server_port, timeout=10)
        values = {'Origin': f'http://127.0.0.1:{self.http.server_port}', 'Content-Type': 'application/x-www-form-urlencoded'}
        values.update(headers or {})
        body = raw if raw is not None else (urlencode(fields).encode() if fields is not None else None)
        connection.request(method, path, body, values)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read().decode()
        connection.close()
        return result

    def form(self):
        status, _, html = self.request()
        self.assertEqual(status, 200)
        values = Forms(html).forms[3]  # Entregable sintético tras los tres pasos.
        return {**values, 'motivo': 'ENSAYO SINTÉTICO · revisar acción', 'correccion': 'Proponer una acción evaluable con su criterio.'}

    def test_task_correction_restart_second_version_and_original(self):
        before = (lector.BASE / FIXTURE).read_bytes()
        fields = self.form()
        status, headers, _ = self.request('POST', '/revision', fields)
        self.assertEqual(status, 303)
        self.assertIn('guardado=1', headers['Location'])
        self.stop()
        self.start()  # Servidor y Application nuevos sobre la misma SQLite.
        _, _, html = self.request()
        self.assertIn(fields['correccion'], html)
        self.assertIn('Resultado original v1', html)
        fields = self.form()
        fields['correccion'] = 'Segunda propuesta sintética con motivo conservado.'
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        history = self.app.reviews.history(fields['target'])
        self.assertEqual([row['version'] for row in history], [1, 2])
        self.assertTrue(all(row['estado'] == 'pendiente' for row in history))
        self.assertIn('texto', json.loads(history[0]['original']))
        self.assertEqual((lector.BASE / FIXTURE).read_bytes(), before)

    def test_stale_version_and_stale_source_preserve_input(self):
        fields = self.form()
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)  # Doble envío idéntico, idempotente.
        fields['solicitud_id'] = 'f' * 64  # Otra propuesta sobre una versión obsoleta.
        status, _, html = self.request('POST', '/revision', fields)
        self.assertEqual(status, 409)
        self.assertIn(fields['correccion'], html)
        fields = self.form()
        fields['source_hash'] = 'alterado'
        self.assertEqual(self.request('POST', '/revision', fields)[0], 409)
        self.assertEqual(len(self.app.reviews.history(fields['target'])), 1)

    def test_original_accessible_when_export_leaves_selection(self):
        fields = self.form()
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        self.app.exports = ()
        status, _, html = self.request()
        self.assertEqual(status, 200)
        self.assertIn('Revisiones de fuentes anteriores', html)
        self.assertIn(fields['correccion'], html)
        self.assertIn('Resultado original v1', html)

    def test_changed_result_bytes_require_refresh_and_keep_original(self):
        fields = self.form()
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        fields = self.form()
        read = operacion.read_relative
        result_path = FIXTURE.replace('estado-fabrica.json', 'resultado.md')
        def changed(path, roots):
            raw = read(path, roots)
            return raw + b'\nENSAYO SINTETICO de nueva version' if path == result_path else raw
        with patch.object(operacion, 'read_relative', side_effect=changed):
            self.assertEqual(self.request('POST', '/revision', fields)[0], 409)
            self.assertIn('la fuente actual tiene otros bytes', self.request()[2])
        self.assertEqual(len(self.app.reviews.history(fields['target'])), 1)

    def test_invalid_post_origin_csrf_target_version_empty_and_size(self):
        fields = self.form()
        for mutation in ({'csrf': 'otra'}, {'target': '../../harness'}, {'version': '-1'},
                         {'motivo': ''}, {'correccion': 'x' * 12001}, {'aprobacion': 'si'}):
            with self.subTest(mutation=list(mutation)):
                self.assertEqual(self.request('POST', '/revision', {**fields, **mutation})[0], 409)
        self.assertEqual(self.request('POST', '/revision', fields, {'Origin': 'https://externo.invalid'})[0], 403)
        self.assertEqual(self.request(headers={'Host': 'externo.invalid'})[0], 403)
        self.assertEqual(self.request('POST', '/revision', raw=b'x' * (192 * 1024 + 1))[0], 409)
        self.assertEqual(self.request('POST', '/revision', raw=b'csrf=%FF')[0], 409)
        self.assertEqual(self.app.reviews.history(fields['target']), [])

    def test_unicode_maximum_length_round_trip(self):
        fields = self.form()
        fields['motivo'] = '\U0001f4dd' * 2000
        fields['correccion'] = '\U0001f4dd' * 12000
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        self.assertEqual(self.app.reviews.history(fields['target'])[0]['correccion'], fields['correccion'])

    def test_real_tanda_review_preserves_editorial_bytes(self):
        source = lector.BASE / operacion.HISTORIC_TANDA
        raw = source.read_bytes()
        fields = Forms(self.request()[2]).forms[-5]
        fields.update(motivo='ENSAYO SINTÉTICO sobre T01 existente', correccion='Revisar los horarios antes de usar esta versión.')
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        original = json.loads(self.app.reviews.history(fields['target'])[0]['original'])
        self.assertEqual(original['id'], 'T01')
        self.assertEqual(source.read_bytes(), raw)

    def test_static_preview_omits_private_reviews_and_preserves_existing_output(self):
        fields = self.form()
        fields['correccion'] = 'SINTETICO-PRIVADO-SOLO-SQLITE'
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        output = Path(self.tmp.name) / 'preview-sintetico'
        with patch.object(lector, 'own_output', side_effect=lambda p: Path(p)):
            servidor.preview(self.app, output)
            with self.assertRaises(FileExistsError):
                servidor.preview(self.app, output)
        html = (output / 'panel.html').read_text()
        self.assertNotIn(fields['correccion'], html)
        self.assertNotIn('<form', html)
        self.assertNotIn('/documento?id=', html)

    def test_documents_allowlist_and_escaped_html(self):
        model = self.app.model()
        doc_id = model['fabricas'][0]['exports'][0]['documento_fuente']['id']
        status, _, html = self.request(path='/documento?id=' + doc_id)
        self.assertEqual(status, 200)
        self.assertIn('ENSAYO SINTÉTICO', html)
        for path in ('/documento?id=../../etc/passwd', '/documento?ruta=privado/contexto.md', '/../../etc/passwd'):
            self.assertIn(self.request(path=path)[0], (400, 404))

    def test_saved_xss_and_sql_text_remain_inert(self):
        fields = self.form()
        fields['correccion'] = "<script>alert(1)</script><img src=x onerror=alert(1)>'); DROP TABLE revisiones; --"
        self.assertEqual(self.request('POST', '/revision', fields)[0], 303)
        status, headers, html = self.request()
        self.assertEqual(status, 200)
        self.assertNotIn('<script', html)
        self.assertNotIn('<img', html)
        self.assertIn('&lt;script', html)
        self.assertIn("default-src 'none'", headers['Content-Security-Policy'])
        self.assertEqual(len(self.app.reviews.history(fields['target'])), 1)

    def test_concurrent_revision_only_one_wins(self):
        item = next(iter(self.app.model()['targets'].values()))
        def append(_):
            try:
                self.app.reviews.append(item, 0, 'ENSAYO SINTÉTICO', 'Propuesta concurrente')
                return 'guardado'
            except ValueError:
                return 'conflicto'
        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(append, range(2))), ['guardado', 'conflicto'])
        self.assertEqual(len(self.app.reviews.history(item['id'])), 1)

    def test_data_directory_rejects_git_and_symlink(self):
        with self.assertRaises(ValueError):
            operacion.Reviews(lector.ROOT / 'datos-locales-prohibidos')
        link = Path(self.tmp.name) / 'enlace'
        link.symlink_to('/tmp', target_is_directory=True)
        with self.assertRaises(ValueError):
            operacion.Reviews(link / 'datos')

    def test_brain_over_http_and_invalid_query(self):
        self.assertIn('patrones.', self.request(path='/?tema=revision&uso=workshop')[2])
        self.assertIn('Consulta del cerebro inválida', self.request(path='/?tema=revision&uso=aceptar')[2])
        self.assertEqual(self.request(path='/?ruta=privado/contexto.md')[0], 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
