"""Pruebas del disparo acotado. No instala timers, hace red ni lanza modelos."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import programacion as p
from motor import Store
from test_flujo import FakeHarness, report


class ScheduledTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='onia-scheduler-test-', dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'ciclo'
        self.config = p.read_json(p.HERE / 'config.ejemplo.json')
        self.config.update(habilitada=True, hora_tanda='17:00', autorizacion='ENSAYO SINTETICO',
                           redaccion_autorizada=True, modelo_hasta='2026-11-15T00:00:00-04:00')
        self.fake = FakeHarness()
        self.reads = 0

    def collect(self, **kwargs):
        self.reads += 1
        result = report()
        result['consulta'] = result['finalizada'] = kwargs['clock']()
        return result

    def tick(self, stamp):
        return p.tick(self.config, self.root, Path('/coordinador-ficticio'),
                      clock=lambda: stamp, adapter_factory=lambda *_: self.fake, collect=self.collect)

    def test_apagado_no_crea_datos_ni_consulta(self):
        self.config['habilitada'] = self.config['redaccion_autorizada'] = False
        self.assertEqual(self.tick('2026-11-12T20:59:00+00:00')['resultado'], 'deshabilitado')
        self.assertFalse(self.root.exists())
        self.assertEqual(self.reads, 0)

    def test_hora_la_paz_deduplicacion_y_consulta_acotada(self):
        before = self.tick('2026-11-12T20:59:00+00:00')
        self.assertEqual(before['ciclos'], 0)
        self.assertEqual(self.fake.calls, [])
        self.tick('2026-11-12T21:00:00+00:00')
        self.tick('2026-11-12T21:01:00+00:00')
        self.tick('2026-11-12T21:02:00+00:00')
        self.assertEqual(self.fake.calls, ['registrar', 'lanzar'])
        self.assertEqual(self.reads, 1)
        self.tick('2026-11-12T21:59:00+00:00')
        self.assertEqual(self.reads, 2)
        self.assertEqual(self.fake.calls.count('lanzar'), 1)

    def test_vigencia_vencida_no_lanza_y_conserva_novedad(self):
        self.config['modelo_hasta'] = '2026-11-12T20:59:00+00:00'
        value = self.tick('2026-11-12T21:00:00+00:00')
        self.assertFalse(value['modelo_en_vigencia'])
        self.assertEqual(self.fake.calls, [])
        self.assertEqual(value['candidatas'], 1)
        self.assertTrue(value['errores'])
        self.assertFalse(json.loads((self.root/'panel.json').read_text())['programacion']['redaccion_autorizada'])


    def test_ventana_12_al_14_inicio17_entrega18(self):
        self.assertEqual(self.tick('2026-11-11T21:00:00+00:00')['ciclos'], 0)
        self.assertEqual(self.tick('2026-11-12T20:59:00+00:00')['ciclos'], 0)
        self.tick('2026-11-12T21:00:00+00:00')
        self.assertEqual(self.fake.calls, ['registrar'])
        self.tick('2026-11-12T22:00:00+00:00')
        self.assertEqual(self.fake.calls, ['registrar'])  # entrega18:00: no nuevo lanzamiento
        projection = json.loads((self.root/'panel.json').read_text())
        self.assertEqual(projection['programacion']['hora_entrega'], '18:00')
        self.assertFalse(projection['programacion']['redaccion_autorizada'])
        self.assertEqual(self.tick('2026-11-15T21:00:00+00:00')['ciclos'], 1)
        self.assertEqual(self.fake.calls, ['registrar'])

    def test_recoge_dictamen_del14_despues_del_corte_sin_renovar(self):
        self.tick('2026-11-14T21:00:00+00:00')
        self.tick('2026-11-14T21:01:00+00:00')
        self.fake.finish()
        self.tick('2026-11-14T21:02:00+00:00')
        self.tick('2026-11-14T21:03:00+00:00')
        self.fake.finish()
        value = self.tick('2026-11-15T04:00:00+00:00')
        self.assertFalse(value['modelo_en_vigencia'])
        self.tick('2026-11-15T04:01:00+00:00')
        self.assertEqual(self.fake.calls, ['registrar','lanzar','cerrar','revisar','recoger'])
        store = Store(self.root)
        try:
            self.assertEqual(store.rows('ciclo')[0]['fase'], 'para_revision_editorial')
            self.assertEqual(len(store.rows('ciclo')), 1)
        finally:
            store.close()

    def test_sin_renovacion_ni_horario_historico(self):
        for field, value in [('modelo_hasta','2026-11-15T00:00:01-04:00'),
                             ('hora_tanda','07:00'),('hora_entrega','19:00'),
                             ('fecha_desde','2026-11-11'),('fecha_hasta','2026-11-15')]:
            config = deepcopy(self.config);config[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                p.plan(config)

    def test_activar_exige_hora_autorizacion_y_vigencia(self):
        for field, value in [('hora_tanda', None), ('autorizacion', None), ('modelo_hasta', None),
                             ('hora_tanda', '25:00'), ('modelo_hasta', '2026-11-14T20:00:00')]:
            with self.subTest(field=field):
                config = deepcopy(self.config)
                config[field] = value
                with self.assertRaises((ValueError, TypeError)):
                    p.plan(config)

    def test_no_acepta_aumentar_cupos_ni_proveedor_sustituto(self):
        for field, value in [('max_sesiones_globales', 10), ('hijos', 1), ('proveedor_sustituto', 'api-pagada')]:
            config = deepcopy(self.config)
            config[field] = value
            with self.assertRaises(ValueError):
                p.plan(config)


if __name__ == '__main__':
    unittest.main()
