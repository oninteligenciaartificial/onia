"""Pasadas finitas de lotes aprobados sobre trabajo y harness_sesiones.

El journal conserva intenciones y efectos. Los estados se leen del registro
canónico. La coordinadora conserva aceptación, integración y despliegue.
"""
import argparse
from contextlib import contextmanager, suppress
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import select
import signal
import subprocess
import time
import uuid

import harness_sesiones as sessions
import trabajo

OPS = {'lanzar', 'reanudar', 'cerrar', 'revisar', 'recoger', 'aceptar', 'integrar', 'desplegar'}
DISPATCH = {'lanzar', 'reanudar', 'revisar'}
OBSERVATION_MAX_AGE = 120


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def timestamp(value):
    require(isinstance(value, str), 'Fecha ISO8601 requerida.')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'Fecha sin zona horaria.')
    return result.timestamp()


def read_json(path):
    # Evitar redirecciones de políticas/observaciones mediante enlaces.
    path = Path(path).absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'Ruta con enlace.')
    return json.loads(path.read_text(encoding='utf-8'))


def codex_quota(result, now):
    """Conservar sólo ventanas de cuota incluida, sin créditos ni datos de cuenta."""
    by_id = result.get('rateLimitsByLimitId')
    require(by_id is None or isinstance(by_id, dict), 'Ventanas de Codex inválidas.')
    limits = by_id.get('codex') if by_id is not None else result.get('rateLimits')
    require(isinstance(limits, dict) and limits.get('limitId') == 'codex',
            'Ventanas de Codex no identificadas.')
    remaining = []
    resets = []
    for name in ('primary', 'secondary'):
        window = limits.get(name)
        if name == 'secondary' and window is None:
            continue
        require(isinstance(window, dict), 'Ventana de cuota ausente.')
        used, reset = window.get('usedPercent'), window.get('resetsAt')
        require(type(used) in (int, float) and 0 <= used <= 100
                and type(reset) is int and reset > now, 'Ventana de cuota inválida o vencida.')
        remaining.append(100 - used)
        resets.append(reset)
    return {
        'fecha': datetime.fromtimestamp(now, timezone.utc).isoformat(),
        'fuente': 'account/rateLimits/read',
        'proveedor': 'openai-chatgpt-incluido',
        'disponible': limits.get('rateLimitReachedType') is None,
        'saldo_extra_autorizado': False,
        'restante_porcentaje': min(remaining),
        'reinicio_mas_proximo': min(resets),
    }


def read_codex_quota():
    """Consultar app-server por stdio con plazo total y sin iniciar turnos."""
    command = ['codex', 'app-server', '--listen', 'stdio://',
               '-c', 'forced_login_method="chatgpt"', '-c', 'model_provider="openai"']
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, start_new_session=True,
                          env=sessions.child_environment({'auth_chatgpt': True})) as process:
        end = time.monotonic() + 20
        buffer = b''
        output_bytes = 0

        def send(message):
            process.stdin.write((json.dumps(message) + '\n').encode())
            process.stdin.flush()

        def receive(ident):
            nonlocal buffer, output_bytes
            while time.monotonic() < end:
                if b'\n' not in buffer:
                    readable, _, _ = select.select([process.stdout], [], [], max(0, end - time.monotonic()))
                    require(bool(readable), 'Consulta de cuota vencida.')
                    chunk = os.read(process.stdout.fileno(), 65536)
                    output_bytes += len(chunk)
                    require(chunk and output_bytes <= 262144, 'Respuesta de cuota interrumpida o excesiva.')
                    buffer += chunk
                    continue
                line, buffer = buffer.split(b'\n', 1)
                message = json.loads(line)
                require(isinstance(message, dict), 'Respuesta de cuota inválida.')
                if message.get('id') == ident:
                    require('error' not in message and isinstance(message.get('result'), dict),
                            'App-server rechazó la consulta de cuota.')
                    return message['result']
            raise ValueError('Consulta de cuota vencida.')

        try:
            send({'id': 1, 'method': 'initialize',
                  'params': {'clientInfo': {'name': 'onia_lote', 'version': '1.0'}}})
            receive(1)
            send({'method': 'initialized'})
            send({'id': 2, 'method': 'account/rateLimits/read',
                  'params': {'excludeResetCreditDetails': True}})
            return codex_quota(receive(2), time.time())
        finally:
            # El lanzador CLI y su binario comparten el grupo privado de esta consulta.
            # Señalar antes de recolectar el PID impide confundir otro grupo posterior.
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                with suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait()


def profile(value):
    require(isinstance(value, dict) and value.get('modelo') == 'gpt-6.1-sol'
            and value.get('esfuerzo') in {'low', 'high'}, 'Perfil fuera del alcance Sol low/high.')


def validate_manifest(manifest):
    require(isinstance(manifest, dict) and type(manifest.get('schema')) is int
            and manifest['schema'] == 1, 'Esquema de lote incompatible.')
    require(re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', manifest.get('id', '')), 'ID de lote inválido.')
    require(type(manifest.get('habilitado')) is bool, 'Falta habilitado explícito.')
    trabajo.nonempty(manifest.get('autorizacion'), 'referencia de autorización')
    require(timestamp(manifest['desde']) < timestamp(manifest['hasta']), 'Vigencia inválida.')
    for key in ('base', 'repositorio', 'operacion'):
        path = Path(manifest[key])
        require(path.is_absolute() and str(path) == str(path.resolve()), 'Ruta absoluta canónica requerida.')
        sessions.operation(path)
    require(manifest['proveedor'] == 'openai-chatgpt-incluido', 'Proveedor fuera del alcance.')
    minimum = manifest['cuota_minima_porcentaje']
    require(type(minimum) in (int, float) and 0 < minimum <= 100, 'Cuota mínima inválida.')
    tasks = manifest['tareas']
    require(isinstance(tasks, list) and tasks, 'Lote con IDs requerido.')
    ids = [task['id'] for task in tasks]
    require(len(ids) == len(set(ids)), 'IDs duplicados en lote.')
    for task in tasks:
        require(re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', task['id']), 'ID de tarea inválido.')
        for key in ('actor', 'revisor', 'criterio'):
            trabajo.nonempty(task[key], key)
        require(task['actor'] != task['revisor'], 'Revisor igual al ejecutor.')
        limit = task.get('subagentes_maximos', 0)
        require(type(limit) is int and limit in (0, 1, 2),
                'Subagentes máximos debe ser un entero de 0 a 2.')
        require(re.fullmatch(r'[0-9a-f]{64}', task['briefing_sha256']), 'Hash de briefing inválido.')
        require(isinstance(task['rutas'], list) and task['rutas'], 'Faltan rutas.')
        for route in task['rutas']:
            require(trabajo.normalize_route(Path(manifest['base']), route) == route, 'Ruta ambigua.')
        operations = task['operaciones']
        require(isinstance(operations, list) and operations and set(operations) <= OPS,
                'Operaciones fuera del contrato.')
        for role in ('ejecutor', 'revisor'):
            profile(task['perfiles'][role])
            count = task['intentos_maximos'][role]
            require(type(count) is int and count >= 1, 'Presupuesto de intentos inválido.')
        require(type(task.get('prioridad', 0)) is int, 'Prioridad inválida.')
        dependencies = task['depende_de']
        require(isinstance(dependencies, list), 'Dependencias inválidas.')
        require(len({dep['id'] for dep in dependencies}) == len(dependencies), 'Dependencias duplicadas.')
        for dep in dependencies:
            require(dep['id'] in ids and dep['id'] != task['id'], 'Dependencia inexistente o propia.')
            require(re.fullmatch(r'[0-9a-f]{40,64}', dep['commit']), 'Commit de dependencia inválido.')
    pending = {task['id']: {d['id'] for d in task['depende_de']} for task in tasks}
    while pending:
        ready = {ident for ident, deps in pending.items() if not deps}
        require(ready, 'Ciclo de dependencias.')
        pending = {ident: deps - ready for ident, deps in pending.items() if ident not in ready}
    return manifest


def current_review(row):
    verdict = row.get('revision_independiente') or {}
    writers = [s for s in row.get('sesiones', []) if s['rol'] == 'ejecutor']
    return bool(verdict.get('veredicto') == 'bueno'
                and verdict.get('commit') == (row.get('cierre') or {}).get('commit')
                and verdict.get('entrega_sha256') == trabajo.delivery_digest(row)
                and verdict.get('session_id')
                and verdict['session_id'] not in {s.get('session_id') for s in writers}
                and verdict.get('revisor') not in {s['responsable'] for s in writers}
                and not any(s['dry_run'] for s in row.get('sesiones', [])))


def fingerprint(row):
    """Evidencia estable del efecto, independiente de revisiones asíncronas de PID."""
    return {
        'sesiones': [{key: s.get(key, 0) if key == 'subagentes_maximos' else s.get(key) for key in
                      ('intento', 'rol', 'session_id', 'reanuda', 'commit_base', 'entrega_sha256',
                       'modelo', 'esfuerzo', 'auth_chatgpt', 'responsable', 'operacion', 'dry_run', 'subagentes_maximos')}
                     for s in row.get('sesiones', [])],
        'commit': (row.get('cierre') or {}).get('commit'),
        'revision_sid': (row.get('revision_independiente') or {}).get('session_id'),
    }


def progress(row):
    # Crear otro intento o incrementar revisión no acredita progreso del producto.
    return digest(dict(commit=(row.get('cierre') or {}).get('commit'),
                       evidencias=row.get('evidencias', []),
                       revision=row.get('revision_independiente')))


class LocalHarness:
    def __init__(self, base, operation, repo):
        self.base, self.operation, self.repo = Path(base), Path(operation), Path(repo)
        require(sessions.repo_for(self.base) == self.repo, 'Repositorio ajeno a la base.')
        require(Path(sessions.__file__).resolve().parent == self.base / '05-herramientas/scripts',
                'API importada desde otro checkout.')
        require(self.operation == Path.home() / 'operacion', 'Usar la operación global del usuario coordinador.')

    def row(self, ident):
        row = trabajo.read_task(self.base, ident)
        trabajo.verify(self.base, row)
        return row

    def reconcile(self, ids):
        with sessions.registry_lock(self.operation):
            for ident in ids:
                sessions.sync(self.operation, self.base, only_id=ident)

    def reservations(self):
        # También cuentan asignaciones sin proceso vivo, hasta liberación explícita.
        return [self.row(ident) for ident in trabajo.all_ids(self.base)]

    def capacity(self, task, role):
        with sessions.registry_lock(self.operation):
            sessions.check_capacity(sessions.indexed_rows(self.operation, self.base), task['id'],
                                    self.base, task['rutas'], role, root=self.operation)

    def integrated(self, commit, refresh=False):
        try:
            if refresh:
                sessions.git(self.repo, 'fetch', 'origin',
                             '+refs/heads/master:refs/remotes/origin/master')
            sessions.git(self.repo, 'merge-base', '--is-ancestor', commit, 'origin/master')
            return True
        except ValueError:
            return False

    def provider(self):
        try:
            result = subprocess.run(['codex', 'login', 'status'], capture_output=True,
                                    text=True, timeout=15, env=sessions.child_environment({'auth_chatgpt': True}))
        except (OSError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0 and 'Logged in using ChatGPT' in result.stdout + result.stderr

    def quota(self):
        require(self.provider(), 'Autenticación ChatGPT no comprobada.')
        return read_codex_quota()

    def invoke(self, op, task, row, observation):
        ident, revision, actor = task['id'], row['revision'], task['actor']
        if op in DISPATCH:
            role = 'revisor' if op == 'revisar' else 'ejecutor'
            selected = task['perfiles'][role]
            return sessions.launch(self.base, ident, self.operation, revision, actor,
                                   approved=True, resume=op == 'reanudar',
                                   reviewer=task['revisor'] if op == 'revisar' else None,
                                   model=selected['modelo'], effort=selected['esfuerzo'],
                                   auth_chatgpt=True,
                                   subagents=0 if role == 'revisor' else task.get('subagentes_maximos', 0))
        if op == 'recoger':
            return sessions.collect_review(self.base, ident, self.operation, revision, retain_worktree=True)
        attestation = observation['cierres'][ident]

        def validate_commit(current, session, commit):
            require(commit == attestation['commit'], 'La comprobación corresponde a otro commit.')
            changed = sessions.git(self.repo, 'diff', '--name-only', '--no-renames',
                                   session['commit_base'], commit).splitlines()
            prefix = self.base.relative_to(self.repo).as_posix() + '/'
            require(changed and all(path.startswith(prefix) and
                    any((path[len(prefix):] == route or path[len(prefix):].startswith(route + '/'))
                        for route in task['rutas']) for path in changed), 'Diff fuera de rutas asignadas.')

        return sessions.close(self.base, ident, self.operation, revision, actor,
                              attestation['resultado'], attestation['comprobacion'],
                              retain_worktree=True, commit_validator=validate_commit)


@contextmanager
def batch_lock(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = sessions.private_path(root, '.lotes.lock')
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Otra pasada de lote está activa.') from None
        yield
    finally:
        os.close(fd)


class Dispatcher:
    def __init__(self, manifest_path, operation, approval=None, adapter=None, clock=None):
        self.path = Path(manifest_path).absolute()
        self.manifest = validate_manifest(read_json(self.path))
        self.hash = digest(self.manifest)
        self.approval = approval
        self.root = sessions.operation(operation)
        require(str(self.root) == self.manifest['operacion'], 'Carpeta de operación distinta del manifiesto.')
        self.folder = sessions.private_path(self.root, 'lotes/' + self.manifest['id'])
        self.journal = sessions.private_path(self.folder, 'journal.jsonl')
        self.stop = sessions.private_path(self.folder, 'STOP.json')
        self.adapter = adapter or LocalHarness(self.manifest['base'], self.root, self.manifest['repositorio'])
        self.clock = clock or (lambda: datetime.now(timezone.utc).timestamp())

    def events(self):
        if not self.journal.exists():
            return []
        raw = self.journal.read_bytes()
        require(raw.endswith(b'\n'), 'Journal truncado. Conservar bytes y conciliar con coordinadora.')
        events = [json.loads(line) for line in raw.splitlines()]
        previous = None
        for event in events:
            require(event['anterior'] == previous, 'Cadena del journal alterada.')
            previous = digest(event)
        return events

    def append(self, kind, **values):
        events = self.events()
        event = dict(tipo=kind, fecha=datetime.fromtimestamp(self.clock(), timezone.utc).isoformat(),
                     anterior=digest(events[-1]) if events else None, manifiesto_sha256=self.hash, **values)
        self.folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(self.journal, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600)
        try:
            data = (json.dumps(event, ensure_ascii=False, allow_nan=False) + '\n').encode()
            while data:
                data = data[os.write(fd, data):]
            os.fsync(fd)
        finally:
            os.close(fd)
        self.fsync_folder()
        return event

    def fsync_folder(self):
        fd = os.open(self.folder, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def permitted(self, effect=False):
        require(digest(read_json(self.path)) == self.hash, 'Manifiesto cambió durante la pasada.')
        require(not self.stop.exists(), 'Lote revocado o STOP. Evidencia conservada.')
        if effect:
            require(self.approval == self.hash, 'Falta SHA256 aprobado del manifiesto.')
            require(self.manifest['habilitado'], 'Configuración deshabilitada.')
            require(timestamp(self.manifest['desde']) <= self.clock() < timestamp(self.manifest['hasta']),
                    'Lote fuera de vigencia.')

    def row(self, task):
        row = self.adapter.row(task['id'])
        require(row.get('schema') == 2, 'Registro histórico. Requiere migración manual.')
        assignment = row.get('asignacion') or {}
        if not assignment and row['estado'] == 'aceptado':
            assignment = next((entry['asignacion'] for entry in reversed(row.get('historial', []))
                               if entry.get('asignacion')), {})
        require(assignment.get('responsable') == task['actor'] and assignment.get('rutas') == task['rutas']
                and (row.get('briefing') or {}).get('sha256') == task['briefing_sha256'],
                'Alcance canónico distinto del aprobado.')
        require(all(s['operacion'] == str(self.root) and not s['dry_run']
                    for s in row.get('sesiones', [])), 'Sesiones de otro modo u operación.')
        return row

    def dependencies(self, task, refresh):
        by_id = {t['id']: t for t in self.manifest['tareas']}
        for dep in task['depende_de']:
            row = self.row(by_id[dep['id']])
            require(row['estado'] == 'aceptado' and current_review(row)
                    and (row.get('cierre') or {}).get('commit') == dep['commit']
                    and (row.get('aceptacion') or {}).get('revisor') == by_id[dep['id']]['revisor'],
                    'Dependencia sin aceptación vigente del commit esperado.')
            require(self.adapter.integrated(dep['commit'], refresh=refresh), 'Dependencia pendiente en origin/master.')

    def candidate(self, task, row, observation=None):
        history = row.get('sesiones', [])
        if any(sessions.alive(s) for s in history):
            return None
        if row['estado'] == 'aceptado':
            require(current_review(row) and row['revision_independiente'].get('revisor') == task['revisor'],
                    'Aceptación con revisión obsoleta o de otro revisor.')
            return None
        if row['estado'] == 'para_revision':
            require(row.get('cierre'), 'Falta cierre.')
            review = row.get('revision_independiente')
            if review:
                require(review.get('entrega_sha256') == trabajo.delivery_digest(row)
                        and review.get('commit') == row['cierre']['commit']
                        and review.get('revisor') == task['revisor'], 'Revisión obsoleta o de otro revisor.')
                return None
            reviewers = [s for s in history if s['rol'] == 'revisor'
                         and s.get('entrega_sha256') == trabajo.delivery_digest(row)]
            if reviewers:
                last = reviewers[-1]
                if last['estado'] == 'finalizada' and last.get('rc') == 0:
                    return 'recoger'
                require(last['estado'] in {'fallida', 'interrumpida', 'finalizada'}
                        and task.get('reintentar_revision_intento') == last['intento'],
                        'Revisor sin finalización correcta. Conciliar el mismo intento.')
                return 'revisar'
            return 'revisar'
        writers = [s for s in history if s['rol'] == 'ejecutor']
        if not writers:
            require(row['estado'] == 'preparado', 'Tarea sin ejecutor fuera de preparado.')
            return 'lanzar'
        last = writers[-1]
        if row['estado'] == 'en_curso' and last['estado'] == 'finalizada' and last.get('rc') == 0:
            return 'cerrar'
        receipt = (observation or {}).get('cierres', {}).get(task['id'], {})
        if (row['estado'] in {'en_espera', 'en_curso'}
                and last['estado'] in {'fallida', 'interrumpida', 'finalizada'}
                and receipt.get('verificacion') == 'correcta'
                and re.fullmatch(r'[0-9a-f]{40,64}', receipt.get('commit', ''))):
            # El cierre vuelve a comprobar commit remoto, alcance y ausencia de procesos.
            return 'cerrar'
        require(row['estado'] in {'en_espera', 'en_curso'} and last.get('session_id')
                and task.get('reanudar_sid') == last['session_id'], 'Retoma requiere SID autorizado y conciliación.')
        return 'reanudar'

    def observation(self, path, *, ignore_stale=False):
        if path is None:
            return {}
        obs = read_json(path)
        require(isinstance(obs, dict) and obs.get('manifiesto_sha256') == self.hash,
                'Observación de otro manifiesto.')
        age = self.clock() - timestamp(obs['fecha'])
        if ignore_stale and age > OBSERVATION_MAX_AGE:
            return {}
        require(0 <= age <= OBSERVATION_MAX_AGE, 'Observación ausente, futura o caducada.')
        return obs

    def check_quota_freshness(self, quota):
        require(0 <= self.clock() - timestamp(quota['fecha']) <= OBSERVATION_MAX_AGE
                and self.clock() < quota['reinicio_mas_proximo'], 'Cuota de Codex caducada.')

    def preflight(self, task, row, op, observation):
        self.dependencies(task, refresh=True)
        if op == 'recoger':
            require(row['sesiones'][-1]['responsable'] == task['revisor'], 'Revisión de otro responsable.')
        if op == 'cerrar':
            receipt = observation.get('cierres', {}).get(task['id'], {})
            require(receipt.get('verificacion') == 'correcta'
                    and re.fullmatch(r'[0-9a-f]{40,64}', receipt.get('commit', '')),
                    'Falta comprobación explícita de la coordinadora para cerrar.')
            for key in ('resultado', 'comprobacion'):
                trabajo.nonempty(receipt.get(key), key)
        if op in DISPATCH:
            require(observation.get('proveedor') == self.manifest['proveedor']
                    and observation.get('disponible') is True and observation.get('saldo_extra_autorizado') is False,
                    'Proveedor/cuota incluida sin comprobar.')
            available = observation.get('restante_porcentaje')
            require(type(available) in (int, float)
                    and self.manifest['cuota_minima_porcentaje'] <= available <= 100, 'Cuota insuficiente o desconocida.')
            require(self.adapter.provider(), 'Autenticación ChatGPT no comprobada.')
            if op == 'reanudar':
                checkpoint = observation.get('retomas', {}).get(task['id'], {})
                require(checkpoint.get('sid') == task['reanudar_sid']
                        and checkpoint.get('revision') == row['revision']
                        and checkpoint.get('auxiliares_terminados') is True,
                        'Falta conciliación de procesos auxiliares para el mismo SID.')
            if op == 'revisar' and task.get('reintentar_revision_intento'):
                checkpoint = observation.get('revisiones', {}).get(task['id'], {})
                require(checkpoint.get('intento') == task['reintentar_revision_intento']
                        and checkpoint.get('revision') == row['revision']
                        and checkpoint.get('auxiliares_terminados') is True,
                        'Falta conciliación de la revisión fallida.')
            role = 'revisor' if op == 'revisar' else 'ejecutor'
            require(sum(s['rol'] == role for s in row.get('sesiones', [])) < task['intentos_maximos'][role],
                    'Presupuesto de intentos agotado.')
            self.adapter.capacity(task, role)
            if role == 'ejecutor':
                for other in self.adapter.reservations():
                    if other['id'] == row['id']:
                        continue
                    require(not any(trabajo.overlapping(a, b) for a in task['rutas']
                                    for b in (other.get('asignacion') or {}).get('rutas', [])),
                            'Conflicto con reserva de ' + other['id'] + '.')
        return observation

    def recover(self, rows):
        events = self.events()
        completed = {e['clave'] for e in events if e['tipo'] in {'efecto', 'sin_efecto'}}
        unresolved = {}
        for intent in (e for e in events if e['tipo'] == 'intencion' and e['clave'] not in completed):
            ident, op = intent['id'], intent['op']
            if ident not in rows:
                unresolved[ident] = intent['clave']
                continue
            row = rows[ident]
            before, after = intent['antes'], fingerprint(row)
            recognized = False
            if op in DISPATCH:
                role = 'revisor' if op == 'revisar' else 'ejecutor'
                old_attempts = {s['intento'] for s in before['sesiones']}
                added = [s for s in after['sesiones'] if s['intento'] not in old_attempts]
                expected = intent['perfil']
                limit = intent.get('subagentes_maximos', 0)
                if len(added) == 1:
                    session = added[0]
                    recognized = (session['rol'] == role and session['session_id']
                                  and session['modelo'] == expected['modelo']
                                  and session['esfuerzo'] == expected['esfuerzo']
                                  and session['responsable'] == intent['responsable']
                                  and session['operacion'] == str(self.root) and not session['dry_run']
                                  and session['auth_chatgpt'] is True
                                  and type(limit) is int and limit in (0, 1, 2)
                                  and type(session['subagentes_maximos']) is int
                                  and session['subagentes_maximos'] == limit
                                  and (role != 'revisor' or limit == 0)
                                  and (op != 'reanudar' or session['session_id'] == intent['sid'])
                                  and (role != 'revisor' or session['entrega_sha256'] == intent['entrega']))
            elif op == 'cerrar':
                recognized = after['commit'] == intent['commit'] and row['estado'] in {'para_revision', 'aceptado'}
            elif op == 'recoger':
                review = row.get('revision_independiente') or {}
                recognized = (after['revision_sid'] == intent['sid'] and review.get('commit') == intent['commit']
                              and review.get('entrega_sha256') == trabajo.delivery_digest(row))
            if recognized:
                self.append('efecto', clave=intent['clave'], id=ident, op=op,
                            recuperado=True, despues=after, revision=row['revision'])
            else:
                unresolved[ident] = intent['clave']
        return unresolved

    def stalled(self, ident, row):
        failures = [e for e in self.events() if e['tipo'] in {'fallo', 'fallo_sesion'} and e['id'] == ident]
        return (len(failures) >= 2 and failures[-1]['progreso'] == failures[-2]['progreso']
                == progress(row))

    def observe_failures(self, rows):
        events = self.events()
        recorded = {(e['id'], e['intento']) for e in events if e['tipo'] == 'fallo_sesion'}
        failed_dispatches = {e['clave'] for e in events if e['tipo'] == 'fallo'}
        observed_dispatches = {e['clave'] for e in events if e['tipo'] == 'efecto'}
        # Una excepción de lanzamiento y el fin fallido del mismo intento
        # pertenecen al mismo fallo, incluso si el supervisor alcanzó a arrancar.
        recorded.update((e['id'], len(e['antes']['sesiones']) + 1) for e in events
                        if e['tipo'] == 'intencion' and e['op'] in DISPATCH
                        and e['clave'] in failed_dispatches & observed_dispatches)
        for ident, row in rows.items():
            history = row.get('sesiones', [])
            if not history:
                continue
            last = history[-1]
            failed = (last['estado'] in {'fallida', 'interrumpida'}
                      or (last['estado'] == 'finalizada' and last.get('rc') not in (None, 0)))
            if failed and not sessions.alive(last) and (ident, last['intento']) not in recorded:
                self.append('fallo_sesion', id=ident, intento=last['intento'],
                            sid=last.get('session_id'), rol=last['rol'], progreso=progress(row))

    def plan(self):
        """Sólo lectura, sin sync, locks, red, cuota ni creación de archivos."""
        result = []
        events = self.events()
        completed = {e['clave'] for e in events if e['tipo'] in {'efecto', 'sin_efecto'}}
        unresolved = {e['id'] for e in events if e['tipo'] == 'intencion' and e['clave'] not in completed}
        for task in self.manifest['tareas']:
            try:
                row = self.row(task)
                require(task['id'] not in unresolved, 'Intención pendiente de conciliación SID/commit.')
                self.dependencies(task, refresh=False)
                op = self.candidate(task, row)
                require(op not in DISPATCH or not self.stalled(task['id'], row),
                        'Dos fallos sin progreso. Diagnóstico requerido.')
                manual = []
                if row['estado'] in {'para_revision', 'aceptado'} and current_review(row):
                    manual = [dict(op=action, autorizada=action in task['operaciones'])
                              for action in ('aceptar', 'integrar', 'desplegar')]
                elif (row.get('revision_independiente') or {}).get('veredicto') == 'cambios':
                    manual = [dict(op='reabrir_y_conciliar_mismo_sid', autorizada='reanudar' in task['operaciones'])]
                result.append(dict(id=task['id'], revision=row['revision'], op=op,
                                   commit=(row.get('cierre') or {}).get('commit'),
                                   revisor=task['revisor'], criterio=task['criterio'], acciones_coordinadora=manual))
            except (ValueError, OSError, KeyError) as exc:
                result.append(dict(id=task['id'], bloqueo=str(exc)))
        return dict(manifiesto_sha256=self.hash, habilitado=self.manifest['habilitado'],
                    revocado=self.stop.exists(), tareas=result)

    def tick(self, observation_path=None, *, refresh_quota=False):
        require(observation_path is not None or refresh_quota, 'Faltan observaciones o --cuota-codex.')

        def read_observation():
            return self.observation(observation_path, ignore_stale=refresh_quota)

        with batch_lock(self.root):
            self.permitted(effect=True)
            self.adapter.reconcile([t['id'] for t in self.manifest['tareas']])
            rows, report = {}, []
            for task in self.manifest['tareas']:
                try:
                    rows[task['id']] = self.row(task)
                except (ValueError, OSError) as exc:
                    report.append(dict(id=task['id'], bloqueo=str(exc)))
            # No retirar IDs con intenciones históricas para eludir un bloqueo.
            historical = {e['id'] for e in self.events() if 'id' in e}
            require(historical <= {t['id'] for t in self.manifest['tareas']}, 'El lote retiró tareas con historial.')
            unresolved = self.recover(rows)
            self.observe_failures(rows)
            candidates = []
            for task in self.manifest['tareas']:
                ident = task['id']
                if ident not in rows:
                    continue
                try:
                    require(ident not in unresolved, 'Intención incierta ' + unresolved.get(ident, '') + '. Conciliar SID/commit.')
                    op = self.candidate(task, rows[ident], read_observation())
                    require(op not in DISPATCH or not self.stalled(ident, rows[ident]),
                            'Dos fallos sin progreso. Diagnóstico de coordinadora requerido.')
                    if op:
                        candidates.append((op, task, rows[ident]))
                except ValueError as exc:
                    report.append(dict(id=ident, bloqueo=str(exc)))
            # Recoger/cerrar libera transiciones. Las revisiones preceden a nuevos productores.
            ranks = {'recoger': 0, 'cerrar': 1, 'revisar': 2, 'reanudar': 3, 'lanzar': 3}
            candidates.sort(key=lambda item: (ranks[item[0]], -item[1].get('prioridad', 0), item[1]['id']))
            quota = None
            quota_error = None
            for op, task, row in candidates:
                ident = task['id']
                try:
                    self.permitted(effect=True)
                    require(op in task['operaciones'], 'Operación sin autorización en manifiesto.')
                    raw_observation = read_observation()
                    observation = raw_observation
                    live_quota = refresh_quota and op in DISPATCH
                    if live_quota:
                        if quota is None and quota_error is None:
                            try:
                                quota = self.adapter.quota()
                            except (ValueError, OSError, KeyError, TypeError, AttributeError):
                                quota_error = 'No se pudo comprobar la cuota incluida de Codex.'
                        require(quota_error is None, quota_error)
                        observation = {**raw_observation, **quota}
                    self.preflight(task, row, op, observation)
                    # Releer después de I/O externo. La API vuelve a cotejar la revisión bajo su lock.
                    current = self.row(task)
                    trabajo.expected(current, row['revision'])
                    self.permitted(effect=True)
                    require(read_observation() == raw_observation, 'Observación cambió durante comprobaciones.')
                    if live_quota:
                        self.check_quota_freshness(quota)
                except (ValueError, OSError, KeyError) as exc:
                    report.append(dict(id=ident, op=op, bloqueo=str(exc)))
                    continue
                role = 'revisor' if op == 'revisar' else 'ejecutor'
                history = row.get('sesiones', [])
                intent = self.append('intencion', clave=uuid.uuid4().hex, id=ident, op=op,
                                     antes=fingerprint(row), revision=row['revision'],
                                     perfil=task['perfiles'][role], responsable=task['revisor'] if role == 'revisor' else task['actor'],
                                     subagentes_maximos=0 if role == 'revisor' else task.get('subagentes_maximos', 0),
                                     entrega=trabajo.delivery_digest(row),
                                     sid=(task['reanudar_sid'] if op == 'reanudar' else history[-1].get('session_id') if history else None),
                                     commit=(observation.get('cierres', {}).get(ident, {}).get('commit') if op == 'cerrar'
                                             else (row.get('cierre') or {}).get('commit')),
                                     cuota={k: observation.get(k) for k in
                                            ('fecha', 'proveedor', 'restante_porcentaje', 'fuente', 'reinicio_mas_proximo')},
                                     modelo_observado=None)
                try:
                    self.permitted(effect=True)
                    require(read_observation() == raw_observation, 'Observación cambió antes del efecto.')
                    if live_quota:
                        self.check_quota_freshness(quota)
                    self.adapter.invoke(op, task, row, observation)
                    after = self.row(task)
                    self.recover({**rows, ident: after})
                    report.append(dict(id=ident, op=op, clave=intent['clave'], revision=after['revision']))
                    # Un efecto como máximo por pasada. El SID puede llegar después.
                    return dict(resultado='avanzado', eventos=report, plan=self.plan())
                except (ValueError, OSError) as exc:
                    self.append('fallo', clave=intent['clave'], id=ident, op=op,
                                progreso=progress(row), causa=type(exc).__name__)
                    report.append(dict(id=ident, op=op, bloqueo='Efecto incierto. Conciliar journal y registro.'))
                    # Otras tareas independientes pueden avanzar en esta misma pasada.
            return dict(resultado='sin_avance', eventos=report, plan=self.plan())

    def revoke(self, reason):
        trabajo.nonempty(reason, 'motivo de STOP')
        self.folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            fd = os.open(self.stop, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return {'resultado': 'ya_revocado'}
        with os.fdopen(fd, 'w') as stream:
            json.dump(dict(motivo=reason, fecha=trabajo.now(), manifiesto_sha256=self.hash), stream)
            stream.flush()
            os.fsync(stream.fileno())
        self.fsync_folder()
        return {'resultado': 'revocado'}

    def resolve_no_effect(self, key, revision, evidence_path):
        """Declaración de la coordinadora tras inspeccionar procesos y artefactos."""
        with batch_lock(self.root):
            events = self.events()
            intent = next((e for e in events if e['tipo'] == 'intencion' and e['clave'] == key), None)
            require(intent is not None, 'Intención desconocida.')
            require(not any(e['tipo'] in {'efecto', 'sin_efecto'} and e['clave'] == key for e in events), 'Intención ya resuelta.')
            row = self.adapter.row(intent['id'])
            trabajo.expected(row, revision)
            require(fingerprint(row) == intent['antes'] and not any(sessions.alive(s) for s in row.get('sesiones', [])),
                    'Cambió la evidencia o hay sesión viva. Conciliar por SID/commit.')
            evidence = Path(evidence_path).absolute()
            statement = read_json(evidence)
            require(statement.get('clave') == key and statement.get('revision') == revision
                    and statement.get('sin_efecto_comprobado') is True,
                    'Falta declaración exacta de ausencia de efecto.')
            trabajo.nonempty(statement.get('comprobacion'), 'comprobación de procesos/logs/worktrees')
            self.append('sin_efecto', clave=key, id=intent['id'], revision=revision,
                        evidencia_sha256=hashlib.sha256(evidence.read_bytes()).hexdigest(),
                        evidencia=str(evidence))
            return {'resultado': 'conciliado_sin_efecto'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifiesto', type=Path, required=True)
    parser.add_argument('--operacion', type=Path, default=Path.home() / 'operacion')
    parser.add_argument('--aprobacion-sha256')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('hash')
    sub.add_parser('plan')
    tick = sub.add_parser('tick')
    tick.add_argument('--observaciones', type=Path)
    tick.add_argument('--cuota-codex', action='store_true', help='Consultar cuota incluida por app-server.')
    stop = sub.add_parser('revocar')
    stop.add_argument('--motivo', required=True)
    resolve = sub.add_parser('conciliar-sin-efecto')
    resolve.add_argument('--clave', required=True)
    resolve.add_argument('--revision-esperada', type=int, required=True)
    resolve.add_argument('--evidencia', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'hash':
            result = {'sha256': digest(validate_manifest(read_json(args.manifiesto)))}
        else:
            dispatcher = Dispatcher(args.manifiesto, args.operacion, args.aprobacion_sha256)
            if args.command == 'plan':
                result = dispatcher.plan()
            elif args.command == 'tick':
                result = dispatcher.tick(args.observaciones, refresh_quota=args.cuota_codex)
            elif args.command == 'revocar':
                result = dispatcher.revoke(args.motivo)
            else:
                result = dispatcher.resolve_no_effect(args.clave, args.revision_esperada, args.evidencia)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        # Las excepciones de transporte de la API ya vienen saneadas.
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
