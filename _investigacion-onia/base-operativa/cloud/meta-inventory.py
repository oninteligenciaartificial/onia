"""Piloto Meta: una página de cuentas publicitarias, sólo datos agregados."""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter

# Contrato de lectura y campos, ejemplo oficial (sin copiar su implementación):
# https://github.com/fbsamples/marketing-api-samples/blob/45274b1dce27a9680710bfa2fbbeac8a5265b382/components/js_src/actselect.js
# Bearer en solicitudes GET de la colección oficial MAPI:
# https://github.com/meta/facebook-business-sdk-codegen/blob/39395f63cfd63ee30ba896717d5e94da11abcbb5/postman/MAPI-%20Public.postman_collection.json
# ads_read es el permiso propuesto; su alcance efectivo se prueba con la petición,
# no se presume suficiente ni se amplía si Meta devuelve 403. Referencia oficial:
# https://github.com/meta/facebook-ios-sdk/blob/f7b636e64a065a8dc6bd2e7ca1705f55ec967d4b/FBSDKCoreKit/FBSDKCoreKit/Permission.swift
# v25.0 fue observada en Graph Explorer de la app ONIA Marketing API.
URL = "https://graph.facebook.com/v25.0/me/adaccounts?fields=id,account_status,currency&limit=10"
MAX_RESPONSE_BYTES = 2_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def summarize(data, status):
    """No devuelve filas, IDs, nombres, cursores ni URLs recibidas."""
    rows = data.get("data") if isinstance(data, dict) else None
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError("Formato inesperado")
    if "error" in data:
        raise ValueError("Respuesta de error")
    states, currencies = Counter(), Counter()
    for row in rows:
        state, currency = row.get("account_status"), row.get("currency")
        if state is not None and (type(state) is not int or not 0 <= state <= 999):
            raise ValueError("Formato de estado inesperado")
        if currency is not None and (not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency)):
            raise ValueError("Formato de moneda inesperado")
        states["sin_dato" if state is None else str(state)] += 1
        currencies["sin_dato" if currency is None else currency] += 1
    paging = data.get("paging")
    return {"http": status, "cuentas_en_pagina": len(rows),
            "estados_en_pagina": dict(sorted(states.items())),
            "monedas_en_pagina": dict(sorted(currencies.items())),
            "hay_siguiente_pagina": isinstance(paging, dict) and bool(paging.get("next"))}


def main():
    key = os.environ.get("META_ADS_ACCESS_TOKEN")
    if not key or key == "REPLACE_IN_SECRET_STORE":
        print("META_ADS_ACCESS_TOKEN no disponible: configurar en Secretos de red de onia.")
        return 2
    try:
        request = urllib.request.Request(URL, headers={"Authorization": "Bearer " + key}, method="GET")
        # build_opener conserva ProxyHandler y HTTPSHandler/TLS predeterminados.
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            if response.status != 200:
                print("HTTP", response.status, "; resultado no aceptado, sin cuerpo ni cabeceras.")
                return 1
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                print("Respuesta excede límite; no se muestra.")
                return 1
            result = summarize(json.loads(payload), response.status)
            print(json.dumps(result, ensure_ascii=True))
            return 0
    except urllib.error.HTTPError as error:
        print("HTTP", error.code, "; no se muestra cuerpo ni cabeceras; no se amplían permisos.")
        return 1
    except Exception:
        print("Fallo de conexión o formato; no se muestran detalles sensibles.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
