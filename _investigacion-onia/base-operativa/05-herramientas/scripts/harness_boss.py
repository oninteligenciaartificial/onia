"""SSH de Boss: protocolo JSON acotado sobre el harness; sin shell ni scheduler."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
if __name__ == '__main__':
    # Los módulos auxiliares y serve deben compartir la clase Rejected.
    sys.modules['harness_boss'] = sys.modules[__name__]
import trabajo
import harness_sesiones as sessions

PROTOCOL = 'onia-harness-v1'
SAFE = re.compile(r'[a-z0-9][a-z0-9-]{0,79}\Z')
READ = {'consultar', 'entrega'}
WRITE = {'ejecutar', 'reanudar', 'cerrar', 'revisar', 'recoger', 'notificar'}


class Rejected(ValueError):
    """Only these deliberately static messages may cross SSH."""


def checked_id(value):
    if not isinstance(value, str) or not SAFE.fullmatch(value):
        raise Rejected('identificador_invalido')
    return value


def no_links(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise Rejected('enlace_no_permitido')
    return path


def private_read(path):
    path = no_links(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise Rejected('permisos_privados_invalidos')
        data = stream.read(262145)
    if len(data) > 262144:
        raise Rejected('archivo_excesivo')
    return json.loads(data)


def private_write(path, value):
    path = no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.parent.stat().st_mode & 0o077:
        raise Rejected('directorio_no_privado')
    temporary = path.parent / ('.' + path.name + '.' + uuid.uuid4().hex)
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    # Persist directory entries too: a reboot must not forget an intent already acted on.
    for parent in (path.parent, path.parent.parent):
        fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


@contextmanager
def locked(root):
    root = no_links(root)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.stat().st_uid != os.getuid() or root.stat().st_mode & 0o077:
        raise Rejected('directorio_no_privado')
    fd = os.open(root / '.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    with os.fdopen(fd, 'a') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise Rejected('lock_invalido')
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def request(value):
    if not isinstance(value, dict) or value.get('version') != 1 or type(value['version']) is not int:
        raise Rejected('protocolo_invalido')
    op = value.get('operacion')
    if op in {'registrar', 'habilitar'}:
        import harness_delegacion
        checked_id(value.get('id'))
        return harness_delegacion.parse(value)
    if op not in READ | WRITE:
        raise Rejected('operacion_no_permitida')
    keys = {'version', 'operacion', 'id'}
    checked_id(value.get('id'))
    if op in WRITE:
        keys |= {'solicitud', 'revision_esperada'}
        checked_id(value.get('solicitud'))
        if type(value.get('revision_esperada')) is not int or value['revision_esperada'] < 1:
            raise Rejected('revision_invalida')
    if set(value) != keys:
        raise Rejected('campos_no_permitidos')
    return value


def snapshot(base, ident):
    row = trabajo.read_task(base, ident)
    trabajo.verify(base, row)
    if not row.get('compartible'):
        raise Rejected('tarea_no_compartible')
    latest = row.get('sesiones', [])[-1:]
    session = latest[0] if latest else {}
    # No results, prompts, free-form log events, filesystem paths or credentials.
    result = {key: row[key] for key in ('id', 'revision', 'estado')}
    result.update(briefing_sha256=(row.get('briefing') or {}).get('sha256'),
                  intento=session.get('intento'), viva=sessions.alive(session),
                  commit=(row.get('cierre') or {}).get('commit'))
    for key in ('modelo', 'esfuerzo', 'session_id', 'estado'):
        val = session.get(key)
        if isinstance(val, str) and re.fullmatch(r'[A-Za-z0-9._-]{1,100}', val):
            result[('solicitado_' if key in {'modelo', 'esfuerzo'} else 'sesion_') + key] = val
    if result['commit'] and not re.fullmatch(r'[0-9a-f]{40,64}', result['commit']):
        result['commit'] = None
    return row, result


def binding(row):
    return digest({'briefing': row.get('briefing'), 'asignacion': row.get('asignacion')})


def authorize(root, value, row, now=None):
    grant = private_read(root / 'permisos' / (value['id'] + '.json'))
    now = now or datetime.now(timezone.utc)
    until = datetime.fromisoformat(grant['vence'])
    if until.tzinfo is None or until <= now or grant.get('revocado') is not False:
        raise Rejected('permiso_vencido_o_revocado')
    if grant.get('id') != value['id'] or not grant.get('autorizacion_sergio'):
        raise Rejected('permiso_invalido')
    actions = grant.get('operaciones')
    if not isinstance(actions, list) or any(x not in WRITE for x in actions):
        raise Rejected('operaciones_invalidas')
    if grant.get('binding') != binding(row) or value['operacion'] not in actions:
        raise Rejected('fuera_del_permiso')
    if grant.get('modelo') != 'gpt-6.1-sol' or grant.get('esfuerzo') not in {'low', 'high'}:
        raise Rejected('modelo_no_autorizado')
    if type(grant.get('max_intentos')) is not int or not 1 <= grant['max_intentos'] <= 6:
        raise Rejected('limite_invalido')
    if grant.get('actor') != (row.get('asignacion') or {}).get('responsable') or not grant.get('actor'):
        raise Rejected('actor_no_autorizado')
    if value['operacion'] == 'revisar' and (not isinstance(grant.get('revisor'), str)
            or not grant['revisor'].strip() or grant['revisor'] == grant['actor']):
        raise Rejected('revisor_distinto_requerido')
    return grant


def invoke(config, value, row, grant):
    base, op = Path(config['base']), Path(config['operacion'])
    ident, revision, action = value['id'], value['revision_esperada'], value['operacion']
    actor = grant['actor']
    if action in {'ejecutar', 'reanudar', 'revisar'}:
        if len(row.get('sesiones', [])) >= grant['max_intentos']:
            raise Rejected('limite_intentos')
        sessions.launch(base, ident, op, revision, actor, approved=True,
                        resume=action == 'reanudar',
                        reviewer=grant.get('revisor') if action == 'revisar' else None,
                        model=grant['modelo'], effort=grant['esfuerzo'], auth_chatgpt=True, subagents=0)
    elif action == 'cerrar':
        import harness_delegacion
        result = sessions.close(base, ident, op, revision, actor, grant['resultado_cierre'],
                                grant['comprobacion_cierre'], retain_worktree=True,
                                commit_validator=lambda current, session, commit:
                                    harness_delegacion.check_product_scope(config, current, grant, session, commit))
        revision = result['tarea']['revision']
    elif action == 'recoger':
        result = sessions.collect_review(base, ident, op, revision, retain_worktree=True)
        revision = result['tarea']['revision']
        import harness_retorno
        return harness_retorno.publish_review(config, ident, revision)
    if action in {'cerrar', 'notificar'}:
        import harness_retorno
        return harness_retorno.deliver(config, ident, expected_revision=revision, expected_binding=binding(row))
    return None


def handle(config, value, config_path=None):
    value = request(value)
    if value['operacion'] in {'registrar', 'habilitar'}:
        import harness_delegacion
        return harness_delegacion.handle(config, value, config_path)
    ident, action = value['id'], value['operacion']
    ids = config.get('lectura_ids')
    if not isinstance(ids, list) or any(not isinstance(x, str) or not SAFE.fullmatch(x) for x in ids):
        raise Rejected('configuracion_ids_invalida')
    if ident not in ids:
        raise Rejected('id_no_habilitado')
    base, root = no_links(config['base']), no_links(config['privado'])
    if action in READ:
        return {'ok': True, 'tarea': snapshot(base, ident)[1]}
    # Serializes bridge calls, not the long-running Codex sessions.
    with locked(root):
        if config_path is not None:
            current = private_read(config_path)
            if any(current.get(k) != config.get(k) for k in ('base', 'operacion', 'privado')):
                raise Rejected('configuracion_cambio_reintentar')
            if not isinstance(current.get('lectura_ids'), list) or ident not in current['lectura_ids']:
                raise Rejected('id_no_habilitado')
            config = current
        row, _ = snapshot(base, ident)
        grant = authorize(root, value, row)
        if config.get('pausado') is not False:
            raise Rejected('puente_pausado')
        path = root / 'solicitudes' / (value['solicitud'] + '.json')
        if path.exists():
            prior = private_read(path)
            if prior['hash'] != digest(value):
                raise Rejected('solicitud_reutilizada')
            if prior['fase'] != 'terminada':
                raise Rejected('conciliacion_necesaria_no_repetir')
            return dict(prior['respuesta'], repetida=True)
        barrier = root / 'barreras' / (ident + '.json')
        previous = private_read(barrier) if barrier.exists() else {}
        if previous.get('fase') in {'iniciada', 'requiere_conciliacion'}:
            raise Rejected('conciliacion_necesaria_no_repetir')
        count = previous.get('contador', 0)
        if count >= 24:
            raise Rejected('limite_solicitudes_coordinador')
        trabajo.expected(row, value['revision_esperada'])
        if action in {'ejecutar', 'reanudar', 'revisar'}:
            import harness_delegacion
            harness_delegacion.check_launch(config, grant)
        record = {'hash': digest(value), 'id': ident, 'fase': 'iniciada',
                  'intentos_previos': len(row.get('sesiones', [])), 'operacion': action}
        barrier_record = {'solicitud': value['solicitud'], 'fase': 'iniciada', 'contador': count + 1}
        private_write(barrier, barrier_record)
        private_write(path, record)  # Durable BEFORE the potentially side-effectful launch.
        try:
            delivery = invoke(config, value, row, grant)
            response = {'ok': True, 'tarea': snapshot(base, ident)[1]}
            if delivery is not None:
                response['retorno'] = delivery
        except Exception:
            # A crashed/failed call may have launched or closed successfully. Never auto-retry it.
            record['fase'] = 'requiere_conciliacion'
            private_write(path, record)
            private_write(barrier, dict(barrier_record, fase='requiere_conciliacion'))
            raise Rejected('conciliacion_necesaria_no_repetir') from None
        private_write(path, dict(record, fase='terminada', respuesta=response))
        private_write(barrier, dict(barrier_record, fase='terminada'))
        return response


def serve(config_path):
    try:
        if os.environ.get('SSH_ORIGINAL_COMMAND') != PROTOCOL:
            raise Rejected('comando_ssh_no_permitido')
        # The forced entrypoint supplies the path; callers cannot supply flags or shell text.
        config = private_read(config_path)
        raw = sys.stdin.buffer.readline(16385)
        if len(raw) > 16384 or not raw.endswith(b'\n'):
            raise Rejected('peticion_excesiva_o_sin_fin')
        result = handle(config, json.loads(raw), config_path=config_path)
        code = 0
    except Rejected as exc:
        result, code = {'ok': False, 'error': str(exc)}, 2
    except Exception:
        result, code = {'ok': False, 'error': 'fallo_local_verificar_sin_secretos'}, 2
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != 'serve':
        sys.exit(2)
    sys.exit(serve(sys.argv[2]))
