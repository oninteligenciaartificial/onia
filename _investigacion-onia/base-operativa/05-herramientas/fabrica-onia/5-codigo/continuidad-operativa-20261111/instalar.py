"""Renderizar dos unidades de usuario. No activar ni ejecutar servicios."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

import continuidad


def render(repo, lista, codex_bin):
    values = dict(REPO=repo, LISTA=lista, CODEX_BIN=codex_bin,
                  ADAPTADOR=Path(repo) / continuidad.HERE.relative_to(continuidad.HERE.parents[5]) / 'continuidad.py')
    # Paths de unidades restringidos para evitar expansión systemd/shell accidental.
    for value in values.values():
        continuidad.require(Path(value).is_absolute() and re.fullmatch(r'/[A-Za-z0-9_./-]+', str(value)))
    service = Path(__file__).with_name('onia-continuidad.service.in').read_text()
    for key, value in values.items():
        service = service.replace('@' + key + '@', str(value))
    return {'onia-continuidad.service': service,
            'onia-continuidad.timer': Path(__file__).with_name('onia-continuidad.timer').read_text()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--lista', required=True, type=Path)
    parser.add_argument('--codex-bin', type=Path, default=Path.home() / '.local/bin')
    parser.add_argument('--destino', type=Path, default=Path.home() / '.config/systemd/user')
    args = parser.parse_args()
    result = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('continuidad.py')),
                             '--repo', str(args.repo), '--lista', str(args.lista), '--validar'], check=False)
    if result.returncode:
        return result.returncode
    units = render(args.repo, args.lista, args.codex_bin)
    continuidad.require(not any(p.is_symlink() for p in (args.destino, *args.destino.parents)))
    # Nunca sobrescribir unidades distintas. Para actualizar, conservar primero la versión previa.
    for name, body in units.items():
        path = args.destino / name
        continuidad.require(not path.is_symlink() and (not path.exists() or path.read_text() == body))
    args.destino.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name, body in units.items():
        path = args.destino / name
        if not path.exists():
            with path.open('x') as stream:
                stream.write(body)
            os.chmod(path, 0o600)
    print('Unidades preparadas; no activadas. Validar y seguir README.md.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
