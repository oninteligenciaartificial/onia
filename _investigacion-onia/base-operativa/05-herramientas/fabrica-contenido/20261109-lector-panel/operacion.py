"""Lectura explícita de contratos y revisiones locales append-only, sin harness."""
from contextlib import contextmanager
from datetime import date, datetime
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3

import lector
import tanda

BASE = lector.BASE
ROOT = lector.ROOT
FACTORY_ROOT = '05-herramientas/fabrica-onia/'
PANEL_ROOT = str(ROOT.relative_to(BASE))
BRAIN_ROOT = '03-referentes/cerebro-operativo/20261109'
DECISIONS = FACTORY_ROOT + 'DECISIONES-SERGIO-20261110.md'
SCOPE = '04-operacion-agentes/evidencias/tanda-fabricas-20261111/ALCANCE-v1.md'
FACTORIES = (
    ('guiones', 'Guiones y calendario', FACTORY_ROOT + '1-guiones-calendario'),
    ('edicion', 'Edición de video', FACTORY_ROOT + '2-edicion-video'),
    ('automatizaciones', 'Automatizaciones', FACTORY_ROOT + '3-automatizaciones'),
    ('whatsapp', 'Chatbot de WhatsApp', FACTORY_ROOT + '4-chatbot-whatsapp'),
    ('codigo', 'Código', FACTORY_ROOT + '5-codigo'),
    ('plataforma', 'Plataforma', FACTORY_ROOT + '6-plataforma'),
)
PRODUCERS = {key: root for key, _, root in FACTORIES if key in ('guiones', 'whatsapp')}
PRODUCERS['panel'] = PANEL_ROOT
PRODUCERS['automatizaciones'] = FACTORY_ROOT + '3-automatizaciones/meta-canales-20261111'
PRODUCERS['estrategias'] = '01-negocio/estrategias-operativas-20261111'
STATES = {'pendiente', 'en_curso', 'bloqueado', 'completado', 'para_revision'}
HISTORIC_TANDA = FACTORY_ROOT + '1-guiones-calendario/salida/guiones-tanda-20261111-v2/guiones-panel.json'
MAX_FILE = 512 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, limit=4000):
    require(isinstance(value, str) and 0 < len(value.strip()) <= limit, 'Texto ausente o demasiado largo')
    require(not any(ord(c) < 32 and c not in '\n\r\t' for c in value), 'Caracteres de control')
    return value


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}', value), 'ID inválido')
    return value


def relative_path(value, roots):
    text(value, 500)
    relative = PurePosixPath(value)
    require(not relative.is_absolute() and str(relative) == value and '..' not in relative.parts
            and not any(c in value for c in '\\:?#\x00'), 'Ruta relativa inválida')
    require(not any(p.startswith('.') or p in ('privado', 'operacion') for p in relative.parts), 'Ruta privada')
    require(any(relative.is_relative_to(PurePosixPath(root)) for root in roots), 'Ruta fuera de las raíces permitidas')
    path = BASE / value
    current = BASE
    for part in relative.parts:
        current = current / part
        require(not current.is_symlink(), 'Enlace simbólico rechazado')
    require(path.resolve().is_relative_to(BASE.resolve()), 'Escape de la base')
    return path


def read_relative(value, roots):
    path = relative_path(value, roots)
    require(path.is_file() and path.stat().st_size <= MAX_FILE, 'Archivo ausente o demasiado grande')
    with path.open('rb') as stream:
        raw = stream.read(MAX_FILE + 1)
    require(len(raw) <= MAX_FILE, 'Archivo demasiado grande')
    return raw


def document(value, roots, documents):
    relative_path(value, roots)
    require(Path(value).suffix in ('.md', '.txt', '.json', '.html'), 'Tipo de documento inválido')
    key = lector.sha(value.encode())[:24]
    documents[key] = {'ruta': value, 'roots': roots}
    return {'id': key, 'ruta': value, 'disponible': (BASE / value).is_file()}


def target(source, local_id, name, original, source_hash, targets):
    key = lector.sha((source + '\n' + local_id).encode())
    revision_hash = lector.sha((source_hash + json.dumps(original, ensure_ascii=False, sort_keys=True)).encode())
    targets[key] = {'id': key, 'nombre': name, 'fuente': source, 'sha256_fuente': source_hash,
                    'huella_revision': revision_hash, 'original': original}
    return key


def load_export(value, documents, targets):
    roots = list(PRODUCERS.values())
    fixture_root = PANEL_ROOT + '/fixtures'
    synthetic = PurePosixPath(value).is_relative_to(PurePosixPath(fixture_root))
    raw = read_relative(value, roots)
    require(Path(value).name == 'estado-fabrica.json', 'Se espera estado-fabrica.json')
    data = json.loads(raw)
    require(isinstance(data, dict) and data.get('schema') == 'onia-fabrica-estado-v1', 'Schema de fábrica inválido')
    producer = data.get('fabrica')
    require(producer in PRODUCERS, 'Productor fuera del contrato')
    owner_roots = [fixture_root] if synthetic else [PRODUCERS[producer]]
    relative_path(value, owner_roots)
    identifier(data.get('id'))
    require(data.get('estado') in STATES, 'Estado descriptivo inválido')
    generated = datetime.fromisoformat(text(data.get('generado'), 60).replace('Z', '+00:00'))
    require(generated.utcoffset() is not None, 'Fecha sin zona horaria')
    source = document(data.get('fuente'), owner_roots, documents)
    steps, deliveries, pending = data.get('pasos'), data.get('entregables'), data.get('pendientes')
    require(all(isinstance(rows, list) and len(rows) <= 80 for rows in (steps, deliveries, pending)), 'Listas inválidas')
    seen = set()
    steps_view = []
    fingerprint = lector.sha(raw)
    for step in steps:
        require(isinstance(step, dict), 'Paso inválido')
        step_id = identifier(step.get('id'))
        require(step_id not in seen, 'Paso duplicado')
        seen.add(step_id)
        text(step.get('nombre'), 200)
        require(step.get('estado') in STATES, 'Estado de paso inválido')
        evidence = step.get('evidencias')
        require(isinstance(evidence, list) and len(evidence) <= 80, 'Evidencias inválidas')
        steps_view.append({**step, 'evidencias': [document(p, owner_roots, documents) for p in evidence],
                           'target': target(value, 'paso-' + step_id, step['nombre'], step, fingerprint, targets)})
    deliveries_view = []
    for delivery in deliveries:
        require(isinstance(delivery, dict), 'Entregable inválido')
        text(delivery.get('nombre'), 200)
        ref = document(delivery.get('ruta'), owner_roots, documents)
        original = dict(delivery)
        if ref['disponible']:
            raw_result = read_relative(delivery['ruta'], owner_roots)
            original.update(texto=raw_result.decode('utf-8'), sha256=lector.sha(raw_result))
        deliveries_view.append({**delivery, 'documento': ref,
                                'target': target(value, 'entrega-' + delivery['ruta'], delivery['nombre'], original, fingerprint, targets)})
    for row in pending:
        require(isinstance(row, dict), 'Pendiente inválido')
        for key in ('motivo', 'responsable', 'siguiente'):
            text(row.get(key), 2000)
    return {**data, 'pasos': steps_view, 'entregables': deliveries_view, 'documento_fuente': source,
            'ruta_export': value, 'sha256': fingerprint, 'sintetico': synthetic}


def build(exports=(), tanda_path=HISTORIC_TANDA):
    documents, targets = {}, {}
    result = {'generado': lector.now(), 'fabricas': [], 'exports_panel': [], 'errores': [],
              'documents': documents, 'targets': targets, 'tanda': None}
    loaded, seen_paths = {}, set()
    for position, value in enumerate(exports, 1):
        try:
            # Un export inválido no deja documentos o targets parcialmente autorizados.
            staged_documents, staged_targets = {}, {}
            data = load_export(value, staged_documents, staged_targets)
            require(value not in seen_paths, 'Ruta repetida en la lista explícita')
            seen_paths.add(value)
            loaded.setdefault(data['fabrica'], []).append(data)
            documents.update(staged_documents)
            targets.update(staged_targets)
        except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError):
            result['errores'].append(f'Export de la entrada {position} rechazado o ausente. Revisar la lista explícita de rutas y el contrato.')
    for key, name, root in FACTORIES:
        result['fabricas'].append({'id': key, 'nombre': name, 'exports': loaded.get(key, []),
                                  'documento': document(root + '/README.md', [root], documents)})
    if 'panel' in loaded:
        result['exports_panel'].extend(loaded['panel'])
    result['exports_estrategias'] = loaded.get('estrategias', [])
    result['decisiones'] = document(DECISIONS, [DECISIONS], documents)
    result['alcance'] = document(SCOPE, [SCOPE], documents)
    result['cerebro_doc'] = document(BRAIN_ROOT + '/README.md', [BRAIN_ROOT], documents)
    result['decisiones_sha256'] = lector.sha(read_relative(DECISIONS, [DECISIONS]))
    result['clases'] = [('Ordenar', '2026-11-13T20:00:00-04:00'),
                        ('Vender', '2026-11-14T14:00:00-04:00'),
                        ('Automatizar', '2026-11-16T20:00:00-04:00')]
    try:
        raw_package = read_relative(tanda_path, [PRODUCERS['guiones']])
        snapshot = tanda.snapshot(BASE / tanda_path)
        require(raw_package == read_relative(tanda_path, [PRODUCERS['guiones']]), 'Paquete cambió durante la lectura')
        package = json.loads(raw_package)
        snapshot['fecha_tanda'] = text(package.get('fecha_tanda'), 60)
        date.fromisoformat(snapshot['fecha_tanda'])
        source_hash = lector.sha(raw_package)
        batch_targets = {}
        for script in snapshot['guiones']:
            script['target'] = target(tanda_path, script['id'], script['id'] + ' · ' + script['titulo'], script.copy(), source_hash, batch_targets)
        targets.update(batch_targets)
        result['tanda'] = snapshot
        result['tanda_ruta'] = tanda_path
        result['tanda_historica'] = tanda_path == HISTORIC_TANDA
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError):
        result['errores'].append('Tanda ausente o inválida. Cotejar ruta, cinco IDs, texto, bytes y hashes de Markdown.')
    return result


def brain(topic='', use=''):
    spec = importlib.util.spec_from_file_location('cerebro_existente', BASE / BRAIN_ROOT / 'consultar.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    topics = [module.etiqueta(topic)] if topic else []
    uses = [module.etiqueta(use)] if use else []
    require(not uses or uses[0] in module.USOS, 'Uso del cerebro inválido')
    catalog = module.cargar(BASE / BRAIN_ROOT / 'catalogo.json')
    return module.consultar(catalog, topics, uses)


class Reviews:
    """Una fila por revisión y versión. El original queda en cada fila confirmada."""

    def __init__(self, directory):
        directory = Path(directory).absolute()
        require(not directory.resolve().is_relative_to(lector.REPO.resolve()), 'Datos de operación deben quedar fuera de Git')
        for path in (directory, *directory.parents):
            git_marker = path / '.git'
            require(not path.is_symlink() and not (git_marker.is_file() or (git_marker / 'HEAD').is_file()),
                    'Directorio de datos dentro de Git o enlazado')
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.path = directory / 'revisiones.sqlite3'
        require(not self.path.is_symlink(), 'Base de datos enlazada')
        require(not self.path.exists() or (self.path.is_file() and self.path.stat().st_nlink == 1), 'Archivo de datos inválido')
        fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600) if not self.path.exists() else None
        if fd is not None:
            os.close(fd)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('''CREATE TABLE IF NOT EXISTS revisiones (
                target TEXT NOT NULL, version INTEGER NOT NULL, fecha TEXT NOT NULL,
                motivo TEXT NOT NULL, correccion TEXT NOT NULL, estado TEXT NOT NULL CHECK(estado='pendiente'),
                fuente TEXT NOT NULL, sha256_fuente TEXT NOT NULL, original TEXT NOT NULL,
                PRIMARY KEY(target, version))''')
            columns = {row['name'] for row in db.execute('PRAGMA table_info(revisiones)')}
            for name, definition in (('solicitud_id', 'TEXT'), ('payload_sha', 'TEXT'),
                                     ('alcance', "TEXT NOT NULL DEFAULT 'pieza'")):
                if name not in columns:
                    db.execute(f'ALTER TABLE revisiones ADD COLUMN {name} {definition}')
            db.execute('CREATE UNIQUE INDEX IF NOT EXISTS revision_solicitud ON revisiones(solicitud_id)')

    @contextmanager
    def connect(self):
        require(not self.path.is_symlink(), 'Base de datos enlazada')
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def history(self, target_id=None):
        with self.connect() as db:
            if target_id is None:
                rows = db.execute('SELECT * FROM revisiones ORDER BY target, version').fetchall()
            else:
                rows = db.execute('SELECT * FROM revisiones WHERE target=? ORDER BY version', (target_id,)).fetchall()
        return [dict(row) for row in rows]

    def retry(self, request_id, payload_sha):
        with self.connect() as db:
            row = db.execute('SELECT * FROM revisiones WHERE solicitud_id=?', (request_id,)).fetchone()
        if row:
            require(row['payload_sha'] == payload_sha, 'El identificador ya se usó con otra propuesta')
            return dict(row)

    def append(self, item, expected, motive, correction, request_id=None, payload_sha=None, scope='pieza'):
        text(motive, 2000)
        text(correction, 12000)
        require(type(expected) is int and expected >= 0, 'Versión inválida')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if request_id:
                saved = db.execute('SELECT * FROM revisiones WHERE solicitud_id=?', (request_id,)).fetchone()
                if saved:
                    require(saved['payload_sha'] == payload_sha, 'Identificador reutilizado con otros datos')
                    return saved['version']
            current = db.execute('SELECT COALESCE(MAX(version),0) FROM revisiones WHERE target=?', (item['id'],)).fetchone()[0]
            require(current == expected, 'La revisión cambió. Recargar antes de guardar.')
            db.execute('''INSERT INTO revisiones
                       (target,version,fecha,motivo,correccion,estado,fuente,sha256_fuente,original,
                        solicitud_id,payload_sha,alcance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                       (item['id'], current + 1, lector.now(), motive, correction, 'pendiente',
                        item['fuente'], item['sha256_fuente'], json.dumps(item['original'], ensure_ascii=False),
                        request_id, payload_sha, scope))
        return current + 1
