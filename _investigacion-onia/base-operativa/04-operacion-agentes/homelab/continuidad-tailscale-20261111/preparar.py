#!/usr/bin/env python3
"""Genera una unidad privada desde metadatos del daemon. Nunca instala ni activa."""
import argparse
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent


def quote(value):
    if any(ord(c) < 32 for c in value):
        raise ValueError('argumento con caracteres de control')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%').replace('$', '$$') + '"'


def validate(argv, home):
    root = home / 'operacion/homelab/tailscale'
    if argv[0] != str(root / 'bin/tailscaled'):
        raise ValueError('binario no esperado')
    # Sólo parámetros necesarios. Lo desconocido se revisa en privado, nunca se imprime.
    flags = {}
    i = 1
    while i < len(argv):
        key, sep, value = argv[i].partition('=')
        if key not in {'--tun', '--state', '--socket', '--port'} or key in flags:
            raise ValueError('argumentos no admitidos; revisar privadamente')
        if not sep:
            i += 1
            if i >= len(argv):
                raise ValueError('argumento incompleto')
            value = argv[i]
        flags[key] = value
        i += 1
    if flags.get('--tun') != 'userspace-networking':
        raise ValueError('modo no esperado')
    if flags.get('--state') != str(root / 'tailscaled.state') or flags.get('--socket') != str(root / 'tailscaled.sock'):
        raise ValueError('estado/socket no esperados')
    if '--port' in flags and (not re.fullmatch(r'[0-9]+', flags['--port']) or int(flags['--port']) > 65535):
        raise ValueError('puerto inválido')
    return argv


def render(argv, guard, cwd):
    if not re.fullmatch(r'/[A-Za-z0-9_./-]*', str(cwd)):
        raise ValueError('directorio de trabajo requiere revisión privada')
    template = (HERE / 'onia-tailscaled.service.in').read_text()
    return template.replace('@EXEC@', ' '.join(map(quote, argv))).replace('@GUARD@', quote(str(guard))).replace('@CWD@', str(cwd))


def capture(pid):
    # Un PID del manager ausente en /proc demuestra que esta vista no es la del host.
    value = subprocess.check_output(['systemctl', '--user', 'show', 'onia-panel.service', '-p', 'MainPID', '--value'], text=True).strip()
    if not value.isdigit() or int(value) < 1 or not Path('/proc', value).exists():
        raise ValueError('vista de procesos incompleta; ejecutar cotejo en host autorizado')
    proc = Path('/proc', str(pid))
    if proc.stat().st_uid != os.getuid():
        raise ValueError('daemon pertenece a otro usuario')
    argv = [x.decode() for x in (proc / 'cmdline').read_bytes().split(b'\0') if x]
    validate(argv, Path.home())
    if (proc / 'exe').resolve() != Path(argv[0]).resolve():
        raise ValueError('ejecutable no coincide')
    cwd = (proc / 'cwd').resolve()
    for name in ['tailscaled.state', 'tailscaled.sock']:
        if (Path.home() / 'operacion/homelab/tailscale' / name).stat().st_uid != os.getuid():
            raise ValueError('propiedad no coincide')
    return argv, cwd


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pid', required=True, type=int)
    p.add_argument('--salida', required=True, type=Path, help='directorio privado nuevo, fuera de Git')
    a = p.parse_args()
    try:
        argv, cwd = capture(a.pid)
        out = a.salida.resolve()
        # Evita copiar argumentos privados dentro de este repositorio.
        repo = next(x for x in HERE.parents if (x / '.git').exists())
        if out.is_relative_to(repo):
            raise ValueError('salida debe estar fuera del repositorio')
        out.mkdir(mode=0o700, parents=False, exist_ok=False)
        guard = out / 'no_duplicar.py'
        guard.write_text((HERE / 'no_duplicar.py').read_text())
        unit = out / 'onia-tailscaled.service'
        unit.write_text(render(argv, guard, cwd))
        guard.chmod(0o600)
        unit.chmod(0o600)
        print('Preparado; sin instalación ni activación. Cotejar en privado y verificar sintaxis.')
    except (OSError, ValueError, subprocess.SubprocessError, UnicodeError):
        p.exit(2, 'Preparación rechazada; no se imprimen argumentos ni detalles privados.\n')


if __name__ == '__main__':
    main()
