"""Modo temporal en loopback del panel existente. Datos locales fuera de Git."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import secrets
import sqlite3
import json
import re
from urllib.parse import parse_qs, urlsplit

import lector
import diario
import operacion
import panel
import cerebro
import correcciones
import acceso
import entregas


class Application:
    def __init__(self, data_directory, exports=(), tanda_path=operacion.HISTORIC_TANDA, flujo_path=None, access_path=None):
        self.reviews = operacion.Reviews(data_directory)
        self.corrections = correcciones.Corrections(self.reviews)
        self.access = acceso.Access(access_path) if access_path else None
        self.exports = tuple(exports)
        self.tanda_path = tanda_path
        self.csrf = secrets.token_urlsafe(32)
        self.flujo_path = flujo_path
        self.last_daily = None
        self.daily_stale = False

    def daily(self):
        if not self.flujo_path:
            return None
        try:
            current = diario.read(self.flujo_path)
            # Render antes de adoptar: un export mal formado conserva el anterior.
            diario.fragment(current)
            self.last_daily, self.daily_stale = current, False
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            self.daily_stale = True
        return self.last_daily

    def model(self):
        model = operacion.build(self.exports, self.tanda_path)
        daily = self.daily()
        if daily:
            diario.attach(model, daily)
        model['daily_stale'] = self.daily_stale
        if self.access:
            model['entregas'] = entregas.available(self.reviews.path.parent)
        cerebro.attach(model)
        self.corrections.attach(model)
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
        if 'objetivo' in query:
            selected = query['objetivo'][0]
            operacion.require(selected in model['targets'], 'Objetivo de corrección desconocido')
            model['correction_target'] = selected
        if 'tema' in query or 'uso' in query:
            try:
                model['brain'] = operacion.brain(query.get('tema', [''])[0], query.get('uso', [''])[0])
            except (OSError, ValueError, TypeError, KeyError, argparse.ArgumentTypeError):
                model['errores'].append('Consulta del cerebro inválida o integridad pendiente. Revisar etiquetas y fuentes.')
        model['guardado'] = query.get('guardado') == ['1']
        snapshot = model['tanda'] or {'schema': 'onia-lector-panel-v1', 'generado': model['generado'],
                                    'alcance': 'Tanda pendiente de reconciliar.', 'commit_entradas_repo': 'Sin anclar'}
        return panel.render(snapshot, model, {'csrf': self.csrf, 'correcciones_v2': True,
                                             'daily_script_hash': diario.script_hash() if self.flujo_path else None})

    def save(self, fields):
        required = {'csrf', 'target', 'source_hash', 'version', 'motivo', 'correccion'}
        operacion.require(required <= set(fields) <= required | {'alcance','solicitud_id'}
                          and all(len(value) == 1 for value in fields.values()), 'Campos inválidos')
        values = {key: value[0] for key, value in fields.items()}
        operacion.require(secrets.compare_digest(values['csrf'], self.csrf), 'Sesión inválida. Recargar.')
        scope = values.get('alcance', 'pieza')
        operacion.require(scope in correcciones.SCOPES, 'Alcance inválido')
        request_id = values.get('solicitud_id')
        payload_sha = lector.sha(json.dumps({k:v for k,v in values.items() if k != 'csrf'}, sort_keys=True).encode())
        if request_id:
            operacion.require(re.fullmatch(r'[a-f0-9]{64}', request_id), 'Identificador inválido')
            existing = self.reviews.retry(request_id, payload_sha)
            if existing:
                return existing['target']
        model = self.model()
        operacion.require(values['target'] in model['targets'], 'Resultado desconocido')
        item = model['targets'][values['target']]
        operacion.require(values['source_hash'] == item['huella_revision'], 'La fuente cambió. Recargar antes de guardar.')
        operacion.require(values['version'].isdigit() and len(values['version']) <= 8, 'Versión inválida')
        self.reviews.append(item, int(values['version']), values['motivo'], values['correccion'], request_id, payload_sha, scope)
        return values['target']

    def action(self, route, fields):
        operacion.require(set(fields) == {'csrf','target','source_hash','version'} and all(len(v)==1 for v in fields.values()), 'Acción inválida')
        values = {key:value[0] for key,value in fields.items()}
        operacion.require(secrets.compare_digest(values['csrf'], self.csrf), 'Sesión inválida')
        operacion.require(values['version'].isdigit() and len(values['version']) <= 8, 'Versión inválida')
        model = self.model()
        operacion.require(values['target'] in model['targets'], 'Objetivo ausente')
        item = model['targets'][values['target']]
        operacion.require(values['source_hash'] == item['huella_revision'], 'La fuente cambió. Recargar')
        revision = int(values['version'])
        if route == '/aplicar':
            row = self.corrections.apply(item, revision)
            return '/version?id=' + row['id']
        request_id = self.corrections.request(item, revision)
        return '/solicitud?id=' + request_id


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
            self.send_header('Referrer-Policy', 'same-origin')
            if status == 401:
                self.send_header('WWW-Authenticate', 'Basic realm="ONIA privado", charset="UTF-8"')
            script_policy = ("; script-src 'sha256-" + diario.script_hash() + "'; connect-src 'self'") if app.flujo_path else ''
            self.send_header('Content-Security-Policy', "default-src 'none'; img-src 'self' data:; font-src data:; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'" + script_policy)
            if location:
                self.send_header('Location', location)
            self.end_headers()
            self.wfile.write(payload)

        def local_request(self):
            expected = app.access.host if app.access else f'127.0.0.1:{self.server.server_port}'
            return self.headers.get_all('Host') == [expected]

        def authenticated(self):
            return not app.access or app.access.authenticated(self.headers.get('Authorization'))

        def delivery(self, query):
            if not app.access:
                return self.send(403, 'Entrega disponible con acceso privado configurado')
            if set(query) != {'id'} or len(query['id']) != 1 or query['id'][0] not in entregas.FILES:
                return self.send(404, 'Entrega desconocida')
            key = query['id'][0]
            try:
                with entregas.opened(app.reviews.path.parent, key) as (source, size, name, mime):
                    if mime == 'text/plain':
                        raw = source.read(size + 1)
                        operacion.require(len(raw) == size, 'Entrega cambió')
                        title = 'Ensayo de WhatsApp' if key == 'whatsapp-demo' else 'Tanda manual del 12 nov'
                        scope = ('Datos ficticios. Despacho y envíos desactivados.' if key == 'whatsapp-demo'
                                 else 'Tanda manual. Borradores para revisión editorial.')
                        body = ('<!doctype html><html lang="es"><meta charset="utf-8">'
                                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                                f'<title>{title}</title><style>body{{font:16px/1.6 system-ui;max-width:850px;'
                                'margin:20px auto;padding:16px}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>'
                                f'<a href="/#hoy">Volver a entregables</a><h1>{title}</h1>'
                                f'<p>{scope}</p><pre>'
                                + panel.e(raw.decode('utf-8')) + '</pre></html>')
                        return self.send(200, body)
                    return self.delivery_file(source, size, name, mime)
            except (OSError, ValueError, RecursionError):
                return self.send(404, 'Entrega no disponible')

        def delivery_file(self, source, size, name, mime):
            media = mime == 'video/mp4'
            requested = self.headers.get_all('Range')
            partial = media and requested is not None
            start, end = 0, size - 1
            if partial:
                try:
                    if len(requested) != 1:
                        raise ValueError('Se admite un rango')
                    start, end = entregas.byte_range(requested[0], size)
                except ValueError:
                    self.send_response(416)
                    self.send_header('Content-Range', f'bytes */{size}')
                    self.send_header('Cache-Control', 'no-store')
                    self.send_header('Content-Length', '0')
                    self.end_headers()
                    return
            remaining = end - start + 1
            try:
                self.connection.settimeout(10)
                self.send_response(206 if partial else 200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Length', str(remaining))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('X-Content-Type-Options', 'nosniff')
                media_policy = "; media-src 'self'" if media else ''
                self.send_header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'" + media_policy)
                self.send_header('Content-Disposition', f'{"inline" if media else "attachment"}; filename="{name}"')
                if media:
                    self.send_header('Accept-Ranges', 'bytes')
                if partial:
                    self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.end_headers()
                source.seek(start)
                while remaining:
                    chunk = source.read(min(remaining, 64 * 1024))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
            except OSError:
                self.close_connection = True

        def do_GET(self):
            if not self.local_request():
                return self.send(403, 'Host local inválido')
            if not self.authenticated():
                return self.send(401, 'Autenticación privada requerida')
            try:
                route = urlsplit(self.path)
                operacion.require(not route.scheme and not route.netloc, 'Ruta inválida')
                query = parse_qs(route.query, keep_blank_values=True, max_num_fields=8, errors='strict')
                if route.path == '/entrega':
                    return self.delivery(query)
                if route.path in ('/version','/solicitud'):
                    operacion.require(set(query) == {'id'} and len(query['id']) == 1, 'Identificador inválido')
                    if route.path == '/solicitud':
                        return self.send(200, app.corrections.exported(query['id'][0]), 'application/json; charset=utf-8')
                    row = next((r for r in app.corrections.versions() if r['id'] == query['id'][0]), None)
                    operacion.require(row is not None, 'Versión ausente')
                    body = '<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Versión local pendiente</title>'
                    body += '<style>body{font:16px/1.6 system-ui;max-width:900px;margin:20px auto;padding:16px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style><a href="/#correcciones">Volver a correcciones</a>'
                    body += '<h1>Versión local · pendiente de revisión</h1><p>' + panel.e(row['id']) + '</p><p>' + panel.e(row['fecha']) + ' · SHA-256 ' + row['sha256'] + '</p>'
                    body += '<h2>Propuesta aplicada localmente</h2><pre>' + panel.e(row['texto']) + '</pre><details><summary>Original conservado</summary><pre>' + panel.e(row['antes']) + '</pre></details></html>'
                    return self.send(200, body)
                if route.path == '/flujo' and not query and app.flujo_path:
                    data = app.daily()
                    if data is None:
                        return self.send(503, 'Ciclo pendiente; productor sin proyección válida')
                    return self.send(200, diario.fragment(data, app.daily_stale))
                if route.path == '/favicon.ico' and not query:
                    return self.send(204, '')
                if route.path == '/':
                    operacion.require(set(query) <= {'tema', 'uso', 'guardado', 'objetivo'} and all(len(v) == 1 for v in query.values()), 'Consulta inválida')
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
            origin = app.access.origin if app.access else f'http://127.0.0.1:{self.server.server_port}'
            if not self.local_request() or self.headers.get_all('Origin') != [origin]:
                return self.send(403, 'Origen local inválido')
            if not self.authenticated():
                return self.send(401, 'Autenticación privada requerida')
            if self.path not in ('/revision','/aplicar','/solicitar'):
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
                fields = parse_qs(raw.decode('utf-8'), keep_blank_values=True, strict_parsing=True, max_num_fields=8, errors='strict')
                if self.path != '/revision':
                    return self.send(303, '', location=app.action(self.path, fields))
                target_id = app.save(fields)
                return self.send(303, '', location='/?guardado=1&objetivo=' + target_id + '#correcciones')
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
    cerebro.attach(model)
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
    parser.add_argument('--flujo', type=Path, help='panel.json saneado del ciclo, privado y fuera de Git')
    parser.add_argument('--acceso', type=Path, help='Configuración privada de origen HTTPS y autenticación, fuera de Git')
    parser.add_argument('--puerto', type=int, default=8765)
    parser.add_argument('--preview', type=Path, help='HTML estático en un directorio nuevo dentro de la ruta asignada')
    args = parser.parse_args()
    try:
        app = Application(args.datos, args.estado, args.tanda, args.flujo, args.acceso)
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
