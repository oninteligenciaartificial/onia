import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import harness
import trabajo


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        source = harness.BASE / "orquestacion.json"
        (self.base / "orquestacion.json").write_bytes(source.read_bytes())
        self.data = json.loads(source.read_text(encoding="utf-8"))
        paths = [self.data["reglas"], *self.data["contexto_comun"],
                 *self.data["archivos_cloud"], *self.data["skills"].values()]
        for route in self.data["areas"].values():
            paths.extend(route["contexto"])
        for relative in paths:
            path = self.base / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture de presencia; no ejecutar.\n", encoding="utf-8")

    def prepare(self, task_id="pieza-1", area="video"):
        return harness.prepare(self.base, task_id, area, "Entregar una pieza",
                               "Video MP4", "Audio y dimensiones revisados", ["Material sintético"])

    def test_doctor_distinguishes_files_from_runtime(self):
        result = harness.doctor(self.base)
        self.assertTrue(result["ok"])
        self.assertIn("No prueba instalación", result["limite"])
        (self.base / "cloud/install.sh").unlink()
        (self.base / "ORQUESTACION.md").unlink()
        result = harness.doctor(self.base)
        self.assertFalse(result["ok"])
        self.assertTrue(any("cloud/install.sh" in error and "checkout" in error for error in result["errores"]))
        self.assertTrue(any("ORQUESTACION.md" in error for error in result["errores"]))
        self.assertFalse((self.base / "operacion").exists())

    def test_invalid_area_writes_nothing(self):
        with self.assertRaisesRegex(ValueError, "Área inválida"):
            self.prepare(area="inexistente")
        self.assertFalse((self.base / "operacion").exists())

    def test_duplicates_preserve_both_files(self):
        result = self.prepare()
        brief = self.base / result["briefing"]
        record = trabajo.task_path(self.base, "pieza-1")
        before = brief.read_bytes(), record.read_bytes()
        with self.assertRaisesRegex(ValueError, "ya existe"):
            self.prepare()
        self.assertEqual(before, (brief.read_bytes(), record.read_bytes()))

    def test_existing_record_does_not_get_a_replacement_brief(self):
        trabajo.create(self.base, "pieza-1", "Objetivo original", "Continuar")
        with self.assertRaisesRegex(ValueError, "ya existe"):
            self.prepare()
        self.assertEqual(trabajo.read_task(self.base, "pieza-1")["objetivo"], "Objetivo original")
        self.assertFalse((self.base / "operacion/encargos/pieza-1.md").exists())

    def test_prepare_and_resume_in_separate_processes(self):
        script = str(Path(harness.__file__).resolve())
        command = [sys.executable, script, "--base", str(self.base)]
        prepared = subprocess.run(command + ["preparar", "venta-1", "--area", "marketing",
                                  "--objetivo", "Vender un taller", "--entregable", "Ficha y embudo",
                                  "--aceptacion", "Recorrido revisado", "--entrada", "Demo disponible"],
                                  capture_output=True, text=True, encoding="utf-8", check=True)
        result = json.loads(prepared.stdout)
        self.assertEqual(result["skill_directora"], "preparar-oferta-y-embudo")
        resumed = subprocess.run(command + ["retomar", "venta-1"], capture_output=True,
                                 text=True, encoding="utf-8", check=True)
        result = json.loads(resumed.stdout)
        self.assertEqual(result["tarea"]["estado"], "preparado")
        self.assertIn("Demo disponible", result["briefing"])
        self.assertIn("Ficha y embudo", result["briefing"])
        self.assertIn("../../ORQUESTACION.md", result["briefing"])
        self.assertIn("no crea agentes", result["nota_harness"])

    def test_routes_and_product_scope(self):
        expected = {"marketing": "preparar-oferta-y-embudo", "video": "producir-video",
                    "desarrollo": "desarrollar-y-verificar", "automatizaciones": "automatizar-n8n",
                    "organizacion": "planificar-dia", "producto": "desarrollar-y-verificar"}
        for area, skill in expected.items():
            with self.subTest(area=area):
                result = self.prepare(task_id="ruta-" + area, area=area)
                self.assertEqual(result["skill_directora"], skill)
                text = (self.base / result["briefing"]).read_text(encoding="utf-8")
                self.assertIn("../../reglas-comunes.md", text)
                self.assertIn("../../" + self.data["skills"][skill], text)
                for support in self.data["areas"][area].get("skills_apoyo", []):
                    self.assertIn("../../" + self.data["skills"][support], text)
                if area == "producto":
                    self.assertEqual(result["modo"], "briefing")
                    self.assertIn("Sólo briefing hasta identificar y leer", text)

    def test_cli_selects_continuity_without_loading_agenda_as_director(self):
        script = str(Path(harness.__file__).resolve())
        prepared = subprocess.run([sys.executable, script, "--base", str(self.base),
                                  "preparar", "entrega-1", "--area", "organizacion",
                                  "--skill", "continuidad-de-trabajo", "--objetivo", "Retomar un proyecto",
                                  "--entregable", "Entrega de continuidad", "--aceptacion", "Estado verificable"],
                                  capture_output=True, text=True, encoding="utf-8", check=True)
        result = json.loads(prepared.stdout)
        self.assertEqual(result["skill_directora"], "continuidad-de-trabajo")
        self.assertIn("planificar-dia", result["skills_apoyo"])
        self.assertNotIn("continuidad-de-trabajo", result["skills_apoyo"])
        text = (self.base / result["briefing"]).read_text(encoding="utf-8")
        self.assertIn("Skill directora: continuidad-de-trabajo", text)
        context = text.split("## Contexto mínimo", 1)[1].split("## Skills de apoyo disponibles", 1)[0]
        self.assertIn("continuidad-de-trabajo/SKILL.md", context)
        self.assertNotIn("planificar-dia/SKILL.md", context)
        supports = text.split("## Skills de apoyo disponibles", 1)[1]
        self.assertIn("No cargarlas automáticamente", supports)
        self.assertIn("planificar-dia/SKILL.md", supports)

    def test_skill_from_another_area_is_rejected_without_writes(self):
        with self.assertRaisesRegex(ValueError, "Skill no habilitada"):
            harness.prepare(self.base, "entrega-1", "organizacion", "Objetivo", "Entrega", "Prueba",
                            skill="producir-video")
        self.assertFalse((self.base / "operacion").exists())

    def test_invalid_id_and_private_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            self.prepare(task_id="../escape")
        for path in ("../escape", "privado/contexto.md", ".env", "ONIA-CENTRAL/AGENTS.md", "C:\\escape"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                harness.safe_path(self.base, path)
        self.data["contexto_comun"].append("privado/contexto.md")
        (self.base / "orquestacion.json").write_text(json.dumps(self.data), encoding="utf-8")
        self.assertFalse(harness.doctor(self.base)["ok"])
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse((self.base / "operacion").exists())

    def test_linked_operation_directory_is_not_written(self):
        outside = self.base / "otro-destino"
        outside.mkdir()
        try:
            os.symlink(outside, self.base / "operacion", target_is_directory=True)
        except OSError as exc:
            self.skipTest("El sistema no permite crear symlinks: " + str(exc))
        with self.assertRaisesRegex(ValueError, "enlace"):
            self.prepare()
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
