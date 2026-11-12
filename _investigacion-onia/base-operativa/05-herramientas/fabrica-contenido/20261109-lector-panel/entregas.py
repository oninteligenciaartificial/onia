"""Archivos fijos de la bandeja privada del panel."""
from contextlib import contextmanager
import json
import os
import re
import stat


MIB = 1024 * 1024
FILES = {
    'montaje-vertical': ('montaje-vertical.mp4', 'video/mp4', 32 * MIB),
    'montaje-horizontal': ('montaje-horizontal.mp4', 'video/mp4', 32 * MIB),
    'whatsapp-demo': ('whatsapp-demo.txt', 'text/plain', 64 * 1024),
    'whatsapp-workflow': ('whatsapp-workflow.json', 'application/json', 2 * MIB),
    'guiones': ('guiones.zip', 'application/zip', 8 * MIB),
    'guiones-hoy': ('guiones-hoy.md', 'text/plain', 256 * 1024),
    'carrusel': ('carrusel.zip', 'application/zip', 32 * MIB),
}


@contextmanager
def opened(data_directory, key):
    name, mime, limit = FILES[key]
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    base = os.open(data_directory, directory_flags)
    try:
        folder = os.open('entregas', directory_flags, dir_fd=base)
        try:
            metadata = os.fstat(folder)
            if metadata.st_uid != os.getuid() or metadata.st_mode & 0o022:
                raise ValueError('Directorio de entregas inválido')
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)
        finally:
            os.close(folder)
    finally:
        os.close(base)
    with os.fdopen(fd, 'rb') as source:
        info = os.fstat(source.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid()
                or info.st_mode & 0o022 or not 0 < info.st_size <= limit):
            raise ValueError('Archivo de entrega inválido')
        if key == 'whatsapp-workflow':
            raw = source.read(limit + 1)
            workflow = json.loads(raw)
            if len(raw) != info.st_size or not isinstance(workflow, dict) or workflow.get('active') is not False:
                raise ValueError('Workflow debe ser un JSON inactivo')
            source.seek(0)
        yield source, info.st_size, name, mime


def available(data_directory):
    visible = set()
    for key in FILES:
        try:
            with opened(data_directory, key):
                visible.add(key)
        except (OSError, ValueError, RecursionError):
            continue
    return visible


def byte_range(value, size):
    match = re.fullmatch(r'bytes=(\d{0,12})-(\d{0,12})', value, flags=re.ASCII)
    if not match or not any(match.groups()):
        raise ValueError('Rango inválido')
    first, last = match.groups()
    if first:
        start, end = int(first), min(int(last), size - 1) if last else size - 1
    else:
        start, end = max(0, size - int(last)), size - 1
    if not 0 <= start <= end < size:
        raise ValueError('Rango fuera del archivo')
    return start, end
