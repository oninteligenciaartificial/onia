#!/usr/bin/env python3
"""Un tick acotado por horario/entrada/reconciliación. No contiene scheduler ni LLM."""
import argparse
from datetime import date, datetime
import json
import os
from pathlib import Path
import sqlite3
import sys
from zoneinfo import ZoneInfo

from comun import (BASE, GENERATOR, HERE, atomic, digest, encoded, immutable, lector,
                   locked, module, no_links, now, private_root, read_json, require)
import fuentes
from adaptador_harness import LocalHarness, observed, task_id
from preflight import PreflightError

g = module('generador_flujo', GENERATOR / 'generar.py')
ZONE = ZoneInfo('America/La_Paz')
ACTIONS = {'FUENTE': 'Revisar disponibilidad y metadatos primarios; conservar último éxito.',
           'MODELO_NO_DISPONIBLE': 'Coordinadora: comprobar proveedor incluido; no sustituir por API pagada.',
           'AUTORIZACION_PENDIENTE': 'Coordinadora: invocar un ensayo para este ID con el sí aplicable.',
           'TRES_CUPOS_OCUPADOS': 'Esperar un cupo del registro global; no crear otra carpeta de operación.',
           'CONCILIACION_NECESARIA': 'Coordinadora: cotejar ID, revisión, SID y journal; no repetir un despacho incierto.',
           'RESULTADO_INVALIDO': 'Contenido/coordinadora: corregir en versión nueva conservando el original.',
           'REVISION_CON_CAMBIOS': 'Coordinadora: revisar dictamen exacto y autorizar corrección acotada; sin relanzar automáticamente.',
           'CUOTA_AGOTADA': 'Esperar cuota incluida y consultar de nuevo en vivo; no comprar ni renovar.',
           'LOGIN_CHATGPT_REQUERIDO': 'Coordinadora: comprobar login ChatGPT incluido en el host; no usar API pagada.',
           'PLAN_INCLUIDO_NO_COMPROBADO': 'Coordinadora: comprobar plan incluido; no sustituir por créditos/API.',
           'CUOTA_PERMISO_DESCONOCIDO': 'Repetir lectura vigente en el host; un permiso desconocido bloquea el lanzamiento.',
           'CUOTA_CODEX_DESCONOCIDA': 'Revisar respuesta vigente de cuota Codex; no usar muestras históricas.',
           'CUOTA_VENTANA_VENCIDA': 'Consultar cuota de nuevo; no suponer renovación porque pasó una fecha de reset.',
           'PREFLIGHT_RPC_FALLIDO': 'Coordinadora: revisar el RPC local y reintentar la lectura; no se lanzó un modelo.',
           'PREFLIGHT_TIMEOUT': 'Lectura de cuota/login agotó el plazo; revisar RPC antes de un nuevo intento.',
           'PREFLIGHT_DATOS_INVALIDOS': 'Respuesta de login/cuota inválida; corregir o actualizar el lector antes de lanzar.',
           'PREFLIGHT_RESPUESTA_EXCESIVA': 'RPC excedió límites de respuesta; revisar protocolo sin exponer sus payloads.',
           'PUBLICACION_PANEL_FALLIDA': 'Reintentar sólo la proyección; conservar última actualización real.'}


class Store:
    """Journal de eventos/efectos y referencias al harness. No es registro de tareas."""
    def __init__(self, root):
        self.root = private_root(root)
        path = no_links(self.root / 'ciclo.sqlite3')
        if not path.exists():
            os.close(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600))
        require(path.is_file() and path.stat().st_nlink == 1 and not path.stat().st_mode & 0o077, 'DB_NO_PRIVADA')
        self.db = sqlite3.connect(path)
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS journal(kind TEXT,key TEXT,data TEXT,PRIMARY KEY(kind,key))')
        self.db.commit()

    def get(self, kind, key, default=None):
        row = self.db.execute('SELECT data FROM journal WHERE kind=? AND key=?', (kind, key)).fetchone()
        return json.loads(row[0]) if row else default

    def put(self, kind, key, value):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO journal VALUES(?,?,?)', (kind, key, encoded(value).decode()))

    def rows(self, kind):
        return [json.loads(row[0]) for row in self.db.execute('SELECT data FROM journal WHERE kind=? ORDER BY key', (kind,))]

    def close(self):
        self.db.close()


def make_request(day, news, stamp, synthetic):
    brain = g.brain_module()
    catalog = brain.cargar(g.BRAIN / 'catalogo.json')
    context = brain.consultar(catalog, [], ['guiones'])
    decisions = BASE / '05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md'
    return {'schema': 'onia-pedido-diario-v1', 'dia': day, 'creado': stamp,
            'sintetico': synthetic, 'noticias': news, 'oferta': g.OFFER,
            'decisiones_sha256': lector.sha(decisions.read_bytes()),
            'cerebro': context, 'cerebro_sha256': lector.sha((g.BRAIN / 'catalogo.json').read_bytes()),
            'prompt': str(HERE / 'PROMPT-DIARIO.md'),
            'generador': str(GENERATOR / 'generar.py'),
            'contratos': str(GENERATOR / 'entradas'),
            'generador_sha256': lector.sha((GENERATOR / 'generar.py').read_bytes()),
            'prompt_sha256': lector.sha((HERE / 'PROMPT-DIARIO.md').read_bytes()),
            'limites': {'candidatas': 20, 'piezas': 5, 'sesiones': 2, 'global': 3, 'hijos': 0,
                        'editorial': 'pendiente', 'publicacion': False}}


def validate_result(request, brief, sources, draft):
    require(brief.get('fecha_tanda') == request['dia'], 'TANDA_DE_OTRO_DIA')
    stamp = g.stamp(brief['generado'])
    require(stamp >= g.stamp(request['creado']) and stamp.astimezone(ZONE).date().isoformat() == request['dia'], 'FECHA_DE_REDACCION_INVALIDA')
    candidates = brief.get('candidatas', [])
    require(len(candidates) == 20 and len({r.get('id') for r in candidates}) == 20, 'VEINTE_CANDIDATAS_REQUERIDAS')
    selected = [r for r in candidates if r.get('decision') == 'seleccionada']
    require(len(selected) == 5 and {r.get('pieza') for r in selected} == set(g.IDS), 'CINCO_SELECCIONADAS_REQUERIDAS')
    for row in candidates:
        for field in ('id', 'idea', 'motivo'):
            g.text_field(row, field)
        require(row.get('decision') in {'seleccionada', 'descartada', 'reserva_evergreen'}, 'DECISION_EDITORIAL_INVALIDA')
    hypotheses = brief.get('hipotesis_editoriales', [])
    require(len(hypotheses) >= 3 and any(r.get('critico') for r in hypotheses), 'CRITICA_EDITORIAL_REQUERIDA')
    expected = {n['url']: n for n in request['noticias']}
    for item in sources.get('items', []):
        if item.get('tipo') == 'web_primaria':
            original = expected.get(item.get('url'))
            require(original and item.get('publicada') == original['publicada']
                    and item.get('fecha_hecho') == original['fecha_hecho']
                    and item.get('sha256_respuesta') == original['sha256_respuesta']
                    and item.get('consultada') == original['consultada'], 'FUENTE_NO_CORRESPONDE_AL_PEDIDO')
    g.validate(brief, sources, draft)


class Engine:
    def __init__(self, root, adapter=None, clock=now, hook=lambda *_: None):
        self.store = Store(root)
        self.root, self.adapter, self.clock, self.hook = self.store.root, adapter, clock, hook

    def ingest(self, report, queue_input=True):
        meta = self.store.get('meta', 'fuentes', {})
        meta.update(ultimo_intento=report['consulta'], errores=report['errores'], cursor=report['cursor'])
        if not report['errores']:
            meta['ultimo_exito'] = report['finalizada']
        self.store.put('meta', 'fuentes', meta)
        fresh = []
        for item in report['items']:
            # También valida eventos entregados por adaptadores/dobles, no sólo el lector HTTP.
            fuentes.canonical(item['url'])
            published = date.fromisoformat(item['publicada'])
            require(published <= datetime.fromisoformat(item['consultada']).date(), 'FUENTE_FUTURA')
            old = self.store.get('noticia', item['url'])
            if old is None:
                # Persistir la obligación antes de deduplicar la noticia: una caída no la pierde.
                editorial_day = datetime.fromisoformat(self.clock()).astimezone(ZONE).date().isoformat()
                if queue_input:
                    self.store.put('entrada_pendiente', editorial_day, {'sintetico': report.get('sintetico', False)})
                fresh.append(item)
            # Mantener la primera fecha observada y las correcciones del artículo, sin crear otro trabajo.
            self.store.put('noticia', item['url'], {**item, 'primera_consulta': (old or item).get('primera_consulta', item['consultada'])})
        return fresh

    def step(self, trigger='entrada', report=None, authorized_id=None, provider=False):
        require(trigger in {'entrada', 'horario', 'reconciliar'}, 'DISPARADOR_INVALIDO')
        stamp = self.clock()
        day = datetime.fromisoformat(stamp).astimezone(ZONE).date().isoformat()
        fresh = self.ingest(report) if report is not None else []
        eligible = [n for n in self.store.rows('noticia') if 0 <= (date.fromisoformat(day) - date.fromisoformat(n['publicada'])).days <= 7]
        cycle = self.store.get('ciclo', day)
        source_failed = bool(self.store.get('meta', 'fuentes', {}).get('errores'))
        unfinished_request = self.store.get('pedido', day)
        fresh_urls = {n['url'] for n in fresh}
        pending_input = self.store.get('entrada_pendiente', day) or {}
        if cycle is None and (unfinished_request or (pending_input and eligible) or any(n['url'] in fresh_urls for n in eligible)
                              or (trigger == 'horario' and not source_failed)):
            request = unfinished_request or make_request(day, eligible[:20], stamp, (report or pending_input or {}).get('sintetico', False))
            self.store.put('pedido', day, request)  # intención durable antes del archivo derivado
            folder = private_root(self.root / 'pedidos')
            path = folder / (task_id(day) + '.json')
            immutable(path, request)
            cycle = {'dia': day, 'id': task_id(day), 'pedido_sha256': digest(request),
                     'pedido': path.name, 'fase': 'pendiente_redaccion', 'creado': request['creado'], 'error': None}
            self.store.put('ciclo', day, cycle)
        if cycle is not None:
            self.store.put('entrada_pendiente', day, False)
        # Reconciliar ciclos previos también, sin lanzar el trabajo de ayer con un permiso para hoy.
        for candidate in self.store.rows('ciclo')[-14:]:
            if candidate['dia'] != day:
                self.advance(candidate, authorized_id, provider)
        if cycle:
            self.advance(cycle, authorized_id, provider)
        try:
            self.project()
        except (OSError, ValueError):
            self.store.put('meta', 'panel_error', {'codigo': 'PUBLICACION_PANEL_FALLIDA', 'fecha': stamp})
            raise
        return self.projection()

    def advance(self, cycle, authorized_id, provider):
        if cycle['fase'] == 'correccion_pendiente_revision':
            return
        try:
            folder = private_root(self.root / 'pedidos')
            path = folder / cycle['pedido']
            if not path.exists():
                original = self.store.get('pedido', cycle['dia'])
                require(original and digest(original) == cycle['pedido_sha256'], 'PEDIDO_NO_RECUPERABLE')
                immutable(path, original)
            request = read_json(path)
            require(digest(request) == cycle['pedido_sha256'], 'PEDIDO_ALTERADO')
        except (OSError, ValueError, KeyError, TypeError):
            cycle['error'] = 'CONCILIACION_NECESARIA'
            self.store.put('ciclo', cycle['dia'], cycle)
            return
        if not self.adapter:
            cycle['error'] = 'MODELO_NO_DISPONIBLE' if not provider else 'AUTORIZACION_PENDIENTE'
            self.store.put('ciclo', cycle['dia'], cycle)
            return
        try:
            row = self.adapter.query(cycle['id'])
            # Journal de efectos es una referencia, el estado de tarea se consulta al harness.
            cycle['harness'] = {k: row.get(k) for k in ('revision', 'state', 'commit', 'review')}
            if row['exists']:
                self.adapter.check_scope(request, row)
            for op in ('registrar', 'lanzar', 'cerrar', 'revisar', 'recoger'):
                action = self.store.get('efecto', cycle['id'] + ':' + op)
                if action and action['fase'] == 'enviando':
                    if observed(op, action['antes'], row):
                        action['fase'] = 'confirmado'
                        self.store.put('efecto', cycle['id'] + ':' + op, action)
                    elif op == 'registrar' and row['exists'] and not row.get('actor'):
                        # Preparación parcial necesita reconciliar asignación con coordinadora.
                        cycle['error'] = 'CONCILIACION_NECESARIA'
                        return
                    else:
                        cycle['error'] = 'CONCILIACION_NECESARIA'
                        return
            if row['exists']:
                writers = [s for s in row.get('sessions', []) if s['role'] == 'ejecutor']
                reviewers = [s for s in row.get('sessions', []) if s['role'] == 'revisor']
                if row.get('commit') != cycle.get('resultado_commit'):
                    cycle['revision_tecnica'] = None
                    cycle['fase'] = 'validando_entrega'
                if row.get('commit') and (not cycle.get('resultado') or row['commit'] != cycle.get('resultado_commit')):
                    self.accept_result(cycle, request, *self.adapter.result(request))
                if (row.get('review') or {}).get('verdict'):
                    review = row['review']
                    require(review.get('commit') == row.get('commit') == cycle.get('resultado_commit'), 'REVISION_OBSOLETA')
                    cycle['revision_tecnica'] = review
                    cycle['fase'] = 'para_revision_editorial' if review['verdict'] == 'bueno' else 'correccion_pendiente'
                    cycle['error'] = None if review['verdict'] == 'bueno' else 'REVISION_CON_CAMBIOS'
                    return
                if row.get('commit'):
                    if not cycle.get('resultado'):
                        self.accept_result(cycle, request, *self.adapter.result(request))
                    if reviewers:
                        if reviewers[-1]['alive']:
                            cycle['fase'], cycle['error'] = 'revision_tecnica_en_curso', None
                            return
                        require(reviewers[-1]['finished'] and reviewers[-1]['rc'] == 0, 'REVISION_FALLIDA')
                        op = 'recoger'
                    else:
                        op = 'revisar'
                elif writers:
                    if writers[-1]['alive']:
                        cycle['fase'], cycle['error'] = 'redaccion_en_curso', None
                        return
                    require(writers[-1]['finished'] and writers[-1]['rc'] == 0, 'REDACCION_FALLIDA')
                    op = 'cerrar'
                else:
                    op = 'lanzar'
            else:
                op = 'registrar'
            if authorized_id != cycle['id']:
                cycle['error'] = 'AUTORIZACION_PENDIENTE'
                return
            if not provider and op not in {'cerrar', 'recoger'}:
                cycle['error'] = 'MODELO_NO_DISPONIBLE'
                return
            if op == 'lanzar':
                require(request['dia'] == datetime.fromisoformat(self.clock()).astimezone(ZONE).date().isoformat(), 'DIA_DE_TANDA_VENCIDO')
                require(request['generador_sha256'] == lector.sha((GENERATOR / 'generar.py').read_bytes()), 'GENERADOR_CAMBIO')
                require(request['decisiones_sha256'] == lector.sha((BASE / '05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md').read_bytes()), 'DECISIONES_CAMBIARON')
                require(request['prompt_sha256'] == lector.sha((HERE / 'PROMPT-DIARIO.md').read_bytes()), 'PROMPT_CAMBIO')
            if op in {'lanzar', 'revisar'} and row['occupied'] >= 3:
                cycle['error'] = 'TRES_CUPOS_OCUPADOS'
                return
            key = cycle['id'] + ':' + op
            prior = self.store.get('efecto', key)
            require(not prior or prior['fase'] == 'preparado', 'EFECTO_YA_CONFIRMADO_RECONCILIAR')
            action = {'operacion': op, 'fase': 'preparado', 'antes': row, 'fecha': self.clock()}
            self.store.put('efecto', key, action)
            self.hook('antes_despacho', op)
            action['fase'] = 'enviando'
            self.store.put('efecto', key, action)  # fsync transacción ANTES del efecto externo
            receipt = self.adapter.invoke(op, request, row, self.root / 'pedidos' / cycle['pedido'])
            if isinstance(receipt, dict) and 'preflight' in receipt:
                cycle['preflight_ultimo'] = receipt['preflight']
            self.hook('despues_despacho', op)
            after = self.adapter.query(cycle['id'])
            require(observed(op, row, after), 'EFECTO_SIN_CONFIRMACION')
            action['fase'] = 'confirmado'
            self.store.put('efecto', key, action)
            cycle['harness'] = {k: after.get(k) for k in ('revision', 'state', 'commit', 'review')}
            cycle['fase'], cycle['error'] = 'harness_' + op, None
        except PreflightError as error:
            # La excepción sólo procede de la lectura anterior a sessions.launch.
            # No hubo despacho: su intención puede intentarse de nuevo con lectura nueva.
            action['fase'] = 'preparado'
            action['preflight_error'] = error.code
            self.store.put('efecto', key, action)
            cycle['error'] = error.code
            cycle['preflight_ultimo'] = {'permitido': False, 'codigo': error.code, 'intento_finalizado': self.clock()}
        except (OSError, ValueError, KeyError, TypeError, AttributeError, StopIteration, UnicodeError):
            # Mensajes de proveedores/harness son privados. No copiar excepciones al panel.
            if cycle.get('error') != 'RESULTADO_INVALIDO':
                cycle['error'] = 'CONCILIACION_NECESARIA'
        finally:
            self.store.put('ciclo', cycle['dia'], cycle)

    def accept_result(self, cycle, request, brief, sources, draft, corrections=None):
        try:
            validate_result(request, brief, sources, draft)
            require(g.stamp(brief['generado']) <= g.stamp(self.clock()), 'REDACCION_FECHADA_EN_FUTURO')
            corrected, _ = g.apply_corrections(draft, corrections)
            source_commit = (cycle.get('harness') or {}).get('commit') if not corrections else None
            version = digest({'brief': brief, 'sources': sources, 'draft': draft, 'corrections': corrections, 'commit': source_commit})
            root = private_root(self.root / 'v3')
            output = no_links(root / (cycle['id'] + '-' + version[:16]))
            if output.exists():
                # Recuperación tras caída posterior al ensamblado: comprobar TODOS los bytes del recibo.
                receipt = g.load(output / 'recibo.json')
                expected = {'brief': g.fingerprint(brief), 'fuentes': g.fingerprint(sources),
                            'redaccion': g.fingerprint(draft), 'correcciones': g.fingerprint(corrections)}
                require(receipt['entradas'] == expected, 'SALIDA_DE_OTRA_ENTRADA')
                for name, item in receipt['archivos'].items():
                    require(Path(name).name == name, 'RUTA_INVALIDA_EN_RECIBO')
                    raw = no_links(output / name).read_bytes()
                    require(lector.sha(raw) == item['sha256'] and len(raw) == item['bytes'], 'SALIDA_INCOMPLETA_O_ALTERADA')
            else:
                g.build(brief, sources, draft, corrections, output, output_root=root)
            result = {'generado': brief['generado'], 'version': corrected['version'], 'huella': version,
                      'sintetico': request['sintetico'], 'commit': source_commit, 'piezas': []}
            for row in g.load(output / 'guiones-panel.json')['guiones']:
                result['piezas'].append({k: row[k] for k in ('id', 'titulo', 'texto', 'sha256', 'version_editorial')})
            # Versiones anteriores son inmutables. Ni aprobadas ni grabadas se pisan.
            self.store.put('resultado', version, result)
            cycle['resultado'], cycle['error'] = version, None
            cycle['resultado_commit'] = source_commit
            if corrections:
                cycle['revision_tecnica'] = None
                cycle['fase'] = 'correccion_pendiente_revision'
            self.store.put('ciclo', cycle['dia'], cycle)
        except (OSError, ValueError, KeyError, TypeError, AttributeError, StopIteration, UnicodeError):
            cycle['error'] = 'RESULTADO_INVALIDO'
            cycle['fase'] = 'resultado_invalido'
            self.store.put('ciclo', cycle['dia'], cycle)
            raise

    def projection(self):
        meta = self.store.get('meta', 'fuentes', {})
        cycles, errors = [], []
        for row in self.store.rows('ciclo')[-14:]:
            summary = {k: row.get(k) for k in ('dia', 'id', 'fase', 'creado', 'error', 'harness', 'revision_tecnica')}
            summary['revision_editorial'] = 'pendiente'
            summary['resultado'] = self.store.get('resultado', row.get('resultado', ''))
            cycles.append(summary)
            if row.get('error'):
                errors.append({'codigo': row['error'], 'siguiente': ACTIONS.get(row['error'], ACTIONS['CONCILIACION_NECESARIA'])})
        for error in meta.get('errores', []):
            errors.append({'codigo': error['codigo'], 'siguiente': ACTIONS['FUENTE']})
        candidates = [{k: n[k] for k in ('url', 'titulo', 'publicada', 'fecha_hecho', 'consultada', 'primera_consulta')}
                      for n in sorted(self.store.rows('noticia'), key=lambda n: n['publicada'], reverse=True)[:20]]
        return {'schema': 'onia-flujo-panel-v1', 'fuente_ultimo_intento': meta.get('ultimo_intento'),
                'fuente_ultimo_exito': meta.get('ultimo_exito'), 'candidatas': candidates, 'ciclos': cycles,
                'errores': errors, 'programacion': {'habilitada': False, 'zona': 'America/La_Paz', 'hora_tanda': None},
                'publicacion_autorizada': False}

    def project(self):
        atomic(self.root / 'panel.json', self.projection())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', required=True, type=Path)
    parser.add_argument('--evento', choices=('entrada', 'horario', 'reconciliar'), default='entrada')
    parser.add_argument('--url', action='append', help='Máximo tres artículos primarios Anthropic; sin URL consulta índice')
    parser.add_argument('--coordinador-base', type=Path)
    parser.add_argument('--ensayo-real', help='ID exacto del único ciclo autorizado en esta invocación; no inicia recurrencia')
    parser.add_argument('--proveedor-disponible', action='store_true', help='Permiso de uso incluido; cada lanzamiento comprueba login/cuota en vivo por RPC')
    args = parser.parse_args(argv)
    try:
        require(not args.ensayo_real or args.coordinador_base, 'ENSAYO_REQUIERE_COORDINADORA')
        require(not args.url or args.evento != 'reconciliar', 'RECONCILIAR_NO_CONSULTA_RED')
        with locked(args.datos):
            adapter = LocalHarness(args.coordinador_base, Path.home() / 'operacion') if args.coordinador_base else None
            engine = Engine(args.datos, adapter)
            try:
                meta = engine.store.get('meta', 'fuentes', {})
                report = None if args.evento == 'reconciliar' else fuentes.collect(args.url, cursor=meta.get('cursor', 0))
                projection = engine.step(args.evento, report, args.ensayo_real, args.proveedor_disponible)
                print(json.dumps({'ciclos': len(projection['ciclos']), 'candidatas': len(projection['candidatas']),
                    'errores': [e['codigo'] for e in projection['errores']], 'programacion_habilitada': False}))
                return 2 if projection['errores'] else 0
            finally:
                engine.store.close()
    except (OSError, ValueError, sqlite3.Error, KeyError, TypeError, AttributeError, StopIteration, UnicodeError):
        print(json.dumps({'error': 'CICLO_PENDIENTE_REVISAR_DATOS_O_JOURNAL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
