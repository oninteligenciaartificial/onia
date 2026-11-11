"""Pruebas de contrato, fallos y consumidor real; sin servicios ni modelos."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

import generar as g

PANEL = g.BASE / '05-herramientas/fabrica-contenido/20261109-lector-panel'
sys.path.insert(0, str(PANEL))
spec = importlib.util.spec_from_file_location('tanda_consumidor', PANEL / 'tanda.py')
tanda = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tanda)


def inputs():
    return [g.load(g.HERE / 'entradas' / name) for name in
            ('brief.json', 'fuentes.json', 'redaccion-r1.json', 'correcciones-r2.json')]


def tree(path):
    return {p.relative_to(path).as_posix(): g.digest(p.read_bytes())
            for p in sorted(path.rglob('*')) if p.is_file()}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.brief, self.sources, self.draft, self.corrections = inputs()
        # Sólo temporales propios dentro de la salida asignada. La tanda raíz se conserva.
        self.temp = tempfile.TemporaryDirectory(prefix='.prueba-', dir=g.OUTPUT_ROOT)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def build(self, name='nueva', corrections=False):
        return g.build(self.brief, self.sources, self.draft,
                       self.corrections if corrections else None, self.root / name)

    def rejected(self, message):
        target = self.root / 'rechazada'
        with self.assertRaisesRegex((ValueError, KeyError), message):
            g.build(self.brief, self.sources, self.draft, None, target)
        self.assertFalse(target.exists(), 'Rechazo dejó salida parcial')

    def test_correccion_en_segunda_salida_conserva_original(self):
        self.build('r1')
        original = tree(self.root / 'r1')
        result = self.build('r2', corrections=True)
        self.assertEqual(result['cambios'], 6)
        self.assertEqual(tree(self.root / 'r1'), original)
        r1 = g.load(self.root / 'r1/guiones-panel.json')['guiones']
        r2 = g.load(self.root / 'r2/guiones-panel.json')['guiones']
        for a, b in zip(r1, r2):
            if a['id'] in {'T01', 'T04'}:
                self.assertIn('te paso la información', a['guion_hablado'])
                self.assertNotIn('te paso la información', b['guion_hablado'])
                self.assertEqual(b['cta'], 'Si te interesa el workshop, comentá NEGOCIO.')
            else:
                self.assertEqual(a['guion_hablado'], b['guion_hablado'])

    def test_redaccion_incompleta_sin_salida(self):
        del self.draft['guiones'][1]['proposito']
        self.rejected('proposito')

    def test_rechaza_ids_duplicados(self):
        self.draft['guiones'][4]['id'] = 'T01'
        self.rejected('cinco piezas')

    def test_rechaza_ideas_duplicadas_normalizadas(self):
        self.draft['guiones'][4]['idea'] = self.draft['guiones'][0]['idea'].upper()
        self.rejected('duplicada')

    def test_rechaza_locucion_duplicada(self):
        self.draft['guiones'][4]['guion_hablado'] = self.draft['guiones'][0]['guion_hablado']
        self.rejected('duplicada')

    def test_destino_duplicado_no_pisa_bytes(self):
        self.build('ocupada')
        before = tree(self.root / 'ocupada')
        with self.assertRaisesRegex(ValueError, 'Salida duplicada'):
            self.build('ocupada', corrections=True)
        self.assertEqual(tree(self.root / 'ocupada'), before)

    def test_rechaza_noticia_sin_fecha(self):
        del self.sources['items'][4]['publicada']
        self.rejected('publicada')

    def test_rechaza_noticia_vieja(self):
        self.sources['items'][4]['fecha_hecho'] = '2025-11-10'
        self.rejected('reciente')

    def test_rechaza_secundaria(self):
        self.sources['items'][4]['primaria'] = False
        self.rejected('primaria')

    def test_rechaza_fuente_local_alterada(self):
        self.sources['items'][0]['sha256'] = '0'*64
        self.rejected('alterada')

    def test_rechaza_horario_obsoleto(self):
        self.brief['oferta']['clases'][1] = '2026-11-14T20:00:00-04:00'
        self.rejected('Oferta/horarios')

    def test_rechaza_cta_distinto_en_copy(self):
        self.draft['guiones'][0]['copy'] = 'Seguí la cuenta.'
        self.rejected('CTA incoherente')

    def test_rechaza_falta_variante(self):
        del self.draft['guiones'][0]['variantes']['horizontal']
        self.rejected('adaptaciones')

    def test_rechaza_aprobacion_editorial(self):
        self.brief['revision_editorial'] = 'aprobada'
        self.rejected('aprobación')

    def test_rechaza_patron_inventado(self):
        self.draft['guiones'][0]['patrones'] = ['inexistente']
        self.rejected('Patrón')

    def test_correccion_obsoleta_no_crea_salida(self):
        self.corrections['entrada_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'otra entrada'):
            self.build(corrections=True)
        self.assertFalse((self.root / 'nueva').exists())

    def test_correccion_con_precondicion_errada_no_crea_salida(self):
        self.corrections['reglas'][0]['antes'] = 'Esto nunca estuvo'
        with self.assertRaisesRegex(ValueError, 'Precondición'):
            self.build(corrections=True)
        self.assertFalse((self.root / 'nueva').exists())

    def test_rechaza_salida_historica(self):
        with self.assertRaisesRegex(ValueError, 'fuera de v3'):
            g.build(self.brief, self.sources, self.draft, None, g.V2 / 'NO-ESCRIBIR')

    def test_rechaza_enlace_salida(self):
        (self.root / 'enlace').symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'enlace'):
            g.build(self.brief, self.sources, self.draft, None, self.root / 'enlace/salida')

    def test_evergreen_explicito_sin_web(self):
        self.sources['items'] = [s for s in self.sources['items'] if s['tipo'] == 'local']
        row = self.draft['guiones'][2]
        row.update({'slot': 'evergreen', 'fuentes': ['CEREBRO', 'V2'],
                    'tipo_evidencia': 'caso_ficticio_no_salida_IA',
                    'motivo_evergreen': 'Entrada de prueba offline; no fuente noticiosa actual.',
                    'apertura': 'Una agenda puede verse perfecta y ser imposible.',
                    'guion_hablado': 'Una agenda puede verse perfecta y ser imposible. En este caso ficticio, la ficha pide inventario, pedidos y entregas. El borrador omite inventario. Compará ambas listas, marcá esa omisión y pedí una nueva versión que conserve todas las tareas. Volvé a comprobarla antes de usarla. Guardá esta lista para revisar tu próximo borrador.',
                    'cta': 'Guardá esta lista para revisar tu próximo borrador.',
                    'copy': 'Ejemplo escrito ficticio, evergreen explícito; no noticia. Guardá esta lista para revisar tu próximo borrador.'})
        self.build('evergreen')
        text = (self.root / 'evergreen/T03.md').read_text()
        self.assertIn('Evergreen explícito:', text)
        del row['motivo_evergreen']
        self.rejected('motivo_evergreen')

    def test_consumidor_tanda_real_y_rechazo_de_md_alterado(self):
        self.build('compatible', corrections=True)
        path = self.root / 'compatible/guiones-panel.json'
        value = tanda.snapshot(path)
        self.assertEqual([r['id'] for r in value['guiones']], g.IDS)
        self.assertTrue(all(r['revision_tecnica'] is None for r in value['guiones']))
        html = tanda.panel.render(value)
        for row in self.draft['guiones']:
            self.assertIn(row['titulo'], html)
        (path.parent / 'T01.md').write_text('Alteración inducida sólo en temporal propio')
        with self.assertRaisesRegex(ValueError, 'difiere'):
            tanda.snapshot(path)

    def test_entrega_raiz_hashes_y_calendario(self):
        path = g.OUTPUT_ROOT
        receipt = g.load(path / 'recibo.json')
        for name, record in receipt['archivos'].items():
            raw = (path / name).read_bytes()
            self.assertEqual(g.digest(raw), record['sha256'])
            self.assertEqual(len(raw), record['bytes'])
        calendar = g.load(path / 'calendario.json')
        self.assertEqual(calendar['clases'], g.OFFER['clases'])
        self.assertTrue(all(p['hora_publicacion'] is None for p in calendar['piezas']))
        snapshot = tanda.snapshot(path / 'guiones-panel.json')
        self.assertEqual(len(snapshot['guiones']), 5)
        self.assertEqual(snapshot['guiones'][0]['version_editorial'], 'r2')

    def test_reproduccion_de_cinco_markdown(self):
        self.build('reproduccion', corrections=True)
        for id in g.IDS:
            self.assertEqual((self.root / 'reproduccion' / (id+'.md')).read_bytes(),
                             (g.OUTPUT_ROOT / (id+'.md')).read_bytes())

    def test_estado_fabrica_rutas_reales_sin_aceptacion(self):
        data = g.load(g.OUTPUT_ROOT / 'estado-fabrica.json')
        self.assertEqual(data['schema'], 'onia-fabrica-estado-v1')
        self.assertEqual(data['estado'], 'para_revision')
        paths = [data['fuente']] + [x['ruta'] for x in data['entregables']]
        paths += [p for step in data['pasos'] for p in step['evidencias']]
        for path in paths:
            self.assertTrue((g.BASE / path).is_file())
        self.assertTrue(data['pendientes'])

    def test_json_claves_repetidas(self):
        path = self.root / 'invalido.json'
        path.write_text('{"a":1,"a":2}')
        with self.assertRaisesRegex(ValueError, 'duplicada'):
            g.load(path)


if __name__ == '__main__':
    unittest.main()
