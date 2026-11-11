#!/usr/bin/env python3
"""Repite pruebas y guarda un recibo nuevo dentro de automatizada/evidencia."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import generar as g
from test_generar import inputs, tanda, tree


def run(destination):
    destination = destination.absolute()
    root = g.HERE / 'evidencia'
    g.require(destination.resolve().is_relative_to(root.resolve()) and destination != root,
              'Evidencia fuera de automatizada/evidencia')
    for parent in [destination, *destination.parents]:
        g.require(not parent.is_symlink(), 'Evidencia con enlace')
        if parent == g.HERE:
            break
    g.require(not destination.exists(), 'Recibo existente; elegir otro nombre')
    before = tree(g.OUTPUT_ROOT)
    process = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(g.HERE),
                              '-p', 'test_*.py', '-v'], capture_output=True, text=True)
    g.require(process.returncode == 0, 'Pruebas fallaron:\n' + process.stderr)
    brief, sources, draft, corrections = inputs()
    with tempfile.TemporaryDirectory(prefix='.demostracion-', dir=g.OUTPUT_ROOT) as tmp:
        scratch = Path(tmp)
        g.build(brief, sources, draft, None, scratch / 'r1')
        original = tree(scratch / 'r1')
        second = g.build(brief, sources, draft, corrections, scratch / 'r2')
        g.require(tree(scratch / 'r1') == original, 'Original alterado')
        reproduced = all((scratch / 'r2' / (id+'.md')).read_bytes() ==
                         (g.OUTPUT_ROOT / (id+'.md')).read_bytes() for id in g.IDS)
        g.require(reproduced, 'Reproducción difiere')
        correction_evidence = g.load(scratch / 'r2/correcciones-aplicadas.json')
        # CLI real: entradas incompletas, idea duplicada y destino existente, sin efectos.
        cli = [sys.executable, '-B', str(g.HERE / 'generar.py'), '--brief', str(g.HERE / 'entradas/brief.json'),
               '--fuentes', str(g.HERE / 'entradas/fuentes.json')]
        negatives = []
        for case in ('incompleta', 'duplicada', 'destino_ocupado'):
            candidate = json.loads(json.dumps(draft))
            if case == 'incompleta':
                del candidate['guiones'][0]['proposito']
            if case == 'duplicada':
                candidate['guiones'][4]['idea'] = candidate['guiones'][0]['idea']
            entry = scratch / (case+'.json')
            entry.write_bytes(g.encoded(candidate))
            output = scratch / ('r1' if case == 'destino_ocupado' else case)
            result = subprocess.run([*cli, '--redaccion', str(entry), '--salida', str(output)],
                                    capture_output=True, text=True)
            g.require(result.returncode == 2, 'No rechazó ' + case)
            g.require(tree(scratch / 'r1') == original, 'Rechazo pisó original')
            if case != 'destino_ocupado':
                g.require(not output.exists(), 'Rechazo dejó salida')
            negatives.append({'caso': case, 'returncode': result.returncode,
                              'error': json.loads(result.stderr), 'original_intacto': True})
        demo = {'versiones': ['r1', second['version']], 'temporales_retirados_al_terminar': True,
                'original_intacto': True, 'cinco_markdown_reproducidos': reproduced,
                'r1_hashes': original, 'r2_hashes': tree(scratch / 'r2'),
                'correccion': correction_evidence, 'rechazos_cli': negatives}
    snapshot = tanda.snapshot(g.OUTPUT_ROOT / 'guiones-panel.json')
    html = tanda.panel.render(snapshot)
    consumer_files = [tanda.__file__, tanda.panel.__file__, tanda.lector.__file__]
    consumers = []
    for name in consumer_files:
        path = Path(name)
        relative = path.relative_to(tanda.lector.REPO).as_posix()
        baseline = subprocess.check_output(['git', '-C', str(tanda.lector.REPO), 'show', 'HEAD:'+relative])
        g.require(baseline == path.read_bytes(), 'Consumidor modificado')
        consumers.append({'ruta': relative, 'sha256': g.digest(baseline), 'igual_a_HEAD': True})
    for name, value in g.load(g.OUTPUT_ROOT / 'recibo.json')['v2_solo_lectura'].items():
        g.require(g.digest((g.V2 / name).read_bytes()) == value, 'v2 alterada')
    g.require(before == tree(g.OUTPUT_ROOT), 'Pruebas modificaron entrega raíz')
    report = {'id_encargo': 'guiones-tanda-automatizada-20261111', 'ensayo_local': True,
        'generado': datetime.now(timezone.utc).isoformat(),
        'base_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'pruebas': {'returncode': process.returncode, 'log': 'unittest.txt'},
        'demostracion': demo,
        'consumidor': {'metodo': 'tanda.snapshot(path) → panel.render(snapshot), módulos reales sin cambios',
            'piezas': [r['id'] for r in snapshot['guiones']],
            'titulo_en_html': {r['id']: r['titulo'] in html for r in snapshot['guiones']},
            'html_bytes': len(html.encode()), 'html_sha256': g.digest(html.encode()),
            'revision_tecnica': [r['revision_tecnica'] for r in snapshot['guiones']],
            'rotulo_heredado': snapshot['guiones'][0]['version'],
            'version_editorial_datos': snapshot['guiones'][0]['version_editorial'], 'archivos': consumers},
        'entrada_y_codigo': {p.relative_to(g.HERE).as_posix(): g.digest(p.read_bytes()) for p in
            [g.HERE/'generar.py', g.HERE/'test_generar.py', g.HERE/'comprobar.py', *sorted((g.HERE/'entradas').glob('*.json'))]},
        'v2_intacta': True, 'v3_intacta': True,
        'llm': {'solicitado': 'gpt-6.1-sol high', 'modelo_observado': None, 'esfuerzo_observado': None,
                'cuota_inicio': None, 'cuota_fin': None, 'intentos_observados': 'Una sesión de ejecutor; intentos canónicos no consultados'},
        'limites': ['Sin prueba visual de navegador ni canal comercial', 'No aprobación editorial ni revisión independiente',
                    'Duraciones sin ensayo humano', 'Rótulo v2 fijo del consumidor: consultar version_editorial y Markdown r2',
                    'Veracidad, voz y duplicados semánticos requieren revisión editorial; controles deterministas no los certifican']}
    destination.mkdir(parents=True, exist_ok=False)
    (destination/'unittest.txt').write_text(process.stdout+process.stderr)
    (destination/'resultado.json').write_bytes(g.encoded(report))
    print(json.dumps({'evidencia': destination.relative_to(g.BASE).as_posix(), 'resultado': 'correcto',
                      'piezas': 5, 'cambios': 6, 'v2_intacta': True, 'v3_intacta': True}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.salida)
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
