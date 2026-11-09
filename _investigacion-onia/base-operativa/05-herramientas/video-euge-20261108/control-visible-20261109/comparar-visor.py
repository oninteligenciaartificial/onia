#!/usr/bin/env python3
"""Comparación acotada con Chromium humano existente; sin CDP ni reiniciarlo.

Operador inspecciona capturas antes de los clics. Sólo URL autorizada y X11 del visor.
No captura audio ni acredita visionado completo. Recibo y capturas quedan privados.
"""
import ctypes as c
import datetime as dt
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import select
import socket
import subprocess
import sys
import tempfile
import time

MANAGER = Path.home() / 'repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py'
URL = 'https://www.youtube.com/watch?v=JuAQILH7dkQ'

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def main():
    os.umask(0o077)
    sys.path.insert(0, str(MANAGER.parent))
    spec = importlib.util.spec_from_file_location('browser_vps', MANAGER)
    manager = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manager)
    with (manager.ROOT / 'visor.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = manager.read_state()
        human = manager.named_process(state, 'chromium')
        if (state.get('status') != 'listo' or not human or
                any(manager.named_process(state, name) for name in ('mcp', 'video'))):
            raise RuntimeError('El visor no está disponible.')
        profile = manager.profile_path()
        if manager.profile_singleton(profile) != f'{socket.gethostname()}-{human["pid"]}':
            raise RuntimeError('El propietario del perfil no coincide.')
        env = manager.viewer_env(state)
        os.environ['DISPLAY'] = env['DISPLAY']
        os.environ['XAUTHORITY'] = env['XAUTHORITY']
        root = manager.private_dir(Path.home() / 'operacion/video-referencia-JuAQILH7dkQ/privado')
        output = Path(tempfile.mkdtemp(prefix='visor-normal-', dir=root))
        receipt = {'inicio_utc': now(), 'url': URL, 'metodo': 'Chromium existente e interfaz X11',
                   'reinicio_chromium': False, 'visionado_completo_acreditado': False,
                   'audio_analizado': False, 'acciones': []}
        def log(action):
            receipt['acciones'].append({'utc': now(), **action})
            (output / 'recibo.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps(action, ensure_ascii=False), flush=True)
        x11 = c.CDLL('libX11.so.6')
        xtst = c.CDLL('libXtst.so.6')
        x11.XOpenDisplay.argtypes = [c.c_char_p]
        x11.XOpenDisplay.restype = c.c_void_p
        x11.XFlush.argtypes = [c.c_void_p]
        x11.XCloseDisplay.argtypes = [c.c_void_p]
        xtst.XTestFakeMotionEvent.argtypes = [c.c_void_p, c.c_int, c.c_int, c.c_int, c.c_ulong]
        xtst.XTestFakeButtonEvent.argtypes = [c.c_void_p, c.c_uint, c.c_int, c.c_ulong]
        display = x11.XOpenDisplay(None)
        if not display:
            raise RuntimeError('No se abrió el display privado.')
        deadline = time.monotonic() + 300
        try:
            # SingletonLock verificado: esta invocación entrega la URL al proceso existente.
            result = subprocess.run([str(manager.CHROME), '--user-data-dir=' + str(profile), URL],
                                    env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL, timeout=15)
            log({'accion': 'abrir_url', 'rc': result.returncode, 'mismo_chromium': manager.live(human)})
            print(json.dumps({'directorio_privado': str(output)}), flush=True)
            if result.returncode or not manager.live(human):
                raise RuntimeError('La navegación no conservó el navegador registrado.')
            count = 0
            while time.monotonic() < deadline:
                if not manager.live(human):
                    raise RuntimeError('Cambió el navegador del visor.')
                if not select.select([sys.stdin], [], [], min(1, max(0, deadline - time.monotonic())))[0]:
                    continue
                line = sys.stdin.readline()
                if not line:
                    break
                command = json.loads(line)
                action = command.get('accion')
                if action == 'salir':
                    break
                if action == 'captura':
                    count += 1
                    dest = output / f'captura-{count:02}.png'
                    capture = subprocess.run(['/usr/bin/ffmpeg', '-nostdin', '-loglevel', 'error',
                        '-f', 'x11grab', '-video_size', '1280x800', '-i', env['DISPLAY'],
                        '-frames:v', '1', str(dest)], env=env, stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
                    log({'accion': 'captura', 'archivo': dest.name, 'rc': capture.returncode})
                    if capture.returncode:
                        raise RuntimeError('La captura falló.')
                elif action == 'clic':
                    x, y = command.get('x'), command.get('y')
                    if (not isinstance(x, int) or not isinstance(y, int) or
                            not 0 <= x < 1280 or not 80 <= y < 800):
                        raise RuntimeError('Coordenadas fuera del contenido del visor.')
                    xtst.XTestFakeMotionEvent(display, -1, x, y, 0)
                    xtst.XTestFakeButtonEvent(display, 1, 1, 0)
                    xtst.XTestFakeButtonEvent(display, 1, 0, 0)
                    x11.XFlush(display)
                    log({'accion': 'clic', 'x': x, 'y': y, 'motivo': command.get('motivo')})
                else:
                    raise RuntimeError('Acción no admitida.')
        finally:
            x11.XCloseDisplay(display)
            receipt['fin_utc'] = now()
            receipt['mismo_chromium_al_final'] = manager.live(human)
            receipt['visor_listo'] = manager.read_state().get('status') == 'listo'
            log({'accion': 'fin', 'mismo_chromium': manager.live(human)})

if __name__ == '__main__':
    main()
