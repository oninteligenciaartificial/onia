"""Recorrido WSGI sintético, sin servidor/red. Exporta sólo un resumen saneado."""

import json
from unittest.mock import patch

import adaptador as a
from pruebas_adaptador import PruebasAdaptador


def ensayar():
    # Reutiliza configuración, HMAC y transporte falso de las pruebas existentes.
    # La guarda de socket evita cualquier salida accidental a red en este ensayo.
    with patch("socket.socket", side_effect=AssertionError("RED_NO_PERMITIDA")):
        PruebasAdaptador.setUpClass()
        caso = PruebasAdaptador("test_flujo_salida_de_ficha_qr_captura_acceso")
        caso.setUp()
        caso.habilitar_falso()
        pasos = []

        def registrar(id_, esperado, observado):
            caso.assertEqual(observado, esperado)
            pasos.append({"id": id_, "esperado": esperado, "observado": observado})

        caso.meta(caso.mensaje("ensayo-info"))
        caso.operador("despachar")
        registrar("informacion", True, a.OFERTA["nombre"] in caso.enviados[-1]["text"]["body"])
        caso.meta(caso.mensaje("ensayo-modalidad", "VIP"))
        registrar("modalidad", "pendiente", caso.sql("SELECT estado FROM clientes")[0][0])
        caso.operador("despachar")
        caso.operador("despachar")
        registrar("qr_configurado_ficticio", "image", caso.enviados[-1]["type"])

        incompleta = {**caso.cfg}
        del incompleta["qr_media_id"]
        try:
            a.validar_config(incompleta, True)
        except ValueError as exc:
            registrar("qr_ausente_explicito", "Config inválida: qr_media_id", str(exc))
        else:
            raise AssertionError("CONFIGURACION_INCOMPLETA_ACEPTADA")

        foto = caso.mensaje("ensayo-captura", type="image", image={"id": "000002"})
        caso.meta(foto)
        caso.operador("despachar")
        registrar("comprobante_pendiente", "pendiente", caso.sql("SELECT estado FROM clientes")[0][0])
        registrar("sin_acceso_tras_captura", 0,
                  caso.sql("SELECT count(*) FROM salida WHERE tipo='confirmado'")[0][0])
        pago = json.dumps(caso.pago(importe=150)).encode()
        codigo, _ = caso.http("/operador/confirmar", cuerpo=pago,
                               auth="Bearer " + caso.cfg["dispatcher_token"])
        registrar("credencial_equivocada", 401, codigo)
        registrar("confirmacion_manual_autenticada", "confirmado",
                  caso.operador("confirmar", caso.pago(importe=150))[1]["resultado"])
        caso.operador("despachar")
        registrar("acceso_ficticio_preparado", 1,
                  caso.sql("SELECT count(*) FROM salida WHERE tipo='confirmado'")[0][0])
        registrar("duplicado_comprobante", 0, caso.meta(foto)[1]["nuevos"])
        registrar("duplicado_confirmacion", "ya_confirmado",
                  caso.operador("confirmar", caso.pago(importe=150))[1]["resultado"])
        registrar("cola_sin_reenvio", "vacio", caso.operador("despachar")[1]["resultado"])
        return {"modo": "WSGI_en_memoria_transporte_falso", "red_bloqueada_en_ensayo": True,
                "meta_invocado": False, "n8n_invocado": False, "servidor_iniciado": False,
                "mensajes_reales": 0, "pagos_reales": 0, "pasos": pasos,
                "limite": "Autenticación con credenciales ficticias; no acredita identidad ni entrega real. Sin datos privados en este resumen."}


if __name__ == "__main__":
    print(json.dumps(ensayar(), ensure_ascii=False, indent=2))
