"""Regresiones de recuperación, atribución y fallos por la entrada CLI real."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


DIRECTORIO = Path(__file__).resolve().parent
SCRIPT = DIRECTORIO / "consultar.py"
SPEC = importlib.util.spec_from_file_location("consultar", SCRIPT)
CLI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLI)


class ConsultaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogo = json.loads((DIRECTORIO / "catalogo.json").read_text())
        # El encargo exige conservar archivos, incluidos los fallos inducidos.
        cls.fixtures = Path(tempfile.mkdtemp(prefix="cerebro-consultable-pruebas-"))

    def ejecutar(self, *argumentos):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *argumentos],
            cwd="/tmp",
            capture_output=True,
            text=True,
            check=False,
        )

    def consulta(self, *argumentos):
        proceso = self.ejecutar("consultar", "--formato", "json", *argumentos)
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        return json.loads(proceso.stdout)

    def catalogo_alterado(self, nombre, mutar):
        datos = copy.deepcopy(self.catalogo)
        mutar(datos)
        ruta = self.fixtures / nombre
        ruta.write_text(json.dumps(datos, ensure_ascii=False))
        return ruta

    def fallo_catalogo(self, ruta, detalle):
        proceso = self.ejecutar("--catalogo", str(ruta), "consultar", "--tema", "tributacion")
        self.assertEqual(proceso.returncode, 2)
        self.assertEqual(proceso.stdout, "")
        self.assertIn(detalle, json.loads(proceso.stderr)["detalle"])
        self.assertNotIn("Traceback", proceso.stderr)

    def test_validacion_completa(self):
        proceso = self.ejecutar("validar")
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        datos = json.loads(proceso.stdout)
        self.assertEqual(datos["referentes"], 19)
        self.assertEqual(datos["piezas_heredadas"], 79)
        self.assertEqual(datos["fuentes_locales"], 28)

    def test_catalogo_total_trazable(self):
        datos = self.consulta()
        self.assertEqual(len({r["referente"] for r in datos["resultados"]}), 19)
        self.assertEqual(datos["cantidad"], 23)
        for item in datos["resultados"]:
            self.assertEqual(item["pasaje"]["fuente"], item["referente"])
            self.assertEqual(item["fuente_publica"]["id"], item["pieza"])
            self.assertIn("https://", item["fuente_publica"]["url"])
            limites = item["cobertura_heredada_referente"]["limites"] + item["limites_adicionales_ficha"]
            self.assertTrue(limites)
            self.assertTrue(item["propuesta_onia"]["comprobacion_pendiente"])

    def test_oferta_para_vender_tiene_fuente_util(self):
        datos = self.consulta("--tema", "oferta", "--uso", "vender")
        pedro = next(r for r in datos["resultados"] if r["id"] == "pedro-buerbaum-p1")
        self.assertEqual(pedro["fuente_publica"]["url"], "https://www.instagram.com/pedrobuerbaum/reel/Dd6oC4EkRX1/")
        self.assertIn("destinatario", pedro["hecho_documentado"])
        self.assertIn("panadería ficticia", pedro["propuesta_onia"]["aplicacion"])

    def test_prioridad_a_y_erik(self):
        datos = self.consulta("--uso", "ideas")
        prioridad = set(CLI.REFERENTES["a"]) | {"erik-taveras"}
        banderas = [r["referente"] in prioridad for r in datos["resultados"]]
        self.assertEqual(banderas, sorted(banderas, reverse=True))

    def test_desconocido_vacio_honesto(self):
        datos = self.consulta("--tema", "tributacion", "--uso", "workshop")
        self.assertEqual(datos["resultados"], [])
        self.assertEqual(datos["cantidad"], 0)
        self.assertIn("selección documental", datos["mensaje"])

    def test_normaliza_tildes_y_mayusculas(self):
        con_tildes = self.consulta("--tema", " REVISIÓN ", "--uso", "ENSEÑAR")
        simple = self.consulta("--tema", "revision", "--uso", "ensenar")
        self.assertEqual(con_tildes, simple)
        self.assertGreater(simple["cantidad"], 0)

    def test_or_en_temas_and_con_uso(self):
        datos = self.consulta("--tema", "oferta", "--tema", "agenda", "--uso", "workshop")
        for item in datos["resultados"]:
            self.assertTrue(set(item["temas"]) & {"oferta", "agenda"})
            self.assertIn("workshop", item["usos"])
        self.assertGreater(datos["cantidad"], 0)

    def test_salida_determinista(self):
        args = ("consultar", "--tema", "contenido", "--uso", "guiones", "--formato", "json")
        primera = self.ejecutar(*args)
        segunda = self.ejecutar(*args)
        self.assertEqual(primera.returncode, 0, primera.stderr)
        self.assertEqual(primera.stdout, segunda.stdout)

    def test_markdown_con_limites_y_dependencia(self):
        proceso = self.ejecutar("consultar", "--tema", "cta", "--uso", "guiones")
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        for texto in ("Hecho documentado.", "Inferencia acotada.", "Propuesta OnIA.", "Música", "misma conversación", "Cierre aceptado", "Pieza pública"):
            self.assertIn(texto, proceso.stdout)

    def test_entradas_invalidas(self):
        for argumentos in (("--uso", "bailar"), ("--tema", ""), ("--tema", "oferta\ncta"), ("--formato", "html")):
            with self.subTest(argumentos=argumentos):
                proceso = self.ejecutar("consultar", *argumentos)
                self.assertEqual(proceso.returncode, 2)
                self.assertNotIn("Traceback", proceso.stderr)

    def test_fuente_faltante_falla_incluso_consulta_vacia(self):
        def mutar(datos):
            datos["fuentes"][0]["ruta"] = "03-referentes/cerebro-operativo/20261109/fuente-ausente.md"
        ruta = self.catalogo_alterado("fuente-faltante.json", mutar)
        self.fallo_catalogo(ruta, "Fuente faltante")

    def test_fuente_alterada(self):
        def mutar(datos):
            datos["fuentes"][0]["sha256"] = "0" * 64
        self.fallo_catalogo(self.catalogo_alterado("huella-alterada.json", mutar), "Fuente alterada")

    def test_pieza_ajena_rechazada(self):
        def mutar(datos):
            datos["referentes"][0]["piezas_seleccionadas"][0]["url"] = "https://example.com/pieza-inventada"
        self.fallo_catalogo(self.catalogo_alterado("pieza-inventada.json", mutar), "Pieza ajena")

    def test_pasaje_otra_pieza_rechazado(self):
        def mutar(datos):
            datos["patrones"][0]["pasaje"] = datos["patrones"][1]["pasaje"]
        self.fallo_catalogo(self.catalogo_alterado("pasaje-otra-pieza.json", mutar), "Pasaje de otra pieza")

    def test_limites_omitidos_rechazados(self):
        def mutar(datos):
            datos["referentes"][0]["cobertura_heredada"]["limites"] = []
        self.fallo_catalogo(self.catalogo_alterado("limites-omitidos.json", mutar), "Límites heredados diferentes")

    def test_fuera_base_rechazado(self):
        def mutar(datos):
            datos["fuentes"][0]["ruta"] = "../../../../etc/passwd"
        self.fallo_catalogo(self.catalogo_alterado("ruta-fuera-base.json", mutar), "Fuente fuera de la base")

    def test_json_invalido_y_esquema_invalido(self):
        ruta = self.fixtures / "json-roto.json"
        ruta.write_text("{invalido")
        self.fallo_catalogo(ruta, "Expecting property name")
        ruta = self.fixtures / "esquema-roto.json"
        ruta.write_text('{"version": 1}')
        self.fallo_catalogo(ruta, "naturaleza")


if __name__ == "__main__":
    unittest.main(verbosity=2)
