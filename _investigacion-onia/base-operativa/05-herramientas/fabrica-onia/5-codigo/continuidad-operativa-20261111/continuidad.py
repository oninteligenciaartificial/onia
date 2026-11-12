"""Una pasada finita de lotes; harness_lote conserva todos los efectos y estados."""
import argparse
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

SCRIPTS = Path('_investigacion-onia/base-operativa/05-herramientas/scripts')
HERE = Path(__file__).resolve().parent
MAX_SECONDS = 480


def require(value):
    if not value:
        raise ValueError('Configuración inválida; consultar contrato en README.md.')


def read(path):
    path = Path(path)
    require(path.is_absolute() and not any(p.is_symlink() for p in (path, *path.parents)))
    return json.loads(path.read_text(encoding='utf-8'))


def load(path, *, operation=None):
    config = read(path)
    require(isinstance(config, dict))
    require(type(config.get('schema')) is int and config['schema'] == 1)
    root = str(operation or Path.home() / 'operacion')
    lots = config['lotes']
    require(isinstance(lots, list) and len(lots) <= 16)
    ids, orders, manifests = set(), set(), set()
    total = 0
    for entry in lots:
        require(isinstance(entry, dict))
        require(re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', entry['id']))
        require(entry['id'] not in ids and entry['orden'] not in orders)
        require(type(entry['orden']) is int and entry['orden'] >= 0)
        require(type(entry['habilitado']) is bool and entry['operacion'] == root)
        require(re.fullmatch(r'[0-9a-f]{64}', entry['manifiesto_sha256']))
        require(type(entry['limite_segundos']) is int and 5 <= entry['limite_segundos'] <= 120)
        for key in ('manifiesto', 'observaciones'):
            value = entry.get(key)
            if key == 'observaciones' and value is None:
                continue
            require(isinstance(value, str) and Path(value).is_absolute())
        require(entry['manifiesto'] not in manifests)
        ids.add(entry['id'])
        orders.add(entry['orden'])
        manifests.add(entry['manifiesto'])
        total += entry['limite_segundos']
    require(total <= MAX_SECONDS)
    return config


def harness(repo):
    scripts = Path(repo) / SCRIPTS
    require(scripts.is_dir())
    sys.path.insert(0, str(scripts))
    module = importlib.import_module('harness_lote')
    require(Path(module.__file__).resolve() == (scripts / 'harness_lote.py').resolve())
    return module


def reason(message):
    # Nunca publicar mensajes arbitrarios de entradas, API, Git o excepciones.
    text = str(message).lower()
    for words, code in [
        (('cuota', 'proveedor', 'chatgpt'), 'cuota_o_autenticacion'),
        (('máximo 3', 'cupo'), 'tres_cupos_ocupados'),
        (('observaci', 'comprobación explícita'), 'evidencia_coordinadora'),
        (('intención', 'journal', 'conciliar', 'sid'), 'conciliar_journal_sid'),
        (('dos fallos', 'presupuesto'), 'diagnosticar_intentos'),
        (('dependencia',), 'dependencia_pendiente'),
        (('reserva', 'conflicto'), 'reserva_de_rutas'),
        (('autorización', 'alcance', 'briefing'), 'alcance_o_autorizacion'),
        (('activa',), 'otra_pasada_activa'),
    ]:
        if any(word in text for word in words):
            return code
    return 'control_canonico'


def describe(dispatcher, result, module):
    events = dispatcher.events()
    tail = events[-1] if events else None
    tasks = []
    failures = {}
    for event in result.get('eventos', []):
        if event.get('bloqueo'):
            failures[event['id']] = reason(event['bloqueo'])
    for item in result['plan']['tareas']:
        record = {'id': item['id']}
        if 'bloqueo' in item or item['id'] in failures:
            record.update(fallo=failures.get(item['id'], reason(item.get('bloqueo', ''))),
                          proxima_accion='coordinadora: revisar control y evidencia canónica')
        elif item.get('op'):
            record['proxima_accion'] = item['op']
        else:
            row = dispatcher.adapter.row(item['id'])
            if row['estado'] == 'aceptado':
                record['proxima_accion'] = 'coordinadora: comprobar integración/despliegue autorizados'
            elif item.get('acciones_coordinadora'):
                record['proxima_accion'] = 'coordinadora: decidir aceptación o reapertura del commit revisado'
            else:
                record['proxima_accion'] = 'esperar sesión existente; siguiente pasada recogerá su estado'
        if item.get('commit'):
            record['commit'] = item['commit']
        if 'revision' in item:
            record['revision'] = item['revision']
        tasks.append(record)
    actions = [{k: event[k] for k in ('id', 'op', 'clave', 'revision')}
               for event in result.get('eventos', []) if 'clave' in event and 'revision' in event]
    return dict(resultado=result['resultado'], tareas=tasks, avances=actions,
                evidencia={'journal_eventos': len(events),
                           'journal_ultimo_sha256': module.digest(tail) if tail else None})


def step(entry, module, *, adapter=None, clock=None):
    manifest = module.validate_manifest(module.read_json(entry['manifiesto']))
    require(manifest['id'] == entry['id'] and manifest['operacion'] == entry['operacion'])
    require(module.digest(manifest) == entry['manifiesto_sha256'])
    dispatcher = module.Dispatcher(entry['manifiesto'], entry['operacion'],
                                   entry['manifiesto_sha256'], adapter=adapter, clock=clock)
    if not entry['habilitado'] or not manifest['habilitado']:
        return dict(resultado='deshabilitado', proxima_accion='coordinadora: habilitar sólo alcance aprobado')
    if dispatcher.stop.exists():
        return dict(resultado='STOP', proxima_accion='coordinadora: conciliar revocación; conservar STOP')
    now = dispatcher.clock()
    if now < module.timestamp(manifest['desde']):
        return dict(resultado='aun_no_vigente', proxima_accion='esperar inicio autorizado')
    if now >= module.timestamp(manifest['hasta']):
        return dict(resultado='expirado', proxima_accion='coordinadora: revisar vigencia y autorización')
    return describe(dispatcher, dispatcher.tick(entry.get('observaciones'), refresh_quota=True), module)


def execute(command, timeout):
    # stdout privado temporal: no copiar texto bruto ni secretos al journal de systemd.
    # Matar sólo el tick, jamás el grupo: el supervisor canónico debe sobrevivir.
    with tempfile.TemporaryFile() as output:
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            try:
                child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                return dict(resultado='limite_de_tiempo', fallo='tick_interrumpido',
                            proxima_accion='siguiente pasada: recuperar journal; coordinadora concilia intención incierta')
            if child.returncode:
                return dict(resultado='bloqueado', fallo='worker_fallido',
                            proxima_accion='coordinadora: inspeccionar entradas y journal canónico')
            output.seek(0)
            raw = output.read(1048577)
            require(len(raw) <= 1048576)
            return json.loads(raw)
        finally:
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    child.kill()
            child.wait()


def run(config, repo, config_path, *, executor=execute, emit=None):
    """Un tick por entrada, sin bucle de reintentos ni persistencia adicional."""
    module = harness(repo)
    reports = []
    for entry in sorted(config['lotes'], key=lambda e: e['orden']):
        report = dict(id=entry['id'], orden=entry['orden'],
                      manifiesto_sha256=entry['manifiesto_sha256'])
        if entry['habilitado']:
            command = [sys.executable, '-B', str(HERE / 'continuidad.py'),
                       '--lista', str(config_path), '--repo', str(repo),
                       '--uno', entry['id'], '--lista-sha256', module.digest(config)]
            try:
                report.update(executor(command, entry['limite_segundos']))
            except (ValueError, OSError, KeyError, TypeError):
                report.update(resultado='bloqueado', fallo='worker_o_salida_invalida',
                              proxima_accion='coordinadora: inspeccionar entradas y journal canónico')
        else:
            report.update(resultado='deshabilitado', proxima_accion='coordinadora: habilitar sólo alcance aprobado')
        report['fecha'] = datetime.now(timezone.utc).isoformat()
        reports.append(report)
        if emit:
            emit(report)
    return dict(resultado='pasada_completa' if reports else 'sin_lotes', lotes=reports,
                avanzados=sum(r['resultado'] == 'avanzado' for r in reports))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lista', required=True, type=Path)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--validar', action='store_true')
    parser.add_argument('--uno', help=argparse.SUPPRESS)
    parser.add_argument('--lista-sha256', help=argparse.SUPPRESS)
    args = parser.parse_args()
    # systemd detiene sólo el padre; finally termina el worker, conservando supervisores.
    def stop(signum, frame):
        raise SystemExit(128 + signum)
    signal.signal(signal.SIGTERM, stop)
    try:
        config = load(args.lista)
        module = harness(args.repo)
        if args.validar:
            for entry in config['lotes']:
                manifest = module.validate_manifest(module.read_json(entry['manifiesto']))
                require(manifest['id'] == entry['id'] and manifest['operacion'] == entry['operacion']
                        and manifest['repositorio'] == str(args.repo.resolve())
                        and module.digest(manifest) == entry['manifiesto_sha256'])
            result = dict(resultado='configuracion_valida', lotes=len(config['lotes']))
        elif args.uno:
            require(module.digest(config) == args.lista_sha256)
            entry = next(e for e in config['lotes'] if e['id'] == args.uno)
            manifest = module.read_json(entry['manifiesto'])
            require(manifest['repositorio'] == str(args.repo.resolve()))
            result = step(entry, module)
        else:
            result = run(config, args.repo, args.lista,
                         emit=lambda r: print(json.dumps(r, ensure_ascii=False), flush=True))
            result = {k: v for k, v in result.items() if k != 'lotes'}
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 0
    except (ValueError, OSError, KeyError, TypeError, StopIteration):
        print(json.dumps(dict(resultado='bloqueado', fallo='entrada_o_control_canonico',
                              proxima_accion='coordinadora: validar lista, manifiesto, observaciones y journal')))
        return 2


if __name__ == '__main__':
    sys.exit(main())
