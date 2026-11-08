#!/usr/bin/env python3
"""Visor privado temporal; no instala, no cambia políticas, no borra perfiles."""
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import time

ROOT = Path.home() / 'operacion/cuentas/analisis-onia'
RUNTIME = ROOT / 'runtime-20261108'
CHROME = Path.home() / 'operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome'
STATE = ROOT / 'visor-estado.json'
PASSWORD = ROOT / 'clave-visor.txt'
BOOT = Path('/proc/sys/kernel/random/boot_id').read_text().strip()


def stamp(pid):
    try:
        raw = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return None if raw[0] == 'Z' else raw[19]
    except (FileNotFoundError, ProcessLookupError):
        return None


def live(p):
    return p.get('boot') == BOOT and p.get('start') is not None and stamp(p['pid']) == p['start']


def read_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {'processes': []}


def save(state):
    STATE.write_text(json.dumps(state, indent=2) + '\n')


def report(state):
    return {**state, 'processes': [{**p, 'alive': live(p)} for p in state['processes']]}


def spawn(state, name, cmd, env):
    log = Path(state['run']) / (name + '.log')
    with log.open('ab') as out:
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=out,
                             env=env, start_new_session=True, close_fds=True)
    state['processes'].append({'name': name, 'pid': p.pid, 'start': stamp(p.pid), 'boot': BOOT})
    save(state)
    return p


def finish(state):
    # Sólo procesos registrados e identidad vigente. Nunca pkill ni kill de grupos.
    for p in reversed(state['processes']):
        if live(p):
            os.kill(p['pid'], signal.SIGTERM)
            end = time.monotonic() + 8
            while live(p) and time.monotonic() < end:
                time.sleep(.1)
            if live(p):
                raise RuntimeError('Un proceso propio no confirmó cierre; conservado para inspección: ' + p['name'])
    state['status'] = 'detenido'
    save(state)


def wait_port(port, proc):
    for _ in range(50):
        if proc.poll() is not None:
            raise RuntimeError('Proceso no inició; consultar log privado')
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=.2):
                return
        except OSError:
            time.sleep(.1)
    raise RuntimeError('Puerto no quedó disponible a tiempo')


def start(control=False):
    old = read_state()
    if any(live(p) for p in old['processes']):
        raise RuntimeError('Ya existe un visor vivo. Consultar estado; no duplicar.')
    # No toma puertos ni displays de otra sesión.
    for port in (5908, 6088):
        with socket.socket() as s:
            s.bind(('127.0.0.1', port))
    display = next((n for n in range(93, 120)
                    if not Path(f'/tmp/.X{n}-lock').exists()
                    and not Path(f'/tmp/.X11-unix/X{n}').exists()), None)
    if display is None:
        raise RuntimeError('Sin display libre')
    run = ROOT / ('sesion-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + secrets.token_hex(3))
    run.mkdir(mode=0o700)
    auth = run / 'Xauthority'
    auth.touch(mode=0o600)
    cookie = secrets.token_hex(16)
    subprocess.run(['xauth', '-f', str(auth)], input=f'add :{display} . {cookie}\n'.encode(),
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    if not PASSWORD.exists():
        with PASSWORD.open('x') as out:
            out.write(''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8)) + '\n')
    if PASSWORD.is_symlink() or PASSWORD.stat().st_mode & 0o077:
        raise RuntimeError('Clave del visor debe ser un archivo privado 0600')
    state = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'run': str(run),
             'display': f':{display}', 'mode': 'control-sin-navegador' if control else 'navegador-publico',
             'status': 'iniciando', 'web': '127.0.0.1:6088', 'vnc': '127.0.0.1:5908', 'processes': []}
    env = dict(os.environ, DISPLAY=f':{display}', XAUTHORITY=str(auth))
    try:
        xvfb = spawn(state, 'display', ['Xvfb', f':{display}', '-screen', '0', '1280x800x24',
                         '-nolisten', 'tcp', '-auth', str(auth)], env)
        for _ in range(50):
            probe = subprocess.run(['xdpyinfo'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if probe.returncode == 0:
                break
            if xvfb.poll() is not None:
                raise RuntimeError('Falló display privado')
            time.sleep(.1)
        else:
            raise RuntimeError('Display no respondió')
        if control:
            app = spawn(state, 'control', ['xmessage', '-geometry', '800x300+100+100', '-buttons', 'Aceptar:0',
                         '-default', 'Aceptar', 'OnIA: control del visor. No hay navegador ni cuenta abierta.'], env)
        else:
            profile = ROOT / 'browser-profile'
            profile.mkdir(mode=0o700, exist_ok=True)
            if profile.is_symlink() or profile.stat().st_mode & 0o077:
                raise RuntimeError('El perfil debe ser un directorio privado 0700')
            app = spawn(state, 'chromium', [str(CHROME), '--user-data-dir=' + str(profile),
                         '--no-first-run', '--no-default-browser-check', '--disable-breakpad',
                         '--window-size=1280,800', '--start-maximized',
                         'https://example.com/'], env)
        time.sleep(2)
        if app.poll() is not None:
            raise RuntimeError('La aplicación no inició. Revisar chromium.log; no desactivar sandbox.')
        venv = dict(env, LD_LIBRARY_PATH=str(RUNTIME / 'sysroot/usr/lib/x86_64-linux-gnu'))
        vnc = spawn(state, 'vnc', [str(RUNTIME / 'sysroot/usr/bin/x11vnc'), '-display', f':{display}',
                    '-auth', str(auth), '-localhost', '-listen', '127.0.0.1', '-no6', '-noipv6',
                    '-rfbport', '5908', '-passwdfile', str(PASSWORD), '-forever', '-nevershared',
                    '-nosel', '-noxrecord'], venv)
        wait_port(5908, vnc)
        web = spawn(state, 'web', [str(RUNTIME / 'websockify/run'), '--file-only',
                    '--web', str(RUNTIME / 'noVNC'), '127.0.0.1:6088', '127.0.0.1:5908'], env)
        wait_port(6088, web)
        state['status'] = 'listo'
        save(state)
        return state
    except Exception:
        finish(state)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comando', choices=['iniciar', 'estado', 'detener', 'prueba-visor'])
    args = parser.parse_args()
    os.umask(0o077)
    ROOT.mkdir(parents=True, mode=0o700, exist_ok=True)
    if ROOT.is_symlink() or ROOT.stat().st_mode & 0o077:
        raise SystemExit('La carpeta privada debe tener modo 0700')
    with (ROOT / 'visor.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.comando in ('iniciar', 'prueba-visor'):
            state = start(args.comando == 'prueba-visor')
        else:
            state = read_state()
            if args.comando == 'detener':
                finish(state)
        print(json.dumps(report(state), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
