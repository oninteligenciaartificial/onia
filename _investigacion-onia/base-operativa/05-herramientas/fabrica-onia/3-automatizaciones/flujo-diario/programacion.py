#!/usr/bin/env python3
"""Valida la configuración o ejecuta un tick acotado; no instala un servicio."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from comun import HERE, locked, now, read_json, require
import fuentes
import motor
from adaptador_harness import LocalHarness, task_id

ZONE = ZoneInfo('America/La_Paz')


def instant(value):
    parsed = datetime.fromisoformat(value)
    require(parsed.tzinfo is not None, 'FECHA_SIN_ZONA')
    return parsed


def plan(config):
    expected = read_json(HERE / 'config.ejemplo.json')
    require(set(config) == set(expected), 'CONFIGURACION_DESCONOCIDA')
    variable = {'habilitada', 'hora_tanda', 'autorizacion', 'redaccion_autorizada', 'modelo_hasta'}
    require(all(config[k] == v for k, v in expected.items() if k not in variable), 'LIMITES_CAMBIADOS')
    for key in ('habilitada', 'redaccion_autorizada'):
        require(type(config[key]) is bool, 'PERMISO_INVALIDO')
    hour = config['hora_tanda']
    require(hour is None or isinstance(hour, str) and re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', hour), 'HORA_INVALIDA')
    require(config['autorizacion'] is None or isinstance(config['autorizacion'], str) and 0 < len(config['autorizacion'].strip()) <= 300, 'AUTORIZACION_INVALIDA')
    if config['modelo_hasta'] is not None:
        instant(config['modelo_hasta'])
    if config['habilitada']:
        require(hour is not None and config['autorizacion'], 'FALTA_HORA_O_AUTORIZACION')
    if config['redaccion_autorizada']:
        require(config['habilitada'] and config['modelo_hasta'], 'FALTA_VIGENCIA_MODELO')
    return {'schema': 'onia-plan-disparo-v1', 'habilitada': config['habilitada'], 'zona': config['zona'],
            'hora_tanda': hour, 'redaccion_autorizada': config['redaccion_autorizada'],
            'modelo_hasta': config['modelo_hasta'], 'efectos_instalados': [],
            'ensayo': 'Cada tick termina; el horario depende de un scheduler instalado con autorización'}


def tick(config, root, coordinator=None, clock=now, adapter_factory=LocalHarness, collect=fuentes.collect):
    selected = plan(config)
    if not selected['habilitada']:
        return {**selected, 'resultado': 'deshabilitado', 'errores': []}
    stamp = clock()
    current = instant(stamp)
    local = current.astimezone(ZONE)
    due = local.strftime('%H:%M') >= config['hora_tanda']
    provider = bool(config['redaccion_autorizada'] and current < instant(config['modelo_hasta']))
    require(not provider or coordinator is not None, 'FALTA_COORDINADOR_CANONICO')
    with locked(root):
        adapter = adapter_factory(coordinator, Path.home() / 'operacion') if coordinator is not None else None
        engine = motor.Engine(root, adapter, clock=clock)
        try:
            meta = engine.store.get('meta', 'fuentes', {})
            last = meta.get('ultimo_intento')
            # Se consultan novedades antes de la hora editorial, sin congelar la tanda demasiado pronto.
            if last is None or (current - instant(last)).total_seconds() >= 3600:
                engine.ingest(collect(cursor=meta.get('cursor', 0), clock=clock), queue_input=False)
            ident = task_id(local.date().isoformat()) if due and config['redaccion_autorizada'] else None
            projection = engine.step('horario' if due else 'reconciliar', authorized_id=ident, provider=provider)
            projection['programacion'] = {'habilitada': True, 'zona': config['zona'], 'hora_tanda': config['hora_tanda'],
                'redaccion_autorizada': provider, 'modelo_hasta': config['modelo_hasta']}
            from comun import atomic
            atomic(engine.root / 'panel.json', projection)
            return {'resultado': 'tick_completado', 'hora_tanda': config['hora_tanda'],
                    'candidatas': len(projection['candidatas']), 'ciclos': len(projection['ciclos']),
                    'modelo_en_vigencia': provider, 'errores': [e['codigo'] for e in projection['errores']]}
        finally:
            engine.store.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=HERE / 'config.ejemplo.json')
    parser.add_argument('--ensayo-disparo', type=Path, help='Un tick determinista sin modelo ni recurrencia')
    parser.add_argument('--tick', action='store_true', help='Ejecutar una vez la configuración autorizada; no instala ni inicia scheduler')
    parser.add_argument('--datos', type=Path)
    parser.add_argument('--coordinador-base', type=Path)
    args = parser.parse_args(argv)
    try:
        require(not (args.tick and args.ensayo_disparo), 'MODOS_INCOMPATIBLES')
        config = read_json(args.config)
        value = plan(config)
        if args.tick:
            require(args.datos is not None, 'FALTA_DIRECTORIO_PRIVADO')
            if config['habilitada']:
                path = args.config.absolute()
                require(not path.resolve().is_relative_to(motor.BASE.parents[1]), 'CONFIG_ACTIVA_DENTRO_GIT')
                info = path.stat()
                require(info.st_uid == os.getuid() and info.st_nlink == 1 and not info.st_mode & 0o077, 'CONFIG_ACTIVA_NO_PRIVADA')
                require(not any((part / '.git').exists() for part in (path.parent, *path.parents)), 'CONFIG_ACTIVA_DENTRO_GIT')
            value = tick(config, args.datos, args.coordinador_base)
        print(json.dumps(value, ensure_ascii=False))
        if args.ensayo_disparo:
            return motor.main(['--datos', str(args.ensayo_disparo), '--evento', 'horario'])
        return 2 if value.get('errores') else 0
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({'error': 'PROGRAMACION_PENDIENTE_REVISAR_CONFIG_Y_DATOS'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
