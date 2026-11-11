"""Proyecta una tanda existente en el panel aceptado sin inferir aprobación."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import lector
import panel


def snapshot(path):
    allowed = lector.BASE/'05-herramientas/fabrica-onia/1-guiones-calendario/salida'
    path = path.resolve(strict=True)
    if not path.is_relative_to(allowed.resolve()) or path.stat().st_size > 512*1024:
        raise ValueError('Tanda fuera de la salida editorial o demasiado grande')
    data = json.loads(path.read_text())
    if data.get('tipo') != 'datos-guiones-no-snapshot-canonico':
        raise ValueError('No es un paquete de guiones')
    rows = data.get('guiones', [])
    if not isinstance(rows, list) or [r.get('id') for r in rows] != ['T01','T02','T03','T04','T05']:
        raise ValueError('Se esperan cinco guiones T01–T05 en orden')
    output = []
    for row in rows:
        source = path.parent/(row['id']+'.md')
        if source.is_symlink() or source.stat().st_size > 128*1024:
            raise ValueError('Origen de guion no admitido')
        raw = source.read_bytes()
        if (hashlib.sha256(raw).hexdigest() != row.get('sha256') or
                len(raw) != row.get('bytes') or raw.decode() != row.get('texto')):
            raise ValueError('El guion difiere de su paquete; reconciliar antes de mostrar')
        output.append({**row, 'version': row.get('version', path.parent.name), 'revision_tecnica': None,
                       'integridad': 'pendiente_revision',
                       'error': 'Bytes cotejados con la tanda local; no acredita aceptación ni publicación.',
                       'origen': str(source.relative_to(lector.BASE))})
    commit = subprocess.check_output(['git', '-C', str(lector.REPO), 'rev-parse', 'HEAD'], text=True).strip()
    names = [str(path.relative_to(lector.REPO))] + [str((path.parent/(r['id']+'.md')).relative_to(lector.REPO)) for r in rows]
    tracked = subprocess.run(['git', '-C', str(lector.REPO), 'ls-files', '--error-unmatch', '--', *names], capture_output=True).returncode == 0
    unchanged = subprocess.run(['git', '-C', str(lector.REPO), 'diff', '--quiet', 'HEAD', '--', *names], capture_output=True).returncode == 0
    anchor = commit if tracked and unchanged else 'Paquete local sin anclar; base del repo ' + commit
    return {'schema': 'onia-lector-panel-v1', 'generado': datetime.now(timezone.utc).isoformat(),
            'guiones': output, 'tareas': [], 'ideas': [], 'fuentes': {'items': [], 'consultas': []},
            'commit_entradas_repo': anchor,
            'alcance': 'Tanda local cotejada. No se consultaron fuentes actuales ni se mutó el harness. Revisión técnica/editorial y autorización de publicación se cotejan por separado.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tanda', required=True, type=Path)
    parser.add_argument('--salida', required=True, type=Path)
    args = parser.parse_args()
    value = snapshot(args.tanda)
    dest = lector.own_output(args.salida)
    dest.mkdir(parents=True, exist_ok=False)
    lector.write_new(dest/'snapshot.json', json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    lector.write_new(dest/'panel.html', panel.render(value))


if __name__ == '__main__':
    main()
