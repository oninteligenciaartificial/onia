"""Inventario acotado: GET únicamente, sin mostrar datos de workflows ni secretos."""
import json
import os
import sys
import urllib.request
import urllib.error

HOST = 'https://n8n-sergio-n8n.hqdqgh.easypanel.host'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def main():
    key = os.environ.get('N8N_API_KEY')
    if not key or key == 'REPLACE_IN_SECRET_STORE':
        print('N8N_API_KEY no disponible: configurar en almacén de secretos de onia.'); return 2
    request = urllib.request.Request(HOST + '/api/v1/workflows?limit=10&excludePinnedData=true', headers={'X-N8N-API-KEY': key}, method='GET')
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            payload = response.read(2_000_001)
            if len(payload) > 2_000_000:
                print('Respuesta excede límite; no se muestra.'); return 1
            data = json.loads(payload)
            rows = data.get('data') if isinstance(data, dict) else None
            if not isinstance(rows, list):
                print('Formato inesperado; no se muestra respuesta.'); return 1
            print(json.dumps({'http':response.status,'workflows_en_pagina':len(rows),'activos_en_pagina':sum(w.get('active') is True for w in rows),'hay_siguiente_pagina':bool(data.get('nextCursor'))})); return 0
    except urllib.error.HTTPError as error:
        print('HTTP', error.code, '; no se muestra cuerpo ni cabeceras.'); return 1
    except Exception:
        print('Fallo de conexión o formato; no se muestran detalles sensibles.'); return 1
if __name__ == '__main__':
    sys.exit(main())
