"""Contratos, seguridad y reinicio; todos los actores y secretos son ficticios."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import adaptador as a
from ensayo import NOW, fixture_config, post, signed
from motor import Event, State, command, decide


class ChannelsTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="onia-meta-test-")
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "estado.sqlite"
        self.cfg = fixture_config()
        self.store = a.Store(self.path, self.cfg["cuentas"])
        self.adapter = a.Adapter(self.cfg, self.store)
        self.scenarios = json.loads((a.ROOT / "fixtures/recorridos.json").read_text())["recorridos"]

    def payload(self, index=0, text="NEGOCIO", delta=0, suffix=""):
        payload = deepcopy(self.scenarios[index]["payload"])
        entry = payload["entry"][0]
        if "changes" in entry:
            value = entry["changes"][0]["value"]
            if payload["object"] == "instagram":
                value["text"] = text
                value["id"] += suffix
                entry["time"] += delta
            else:
                value["message"] = text
                value["comment_id"] += suffix
                value["created_time"] += delta
        else:
            message = entry["messaging"][0]
            message["message"]["text"] = text
            message["message"]["mid"] += suffix
            message["timestamp"] += delta * 1000
        return payload

    def assert_rejected(self, code, fn):
        with self.assertRaises(a.Rejected) as caught:
            fn()
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def outbox(self):
        with self.store.transaction() as db:
            return [dict(row) for row in db.execute("SELECT * FROM outbox ORDER BY rowid")]

    def test_four_channels_roundtrip_restart_and_all_transport_failures(self):
        outcomes = json.loads((a.ROOT / "fixtures/resultados.json").read_text())["casos"]
        for index, scenario in enumerate(self.scenarios):
            for case_number, case in enumerate(outcomes):
                with self.subTest(channel=scenario["canal"], outcome=case["resultado"]):
                    store = a.Store(Path(self.directory.name) / f"canal-{index}-{case_number}.sqlite", self.cfg["cuentas"])
                    adapter = a.Adapter(self.cfg, store)
                    payload = self.payload(index, delta=case_number, suffix=str(case_number))
                    result = post(adapter, payload)
                    self.assertEqual(result["resultados"][0]["resultado"], "informacion_preparada")
                    output = store.simulate_one(case["resultado"], NOW + 4)
                    self.assertEqual(output["resultado"], case["esperado"])
                    self.assertEqual(output["envios_reales"], 0)
                    restarted = a.Adapter(self.cfg, a.Store(store.path, self.cfg["cuentas"]))
                    self.assertEqual(post(restarted, payload)["resultados"][0]["resultado"], "duplicado")
                    self.assertEqual(store.simulate_one("exito", NOW + 4)["resultado"], "sin_pendientes")

    def test_negocio_exact_words_and_safe_unknown(self):
        for text in ("NEGOCIO", " negocio! ", "Quiero NEGOCIO", "Info NEGOCIO"):
            self.assertEqual(command(text), "negocio")
        for text in ("NEGOCIOS", "no entiendo NEGOCIO", "hola", "pagué", "VIP"):
            self.assertEqual(command(text), "manual")

    def test_baja_precedes_negocio_and_injection(self):
        for text in ("NEGOCIO BAJA", "STOP", "BAJA; $(x)", "no quiero NEGOCIO"):
            self.assertEqual(command(text), "baja")

    def test_pure_decision_preserves_input(self):
        event = Event("instagram_dm", "1", "2", "m.1", NOW, "NEGOCIO", "m.1")
        prior = State()
        snapshot = asdict(prior)
        result = decide(event, prior, NOW, True)
        self.assertEqual(asdict(prior), snapshot)
        self.assertTrue(result.state.interested)

    def test_baja_cancels_comment_pending_and_survives_dm_restart(self):
        post(self.adapter, self.payload())
        post(self.adapter, self.payload(1, "BAJA", delta=1))
        self.assertEqual(self.outbox()[0]["status"], "cancelado_baja")
        restarted = a.Adapter(self.cfg, a.Store(self.path, self.cfg["cuentas"]))
        result = post(restarted, self.payload(1, delta=2, suffix="2"))
        self.assertEqual(result["resultados"][0]["resultado"], "cese_vigente")
        self.assertEqual(len(self.outbox()), 1)

    def test_late_baja_still_stops(self):
        post(self.adapter, self.payload())
        result = post(self.adapter, self.payload(1, "BAJA", delta=-10000))
        self.assertEqual(result["resultados"][0]["resultado"], "baja")
        self.assertEqual(self.outbox()[0]["status"], "cancelado_baja")

    def test_old_and_equal_order_do_not_replace_context(self):
        post(self.adapter, self.payload())
        for delta in (-1, 0):
            result = post(self.adapter, self.payload(1, delta=delta, suffix=str(delta)))
            self.assertEqual(result["resultados"][0]["resultado"], "orden_tardio")
        self.assertEqual(len(self.outbox()), 1)

    def test_stale_local_not_meta_window(self):
        result = post(self.adapter, self.payload(delta=-3601))
        self.assertEqual(result["resultados"][0]["resultado"], "evento_caducado_local")
        self.assertFalse(self.outbox())

    def test_expiry_before_simulation(self):
        post(self.adapter, self.payload())
        self.assertEqual(self.store.simulate_one("exito", NOW + 3601)["resultado"], "cancelado_caducidad_local")

    def test_pending_offer_expiry_cancels_fresh_event_each_channel(self):
        manifest = json.loads((a.ROOT / "oferta-referencia.json").read_text())
        offer = json.loads((a.BASE / manifest["catalogo"]).read_text())["oferta"]
        expiry = int(datetime.fromisoformat(offer["clases"][-1]).timestamp())
        for index, scenario in enumerate(self.scenarios):
            with self.subTest(channel=scenario["canal"]):
                store = a.Store(Path(self.directory.name) / f"vencimiento-{index}.sqlite", self.cfg["cuentas"])
                payload = self.payload(index, delta=expiry - 1 - NOW)
                self.assertEqual(post(a.Adapter(self.cfg, store), payload, expiry - 1)["resultados"][0]["resultado"],
                                 "informacion_preparada")
                self.assertFalse(a.load_offer(expiry)[0])
                self.assertEqual(store.simulate_one("exito", expiry)["resultado"], "cancelado_oferta_no_vigente")
                with store.transaction() as db:
                    row = db.execute("SELECT status,outcome FROM outbox").fetchone()
                    self.assertEqual(tuple(row), ("cancelado_oferta_no_vigente", None))
                restarted = a.Store(store.path, self.cfg["cuentas"])
                self.assertEqual(restarted.simulate_one("exito", expiry)["resultado"], "sin_pendientes")

    def test_pending_offer_source_change_cancels_after_restart(self):
        original = Path.read_bytes
        for source in ("DECISIONES-SERGIO-20261110.md", "mensajes.json"):
            def changed(path):
                raw = original(path)
                if path.name != source:
                    return raw
                if source.endswith(".md"):
                    return raw + b"\n"
                catalog = json.loads(raw)
                catalog["oferta"]["nombre"] += " FICTICIO_CAMBIO"
                return json.dumps(catalog).encode()
            for index, scenario in enumerate(self.scenarios):
                with self.subTest(channel=scenario["canal"], source=source):
                    store = a.Store(Path(self.directory.name) / f"fuente-{source}-{index}.sqlite", self.cfg["cuentas"])
                    post(a.Adapter(self.cfg, store), self.payload(index))
                    restarted = a.Store(store.path, self.cfg["cuentas"])
                    with patch.object(Path, "read_bytes", changed):
                        self.assertFalse(a.load_offer(NOW + 1)[0])
                        result = restarted.simulate_one("exito", NOW + 1)
                    self.assertEqual(result["resultado"], "cancelado_oferta_no_vigente")
                    self.assertEqual(result["envios_reales"], 0)
                    self.assertEqual(restarted.simulate_one("exito", NOW + 2)["resultado"], "sin_pendientes")

    def test_pending_offer_missing_or_invalid_source_fails_closed(self):
        original = Path.read_bytes
        for source in ("DECISIONES-SERGIO-20261110.md", "mensajes.json", "oferta-referencia.json"):
            for failure in ("ausente", "json_invalido"):
                def unavailable(path):
                    if path.name == source:
                        if failure == "ausente":
                            raise FileNotFoundError("FUENTE_FICTICIA_NO_DISPONIBLE")
                        # Una decisión alterada falla por hash; los JSON por parseo.
                        return b"{"
                    return original(path)
                with self.subTest(source=source, failure=failure):
                    store = a.Store(Path(self.directory.name) / f"ausente-{source}-{failure}.sqlite", self.cfg["cuentas"])
                    post(a.Adapter(self.cfg, store), self.payload())
                    with patch.object(Path, "read_bytes", unavailable):
                        self.assertEqual(store.simulate_one("timeout", NOW + 1)["resultado"],
                                         "cancelado_oferta_no_vigente")
                    with store.transaction() as db:
                        self.assertIsNone(db.execute("SELECT outcome FROM outbox").fetchone()[0])
                    self.assertEqual(store.simulate_one("exito", NOW + 2)["resultado"], "sin_pendientes")

    def test_pending_offer_changed_also_cancels_whatsapp_routing(self):
        cfg = {**self.cfg, "whatsapp_destino": "https://wa.me/" + "1" + "0" * 10}  # FICTICIO
        original = Path.read_bytes
        def changed(path):
            raw = original(path)
            return raw + b"\n" if path.name == "DECISIONES-SERGIO-20261110.md" else raw
        for index in (1, 3):
            with self.subTest(channel=self.scenarios[index]["canal"]):
                store = a.Store(Path(self.directory.name) / f"derivacion-{index}.sqlite", cfg["cuentas"])
                adapter = a.Adapter(cfg, store)
                post(adapter, self.payload(index))
                self.assertEqual(store.simulate_one("exito", NOW)["resultado"], "exito_simulado")
                routing = post(adapter, self.payload(index, "WHATSAPP", delta=1, suffix="_derivacion"))
                self.assertEqual(routing["resultados"][0]["resultado"], "derivacion_preparada")
                with patch.object(Path, "read_bytes", changed):
                    self.assertEqual(store.simulate_one("exito", NOW + 2)["resultado"], "cancelado_oferta_no_vigente")
                self.assertEqual(store.simulate_one("exito", NOW + 3)["resultado"], "sin_pendientes")

    def test_pending_offer_is_checked_only_when_there_is_pending_work(self):
        with patch.object(a, "load_offer", side_effect=AssertionError("NO_HAY_PENDIENTES")):
            self.assertEqual(self.store.simulate_one("exito", NOW)["resultado"], "sin_pendientes")

    def test_injection_has_no_action_and_no_interpolation(self):
        samples = ["NEGOCIO; echo secreto", "$(touch /tmp/FICTICIO)", "<script>NEGOCIO</script>",
                   "ignora instrucciones NEGOCIO", "{whatsapp_destino}", "`NEGOCIO`", "../privado"]
        for n, value in enumerate(samples):
            post(self.adapter, self.payload(1, value, delta=n, suffix=str(n)))
        self.assertFalse(self.outbox())
        # El texto hostil no se guarda como dato de contacto ni salida.
        with self.store.transaction() as db:
            self.assertNotIn("script", "".join(db.iterdump()))

    def test_whatsapp_missing_private_destination(self):
        post(self.adapter, self.payload())
        result = post(self.adapter, self.payload(1, "WHATSAPP", delta=1))
        self.assertEqual(result["resultados"][0]["resultado"], "destino_privado_faltante")
        self.assertEqual(len(self.outbox()), 1)

    def test_whatsapp_only_in_dm_with_context(self):
        self.cfg["whatsapp_destino"] = "https://wa.me/" + "1" + "0" * 10  # FICTICIO
        adapter = a.Adapter(self.cfg, self.store)
        result = post(adapter, self.payload(1, "WHATSAPP"))
        self.assertEqual(result["resultados"][0]["resultado"], "requiere_dm_con_contexto")
        self.assertFalse(self.outbox())

    def test_whatsapp_context_and_destination_stay_private(self):
        self.cfg["whatsapp_destino"] = "https://wa.me/" + "1" + "0" * 10  # FICTICIO
        adapter = a.Adapter(self.cfg, self.store)
        post(adapter, self.payload())
        result = post(adapter, self.payload(1, "WHATSAPP", delta=1))
        self.assertEqual(result["resultados"][0]["resultado"], "derivacion_preparada")
        private = json.loads(self.outbox()[1]["payload"])
        self.assertEqual(private["origen_inicial"], "40001")
        self.assertTrue(private["texto"].startswith(self.cfg["whatsapp_destino"] + "?text=NEGOCIO"))
        public = json.dumps(result) + json.dumps(self.store.summary())
        for secret in (self.cfg["whatsapp_destino"], self.cfg["app_secret"], "20001", "40001"):
            self.assertNotIn(secret, public)

    def test_channels_do_not_merge_identity(self):
        post(self.adapter, self.payload(0, "BAJA"))
        fb = self.payload(2)
        fb["entry"][0]["changes"][0]["value"]["from"]["id"] = "20001"
        self.assertEqual(post(self.adapter, fb)["resultados"][0]["resultado"], "informacion_preparada")

    def test_offer_current_and_expiry(self):
        valid, reply = a.load_offer(NOW)
        self.assertTrue(valid)
        for fragment in ("Claude de 0 a 100", "13 nov 2026, 20:00", "14 nov, 14:00", "16 nov, 20:00", "Bs 50", "Bs 150", "BAJA"):
            self.assertIn(fragment, reply)
        self.assertFalse(a.load_offer(NOW + 10 * 86400)[0])

    def test_offer_hash_change_fails_closed(self):
        original = Path.read_bytes
        def altered(path):
            raw = original(path)
            return raw + b"\n" if path.name == "DECISIONES-SERGIO-20261110.md" else raw
        with patch.object(Path, "read_bytes", altered):
            self.assertFalse(a.load_offer(NOW)[0])

    def test_baja_survives_missing_offer(self):
        def missing(now):
            raise FileNotFoundError("FICTICIO")
        adapter = a.Adapter(self.cfg, self.store, missing)
        self.assertEqual(post(adapter, self.payload())["resultados"][0]["resultado"], "oferta_no_vigente")
        self.assertEqual(post(adapter, self.payload(1, "BAJA", delta=1))["resultados"][0]["resultado"], "baja")

    def test_signature_missing_wrong_and_tampered(self):
        raw, headers = signed(self.cfg, self.payload())
        for altered in ({"content-type": "application/json"}, {**headers, "x-hub-signature-256": "sha1=FICTICIO"}):
            self.assert_rejected("FIRMA_INVALIDA", lambda: self.adapter.handle("POST", altered, raw, {}, NOW))
        self.assert_rejected("FIRMA_INVALIDA", lambda: self.adapter.handle("POST", headers, raw + b" ", {}, NOW))
        self.assertEqual(self.store.summary()["eventos"], 0)

    def test_payload_and_content_type_limits(self):
        self.assert_rejected("PAYLOAD_EXCESIVO", lambda: self.adapter.handle("POST", {}, b"x" * (a.MAX_BODY + 1), {}, NOW))
        self.assert_rejected("TIPO_INVALIDO", lambda: self.adapter.handle("POST", {}, b"{}", {}, NOW))

    def test_verification_and_methods(self):
        query = {"hub.mode": "subscribe", "hub.verify_token": self.cfg["verify_token"], "hub.challenge": "12345"}
        self.assertEqual(self.adapter.handle("GET", {}, b"", query, NOW), {"status": 200, "challenge": "12345"})
        self.assert_rejected("VERIFICACION_INVALIDA", lambda: self.adapter.handle("GET", {}, b"", {**query, "hub.verify_token": "otro"}, NOW))
        self.assert_rejected("CHALLENGE_INVALIDO", lambda: self.adapter.handle("GET", {}, b"", {**query, "hub.challenge": "<script>"}, NOW))
        self.assert_rejected("METODO_INVALIDO", lambda: self.adapter.handle("DELETE", {}, b"", {}, NOW))

    def test_duplicate_json_and_non_finite(self):
        self.assert_rejected("JSON_CLAVE_DUPLICADA", lambda: a.strict_json(b'{"object":1,"object":2}'))
        for raw in (b'{"x":NaN}', b'{', b'[]', b'\xff'):
            with self.assertRaises(a.Rejected):
                a.strict_json(raw)

    def test_account_and_recipient_rejection_all_or_nothing(self):
        payload = self.payload()
        wrong = deepcopy(payload["entry"][0])
        wrong["id"] = "99999"
        payload["entry"].append(wrong)
        self.assert_rejected("CUENTA_INVALIDA", lambda: post(self.adapter, payload))
        self.assertEqual(self.store.summary()["eventos"], 0)
        payload = self.payload(1)
        payload["entry"][0]["messaging"][0]["recipient"]["id"] = "99999"
        self.assert_rejected("DESTINATARIO_INVALIDO", lambda: post(self.adapter, payload))

    def test_actor_invalid_and_reused_identity(self):
        payload = self.payload()
        payload["entry"][0]["changes"][0]["value"]["from"]["id"] = "$(x)"
        self.assert_rejected("IDENTIDAD_COMENTARIO_INVALIDA", lambda: post(self.adapter, payload))
        post(self.adapter, self.payload())
        self.assert_rejected("ID_REUTILIZADO_CON_OTROS_DATOS", lambda: post(self.adapter, self.payload(text="otro")))
        self.assertEqual(self.store.summary()["eventos"], 1)

    def test_future_and_bad_timestamp(self):
        self.assert_rejected("FECHA_FUTURA", lambda: post(self.adapter, self.payload(delta=301)))
        payload = self.payload(1)
        payload["entry"][0]["messaging"][0]["timestamp"] = True
        self.assert_rejected("FECHA_INVALIDA", lambda: post(self.adapter, payload))

    def test_batch_limit_and_malformed(self):
        payload = self.payload(1)
        payload["entry"][0]["messaging"] *= 101
        self.assert_rejected("LISTA_INVALIDA", lambda: post(self.adapter, payload))
        for key, value in (("entry", {}), ("object", "otro")):
            with self.assertRaises(a.Rejected):
                post(self.adapter, {**self.payload(), key: value})

    def test_long_and_control_text(self):
        for value in ("a" * 2001, "NEGOCIO\x00", 123, ""):
            self.assert_rejected("TEXTO_INVALIDO", lambda: post(self.adapter, self.payload(text=value)))

    def test_echo_and_attachments_never_trigger(self):
        echo = self.payload(1)
        msg = echo["entry"][0]["messaging"][0]
        msg["message"]["is_echo"] = True
        self.assert_rejected("ECHO_IDENTIDAD_INVALIDA", lambda: post(self.adapter, echo))
        msg["sender"]["id"], msg["recipient"]["id"] = "10001", "20001"
        self.assertEqual(post(self.adapter, echo)["resultados"], [])
        attached = self.payload(1)
        attached["entry"][0]["messaging"][0]["message"].pop("text")
        self.assertEqual(post(self.adapter, attached)["resultados"], [])
        self.assertFalse(self.outbox())

    def test_concurrent_duplicate_is_atomic(self):
        payload = self.payload()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: post(self.adapter, payload), range(2)))
        self.assertEqual(sorted(r["resultados"][0]["resultado"] for r in results), ["duplicado", "informacion_preparada"])
        self.assertEqual(len(self.outbox()), 1)

    def test_concurrent_dispatch_and_uncertain_do_not_retry(self):
        post(self.adapter, self.payload())
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.store.simulate_one("timeout", NOW), range(2)))
        self.assertEqual(sorted(r["resultado"] for r in results), ["incierto_simulado", "sin_pendientes"])
        restarted = a.Store(self.path, self.cfg["cuentas"])
        self.assertEqual(restarted.simulate_one("exito", NOW)["resultado"], "sin_pendientes")

    def test_transaction_rolls_back_prior_valid_event_on_collision(self):
        post(self.adapter, self.payload())
        first = self.payload(1, delta=1)
        collision = self.payload(text="OTRO")
        first["entry"].extend(collision["entry"])
        self.assert_rejected("ID_REUTILIZADO_CON_OTROS_DATOS", lambda: post(self.adapter, first))
        self.assertEqual(self.store.summary()["eventos"], 1)
        self.assertEqual(len(self.outbox()), 1)

    def test_binding_and_database_permissions(self):
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        accounts = {**self.cfg["cuentas"], "instagram": "99999"}
        self.assert_rejected("BASE_DE_OTRAS_CUENTAS", lambda: a.Store(self.path, accounts))
        self.assert_rejected("BASE_DE_OTRAS_CUENTAS", lambda: a.Adapter({**self.cfg, "cuentas": accounts}, self.store))
        os.chmod(self.path, 0o644)
        self.assert_rejected("ARCHIVO_NO_PRIVADO", lambda: a.Store(self.path, self.cfg["cuentas"]))

    def test_reject_symlink_repository_and_public_config(self):
        link = Path(self.directory.name) / "enlace.sqlite"
        link.symlink_to(self.path)
        self.assert_rejected("ARCHIVO_NO_PRIVADO", lambda: a.Store(link, self.cfg["cuentas"]))
        self.assert_rejected("RUTA_EN_REPOSITORIO", lambda: a.Store(a.ROOT / "no-crear.sqlite", self.cfg["cuentas"]))
        cfg = Path(self.directory.name) / "config.json"
        cfg.write_text(json.dumps(self.cfg))
        os.chmod(cfg, 0o644)
        self.assert_rejected("ARCHIVO_NO_PRIVADO", lambda: a.read_config(cfg))
        os.chmod(cfg, 0o600)
        self.assertEqual(a.read_config(cfg), self.cfg)

    def test_no_real_network_even_if_enable_requested(self):
        for enabled in (True, "false", 1, None):
            self.assert_rejected("ACTIVACION_PENDIENTE", lambda: a.validate_config({**self.cfg, "envios_habilitados": enabled}))
        with patch("socket.socket", side_effect=AssertionError("RED_PROHIBIDA")):
            self.assert_rejected("ACTIVACION_PENDIENTE", lambda: a.RealConnector().send({"text": "NEGOCIO"}))
            self.assertEqual(post(self.adapter, self.payload())["envios_reales"], 0)

    def test_destination_rejects_arbitrary_host_query_and_injection(self):
        for destination in ("https://example.invalid", "http://wa.me/10000000000", "https://wa.me/10000000000?token=x", "$(x)"):
            self.assert_rejected("DESTINO_PRIVADO_INVALIDO", lambda: a.validate_config({**self.cfg, "whatsapp_destino": destination}))

    def test_panel_consumer_contract_uses_native_allowlist(self):
        import puente_panel
        result = puente_panel.consume()
        self.assertEqual(result["estado"], "para_revision")
        self.assertEqual(result["exports_consumidos"], 1)
        self.assertEqual(result["entradas_faltantes"], 4)
        self.assertTrue(result["documentos_disponibles"])
        self.assertFalse(result["errores_modelo"])
        self.assertFalse(result["ui_publicada"])
        self.assertEqual(result["lector_sin_puente"], "admitido")
        self.assertEqual(puente_panel.reader().PRODUCERS["automatizaciones"],
                         str(puente_panel.ROOT.relative_to(puente_panel.BASE)))

    def test_each_channel_late_injection_identity_and_baja(self):
        for index, scenario in enumerate(self.scenarios):
            with self.subTest(channel=scenario["canal"]):
                store = a.Store(Path(self.directory.name) / f"seguridad-{index}.sqlite", self.cfg["cuentas"])
                adapter = a.Adapter(self.cfg, store)
                for value, delta, expected in (("NEGOCIO", 0, "informacion_preparada"),
                                               ("NEGOCIO", -1, "orden_tardio"),
                                               ("NEGOCIO; $(FICTICIO)", 1, "inyeccion"),
                                               ("BAJA", -100, "baja"),
                                               ("NEGOCIO", 2, "cese_vigente")):
                    result = post(adapter, self.payload(index, value, delta, str(delta + 500)))
                    self.assertEqual(result["resultados"][0]["resultado"], expected)
                self.assertEqual(store.summary()["salidas"], {"cancelado_baja": 1})
                invalid = self.payload(index, suffix="123")
                invalid["entry"][0]["id"] = "99999"
                self.assert_rejected("CUENTA_INVALIDA", lambda: post(adapter, invalid))

    def test_public_journey_has_four_routes_and_failure_receipts(self):
        from ensayo import run
        result = run()
        self.assertEqual(result["tipo_evidencia"], "SIMULACION_LOCAL_NO_E2E")
        self.assertEqual(len(result["canales"]), 4)
        self.assertEqual(len(result["resultados_transporte_por_canal"]), 16)
        for channel in result["canales"]:
            self.assertEqual(channel["destino_ausente"]["resultados"][0]["resultado"], "destino_privado_faltante")
            self.assertEqual(channel["derivacion_con_destino_ficticio"]["resultados"][0]["resultado"], "derivacion_preparada")
            self.assertEqual(channel["tras_baja"]["resultados"][0]["resultado"], "cese_vigente")
        for row in result["resultados_transporte_por_canal"]:
            self.assertEqual(row["siguiente_intento"]["resultado"], "sin_pendientes")
            self.assertEqual(row["salida"]["envios_reales"], 0)
        public = json.dumps(result)
        self.assertNotIn("wa.me", public)
        self.assertNotIn(self.cfg["app_secret"], public)

    def test_detailed_export_never_claims_readiness(self):
        data = json.loads((a.ROOT / "contrato-canales.json").read_text())
        self.assertEqual(data["modo"], "simulacion")
        self.assertFalse(data["conector_real_habilitado"])
        self.assertEqual(data["envios_reales"], 0)
        self.assertTrue(data["aprobacion_pendiente"])
        self.assertEqual({r["canal"] for r in data["canales"]}, {r["canal"] for r in self.scenarios})
        for row in data["canales"]:
            self.assertFalse(row["listo"])
            self.assertFalse(row["e2e_real"])
            self.assertTrue(row["entradas_faltantes"])
            self.assertTrue((a.BASE / row["prueba"]).is_file())

    def test_config_is_snapshot(self):
        self.cfg["cuentas"]["instagram"] = "99999"
        self.cfg["app_secret"] = "FICTICIO_CAMBIO_POSTERIOR_000000"
        original_cfg = fixture_config()
        self.assertEqual(self.adapter.config, original_cfg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
