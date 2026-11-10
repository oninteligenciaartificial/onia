"""Runtime Linux de harness.py. El registro de trabajo sigue siendo la autoridad.

El TSV es un índice recuperable de registros canónicos, no otra cola de tareas.
Los procesos sólo se inician mediante lanzar/reanudar/revisar con autorización.
"""
from contextlib import contextmanager
from copy import deepcopy
import csv
import fcntl
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import threading
import uuid

import trabajo

FIELDS = ('id', 'base', 'intento', 'rol', 'pid', 'pid_inicio', 'supervisor_pid',
          'supervisor_inicio', 'rama', 'session_id', 'estado', 'log', 'worktree', 'rutas', 'dry_run')
ACTIVE = {'iniciando', 'ejecutando', 'simulada'}


def private_path(root, name):
    return trabajo.safe_path(Path(root).absolute(), name)


def operation(root, dry_run=False):
    root = Path(root).expanduser().absolute()
    # No aceptar siquiera el directorio raíz mediante un symlink.
    if any(p.is_symlink() for p in (root, *root.parents)):
        raise ValueError('La carpeta de operación contiene un enlace.')
    return private_path(root, 'harness-dry-run') if dry_run else root


@contextmanager
def registry_lock(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = private_path(root, '.harness.lock')
    with path.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def git_environment():
    # No heredar redirecciones de índice/objetos/configuración de otro checkout.
    return {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}


def git(repo, *args):
    try:
        env = git_environment()
        prefix = ['git', '-C', str(repo), '-c', 'core.hooksPath=/dev/null',
                  '-c', 'core.fsmonitor=false', '-c', 'protocol.ext.allow=never',
                  '-c', 'submodule.recurse=false']
        # status/worktree pueden ejecutar filtros incluso sin hooks. Enumerar sólo
        # nombres (config no ejecuta filtros), neutralizarlos en este repositorio.
        filters = subprocess.run(prefix + ['config', '--name-only', '--get-regexp',
                                 r'^filter\..*\.(clean|smudge|process|required)$'],
                                 capture_output=True, text=True, timeout=120, env=env)
        if filters.returncode not in (0, 1):
            raise ValueError('No se pudo comprobar la configuración Git.')
        for driver in sorted({key.rsplit('.', 1)[0] for key in filters.stdout.splitlines()}):
            for option, value in [('clean', ''), ('smudge', ''), ('process', ''), ('required', 'false')]:
                prefix += ['-c', driver + '.' + option + '=' + value]
        # Conservar la identidad SSH del coordinador. Git de ejecutoras se consulta
        # sin transporte; el fetch de sus entregas usa el origin del coordinador.
        result = subprocess.run(prefix + list(args), capture_output=True,
                                text=True, encoding='utf-8', timeout=120, env=env)
    except subprocess.TimeoutExpired:
        raise ValueError('Git excedió 120 s en ' + args[0] + '; conservar estado y revisar acceso.') from None
    if result.returncode:
        # stderr de Git puede contener URLs autenticadas; nunca volcarlo al chat.
        raise ValueError('Git falló en ' + args[0] + '; código ' + str(result.returncode)
                         + '. Revisar acceso/estado local sin imprimir credenciales.')
    return result.stdout.strip()


def repo_for(base):
    return Path(git(base, 'rev-parse', '--show-toplevel')).resolve()


def process_start(pid):
    if not pid:
        return None
    try:
        fields = Path('/proc', str(pid), 'stat').read_text().rsplit(')', 1)[1].split()
        if fields[0] == 'Z':
            return None
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        return boot + ':' + fields[19]
    except FileNotFoundError:
        return None


def alive(session):
    # PID + arranque del proceso + boot id evitan confundir un PID reutilizado.
    return any(session.get(key) and session.get(start) and
               process_start(session[key]) == session[start]
               for key, start in (('pid', 'pid_inicio'), ('supervisor_pid', 'supervisor_inicio')))


def scan_log(path, offset=0):
    result = {'ultimo_evento': None, 'session_id': None, 'turn_failed': False}
    if not path.exists():
        return result
    with path.open('rb') as stream:
        stream.seek(offset)
        for line in stream:
            if not line.endswith(b'\n'):
                continue
            try:
                event = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if not isinstance(event, dict):
                continue
            result['ultimo_evento'] = event.get('type', 'desconocido')
            if event.get('type') == 'thread.started':
                sid = event.get('thread_id')
                try:
                    result['session_id'] = str(uuid.UUID(sid))
                except (ValueError, TypeError, AttributeError):
                    pass
            if event.get('type') == 'turn.failed':
                result['turn_failed'] = True
    return result


def save_index(root, rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDS, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    for base, row in rows:
        for session in row.get('sesiones', []):
            data = {key: session.get(key, '') for key in FIELDS}
            data.update(id=row['id'], base=str(base), rutas=json.dumps(session['rutas']),
                        dry_run=str(session['dry_run']).lower())
            writer.writerow(data)
    path = private_path(root, 'sesiones.tsv')
    temporary = private_path(root, 'sesiones.tsv.tmp')
    with temporary.open('w', encoding='utf-8') as stream:
        stream.write(output.getvalue())
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def indexed_rows(root, base):
    keys = {(str(base), ident) for ident in trabajo.all_ids(base)}
    index = private_path(root, 'sesiones.tsv')
    if index.exists():
        with index.open(encoding='utf-8') as stream:
            reader = csv.DictReader(stream, delimiter='\t')
            if reader.fieldnames != list(FIELDS):
                raise ValueError('Índice de sesiones incompatible; conservar y conciliar.')
            keys.update((r['base'], r['id']) for r in reader)
    rows = []
    for location, ident in sorted(keys):
        path = Path(location)
        row = trabajo.read_task(path, ident)  # Fallar cerrado si desaparece un registro.
        if any(s['operacion'] == str(root) for s in row.get('sesiones', [])):
            rows.append((path, row))
    return rows


def change(base, task_id, transform, expected_revision=None):
    row = trabajo.read_task(base, task_id)
    return trabajo.mutate(base, task_id, row['revision'] if expected_revision is None else expected_revision,
                          transform, review=True)


def sync(root, base, only_id=None):
    rows = indexed_rows(root, base)
    for location, row in rows:
        if only_id is not None and (location != Path(base) or row['id'] != only_id):
            continue
        sessions = deepcopy(row['sesiones'])
        for session in sessions:
            if session['operacion'] != str(root) or session['dry_run']:
                continue
            events = scan_log(private_path(root, session['log_rel']), session.get('log_offset', 0))
            if events['session_id']:
                session['session_id'] = events['session_id']
            session['ultimo_evento'] = events['ultimo_evento']
            if session['estado'] in ACTIVE and not alive(session):
                session['estado'] = 'interrumpida'
        if sessions != row['sesiones']:
            def update(current):
                current['sesiones'] = sessions
                if current['estado'] == 'en_curso' and sessions[-1]['estado'] == 'interrumpida':
                    current.update(estado='en_espera', proximo_paso='Revisar log y reanudar por session id.')
                return current
            change(location, row['id'], update)
    rows = indexed_rows(root, base)
    save_index(root, rows)
    return rows


def session_update(root, base, ident, attempt, **values):
    def update(row):
        session = next(s for s in row['sesiones'] if s['intento'] == attempt)
        session.update(values)
        if values.get('estado') in {'fallida', 'interrumpida'} and session['rol'] == 'ejecutor':
            row.update(estado='en_espera', proximo_paso='Revisar log y usar reanudar, conservando session id.')
        return row
    row = change(base, ident, update)
    save_index(root, indexed_rows(root, base))
    return row


def check_capacity(rows, task_id, base, routes, role):
    live = [(b, r, s) for b, r in rows for s in r['sesiones']
            if alive(s) or (s['dry_run'] and s['estado'] == 'simulada')]
    if len(live) >= 3:
        raise ValueError('Máximo 3 sesiones vivas; esperar antes de lanzar una cuarta.')
    for location, row, session in live:
        if row['id'] == task_id:
            raise ValueError('La tarea ya tiene una sesión viva (también se rechazan IDs duplicados entre bases).')
        if role == 'ejecutor' and session['rol'] == 'ejecutor':
            if any(trabajo.overlapping(a, b) for a in routes for b in session['rutas']):
                raise ValueError('Colisión de rutas con sesión viva de ' + row['id'] + '.')


def permission_args(session):
    """Perfil acotado; rutas literales TOML, nunca claves CLI separadas por puntos."""
    owner, directory = session['git_repo'], session['git_dir']
    paths = {owner: 'write', directory: 'write'}
    table = '{' + ', '.join(json.dumps(k) + ' = ' + json.dumps(v) for k, v in paths.items()) + '}'
    return ['-c', 'default_permissions="harness-git"',
            '-c', 'permissions.harness-git.extends=":workspace"',
            '-c', 'permissions.harness-git.network.enabled=true',
            '-c', 'permissions.harness-git.filesystem=' + table]


def validate_private_git(session, ident):
    owner = private_path(Path(session['operacion']), 'git/' + ident + '.git')
    worktree = Path(session['worktree'])
    if any(path.is_symlink() for path in (worktree, *worktree.parents)):
        raise ValueError('El worktree contiene un enlace; conservar y conciliar.')
    expected_dir = private_path(owner, 'worktrees/' + worktree.name)
    for relative in ('config', 'objects', 'refs', 'worktrees'):
        private_path(owner, relative)  # Validar antes de cargar configuración Git.
    if (session.get('git_repo') != str(owner) or session.get('git_dir') != str(expected_dir)
            or git(owner, 'rev-parse', '--is-bare-repository') != 'true'):
        raise ValueError('Metadatos Git privados inválidos; conservar y conciliar.')
    if (owner / 'objects/info/alternates').exists():
        raise ValueError('El Git privado no debe depender de objetos de otro repositorio.')
    if worktree.exists() and (git(worktree, 'rev-parse', '--absolute-git-dir') != str(expected_dir)
            or Path(git(worktree, 'rev-parse', '--path-format=absolute', '--git-common-dir')) != owner):
        raise ValueError('El worktree no pertenece a sus metadatos Git privados.')
    if worktree.exists():
        reject_submodules(worktree)
    return owner


def create_private_git(repo, root, ident, branch, worktree):
    owner = private_path(root, 'git/' + ident + '.git')
    if owner.exists() or worktree.exists() or worktree.is_symlink():
        raise ValueError('Git privado o worktree existente; conservar y conciliar, no sobrescribir.')
    owner.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    git(repo, 'init', '--bare', str(owner))
    git(owner, 'remote', 'add', 'origin', git(repo, 'remote', 'get-url', 'origin'))
    # Identidad técnica sólo en este repositorio; sin cambiar el usuario global.
    git(owner, 'config', 'user.name', 'OnIA Codex')
    git(owner, 'config', 'user.email', 'onia-codex-worker@localhost')
    git(owner, 'config', 'commit.gpgsign', 'false')
    git(owner, 'config', 'core.hooksPath', str(owner / 'hooks'))
    git(owner, 'fetch', 'origin', '+refs/heads/master:refs/remotes/origin/master')
    commit = git(owner, 'rev-parse', 'origin/master')
    git(owner, 'worktree', 'add', '-b', branch, str(worktree), commit)
    return owner, commit


def command(session, codex='codex'):
    review = session['rol'] == 'revisor'
    isolated = bool(session.get('git_repo')) and not review
    args = [codex, '-a', 'never']
    if isolated:
        args += permission_args(session) + ['exec', '--json', '--ignore-user-config', '-C', session['worktree']]
    else:
        # Compatibilidad: una retoma antigua conserva su sandbox y dueño Git.
        args += ['-c', 'sandbox_workspace_write.network_access=' + ('false' if review else 'true'),
                 'exec', '--json', '--sandbox', 'read-only' if review else 'workspace-write',
                 '-C', session['worktree']]
    if review:
        args += ['--ignore-user-config', '--output-schema', session['schema'],
                 '--output-last-message', session['veredicto_archivo']]
    if session.get('modelo'):
        args += ['--model', session['modelo']]
    if session.get('esfuerzo'):
        args += ['-c', 'model_reasoning_effort=' + json.dumps(session['esfuerzo'])]
    if session.get('auth_chatgpt'):
        args += ['-c', 'forced_login_method="chatgpt"', '-c', 'model_provider="openai"']
    # Overrides por intento: nunca heredar una delegación global implícita.
    limit = session.get('subagentes_maximos', 0) if not review else 0
    enabled = 'true' if limit else 'false'
    args += ['-c', 'agents.enabled=' + enabled,
             '-c', 'features.multi_agent=' + enabled,
             '-c', 'features.multi_agent_v2=false']
    if limit:
        args += ['-c', 'agents.max_concurrent_threads_per_session=' + str(limit),
                 '-c', 'agents.max_depth=1']
        if session.get('modelo'):
            args += ['-c', 'agents.default_subagent_model=' + json.dumps(session['modelo'])]
        if session.get('esfuerzo'):
            args += ['-c', 'agents.default_subagent_reasoning_effort=' + json.dumps(session['esfuerzo'])]
    if session.get('reanuda'):
        args += ['resume', session['reanuda']]
    return args + ['-']


def link_skills(repo, base, dry_run=False):
    import harness
    data = harness.manifest(base)
    links = []
    # Sólo directoras propias con SKILL.md: los apoyos externos no son instaladores.
    for name, source in data['skills'].items():
        if name.startswith('tercero-'):
            continue
        if not re.fullmatch(r'[a-z0-9-]+', name):
            raise ValueError('Nombre de skill inválido.')
        target = harness.safe_path(base, source)
        if target.name != 'SKILL.md' or not target.is_file():
            raise ValueError('Falta fuente canónica de skill: ' + name)
        directory = repo / '.agents' / 'skills'
        if any(p.is_symlink() for p in (repo / '.agents', directory)):
            raise ValueError('El directorio de skills contiene enlaces; conservar y revisar.')
        link = directory / name
        if os.path.lexists(link):
            if not link.is_symlink() or link.resolve() != target.parent.resolve():
                raise ValueError('Skill existente diferente; no se reemplazó: ' + name)
        elif not dry_run:
            directory.mkdir(parents=True, exist_ok=True)
            link.symlink_to(os.path.relpath(target.parent, directory), target_is_directory=True)
        links.append(name)
    return {'skills': links, 'dry_run': dry_run}


def launch(base, ident, root, revision, actor, approved=False, dry_run=False, resume=False,
           reviewer=None, model=None, effort=None, auth_chatgpt=False, subagents=None):
    base = Path(base).resolve()
    if model is not None and not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9._-]{0,99}', model):
        raise ValueError('Modelo inválido.')
    if effort is not None and effort not in trabajo.EFFORTS:
        raise ValueError('Esfuerzo inválido.')
    if subagents is not None and (type(subagents) is not int or subagents not in range(3)):
        raise ValueError('Subagentes máximos debe ser un entero de 0 a 2.')
    if reviewer and subagents not in (None, 0):
        raise ValueError('La revisión independiente no delega subagentes.')
    trabajo.task_path(base, ident)
    root = operation(root, dry_run)
    if not dry_run and not approved:
        raise ValueError('Falta el sí de Sergio: usar --si-sergio sólo con autorización aplicable al lanzamiento.')
    with registry_lock(root):
        # Comprobar la revisión ANTES de reconciliar metadatos asíncronos.
        row = trabajo.read_task(base, ident)
        trabajo.expected(row, revision)
        trabajo.verify(base, row)
        authorized_scope = (row.get('briefing'), row.get('asignacion'))
        rows = sync(root, base, only_id=ident)
        row = trabajo.read_task(base, ident)
        if authorized_scope != (row.get('briefing'), row.get('asignacion')):
            raise ValueError('Cambió el alcance durante la conciliación; renovar autorización.')
        if not row.get('briefing') or not row.get('asignacion'):
            raise ValueError('Lanzar requiere preparar y asignar responsable/rutas primero.')
        assignment = row['asignacion']
        if actor != assignment['responsable']:
            raise ValueError('Actor distinto del responsable asignado.')
        if any(s['dry_run'] != dry_run or s['operacion'] != str(root) for s in row.get('sesiones', [])):
            raise ValueError('No mezclar simulación, operación real ni carpetas de operación para un ID.')
        role = 'revisor' if reviewer else 'ejecutor'
        previous = next((s for s in reversed(row.get('sesiones', [])) if s['rol'] == 'ejecutor'), None)
        if resume and previous:
            model = model or previous.get('modelo')
            effort = effort or previous.get('esfuerzo')
            auth_chatgpt = auth_chatgpt or previous.get('auth_chatgpt', False)
            if subagents is None:
                subagents = previous.get('subagentes_maximos', 0)
        if subagents is None:
            subagents = 0
        if reviewer:
            reviewer = trabajo.nonempty(reviewer, 'revisor')
            if reviewer in {actor, *[s['responsable'] for s in row.get('sesiones', []) if s['rol'] == 'ejecutor']}:
                raise ValueError('El revisor debe ser distinto del ejecutor.')
            if row['estado'] != 'para_revision' or not row.get('cierre'):
                raise ValueError('Revisar requiere cierre publicado y estado para_revision.')
        else:
            trabajo.require_open(row)
            if previous and not resume:
                raise ValueError('Ya se lanzó esta tarea; usar reanudar, nunca empezar desde cero.')
            if resume and (not previous or not previous.get('session_id')):
                raise ValueError('Falta session id recuperable; conservar log, no relanzar desde cero.')
            if resume and (alive(previous) or previous['estado'] == 'simulada'):
                raise ValueError('La sesión sigue viva; no puede reanudarse simultáneamente.')
        check_capacity(rows, ident, base, assignment['rutas'], role)
        if not dry_run and not shutil.which('codex'):
            raise ValueError('Codex no está disponible en PATH; no se creó worktree.')
        repo = repo_for(base)
        for source in (repo / 'AGENTS.md', base / '04-operacion-agentes/reglas-comunes.md',
                       base / '04-operacion-agentes/boss-memoria.md'):
            if not source.is_file():
                raise ValueError('Falta contexto obligatorio: ' + source.name)
        attempt = len(row.get('sesiones', [])) + 1
        branch = 'codex/ws-' + ident
        worktree = repo.parent / ('onia-ws-' + ident + (f'-revision-{attempt}' if reviewer else ''))
        start_commit = 'simulado'
        git_owner = None
        log_rel = 'logs/' + ident + (f'.revision-{attempt}' if reviewer else '') + '.jsonl'
        if not resume and private_path(root, log_rel).exists():
            raise ValueError('Log existente sin retoma; se conserva y no se sobrescribe.')
        if not dry_run:
            if reviewer:
                git(repo, 'fetch', 'origin')
                start_commit = row['cierre']['commit']
                ensure_remote(repo, start_commit, previous['rama'])
                git(repo, 'worktree', 'add', '--detach', str(worktree), start_commit)
            elif resume:
                branch = previous['rama']
                worktree = Path(previous['worktree'])
                start_commit = previous['commit_base']
                git_owner = validate_private_git(previous, ident) if previous.get('git_repo') else None
                if not worktree.exists():
                    git(git_owner or repo, 'worktree', 'add', str(worktree), branch)
                if git(worktree, 'branch', '--show-current') != branch:
                    raise ValueError('El worktree ya no está en la rama de la sesión.')
            else:
                git_owner, start_commit = create_private_git(repo, root, ident, branch, worktree)
            link_skills(worktree, worktree / base.relative_to(repo))
        elif not reviewer:
            git_owner = Path(previous['git_repo']) if resume and previous.get('git_repo') else private_path(root, 'git/' + ident + '.git')
        logs = private_path(root, 'logs')
        logs.mkdir(parents=True, exist_ok=True, mode=0o700)
        log_rel = 'logs/' + ident + (f'.revision-{attempt}' if reviewer else '') + '.jsonl'
        log = private_path(root, log_rel)
        if not resume and log.exists():
            raise ValueError('Log existente sin retoma; se conserva y no se sobrescribe.')
        prompt_file = private_path(root, f'logs/{ident}.{attempt}.briefing.txt')
        session = dict(intento=attempt, rol=role, responsable=reviewer or actor, pid=None,
                       pid_inicio=None, supervisor_pid=None, supervisor_inicio=None,
                       rama=branch if not reviewer else '(detached)', session_id=None,
                       estado='simulada' if dry_run else 'iniciando', operacion=str(root),
                       log=str(log), log_rel=log_rel, log_offset=log.stat().st_size if log.exists() else 0,
                       worktree=str(worktree), rutas=assignment['rutas'], dry_run=dry_run,
                       commit_base=start_commit, reanuda=previous['session_id'] if resume else None,
                       briefing=str(prompt_file), inicio=trabajo.now(), rc=None, ultimo_evento=None,
                       modelo=model, esfuerzo=effort, auth_chatgpt=auth_chatgpt,
                       subagentes_maximos=subagents)
        if git_owner:
            session.update(git_repo=str(git_owner), git_dir=str(git_owner / 'worktrees' / worktree.name),
                           perfil_permisos='harness-git')
            if not dry_run:
                validate_private_git(session, ident)
        prompt = ('Una tarea por sesión. Leé AGENTS.md, reglas-comunes.md y boss-memoria.md.\n'
                  'El coordinador conserva el registro canónico: no modificar su JSON ni su briefing.\n'
                  'Base operativa dentro de este worktree: ' + str(base.relative_to(repo)) + '\n'
                  'El briefing se recibe por stdin; su archivo no tiene que existir en este worktree.\n'
                  'Los enlaces del briefing se resuelven desde base-operativa/' + row['briefing']['archivo'] + '.\n'
                  'Rutas asignadas (relativas a base-operativa): ' + json.dumps(assignment['rutas']) + '\n\n'
                  + row['briefing']['contenido'])
        if resume:
            prompt += ('\nCONTINUIDAD DEL REGISTRO ACTUAL:\n' + row['resultado'] + '\n'
                       + row['comprobacion'] + '\nPróximo paso: ' + row['proximo_paso'] + '\n')
            # actualizar conserva los recibos aunque limpie la revisión vigente.
            # verify ya comprobó sus bytes antes de leer el último veredicto.
            if row.get('evidencias_revision'):
                ref = row['evidencias_revision'][-1]
                feedback = trabajo.safe_path(base, ref['archivo']).read_text(encoding='utf-8')
                prompt += ('\nÚLTIMO VEREDICTO INDEPENDIENTE CONSERVADO (cotejar su commit):\n'
                           + feedback + '\nFuente: ' + ref['archivo'] + '\n'
                           'Resolver los cambios indicados que correspondan a la entrega; no ocultar límites.\n')
        if reviewer:
            session['entrega_sha256'] = trabajo.delivery_digest(row)
            session['schema'] = str(private_path(root, f'logs/{ident}.{attempt}.schema.json'))
            session['veredicto_archivo'] = str(private_path(root, f'logs/{ident}.{attempt}.veredicto.json'))
            schema = {'type': 'object', 'properties': {
                'veredicto': {'type': 'string', 'enum': ['bueno', 'cambios']},
                'commit': {'type': 'string'}, 'criterio': {'type': 'string'}},
                'required': ['veredicto', 'commit', 'criterio'], 'additionalProperties': False}
            Path(session['schema']).write_text(json.dumps(schema), encoding='utf-8')
            prompt += ('\n\nREVISIÓN INDEPENDIENTE DE SÓLO LECTURA. No editar ni aceptar la tarea.\n'
                       'Cotejá la entrega con cada criterio de aceptación y la evidencia.\n'
                       'Commit a revisar: ' + row['cierre']['commit'] + '\n'
                       'Comparar con commit base: ' + row['cierre']['commit_base'] + '\n'
                       'Resultado y comprobación declarados: ' + row['resultado'] + '\n' + row['comprobacion'] + '\n'
                       'Inventario de evidencia (no sustituye su lectura): ' + json.dumps(row['evidencias']) + '\n'
                       'Emití el veredicto JSON conforme al esquema; cambios si falta evidencia.\n')
            for ref in row['evidencias']:
                evidence_bytes = trabajo.safe_path(base, ref['archivo']).read_bytes()
                try:
                    content = evidence_bytes.decode('utf-8') if len(evidence_bytes) <= 65536 else None
                except UnicodeDecodeError:
                    content = None
                prompt += '\nEvidencia ' + ref['archivo'] + ':\n' + (content if content is not None
                    else 'Contenido no adjunto (binario o >64 KiB); cotejar en commit, o declarar faltante.') + '\n'
        else:
            prompt += ('\n\nAl finalizar: comprobá, commit y push origin ' + branch + '.\n'
                       'Hacé el commit y push vos desde tu sandbox; no pedir publicación al coordinador.\n'
                       'Usá push explícito sólo a la rama asignada, sin force; no cambiar otras ramas ni configuración global.\n'
                       'Informá hash y evidencia. El coordinador ejecutará cerrar y luego una revisión independiente.\n'
                       'No iniciar otras tareas, sesiones, servicios ni efectos externos fuera del encargo.\n'
                       'Subagentes nativos autorizados por este intento: ' + str(subagents) + ' hijos abiertos como máximo; sin nietos.\n'
                       'Cada hijo recibe un archivo exclusivo. Cerrarlo/liberarlo antes de reutilizar su cupo; el ejecutor publica una vez al terminar todos.\n')
        with prompt_file.open('x', encoding='utf-8') as stream:
            stream.write(prompt)
        if dry_run:
            session['session_id'] = str(uuid.uuid4())
            session['ultimo_evento'] = 'harness.dry_run'
            with log.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps({'type': 'harness.dry_run', 'simulado': True}) + '\n')
        def register(current):
            current.setdefault('sesiones', []).append(session)
            if not reviewer:
                current.update(estado='en_curso', aceptacion=None, revision_independiente=None,
                               cierre=None, proximo_paso='Comprobar estado, commit y push; luego cerrar.')
            return current
        row = change(base, ident, register, expected_revision=row['revision'])
        save_index(root, indexed_rows(root, base))
        if not dry_run:
            supervisor_log = private_path(root, f'logs/{ident}.{attempt}.supervisor.log')
            try:
                with supervisor_log.open('xb') as output:
                    worker = subprocess.Popen([sys.executable, str(Path(__file__).with_name('harness.py')),
                        '--base', str(base), '--operacion', str(root), '_ejecutar', ident,
                        '--intento', str(attempt)], stdin=subprocess.DEVNULL, stdout=output,
                        stderr=output, start_new_session=True, close_fds=True)
                # Recolectar al hijo si este intérprete sigue abierto (tests/API); en CLI
                # el supervisor queda desacoplado y es adoptado por el sistema.
                threading.Thread(target=worker.wait, daemon=True).start()
                row = session_update(root, base, ident, attempt, supervisor_pid=worker.pid,
                                     supervisor_inicio=process_start(worker.pid))
            except OSError:
                session_update(root, base, ident, attempt, estado='fallida', rc=-1)
                raise
        return {'tarea': trabajo.brief_view(row), 'comando': command(session),
                'dry_run': dry_run, 'nota': 'Simulación: no se invocó Codex ni se creó worktree.' if dry_run
                else 'Supervisor en segundo plano; consultar estado para PID e ID de Codex.'}


def child_environment(session):
    environment = git_environment()
    if session.get('auth_chatgpt'):
        for key in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL'):
            environment.pop(key, None)
    return environment


def worker(base, ident, root, attempt):
    root, base = Path(root), Path(base).resolve()
    with registry_lock(root):
        row = trabajo.read_task(base, ident)
        session = next(s for s in row['sesiones'] if s['intento'] == attempt)
        if session['dry_run'] or session['estado'] != 'iniciando' or session['supervisor_pid'] != os.getpid():
            raise ValueError('Supervisor no autorizado para este intento.')
        if session.get('git_repo'):
            validate_private_git(session, ident)
        codex = shutil.which('codex')
        if not codex:
            session_update(root, base, ident, attempt, estado='fallida', rc=127)
            return 127
        try:
            with Path(session['briefing']).open('rb') as prompt, Path(session['log']).open('ab') as output, \
                    private_path(root, f'logs/{ident}.{attempt}.stderr.log').open('xb') as errors:
                gate_read, gate_write = os.pipe()
                try:
                    # El hijo no ejecuta Codex hasta que su PID quede persistido. Si
                    # muere el supervisor antes, EOF cierra el hijo sin crear sesión.
                    bootstrap = ('import os,sys; fd=int(sys.argv[1]); '
                                 'ready=os.read(fd,1); os.close(fd); '
                                 'ready == b"1" or sys.exit(125); '
                                 'os.execvp(sys.argv[2],sys.argv[2:])')
                    child = subprocess.Popen([sys.executable, '-c', bootstrap, str(gate_read),
                        *command(session, codex)], stdin=prompt, stdout=output, stderr=errors,
                        cwd=session['worktree'], close_fds=True, pass_fds=(gate_read,),
                        env=child_environment(session))
                    with os.fdopen(gate_write, 'wb') as gate:
                        gate_write = None
                        session_update(root, base, ident, attempt, pid=child.pid,
                                       pid_inicio=process_start(child.pid), estado='ejecutando')
                        gate.write(b'1')
                finally:
                    os.close(gate_read)
                    if gate_write is not None:
                        os.close(gate_write)
        except OSError:
            session_update(root, base, ident, attempt, estado='fallida', rc=126)
            return 126
    last_sid = None
    while child.poll() is None:
        events = scan_log(Path(session['log']), session['log_offset'])
        if events['session_id'] and events['session_id'] != last_sid:
            last_sid = events['session_id']
            with registry_lock(root):
                session_update(root, base, ident, attempt, session_id=last_sid,
                               ultimo_evento=events['ultimo_evento'])
        time.sleep(0.25)
    events = scan_log(Path(session['log']), session['log_offset'])
    with registry_lock(root):
        session_update(root, base, ident, attempt, session_id=events['session_id'] or last_sid or session['reanuda'],
                       ultimo_evento=events['ultimo_evento'], rc=child.returncode, fin=trabajo.now(),
                       estado='finalizada' if child.returncode == 0 and not events['turn_failed'] else 'fallida')
    return child.returncode


def status(base, root, dry_run=False):
    root = operation(root, dry_run)
    with registry_lock(root):
        rows = sync(root, Path(base).resolve())
        return {'dry_run': dry_run, 'sesiones': [dict(id=row['id'], base=str(location),
                intento=s['intento'], rol=s['rol'], pid=s['pid'], pid_vivo=bool(s['pid'] and
                s['pid_inicio'] and process_start(s['pid']) == s['pid_inicio']),
                supervisor_vivo=bool(s['supervisor_pid'] and s['supervisor_inicio'] and
                process_start(s['supervisor_pid']) == s['supervisor_inicio']),
                viva_simulada=s['dry_run'] and s['estado'] == 'simulada', session_id=s['session_id'],
                rama=s['rama'], estado_sesion=s['estado'], estado_tarea=row['estado'],
                revision=row['revision'], ultimo_evento=s.get('ultimo_evento'), log=s['log'])
                for location, row in rows for s in row['sesiones']]}


def ensure_remote(repo, commit, branch):
    # Algunos clones sólo recuperan master. Actualizar explícitamente la rama de
    # esta tarea evita rechazar un push real o aceptar una referencia obsoleta.
    try:
        git(repo, 'fetch', 'origin', '+refs/heads/' + branch + ':refs/remotes/origin/' + branch)
    except ValueError as exc:
        raise ValueError('Commit no está en origin o no se pudo recuperar su rama; '
                         'tarea abierta, comprobar push y acceso.') from exc
    branches = git(repo, 'branch', '-r', '--contains', commit, '--format=%(refname:short)').splitlines()
    branches = [b for b in branches if b.startswith('origin/') and b != 'origin/HEAD']
    if 'origin/' + branch not in branches:
        raise ValueError('Commit no está en origin: tarea abierta; hacer push y volver a cerrar.')
    return branches


def write_evidence(base, row, name, content):
    folder = trabajo.PUBLIC_EVIDENCE if row['compartible'] else 'operacion/evidencias/'
    relative = folder + row['id'] + '/' + name
    path = trabajo.safe_path(base, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(content, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return trabajo.evidence(base, relative, row['compartible'])


def clean_worktree(repo, worktree):
    # Nunca --force. Git conserva la rama. Incluso archivos ignorados ajenos bloquean.
    reject_submodules(worktree)
    dirty = git(worktree, 'status', '--porcelain', '--untracked-files=all')
    if dirty:
        raise ValueError('Worktree con cambios; conservarlo, commit/push antes de cerrar.')
    import harness
    base = worktree / '_investigacion-onia/base-operativa'
    own_links = {'.agents/skills/' + name: harness.safe_path(base, source).parent
                 for name, source in harness.manifest(base)['skills'].items()
                 if not name.startswith('tercero-')}
    ignored = git(worktree, 'ls-files', '--others', '--ignored', '--exclude-standard').splitlines()
    for name in ignored:
        path = worktree / name
        if not (name in own_links and path.is_symlink() and path.resolve() == own_links[name]):
            raise ValueError('Worktree contiene archivos ignorados; preservarlos fuera antes de cerrar: ' + name)
    git(repo, 'worktree', 'remove', str(worktree))


def reject_submodules(worktree):
    # No inspeccionar configuraciones ejecutables de submódulos no revisados.
    for entries in (git(worktree, 'ls-tree', '-r', 'HEAD'), git(worktree, 'ls-files', '--stage')):
        if any(line.startswith('160000 ') for line in entries.splitlines()):
            raise ValueError('Submódulos fuera del piloto; conservar y conciliar.')


def validate_retained_worktree(worktree, commit):
    if not worktree.is_dir() or Path(git(worktree, 'rev-parse', '--show-toplevel')) != worktree:
        raise ValueError('Falta el worktree de la sesión; conciliar antes de conservarlo.')
    if git(worktree, 'rev-parse', 'HEAD') != commit:
        raise ValueError('HEAD del worktree no coincide con el commit de entrega.')
    reject_submodules(worktree)
    if git(worktree, '--no-optional-locks', 'status', '--porcelain', '--untracked-files=no',
           '--ignore-submodules=untracked'):
        raise ValueError('Worktree con cambios versionados; deben coincidir con el commit de entrega.')


def close(base, ident, root, revision, actor, result, check, dry_run=False, *, retain_worktree=False):
    base = Path(base).resolve()
    result = trabajo.nonempty(result, 'resultado')
    check = trabajo.nonempty(check, 'comprobación')
    root = operation(root, dry_run)
    with registry_lock(root):
        row = trabajo.read_task(base, ident)
        trabajo.expected(row, revision)
        trabajo.verify(base, row)
        authorized_scope = (row.get('briefing'), row.get('asignacion'))
        sync(root, base, only_id=ident)
        row = trabajo.read_task(base, ident)
        if authorized_scope != (row.get('briefing'), row.get('asignacion')):
            raise ValueError('Cambió el alcance durante la conciliación; renovar autorización.')
        if row['asignacion']['responsable'] != actor:
            raise ValueError('Actor distinto del ejecutor.')
        session = next((s for s in reversed(row.get('sesiones', [])) if s['rol'] == 'ejecutor'), None)
        if not session or session['dry_run'] != dry_run or session['operacion'] != str(root):
            raise ValueError('No hay una sesión de este modo para cerrar.')
        if alive(session):
            raise ValueError('La sesión sigue viva; esperar antes de cerrar.')
        if row['estado'] in {'aceptado', 'para_revision'}:
            raise ValueError('La tarea ya fue cerrada; reabrir explícitamente para otra entrega.')
        if not dry_run and not session.get('session_id'):
            raise ValueError('Falta session id del ejecutor; recuperar eventos antes de cerrar.')
        repo = repo_for(base)
        if dry_run:
            commit, branches = 'simulado', ['origin/simulado']
        else:
            git(repo, 'fetch', 'origin')
            git_owner = validate_private_git(session, ident) if session.get('git_repo') else repo
            commit = git(git_owner, 'rev-parse', session['rama'] + '^{commit}')
            if commit == session['commit_base']:
                raise ValueError('No hay commit de entrega nuevo; tarea abierta.')
            git(git_owner, 'merge-base', '--is-ancestor', session['commit_base'], commit)
            branches = ensure_remote(repo, commit, session['rama'])
            worktree = Path(session['worktree'])
            if retain_worktree:
                validate_retained_worktree(worktree, commit)
            elif worktree.exists():
                if git(worktree, 'rev-parse', 'HEAD') != commit:
                    raise ValueError('HEAD del worktree no coincide con la rama asignada.')
                clean_worktree(git_owner, worktree)
        receipt = dict(commit=commit, commit_base=session['commit_base'], ramas_origin=branches,
                       fecha=trabajo.now(), dry_run=dry_run, intento=session['intento'])
        if retain_worktree and not dry_run:
            receipt['worktree_conservado'] = True
        ref = write_evidence(base, row, f'cierre-r{row["revision"]}-{uuid.uuid4().hex[:8]}.json', receipt)
        def finish(current):
            current['cierre'] = dict(receipt, evidencia=ref)
            current['evidencias'].append(ref)
            current.update(estado='para_revision', resultado=trabajo.nonempty(result, 'resultado'),
                           comprobacion=trabajo.nonempty(check, 'comprobación'), verificacion='correcta',
                           revision_independiente=None, aceptacion=None, proximo_paso='Lanzar revisor distinto; recoger veredicto antes de aceptar.')
            current['sesiones'][session['intento'] - 1]['estado'] = 'cerrada'
            return current
        row = change(base, ident, finish, expected_revision=row['revision'])
        save_index(root, indexed_rows(root, base))
        return {'tarea': trabajo.brief_view(row), 'dry_run': dry_run,
                'nota': 'Simulación sin prueba remota; aceptar está prohibido.' if dry_run
                else 'Commit comprobado en origin; rama conservada, revisión pendiente. Integrar a master antes de dar el trabajo por terminado.'}


def collect_review(base, ident, root, revision, *, retain_worktree=False):
    base = Path(base).resolve()
    root = operation(root)
    with registry_lock(root):
        row = trabajo.read_task(base, ident)
        trabajo.expected(row, revision)
        trabajo.verify(base, row)
        authorized_scope = (row.get('briefing'), row.get('asignacion'))
        sync(root, base, only_id=ident)
        row = trabajo.read_task(base, ident)
        if authorized_scope != (row.get('briefing'), row.get('asignacion')):
            raise ValueError('Cambió el alcance durante la conciliación; renovar autorización.')
        session = row['sesiones'][-1]
        executors = {s['session_id'] for s in row['sesiones'] if s['rol'] == 'ejecutor'}
        if (None in executors or session['rol'] != 'revisor' or session['dry_run'] or alive(session)
                or session['operacion'] != str(root)
                or session['rc'] != 0 or session['estado'] != 'finalizada'
                or not session['session_id'] or session['session_id'] in executors):
            raise ValueError('Falta revisión finalizada, exitosa y con session id distinto del ejecutor.')
        if session['entrega_sha256'] != trabajo.delivery_digest(row):
            raise ValueError('Revisión obsoleta: cambió la entrega.')
        verdict = json.loads(Path(session['veredicto_archivo']).read_text(encoding='utf-8'))
        if (not isinstance(verdict, dict) or verdict.get('veredicto') not in {'bueno', 'cambios'}
                or verdict.get('commit') != row['cierre']['commit']):
            raise ValueError('Veredicto inválido o referido a otro commit.')
        trabajo.nonempty(verdict.get('criterio'), 'criterio del veredicto')
        existing = row.get('revision_independiente')
        if existing and existing['session_id'] == session['session_id']:
            return {'tarea': trabajo.brief_view(row), 'nota': 'Veredicto ya recogido e íntegro.'}
        worktree = Path(session['worktree'])
        verdict = {key: verdict[key] for key in ('veredicto', 'commit', 'criterio')}
        if retain_worktree:
            validate_retained_worktree(worktree, verdict['commit'])
            verdict['worktree_conservado'] = True
        elif worktree.exists():
            clean_worktree(repo_for(base), worktree)
        ref = write_evidence(base, row, f'revision-{session["intento"]}-{uuid.uuid4().hex[:8]}.json', verdict)
        def finish(current):
            current.setdefault('evidencias_revision', []).append(ref)
            current['revision_independiente'] = dict(verdict, revisor=session['responsable'],
                session_id=session['session_id'], entrega_sha256=session['entrega_sha256'], evidencia=ref)
            # La evidencia de revisión se verifica aparte para no cambiar el digest de la entrega.
            return current
        row = change(base, ident, finish, expected_revision=row['revision'])
        save_index(root, indexed_rows(root, base))
        return {'tarea': trabajo.brief_view(row), 'nota': 'Veredicto guardado; aceptar requiere bueno.'}
