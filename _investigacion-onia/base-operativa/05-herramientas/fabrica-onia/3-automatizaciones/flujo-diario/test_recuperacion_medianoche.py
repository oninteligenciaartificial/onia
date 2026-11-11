"""Regresión del dictamen7: recuperar entregas fechadas sin rehacerlas tras medianoche.

Sólo dobles y textos sintéticos: sin RPC, red, modelos ni tareas canónicas reales.
"""
from copy import deepcopy
from datetime import datetime, timedelta
import hashlib
from pathlib import Path
import tempfile
import unittest

import programacion as p
from motor import Store
import test_flujo as fixture
from adaptador_harness import task_id


class MultiDayHarness:
    """Un registro sintético por ID, con cupos compartidos y sesiones independientes."""
    def __init__(self):
        self.days, self.calls = {}, []
        self.extra_occupied, self.max_alive = 0, 0

    def occupied(self):
        return self.extra_occupied + sum(s['alive'] for fake in self.days.values()
                                         for s in fake.row.get('sessions', []))

    def query(self, ident):
        row = self.days[ident].query(ident) if ident in self.days else {'exists': False}
        return {**row, 'occupied': self.occupied()}

    check_scope = fixture.FakeHarness.check_scope
    scope = staticmethod(fixture.FakeHarness.scope)
    goal = staticmethod(fixture.FakeHarness.goal)

    def invoke(self, op, request, before, path):
        ident = task_id(request['dia'])
        fake = self.days.setdefault(ident, fixture.FakeHarness())
        if op in {'lanzar', 'revisar'}:
            assert self.occupied() < 3
            assert len(fake.row.get('sessions', [])) < 2
        fake.invoke(op, request, before, path)
        if op == 'cerrar':
            fake.row['commit'] = hashlib.sha256(ident.encode()).hexdigest()[:40]
        self.calls.append((request['dia'], op))
        self.max_alive = max(self.max_alive, self.occupied())

    def result(self, request):
        return self.days[task_id(request['dia'])].result(request)

    def finish(self, day):
        self.days[task_id(day)].finish()


class MidnightRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='onia-medianoche-', dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'ciclo'
        self.config = p.read_json(p.HERE / 'config.ejemplo.json')
        self.config.update(habilitada=True, autorizacion='ENSAYO SINTETICO 12–14', redaccion_autorizada=True)
        self.fake = MultiDayHarness()

    def collect(self, **kwargs):
        report = fixture.report()
        report['consulta'] = report['finalizada'] = kwargs['clock']()
        return report

    def tick(self, stamp):
        before = len(self.fake.calls)
        result = p.tick(self.config, self.root, Path('/coordinador-sintetico'),
                        clock=lambda: stamp, adapter_factory=lambda *_: self.fake, collect=self.collect)
        self.assertLessEqual(len(self.fake.calls)-before, 1, 'Máximo un efecto por tick')
        return result

    def cycles(self):
        store = Store(self.root)
        try:
            return store.rows('ciclo')
        finally:
            store.close()

    def close_day(self, day):
        self.tick(day+'T21:00:00+00:00')  #17:00 LaPaz, registrar
        self.tick(day+'T21:01:00+00:00')
        self.fake.finish(day)
        self.tick(day+'T21:02:00+00:00')
        self.assertEqual(self.fake.days[task_id(day)].calls, ['registrar', 'lanzar', 'cerrar'])

    def recover(self, previous, stamp):
        original = (self.root/'pedidos'/(task_id(previous)+'.json')).read_bytes()
        self.tick(stamp)
        cycle = next(c for c in self.cycles() if c['dia'] == previous)
        self.assertEqual(self.fake.calls[-1], (previous, 'revisar'), cycle.get('error'))
        self.assertIsNone(cycle['error'])
        self.assertEqual((self.root/'pedidos'/(task_id(previous)+'.json')).read_bytes(), original)
        self.assertEqual(cycle['resultado_commit'], self.fake.days[task_id(previous)].row['commit'])
        self.fake.finish(previous)
        when = datetime.fromisoformat(stamp)
        self.tick((when+timedelta(minutes=1)).isoformat())
        self.assertEqual(self.fake.calls[-1], (previous, 'recoger'))
        self.tick((when+timedelta(minutes=2)).isoformat())
        cycle = next(c for c in self.cycles() if c['dia'] == previous)
        self.assertEqual(cycle['fase'], 'para_revision_editorial')
        self.assertEqual(self.fake.days[task_id(previous)].calls, ['registrar', 'lanzar', 'cerrar', 'revisar', 'recoger'])

    def test_tanda12_se_revisa_el13_antes17(self):
        self.close_day('2026-11-12')
        self.recover('2026-11-12', '2026-11-13T04:01:00+00:00')
        self.assertEqual([c['dia'] for c in self.cycles()], ['2026-11-12'])
        self.assertNotIn(task_id('2026-11-13'), self.fake.days)

    def test_tanda12_se_revisa_el13_despues17_sin_que_la_nueva_la_tape(self):
        self.close_day('2026-11-12')
        self.recover('2026-11-12', '2026-11-13T21:01:00+00:00')
        self.tick('2026-11-13T21:04:00+00:00')
        self.assertIn(('2026-11-13', 'registrar'), self.fake.calls)
        self.assertEqual(self.fake.days[task_id('2026-11-12')].calls.count('revisar'), 1)

    def test_tanda12_se_revisa_el14_antes17(self):
        self.close_day('2026-11-12')
        self.recover('2026-11-12', '2026-11-14T20:59:00+00:00')
        self.assertNotIn(task_id('2026-11-14'), self.fake.days)

    def test_tanda12_se_revisa_el14_despues18_objetivo(self):
        self.close_day('2026-11-12')
        self.recover('2026-11-12', '2026-11-14T22:01:00+00:00')

    def test_secuencia12_13_14_y_recogida_el15_sin_renovar(self):
        self.close_day('2026-11-12')
        self.recover('2026-11-12', '2026-11-13T04:01:00+00:00')
        self.close_day('2026-11-13')
        self.recover('2026-11-13', '2026-11-14T20:50:00+00:00')
        self.close_day('2026-11-14')
        self.tick('2026-11-14T22:30:00+00:00')  #18:30 sigue dentro de vigencia
        self.fake.finish('2026-11-14')
        self.tick('2026-11-15T04:00:00+00:00')
        self.tick('2026-11-15T04:01:00+00:00')
        self.assertEqual(len(self.cycles()), 3)
        self.assertTrue(all(c['fase'] == 'para_revision_editorial' for c in self.cycles()))
        self.assertTrue(all(len(fake.row['sessions']) == 2 for fake in self.fake.days.values()))
        self.assertLessEqual(self.fake.max_alive, 3)

    def test_corte_no_autoriza_revisora_nueva_ni_recrea_tanda(self):
        self.close_day('2026-11-12')
        before = deepcopy(self.fake.calls)
        value = self.tick('2026-11-15T04:00:00+00:00')
        self.assertFalse(value['modelo_en_vigencia'])
        self.assertEqual(self.fake.calls, before)
        self.assertIn('MODELO_NO_DISPONIBLE', value['errores'])
        self.assertEqual(len(self.cycles()), 1)

    def test_revocacion_no_autoriza_tanda_anterior(self):
        self.close_day('2026-11-12')
        self.config['redaccion_autorizada'] = False
        before = deepcopy(self.fake.calls)
        self.tick('2026-11-13T04:01:00+00:00')
        self.assertEqual(self.fake.calls, before)
        self.assertEqual(self.cycles()[0]['error'], 'AUTORIZACION_PENDIENTE')

    def test_cupos_llenos_no_revisan_anterior_y_luego_recupera_mismo_id(self):
        self.close_day('2026-11-12')
        self.fake.extra_occupied = 3
        value = self.tick('2026-11-13T04:01:00+00:00')
        self.assertIn('TRES_CUPOS_OCUPADOS', value['errores'])
        self.assertEqual(len(self.fake.calls), 3)
        self.fake.extra_occupied = 0
        self.recover('2026-11-12', '2026-11-13T04:02:00+00:00')

    def test_pedido_anterior_sin_escritora_no_se_redacta_con_fecha_inventada(self):
        self.tick('2026-11-12T21:00:00+00:00')  # Sólo registrado, sin escritora.
        self.tick('2026-11-13T04:01:00+00:00')
        self.tick('2026-11-13T21:00:00+00:00')
        self.assertEqual(self.fake.days[task_id('2026-11-12')].calls, ['registrar'])
        self.assertNotIn(('2026-11-12', 'lanzar'), self.fake.calls)


if __name__ == '__main__':
    unittest.main()
