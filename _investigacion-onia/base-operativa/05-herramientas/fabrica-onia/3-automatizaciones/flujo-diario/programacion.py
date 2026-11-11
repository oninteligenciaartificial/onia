#!/usr/bin/env python3
"""Valida el plan DESHABILITADO o dispara un único tick determinista de ensayo."""
import argparse
import json
from pathlib import Path

from comun import HERE, read_json, require
import motor


def plan(config):
    expected = read_json(HERE / 'config.ejemplo.json')
    require(set(config) == set(expected), 'CONFIGURACION_DESCONOCIDA')
    require(config == expected, 'ESTA_ENTREGA_SOLO_ADMITE_EL_PLAN_DESHABILITADO')
    return {'schema': 'onia-plan-disparo-v1', 'habilitada': False, 'zona': config['zona'],
            'hora_tanda': None, 'consulta_horaria': 'propuesta_sin_activar',
            'efectos_instalados': [], 'ensayo': 'Un tick manual; no queda proceso residente'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=HERE / 'config.ejemplo.json')
    parser.add_argument('--ensayo-disparo', type=Path, help='Datos privados de UN tick horario; no llama harness ni modelo')
    args = parser.parse_args(argv)
    try:
        value = plan(read_json(args.config))
        print(json.dumps(value, ensure_ascii=False))
        if args.ensayo_disparo:
            return motor.main(['--datos', str(args.ensayo_disparo), '--evento', 'horario'])
        return 0
    except (OSError, ValueError):
        print(json.dumps({'error': 'PROGRAMACION_NO_HABILITADA_REVISAR_CONFIG'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
