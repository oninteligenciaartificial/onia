#!/usr/bin/env python3
"""Ejecuta pruebas locales con clips y un perfil sintéticos."""
import ast
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
INSTALL = Path.home() / 'operacion/browser-piloto-20261108'


def main():
    os.umask(0o077)
    ast.parse((HERE / 'ejecutar.py').read_text())
    subprocess.run([sys.executable, '-B', str(HERE / 'prueba-terminal.py')], check=True)
    subprocess.run(['node', '--check', str(HERE / 'reproduccion.cjs')], check=True)
    subprocess.run(['node', str(HERE / 'prueba-limites.cjs')], check=True)
    root = Path(tempfile.mkdtemp(prefix='onia-euge-playback-'))
    auth = root / 'Xauthority'
    auth.touch()
    display = next(f':{number}' for number in range(160, 190)
                   if not Path(f'/tmp/.X{number}-lock').exists()
                   and not Path(f'/tmp/.X11-unix/X{number}').exists())
    subprocess.run(['xauth', '-f', str(auth)], input=f'add {display} . {secrets.token_hex(16)}\n',
                   text=True, stdout=subprocess.DEVNULL, check=True)
    for source, duration, name in (
        ('testsrc2=size=256x144:rate=12', '3', 'content.webm'),
        ('color=c=red:s=256x144:r=12', '0.8', 'ad.webm'),
    ):
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi', '-i', source,
                        '-t', duration, '-c:v', 'libvpx', str(root / name)], check=True)
    xvfb = subprocess.Popen(['Xvfb', display, '-screen', '0', '1280x800x24', '-nolisten', 'tcp',
                             '-auth', str(auth)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        env = dict(os.environ, DISPLAY=display, XAUTHORITY=str(auth))
        for _ in range(50):
            ready = subprocess.run(['xdpyinfo'], env=env, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL).returncode == 0
            if ready:
                break
            if xvfb.poll() is not None:
                raise RuntimeError('Falló Xvfb de prueba')
            time.sleep(.1)
        else:
            raise RuntimeError('Xvfb de prueba no respondió')
        subprocess.run(['node', str(HERE / 'prueba-reproduccion.cjs'), str(HERE / 'reproduccion.cjs'),
                        str(INSTALL), str(root)], env=env, check=True, timeout=60)
    finally:
        xvfb.terminate()
        xvfb.wait(timeout=5)


if __name__ == '__main__':
    main()
