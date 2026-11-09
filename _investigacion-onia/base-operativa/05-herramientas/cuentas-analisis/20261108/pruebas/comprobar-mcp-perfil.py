#!/usr/bin/env python3
"""Prueba de integración con un perfil sintético y un display propio en el VPS."""
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import secrets
import select
import signal
import subprocess
import sys
import tempfile
import threading
import time

MANAGER = Path(__file__).resolve().parents[1] / 'browser-vps.py'
sys.path.insert(0, str(MANAGER.parent))
SPEC = importlib.util.spec_from_file_location('browser_vps', MANAGER)
manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manager)


def sandbox_root(root):
    manager.ROOT = root
    manager.STATE = root / 'visor-estado.json'


def read_state():
    return manager.report(manager.read_state())


def invoke(command):
    return subprocess.Popen([sys.executable, '-B', __file__, str(manager.ROOT), command],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def control(command, error=None):
    with invoke(command) as proc:
        out, err = proc.communicate(timeout=10)
    if error is not None:
        assert proc.returncode != 0 and error in err.decode(), (proc.returncode, err)
    else:
        assert proc.returncode == 0, err
    return out


def read_message(proc, timeout=45):
    # Lee una línea aun si el cliente recibe notificaciones intercaladas.
    end = time.monotonic() + timeout
    line = bytearray()
    while not line.endswith(b'\n'):
        if not select.select([proc.stdout], [], [], max(0, end - time.monotonic()))[0]:
            raise AssertionError('El MCP no respondió')
        byte = os.read(proc.stdout.fileno(), 1)
        if not byte:
            raise AssertionError(proc.stderr.read().decode())
        line.extend(byte)
    return json.loads(line)


def send(proc, method, params, request_id=None, expected_error=None):
    msg = {'jsonrpc': '2.0', 'method': method, 'params': params}
    if request_id is not None:
        msg['id'] = request_id
    proc.stdin.write((json.dumps(msg) + '\n').encode())
    proc.stdin.flush()
    if request_id is None:
        return None
    while (response := read_message(proc)).get('id') != request_id:
        pass
    if expected_error:
        assert expected_error in response.get('error', {}).get('message', ''), response
        return None
    assert 'error' not in response, response
    return response['result']


def initialize(proc):
    send(proc, 'initialize', {
        'protocolVersion': '2024-11-05', 'capabilities': {},
        'clientInfo': {'name': 'perfil-sintetico', 'version': '1'}
    }, 1)
    send(proc, 'notifications/initialized', {})


def call(proc, name, args, number):
    result = send(proc, 'tools/call', {'name': name, 'arguments': args}, number)
    assert not result.get('isError'), result
    return result


class Demo(BaseHTTPRequestHandler):
    def do_GET(self):
        cookie = SimpleCookie(self.headers.get('Cookie'))
        session = cookie.get('onia-fixture')
        signed_in = session is not None and session.value == 'sesion-ficticia'
        if self.path == '/set':
            content = b"<script>localStorage.setItem('onia-test', 'perfil-conservado'); fetch('/ready')</script>"
        elif self.path == '/ready':
            self.server.arrived.set()
            content = b'OK'
        elif self.path == '/redirect':
            self.send_response(302)
            self.send_header('Location', '/check')
            self.end_headers()
            return
        else:
            content = b"<h1></h1><script>document.querySelector('h1').textContent = localStorage.getItem('onia-test') || 'perfil-vacio'</script>"
            if signed_in:
                content += b'<p>sesion-sintetica-activa</p>'
                if self.path == '/human-check':
                    self.server.human_checked.set()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        if self.path == '/set':
            self.send_header('Set-Cookie', 'onia-fixture=sesion-ficticia; Path=/; HttpOnly; Max-Age=3600')
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *_):
        pass


def start_viewer(root):
    run = root / 'sesion-sintetica'
    run.mkdir()
    auth = run / 'Xauthority'
    auth.touch()
    display = next(f':{n}' for n in range(130, 160)
                   if not Path(f'/tmp/.X{n}-lock').exists()
                   and not Path(f'/tmp/.X11-unix/X{n}').exists())
    subprocess.run(['xauth', '-f', str(auth)], input=f'add {display} . {secrets.token_hex(16)}\n',
                   text=True, check=True)
    xvfb = subprocess.Popen(['Xvfb', display, '-screen', '0', '1280x800x24',
                             '-nolisten', 'tcp', '-auth', str(auth)], stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
    for _ in range(50):
        env = dict(os.environ, DISPLAY=display, XAUTHORITY=str(auth))
        if subprocess.run(['xdpyinfo'], env=env, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode == 0:
            break
        if xvfb.poll() is not None:
            raise AssertionError(xvfb.stderr.read().decode())
        time.sleep(.1)
    else:
        xvfb.terminate()
        raise AssertionError('Xvfb no inició')
    state = {'display': display, 'run': str(run), 'mode': 'navegador-publico',
             'status': 'listo', 'processes': [manager.process_identity('display', xvfb.pid)]}
    for name in ('vnc', 'web'):
        manager.spawn(state, name, ['sleep', '240'], os.environ)
    return state


def browser_pid(profile):
    return int((profile / 'SingletonLock').readlink().name.rsplit('-', 1)[1])


def sandboxed_renderer(browser):
    children = [browser]
    while children:
        pid = children.pop()
        try:
            proc = Path(f'/proc/{pid}')
            children.extend(map(int, (proc / f'task/{pid}/children').read_text().split()))
            if b'--type=renderer' in (proc / 'cmdline').read_bytes():
                status = (proc / 'status').read_text().splitlines()
                if 'Seccomp:\t2' in status and 'NoNewPrivs:\t1' in status:
                    return True
        except FileNotFoundError:
            continue
    return False


def main():
    os.umask(0o077)
    sandbox_root(Path(tempfile.mkdtemp(prefix='onia-mcp-test-')))
    profile = manager.profile_path(create=True)
    demo = ThreadingHTTPServer(('127.0.0.1', 0), Demo)
    demo.arrived = threading.Event()
    demo.human_checked = threading.Event()
    threading.Thread(target=demo.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{demo.server_port}'
    urls = manager.ROOT / 'urls'
    urls.write_text('https://example.com/\n')
    assert manager.load_urls(urls) == {'https://example.com/'}
    urls.write_text(base + '/check\n' + base + '/redirect\n')
    state = start_viewer(manager.ROOT)
    viewer = {p['name']: p['pid'] for p in state['processes']}
    try:
        env = manager.viewer_env(state)
        first = manager.human_browser(state, env, profile, base + '/set')
        assert demo.arrived.wait(15), 'Chromium humano sintético no cargó'
        threading.Thread(target=first.wait, daemon=True).start()
        # localStorage confirma escritura al script antes del flush diferido en disco.
        time.sleep(6)
        proc = invoke('mcp')
        try:
            initialize(proc)
            current = read_state()
            assert current['status'] == 'mcp'
            assert not manager.live(manager.process_identity('chromium', first.pid))
            assert {p['name']: p['pid'] for p in current['processes'] if p['name'] in viewer} == viewer
            for operation in ('mcp', 'detener', 'recuperar', 'iniciar'):
                control(operation, 'préstamo del perfil')
            control('estado')
            tools = send(proc, 'tools/list', {}, 10)['tools']
            assert {tool['name'] for tool in tools} == {'browser_navigate', 'browser_snapshot', 'browser_close'}
            rejected = (
                ('browser_snapshot', {}, 'Navegar primero'),
                ('browser_evaluate', {}, 'Herramienta fuera'),
                ('browser_navigate', {'url': base + '/set'}, 'URL fuera'),
            )
            for index, (name, params, error) in enumerate(rejected, 11):
                send(proc, 'tools/call', {'name': name, 'arguments': params}, index, error)
            call(proc, 'browser_navigate', {'url': base + '/check'}, 2)
            send(proc, 'tools/call', {'name': 'browser_snapshot', 'arguments': {'filename': 'x'}},
                 16, 'no admite argumentos')
            result = json.dumps(call(proc, 'browser_snapshot', {}, 3))
            assert 'perfil-conservado' in result and 'sesion-sintetica-activa' in result, result
            pid = browser_pid(profile)
            argv = Path(f'/proc/{pid}/cmdline').read_bytes()
            assert b'--remote-debugging-pipe' in argv
            assert b'--remote-debugging-port' not in argv and b'--no-sandbox' not in argv
            assert sandboxed_renderer(pid)
            listeners = subprocess.check_output(['ss', '-ltnp'], text=True)
            mcp_pid = next(p['pid'] for p in current['processes'] if p['name'] == 'mcp')
            assert all(f'pid={n},' not in listeners for n in (pid, mcp_pid))
            assert manager.profile_busy(profile)
            send(proc, 'tools/call', {'name': 'browser_navigate', 'arguments': {'url': base + '/redirect'}},
                 17, 'no coincide')
            send(proc, 'tools/call', {'name': 'browser_snapshot', 'arguments': {}}, 18, 'Navegar primero')
            call(proc, 'browser_close', {}, 4)
        finally:
            proc.stdin.close()
            assert proc.wait(timeout=30) == 0, proc.stderr.read().decode()
        current = read_state()
        assert current['status'] == 'listo'
        human = manager.named_process(current, 'chromium')
        assert human and human['pid'] != first.pid
        assert 'mcp_inicio_utc' in current and 'mcp_fin_utc' in current
        # Chromium entrega la URL por su singleton al navegador humano restaurado.
        subprocess.run([str(manager.CHROME), '--user-data-dir=' + str(profile), base + '/human-check'],
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=10, check=True)
        assert demo.human_checked.wait(10), 'Chromium humano restaurado perdió la sesión ficticia'
        assert browser_pid(profile) == human['pid']

        # Corte después de registrar Chromium restaurado, antes de guardar "listo".
        recovered = manager.read_state()
        recovered['status'] = 'recuperar'
        mismatched = dict(recovered, processes=[
            manager.process_identity('chromium', viewer['vnc']) if proc['name'] == 'chromium' else proc
            for proc in recovered['processes']
        ])
        manager.save(mismatched)
        try:
            control('mcp', 'El propietario del perfil no coincide')
            assert manager.read_state() == mismatched and browser_pid(profile) == human['pid']
        finally:
            manager.save(recovered)

        proc = invoke('mcp')
        try:
            initialize(proc)
            call(proc, 'browser_navigate', {'url': base + '/check'}, 2)
            result = json.dumps(call(proc, 'browser_snapshot', {}, 3))
            assert 'perfil-conservado' in result and 'sesion-sintetica-activa' in result, result
            proc.send_signal(signal.SIGTERM)
            assert proc.wait(timeout=30) == 128 + signal.SIGTERM, proc.stderr.read().decode()
        finally:
            proc.stdin.close()
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=30)
        assert read_state()['status'] == 'listo'
        proc = invoke('mcp')
        try:
            initialize(proc)
            call(proc, 'browser_navigate', {'url': base + '/check'}, 2)
            proc.kill()
            assert proc.wait(timeout=10) == -signal.SIGKILL
        finally:
            proc.stdin.close()
        # La muerte del supervisor corta stdin del servidor. Hasta que éste
        # salga, su descriptor del lock y el singleton protegen el perfil.
        for _ in range(50):
            if not manager.named_process(read_state(), 'mcp'):
                break
            time.sleep(.2)
        else:
            raise AssertionError('El servidor MCP no salió al perder al supervisor')
        control('recuperar')
        assert read_state()['status'] == 'listo'
        assert all(manager.named_process(read_state(), name)['pid'] == pid for name, pid in viewer.items())
        print('OK: perfil y sesión HttpOnly sintéticos, traspaso exclusivo, destinos y herramientas acotados, '
              'stdio/pipe, EOF/SIGTERM/SIGKILL, reentrada conciliada y visor conservado.')
    finally:
        control('detener')
        demo.shutdown()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        sandbox_root(Path(sys.argv[1]))
        command = sys.argv[2]
        sys.argv = [sys.argv[0], command]
        if command == 'mcp':
            # Sólo el fixture acepta HTTP de loopback y sus dos rutas sintéticas.
            urls = manager.ROOT / 'urls'
            manager.load_urls = lambda path: frozenset(path.read_text().splitlines())
            sys.argv.extend(['--urls', str(urls)])
        try:
            sys.exit(manager.main())
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
            sys.exit(str(error))
    main()
