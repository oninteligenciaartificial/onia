#!/usr/bin/env python3
"""ExecCondition: 0 libre, 1 ocupado, 255 comprobación incierta. Sin logs privados."""
import errno
import os
from pathlib import Path
import socket
import subprocess


def socket_free(path):
    with socket.socket(socket.AF_UNIX) as client:
        client.settimeout(1)
        try:
            client.connect(str(path))
        except OSError as exc:
            if exc.errno in {errno.ENOENT, errno.ECONNREFUSED}:
                return True
            raise
        return False


def check():
    if Path('/proc/1/comm').read_text().strip() != 'systemd':
        return 255
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            comm = (proc / 'comm').read_text().strip()
            if comm == 'tailscaled':
                # Cualquier daemon visible bloquea; no decidir por identidad ni leer su estado.
                return 1
        except FileNotFoundError:
            continue
        except PermissionError:
            # /proc de otros usuarios puede estar restringido; el socket propio se coteja abajo.
            if proc.stat().st_uid == os.getuid():
                return 255
    return 0 if socket_free(Path.home() / 'operacion/homelab/tailscale/tailscaled.sock') else 1


if __name__ == '__main__':
    try:
        raise SystemExit(check())
    except (OSError, subprocess.SubprocessError):
        raise SystemExit(255)
