"""Ensayo sintético reproducible con dos procesos reales del servidor temporal."""
import hashlib
import http.client
import json
from pathlib import Path
import re
import select
import signal
import sqlite3
import subprocess
import sys
import tempfile
from urllib.parse import urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import lector
import operacion
from test_operacion import Forms


def start(data):
    process = subprocess.Popen(
        [sys.executable, '-B', str(ROOT / 'servidor.py'), '--datos', data, '--puerto', '0'],
        cwd=lector.REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert select.select([process.stdout], [], [], 15)[0], 'Servidor sin URL en 15 segundos'
        match = re.search(r'http://127.0.0.1:\d+', process.stdout.readline())
        assert match, 'Servidor sin URL local'
        return process, match[0]
    except BaseException:
        stop(process)
        raise


def stop(process):
    process.send_signal(signal.SIGINT)
    try:
        process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        raise


def request(url, path='/', method='GET', fields=None):
    connection = http.client.HTTPConnection('127.0.0.1', urlsplit(url).port, timeout=15)
    headers = {'Origin': url, 'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        connection.request(method, path, urlencode(fields) if fields else None, headers)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read().decode()
    finally:
        connection.close()


def run(data):
    original = hashlib.sha256((lector.BASE / operacion.HISTORIC_TANDA).read_bytes()).hexdigest()
    process, url = start(data)
    try:
        status, _, html = request(url)
        assert status == 200 and 'Codex escribe' in html
        fields = Forms(html).forms[0]
        fields.update(motivo='ENSAYO SINTÉTICO de persistencia del código corregido',
                      correccion='ENSAYO SINTÉTICO de versión privada nueva.', alcance='pieza')
        for _ in range(2):
            assert request(url, '/revision', 'POST', fields)[0] == 303
        action = {key: fields[key] for key in ('csrf', 'target', 'source_hash')}
        action['version'] = '1'
        status, headers, _ = request(url, '/aplicar', 'POST', action)
        assert status == 303
        version_url = headers['Location']
        assert request(url, '/aplicar', 'POST', action)[1]['Location'] == version_url
        assert 'Original conservado' in request(url, version_url)[2]
    finally:
        stop(process)

    process, url = start(data)
    try:
        status, _, html = request(url, version_url)
        assert status == 200 and fields['correccion'] in html
        target = lector.sha(b'panel/seccion/calendario\ncalendario')
        status, _, html = request(url, '/?objetivo=' + target)
        assert status == 200
        fields = Forms(html).forms[-1]
        fields.update(motivo='ENSAYO SINTÉTICO de decisión pendiente',
                      correccion='Propuesta de revisión del calendario.', alcance='canonico')
        assert request(url, '/revision', 'POST', fields)[0] == 303
        action = {key: fields[key] for key in ('csrf', 'target', 'source_hash')}
        action['version'] = '1'
        assert request(url, '/aplicar', 'POST', action)[0] == 409
        status, headers, _ = request(url, '/solicitar', 'POST', action)
        assert status == 303
        assert request(url, '/solicitar', 'POST', action)[1]['Location'] == headers['Location']
        payload = json.loads(request(url, headers['Location'])[2])
        assert payload['estado'] == 'pendiente_coordinacion'
        assert operacion.DECISIONS in payload['dependencias']
        with sqlite3.connect(Path(data) / 'revisiones.sqlite3') as db:
            counts = [db.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0]
                      for table in ('revisiones', 'versiones_locales', 'solicitudes_coordinacion')]
        assert counts == [2, 1, 1], counts
        assert hashlib.sha256((lector.BASE / operacion.HISTORIC_TANDA).read_bytes()).hexdigest() == original
        return {'resultado': 'OK', 'ensayo': 'SINTÉTICO sobre guion histórico y decisión propuesta',
                'procesos': 2, 'reinicio_persistencia': True,
                'revisiones': counts[0], 'versiones_locales': counts[1], 'solicitudes': counts[2],
                'reintentos_idempotentes': True, 'original_conservado': True,
                'servidores_cerrados': True, 'datos': 'SQLite sintética temporal fuera de Git'}
    finally:
        stop(process)


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='onia-cerebro-cli-corregido-') as data:
        result = run(data)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))
