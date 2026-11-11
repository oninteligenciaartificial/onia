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
        self.config.update(habilitada=True, hora_tanda='14:30', autorizacion='ENSAYO SINTETICO',
                           redaccion_autorizada=True, modelo_hasta='2026-11-14T23:00:00-04:00')
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
        self.assertEqual(self.tick('2026-11-11T18:29:00+00:00')['resultado'], 'deshabilitado')
        self.assertFalse(self.root.exists())
        self.assertEqual(self.reads, 0)

    def test_hora_la_paz_deduplicacion_y_consulta_acotada(self):
        before = self.tick('2026-11-11T18:29:00+00:00')
        self.assertEqual(before['ciclos'], 0)
        self.assertEqual(self.fake.calls, [])
        self.tick('2026-11-11T18:30:00+00:00')
        self.tick('2026-11-11T18:31:00+00:00')
        self.tick('2026-11-11T18:32:00+00:00')
        self.assertEqual(self.fake.calls, ['registrar', 'lanzar'])
        self.assertEqual(self.reads, 1)
        self.tick('2026-11-11T19:30:00+00:00')
        self.assertEqual(self.reads, 2)
        self.assertEqual(self.fake.calls.count('lanzar'), 1)

    def test_vigencia_vencida_no_lanza_y_conserva_novedad(self):
        self.config['modelo_hasta'] = '2026-11-11T18:29:00+00:00'
        value = self.tick('2026-11-11T18:30:00+00:00')
        self.assertFalse(value['modelo_en_vigencia'])
        self.assertEqual(self.fake.calls, [])
        self.assertEqual(value['candidatas'], 1)
        self.assertTrue(value['errores'])
        self.assertFalse(json.loads((self.root/'panel.json').read_text())['programacion']['redaccion_autorizada'])

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
