"""Pruebas sin red ni credenciales reales del límite de salida del piloto Meta."""
import contextlib
import importlib.util
import io
import json
import unittest
import urllib.error
import urllib.request
import urllib.response
from email.message import Message
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("meta_inventory", Path(__file__).with_name("meta-inventory.py"))
meta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meta)


class MetaInventoryTests(unittest.TestCase):
    def test_only_aggregates_leave_response(self):
        payload = {"data": [
            {"id": "act_SYNTHETIC_ID_A", "name": "PRIVATE_NAME", "account_status": 1, "currency": "BOB"},
            {"id": "act_SYNTHETIC_ID_B", "account_status": 1, "currency": "BOB"},
            {"id": "act_SYNTHETIC_ID_C", "account_status": 2, "currency": "USD"}],
            "paging": {"next": "https://example.invalid/?access_token=SYNTHETIC_SECRET"}}
        result = meta.summarize(payload, 200)
        self.assertEqual(result["cuentas_en_pagina"], 3)
        self.assertEqual(result["estados_en_pagina"], {"1": 2, "2": 1})
        self.assertEqual(result["monedas_en_pagina"], {"BOB": 2, "USD": 1})
        self.assertTrue(result["hay_siguiente_pagina"])
        output = json.dumps(result)
        for private in ("SYNTHETIC", "PRIVATE_NAME", "example.invalid", "access_token"):
            self.assertNotIn(private, output)

    def test_unexpected_payload_cannot_smuggle_text_into_summary(self):
        for payload in ({"data": ["PRIVATE_NAME"]}, {"data": [{"currency": "SYNTHETIC_SECRET"}]},
                        {"data": [{"account_status": "PRIVATE_NAME"}]}, {"error": "PRIVATE", "data": []}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                meta.summarize(payload, 200)
        self.assertEqual(meta.summarize({"data": []}, 200)["cuentas_en_pagina"], 0)

    def test_missing_secret_does_not_open_a_connection(self):
        with patch.dict(meta.os.environ, {}, clear=True), patch.object(meta.urllib.request, "build_opener") as opener:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(meta.main(), 2)
            opener.assert_not_called()
            self.assertIn("no disponible", output.getvalue())

    def test_http_failure_does_not_disclose_sensitive_error_content(self):
        error = urllib.error.HTTPError("https://example.invalid/SYNTHETIC_SECRET", 403,
                                       "PRIVATE_REASON", {"PRIVATE_HEADER": "SYNTHETIC_SECRET"},
                                       io.BytesIO(b"PRIVATE_BODY"))
        class RejectedTransport:
            def open(self, request, timeout):
                self_url = request.full_url
                if request.get_method() != "GET" or not self_url.startswith("https://graph.facebook.com/v25.0/me/adaccounts?"):
                    raise AssertionError("Solicitud inesperada")
                if "SYNTHETIC_SECRET" in self_url or request.get_header("Authorization") != "Bearer SYNTHETIC_SECRET":
                    raise AssertionError("Transporte de token incorrecto")
                raise error
        with patch.dict(meta.os.environ, {"META_ADS_ACCESS_TOKEN": "SYNTHETIC_SECRET"}, clear=True):
            with patch.object(meta.urllib.request, "build_opener", return_value=RejectedTransport()):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(meta.main(), 1)
        self.assertIn("HTTP 403", output.getvalue())
        self.assertNotIn("SYNTHETIC_SECRET", output.getvalue())
        self.assertNotIn("PRIVATE", output.getvalue())

    def test_large_response_is_rejected_without_outputting_payload(self):
        class LargeResponse(io.BytesIO):
            status = 200
        class Transport:
            def open(self, request, timeout):
                return LargeResponse(b"S" * (meta.MAX_RESPONSE_BYTES + 1))
        with patch.dict(meta.os.environ, {"META_ADS_ACCESS_TOKEN": "SYNTHETIC_SECRET"}, clear=True):
            with patch.object(meta.urllib.request, "build_opener", return_value=Transport()):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(meta.main(), 1)
        self.assertIn("excede límite", output.getvalue())
        self.assertLess(len(output.getvalue()), 100)

    def test_redirect_is_rejected_before_a_second_request(self):
        requests = []
        class OfflineHTTPS(urllib.request.BaseHandler):
            handler_order = 100

            def https_open(self, request):
                requests.append(request.full_url)
                headers = Message()
                headers["Location"] = "https://unapproved.invalid/collect"
                response = urllib.response.addinfourl(io.BytesIO(b"PRIVATE_BODY"), headers,
                                                     request.full_url, code=302)
                response.msg = "Found"
                return response
        # Uses urllib's real redirect/error chain; transport is entirely in memory.
        opener = urllib.request.build_opener(OfflineHTTPS(), meta.NoRedirect())
        request = urllib.request.Request(meta.URL, headers={"Authorization": "Bearer SYNTHETIC_SECRET"})
        with self.assertRaises(urllib.error.HTTPError) as failure:
            opener.open(request, timeout=1)
        self.assertEqual(failure.exception.code, 302)
        failure.exception.close()
        self.assertEqual(requests, [meta.URL])


if __name__ == "__main__":
    unittest.main()
