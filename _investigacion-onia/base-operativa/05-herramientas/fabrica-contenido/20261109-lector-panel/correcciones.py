"""Versiones y solicitudes privadas. Operaciones fijas, transaccionales y append-only."""
import json

import lector
from operacion import require, target, text

SCOPES = ('pieza', 'seccion', 'canonico', 'llm')


class Corrections:
    def __init__(self, reviews):
        self.reviews = reviews
        with reviews.connect() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS versiones_locales (
                id TEXT PRIMARY KEY, target TEXT NOT NULL, revision INTEGER NOT NULL,
                version INTEGER NOT NULL, fecha TEXT NOT NULL, antes TEXT NOT NULL,
                texto TEXT NOT NULL, sha256 TEXT NOT NULL, motivo TEXT NOT NULL,
                UNIQUE(target,revision))''')
            db.execute('''CREATE TABLE IF NOT EXISTS solicitudes_coordinacion (
                id TEXT PRIMARY KEY, target TEXT NOT NULL, revision INTEGER NOT NULL,
                contenido TEXT NOT NULL, UNIQUE(target,revision))''')

    def versions(self):
        with self.reviews.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM versiones_locales ORDER BY fecha,id')]

    def attach(self, model):
        model['versiones_locales'] = self.versions()
        for row in model['versiones_locales']:
            original = {'id': row['id'], 'version': row['version'], 'texto': row['texto'],
                        'sha256': row['sha256'], 'estado': 'pendiente_revision', 'revision_origen': row['revision']}
            key = target('version-local/' + row['id'], row['id'], 'Versión local ' + row['id'],
                         original, row['sha256'], model['targets'])
            model['targets'][key]['editable_local'] = True
            row['target_local'] = key
        model['aplicaciones'] = {(row['target'], row['revision']): row for row in model['versiones_locales']}
        with self.reviews.connect() as db:
            model['solicitudes'] = [dict(row) for row in db.execute('SELECT * FROM solicitudes_coordinacion ORDER BY id')]

    def apply(self, item, revision):
        require(item.get('editable_local') is True, 'Este objetivo requiere coordinación')
        with self.reviews.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT * FROM versiones_locales WHERE target=? AND revision=?', (item['id'], revision)).fetchone()
            if existing:
                return dict(existing)
            row = db.execute('SELECT * FROM revisiones WHERE target=? AND version=?', (item['id'], revision)).fetchone()
            require(row is not None and row['alcance'] == 'pieza', 'Revisión local de pieza requerida')
            latest = db.execute('SELECT MAX(version) FROM revisiones WHERE target=?', (item['id'],)).fetchone()[0]
            require(latest == revision, 'Hay una observación posterior. Recargar antes de aplicar')
            original = json.loads(row['original'])
            require(original == item['original'] and row['sha256_fuente'] == item['sha256_fuente'], 'La fuente cambió')
            before = original.get('texto')
            text(before, 512 * 1024)
            text(row['correccion'], 12000)
            number = db.execute('SELECT COALESCE(MAX(version),0)+1 FROM versiones_locales WHERE target=?', (item['id'],)).fetchone()[0]
            version_id = 'local-' + lector.sha((item['id'] + '/' + str(revision)).encode())[:24]
            db.execute('INSERT INTO versiones_locales VALUES (?,?,?,?,?,?,?,?,?)',
                       (version_id, item['id'], revision, number, lector.now(), before,
                        row['correccion'], lector.sha(row['correccion'].encode()), row['motivo']))
            return dict(db.execute('SELECT * FROM versiones_locales WHERE id=?', (version_id,)).fetchone())

    def request(self, item, revision):
        with self.reviews.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT * FROM solicitudes_coordinacion WHERE target=? AND revision=?', (item['id'], revision)).fetchone()
            if existing:
                return existing['id']
            row = db.execute('SELECT * FROM revisiones WHERE target=? AND version=?', (item['id'], revision)).fetchone()
            require(row is not None, 'Observación ausente')
            request_id = 'sol-' + lector.sha((item['id'] + '/' + str(revision)).encode())[:24]
            original = json.loads(row['original'])
            dependencies = list(original.get('fuentes') or [row['fuente']])
            if row['alcance'] == 'canonico':
                dependencies.append('05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md')
            value = {'schema': 'onia-solicitud-correccion-v1', 'id': request_id,
                     'objetivo': item['nombre'], 'target': item['id'], 'version_observacion': revision,
                     'fuente': row['fuente'], 'sha256_fuente': row['sha256_fuente'],
                     'original': original, 'motivo': row['motivo'],
                     'propuesta': row['correccion'], 'alcance': row['alcance'],
                     'dependencias': dependencies, 'estado': 'pendiente_coordinacion', 'generado': lector.now()}
            db.execute('INSERT INTO solicitudes_coordinacion VALUES (?,?,?,?)',
                       (request_id, item['id'], revision, json.dumps(value, ensure_ascii=False)))
            return request_id

    def exported(self, request_id):
        with self.reviews.connect() as db:
            row = db.execute('SELECT contenido FROM solicitudes_coordinacion WHERE id=?', (request_id,)).fetchone()
        require(row is not None, 'Solicitud desconocida')
        return row['contenido']
