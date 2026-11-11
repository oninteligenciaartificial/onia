#!/usr/bin/env python3
"""Una grabación, hasta cinco piezas, dos formatos. Sin decisiones editoriales ni red."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from types import SimpleNamespace
import procesar as editor


def process(args):
    output = args.salida.absolute()
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    report = {'version': 1, 'fecha_utc': datetime.now(timezone.utc).isoformat(),
              'resultado': 'fallido', 'revision_humana': 'pendiente', 'piezas': [],
              'broll': [], 'asr_ejecuciones': 0}
    try:
        manifest = args.plan.resolve(strict=True)
        data = editor.read_json(manifest)
        editor.keys(data, ('version', 'entrada', 'piezas'), ('transcripcion',))
        if type(data['version']) is not int or data['version'] != 1:
            raise ValueError('Versión de lote inválida.')
        pieces = data['piezas']
        if not isinstance(pieces, list) or not 1 <= len(pieces) <= 5:
            raise ValueError('Un lote requiere de una a cinco piezas con cortes revisados.')
        source = editor.local_file(manifest.parent, data['entrada'], media=True)
        inputs = {manifest: editor.digest(manifest), source: editor.digest(source)}
        report.update(sha256_plan=inputs[manifest], sha256_entrada=inputs[source])
        info = editor.probe(source)
        ids = set()
        for piece in pieces:
            editor.keys(piece, ('id', 'tipo', 'intervalos'), ('broll',))
            if piece['id'] not in ('T01', 'T02', 'T03', 'T04', 'T05') or piece['id'] in ids:
                raise ValueError('IDs únicos T01 a T05 requeridos.')
            ids.add(piece['id'])
            if piece['tipo'] not in ('reel', 'talking_head'):
                raise ValueError('Vlog excluido del lote.')
            editor.intervals(piece['intervalos'], info['duration'])
            overlays = piece.get('broll', [])
            if not isinstance(overlays, list):
                raise ValueError('B-roll debe ser una lista.')
            resolved = []
            for row in overlays:
                editor.keys(row, ('archivo', 'start', 'end', 'source_start'))
                path = editor.local_file(manifest.parent, row['archivo'], media=True)
                inputs.setdefault(path, editor.digest(path))
                report['broll'].append({'id': piece['id'], 'indice': len(resolved), 'sha256': inputs[path]})
                resolved.append({**row, 'archivo': str(path)})
            piece['broll'] = resolved
        transcript = editor.local_file(manifest.parent, data['transcripcion']) if 'transcripcion' in data else None
        if transcript is None:
            if info['audio_index'] is None:
                raise ValueError('Falta audio o transcripción aportada.')
            transcript = output/'transcripcion.json'
            report['asr_ejecuciones'] = 1
            editor.run([str(args.asr_python.expanduser()), str(editor.BASE/'asr_offline.py'),
                        '--entrada', str(source), '--salida', str(transcript),
                        '--modelos', str(args.modelos.expanduser())], args.timeout)
        editor.segments(editor.read_json(transcript), info['duration'])
        transcript_hash = editor.digest(transcript)
        report['sha256_transcripcion'] = transcript_hash
        inputs[transcript] = transcript_hash

        def verify_inputs():
            if any(editor.digest(path) != value for path, value in inputs.items()):
                raise ValueError('Una entrada cambió durante el lote; conservar para revisión.')

        verify_inputs()
        for piece in pieces:
            plan = {key: value for key, value in piece.items() if key != 'id'}
            plan.update(version=1, entrada=str(source), transcripcion=str(transcript))
            plan_path = output/(piece['id']+'-plan.json')
            editor.write_json(plan_path, plan)
            for shape, width in (('vertical', 360 if args.preview else 720),
                                 ('horizontal', 640 if args.preview else 1280)):
                dest = output/(piece['id']+'-'+shape)
                verify_inputs()
                # El editor limita cada subproceso; no matar sólo un Python padre
                # con un segundo timeout mientras FFmpeg sigue corriendo.
                item = editor.process(SimpleNamespace(plan=plan_path, salida=dest,
                    formato=shape, ancho=width, timeout=args.timeout,
                    asr_python=args.asr_python, modelos=args.modelos))
                verify_inputs()
                report['piezas'].append({'id': piece['id'], 'formato': shape,
                                        'carpeta': dest.name, 'resultado': item['resultado'],
                                        'sha256_salida': item['sha256_salida']})
        verify_inputs()
        report['resultado'] = 'renderizado_pendiente_revision'
    except (ValueError, OSError, KeyError, TypeError):
        report['error'] = 'Lote incompleto. Conservar carpeta y revisar los reportes por pieza; no publicar.'
        raise
    finally:
        editor.write_json(output/'lote-reporte.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--salida', required=True, type=Path)
    parser.add_argument('--preview', action='store_true')
    parser.add_argument('--timeout', type=int, choices=range(1, 3601), default=600, metavar='1..3600')
    parser.add_argument('--asr-python', type=Path, default=Path('~/asr/venv/bin/python'))
    parser.add_argument('--modelos', type=Path, default=Path('~/asr/modelos'))
    args = parser.parse_args()
    try:
        result = process(args)
        print(result['resultado'])
    except (ValueError, OSError, KeyError, TypeError):
        print('Lote rechazado o incompleto; conservar entradas y revisar recibos.', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
