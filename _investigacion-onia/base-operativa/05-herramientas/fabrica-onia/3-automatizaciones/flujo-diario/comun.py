"""Primitivas privadas del ciclo. Sin red, shell, tareas ni procesos residentes."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[3]
REPO = BASE.parents[1]
PANEL = BASE / '05-herramientas/fabrica-contenido/20261109-lector-panel'
GENERATOR = BASE / '05-herramientas/fabrica-onia/1-guiones-calendario/automatizada'


def require(ok, code):
    if not ok:
        raise ValueError(code)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


sys.path.insert(0, str(PANEL))
import lector


def now():
    return datetime.now(timezone.utc).isoformat()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def no_links(path):
    path = Path(path).absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'ENLACE_RECHAZADO')
    return path


def private_root(path):
    path = no_links(path)
    require(not path.resolve().is_relative_to(REPO.resolve()), 'DATOS_DENTRO_GIT')
    for part in (path, *path.parents):
        require(not ((part / '.git').is_file() or (part / '.git/HEAD').is_file()) and not ((part / 'objects').is_dir() and (part / 'HEAD').is_file()), 'DATOS_DENTRO_GIT')
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    info = path.stat()
    require(info.st_uid == os.getuid() and not info.st_mode & 0o077, 'DIRECTORIO_NO_PRIVADO')
    return path


def read_json(path, maximum=2*1024*1024):
    path = no_links(path)
    info = path.stat()
    require(stat.S_ISREG(info.st_mode) and info.st_size <= maximum, 'ARCHIVO_INVALIDO')
    return json.loads(path.read_bytes())


def atomic(path, value):
    path = no_links(path)
    require(path.parent.is_dir(), 'DIRECTORIO_AUSENTE')
    fd, temporary = tempfile.mkstemp(prefix='.flujo-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(encoded(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def immutable(path, value):
    path = no_links(path)
    raw = encoded(value)
    if path.exists():
        require(path.read_bytes() == raw, 'ORIGINAL_DIFERENTE')
        return
    fd, temporary = tempfile.mkstemp(prefix='.pedido-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)  # publicación completa y exclusiva, sin reemplazar original
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(root):
    root = private_root(root)
    path = no_links(root / '.lock')
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield root
