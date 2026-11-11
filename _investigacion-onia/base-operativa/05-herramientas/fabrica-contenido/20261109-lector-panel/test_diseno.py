"""Regresiones del contrato HTML y del origen. La fidelidad visual exige navegador."""
from html.parser import HTMLParser
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import HTTPServer

import diseno
import lector
import operacion
import panel
import servidor


class Structure(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.links = []
        self.stack = []
        self.main_sections = []
        self.radios = []
        self.controls = []
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag == 'section' and 'screen' in attrs.get('class', '').split():
            self.main_sections.append(attrs['id'])
        if tag == 'input' and attrs.get('type') == 'radio':
            self.radios.append(attrs)
        if tag in ('script', 'iframe', 'img'):
            self.controls.append(tag)


class DesignTests(unittest.TestCase):
    def test_preview_native_navigation_resolves_and_selectors_have_targets(self):
        model = operacion.build()
        html = panel.render(model['tanda'], model)
        parsed = Structure(html)
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        for link in parsed.links:
            if link.startswith('#'):
                self.assertIn(link[1:], parsed.ids)
        self.assertTrue({'hoy','fabricas','calendario','cerebro','montaje','guiones'} <= set(parsed.main_sections))
        self.assertEqual([row['id'] for row in parsed.radios], ['tab-resultado','tab-fuentes','tab-cambios'])
        self.assertEqual(parsed.controls, [])
        self.assertIn('Tu fábrica, paso a paso', html)
        self.assertIn("form-action 'none'", html)
        self.assertIn('font/woff2;base64,', html)
        self.assertIn('image/svg+xml;base64,', html)
        self.assertIn('&quot;bytes&quot;', html)
        self.assertIn('&quot;revision_tecnica&quot;', html)
        self.assertIn(model['tanda']['guiones'][0]['sha256'], html)

    def test_missing_exports_never_create_completed_circles(self):
        model = operacion.build()
        rows = diseno.factory_rows(model)
        self.assertEqual(rows.count('class="factory-row"'), 6)
        self.assertNotIn('circle-check-filled', rows)
        self.assertIn('5 borradores históricos', rows)
        self.assertEqual(rows.count('Resumen pendiente de recibir'), 5)

    def test_fixture_steps_are_labelled_and_completion_comes_from_contract(self):
        fixture = operacion.PANEL_ROOT + '/fixtures/tarea-sintetica/estado-fabrica.json'
        model = operacion.build([fixture])
        rows = diseno.factory_rows(model)
        self.assertIn('ENSAYO SINTÉTICO', rows)
        self.assertEqual(rows.count('icon-circle-check-filled'), 2)
        self.assertIn('Recibir una entrada concreta', rows)

    def test_header_date_uses_snapshot_and_la_paz_zone(self):
        model = operacion.build()
        model['generado'] = '2026-11-12T02:10:00+00:00'
        html = panel.render(model['tanda'], model)
        self.assertIn('Miércoles 11 nov 2026</time>', html)
        self.assertIn('2026-11-12T02:10:00+00:00', html)

    def test_embedded_library_assets_match_sources_and_licenses(self):
        assets = json.loads((lector.ROOT / 'recursos/FUENTES.json').read_text())
        for item in assets['iconos']:
            raw = (lector.ROOT / 'recursos/tabler' / item['archivo']).read_bytes()
            self.assertEqual(lector.sha(raw), item['sha256'])
        html = panel.render(operacion.build()['tanda'], operacion.build())
        self.assertIn('MIT License', html)
        self.assertIn('SIL OPEN FONT LICENSE', html)
        self.assertNotIn('<svg', html)
        self.assertNotIn('<script', html)
        with self.assertRaises(ValueError):
            diseno.icon('../../privado')


class OriginTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='onia-origen-sintetico-')
        self.app = servidor.Application(self.directory.name)
        self.http = HTTPServer(('127.0.0.1', 0), servidor.handler_for(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever, kwargs={'poll_interval': 0.01})
        self.thread.start()

    def tearDown(self):
        self.http.shutdown()
        self.thread.join(timeout=5)
        self.http.server_close()
        self.directory.cleanup()

    def request(self, method='GET', headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.http.server_port, timeout=10)
        conn.request(method, '/' if method=='GET' else '/revision', b'' if method=='POST' else None, headers or {})
        response = conn.getresponse()
        value = response.status, dict(response.getheaders()), response.read().decode()
        conn.close()
        return value

    def test_header_and_html_referrer_policies_allow_real_same_origin_post(self):
        status, headers, html = self.request()
        self.assertEqual(status, 200)
        self.assertEqual(headers['Referrer-Policy'], 'same-origin')
        self.assertIn('<meta name="referrer" content="same-origin">', html)
        self.assertNotIn('content="no-referrer"', html)
        self.assertIn("default-src 'none'", headers['Content-Security-Policy'])
        self.assertNotIn('script-src', headers['Content-Security-Policy'])
        self.assertIn("form-action 'self'", headers['Content-Security-Policy'])

    def test_null_missing_wildcard_and_foreign_origin_stay_forbidden(self):
        for value in (None, 'null', '*', 'https://externo.invalid', 'http://127.0.0.1:1'):
            headers = {} if value is None else {'Origin': value}
            with self.subTest(origin=value):
                self.assertEqual(self.request('POST', headers)[0], 403)
        self.assertEqual(self.app.reviews.history(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
