"""Control temporal privado del runtime existente. CLI de preparación/monitor/fin.

No lanza sesiones. Las admisiones siguen pasando por harness_sesiones.
"""
from contextlib import contextmanager, ExitStack
import argparse
import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import sys
import time
import uuid

import harness_boss as private
import harness_sesiones as sessions

DIRECTORY = 'ensayo-cuatro'
QUOTA_PREFLIGHT = 'ensayo-cuatro-preflight'
RESOURCE_TTL = 15
QUOTA_TTL = 60
MAX_DURATION = 1800
BUDGET = 2


def require(condition, message):
    if not condition:
        raise ValueError('ensayo_' + message)


def number(value, minimum=0, maximum=float('inf')):
    require(type(value) in (int, float) and (type(value) is int or math.isfinite(value))
            and minimum <= value <= maximum, 'numero_invalido')
    return value


def fresh(timestamp, ttl, now):
    number(timestamp)
    require(0 <= now - timestamp <= ttl, 'dato_caduco_o_futuro')


def directory(root):
    root = private.no_links(Path(root).absolute())
    info = root.stat()
    require(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid()
            and info.st_mode & 0o022 == 0, 'operacion_insegura')
    path = private.no_links(root / DIRECTORY)
    info = path.stat()
    require(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid()
            and info.st_mode & 0o077 == 0, 'directorio_no_privado')
    return path


def read(path):
    value = private.private_read(path)
    require(path.stat().st_nlink == 1, 'enlace_duro_no_permitido')
    require(isinstance(value, dict), 'objeto_invalido')
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def policy(root, now=None, expired=False):
    now = time.time() if now is None else now
    path = directory(root)
    value = read(path / 'politica.json')
    require(set(value) == {'schema', 'lote', 'base', 'ids', 'inicio', 'vence', 'presupuesto',
                           'cuota_inicial'}, 'politica_invalida')
    require(type(value['schema']) is int and value['schema'] == 1, 'schema_invalido')
    require(isinstance(value['lote'], str) and len(value['lote']) == 32
            and all(char in '0123456789abcdef' for char in value['lote']), 'lote_invalido')
    base = private.no_links(value['base'])
    require(base.is_absolute() and str(base) == value['base'] and base.is_dir(), 'base_invalida')
    ids = value['ids']
    require(isinstance(ids, list) and bool(ids)
            and all(isinstance(i, str) and private.SAFE.fullmatch(i) for i in ids)
            and len(set(ids)) == len(ids), 'ids_invalidos')
    number(value['inicio'])
    number(value['vence'])
    require(0 < value['vence'] - value['inicio'] <= MAX_DURATION, 'duracion_invalida')
    require(value['inicio'] <= now, 'inicio_futuro')
    if not expired:
        require(now < value['vence'], 'vencido')
    require(type(value['presupuesto']) is int and value['presupuesto'] == BUDGET, 'presupuesto_invalido')
    quota(value['cuota_inicial'], value['inicio'])
    return value


def quota(value, now):
    require(isinstance(value, dict) and set(value) == {'fecha', 'ventanas'}, 'cuota_desconocida')
    fresh(value['fecha'], QUOTA_TTL, now)
    windows = value['ventanas']
    require(isinstance(windows, dict) and set(windows) in ({'primary'}, {'primary', 'secondary'}), 'cuota_desconocida')
    for window in windows.values():
        require(isinstance(window, dict) and set(window) == {'usedPercent', 'windowDurationMins', 'resetsAt'},
                'cuota_desconocida')
        number(window['usedPercent'], 0, 100)
        number(window['windowDurationMins'], 1)
        require(number(window['resetsAt'], 1) > now, 'ventana_vencida')
    return value


def quota_budget(initial, current, now):
    quota(current, now)
    require(set(initial['ventanas']) == set(current['ventanas']), 'ventana_cambiada')
    for name, before in initial['ventanas'].items():
        after = current['ventanas'][name]
        require(all(before[k] == after[k] for k in ('windowDurationMins', 'resetsAt')),
                'ventana_cambiada')
        spent = after['usedPercent'] - before['usedPercent']
        require(0 <= spent < BUDGET and after['usedPercent'] < 100, 'presupuesto_agotado_o_cuota_alterada')


def resources(value, now):
    require(isinstance(value, dict) and set(value) == {'fecha', 'cpu', 'ram_disponible',
            'psi_cpu', 'psi_memoria', 'psi_io', 'swap_usado', 'swap_paginas_s'}, 'recursos_desconocidos')
    fresh(value['fecha'], RESOURCE_TTL, now)
    for name in ('cpu', 'ram_disponible', 'psi_cpu', 'psi_memoria', 'psi_io', 'swap_usado'):
        number(value[name], 0, 100)
    number(value['swap_paginas_s'])
    require(value['cpu'] < 85 and value['ram_disponible'] >= 20
            and value['psi_cpu'] < 20 and value['psi_memoria'] < 10 and value['psi_io'] < 10
            and value['swap_paginas_s'] < 256, 'saturacion')


def health(root, value, now=None):
    now = time.time() if now is None else now
    path = directory(root)
    require(not os.path.lexists(path / 'STOP'), 'STOP')
    current = read(path / 'estado.json')
    require(read(path / 'preparacion.json').get('politica_sha256') == digest(value), 'politica_alterada')
    recorded = read_receipt(path, current.pop('recibo', None), changed='estado_alterado')
    require(recorded == dict(current, evento='muestra'), 'estado_alterado')
    require(current.get('politica_sha256') == digest(value), 'politica_alterada')
    journal = read(path / 'procesos.json')
    require(journal.get('politica_sha256') == digest(value)
            and current.get('procesos_sha256') == digest(journal), 'inventario_alterado')
    require(current.get('estado') == 'listo', 'monitor_bloqueado')
    fresh(current.get('fecha'), RESOURCE_TTL, now)
    pid = current.get('pid')
    require(type(pid) is int and pid > 0 and isinstance(current.get('pid_inicio'), str)
            and sessions.process_start(pid) == current['pid_inicio'], 'monitor_muerto_o_reciclado')
    require(Path('/proc', str(pid)).stat().st_uid == os.getuid(), 'monitor_ajeno')
    quota_budget(value['cuota_inicial'], current.get('cuota'), now)
    resources(current.get('recursos'), now)
    return current


def live_sessions(rows):
    return [(str(base), row['id'], s) for base, row in rows for s in row.get('sesiones', [])
            if sessions.alive(s) or (s.get('dry_run') and s.get('estado') == 'simulada')]


def members(value, rows, questions):
    tag = digest(value)
    result = live_sessions(rows)
    for ident, slot in questions:
        result.append((slot.get('base'), ident, slot))
    require(len(result) <= 4, 'mas_de_cuatro')
    seen = set()
    for base, ident, item in result:
        require(base == value['base'] and ident in value['ids']
                and item.get('ensayo_sha256') == tag and not item.get('dry_run'), 'sesion_ajena')
        require(ident not in seen, 'id_duplicado')
        seen.add(ident)
    return result


def admission(root, base, ident, rows, questions):
    """Devuelve la huella del permiso, o None para los tres cupos habituales."""
    if root is None or not os.path.lexists(Path(root) / DIRECTORY):
        return None
    value = policy(root)
    require(str(base) == value['base'] and ident in value['ids'], 'id_o_base_no_autorizado')
    health(root, value)
    members(value, rows, questions)
    require_verified_owners(root, value, rows)
    return digest(value)


def revalidate(root, base, ident, tag):
    value = policy(root)
    require(str(base) == value['base'] and ident in value['ids'] and digest(value) == tag,
            'permiso_cambiado')
    health(root, value)


def quota_response(result, now):
    """Primary is required; providers may omit or null the secondary window."""
    require(isinstance(result, dict), 'cuota_desconocida')
    by_id = result.get('rateLimitsByLimitId')
    if by_id:
        require(isinstance(by_id, dict), 'cuota_desconocida')
        limits = by_id.get('codex')
    else:
        limits = result.get('rateLimits')
    require(isinstance(limits, dict), 'cuota_desconocida')
    windows = {}
    for key in ('primary', 'secondary'):
        window = limits.get(key)
        if key == 'secondary' and window is None:
            continue
        require(isinstance(window, dict), 'cuota_desconocida')
        windows[key] = {field: window.get(field)
                        for field in ('usedPercent', 'windowDurationMins', 'resetsAt')}
    return quota({'fecha': now, 'ventanas': windows}, now)


def read_quota(deadline=None, stop_path=None, *, preflight_root=None):
    end = min(time.time() + 50, deadline if deadline is not None else float('inf'))
    require(end > time.time(), 'rpc_timeout')
    if stop_path:
        stop_path = Path(stop_path)
        root = stop_path.parent.parent
        path = directory(root)
        tag = digest(policy(root, expired=True))
    else:
        require(preflight_root is not None, 'preflight_raiz_requerida')
        path = private.no_links(Path(preflight_root) / QUOTA_PREFLIGHT)
        path.mkdir(mode=0o700, exist_ok=True)
        info = path.stat()
        require(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid()
                and info.st_mode & 0o077 == 0, 'preflight_no_privado')
        tag = QUOTA_PREFLIGHT
        require(not os.path.lexists(path / 'STOP')
                and not pending_custody_files(path, tag, {}), 'preflight_sin_drenaje')

    gate_read, gate_write = os.pipe()
    process = None
    identity = None
    try:
        with os.fdopen(gate_read, 'rb', buffering=0) as gate_in, \
                os.fdopen(gate_write, 'wb', buffering=0) as gate_out:
            argv = subprocess_entry('quota_worker', [str(end), str(stop_path) if stop_path else '',
                                                     str(path), tag, str(gate_read)])
            process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                       pass_fds=(gate_in.fileno(),))
            identity = custody_identity(
                {'pid': process.pid, 'pid_inicio': sessions.process_start(process.pid)}, tag)
            private.private_write(quota_registration(path, identity),
                                  dict(identity, evento='lector_cuota_registrado'))
            gate_out.write(b'1')
        output, _ = process.communicate(timeout=max(0, end - time.time()) + 5)
    finally:
        if process is not None:
            try:
                if process.poll() is None:
                    if identity is not None:
                        terminate([identity])
                    process.wait(timeout=5)
            finally:
                process.stdout.close()
    require(process.returncode == 0, 'rpc_sin_drenaje_o_fallido')
    return quota(json.loads(output), time.time())


def quota_worker(deadline, stop, scope, tag, gate):
    with os.fdopen(int(gate), 'rb', buffering=0) as gate_in:
        if gate_in.read(1) != b'1':
            return 125
    path = Path(scope)
    with Custody(path, tag) as owner:
        require(read(quota_registration(path, owner.identity)) ==
                dict(owner.identity, evento='lector_cuota_registrado'), 'lector_cuota_sin_registro')
        value = read_quota_rpc(owner, float(deadline), Path(stop) if stop else None)
    print(json.dumps(value), flush=True)
    return 0


def read_quota_rpc(owner, deadline, stop_path):
    """RPC de sólo lectura cotejado con /tmp/onia-read-quota-rpc.py.

    Usar directamente el protocolo permite terminar por pidfd+SIGTERM incluso
    cuando vence el ensayo mientras el RPC espera. No ejecutar código de /tmp.
    """
    require(hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'), 'pidfd_no_disponible')
    require(stop_path is None or not os.path.lexists(stop_path), 'STOP')
    require(not owner.stopping, 'cuota_interrumpida')
    owner.child = process = subprocess.Popen(['codex', 'app-server', '--listen', 'stdio://'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               env=sessions.child_environment({'auth_chatgpt': True}))
    end = deadline
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    pending = b''

    def rpc(ident, method, params):
        nonlocal pending
        request = {'method': method, 'params': params}
        if ident is not None:
            request['id'] = ident
        process.stdin.write((json.dumps(request) + '\n').encode())
        process.stdin.flush()
        if ident is None:
            return None
        while time.time() < end:
            require(stop_path is None or not os.path.lexists(stop_path), 'STOP')
            require(not owner.stopping, 'cuota_interrumpida')
            if b'\n' not in pending:
                if not selector.select(min(0.2, max(0, end - time.time()))):
                    continue
                chunk = os.read(process.stdout.fileno(), 65536)
                require(bool(chunk), 'rpc_interrumpido')
                pending += chunk
                require(len(pending) <= 262144, 'rpc_excesivo')
            while b'\n' in pending:
                line, pending = pending.split(b'\n', 1)
                value = json.loads(line)
                if value.get('id') == ident:
                    require('error' not in value, 'rpc_rechazado')
                    return value['result']
        raise ValueError('ensayo_rpc_timeout')

    try:
        rpc(1, 'initialize', {'clientInfo': {'name': 'onia_quota_readonly', 'version': '1.0'}})
        rpc(None, 'initialized', {})
        result = rpc(2, 'account/rateLimits/read', {'excludeResetCreditDetails': True})
        return quota_response(result, time.time())
    finally:
        selector.close()
        process.stdin.close()
        process.stdout.close()


def counters():
    cpu = [int(x) for x in Path('/proc/stat').read_text().splitlines()[0].split()[1:9]]
    memory = {line.split()[0].rstrip(':'): int(line.split()[1])
              for line in Path('/proc/meminfo').read_text().splitlines()}
    vm = {line.split()[0]: int(line.split()[1]) for line in Path('/proc/vmstat').read_text().splitlines()}
    pressure = {}
    for name in ('cpu', 'memory', 'io'):
        some = next(line for line in Path('/proc/pressure', name).read_text().splitlines()
                    if line.startswith('some '))
        pressure[name] = float(dict(field.split('=') for field in some.split()[1:])['avg10'])
    return cpu, memory, vm['pswpin'] + vm['pswpout'], pressure


def read_resources():
    before, _, swap_before, _ = counters()
    start = time.monotonic()
    time.sleep(0.2)
    after, memory, swap_after, pressure = counters()
    elapsed = time.monotonic() - start
    total = sum(after) - sum(before)
    require(total > 0 and swap_after >= swap_before, 'contadores_invalidos')
    idle = after[3] + after[4] - before[3] - before[4]
    return {'fecha': time.time(), 'cpu': 100 * (1 - idle / total),
            'ram_disponible': 100 * memory['MemAvailable'] / memory['MemTotal'],
            'psi_cpu': pressure['cpu'], 'psi_memoria': pressure['memory'], 'psi_io': pressure['io'],
            'swap_usado': 100 * (1 - memory['SwapFree'] / memory['SwapTotal']) if memory['SwapTotal'] else 0,
            'swap_paginas_s': (swap_after - swap_before) / elapsed}


def prepare(root, base, ids, duration):
    require(type(duration) is int and 1 <= duration <= MAX_DURATION, 'duracion_invalida')
    root = sessions.operation(root)
    with sessions.registry_lock(root):
        info = root.stat()
        require(info.st_uid == os.getuid() and info.st_mode & 0o022 == 0, 'operacion_insegura')
        require(not os.path.lexists(root / DIRECTORY), 'lote_existente_conservar')
        # Preparar requiere un registro global conciliable y libre.
        require(not live_sessions(sessions.indexed_rows(root, base))
                and not sessions.active_questions(root), 'registro_ocupado')
        require(isinstance(ids, list) and bool(ids) and len(set(ids)) == len(ids), 'ids_invalidos')
        for ident in ids:
            private.checked_id(ident)
        require(private.no_links(base) == base and base.is_dir(), 'base_invalida')
        initial = read_quota(preflight_root=root)
        now = time.time()
        value = {'schema': 1, 'lote': uuid.uuid4().hex, 'base': str(base), 'ids': ids,
                 'inicio': now, 'vence': now + duration, 'presupuesto': BUDGET,
                 'cuota_inicial': initial}
        quota_budget(initial, initial, now)
        sample = read_resources()
        resources(sample, time.time())
        path = root / DIRECTORY
        path.mkdir(mode=0o700)
        try:
            private.private_write(path / 'politica.json', value)
            policy(root)
        except Exception:
            private.private_write(path / 'STOP', {'motivo': 'preparacion_invalida'})
            raise
        private.private_write(path / 'preparacion.json', {'politica_sha256': digest(value),
                              'cuota': initial, 'recursos': sample, 'fecha': now})
    return {'estado': 'preparado', 'monitor_requerido': True}


def process_info(pid):
    info = Path('/proc', str(pid)).stat()
    fields = Path('/proc', str(pid), 'stat').read_text().rsplit(')', 1)[1].split()
    return info.st_uid, int(fields[1])


def process_tree(seeds):
    """Identidades observadas con ascendencia comprobada. No usar grupos Unix."""
    found = {}
    for item in seeds:
        pid, start = item.get('pid'), item.get('pid_inicio')
        if type(pid) is int and start and sessions.process_start(pid) == start:
            require(process_info(pid)[0] == os.getuid(), 'proceso_ajeno')
            found[pid] = start
    # Un recorrido del árbol, sin asumir que los PIDs sean crecientes.
    pending = {int(p.name) for p in Path('/proc').iterdir() if p.name.isdigit()}
    while pending:
        added = set()
        for pid in pending:
            try:
                uid, parent = process_info(pid)
                start = sessions.process_start(pid)
                if parent in found and start and sessions.process_start(parent) == found[parent]:
                    require(uid == os.getuid(), 'descendiente_ajeno')
                    # Releer ascendencia tras identificar ambos extremos.
                    require(process_info(pid)[1] == parent and sessions.process_start(pid) == start,
                            'arbol_cambio')
                    found[pid] = start
                    added.add(pid)
            except (FileNotFoundError, ProcessLookupError):
                continue
        if not added:
            break
        pending -= added
    return [{'pid': pid, 'pid_inicio': start} for pid, start in sorted(found.items())]


def terminate(items):
    require(hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'), 'pidfd_no_disponible')
    for item in items:
        pid, start = item['pid'], item['pid_inicio']
        require(type(pid) is int and pid > 1 and pid != os.getpid() and isinstance(start, str),
                'identidad_invalida')
    sent, skipped = [], []
    for item in items:
        pid, start = item['pid'], item['pid_inicio']
        try:
            fd = os.pidfd_open(pid)
        except ProcessLookupError:
            skipped.append(item)
            continue
        try:
            if sessions.process_start(pid) != start:
                skipped.append(item)
                continue
            require(process_info(pid)[0] == os.getuid(), 'proceso_ajeno')
            signal.pidfd_send_signal(fd, signal.SIGTERM)
            sent.append(item)
        except ProcessLookupError:
            skipped.append(item)
        finally:
            os.close(fd)
    return sent, skipped



# Linux includes clone children with other exit signals in the wait proof.
WAIT_ALL = 0x40000000


def custody_path(path, identity):
    return path / ('custodia-' + digest(identity) + '.json')


def quota_registration(path, identity):
    return path / ('cuota-' + digest(identity) + '.json')


def custody_identity(record, tag):
    pid, start = record.get('pid'), record.get('pid_inicio')
    require(type(pid) is int and pid > 1 and isinstance(start, str) and bool(start),
            'identidad_custodia_invalida')
    return {'pid': pid, 'pid_inicio': start, 'politica_sha256': tag}


class Custody:
    """Dedicated subreaper for one executable and its descendants."""

    def __init__(self, path, tag):
        self.identity = custody_identity(
            {'pid': os.getpid(), 'pid_inicio': sessions.process_start(os.getpid())}, tag)
        self.path = custody_path(path, self.identity)
        self.child = None
        self.stopping = False

    def __enter__(self):
        require(not os.path.lexists(self.path), 'custodia_existente')
        # PR_SET_CHILD_SUBREAPER: even a double fork or setsid reparents here.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), 'PR_SET_CHILD_SUBREAPER')
        signal.signal(signal.SIGTERM, self.request_stop)
        private.private_write(self.path, dict(self.identity, estado='pendiente'))
        return self

    def request_stop(self, _signum, _frame):
        self.stopping = True

    def __exit__(self, _type, _value, _traceback):
        try:
            self.drain()
        except Exception:
            private.private_write(self.path.parent / 'STOP',
                                  {'motivo': 'custodia_sin_cierre', 'fecha': time.time()})
            raise

    def drain(self):
        end = time.monotonic() + 3
        sent = set()
        while True:
            # Popen must collect its own child's status before waitpid(-1).
            if self.child is None or self.child.poll() is not None:
                try:
                    pid, _status = os.waitpid(-1, os.WNOHANG | WAIT_ALL)
                except ChildProcessError:
                    reference = receipt(self.path.parent, dict(self.identity, evento='custodia_echild'))
                    private.private_write(self.path, dict(self.identity, estado='drenada', recibo=reference))
                    return
                if pid:
                    continue
            require(time.monotonic() < end, 'descendientes_sin_drenar')
            try:
                children = [i for i in process_tree([self.identity])
                            if i['pid'] != self.identity['pid']
                            and (i['pid'], i['pid_inicio']) not in sent]
            except ValueError as exc:
                if str(exc) != 'ensayo_arbol_cambio':
                    raise
                children = []
            terminated, _skipped = terminate(children)
            sent.update((i['pid'], i['pid_inicio']) for i in terminated)
            time.sleep(0.05)


def run_in_custody(root, base, ident, tag, argv, gate_read=None):
    with Custody(directory(root), tag) as owner:
        if gate_read is not None:
            with os.fdopen(gate_read, 'rb', buffering=0) as gate:
                if gate.read(1) != b'1':
                    return 125
        revalidate(root, base, ident, tag)
        if owner.stopping:
            return 143
        owner.child = subprocess.Popen(argv)
        while owner.child.poll() is None and not owner.stopping:
            time.sleep(0.05)
        return 143 if owner.stopping else owner.child.returncode


def subprocess_entry(function, args):
    bootstrap = """import sys
sys.path.insert(0, sys.argv[1])
import harness_ensayo
sys.exit(getattr(harness_ensayo, sys.argv[2])(*sys.argv[3:]))
"""
    return [sys.executable, '-B', '-c', bootstrap, str(Path(__file__).resolve().parent), function, *args]


def custody_worker(root, base, ident, tag, gate, *argv):
    return run_in_custody(Path(root), Path(base), ident, tag, argv, int(gate) if gate else None)


def custody_command(root, base, ident, tag, argv, gate_read=None):
    # Establish custody before waiting for the existing PID registration gate.
    return subprocess_entry('custody_worker',
                            [str(root), str(base), ident, tag, '' if gate_read is None else str(gate_read), *argv])


def pending_custodies(root, value, rows):
    """Check historical attempts too. A dead PID without proof remains uncertain."""
    tag = digest(value)
    expected = {}
    for base, row in rows:
        if str(base) != value['base'] or row['id'] not in value['ids']:
            continue
        for record in row.get('sesiones', []):
            if record.get('ensayo_sha256') == tag and record.get('pid') is not None:
                identity = custody_identity(record, tag)
                expected[digest(identity)] = identity

    slots = sessions.private_path(root, 'preguntas-slots')
    for ident in value['ids']:
        path = slots / (ident + '.json')
        if os.path.lexists(path):
            record = read(path)
            if record.get('ensayo_sha256') == tag and record.get('pid') is not None:
                require(record.get('base') == value['base'], 'slot_ajeno')
                identity = custody_identity(record, tag)
                expected[digest(identity)] = identity

    return pending_custody_files(directory(root), tag, expected)


def pending_custody_files(folder, tag, expected):
    for path in folder.glob('cuota-*.json'):
        record = read(path)
        identity = custody_identity(record, tag)
        require(path == quota_registration(folder, identity)
                and record == dict(identity, evento='lector_cuota_registrado'), 'lector_cuota_alterado')
        expected[digest(identity)] = identity

    pending = dict(expected)
    for path in folder.glob('custodia-*.json'):
        record = read(path)
        identity = custody_identity(record, tag)
        key = digest(identity)
        require(path == custody_path(folder, identity) and
                record.get('politica_sha256') == tag and
                record.get('estado') in {'pendiente', 'drenada'}, 'custodia_alterada')
        # A receipt cannot grant process ownership by itself.
        require(expected.get(key) == identity, 'custodia_sin_registro')
        if record['estado'] == 'drenada':
            require(read_receipt(folder, record.get('recibo')) ==
                    dict(identity, evento='custodia_echild'), 'custodia_alterada')
            pending.pop(key, None)
        else:
            require(set(record) == set(identity) | {'estado'}, 'custodia_alterada')
    return list(pending.values())


def require_verified_owners(root, value, rows):
    for owner in pending_custodies(root, value, rows):
        require(sessions.process_start(owner['pid']) == owner['pid_inicio'],
                'custodia_sin_cierre')


def inventory(root, value):
    rows = sessions.indexed_rows(root, Path(value['base']))
    questions = sessions.active_questions(root)
    # Para parar se selecciona sólo pertenencia exacta, aunque haya ajenos vivos.
    owned = [s for base, ident, s in live_sessions(rows)
             if base == value['base'] and ident in value['ids']
             and s.get('ensayo_sha256') == digest(value)]
    owned.extend(s for ident, s in questions if s.get('base') == value['base']
                 and ident in value['ids'] and s.get('ensayo_sha256') == digest(value))
    return rows, questions, owned


def receipt(path, event):
    name = 'recibo-' + str(time.time_ns()) + '-' + uuid.uuid4().hex + '.json'
    private.private_write(path / name, event)
    return {'archivo': name, 'sha256': digest(event)}


def read_receipt(path, reference, *, changed='recibo_alterado'):
    require(isinstance(reference, dict) and set(reference) == {'archivo', 'sha256'}
            and isinstance(reference['archivo'], str)
            and Path(reference['archivo']).name == reference['archivo']
            and reference['archivo'].startswith('recibo-'), 'recibo_invalido')
    recorded = read(path / reference['archivo'])
    require(digest(recorded) == reference['sha256'], changed)
    return recorded


def stop(root, reason='fin_operador', trusted=None):
    path = directory(root)
    # STOP no espera a Git ni al lock global. Lee snapshots atómicos; no modifica el registro del harness.
    private.private_write(path / 'STOP', {'motivo': reason, 'fecha': time.time()})
    value = policy(root, expired=True)
    preparation = read(path / 'preparacion.json')
    require(preparation.get('politica_sha256') == digest(value), 'politica_alterada')
    rows, _, owned = inventory(root, value)
    has_journal = os.path.lexists(path / 'procesos.json')
    has_state = os.path.lexists(path / 'estado.json')
    require(has_journal == has_state, 'inventario_incompleto')
    if not has_journal:
        require(not any(read(p).get('evento') == 'muestra'
                        for p in path.glob('recibo-*.json')), 'inventario_perdido')
    journal = read(path / 'procesos.json') if has_journal else {}
    if has_journal:
        require(journal.get('politica_sha256') == digest(value), 'inventario_alterado')
        state = read(path / 'estado.json')
        require(state.get('procesos_sha256') == digest(journal), 'inventario_alterado')
        recorded = read_receipt(path, state.pop('recibo', None), changed='estado_alterado')
        require(recorded == dict(state, evento='muestra')
                and state.get('politica_sha256') == digest(value), 'estado_alterado')
    pending = pending_custodies(root, value, rows)
    items = (trusted or []) + journal.get('procesos', []) + process_tree(owned + pending)
    # A bootstrap without a receipt has not yet been able to start its model.
    # Let it observe STOP and record the empty drain instead of killing it early.
    starting = {(i['pid'], i['pid_inicio']) for i in pending
                if not os.path.lexists(custody_path(path, i))}
    unique = {(item['pid'], item['pid_inicio']): item for item in items
              if (item['pid'], item['pid_inicio']) not in starting}
    receipt(path, {'evento': 'intencion_SIGTERM', 'motivo': reason, 'fecha': time.time(),
                   'procesos': list(unique.values())})
    sent, skipped = terminate(list(unique.values()))
    receipt(path, {'evento': 'SIGTERM', 'motivo': reason, 'fecha': time.time(),
                   'enviados': sent, 'omitidos': skipped})
    deadline = time.monotonic() + 5
    while True:
        rows, _, pending_members = inventory(root, value)
        unverified = pending_custodies(root, value, rows)
        remaining = [i for i in unique.values() if sessions.process_start(i['pid']) == i['pid_inicio']]
        custody_alive = any(sessions.process_start(i['pid']) == i['pid_inicio'] for i in unverified)
        if not (remaining or pending_members or custody_alive) or time.monotonic() >= deadline:
            break
        time.sleep(0.1)
    result = {'estado': 'bloqueado' if remaining or pending_members or unverified else 'parado',
              'fecha': time.time(), 'custodias_sin_cierre': unverified,
              'pendientes': remaining, 'reservas_pendientes': len(pending_members),
              'politica_sha256': digest(value)}
    private.private_write(path / 'fin.json', result)
    return {'estado': result['estado'], 'SIGTERM': len(sent), 'pendientes': len(remaining),
            'reservas_pendientes': len(pending_members), 'custodias_sin_cierre': len(unverified)}


@contextmanager
def monitor_registry(root, expires):
    end = time.monotonic() + 5
    with ExitStack() as stack:
        while True:
            require(time.time() < expires and time.monotonic() < end, 'registro_ocupado_o_vencido')
            require(not os.path.lexists(Path(root) / DIRECTORY / 'STOP'), 'STOP')
            try:
                stack.enter_context(sessions.registry_lock(root, nonblocking=True))
                break
            except ValueError as exc:
                if not str(exc).startswith('Registro ocupado'):
                    raise
                time.sleep(0.05)
        yield


def monitor(root):
    path = directory(root)
    tracked = {}
    published = False
    with private.locked(path, nonblocking=True):
        value = policy(root)
        require(read(path / 'preparacion.json').get('politica_sha256') == digest(value), 'politica_alterada')
        require(not os.path.lexists(path / 'estado.json')
                and not os.path.lexists(path / 'procesos.json')
                and not any(read(p).get('evento') == 'muestra'
                            for p in path.glob('recibo-*.json')), 'monitor_ya_iniciado')
        try:
            while True:
                require(not os.path.lexists(path / 'STOP'), 'STOP')
                require(digest(policy(root)) == digest(value), 'politica_alterada')
                current_quota = read_quota(value['vence'], path / 'STOP')
                sample = read_resources()
                now = time.time()
                quota_budget(value['cuota_inicial'], current_quota, now)
                resources(sample, now)
                with monitor_registry(root, value['vence']):
                    require(not os.path.lexists(path / 'STOP'), 'STOP')
                    require(digest(policy(root)) == digest(value), 'politica_alterada')
                    if published:
                        health(root, value)
                    else:
                        require(not os.path.lexists(path / 'estado.json')
                                and not os.path.lexists(path / 'procesos.json'), 'monitor_ya_iniciado')
                    rows, questions, owned = inventory(root, value)
                    members(value, rows, questions)
                    require_verified_owners(root, value, rows)
                    tracked = {key: item for key, item in tracked.items()
                               if sessions.process_start(item['pid']) == item['pid_inicio']}
                    for item in process_tree(owned):
                        tracked[(item['pid'], item['pid_inicio'])] = item
                    journal = {'politica_sha256': digest(value), 'procesos': list(tracked.values())}
                    private.private_write(path / 'procesos.json', journal)
                    state = {'estado': 'listo', 'politica_sha256': digest(value), 'fecha': now,
                             'pid': os.getpid(), 'pid_inicio': sessions.process_start(os.getpid()),
                             'cuota': current_quota, 'recursos': sample, 'procesos_sha256': digest(journal)}
                    state['recibo'] = receipt(path, dict(state, evento='muestra'))
                    private.private_write(path / 'estado.json', state)
                    published = True
                # Espera corta para STOP y límite temporal, sin otro servicio.
                for _ in range(50):
                    if os.path.lexists(path / 'STOP') or time.time() >= value['vence']:
                        break
                    time.sleep(0.1)
        except (Exception, KeyboardInterrupt) as exc:
            reason = str(exc) if isinstance(exc, ValueError) and str(exc).startswith('ensayo_') else 'monitor_detenido'
            private.private_write(path / 'STOP', {'motivo': reason, 'fecha': time.time()})
            receipt(path, {'evento': 'bloqueo', 'motivo': reason, 'fecha': time.time()})
            return stop(root, reason, list(tracked.values()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operacion', type=Path, required=True)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('preparar')
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--id', action='append', required=True)
    p.add_argument('--segundos', type=int, default=MAX_DURATION)
    commands.add_parser('monitor')
    commands.add_parser('fin')
    commands.add_parser('estado')
    args = parser.parse_args()
    try:
        root = sessions.operation(args.operacion)
        if args.command == 'preparar':
            result = prepare(root, args.base.absolute(), args.id, args.segundos)
        elif args.command == 'monitor':
            # SIGTERM también pasa por STOP y la parada verificada.
            def interrupted(signum, frame):
                raise KeyboardInterrupt
            signal.signal(signal.SIGTERM, interrupted)
            result = monitor(root)
        elif args.command == 'fin':
            result = stop(root)
        else:
            value = policy(root)
            health(root, value)
            result = {'estado': 'listo', 'maximo': 4}
        print(json.dumps(result))
        return 2 if result['estado'] == 'bloqueado' else 0
    except (OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.SubprocessError):
        # Errores del operador/RPC pueden contener datos privados.
        print(json.dumps({'estado': 'bloqueado', 'error': 'control_del_ensayo_no_verificable'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
