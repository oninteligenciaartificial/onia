#!/usr/bin/env python3
"""Préstamo exclusivo del visor para reproducir JuAQILH7dkQ sin saltos."""
import datetime as dt
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import time

HOME_PATH = Path.home()
MANAGER = HOME_PATH / ('repos/onia-coordinador/_investigacion-onia/base-operativa/'
                       '05-herramientas/cuentas-analisis/20261108/browser-vps.py')
OUTPUT = HOME_PATH / 'operacion/video-referencia-JuAQILH7dkQ'
SCRIPT = Path(__file__).resolve().with_name('reproduccion.cjs')


def load_manager():
    sys.path.insert(0, str(MANAGER.parent))
    spec = importlib.util.spec_from_file_location('browser_vps', MANAGER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stop_child(child):
    child.stdin.close()
    if child.poll() is not None:
        return
    child.terminate()
    try:
        child.wait(timeout=16)
    except subprocess.TimeoutExpired:
        # Sólo el proceso Node que se creó aquí. El gestor aún comprueba si
        # quedan procesos del perfil antes de intentar devolver el visor.
        child.kill()
        child.wait(timeout=3)


def capture(manager, lock):
    # Reserva el último medio minuto para cerrar y devolver el perfil.
    budget = 2970
    until = os.environ.get('ONIA_VIDEO_HASTA_UTC')
    if until:
        stop_at = dt.datetime.fromisoformat(until)
        if stop_at.utcoffset() != dt.timedelta(0):
            raise RuntimeError('El límite absoluto debe estar en UTC.')
        budget = min(budget, (stop_at - dt.datetime.now(dt.timezone.utc)).total_seconds() - 30)
    if budget <= 0:
        raise RuntimeError('Se agotó el tiempo autorizado para este intento.')
    deadline = time.monotonic() + budget
    state = manager.read_state()
    human = manager.named_process(state, 'chromium')
    if (state.get('mode') != 'navegador-publico' or state.get('status') not in ('listo', 'recuperar')
            or not human or manager.named_process(state, 'mcp') or manager.named_process(state, 'video')):
        raise RuntimeError('El visor debe estar listo con Chromium humano y sin otro préstamo.')
    env, profile = manager.viewer_env(state), manager.profile_path()
    if manager.profile_singleton(profile) != f'{socket.gethostname()}-{human["pid"]}' or not manager.live(human):
        raise RuntimeError('El propietario del perfil no coincide con Chromium humano registrado.')
    if not (SCRIPT.is_file() and manager.NODE.is_file() and manager.CHROME.is_file()
            and (manager.INSTALL / 'node_modules/playwright/package.json').is_file()):
        raise RuntimeError('Falta el capturador o la instalación reutilizada.')

    parent = manager.private_dir(OUTPUT, create=True)
    private = manager.private_dir(parent / 'privado', create=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = Path(tempfile.mkdtemp(prefix=f'reproduccion-{stamp}-', dir=private))
    print(json.dumps({'directorio_privado': str(output)}), flush=True)

    browser_env = {key: env[key] for key in ('LANG', 'LC_ALL', 'USER', 'LOGNAME',
                  'DISPLAY', 'XAUTHORITY', 'XDG_RUNTIME_DIR', 'XDG_CURRENT_DESKTOP',
                  'DESKTOP_SESSION', 'DBUS_SESSION_BUS_ADDRESS') if key in env}
    runtime = Path(state['run'])
    browser_env.update(HOME=str(HOME_PATH), PATH='/usr/bin:/bin',
                       XDG_CACHE_HOME=str(runtime / 'mcp-cache'),
                       XDG_CONFIG_HOME=str(runtime / 'mcp-config'))

    interrupted = None

    def request_stop(signum, _frame):
        nonlocal interrupted
        interrupted = signum

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, request_stop)

    child = None
    expired = False
    state['status'] = 'muestra-video'
    state['video_inicio_utc'] = now()
    state.pop('video_fin_utc', None)
    manager.save(state)
    try:
        manager.close_human(human, env, lock)
        manager.await_free_profile(profile)
        if interrupted is None:
            command = [str(manager.NODE), str(SCRIPT), str(manager.INSTALL), str(manager.CHROME),
                       str(profile), str(output)]
            child = subprocess.Popen(command, cwd=output, env=browser_env,
                                     start_new_session=True, pass_fds=(lock.fileno(),),
                                     stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
            state['processes'].append(manager.process_identity('video', child.pid))
            manager.save(state)
            while child.poll() is None and interrupted is None:
                if time.monotonic() >= deadline:
                    expired = True
                    break
                time.sleep(.2)
    finally:
        if child is not None:
            stop_child(child)
        state['processes'] = [proc for proc in state['processes'] if proc['name'] != 'video']
        state['status'] = 'recuperar'
        state['video_fin_utc'] = now()
        manager.save(state)
        manager.restore_human(state, manager.viewer_env(state), profile)

    manifest = output / 'muestra.json'
    if not manifest.is_file():
        reason = 'LIMITE_DE_TIEMPO' if expired else 'INTERRUMPIDO' if interrupted else 'SIN_MANIFIESTO'
        manifest.write_text(json.dumps({'status': 'sin_fotogramas', 'diagnostico': reason, 'frames': []}) + '\n')
    result = json.loads(manifest.read_text())
    print(json.dumps({'manifest': str(manifest), 'status': result.get('status'),
                      'frames': len(result.get('frames', [])), 'diagnostico': result.get('diagnostico'),
                      'destino': result.get('destino'), 'visor': state['status']}, ensure_ascii=False))
    if interrupted:
        return 128 + interrupted
    if expired:
        return 124
    return child.returncode if child is not None else 2


def main():
    if sys.argv[1:]:
        raise RuntimeError('Este capturador sólo admite el video público fijado en el código.')
    os.umask(0o077)
    manager = load_manager()
    manager.private_dir(manager.ROOT)
    with (manager.ROOT / 'visor.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('El visor está prestado. Esperar a que termine la sesión activa.') from None
        return capture(manager, lock)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
