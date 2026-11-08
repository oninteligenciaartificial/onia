#!/usr/bin/python3
"""Inyección MCP por proceso; no instala ni cambia configuración global."""
import json,os,sys
from pathlib import Path
REAL='/home/onia-codex-worker/.local/bin/codex'
INSTALL=Path('/home/onia-codex-worker/operacion/browser-piloto-20261108')
def overrides(cwd):
    output=Path(cwd)/'_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/capturas'
    config={
      'command':'/usr/bin/node',
      'args':[str(INSTALL/'node_modules/@playwright/mcp/cli.js'),'--headless','--isolated','--sandbox','--executable-path',str(INSTALL/'browsers/chromium-1252/chrome-linux64/chrome'),'--output-dir',str(output)],
      'enabled':True,'required':True,'startup_timeout_sec':30,'tool_timeout_sec':60,
      # Sergio autorizó estas cuatro llamadas de lectura/navegación/captura.
      'default_tools_approval_mode':'approve',
      'enabled_tools':['browser_navigate','browser_snapshot','browser_take_screenshot','browser_close'],
    }
    args=[]
    for key,value in config.items():
        args+=['-c','mcp_servers.playwright.'+key+'='+json.dumps(value)]
    return args
if __name__=='__main__':
    for file in (Path(REAL),INSTALL/'node_modules/@playwright/mcp/cli.js',INSTALL/'browsers/chromium-1252/chrome-linux64/chrome'):
        if not file.is_file():raise SystemExit('Falta instalación existente: '+str(file))
    os.execv(REAL,[REAL,*overrides(Path.cwd()),*sys.argv[1:]])
