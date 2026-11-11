"""Integración HTTP del nuevo productor, sin repetir la suite de diseño histórica."""
import copy
import http.client
from http.server import HTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from urllib.parse import urlencode

import diario
import operacion
import servidor

FLOW = operacion.BASE / '05-herramientas/fabrica-onia/3-automatizaciones/flujo-diario'
sys.path.insert(0, str(FLOW))
import test_flujo
from comun import atomic


class DailyPanelTests(unittest.TestCase):
    def setUp(self):
        self.flow = test_flujo.FlowTests('test_ciclo_completo_y_evento_duplicado')
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.data = self.flow.complete()
        self.tmp = tempfile.TemporaryDirectory(prefix='onia-panel-daily-')
        self.addCleanup(self.tmp.cleanup)
        self.app = servidor.Application(Path(self.tmp.name), flujo_path=self.flow.root/'panel.json')
        self.server = HTTPServer(('127.0.0.1', 0), servidor.handler_for(self.app))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)
        self.host = f'127.0.0.1:{self.server.server_port}'

    def stop(self):
        self.server.shutdown()
        self.thread.join(timeout=2)
        self.server.server_close()

    def request(self, method, route, body=None, extra=None):
        headers = {'Host': self.host, **(extra or {})}
        client = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        client.request(method, route, body, headers)
        response = client.getresponse()
        result = response.status, dict(response.getheaders()), response.read().decode()
        client.close()
        return result

    def test_feed_y_guiones_revision_persistida_original_conservado(self):
        status, headers, html = self.request('GET', '/')
        self.assertEqual(status, 200)
        self.assertIn('Flujo diario', html)
        self.assertIn('ENSAYO SINTÉTICO', html)
        self.assertIn("script-src 'sha256-" + diario.script_hash(), headers['Content-Security-Policy'])
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        model = self.app.model()
        row = model['tanda']['guiones'][0]
        target = model['targets'][row['target']]
        fields = {'csrf': self.app.csrf, 'target': row['target'], 'source_hash': target['huella_revision'],
                  'version': '0', 'motivo': 'ENSAYO de corrección', 'correccion': 'Revisar la entrada y conservar el original'}
        status, _, _ = self.request('POST', '/revision', urlencode(fields), {'Origin': 'http://'+self.host,
                                  'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(status, 303)
        restarted = servidor.Application(Path(self.tmp.name), flujo_path=self.flow.root/'panel.json')
        history = restarted.model()['histories'][row['target']]
        self.assertEqual(len(history), 1)
        self.assertIn(row['texto'], json.loads(history[0]['original'])['texto'])
        self.assertEqual(self.flow.engine.projection()['ciclos'][0]['resultado']['version'], 'r1')
        fields['version'] = '0'
        self.assertEqual(self.request('POST', '/revision', urlencode(fields), {'Origin': 'http://'+self.host,
                                  'Content-Type': 'application/x-www-form-urlencoded'})[0], 409)

    def test_feed_fallido_conserva_ultimo_exito_y_no_renueva_fecha(self):
        self.request('GET', '/')
        expected = self.data['fuente_ultimo_exito']
        (self.flow.root/'panel.json').write_text('{roto')
        status, _, html = self.request('GET', '/flujo')
        self.assertEqual(status, 200)
        self.assertIn('Actualización fallida', html)
        self.assertIn(expected, html)
        self.assertIn('ENSAYO SINTÉTICO', html)
        new_app = servidor.Application(Path(self.tmp.name), flujo_path=self.flow.root/'panel.json')
        self.assertIsNone(new_app.daily())

    def test_proyeccion_incompleta_no_reemplaza_cache_ni_rompe_pagina(self):
        self.assertEqual(self.request('GET', '/')[0], 200)
        original = copy.deepcopy(self.app.last_daily)
        for field in ('huella', 'generado', 'version'):
            with self.subTest(field=field):
                malformed = copy.deepcopy(self.data)
                del malformed['ciclos'][0]['resultado'][field]
                atomic(self.flow.root/'panel.json', malformed)
                self.assertEqual(self.request('GET', '/')[0], 200)
                self.assertEqual(self.app.last_daily, original)
                self.assertTrue(self.app.daily_stale)
        malformed = copy.deepcopy(self.data)
        del malformed['ciclos'][0]['resultado']['piezas'][0]['version_editorial']
        atomic(self.flow.root/'panel.json', malformed)
        self.assertEqual(self.request('GET', '/')[0], 200)
        self.assertEqual(self.app.last_daily, original)

    def test_host_origin_csrf_huella_inyeccion_y_rutas_privadas(self):
        self.assertEqual(self.request('GET', '/flujo', extra={'Host': 'evil.test'})[0], 403)
        self.assertEqual(self.request('GET', '/flujo?archivo=/etc/passwd')[0], 404)
        self.assertEqual(self.request('POST', '/revision', '', {'Origin': 'http://evil.test'})[0], 403)
        self.assertEqual(self.request('GET', '/documento?id=../../panel.json')[0], 400)
        hostile = copy.deepcopy(self.data)
        hostile['candidatas'][0]['titulo'] = '<script>fetch("https://evil.test")</script>'
        hostile['private_payload'] = 'SECRET DO NOT DISPLAY'
        atomic(self.flow.root/'panel.json', hostile)
        _, _, html = self.request('GET', '/flujo')
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('SECRET DO NOT DISPLAY', html)
        model = self.app.model()
        target = model['tanda']['guiones'][0]['target']
        fields = {'csrf': ['wrong'], 'target': [target], 'source_hash': ['wrong'], 'version': ['0'], 'motivo': ['x'], 'correccion': ['y']}
        with self.assertRaises(ValueError):
            self.app.save(fields)
        fields['csrf'] = [self.app.csrf]
        with self.assertRaises(ValueError):
            self.app.save(fields)

    def test_paquete_alterado_no_desplaza_el_ultimo_bueno(self):
        good = self.app.daily()
        hostile = copy.deepcopy(self.data)
        hostile['ciclos'][0]['resultado']['piezas'][0]['texto'] = 'alterado'
        atomic(self.flow.root/'panel.json', hostile)
        self.assertEqual(self.app.daily(), good)
        self.assertTrue(self.app.daily_stale)


if __name__ == '__main__':
    unittest.main()
