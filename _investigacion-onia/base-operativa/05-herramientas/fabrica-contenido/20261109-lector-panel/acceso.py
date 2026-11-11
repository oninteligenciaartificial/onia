"""Origen privado explícito y autenticación Basic detrás de TLS del proxy del VPS."""
import argparse
import base64
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
from urllib.parse import urlsplit

import lector
from operacion import require, text

ITERATIONS = 600000


def private_file(path):
    path = Path(path).absolute()
    require(not path.resolve().is_relative_to(lector.REPO.resolve()), 'Credenciales deben quedar fuera de Git')
    for parent in (path, *path.parents):
        require(not parent.is_symlink(), 'Ruta de credenciales enlazada')
        require(not (parent / '.git').is_file() and not (parent / '.git/HEAD').is_file(), 'Credenciales dentro de Git')
    return path


def origin(value):
    parsed = urlsplit(text(value, 300))
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password,
            'Origen HTTPS explícito requerido')
    require(parsed.path == '' and not parsed.query and not parsed.fragment and '*' not in value
            and not any(c.isspace() for c in value) and '\\' not in value, 'Origen inválido')
    require(parsed.port is None or 1 <= parsed.port <= 65535, 'Puerto de origen inválido')
    return parsed


class Access:
    def __init__(self, path):
        path = private_file(path)
        require(path.is_file() and path.stat().st_size <= 8192 and path.stat().st_mode & 0o077 == 0
                and path.stat().st_nlink == 1, 'Credenciales deben ser un archivo privado 0600')
        data = json.loads(path.read_text())
        require(data.get('schema') == 'onia-panel-acceso-v1', 'Contrato de acceso inválido')
        parsed = origin(data.get('origen_externo'))
        self.host = parsed.netloc.lower()
        if parsed.port == 443:
            self.host = self.host.rsplit(':', 1)[0]
        self.origin = 'https://' + self.host
        self.user = text(data.get('usuario'), 100)
        require(not any(c in self.user for c in ':\r\n\t'), 'Usuario inválido')
        self.salt = data.get('salt', '')
        self.digest = data.get('password_pbkdf2_sha256', '')
        require(re.fullmatch(r'[0-9a-f]{32}', self.salt) and re.fullmatch(r'[0-9a-f]{64}', self.digest), 'Credencial incompleta')

    def authenticated(self, header):
        try:
            require(isinstance(header, str) and header.startswith('Basic ') and len(header) < 3000, 'Autenticación requerida')
            value = base64.b64decode(header[6:], validate=True).decode('utf-8')
            user, password = value.split(':', 1)
            require(0 < len(password.encode()) <= 1000, 'Credencial inválida')
            digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(self.salt), ITERATIONS).hex()
            return secrets.compare_digest(user.encode(), self.user.encode()) and secrets.compare_digest(digest, self.digest)
        except (ValueError, TypeError, UnicodeError):
            return False


def create(path, external_origin, user, password):
    origin(external_origin)
    text(user, 100)
    require(not any(c in user for c in ':\r\n\t'), 'Usuario inválido')
    require(24 <= len(password) and len(password.encode()) <= 1000, 'Contraseña privada de al menos 24 caracteres y hasta 1000 bytes requerida')
    path = private_file(path)
    require(path.parent.is_dir(), 'Crear previamente el directorio privado de credenciales')
    salt = secrets.token_hex(16)
    data = {'schema': 'onia-panel-acceso-v1', 'origen_externo': external_origin,
            'usuario': user, 'salt': salt,
            'password_pbkdf2_sha256': hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), ITERATIONS).hex()}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--crear', type=Path, required=True)
    parser.add_argument('--origen', required=True)
    parser.add_argument('--usuario', required=True)
    args = parser.parse_args()
    password = getpass.getpass('Contraseña privada (mínimo 24 caracteres): ')
    require(password == getpass.getpass('Repetir contraseña: '), 'Las contraseñas difieren')
    create(args.crear, args.origen, args.usuario, password)
    print('Configuración privada escrita. Conservar la contraseña fuera de Git.')
