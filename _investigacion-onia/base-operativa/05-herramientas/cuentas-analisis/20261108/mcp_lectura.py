"""Filtro de herramientas y destinos para el perfil de análisis autenticado."""
import json
import os
import re
import select
import selectors
import stat
import sys
import time
from urllib.parse import urlsplit

TOOLS = frozenset(('browser_navigate', 'browser_snapshot', 'browser_close'))
PROTOCOL = frozenset(('initialize', 'notifications/initialized', 'ping', 'tools/list',
                      'notifications/cancelled'))
FRAME_LIMIT = 2 * 1024 * 1024


def load_urls(path):
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), 'r') as src:
        info = os.fstat(src.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise RuntimeError('La lista de URLs debe ser un archivo propio y privado.')
        if info.st_size > 65536:
            raise RuntimeError('La lista de URLs es demasiado larga.')
        urls = frozenset(line.strip() for line in src if line.strip())
    if not urls:
        raise RuntimeError('La lista de URLs aprobadas está vacía.')
    for url in urls:
        parts = urlsplit(url)
        if (parts.scheme != 'https' or not parts.hostname or parts.netloc != parts.hostname
                or not parts.path.startswith('/') or parts.query or parts.fragment
                or not re.fullmatch(r'https://[^\s?#]+', url)):
            raise RuntimeError('Cada destino aprobado debe ser una URL HTTPS exacta sin query ni fragmento.')
    return urls


def write_message(stream, message, interrupted):
    fd = stream.fileno()
    data = memoryview((json.dumps(message) + '\n').encode())
    deadline = time.monotonic() + 10
    while data and not interrupted():
        if time.monotonic() >= deadline:
            raise RuntimeError('El destino dejó de leer el canal MCP.')
        if not select.select([], [fd], [], .1)[1]:
            continue
        try:
            data = data[os.write(fd, data):]
        except BlockingIOError:
            continue


def refused(request_id, reason):
    return {'jsonrpc': '2.0', 'id': request_id,
            'error': {'code': -32602, 'message': reason}}


def success(request_id, text):
    return {'jsonrpc': '2.0', 'id': request_id,
            'result': {'content': [{'type': 'text', 'text': text}]}}


class Reader:
    def __init__(self, urls):
        self.urls = urls
        self.pending = {}
        self.page = None

    def request(self, message):
        """Devuelve (solicitud al MCP, respuesta al cliente), una u otra."""
        if not isinstance(message, dict) or message.get('jsonrpc') != '2.0':
            return None, refused(None, 'Se espera un mensaje JSON-RPC individual.')
        method = message.get('method')
        request_id = message.get('id')
        if not isinstance(method, str) or (request_id is not None and type(request_id) not in (str, int)):
            return None, refused(None, 'Solicitud MCP inválida.')
        if request_id in self.pending:
            return None, refused(None, 'Identificador MCP duplicado.')
        if method in PROTOCOL:
            if method == 'tools/list' and request_id is not None:
                self.pending[request_id] = ('tools/list', None)
            return message, None
        if method != 'tools/call' or request_id is None:
            return None, refused(request_id, 'Método MCP fuera de alcance.')
        if any(name in TOOLS for name, _ in self.pending.values()):
            return None, refused(request_id, 'Esperar el resultado de la herramienta anterior.')
        params = message.get('params')
        if not isinstance(params, dict) or set(params) - {'name', 'arguments', '_meta'}:
            return None, refused(request_id, 'Parámetros de herramienta inválidos.')
        name = params.get('name')
        args = params.get('arguments', {})
        if not isinstance(name, str) or name not in TOOLS or not isinstance(args, dict):
            return None, refused(request_id, 'Herramienta fuera de alcance.')
        target = None
        if name == 'browser_navigate':
            self.page = None
            target = args.get('url')
            if set(args) != {'url'} or not isinstance(target, str) or target not in self.urls:
                return None, refused(request_id, 'URL fuera de la lista aprobada.')
        elif args:
            return None, refused(request_id, 'La herramienta no admite argumentos en este perfil.')
        elif name == 'browser_snapshot':
            target = self.page
            if target is None:
                return None, refused(request_id, 'Navegar primero a un destino aprobado.')
        else:
            self.page = None
        self.pending[request_id] = (name, target)
        return message, None

    def response(self, message):
        # El MCP sin roots ni WebMCP no necesita enviar solicitudes al cliente.
        if not isinstance(message, dict) or 'method' in message:
            return None
        request_id = message.get('id')
        name, target = self.pending.pop(request_id, (None, None))
        result = message.get('result', {})
        if name == 'tools/list' and isinstance(result.get('tools'), list):
            result['tools'] = [tool for tool in result['tools'] if tool.get('name') in TOOLS]
            result.pop('nextCursor', None)
        if name in TOOLS and ('error' in message or result.get('isError')):
            self.page = None
            return refused(request_id, 'Playwright no completó la operación de lectura.')
        if name == 'browser_close':
            return success(request_id, 'Navegador de análisis cerrado.')
        if name in ('browser_navigate', 'browser_snapshot'):
            text = '\n'.join(item['text'] for item in result.get('content', [])
                             if item.get('type') == 'text')
            header = text.split('### Snapshot', 1)[0]
            urls = re.findall(r'^- Page URL: (\S+)$', header, re.MULTILINE)
            if urls != [target]:
                self.page = None
                return refused(request_id, 'La página abierta no coincide con el destino aprobado.')
            self.page = target
            if name == 'browser_navigate':
                return success(request_id, 'Destino aprobado abierto.')
            # Evita reenviar títulos y direcciones de otras pestañas.
            return success(request_id, text.partition('### Snapshot\n')[2])
        return message


def relay(child, urls, interrupted):
    reader = Reader(urls)
    buffers = {name: bytearray() for name in ('client', 'server')}
    deadline = None
    os.set_blocking(child.stdin.fileno(), False)
    os.set_blocking(sys.stdout.fileno(), False)
    with selectors.SelectSelector() as selector:
        selector.register(sys.stdin.buffer, selectors.EVENT_READ, 'client')
        selector.register(child.stdout, selectors.EVENT_READ, 'server')
        while not interrupted() and (deadline is None or time.monotonic() < deadline):
            ready = selector.select(.1)
            if not ready and child.poll() is not None:
                return
            for key, _ in ready:
                origin = key.data
                chunk = os.read(key.fd, 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    if origin == 'server':
                        return
                    child.stdin.close()
                    deadline = time.monotonic() + 16
                    continue
                buffer = buffers[origin]
                buffer.extend(chunk)
                if len(buffer) > FRAME_LIMIT:
                    raise RuntimeError('Mensaje MCP demasiado grande.')
                while (end := buffer.find(b'\n')) >= 0:
                    line = bytes(buffer[:end])
                    del buffer[:end + 1]
                    message = json.loads(line)
                    if origin == 'client':
                        request, response = reader.request(message)
                        if request is not None:
                            write_message(child.stdin, request, interrupted)
                    else:
                        response = reader.response(message)
                    if response is not None:
                        write_message(sys.stdout.buffer, response, interrupted)
