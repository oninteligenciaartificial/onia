#!/usr/bin/env python3
"""Operate the authorized video's visible controls while holding the existing visor lease."""
import ctypes as c
import datetime as dt
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import tempfile
import time

MANAGER = Path.home() / 'repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py'
PRIVATE = Path.home() / 'operacion/video-referencia-JuAQILH7dkQ/privado'
AUXILIARY = Path(__file__).resolve().parents[1] / 'audio/capturar-pestana.html'
URL = 'https://www.youtube.com/watch?v=JuAQILH7dkQ'
WIDTH, HEIGHT = 1280, 800
LIMIT = 50 * 60


def main():
    os.umask(0o077)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(MANAGER.parent))
    spec = importlib.util.spec_from_file_location('browser_vps', MANAGER)
    manager = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manager)
    with (manager.ROOT / 'visor.lock').open('r') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = manager.read_state()
        human = manager.named_process(state, 'chromium')
        profile = manager.profile_path()
        if not human:
            raise RuntimeError('Chromium humano registrado no está activo.')
        owner = f'{socket.gethostname()}-{human["pid"]}'

        def verify():
            current = manager.read_state()
            if (current.get('status') != 'listo' or current.get('run') != state.get('run')
                    or not manager.live(human)
                    or any(manager.named_process(current, name) for name in ('mcp', 'video'))
                    or manager.profile_singleton(profile) != owner):
                raise RuntimeError('El visor o su propietario cambiaron.')
            return manager.viewer_env(current)

        env = verify()
        os.environ.update(DISPLAY=env['DISPLAY'], XAUTHORITY=env['XAUTHORITY'])
        dest = Path(tempfile.mkdtemp(prefix='visor-av-', dir=manager.private_dir(PRIVATE)))
        def open_auxiliary():
            if not AUXILIARY.is_file() or AUXILIARY.is_symlink():
                raise RuntimeError('Falta la página auxiliar local.')
            return subprocess.run(
                [str(manager.CHROME), '--user-data-dir=' + str(profile), AUXILIARY.as_uri()],
                env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, timeout=15).returncode

        evidence = {
            'controlador_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'auxiliar_sha256': hashlib.sha256(AUXILIARY.read_bytes()).hexdigest(),
            'identidad_chromium_sha256': hashlib.sha256(
                json.dumps([human['pid'], human['start'], human['boot']]).encode()).hexdigest(),
        }
        operate(env, dest, verify, open_auxiliary, evidence)


def operate(env, dest, verify, open_auxiliary, evidence):
    x11 = c.CDLL('libX11.so.6')
    xtst = c.CDLL('libXtst.so.6')
    x11.XOpenDisplay.argtypes = [c.c_char_p]
    x11.XOpenDisplay.restype = c.c_void_p
    x11.XFlush.argtypes = [c.c_void_p]
    x11.XCloseDisplay.argtypes = [c.c_void_p]
    x11.XDefaultScreen.argtypes = [c.c_void_p]
    x11.XDisplayWidth.argtypes = [c.c_void_p, c.c_int]
    x11.XDisplayHeight.argtypes = [c.c_void_p, c.c_int]
    x11.XKeysymToKeycode.argtypes = [c.c_void_p, c.c_ulong]
    x11.XKeysymToKeycode.restype = c.c_ubyte
    x11.XStringToKeysym.argtypes = [c.c_char_p]
    x11.XStringToKeysym.restype = c.c_ulong
    xtst.XTestFakeMotionEvent.argtypes = [c.c_void_p, c.c_int, c.c_int, c.c_int, c.c_ulong]
    xtst.XTestFakeButtonEvent.argtypes = [c.c_void_p, c.c_uint, c.c_int, c.c_ulong]
    xtst.XTestFakeKeyEvent.argtypes = [c.c_void_p, c.c_uint, c.c_int, c.c_ulong]
    display = x11.XOpenDisplay(None)
    if not display:
        raise RuntimeError('No se pudo conectar al display privado.')
    start = time.monotonic()
    deadline = start + LIMIT
    actions = dest / 'acciones.jsonl'
    count = 0
    inspected = None
    record_count = 0
    recorder = None

    def log(action, **fields):
        event = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                 'monotonic': round(time.monotonic(), 6), 'accion': action, **fields}
        with actions.open('a') as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + '\n')
        print(json.dumps(event, ensure_ascii=False), flush=True)

    def grab(x, y, w, h, fps):
        return ['/usr/bin/ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'warning',
                '-f', 'x11grab', '-draw_mouse', '0', '-framerate', str(fps),
                '-video_size', f'{w}x{h}', '-i', f'{env["DISPLAY"]}+{x},{y}']

    def stop_recording():
        nonlocal recorder
        if recorder is None:
            return
        if recorder.poll() is None:
            recorder.send_signal(signal.SIGINT)
        try:
            rc = recorder.wait(timeout=12)
        except subprocess.TimeoutExpired:
            recorder.terminate()
            try:
                rc = recorder.wait(timeout=8)
            except subprocess.TimeoutExpired:
                recorder.kill()
                rc = recorder.wait()
        log('fin_captura_video', rc=rc)
        recorder = None

    def signal_exit(_sig, _frame):
        raise SystemExit(2)

    def key_event(name, pressed):
        keysym = x11.XStringToKeysym(name.encode('ascii'))
        keycode = x11.XKeysymToKeycode(display, keysym)
        if not keycode:
            raise ValueError('El teclado X11 no reconoce una tecla requerida.')
        xtst.XTestFakeKeyEvent(display, keycode, int(pressed), 0)

    def press(name, modifier=None):
        if modifier:
            key_event(modifier, True)
        try:
            key_event(name, True)
            key_event(name, False)
        finally:
            if modifier:
                key_event(modifier, False)

    signal.signal(signal.SIGTERM, signal_exit)
    try:
        screen = x11.XDefaultScreen(display)
        if (x11.XDisplayWidth(display, screen), x11.XDisplayHeight(display, screen)) != (WIDTH, HEIGHT):
            raise RuntimeError('Dimensiones del visor inesperadas.')
        log('lease', directorio_privado=str(dest), url=URL, chromium_existente=True, **evidence)
        while time.monotonic() < deadline:
            verify()
            if recorder is not None and recorder.poll() is not None:
                stop_recording()
            if not select.select([sys.stdin], [], [], 1)[0]:
                continue
            line = sys.stdin.readline()
            if not line:
                break
            try:
                command = json.loads(line)
                action = command['accion']
                if action == 'salir':
                    break
                if action == 'captura':
                    count += 1
                    inspected = None
                    output = dest / f'captura-{count:03}.png'
                    started = time.monotonic()
                    result = subprocess.run(grab(0, 0, WIDTH, HEIGHT, 15)
                                            + ['-frames:v', '1', '-n', str(output)],
                                            env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL, timeout=7)
                    log(action, archivo=output.name, rc=result.returncode,
                        monotonic_inicio=round(started, 6))
                    if result.returncode == 0 and output.is_file():
                        inspected = (count, time.monotonic())
                elif action in {'clic', 'mover', 'tecla', 'texto', 'abrir_auxiliar'}:
                    if (not inspected or command.get('captura') != inspected[0]
                            or time.monotonic() - inspected[1] > 90):
                        raise ValueError('Referenciar la última captura inspeccionada.')
                    if action == 'abrir_auxiliar':
                        rc = open_auxiliary()
                        verify()
                        log(action, rc=rc)
                        continue
                    elif action == 'tecla':
                        keys = {'0': ('0',), 'Escape': ('Escape',), 'Return': ('Return',),
                                'Control+a': ('a', 'Control_L'), 'Control+l': ('l', 'Control_L'),
                                'Control+s': ('s', 'Control_L')}
                        key = keys.get(command['tecla'])
                        if key is None:
                            raise ValueError('Tecla no admitida.')
                        press(*key)
                    elif action == 'texto':
                        value = command['valor']
                        if type(value) is int and 5 <= value <= 1860:
                            value = str(value)
                        elif value in {'piloto.webm', 'tramo-1.webm', 'tramo-2.webm'}:
                            path = dest / value
                            if path.exists() or path.is_symlink():
                                raise ValueError('El archivo de destino ya existe.')
                            value = str(path)
                        else:
                            raise ValueError('Sólo se admiten la duración o un destino privado.')
                        aliases = {'/': 'slash', '.': 'period', '-': 'minus',
                                   '_': 'minus'}
                        for char in value:
                            modifier = 'Shift_L' if char.isupper() or char == '_' else None
                            press(aliases.get(char, char.lower()), modifier)
                    else:
                        x, y = command['x'], command['y']
                        if (type(x) is not int or type(y) is not int or not 0 <= x < WIDTH
                                or not (18 <= y <= 46 or 80 <= y < HEIGHT)):
                            raise ValueError('Coordenadas fuera del área admitida.')
                        xtst.XTestFakeMotionEvent(display, -1, x, y, 0)
                        if action == 'clic':
                            xtst.XTestFakeButtonEvent(display, 1, 1, 0)
                            xtst.XTestFakeButtonEvent(display, 1, 0, 0)
                    x11.XFlush(display)
                    log(action, detalle=command)
                elif action == 'grabar':
                    if (recorder is not None or not inspected or command.get('captura') != inspected[0]
                            or time.monotonic() - inspected[1] > 90):
                        raise ValueError('Grabación activa o sin confirmación visual.')
                    x, y, w, h = command['rectangulo']
                    seconds = command['segundos']
                    if (any(type(value) is not int or value % 2 for value in (x, y, w, h))
                            or min(x, y) < 0 or min(w, h) <= 0 or x + w > WIDTH
                            or y + h > HEIGHT or type(seconds) is not int or not 1 <= seconds <= 1850):
                        raise ValueError('Rectángulo o duración fuera de alcance.')
                    record_count += 1
                    output = dest / f'video-{record_count:02}.mkv'
                    with (dest / f'video-{record_count:02}.log').open('xb') as stderr:
                        recorder = subprocess.Popen(
                            grab(x, y, w, h, 30) + ['-t', str(seconds), '-an', '-c:v', 'libx264',
                                '-preset', 'ultrafast', '-threads', '2', '-pix_fmt', 'yuv420p',
                                '-crf', '21', '-maxrate', '8M', '-bufsize', '16M',
                                '-fps_mode', 'passthrough', '-n', str(output)],
                            env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=stderr)
                    log(action, archivo=output.name, detalle=command)
                elif action == 'detener':
                    stop_recording()
                else:
                    raise ValueError('Acción no admitida.')
            except (ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
                log('error_accion', tipo=type(error).__name__, detalle=str(error))
    finally:
        try:
            stop_recording()
            try:
                verify()
                preserved = True
            except RuntimeError:
                preserved = False
            log('fin_lease', mismo_visor=preserved)
        finally:
            x11.XCloseDisplay(display)


if __name__ == '__main__':
    main()
