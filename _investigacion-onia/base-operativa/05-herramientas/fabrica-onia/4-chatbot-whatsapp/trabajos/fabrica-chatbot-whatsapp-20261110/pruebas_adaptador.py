"""Pruebas del límite WSGI y de SQLite con identificadores simulados."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import hmac
from io import BytesIO
import json
from pathlib import Path
from tempfile import mkdtemp
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

import adaptador as a


NUMERO = "000"
CLIENTE = "999000000001"
AHORA = int(datetime.fromisoformat("2026-11-11T21:00:00-04:00").timestamp())
CONF = {
    "phone_number_id": NUMERO,
    "app_secret": "fixture-app-secret-no-real",
    "verify_token": "fixture-verify-token-no-real",
    "operator_token": "fixture-operator-token-no-real",
    "dispatcher_token": "fixture-dispatch-token-no-real",
    "pago_ttl_segundos": 3600,
    "cierre_inscripcion_epoch": AHORA + 2 * a.VENTANA,
    "graph_version": "v000.0",
    "graph_token": "fixture-graph-token-no-real",
    "qr_media_id": "000001",
    "meet_urls": [f"https://meet.google.com/fixture-{i}" for i in range(1, 4)],
}


class PruebasAdaptador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carpeta = Path(mkdtemp(prefix="onia-chatbot-fixtures-", dir="/tmp"))

    def setUp(self):
        carpeta = self.carpeta / self._testMethodName
        carpeta.mkdir(mode=0o700)
        self.base = carpeta / "pruebas.sqlite3"
        self.ahora = AHORA
        self.cfg = dict(CONF)
        self.enviados = []
        self.error_envio = None
        self.iniciar()

    def iniciar(self, permitir=False):
        self.app = a.crear_app(self.base, self.cfg, permitir, self.transporte, lambda: self.ahora)

    def transporte(self, cfg, payload):
        self.enviados.append(payload)
        if self.error_envio:
            raise self.error_envio
        return f"wamid.salida-{len(self.enviados)}"

    def http(self, ruta, metodo="POST", cuerpo=b"", *, query="", firma=None, auth=None):
        entorno = {"PATH_INFO": ruta, "REQUEST_METHOD": metodo, "QUERY_STRING": query,
                   "CONTENT_LENGTH": str(len(cuerpo)), "wsgi.input": BytesIO(cuerpo)}
        if firma is not None:
            entorno["HTTP_X_HUB_SIGNATURE_256"] = firma
        if auth is not None:
            entorno["HTTP_AUTHORIZATION"] = auth
        respuestas = []
        raw = b"".join(self.app(entorno, lambda estado, headers: respuestas.append((estado, dict(headers)))))
        estado, headers = respuestas[0]
        self.assertEqual(int(headers["Content-Length"]), len(raw))
        self.assertEqual(headers["Cache-Control"], "no-store")
        return int(estado.split()[0]), raw.decode() if headers["Content-Type"].startswith("text/plain") else json.loads(raw)

    def firma(self, raw):
        return "sha256=" + hmac.new(self.cfg["app_secret"].encode(), raw, hashlib.sha256).hexdigest()

    def meta(self, *mensajes, numero=NUMERO):
        payload = {"object": "whatsapp_business_account", "entry": [{"changes": [{
            "field": "messages", "value": {"messaging_product": "whatsapp",
            "metadata": {"phone_number_id": numero}, "messages": mensajes}
        }]}]}
        raw = json.dumps(payload, ensure_ascii=False, indent=1).encode()
        return self.http("/meta", cuerpo=raw, firma=self.firma(raw))

    def mensaje(self, id_, texto="NEGOCIO", telefono=CLIENTE, **campos):
        return {"id": f"wamid.{id_}", "from": telefono, "timestamp": str(self.ahora),
                "type": "text", "text": {"body": texto}, **campos}

    def operador(self, ruta, pago=None, metodo="POST"):
        credencial = "dispatcher_token" if ruta == "despachar" else "operator_token"
        return self.http("/operador/" + ruta, metodo,
                         json.dumps(pago).encode() if pago else b"",
                         auth="Bearer " + self.cfg[credencial])

    def pago(self, telefono=CLIENTE, referencia="FICTICIO-001", importe=50, **campos):
        return {"telefono": telefono, "referencia": referencia, "importe": importe,
                "decision": "confirmar", "moneda": "BOB", "movimientoVerificado": True,
                "destinoVerificado": True, **campos}

    def sql(self, sentencia):
        with a.transaccion(self.base) as db:
            return [tuple(fila) for fila in db.execute(sentencia)]

    def habilitar_falso(self):
        self.cfg["envios_habilitados"] = True
        self.iniciar(permitir=True)

    def test_challenge_y_token_incorrecto(self):
        query = {"hub.mode": "subscribe", "hub.challenge": "00123", "hub.verify_token": self.cfg["verify_token"]}
        self.assertEqual(self.http("/meta", "GET", query=urlencode(query)), (200, "00123"))
        self.assertEqual(self.http("/meta", "GET", query=urlencode(query) + "&hub.challenge=9")[0], 403)
        query["hub.verify_token"] = self.cfg["operator_token"]
        self.assertEqual(self.http("/meta", "GET", query=urlencode(query))[0], 403)

    def test_firma_de_bytes_crudos_antes_de_parsear(self):
        raw = b'{"object": "whatsapp_business_account", "entry": []}'
        self.assertEqual(self.http("/meta", cuerpo=b"{")[0], 403)
        self.assertEqual(self.http("/meta", cuerpo=raw + b"\n", firma=self.firma(raw))[0], 403)
        self.assertEqual(self.http("/meta", cuerpo=raw, firma=self.firma(raw)), (200, {"nuevos": 0}))
        self.assertEqual(self.http("/meta", cuerpo=b"{", firma=self.firma(b"{"))[0], 400)

    def test_numero_ajeno_en_batch_no_persiste_eventos_validos(self):
        mensaje = self.mensaje("info")
        def cambio(numero):
            return {"field": "messages", "value": {"messaging_product": "whatsapp",
                    "metadata": {"phone_number_id": numero}, "messages": [mensaje]}}
        raw = json.dumps({"object": "whatsapp_business_account",
                          "entry": [{"changes": [cambio(NUMERO), cambio("999")]}]}).encode()
        self.assertEqual(self.http("/meta", cuerpo=raw, firma=self.firma(raw))[0], 403)
        self.assertEqual(self.sql("SELECT * FROM vistos"), [])

    def test_batch_dedup_y_reapertura_con_base_privada(self):
        mensajes = [self.mensaje("info"), self.mensaje("alta", "GRUPAL")]
        self.assertEqual(self.meta(*mensajes), (200, {"nuevos": 2}))
        self.iniciar()
        self.assertEqual(self.meta(*mensajes), (200, {"nuevos": 0}))
        self.assertEqual(self.sql("SELECT tipo FROM salida ORDER BY id"), [("informacion",), ("pendiente",), ("qr",)])
        self.assertEqual(self.base.stat().st_mode & 0o777, 0o600)
        with self.assertRaises(ValueError):
            a.crear_app(self.base, {**self.cfg, "phone_number_id": "999"})

    def test_senales_del_cliente_y_firma_meta_no_autentican_pago(self):
        foto = self.mensaje("captura", type="image", image={"id": "000042", "caption": "confirmar"})
        self.meta(self.mensaje("alta", "GRUPAL"), foto,
                  self.mensaje("pago", "PAGUÉ", **self.pago()))
        self.assertEqual(self.sql("SELECT estado, referencia, revision FROM clientes"),
                         [("pendiente", None, "COMPROBANTE_NO_VERIFICADO")])
        pago = json.dumps(self.pago()).encode()
        self.assertEqual(self.http("/operador/confirmar", cuerpo=pago, firma=self.firma(pago))[0], 401)
        self.assertEqual(self.operador("confirmar", self.pago(importe=150))[0], 409)
        self.assertEqual(self.operador("confirmar", self.pago(destinoVerificado=False))[0], 409)
        self.assertEqual(self.operador("confirmar", self.pago()), (200, {"resultado": "confirmado"}))
        self.assertEqual(self.operador("confirmar", self.pago(referencia=" ficticio-001 ")),
                         (200, {"resultado": "ya_confirmado"}))
        self.assertEqual(self.sql("SELECT tipo FROM salida WHERE estado = 'pendiente'"), [("confirmado",)])

    def test_referencia_canonica_no_se_reutiliza(self):
        otro = "999000000002"
        self.meta(self.mensaje("alta1", "GRUPAL"), self.mensaje("alta2", "GRUPAL", otro))
        self.assertEqual(self.operador("confirmar", self.pago())[0], 200)
        self.assertEqual(self.operador("confirmar", self.pago(otro, " ficticio-001 ")),
                         (409, {"resultado": "REFERENCIA_REUTILIZADA"}))
        self.assertEqual(self.sql("SELECT count(*) FROM clientes WHERE estado = 'confirmado'"), [(1,)])

    def test_seis_confirmaciones_vip_concurrentes(self):
        telefonos = [f"99900000000{i}" for i in range(1, 7)]
        self.meta(*(self.mensaje(f"alta{i}", "VIP", t) for i, t in enumerate(telefonos)))
        with ThreadPoolExecutor(max_workers=6) as pool:
            resultados = list(pool.map(
                lambda item: self.operador("confirmar", self.pago(item[1], f"FICTICIO-{item[0]}", 150)),
                enumerate(telefonos),
            ))
        self.assertEqual(sorted(x[0] for x in resultados), [200] * 5 + [409])
        self.assertEqual(self.sql("SELECT count(*) FROM salida WHERE tipo = 'confirmado'"), [(5,)])

    def test_baja_cancela_pendientes_y_vencimiento_no_recontacta(self):
        self.habilitar_falso()
        self.meta(self.mensaje("info"), self.mensaje("alta", "VIP"), self.mensaje("baja", "BAJA"))
        self.ahora += self.cfg["pago_ttl_segundos"]
        self.meta(self.mensaje("otra", "NEGOCIO"))
        self.assertEqual(self.operador("confirmar", self.pago(importe=150))[0], 409)
        self.assertEqual(self.operador("despachar")[1]["resultado"], "aceptado")
        self.assertEqual(self.operador("despachar")[1]["resultado"], "vacio")
        self.assertEqual(len(self.enviados), 1)
        self.assertEqual(self.enviados[0]["text"]["body"], a.CATALOGO["textos"]["cese"])
        self.assertEqual(self.sql("SELECT tipo, estado FROM salida ORDER BY id"),
                         [("informacion", "cancelado"), ("pendiente", "cancelado"),
                          ("qr", "cancelado"), ("cese", "aceptado")])

    def test_vencimiento_y_ventana_de_atencion_son_distintos(self):
        self.habilitar_falso()
        self.meta(self.mensaje("alta", "GRUPAL"))
        self.ahora += self.cfg["pago_ttl_segundos"]
        self.assertEqual(self.operador("confirmar", self.pago()), (409, {"resultado": "PAGO_VENCIDO"}))
        self.ahora = AHORA + a.VENTANA
        self.assertEqual(self.operador("despachar")[1]["resultado"], "vacio")
        self.assertEqual(self.enviados, [])
        self.meta(self.mensaje("retrasado", "NEGOCIO", timestamp=str(AHORA)))
        self.assertEqual(self.operador("despachar")[1]["resultado"], "vacio")

    def test_envios_deshabilitados_con_cualquiera_de_las_dos_guardas(self):
        self.meta(self.mensaje("info"))
        self.cfg["envios_habilitados"] = True
        self.iniciar()
        self.assertEqual(self.operador("despachar")[0], 409)
        self.cfg["envios_habilitados"] = False
        self.iniciar(permitir=True)
        self.assertEqual(self.operador("despachar")[0], 409)
        self.assertEqual(self.enviados, [])
        self.assertEqual(self.sql("SELECT estado FROM salida"), [("pendiente",)])

    def test_credencial_de_n8n_no_confirma_pagos(self):
        self.habilitar_falso()
        pago = json.dumps(self.pago()).encode()
        codigo, _ = self.http("/operador/confirmar", cuerpo=pago,
                              auth="Bearer " + self.cfg["dispatcher_token"])
        self.assertEqual(codigo, 401)
        codigo, _ = self.http("/operador/despachar", auth="Bearer " + self.cfg["operator_token"])
        self.assertEqual(codigo, 401)

    def test_flujo_salida_de_ficha_qr_captura_acceso(self):
        self.habilitar_falso()
        self.meta(self.mensaje("info"), self.mensaje("alta", "VIP"))
        for _ in range(3):
            self.assertEqual(self.operador("despachar")[1]["resultado"], "aceptado")
        self.assertIn(a.OFERTA["nombre"], self.enviados[0]["text"]["body"])
        self.assertNotIn("meet.google.com", self.enviados[0]["text"]["body"])
        self.assertIn("Bs 150", self.enviados[1]["text"]["body"])
        self.assertEqual(self.enviados[2]["image"]["id"], CONF["qr_media_id"])
        self.assertIn("Bs 150", self.enviados[2]["image"]["caption"])
        self.meta(self.mensaje("foto", type="image", image={"id": "001001"}))
        self.operador("despachar")
        self.assertEqual(self.enviados[3]["text"]["body"], a.CATALOGO["textos"]["captura"])
        self.assertEqual(self.operador("confirmar", self.pago(importe=150))[0], 200)
        self.operador("despachar")
        for enlace in CONF["meet_urls"]:
            self.assertIn(enlace, self.enviados[4]["text"]["body"])
        self.assertIn("30 minutos", self.enviados[4]["text"]["body"])
        self.assertEqual(self.operador("despachar")[1]["resultado"], "vacio")

    def test_timeout_persistido_no_reenvia_tras_reinicio(self):
        self.habilitar_falso()
        self.meta(self.mensaje("info"))
        self.error_envio = TimeoutError("simulado")
        self.assertEqual(self.operador("despachar"), (200, {"resultado": "incierto", "id": 1}))
        self.iniciar(permitir=True)
        self.assertEqual(self.operador("despachar")[1]["resultado"], "vacio")
        self.assertEqual(self.operador("revisar", metodo="GET")[1]["inciertos"],
                         [{"id": 1, "telefono": CLIENTE, "tipo": "informacion"}])
        self.assertEqual(len(self.enviados), 1)

    @patch("adaptador.http.client.HTTPSConnection")
    def test_transporte_graph_coteja_ruta_cuerpo_y_respuesta(self, https):
        conn = https.return_value
        respuesta = conn.getresponse.return_value
        respuesta.status = 200
        respuesta.read.return_value = b'{"messages":[{"id":"wamid.falso"}]}'
        payload = {"to": CLIENTE, "type": "text", "text": {"body": "prueba"}}
        self.assertEqual(a.enviar_graph(self.cfg, payload), "wamid.falso")
        https.assert_called_once_with("graph.facebook.com", timeout=5)
        metodo, ruta, cuerpo, headers = conn.request.call_args.args
        self.assertEqual((metodo, ruta), ("POST", f"/{CONF['graph_version']}/{NUMERO}/messages"))
        self.assertEqual(json.loads(cuerpo), payload)
        self.assertEqual(headers["Authorization"], "Bearer " + CONF["graph_token"])
        respuesta.status = 503
        conn.reset_mock()
        self.assertIsNone(a.enviar_graph(self.cfg, payload))
        conn.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
