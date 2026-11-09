#!/usr/bin/env python3
"""Conecta el visor de cuentas en una sola invocación de Codex."""
import json
import os
from pathlib import Path
import sys

CODEX = Path.home() / '.local/bin/codex'
MANAGER = Path(__file__).resolve().with_name('browser-vps.py')


def overrides(urls):
    config = {
        'command': '/usr/bin/python3',
        'args': ['-B', str(MANAGER), 'mcp', '--urls', str(urls)],
        'enabled': True,
        'required': True,
        'startup_timeout_sec': 45,
        'tool_timeout_sec': 75,
        'default_tools_approval_mode': 'approve',
        'enabled_tools': ['browser_navigate', 'browser_snapshot', 'browser_close'],
    }
    args = []
    for key, value in config.items():
        args += ['-c', 'mcp_servers.cuentas_analisis.' + key + '=' + json.dumps(value)]
    return args


if __name__ == '__main__':
    if not CODEX.is_file() or not MANAGER.is_file():
        sys.exit('Falta Codex o el gestor del navegador.')
    urls = os.environ.get('ONIA_BROWSER_URLS_FILE')
    if not urls or not Path(urls).is_absolute():
        sys.exit('ONIA_BROWSER_URLS_FILE debe indicar la lista privada de URLs (ruta absoluta).')
    os.execv(CODEX, [str(CODEX), *overrides(Path(urls)), *sys.argv[1:]])
