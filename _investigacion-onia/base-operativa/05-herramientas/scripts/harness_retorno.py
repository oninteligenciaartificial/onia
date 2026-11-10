"""Publica sólo el registro/evidencia de una tarea y notifica a Boss una vez."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import uuid

import trabajo
from harness_boss import Rejected, checked_id, locked, no_links, private_read, private_write, binding


def git(repo, *args, data=None, index=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    if index is not None:
        env['GIT_INDEX_FILE'] = str(index)
    result = subprocess.run(['git', '-C', str(repo), '-c', 'user.name=OnIA Codex',
                             '-c', 'user.email=onia-codex-worker@localhost', *args],
                            input=data, capture_output=True, env=env, timeout=120)
    if result.returncode:
        raise Rejected('publicacion_pendiente_conciliar_git')
    return result.stdout.decode().strip()


def safe_content(blob):
    text = blob.decode('utf-8')
    if len(blob) > 2_000_000 or any(re.search(pattern, text) for pattern in (
            r'-----BEGIN .*PRIVATE KEY', r'gh[pousr]_[A-Za-z0-9]{20,}',
            r'(?i)Bearer\s+[A-Za-z0-9._-]{20,}',
            r'https?://[^\s/]+:[^\s/]+@', r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')):
        raise Rejected('contenido_no_compartible')


def publish(config, row):
    """Private Git index; never stages, cleans or resets the coordinator checkout."""
    base = no_links(config['base'])
    repo = Path(git(base, 'rev-parse', '--show-toplevel'))
    root = no_links(config['privado'])
    ident = checked_id(row['id'])
    task = trabajo.task_path(base, ident, True)
    relative = task.relative_to(repo).as_posix()
    task_bytes = trabajo.regular_bytes(task)
    if json.loads(task_bytes) != row:
        raise Rejected('tarea_cambio_durante_publicacion')
    trabajo.verify(base, row)
    refs = [row['briefing'], *row['evidencias'], *row.get('evidencias_revision', [])]
    refs.extend(x['fuente'] for x in row.get('decisiones', []))
    observed = (row.get('ejecucion') or {}).get('observado')
    if observed:
        refs.append(observed['fuente'])
    for field in ('cierre', 'revision_independiente'):
        if (row.get(field) or {}).get('evidencia'):
            refs.append(row[field]['evidencia'])
    git(repo, 'fetch', 'origin', 'refs/heads/master:refs/remotes/origin/master')
    remote = git(repo, 'rev-parse', 'refs/remotes/origin/master')
    remote_entry = git(repo, 'ls-tree', remote, '--', relative)
    remote_task = git(repo, 'rev-parse', remote + ':' + relative) if remote_entry else None
    remote_row = json.loads(git(repo, 'show', remote + ':' + relative)) if remote_entry else None
    local_task = git(repo, 'hash-object', '--stdin', data=task_bytes)
    marker = root / 'publicaciones' / (ident + '.json')
    old = private_read(marker) if marker.exists() else None
    # Una publicación manual verificada puede adelantar HEAD desde el último
    # aviso; no exigir que un marcador de transporte sea el estado canónico.
    head_entry = git(repo, 'ls-tree', 'HEAD', '--', relative)
    known = {local_task}
    if head_entry:
        known.add(git(repo, 'rev-parse', 'HEAD:' + relative))
    if old:
        known.add(old['task_blob'])
    if remote_task is not None and remote_task not in known:
        raise Rejected('registro_remoto_cambio_no_sobrescribir')
    if remote_task is None and (head_entry or old):
        raise Rejected('registro_remoto_desaparecido')
    if remote_row and (remote_row['revision'] > row['revision'] or (remote_row['revision'] == row['revision'] and remote_task != local_task)):
        raise Rejected('revision_remota_no_retroceder')
    index = root / ('indice-' + uuid.uuid4().hex)
    git(repo, 'read-tree', remote, index=index)
    files = {relative: task_bytes}
    checks = {}
    for ref in refs:
        path = trabajo.safe_path(base, ref['archivo'])
        data = trabajo.regular_bytes(path)
        if hashlib.sha256(data).hexdigest() != ref['sha256']:
            raise Rejected('evidencia_cambio')
        name = path.relative_to(repo).as_posix()
        entry = git(repo, 'ls-tree', remote, '--', name)
        sha = git(repo, 'hash-object', '--stdin', data=data)
        checks[name] = sha
        if entry and entry.split('\t')[0] != '100644 blob ' + sha:
            raise Rejected('evidencia_remota_inmutable_no_sobrescribir')
        own = (ref['archivo'].startswith('04-operacion-agentes/evidencias/' + ident + '/')
               or ref['archivo'] == '04-operacion-agentes/encargos/' + ident + '.md')
        if not own:
            # Context outside this task may be referenced only when already published unchanged.
            if git(repo, 'rev-parse', remote + ':' + name) != git(repo, 'hash-object', '--stdin', data=data):
                raise Rejected('fuente_externa_no_publicada')
            continue
        files[name] = data
    for name, data in files.items():
        safe_content(data)
        sha = git(repo, 'hash-object', '-w', '--stdin', data=data)
        checks[name] = sha
        git(repo, 'update-index', '--add', '--cacheinfo', '100644,' + sha + ',' + name, index=index)
    tree = git(repo, 'write-tree', index=index)
    if tree == git(repo, 'rev-parse', remote + '^{tree}'):
        commit = remote
    else:
        commit = git(repo, 'commit-tree', tree, '-p', remote,
                     '-m', 'harness: estado ' + ident + ' r' + str(row['revision']))
        git(repo, 'push', 'origin', commit + ':refs/heads/master')  # Fast-forward only; no force.
    current = git(repo, 'ls-remote', 'origin', 'refs/heads/master').split()[0]
    if current != commit:
        git(repo, 'fetch', 'origin', 'refs/heads/master:refs/remotes/origin/master')
        git(repo, 'merge-base', '--is-ancestor', commit, 'origin/master')
    for name, expected in checks.items():
        entry = git(repo, 'ls-tree', current, '--', name)
        if entry.split('\t')[0] != '100644 blob ' + expected:
            raise Rejected('snapshot_remoto_sustituido')
    private_write(marker, {'commit': commit, 'task_blob': local_task})
    return commit


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_secret(config):
    if set(config) != {'url', 'clave'}:
        raise Rejected('configuracion_webhook_invalida')
    url, key = config['url'], config['clave']
    if not isinstance(url, str) or not isinstance(key, str):
        raise Rejected('configuracion_webhook_invalida')
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
            or parsed.fragment or parsed.port not in (None, 443)
            or any(c.isspace() for c in url + key) or len(key) < 16):
        raise Rejected('configuracion_webhook_invalida')
    # Config is typed locally by Sergio, never supplied by an SSH caller.
    return url, key


def post(secret, payload):
    url, key = validate_secret(secret)
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST',
                                 headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(req, timeout=15) as response:
        return response.status == 200


def deliver(config, ident, sender=post, expected_revision=None, expected_binding=None, finished_attempt=None, on_snapshot=None):
    ident = checked_id(ident)
    if not isinstance(config.get('lectura_ids'), list) or ident not in config['lectura_ids']:
        raise Rejected('id_no_habilitado')
    root, base = no_links(config['privado']), no_links(config['base'])
    with locked(root / 'retornos'), trabajo.locked(base, ident):
        row = trabajo.read_task(base, ident)
        if ((expected_revision is not None and row['revision'] != expected_revision)
                or (expected_binding is not None and binding(row) != expected_binding)):
            raise Rejected('snapshot_autorizado_cambio')
        if not row.get('compartible'):
            raise Rejected('tarea_no_compartible')
        trabajo.verify(base, row)
        if finished_attempt is not None:
            terminal_session(row, finished_attempt, config['operacion'])
        else:
            if not row.get('cierre'):
                raise Rejected('sin_cierre_compartible')
            if row['cierre'].get('dry_run'):
                raise Rejected('sin_avisos_de_simulacion')
        if on_snapshot is not None:
            on_snapshot(row)
        event = root / 'retornos' / (ident + '-r' + str(row['revision']) + '.json')
        if event.exists():
            prior = private_read(event)
            if prior['estado_envio'] in {'enviando', 'incierto', 'recibido_http'}:
                return {'estado_envio': prior['estado_envio'], 'repetido': True,
                        'acuse_boss': False, 'commit': prior['payload']['commit'], 'revision': row['revision']}
        try:
            commit = publish(config, row)
        except Exception:
            return {'estado_envio': 'pendiente_publicacion', 'acuse_boss': False, 'revision': row['revision']}
        payload = {k: row[k] for k in ('id', 'revision', 'estado')}
        payload['commit'] = commit  # Snapshot in master containing THIS task revision.
        record = {'payload': payload, 'estado_envio': 'pendiente_configuracion'}
        private_write(event, record)
        secret_path = root / 'webhook.json'
        if not secret_path.exists():
            return {'estado_envio': record['estado_envio'], 'acuse_boss': False, 'commit': commit, 'revision': row['revision']}
        secret = private_read(secret_path)
        validate_secret(secret)
        private_write(event, dict(record, estado_envio='enviando'))
        try:
            received = sender(secret, payload)
        except Exception:
            received = False
        status = 'recibido_http' if received else 'incierto'
        private_write(event, dict(record, estado_envio=status))
        return {'estado_envio': status, 'acuse_boss': False, 'commit': commit, 'revision': row['revision']}


def terminal_session(row, attempt, operation):
    import harness_sesiones as sessions
    matches = [s for s in row.get('sesiones', []) if s['intento'] == attempt]
    if (len(matches) != 1 or type(attempt) is not int
            or matches[0]['operacion'] != str(operation) or matches[0]['dry_run']
            or matches[0]['estado'] not in {'finalizada', 'fallida', 'interrumpida', 'cerrada'}
            or not matches[0].get('fin') or sessions.alive(matches[0])):
        raise Rejected('sin_fin_de_sesion_comprobado')
    return matches[0]


def session_finished(base, operation, ident, attempt, retry_pending=False):
    """Callback optativo, una vez por intento; no crea vigilancia ni sesiones."""
    root = no_links(Path(operation) / 'puente-boss')
    config_path = root / 'config.json'
    if not config_path.exists():
        return None
    with locked(root):
        config = private_read(config_path)
        if (config.get('avisar_fin_sesion') is not True or config.get('pausado') is not False
                or not isinstance(config.get('lectura_ids'), list) or ident not in config['lectura_ids']
                or not isinstance(config.get('avisos_fin_ids'), list) or ident not in config['avisos_fin_ids']):
            return None
        if (Path(config['base']) != Path(base) or Path(config['operacion']) != Path(operation)
                or Path(config['privado']) != root):
            raise Rejected('base_no_configurada')
        checked_id(ident)
        if type(attempt) is not int or attempt < 1:
            raise Rejected('intento_invalido')
        marker = root / 'fines' / (ident + '-i' + str(attempt) + '.json')
        expected = None
        if marker.exists():
            # Incluso una caída entre POST y registro impide despertar dos veces.
            prior = private_read(marker)
            if not retry_pending or prior['estado_envio'] not in {'pendiente_publicacion', 'pendiente_configuracion'}:
                return dict(prior, repetido=True)
            expected = prior['revision']  # Cambio de snapshot exige conciliación explícita.
        pending = {'id': ident, 'intento': attempt, 'revision': expected, 'estado_envio': 'iniciando'}
        def remember(row):
            pending['revision'] = row['revision']
            private_write(marker, pending)  # Snapshot válido; antes de publicar o POST.
        try:
            # Elegir/verificar el snapshot ocurre una sola vez bajo el lock de
            # tarea de deliver; admite un intento terminado ya cerrado/anterior.
            result = deliver(config, ident, expected_revision=expected, finished_attempt=attempt, on_snapshot=remember)
        except Exception:
            if marker.exists():
                private_write(marker, dict(pending, estado_envio='requiere_conciliacion'))
            raise
        private_write(marker, dict(pending, **result))
        return result


def publish_review(config, ident, expected_revision):
    """Recoger publica el veredicto para que Boss pueda leerlo sin shell libre."""
    base = no_links(config['base'])
    with locked(no_links(config['privado']) / 'retornos'), trabajo.locked(base, ident):
        row = trabajo.read_task(base, ident)
        trabajo.expected(row, expected_revision)
        if not row.get('revision_independiente'):
            raise Rejected('sin_revision_recogida')
        trabajo.verify(base, row)
        try:
            commit = publish(config, row)
        except Exception:
            # El veredicto ya está guardado: un nuevo recoger puede publicarlo
            # sin lanzar revisor ni bloquear toda la tarea por un fallo Git.
            return {'estado_publicacion': 'pendiente_publicacion', 'revision': row['revision']}
        return {'estado_publicacion': 'publicado', 'commit': commit}


def configured(base, operation, ident, expected_revision=None):
    """Local CLI opt-in; not a global hook affecting old tasks."""
    root = no_links(Path(operation) / 'puente-boss')
    config = private_read(root / 'config.json')
    if Path(config['base']) != Path(base) or Path(config['operacion']) != Path(operation):
        raise Rejected('base_no_configurada')
    return deliver(config, ident, expected_revision=expected_revision)
