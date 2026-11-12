"""Comprobación optativa de objetos Git fijados por la coordinadora.

El despachador y harness existentes conservan las transiciones y sus locks.
El único perfil implementado coteja bytes esperados de blobs regulares.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import select
import subprocess
import sys
import time
import uuid

SCRIPTS = Path(__file__).resolve().parents[3] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import harness_lote as lote
import harness_sesiones as sessions

require = lote.require
MAX_BLOB = 8 * 1024 * 1024
MAX_TOTAL = 32 * 1024 * 1024
MAX_DIFF = 1024 * 1024
MAX_TASKS = 32
ALLOWED_OPS = {'cerrar', 'revisar', 'recoger'}


def exact_keys(value, keys):
    require(isinstance(value, dict) and set(value) == set(keys.split()),
            'Campos fuera del perfil cerrado de comprobación.')


def full_commit(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', value),
            'Se requiere un commit completo literal.')


def route(value):
    require(isinstance(value, str) and 0 < len(value) <= 512
            and not any(ord(c) < 32 or ord(c) == 127 for c in value), 'Ruta inválida.')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value
            and not any(p in {'..', '.', ''} or p.lower() == '.git' for p in value.split('/'))
            and '\\' not in value, 'Ruta relativa literal requerida.')
    return value


def validate_profile(profile):
    exact_keys(profile, 'schema habilitado tipo autorizacion manifiesto_sha256 desde hasta tareas')
    require(type(profile['schema']) is int and profile['schema'] == 1, 'Esquema de perfil incompatible.')
    require(type(profile['habilitado']) is bool, 'Habilitación explícita requerida.')
    require(profile['tipo'] == 'git-artefactos-v1', 'Perfil requiere decisión humana o implementación revisada.')
    require(isinstance(profile['autorizacion'], str) and profile['autorizacion'].strip(), 'Falta autorización.')
    require(re.fullmatch(r'[0-9a-f]{64}', profile['manifiesto_sha256']), 'Hash de manifiesto inválido.')
    require(lote.timestamp(profile['desde']) < lote.timestamp(profile['hasta']), 'Vigencia de perfil inválida.')
    targets = profile['tareas']
    require(isinstance(targets, dict) and 0 < len(targets) <= MAX_TASKS, 'Cantidad de tareas fuera de límite.')
    for ident, target in targets.items():
        require(re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', ident), 'ID inválido.')
        exact_keys(target, 'commit commit_base artefactos')
        full_commit(target['commit'])
        full_commit(target['commit_base'])
        artifacts = target['artefactos']
        require(isinstance(artifacts, list) and 0 < len(artifacts) <= 64, 'Cantidad de artefactos fuera de límite.')
        paths = []
        for artifact in artifacts:
            exact_keys(artifact, 'ruta tamano sha256')
            paths.append(route(artifact['ruta']))
            require(type(artifact['tamano']) is int and 0 <= artifact['tamano'] <= MAX_BLOB,
                    'Tamaño de artefacto fuera de límite.')
            require(re.fullmatch(r'[0-9a-f]{64}', artifact['sha256']), 'Hash de artefacto inválido.')
        require(len(paths) == len(set(paths)), 'Artefactos duplicados.')
        require(sum(a['tamano'] for a in artifacts) <= MAX_TOTAL, 'Tamaño total fuera de límite.')
    return profile


def git_read(repo, *args, limit=MAX_DIFF):
    """Comandos fijos, salida y tiempo acotados, transporte y reemplazos bloqueados."""
    env = dict(PATH='/usr/bin:/bin', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0')
    command = ['/usr/bin/git', '--no-optional-locks', '--no-replace-objects', '--literal-pathspecs',
               '-C', str(repo), '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
               '-c', 'protocol.allow=never', '-c', 'credential.helper=', *args]
    with subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as process:
        deadline = time.monotonic() + 10
        output = bytearray()
        try:
            while True:
                remaining = deadline - time.monotonic()
                require(remaining > 0, 'Lectura Git excedió 10 s.')
                ready, _, _ = select.select([process.stdout], [], [], remaining)
                require(ready, 'Lectura Git excedió 10 s.')
                block = os.read(process.stdout.fileno(), min(65536, limit + 1 - len(output)))
                if not block:
                    break
                output.extend(block)
                require(len(output) <= limit, 'Salida Git excedió el límite.')
            require(process.wait(timeout=max(0.01, deadline - time.monotonic())) == 0,
                    'Objeto Git ausente, inelegible o lectura fallida.')
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    return bytes(output)


class EvidencePolicy:
    def __init__(self, path, approval, manifest, clock=None):
        self.path = Path(path)
        self.profile = validate_profile(lote.read_json(self.path))
        self.hash = lote.digest(self.profile)
        require(approval == self.hash, 'Falta SHA256 aprobado del perfil.')
        self.manifest = manifest
        self.clock = clock or (lambda: datetime.now(timezone.utc).timestamp())
        require(self.profile['manifiesto_sha256'] == lote.digest(manifest), 'Perfil de otro manifiesto.')
        require(set(self.profile['tareas']) == {t['id'] for t in manifest['tareas']},
                'Cada tarea del lote necesita su commit y perfil explícitos.')
        require(all(set(t['operaciones']) <= ALLOWED_OPS for t in manifest['tareas']),
                'Este adaptador admite cerrar, revisar y recoger.')

    def active(self):
        require(lote.digest(lote.read_json(self.path)) == self.hash, 'Perfil alterado durante la pasada.')
        require(self.profile['habilitado'], 'Perfil deshabilitado.')
        require(lote.timestamp(self.profile['desde']) <= self.clock() < lote.timestamp(self.profile['hasta']),
                'Perfil fuera de vigencia.')

    def target(self, task, row):
        self.active()
        assignment = row.get('asignacion') or {}
        require(assignment.get('responsable') == task['actor'] and assignment.get('rutas') == task['rutas']
                and (row.get('briefing') or {}).get('sha256') == task['briefing_sha256'],
                'Alcance canónico distinto del perfil aprobado.')
        return self.profile['tareas'][task['id']]

    def verify(self, task, row):
        target = self.target(task, row)
        require(row['estado'] in {'en_curso', 'en_espera'}, 'Estado inelegible para evidencia de cierre.')
        writers = [s for s in row.get('sesiones', []) if s['rol'] == 'ejecutor']
        require(writers, 'Falta ejecutor inscrito en el harness.')
        session = writers[-1]
        require(not session['dry_run'] and session.get('session_id') and not sessions.alive(session)
                and session['estado'] in {'finalizada', 'fallida', 'interrumpida'}
                and session['operacion'] == self.manifest['operacion'], 'Ejecutor inelegible o vivo.')
        require(session['commit_base'] == target['commit_base'], 'Commit base distinto del aprobado.')
        require(session['rama'] == 'codex/ws-' + task['id'], 'Rama distinta de la tarea.')
        repo = (sessions.validate_private_git(session, task['id']) if session.get('git_repo')
                else Path(self.manifest['repositorio']))
        commit = target['commit']
        head = git_read(repo, 'rev-parse', '--verify', 'refs/heads/' + session['rama'] + '^{commit}', limit=128)
        require(head.decode().strip() == commit, 'Commit no elegible en la rama asignada.')
        require(git_read(repo, 'cat-file', '-t', commit, limit=32) == b'commit\n', 'Objeto distinto de commit.')
        require(commit != target['commit_base'], 'Falta entrega nueva.')
        git_read(repo, 'merge-base', '--is-ancestor', target['commit_base'], commit, limit=0)
        prefix = Path(self.manifest['base']).relative_to(self.manifest['repositorio']).as_posix() + '/'
        artifacts = target['artefactos']
        expected = {prefix + a['ruta'] for a in artifacts}
        for artifact in artifacts:
            require(any(artifact['ruta'] == p or artifact['ruta'].startswith(p + '/') for p in task['rutas']),
                    'Artefacto fuera de rutas asignadas.')
        changed = git_read(repo, 'diff-tree', '--no-ext-diff', '--no-textconv', '--no-commit-id',
                           '--name-only', '--no-renames', '-r', '-z', target['commit_base'], commit)
        require(set(changed.decode('utf-8').rstrip('\0').split('\0')) == expected,
                'El diff completo debe coincidir con los artefactos esperados.')
        observed = []
        for artifact in artifacts:
            path = prefix + artifact['ruta']
            entry = git_read(repo, 'ls-tree', '-z', '--full-tree', commit, '--', path, limit=2048)
            metadata, name = entry.rstrip(b'\0').split(b'\t', 1)
            mode, kind, oid = metadata.decode('ascii').split()
            require(name.decode('utf-8') == path and mode == '100644' and kind == 'blob',
                    'Se requiere un blob regular 100644 en la ruta exacta.')
            size = int(git_read(repo, 'cat-file', '-s', oid, limit=32))
            require(size == artifact['tamano'], 'Tamaño de artefacto falso.')
            data = git_read(repo, 'cat-file', 'blob', oid, limit=size)
            require(len(data) == size and hashlib.sha256(data).hexdigest() == artifact['sha256'],
                    'Hash de artefacto falso.')
            observed.append(dict(artifact, objeto_git=oid))
        self.active()
        return dict(commit=commit, verificacion='correcta',
                    resultado='Artefactos Git cotejados mecánicamente en el commit fijado.',
                    comprobacion=f'git-artefactos-v1 perfil_sha256={self.hash} '
                                 f'artefactos_sha256={lote.digest(observed)} cantidad={len(observed)}')

    def gate(self, op, task, row, observation):
        target = self.target(task, row)
        require(op in ALLOWED_OPS, 'Operación fuera del adaptador.')
        if op == 'cerrar':
            require(observation.get('perfil_sha256') == self.hash
                    and observation.get('cierres', {}).get(task['id']) == self.verify(task, row),
                    'Declaración de cierre falsa o de otro perfil.')
        else:
            require((row.get('cierre') or {}).get('commit') == target['commit'],
                    'Revisión o recogida de otro commit.')


class VerifiedHarness(lote.LocalHarness):
    def invoke(self, op, task, row, observation):
        self.evidence.gate(op, task, row, observation)
        return super().invoke(op, task, row, observation)


class VerifiedDispatcher(lote.Dispatcher):
    def preflight(self, task, row, op, observation):
        self.adapter.evidence.gate(op, task, row, observation)
        return super().preflight(task, row, op, observation)


def observation(dispatcher):
    policy = dispatcher.adapter.evidence
    policy.active()
    result = dict(manifiesto_sha256=dispatcher.hash, perfil_sha256=policy.hash,
                  fecha=datetime.fromtimestamp(policy.clock(), timezone.utc).isoformat(), cierres={}, fallos=[])
    for task in dispatcher.manifest['tareas']:
        try:
            row = dispatcher.row(task)
            if row['estado'] in {'en_curso', 'en_espera'}:
                result['cierres'][task['id']] = policy.verify(task, row)
        except (ValueError, OSError, KeyError, UnicodeError) as exc:
            result['fallos'].append(dict(id=task['id'], causa=str(exc)))
    return result


def tick(dispatcher):
    """Una pasada del contrato aprobado, con evidencia privada conservada por intento."""
    dispatcher.permitted(effect=True)
    report = observation(dispatcher)
    folder = sessions.private_path(dispatcher.folder, 'evidencia-mecanica')
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = sessions.private_path(folder, uuid.uuid4().hex + '.json')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())
    directory = os.open(folder, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    result = dispatcher.tick(path, refresh_quota=True)
    return dict(result, evidencia=str(path), fallos_evidencia=report['fallos'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifiesto', type=Path)
    parser.add_argument('--aprobacion-sha256')
    parser.add_argument('--perfil', type=Path, required=True)
    parser.add_argument('--perfil-sha256')
    parser.add_argument('accion', choices=('hash-perfil', 'verificar', 'tick'))
    args = parser.parse_args(argv)
    try:
        if args.accion == 'hash-perfil':
            result = dict(perfil_sha256=lote.digest(validate_profile(lote.read_json(args.perfil))))
        else:
            require(args.manifiesto and args.aprobacion_sha256 and args.perfil_sha256,
                    'Se requieren manifiesto y ambos hashes aprobados.')
            manifest = lote.validate_manifest(lote.read_json(args.manifiesto))
            policy = EvidencePolicy(args.perfil, args.perfil_sha256, manifest)
            adapter = VerifiedHarness(manifest['base'], manifest['operacion'], manifest['repositorio'])
            adapter.evidence = policy
            dispatcher = VerifiedDispatcher(args.manifiesto, manifest['operacion'],
                                            args.aprobacion_sha256, adapter=adapter)
            dispatcher.permitted(effect=True)
            result = tick(dispatcher) if args.accion == 'tick' else observation(dispatcher)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        blocked = (result.get('fallos') or result.get('fallos_evidencia')
                   or any(event.get('bloqueo') for event in result.get('eventos', [])))
        return 2 if blocked else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps(dict(resultado='bloqueado', causa=str(exc)), ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
