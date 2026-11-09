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
import stat
import sys
import tempfile
import subprocess
import time

from mcp_lectura import load_urls, relay

ROOT = Path.home() / 'operacion/cuentas/analisis-onia'
RUNTIME = ROOT / 'runtime-20261108'
INSTALL = Path.home() / 'operacion/browser-piloto-20261108'
CHROME = INSTALL / 'browsers/chromium-1252/chrome-linux64/chrome'
MCP = INSTALL / 'node_modules/@playwright/mcp/cli.js'
NODE = Path('/usr/bin/node')
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
    # estado puede leerse durante el préstamo del perfil.
    with tempfile.NamedTemporaryFile(mode='w', dir=ROOT, prefix='.visor-', delete=False) as temp:
        json.dump(state, temp, indent=2)
        temp.write('\n')
    os.replace(temp.name, STATE)


def report(state):
    return {**state, 'processes': [{**p, 'alive': live(p)} for p in state['processes']]}


def spawn(state, name, cmd, env):
    log = Path(state['run']) / (name + '.log')
    with log.open('ab') as out:
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=out,
                             env=env, start_new_session=True, close_fds=True)
    state['processes'].append(process_identity(name, p.pid))
    try:
        save(state)
    except OSError:
        p.terminate()
        p.wait(timeout=8)
        raise
    return p


def process_identity(name, pid):
    return {'name': name, 'pid': pid, 'start': stamp(pid), 'boot': BOOT}


def terminate(p):
    # Sólo un proceso registrado con identidad vigente.
    if not live(p):
        return
    try:
        fd = os.pidfd_open(p['pid'])
    except ProcessLookupError:
        return
    try:
        if live(p):
            signal.pidfd_send_signal(fd, signal.SIGTERM)
    except ProcessLookupError:
        return
    finally:
        os.close(fd)
    end = time.monotonic() + 8
    while live(p) and time.monotonic() < end:
        time.sleep(.1)
    if live(p):
        raise RuntimeError('Un proceso propio no confirmó cierre: ' + p['name'])


def close_human(browser, env, lock):
    helper = Path(__file__).with_name('cerrar-ventanas-x11.py')
    if not live(browser):
        return
    result = subprocess.run([sys.executable, str(helper), str(browser['pid'])],
                            env=dict(env, LC_ALL='C'), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, timeout=10, pass_fds=(lock.fileno(),))
    if result.returncode and live(browser):
        raise RuntimeError('Chromium no aceptó el cierre de ventana. Se conserva el visor.')
    end = time.monotonic() + 8
    while live(browser) and time.monotonic() < end:
        time.sleep(.1)
    if live(browser):
        raise RuntimeError('Chromium no terminó el cierre de ventana. Se conserva el visor.')


def finish(state):
    for p in reversed(state['processes']):
        terminate(p)
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


def private_dir(path, create=False):
    if create:
        path.mkdir(mode=0o700, exist_ok=True)
    mode = path.lstat()
    if not stat.S_ISDIR(mode.st_mode) or mode.st_uid != os.getuid() or mode.st_mode & 0o077:
        raise RuntimeError(f'Directorio propio y privado requerido: {path}')
    return path


def profile_path(create=False):
    return private_dir(ROOT / 'browser-profile', create)


def named_process(state, name):
    return next((p for p in state['processes'] if p['name'] == name and live(p)), None)


def profile_singleton(profile):
    try:
        return os.readlink(profile / 'SingletonLock')
    except FileNotFoundError:
        return None


def profile_busy(profile):
    # También cubre un Chromium huérfano que sobrevivió al servidor MCP.
    # Nunca se mata un proceso encontrado mediante el SingletonLock.
    target = profile_singleton(profile)
    if target:
        host, _, pid = target.rpartition('-')
        if host != socket.gethostname() or not pid.isdecimal() or stamp(int(pid)):
            return True
    argument = os.fsencode('--user-data-dir=' + str(profile))
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            if (entry / 'exe').readlink() != CHROME:
                continue
            # Chromium puede reescribir argv como una cadena de argumentos.
            argv = (entry / 'cmdline').read_bytes().replace(b'\0', b' ')
            if b' ' + argument + b' ' in argv + b' ':
                return True
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return False


def await_free_profile(profile):
    for _ in range(50):
        if not profile_busy(profile):
            return
        time.sleep(.1)
    raise RuntimeError('El perfil sigue ocupado. Consultar estado antes de recuperarlo.')


def human_browser(state, env, profile, url):
    if profile_busy(profile):
        raise RuntimeError('El perfil sigue ocupado. Consultar estado antes de recuperarlo.')
    return spawn(state, 'chromium', [str(CHROME), '--user-data-dir=' + str(profile),
                 '--no-first-run', '--no-default-browser-check', '--disable-breakpad',
                 '--window-size=1280,800', '--start-maximized', url], env)


def viewer_env(state):
    if any(not named_process(state, name) for name in ('display', 'vnc', 'web')):
        raise RuntimeError('Hace falta el visor completo y activo.')
    display = state['display']
    if not display.startswith(':') or not display[1:].isdecimal():
        raise RuntimeError('Display privado inválido.')
    run = Path(state['run'])
    if run.parent != ROOT:
        raise RuntimeError('La sesión del visor no está dentro de la carpeta privada.')
    private_dir(run)
    auth = run / 'Xauthority'
    mode = auth.lstat()
    if not stat.S_ISREG(mode.st_mode) or mode.st_uid != os.getuid() or mode.st_mode & 0o077:
        raise RuntimeError('Xauthority debe ser un archivo propio y privado.')
    return dict(os.environ, DISPLAY=display, XAUTHORITY=str(auth))


def restore_human(state, env, profile):
    if named_process(state, 'mcp'):
        raise RuntimeError('El servidor MCP sigue activo. Consultar estado.')
    if not named_process(state, 'chromium'):
        await_free_profile(profile)
        state['processes'] = [p for p in state['processes'] if p['name'] not in ('chromium', 'mcp')]
        browser = human_browser(state, env, profile, 'about:blank')
        time.sleep(1)
        if browser.poll() is not None:
            raise RuntimeError('Chromium humano no inició. Consultar chromium.log.')
    state['status'] = 'listo'
    save(state)
    return state


def mcp_command(state, env, profile):
    if not all(path.is_file() for path in (MCP, CHROME, NODE)):
        raise RuntimeError('Falta la instalación existente de Chromium o Playwright MCP.')
    run = Path(state['run'])
    workspace = private_dir(run / 'mcp', create=True)
    config = run / 'playwright-mcp.json'
    # El Chromium humano y Playwright deben elegir el mismo backend del perfil.
    config.write_text(json.dumps({'browser': {'launchOptions': {
        'ignoreDefaultArgs': ['--disable-field-trial-config', '--password-store=basic'],
    }, 'contextOptions': {'acceptDownloads': False}}}) + '\n')
    sockets = private_dir(ROOT / '.mcp-sockets', create=True)
    # Playwright 0.0.84 enlaza un socket Unix adicional además del pipe CDP.
    if len(os.fsencode(sockets / 'browser' / ('0' * 16 + '.sock'))) > 103:
        raise RuntimeError('Ruta demasiado larga para el socket Unix privado de Playwright.')
    # Entorno explícito. No hereda flags PLAYWRIGHT_MCP_*, NODE_OPTIONS ni tokens.
    mcp_env = {k: env[k] for k in ('LANG', 'LC_ALL', 'USER', 'LOGNAME', 'XDG_RUNTIME_DIR',
                                 'XDG_CURRENT_DESKTOP', 'DESKTOP_SESSION', 'DBUS_SESSION_BUS_ADDRESS') if k in env}
    mcp_env.update(HOME=str(Path.home()), PATH='/usr/bin:/bin',
                   DISPLAY=env['DISPLAY'], XAUTHORITY=env['XAUTHORITY'],
                   XDG_CACHE_HOME=str(run / 'mcp-cache'),
                   XDG_CONFIG_HOME=str(run / 'mcp-config'), PWTEST_SOCKETS_DIR=str(sockets))
    command = [str(NODE), str(MCP), '--config', str(config), '--sandbox', '--user-data-dir', str(profile),
               '--executable-path', str(CHROME), '--ignore-roots', '--no-webmcp',
               '--image-responses', 'omit', '--codegen', 'none', '--snapshot-mode', 'none',
               '--output-dir', str(workspace)]
    return command, mcp_env, workspace


def serve_mcp(lock, urls):
    state = read_state()
    status = state.get('status')
    if state.get('mode') != 'navegador-publico' or status not in ('listo', 'recuperar'):
        raise RuntimeError('El visor humano debe estar listo. Consultar estado y recuperar.')
    human = named_process(state, 'chromium')
    if not human or named_process(state, 'mcp'):
        raise RuntimeError('Falta Chromium humano o existe otra conexión. Consultar estado.')
    env, profile = viewer_env(state), profile_path()
    if status == 'recuperar':
        # El supervisor previo pudo terminar después de abrir Chromium humano
        # y guardar su identidad, antes de marcar el visor como listo.
        owner = f'{socket.gethostname()}-{human["pid"]}'
        if profile_singleton(profile) != owner or not live(human):
            raise RuntimeError('El propietario del perfil no coincide con Chromium humano registrado.')
    command, mcp_env, workspace = mcp_command(state, env, profile)
    # Las señales blandas se traducen en cierre ordenado del servidor y restauración.
    interrupted = None

    def request_close(signum, _frame):
        nonlocal interrupted
        interrupted = signum

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, request_close)
    child = None
    state['status'] = 'traspaso-mcp'
    state['mcp_inicio_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    state.pop('mcp_fin_utc', None)
    save(state)
    try:
        close_human(human, env, lock)
        await_free_profile(profile)
        if interrupted is None:
            # El hijo conserva el préstamo incluso si este supervisor recibe SIGKILL.
            child = subprocess.Popen(command, cwd=workspace, env=mcp_env,
                                     start_new_session=True, pass_fds=(lock.fileno(),),
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            state['processes'].append(process_identity('mcp', child.pid))
            state['status'] = 'mcp'
            save(state)
            relay(child, urls, lambda: interrupted)
    finally:
        if child is not None and child.poll() is None:
            child.terminate()
            # El watchdog del MCP espera un máximo de 15 s para cerrar el perfil.
            try:
                child.wait(timeout=18)
            except subprocess.TimeoutExpired:
                # Sólo el servidor propio. La recuperación comprobará el perfil
                # y rechazará abrir Chromium si aún queda un proceso del perfil.
                child.kill()
                child.wait(timeout=3)
        state['status'] = 'recuperar'
        state['mcp_fin_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save(state)
        restore_human(state, viewer_env(state), profile)
    if interrupted is not None:
        return 128 + interrupted
    return child.returncode if child is not None else 1


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
            app = human_browser(state, env, profile_path(create=True), 'https://example.com/')
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
    parser.add_argument('comando', choices=['iniciar', 'estado', 'detener', 'prueba-visor', 'mcp', 'recuperar'])
    parser.add_argument('--urls', type=Path, help='Lista privada de destinos HTTPS, requerida para mcp.')
    args = parser.parse_args()
    if args.comando == 'mcp' and args.urls is None:
        parser.error('mcp requiere --urls')
    os.umask(0o077)
    if args.comando == 'estado':
        print(json.dumps(report(read_state()), ensure_ascii=False, indent=2))
        return 0
    if args.comando in ('iniciar', 'prueba-visor'):
        ROOT.mkdir(parents=True, mode=0o700, exist_ok=True)
    private_dir(ROOT)
    with (ROOT / 'visor.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Otro comando o servidor MCP tiene el préstamo del perfil.') from None
        if args.comando == 'mcp':
            return serve_mcp(lock, load_urls(args.urls))
        if args.comando in ('iniciar', 'prueba-visor'):
            state = start(args.comando == 'prueba-visor')
        else:
            state = read_state()
            if args.comando == 'detener':
                finish(state)
            elif state.get('mode') == 'navegador-publico':
                restore_human(state, viewer_env(state), profile_path())
            else:
                raise RuntimeError('No hay una sesión de navegador que recuperar.')
        print(json.dumps(report(state), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
