#!/usr/bin/env python3
"""Recorrido SINTÉTICO repetible, sin red ni Codex. Sólo escribe en datos privados nuevos."""
import argparse
from pathlib import Path
import json

from comun import locked, require
from motor import Engine
from test_flujo import FakeHarness, report, STAMP, DAY
from adaptador_harness import task_id


def run(root):
    with locked(root):
        require(not (root / 'ciclo.sqlite3').exists(), 'ENSAYO_REQUIERE_DATOS_NUEVOS')
        fake = FakeHarness()
        engine = Engine(root, fake, clock=lambda: STAMP)
        try:
            engine.step('entrada', report(), task_id(DAY), True)
            engine.step('reconciliar', authorized_id=task_id(DAY), provider=True)
            fake.finish()
            engine.step('reconciliar', authorized_id=task_id(DAY), provider=True)
            engine.step('reconciliar', authorized_id=task_id(DAY), provider=True)
            fake.finish()
            engine.step('reconciliar', authorized_id=task_id(DAY), provider=True)
            view = engine.step('reconciliar', authorized_id=task_id(DAY), provider=True)
            require(view['ciclos'][0]['fase'] == 'para_revision_editorial', 'ENSAYO_INCOMPLETO')
            return {'naturaleza': 'SINTETICO: textos fijos y doble del harness; sin modelo real',
                    'operaciones_doble': fake.calls, 'piezas': len(view['ciclos'][0]['resultado']['piezas']),
                    'panel': 'panel.json', 'fuente_real': False, 'modelo_real': False,
                    'programacion_habilitada': False}
        finally:
            engine.store.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.datos), ensure_ascii=False))


if __name__ == '__main__':
    main()
