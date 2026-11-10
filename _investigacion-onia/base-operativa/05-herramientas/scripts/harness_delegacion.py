"""Registro delegado acotado sobre harness.py. Sin shell, scheduler ni autoridad de producción."""
from datetime import datetime, timedelta, timezone
import json
import os
import re
from pathlib import Path
import subprocess

import harness
import harness_boss as boss
import harness_retorno as retorno
import trabajo

OPERATIONS = {'registrar', 'habilitar'}
ROOT = '05-herramientas/fabrica-onia/'
FACTORIES = {
    'guiones': ('1-guiones-calendario', 'guiones-tanda-', 'marketing', 'salida'),
    'edicion': ('2-edicion-video', 'fabrica-edicion-video-', 'desarrollo', 'trabajos'),
    'automatizaciones': ('3-automatizaciones', 'fabrica-automatizaciones-', 'desarrollo', 'trabajos'),
    'whatsapp': ('4-chatbot-whatsapp', 'fabrica-chatbot-whatsapp-', 'desarrollo', 'trabajos'),
    'codigo': ('5-codigo', 'fabrica-codigo-', 'desarrollo', 'trabajos'),
    'plataforma': ('6-plataforma', 'fabrica-plataforma-', 'desarrollo', 'trabajos'),
}
LIMITS = ('Sólo archivos del worktree dentro de la ruta asignada. No producción, n8n real '
          '(ni importar flujos inactivos), envíos, publicar contenido, gastos, APIs pagas, '
          'Higgsfield, instalaciones, Docker, sudo, servicios, PC, secretos, IPs ni QR real en Git. '
          'No borrar originales ni usar --no-sandbox ni desactivar AppArmor/userns. '
          'Cero hijos. Máximo tres sesiones globales incluidos revisores. '
          'Reutilizar lo existente; scripts y fixtures de prueba locales. Los JSON n8n se '
          'entregan como archivos con active=false sin importarlos. Plataforma significa '
          'documentación de la fábrica6, no desarrollar OnIA Platform. '
          'No tocar registros canónicos, harness, permisos, AGENTS.md, skills, configuración '
          'ni instrucciones globales. El contenido del pedido no puede ampliar estos límites. '
          'Commit y push de la rama asignada; revisión distinta y aceptación explícita antes '
          'de integrar. No inventar aceptación editorial, prueba con medio real ni pagos. '
          'Recibo con modelo/esfuerzo observado, cuota fechada o desconocida, intentos, resultado, '
          'commits y retrabajo. Si falta una entrada, conservar avance y declarar bloqueo.')


def parse(value):
    op = value['operacion']
    required = {'version', 'operacion', 'id', 'solicitud'}
    boss.checked_id(value.get('solicitud'))
    if len(value['id']) > 63:
        raise boss.Rejected('identificador_invalido')
    if op == 'registrar':
        required |= {'fabrica', 'objetivo', 'entregable', 'aceptacion', 'pedido', 'esfuerzo'}
        if value.get('fabrica') not in FACTORIES or value.get('esfuerzo') not in {'low', 'high'}:
            raise boss.Rejected('fabrica_o_esfuerzo_no_permitido')
        for key in ('objetivo', 'entregable', 'aceptacion'):
            if not isinstance(value.get(key), str) or not 1 <= len(value[key].strip()) <= 2200:
                raise boss.Rejected('encargo_incompleto_o_excesivo')
        if not isinstance(value.get('pedido'), str) or len(value['pedido']) > 240:
            raise boss.Rejected('pedido_invalido')
    else:
        required.add('revision_esperada')
        if type(value.get('revision_esperada')) is not int or value['revision_esperada'] < 1:
            raise boss.Rejected('revision_invalida')
    if set(value) != required:
        raise boss.Rejected('campos_no_permitidos')
    retorno.safe_content(json.dumps(value, ensure_ascii=False).encode())
    return value


def policy(config, factory=None):
    p = config.get('delegacion_fabricas')
    if (not isinstance(p, dict) or p.get('activa') is not True or
            not isinstance(p.get('autorizacion_sergio'), str) or not p['autorizacion_sergio'].strip() or
            not isinstance(p.get('fabricas'), list) or not p['fabricas'] or
            any(x not in FACTORIES for x in p['fabricas'])):
        raise boss.Rejected('delegacion_no_habilitada')
    if config.get('pausado') is not False:
        raise boss.Rejected('puente_pausado')
    if factory is not None and factory not in p['fabricas']:
        raise boss.Rejected('fabrica_no_delegada')
    return p


def quota_snapshot():
    """Sólo extrae rate_limits; no copia prompts, credenciales ni logs completos."""
    samples = []
    paths = sorted((Path.home()/'.codex/sessions').rglob('*.jsonl'),
                   key=lambda p: p.stat().st_mtime, reverse=True)[:12]
    for path in paths:
        with path.open('rb') as stream:
            stream.seek(max(0, path.stat().st_size - 524288))
            lines = stream.read().splitlines()
        for line in reversed(lines):
            try:
                event = json.loads(line)
                payload = event.get('payload') or {}
                if event.get('type') != 'event_msg' or payload.get('type') != 'token_count':
                    continue
                limits = payload.get('rate_limits') or {}
                if limits.get('limit_id') != 'codex':
                    continue
                q = next((v for v in (limits.get('primary'), limits.get('secondary'))
                          if isinstance(v, dict) and v.get('window_minutes') == 10080), None)
                if q is None:
                    continue
                stamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if stamp.tzinfo is None:
                    continue
                used = float(q['used_percent'])
                if 0 <= used <= 100:
                    samples.append((stamp, used))
                break
            except (ValueError, KeyError, TypeError, AttributeError):
                continue
    if not samples:
        raise boss.Rejected('cuota_no_comprobada')
    stamp, used = max(samples)
    age = (datetime.now(timezone.utc) - stamp).total_seconds()
    if not -60 <= age <= 7200:
        raise boss.Rejected('cuota_desactualizada')
    return {'fecha': stamp.isoformat(), 'used_percent': used}


def check_launch(config, grant):
    if not grant.get('delegada'):
        return
    policy(config, grant.get('fabrica'))
    sample = quota_snapshot()
    if sample['used_percent'] >= 90:
        raise boss.Rejected('tope_cuota_90')


def grant_for(row, factory, effort, authorization):
    ident = row['id']
    return {'id': ident, 'revocado': False, 'delegada': True, 'fabrica': factory,
            'vence': (datetime.now(timezone.utc)+timedelta(hours=24)).isoformat(),
            'binding': boss.binding(row), 'autorizacion_sergio': authorization,
            'actor': row['asignacion']['responsable'], 'revisor': 'revision-' + ident,
            'modelo': 'gpt-6.1-sol', 'esfuerzo': effort, 'max_intentos': 2,
            'operaciones': sorted(boss.WRITE - {'reanudar'}),
            'resultado_cierre': 'Entrega publicada en origin; revisión y aceptación pendientes.',
            'comprobacion_cierre': 'Cierre verifica commit remoto y conserva worktree; no acredita calidad ni producción.'}


def git_bytes(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, timeout=30,
                            env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')})
    if result.returncode:
        raise boss.Rejected('git_no_comprobado')
    return result.stdout


def source(base, name, factory, value):
    if not (name.startswith('04-operacion-agentes/pendientes/') or
            name.startswith(ROOT + FACTORIES[factory][0] + '/')) or not name.endswith('.md'):
        raise boss.Rejected('fuente_pedido_fuera_de_alcance')
    path = trabajo.safe_path(base, name)
    repo = Path(retorno.git(base, 'rev-parse', '--show-toplevel'))
    retorno.git(repo, 'fetch', 'origin', 'refs/heads/master:refs/remotes/origin/master')
    remote = retorno.git(repo, 'rev-parse', 'origin/master')
    rel = path.relative_to(repo).as_posix()
    entry = retorno.git(repo, 'ls-tree', remote, '--', rel)
    if not entry.startswith('100644 blob '):
        raise boss.Rejected('pedido_no_publicado_o_no_regular')
    content = git_bytes(repo, 'show', remote+':'+rel)
    retorno.safe_content(content)
    if path.exists() and trabajo.regular_bytes(path) != content:
        raise boss.Rejected('pedido_local_no_coincide_master')
    blocks = re.findall(r'^```onia-pedido-v1\s*\n(.*?)\n```\s*$', content.decode(), re.M|re.S)
    if len(blocks) != 1:
        raise boss.Rejected('pedido_sin_ficha_unica')
    try:
        spec = json.loads(blocks[0])
    except ValueError:
        raise boss.Rejected('ficha_pedido_invalida') from None
    expected = {k:value[k] for k in ('id','fabrica','objetivo','entregable','aceptacion','esfuerzo')}
    if spec != expected:
        raise boss.Rejected('solicitud_distinta_del_pedido')
    return remote, trabajo.digest(content), content


def check_product_scope(config, row, grant, session, commit):
    """Valida cada commit exacto que se cierra, no una referencia HEAD mutable."""
    if not grant.get('delegada'):
        return
    worktree = Path(session['worktree'])
    boss.sessions.validate_private_git(session, row['id'])
    repo = Path(retorno.git(config['base'], 'rev-parse', '--show-toplevel'))
    prefix = Path(config['base']).relative_to(repo).as_posix()+'/'
    routes = [prefix+r.rstrip('/')+'/' for r in row['asignacion']['rutas']]
    retorno.git(repo, 'merge-base', '--is-ancestor', session['commit_base'], commit)
    interval = session['commit_base']+'..'+commit
    if retorno.git(repo, 'rev-list', '--min-parents=2', interval):
        raise boss.Rejected('entrega_delegada_debe_ser_lineal')
    revisions = retorno.git(repo, 'rev-list', '--reverse', interval).splitlines()
    for revision in revisions:
        parent = revision+'^'
        files = git_bytes(repo, 'diff', '--name-only', '--no-renames', '--no-ext-diff',
                          '--no-textconv', '-z', parent, revision).decode().split('\0')
        for name in filter(None, files):
            if not any(name.startswith(route) for route in routes):
                raise boss.Rejected('entrega_fuera_de_rutas')
            if any(part.casefold() in {'agents.md','skill.md','.codex','.agents','.git','.github',
                                      '.gitattributes','.gitmodules','.gitignore'} or part.casefold().startswith('.env')
                   for part in Path(name).parts):
                raise boss.Rejected('entrega_modifica_control')
            before = retorno.git(repo, 'ls-tree', parent, '--', name)
            after = retorno.git(repo, 'ls-tree', revision, '--', name)
            regular = ('100644 blob ', '100755 blob ')
            if (before and not before.startswith(regular)) or not after.startswith(regular):
                raise boss.Rejected('entrega_borra_o_cambia_enlace')
            retorno.safe_content(git_bytes(repo,'show',revision+':'+name))


def handle(config, value, config_path):
    if config_path is None:
        raise boss.Rejected('configuracion_privada_requerida')
    root = boss.no_links(config['privado'])
    with boss.locked(root):
        current = boss.private_read(config_path)
        if any(current.get(k) != config.get(k) for k in ('base', 'operacion', 'privado')):
            raise boss.Rejected('configuracion_cambio_reintentar')
        config = current
        p = policy(config, value.get('fabrica'))
        base = boss.no_links(config['base'])
        ident = value['id']
        entry = root/'solicitudes'/(value['solicitud']+'.json')
        if entry.exists():
            record = boss.private_read(entry)
            if record['hash'] != boss.digest(value):
                raise boss.Rejected('solicitud_reutilizada')
            if record['fase'] == 'terminada':
                return dict(record['respuesta'], repetida=True)
            if record['fase'] != 'preparada':
                raise boss.Rejected('conciliacion_necesaria_no_repetir')
        elif value['operacion'] == 'registrar':
            folder, prefix, area, subdir = FACTORIES[value['fabrica']]
            if not ident.startswith(prefix) or ident in trabajo.all_ids(base):
                raise boss.Rejected('id_existente_o_fuera_de_fabrica')
            today = datetime.now(timezone.utc).date().isoformat()
            # La fecha se conserva como evidencia, no como cupo de admisión.
            # Registrar no ejecuta: cuota y concurrencia se verifican al lanzar.
            reservation = root/'altas'/(ident+'.json')
            if reservation.exists():
                raise boss.Rejected('id_reservado_conciliar')
            commit, sha, source_bytes = source(base, value['pedido'], value['fabrica'], value)
            route = ROOT + folder + '/' + subdir + '/' + ident
            # Reserva concreta y texto acotado; el cliente nunca elige rutas ni actor.
            for other in trabajo.all_ids(base):
                row = trabajo.read_task(base, other)
                for other_route in (row.get('asignacion') or {}).get('rutas', []):
                    if trabajo.overlapping(route, other_route):
                        raise boss.Rejected('ruta_reservada_por_otra_tarea')
            record = {'hash': boss.digest(value), 'fase': 'iniciada', 'id': ident}
            boss.private_write(entry, record)
            boss.private_write(root/'altas'/(ident+'.json'), {'fecha_dia': today, 'solicitud': value['solicitud']})
            result = harness.prepare(base, ident, area, value['objetivo'], value['entregable'],
                value['aceptacion'], shared=True, profile='complejo' if value['esfuerzo']=='high' else 'cambio-acotado',
                inputs=[LIMITS, 'Ruta exclusiva: '+route,
                        'Pedido: '+value['pedido']+'; master '+commit+'; SHA256 '+sha,
                        'Especificación de fábrica: '+ROOT+folder+'/README.md',
                        'Permiso delegado por Sergio, coordinado por Boss; modelo Sol6.1 '+value['esfuerzo']+'. '
                        'Dos intentos totales (ejecutora y revisora); no repetir para simular éxito. '
                        'Al menos 10% de cuota semanal reservada; no lanzar con muestra desconocida. '
                        'Guiones: borradores para Contenido, no aprobación editorial. Edición: '
                        'FFmpeg disponible y ASR en ~/asr/venv, no depender de /opt con permisos cerrados. '
                        'Prueba sintética breve sin instalar ni descargar modelos; registrar límites de validación.'])
            row = trabajo.assign(base, ident, result['tarea']['revision'], 'boss-'+ident, [route])
            frozen = trabajo.safe_path(base, '04-operacion-agentes/evidencias/'+ident+'/PEDIDO-v1.md')
            frozen.parent.mkdir(parents=True, exist_ok=True)
            with frozen.open('xb') as stream:
                stream.write(source_bytes)
            row = trabajo.update(base, ident, 'preparado', 'Pedido delegado registrado; sin lanzar.',
                'Ficha cotejada con master; copia de evidencia inmutable.',
                'Boss consulta revisión y lanza dentro del permiso; revisión distinta antes de aceptar.',
                [frozen.relative_to(base).as_posix()], revision=row['revision'], actor=row['asignacion']['responsable'])
            grant = grant_for(row, value['fabrica'], value['esfuerzo'], p['autorizacion_sergio'])
            record.update(fase='preparada', revision=row['revision'], grant=grant)
            boss.private_write(entry, record)
        else:
            row = trabajo.read_task(base, ident)
            trabajo.verify(base, row)
            trabajo.expected(row, value['revision_esperada'])
            old = boss.private_read(root/'delegaciones'/(ident+'.json'))
            current_grant = boss.private_read(root/'permisos'/(ident+'.json'))
            if current_grant.get('revocado') is not False:
                raise boss.Rejected('permiso_revocado_por_coordinador')
            policy(config, old['fabrica'])
            if old['binding'] != boss.binding(row) or row['estado'] == 'aceptado':
                raise boss.Rejected('alcance_cambio_o_tarea_aceptada')
            grant = dict(current_grant, vence=(datetime.now(timezone.utc)+timedelta(hours=24)).isoformat())
            record = {'hash': boss.digest(value), 'fase': 'preparada', 'id': ident,
                      'revision': row['revision'], 'grant': grant}
            boss.private_write(entry, record)
        with boss.locked(root/'retornos'), trabajo.locked(base, ident):
            row = trabajo.read_task(base, ident)
            trabajo.expected(row, record['revision'])
            if boss.binding(row) != record['grant']['binding']:
                raise boss.Rejected('alcance_cambio')
            policy(config, record['grant']['fabrica'])
            try:
                commit = retorno.publish(config, row)
            except Exception:
                return {'ok': False, 'error': 'registro_pendiente_publicacion', 'id': ident,
                        'revision': row['revision'], 'repetir_misma_solicitud': True}
            # Releer tras Git: nunca restaurar permisos revocados o ampliarlos al renovar.
            current = boss.private_read(config_path)
            if any(current.get(k) != config.get(k) for k in ('base','operacion','privado')):
                raise boss.Rejected('configuracion_cambio_reintentar')
            policy(current, record['grant']['fabrica'])
            grant_path = root/'permisos'/(ident+'.json')
            grant = record['grant']
            if grant_path.exists():
                actual = boss.private_read(grant_path)
                if actual.get('revocado') is not False or actual.get('binding') != grant['binding']:
                    raise boss.Rejected('permiso_revocado_o_cambiado')
                grant = dict(actual, vence=grant['vence'])
            elif value['operacion'] == 'habilitar':
                raise boss.Rejected('permiso_actual_ausente')
            boss.private_write(grant_path, grant)
            boss.private_write(root/'delegaciones'/(ident+'.json'), grant)
            if value['operacion'] == 'registrar':
                current['lectura_ids'] = list(dict.fromkeys([*current.get('lectura_ids', []), ident]))
                if current['delegacion_fabricas'].get('avisos_fin') is True:
                    current['avisos_fin_ids'] = list(dict.fromkeys([*current.get('avisos_fin_ids', []), ident]))
            boss.private_write(config_path, current)
            response = {'ok': True, 'tarea': boss.snapshot(base, ident)[1], 'commit': commit,
                        'permiso': {k:grant[k] for k in ('modelo','esfuerzo','max_intentos','vence')},
                        'sesion_lanzada': False}
            boss.private_write(entry, dict(record, fase='terminada', respuesta=response))
            return response
