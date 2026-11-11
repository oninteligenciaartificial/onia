"""Modo temporal en loopback del panel existente. Datos locales fuera de Git."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import secrets
import sqlite3
from urllib.parse import parse_qs, urlsplit

import lector
import operacion
import panel


class Application:
    def __init__(self, data_directory, exports=(), tanda_path=operacion.HISTORIC_TANDA):
        self.reviews = operacion.Reviews(data_directory)
        self.exports = tuple(exports)
        self.tanda_path = tanda_path
        self.csrf = secrets.token_urlsafe(32)

    def model(self):
        model = operacion.build(self.exports, self.tanda_path)
        model['histories'] = {}
        model['revisiones_anteriores'] = []
        for row in self.reviews.history():
            if row['target'] in model['targets']:
                model['histories'].setdefault(row['target'], []).append(row)
            else:
                model['revisiones_anteriores'].append(row)
        return model

    def html(self, query=None):
        query = query or {}
        model = self.model()
        if 'tema' in query or 'uso' in query:
            try:
                model['brain'] = operacion.brain(query.get('tema', [''])[0], query.get('uso', [''])[0])
            except (OSError, ValueError, TypeError, KeyError, argparse.ArgumentTypeError):
                model['errores'].append('Consulta del cerebro inválida o integridad pendiente. Revisar etiquetas y fuentes.')
        model['guardado'] = query.get('guardado') == ['1']
        snapshot = model['tanda'] or {'schema': 'onia-lector-panel-v1', 'generado': model['generado'],
                                    'alcance': 'Tanda pendiente de reconciliar.', 'commit_entradas_repo': 'Sin anclar'}
        return panel.render(snapshot, model, {'csrf': self.csrf})

    def save(self, fields):
        operacion.require(set(fields) == {'csrf', 'target', 'source_hash', 'version', 'motivo', 'correccion'}
                          and all(len(value) == 1 for value in fields.values()), 'Campos inválidos')
        values = {key: value[0] for key, value in fields.items()}
        operacion.require(secrets.compare_digest(values['csrf'], self.csrf), 'Sesión inválida. Recargar.')
        model = self.model()
        operacion.require(values['target'] in model['targets'], 'Resultado desconocido')
        item = model['targets'][values['target']]
        operacion.require(values['source_hash'] == item['huella_revision'], 'La fuente cambió. Recargar antes de guardar.')
        operacion.require(values['version'].isdigit() and len(values['version']) <= 8, 'Versión inválida')
        self.reviews.append(item, int(values['version']), values['motivo'], values['correccion'])
        return values['target']


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'OnIA-local'

        def log_message(self, *_):
            # Los textos, rutas y datos de las revisiones quedan fuera de logs HTTP.
            pass

        def send(self, status, body, content_type='text/html; charset=utf-8', location=None):
            payload = body.encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
            if location:
                self.send_header('Location', location)
            self.end_headers()
            self.wfile.write(payload)

        def local_request(self):
            return self.headers.get('Host') == f'127.0.0.1:{self.server.server_port}'

        def do_GET(self):
            if not self.local_request():
                return self.send(403, 'Host local inválido')
            try:
                route = urlsplit(self.path)
                operacion.require(not route.scheme and not route.netloc, 'Ruta inválida')
                query = parse_qs(route.query, keep_blank_values=True, max_num_fields=8, errors='strict')
                if route.path == '/':
                    operacion.require(set(query) <= {'tema', 'uso', 'guardado'} and all(len(v) == 1 for v in query.values()), 'Consulta inválida')
                    return self.send(200, app.html(query))
                if route.path == '/documento':
                    operacion.require(set(query) == {'id'} and len(query['id']) == 1, 'Documento inválido')
                    docs = app.model()['documents']
                    operacion.require(query['id'][0] in docs, 'Documento fuera de la lista explícita')
                    doc = docs[query['id'][0]]
                    raw = operacion.read_relative(doc['ruta'], doc['roots'])
                    body = f'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
                    <title>Evidencia local</title><style>body{{font:16px/1.6 system-ui;max-width:1000px;margin:24px auto;padding:18px;overflow-wrap:anywhere}}pre{{white-space:pre-wrap}}</style>
                    <a href="/">Volver al panel</a><h1>Evidencia local</h1><p>{panel.e(doc['ruta'])}</p>
                    <p>Lectura local {panel.e(lector.now())}<br>SHA-256 {lector.sha(raw)}</p><pre>{panel.e(raw.decode('utf-8'))}</pre></html>'''
                    return self.send(200, body)
                return self.send(404, 'Ruta desconocida')
            except (OSError, ValueError, TypeError, KeyError, UnicodeError):
                return self.send(400, '<p>Entrada o documento inválido. Revisar la ruta permitida y su disponibilidad.</p><a href="/">Volver al panel</a>')

        def do_POST(self):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if not self.local_request() or self.headers.get('Origin') != origin:
                return self.send(403, 'Origen local inválido')
            if self.path != '/revision':
                return self.send(404, 'Ruta desconocida')
            fields = {}
            try:
                operacion.require(self.headers.get('Content-Type', '').split(';')[0] == 'application/x-www-form-urlencoded', 'Tipo de formulario inválido')
                operacion.require(not self.headers.get('Transfer-Encoding'), 'Codificación inválida')
                length = self.headers.get('Content-Length', '')
                operacion.require(length.isdigit() and 0 < int(length) <= 192 * 1024, 'Tamaño de formulario inválido')
                self.connection.settimeout(5)
                raw = self.rfile.read(int(length))
                operacion.require(len(raw) == int(length), 'Formulario incompleto')
                fields = parse_qs(raw.decode('utf-8'), keep_blank_values=True, strict_parsing=True, max_num_fields=6, errors='strict')
                target_id = app.save(fields)
                return self.send(303, '', location='/?guardado=1#revision-' + target_id)
            except (OSError, ValueError, TypeError, KeyError, UnicodeError, sqlite3.Error):
                # Preservar lo escrito permite resolver un conflicto sin perder la propuesta.
                draft = '\n'.join(fields.get('motivo', []) + fields.get('correccion', []))
                return self.send(409, '<p>Revisión sin guardar. La fuente, versión o entrada requiere conciliación. Recargá el resultado antes de reintentar.</p>'
                                 + '<pre>' + panel.e(draft) + '</pre><a href="/">Volver al panel</a>')

    return Handler


def preview(app, output):
    output = lector.own_output(output)
    output.mkdir(exist_ok=False)
    model = operacion.build(app.exports, app.tanda_path)
    model['brain'] = operacion.brain('revision', '')
    # El preview conserva links relativos a documentos del mismo checkout.
    for doc in model['documents'].values():
        doc['href'] = os.path.relpath(lector.BASE / doc['ruta'], output)
    def attach_links(value):
        if isinstance(value, dict):
            if 'id' in value and 'ruta' in value and value['id'] in model['documents']:
                value['href'] = model['documents'][value['id']]['href']
                if lector.BASE / value['ruta'] == output / 'panel.html':
                    value['disponible'] = True
            for child in value.values():
                attach_links(child)
        elif isinstance(value, list):
            for child in value:
                attach_links(child)
    attach_links(model)
    snapshot = model['tanda'] or {'schema': 'onia-lector-panel-v1', 'generado': model['generado'],
                                'alcance': 'Tanda pendiente', 'commit_entradas_repo': 'Sin anclar'}
    lector.write_new(output / 'panel.html', panel.render(snapshot, model))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, required=True, help='Directorio privado fuera de cualquier repositorio Git')
    parser.add_argument('--estado', action='append', default=[], help='Ruta relativa a base-operativa, repetible')
    parser.add_argument('--tanda', default=operacion.HISTORIC_TANDA, help='Paquete editorial relativo a base-operativa')
    parser.add_argument('--puerto', type=int, default=8765)
    parser.add_argument('--preview', type=Path, help='HTML estático en un directorio nuevo dentro de la ruta asignada')
    args = parser.parse_args()
    try:
        app = Application(args.datos, args.estado, args.tanda)
        if args.preview:
            preview(app, args.preview)
            print('Preview HTML generado. Revisiones locales en el directorio privado indicado.')
            return 0
        server = HTTPServer(('127.0.0.1', args.puerto), handler_for(app))
        server.timeout = 5
        print(f'Panel local http://127.0.0.1:{server.server_port} · detener con Ctrl+C', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return 0
    except (OSError, ValueError, sqlite3.Error):
        print('No se pudo iniciar. Verificar datos fuera de Git, rutas permitidas y puerto local.')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
