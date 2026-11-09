#!/usr/bin/env python3
"""Build a shareable index from reviewed timestamps and private media, without copying the media."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image


def fingerprint(path):
    with path.open('rb') as source:
        digest = hashlib.file_digest(source, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def read_log(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def inspect_session(directory, index_path):
    events = read_log(directory / 'acciones.jsonl')
    captures = {event['archivo']: event for event in events
                if event['accion'] == 'captura' and event.get('rc') == 0}
    points = []
    with index_path.open(newline='') as source:
        for row in csv.DictReader(source, delimiter='\t'):
            filename = f'captura-{row.pop("captura")}.png'
            event = captures[filename]
            points.append({
                'archivo_privado': filename,
                'utc_captura_terminada': event['utc'],
                'monotonic_orden_captura': event['monotonic_inicio'],
                'monotonic_captura_terminada': event['monotonic'],
                **row, **fingerprint(directory / filename),
            })
    keys = ('accion', 'utc', 'monotonic')
    actions = []
    for event in events:
        if event['accion'] in ('lease', 'fin_lease', 'abrir_auxiliar', 'clic', 'tecla'):
            action = {key: event[key] for key in keys}
            for key in ('mismo_visor', 'rc', 'controlador_sha256', 'auxiliar_sha256',
                        'identidad_chromium_sha256'):
                if key in event:
                    action[key] = event[key]
            detail = event.get('detalle', {})
            for key in ('captura', 'motivo', 'tecla'):
                if key in detail:
                    action[key] = detail[key]
            actions.append(action)
    return {'acciones': actions, 'puntos': points}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sesion', type=Path, action='append', required=True,
                        help='Directorio privado con capturas y acciones; repetir por tramo.')
    parser.add_argument('--origen', type=Path, required=True,
                        help='Directorio privado de la comprobación original de pista.')
    parser.add_argument('--media', type=Path, action='append', required=True,
                        help='WebM privado guardado. Repetir en orden piloto, tramo 1, tramo 2.')
    args = parser.parse_args()
    if len(args.sesion) != 2 or len(args.media) != 3:
        parser.error('Se requieren dos sesiones de tramos y tres WebM, incluido el piloto.')
    workspace = Path(__file__).resolve().parent
    origins = {
        'menu_configuracion': 'captura-003.png',
        'audio_ingles_inicial': 'captura-005.png',
        'audio_original_seleccionado': 'captura-006.png',
        'autoplay_desactivado': 'captura-011.png',
    }
    sessions = [
        inspect_session(directory, workspace / name)
        for directory, name in zip(args.sesion, ('puntos.tsv', 'puntos-tramo2.tsv'), strict=True)
    ]
    crop = (215, 266, 1068, 746)
    join = []
    for directory, name in zip(args.sesion, ('captura-066.png', 'captura-008.png'), strict=True):
        path = directory / name
        with Image.open(path) as image:
            pixels = image.convert('RGB').crop(crop).tobytes()
        join.append({
            'archivo_privado': name,
            'rgb_sha256': hashlib.sha256(pixels).hexdigest(),
            **fingerprint(path),
        })

    result = {
        'schema': 1,
        'id': 'video-euge-20261108',
        'fuente': 'https://www.youtube.com/watch?v=JuAQILH7dkQ',
        'metodo': 'Chromium humano existente operado por interfaz X11 y captura nativa de una pestaña con su audio',
        'audio_interfaz': 'Spanish (US) original',
        'escucha_directa': False,
        'inspeccion_visual': 'Muestras en hitos; los WebM conservan el flujo capturado para revisión posterior.',
        'pista_origen': {
            key: {'archivo_privado': filename, **fingerprint(args.origen / filename)}
            for key, filename in origins.items()
        },
        'controladores': {
            'tramo_1_bytes_preservados_hash_no_registrado_en_arranque': fingerprint(
                workspace / 'visor-av-tramo1.ejecutado.py'),
            'tramo_2_snapshot_ejecutado': fingerprint(workspace / 'visor-av-tramo2.ejecutado.py'),
        },
        'auxiliar': fingerprint(workspace.parent / 'audio/capturar-pestana.html'),
        'medios': [
            {'archivo_privado': path.name, **fingerprint(path)}
            for path in args.media
        ],
        'costura_15_10': {
            'rectangulo_xyxy': crop,
            'capturas_en_orden': join,
            'rgb_identico': join[0]['rgb_sha256'] == join[1]['rgb_sha256'],
        },
        'sesiones': sessions,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
