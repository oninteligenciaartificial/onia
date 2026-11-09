"""Regresiones sin red. No toca registros canónicos ni crea tareas."""
import copy
from email.message import Message
import json
from pathlib import Path
import socket
import sys
import time
import unittest
from unittest.mock import patch
import urllib.error

sys.dont_write_bytecode = True
import lector
import panel


def page(source=lector.SOURCES[0], date=True, title=None):
    title = title or source['titulo_esperado']
    return (f'<html><title>{title}</title>' +
            ('<time datetime="2026-03-16T21:18:18Z">March 16, 2026</time>' if date else '') +
            '<script>DO_NOT_EXECUTE</script></html>').encode()


class Response:
    status = 200

    def __init__(self, data, url=None, content_type='text/html', length=None, encoding=None):
        self.data = data
        self.url = url or lector.SOURCES[0]['url']
        self.headers = Message()
        self.headers['Content-Type'] = content_type
        if length is not None:
            self.headers['Content-Length'] = str(length)
        if encoding:
            self.headers['Content-Encoding'] = encoding

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def geturl(self):
        return self.url

    def read(self, limit):
        return self.data[:limit]


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Toda la suite impide sockets, incluidos fallos o regresiones inesperadas.
        cls.no_network = patch.object(socket, 'socket', side_effect=AssertionError('RED_PROHIBIDA'))
        cls.no_network.start()

    @classmethod
    def tearDownClass(cls):
        cls.no_network.stop()

    def test_duplicado_utm_no_vuelve_a_leer(self):
        source = lector.SOURCES[0]
        duplicate = dict(source, id='alias-F01', url=source['url'] + '?utm_source=test#top')
        calls = []
        result = lector.ingest([source, duplicate], lambda url: calls.append(url) or page())
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(result['items']), 1)
        self.assertEqual(result['consultas'][1]['resultado'], 'duplicado')
        self.assertEqual(result['items'][0]['alias'][0]['id'], 'alias-F01')

    def test_fecha_ausente_no_inventa_publicacion(self):
        item = lector.parse_page(page(date=False), lector.SOURCES[0], '2026-11-09T00:00:00+00:00')
        for key in ['fecha_publicacion', 'fecha_hecho', 'fecha_visible']:
            self.assertIsNone(item[key])
        self.assertFalse(item['elegible_noticia'])

    def test_fecha_visible_no_se_convierte_en_publicacion(self):
        item = lector.parse_page(page(), lector.SOURCES[0], lector.now())
        self.assertIn('2026-03-16', item['fecha_visible']['valor'])
        self.assertIsNone(item['fecha_publicacion'])
        self.assertIsNone(item['fecha_hecho'])

    def test_fallo_por_fuente_continua_independiente(self):
        def transport(url):
            if url == lector.SOURCES[0]['url']:
                raise urllib.error.HTTPError(url, 403, 'no', {}, None)
            return page(lector.SOURCES[1])
        result = lector.ingest(transport=transport)
        self.assertEqual([x['resultado'] for x in result['consultas']], ['fallo', 'leida'])
        self.assertEqual(result['consultas'][0]['error'], 'HTTP_403')
        self.assertEqual(result['items'][0]['id'], 'F02')

    def test_timeout_visible_sin_detalle_sensible(self):
        def broken(_):
            raise TimeoutError('secret-that-must-not-leak')
        result = lector.ingest([lector.SOURCES[0]], broken)
        self.assertEqual(result['consultas'][0]['error'], 'TIMEOUT')
        self.assertNotIn('secret-that', json.dumps(result))

    def test_deadline_total_interrumpe_goteo(self):
        with self.assertRaises(TimeoutError):
            with lector.deadline(0.02):
                time.sleep(0.1)

    def test_url_externa_privada_o_autenticada_rechazada(self):
        for url in ['http://support.claude.com/en/articles/test', 'https://127.0.0.1/en/articles/test',
                    'https://support.claude.com.evil.invalid/en/articles/test',
                    'https://user:secret@support.claude.com/en/articles/test',
                    'https://support.claude.com/en/articles/test?token=secret',
                    'https://support.claude.com:443/en/articles/test']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                lector.canonical_url(url)
        with self.assertRaises(lector.Rejected):
            lector.fetch('https://support.claude.com/en/articles/no-catalogada')

    def test_redireccion_nunca_se_sigue(self):
        with self.assertRaisesRegex(lector.Rejected, 'REDIRECCION_RECHAZADA'):
            lector.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://127.0.0.1/')

    def test_respuesta_insegura_tamano_tipo_compresion_destino(self):
        cases = [(Response(page(), content_type='application/json'), 'TIPO_NO_PERMITIDO'),
                 (Response(page(), length=lector.MAX_BYTES + 1), 'TAMANO_EXCEDIDO'),
                 (Response(b'a' * (lector.MAX_BYTES + 1)), 'TAMANO_EXCEDIDO'),
                 (Response(page(), encoding='gzip'), 'COMPRESION_NO_PERMITIDA'),
                 (Response(page(), url='https://evil.invalid/'), 'RESPUESTA_NO_PERMITIDA')]
        for response, code in cases:
            with self.subTest(code=code), patch('urllib.request.OpenerDirector.open', return_value=response):
                with self.assertRaisesRegex(lector.Rejected, code):
                    lector.fetch(lector.SOURCES[0]['url'])

    def test_challenge_200_no_es_fuente(self):
        result = lector.ingest([lector.SOURCES[0]], lambda _: b'<title>Log in to continue</title>')
        self.assertEqual(result['consultas'][0]['error'], 'PAGINA_NO_RECONOCIDA')
        self.assertEqual(result['items'], [])

    def test_limites_no_hacen_red(self):
        with self.assertRaisesRegex(lector.Rejected, 'LIMITE_FUENTES'):
            lector.ingest([lector.SOURCES[0]] * 4)
        with self.assertRaisesRegex(lector.Rejected, 'TAMANO_EXCEDIDO'):
            lector.parse_page(b'a' * (lector.MAX_BYTES + 1), lector.SOURCES[0], lector.now())

    def test_snapshot_real_y_guiones_anclados(self):
        snapshot = lector.build_snapshot(lector.ingest(transport=lambda url: page(next(s for s in lector.SOURCES if s['url'] == url))))
        self.assertEqual([g['integridad'] for g in snapshot['guiones']], ['verificada', 'verificada'])
        self.assertTrue(all(t['integridad'] == 'verificada' for t in snapshot['tareas']))
        self.assertEqual(len(snapshot['ideas']), 2)
        self.assertTrue(all(value is False for value in snapshot['efectos'].values()))

    def test_guion_alterado_no_falsa_revision(self):
        harness = lector.load_harness()
        task = lector.project_task(lector.TASKS[-1], harness, lector.git('rev-parse', 'HEAD').decode().strip())
        original = Path.read_bytes
        def tampered(path):
            raw = original(path)
            return raw + b'\nALTERADO' if path.name == 'GUION-01-WORKSHOP.md' else raw
        with patch.object(Path, 'read_bytes', tampered):
            scripts, ideas = lector.project_scripts(task)
        self.assertEqual(scripts[0]['integridad'], 'fallo')
        self.assertEqual(scripts[0]['texto'], '')
        self.assertEqual(scripts[1]['integridad'], 'verificada')
        self.assertEqual(len(ideas), 1)

    def test_harness_evidencia_corrupta_no_falso_estado(self):
        harness = lector.load_harness()
        with patch.object(harness, 'verify', side_effect=ValueError('corrupta')):
            result = lector.project_task(lector.TASKS[-1], harness, 'HEAD')
        self.assertEqual(result['integridad'], 'fallo')
        self.assertNotIn('estado', result)
        self.assertIsNone(result['revision_tecnica'])

    def test_html_escapa_respuesta_y_rechaza_links(self):
        snapshot = lector.build_snapshot(lector.ingest(transport=lambda url: page(next(s for s in lector.SOURCES if s['url'] == url))))
        snapshot['fuentes']['items'][0]['titulo'] = '<img src=x onerror=alert(1)>'
        snapshot['fuentes']['items'][0]['url_canonica'] = 'javascript:alert(1)'
        html = panel.render(snapshot)
        self.assertNotIn('<img', html)
        self.assertNotIn('href="javascript:', html)
        self.assertIn('&lt;img', html)
        self.assertNotIn('<script', html)
        self.assertIn("default-src 'none'", html)

    def test_panel_vacio_y_fallo_legibles(self):
        s = {'schema': 'onia-lector-panel-v1', 'fuentes': {}, 'generado': lector.now(),
             'alcance': 'SINTETICO', 'commit_entradas_repo': 'synthetic'}
        html = panel.render(s)
        for text in ['Sin fuentes leídas', 'Sin ideas verificables', 'Sin guiones verificables', 'Sin tareas verificadas']:
            self.assertIn(text, html)

    def test_salida_no_escribe_fuera_ni_pisa_recibo(self):
        with self.assertRaises(lector.Rejected):
            lector.own_output('/tmp/fuera-de-entrega.json')
        with self.assertRaises(FileExistsError):
            lector.write_new(lector.ROOT / 'lector.py', 'no sobrescribir')


if __name__ == '__main__':
    unittest.main(verbosity=2)
