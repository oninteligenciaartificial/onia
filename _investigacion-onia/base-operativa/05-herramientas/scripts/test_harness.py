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
        source = harness.BASE / "04-operacion-agentes/orquestacion.json"
        manifest = self.base / "04-operacion-agentes/orquestacion.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_bytes(source.read_bytes())
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
        install = next(path for path in self.data["archivos_cloud"] if path.endswith("install.sh"))
        orchestration = next(path for path in self.data["contexto_comun"] if path.endswith("ORQUESTACION.md"))
        (self.base / install).unlink()
        (self.base / orchestration).unlink()
        result = harness.doctor(self.base)
        self.assertFalse(result["ok"])
        self.assertTrue(any(install in error and "checkout" in error for error in result["errores"]))
        self.assertTrue(any(orchestration in error for error in result["errores"]))
        self.assertFalse((self.base / "operacion").exists())

    def test_invalid_area_writes_nothing(self):
        with self.assertRaisesRegex(ValueError, "Área inválida"):
            self.prepare(area="inexistente")
        self.assertFalse((self.base / "operacion").exists())

    def test_ensayo_incompleto_no_crea_archivos(self):
        with self.assertRaisesRegex(ValueError, "Ensayo requiere"):
            harness.prepare(self.base, "ensayo-1", "desarrollo", "Evaluar", "Informe", "Control",
                            ensayo=True, investigacion="reglas-comunes.md",
                            capacidad="Audio y fuente documentada", control="Silencio decide",
                            leccion="No inferir RAM de pesos")
        self.assertFalse((self.base / "operacion").exists())
        result = subprocess.run([sys.executable, str(Path(harness.__file__).resolve()),
                                 "--base", str(self.base), "preparar", "ensayo-2",
                                 "--area", "desarrollo", "--objetivo", "Evaluar",
                                 "--entregable", "Informe", "--aceptacion", "Control", "--ensayo"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Ensayo requiere", json.loads(result.stdout)["error"])
        self.assertFalse((self.base / "operacion").exists())

    def test_ensayo_exige_fuente_existente_y_no_privada(self):
        fields = dict(ensayo=True, capacidad="Audio; fuente documentada", hipotesis="Cabe con RAM por medir",
                      control="Silencio: detener si inventa eventos", leccion="No inferir RAM de pesos")
        for source in ("inexistente.md", "privado/contexto.md", "../fuera.md"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                harness.prepare(self.base, "ensayo-1", "desarrollo", "Evaluar", "Informe", "Control",
                                investigacion=source, **fields)
        self.assertFalse((self.base / "operacion").exists())

    def test_cli_ensayo_completo_guarda_contexto_y_retoma(self):
        source = self.base / "investigacion.md"
        source.write_text("Licencia, compatibilidad, recursos y límites consultados.\n", encoding="utf-8")
        command = [sys.executable, str(Path(harness.__file__).resolve()), "--base", str(self.base),
                   "preparar", "ensayo-1", "--area", "desarrollo", "--objetivo", "Evaluar audio",
                   "--entregable", "Informe", "--aceptacion", "Control informado", "--ensayo",
                   "--investigacion", "investigacion.md", "--capacidad", "Audio y fuente oficial",
                   "--hipotesis", "RAM pico desconocida; medir", "--control", "Silencio: detener si inventa",
                   "--leccion", "No confundir pesos en disco con RAM"]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True)
        brief = (self.base / json.loads(result.stdout)["briefing"]).read_text(encoding="utf-8")
        for item in ("../../investigacion.md", "Audio y fuente oficial", "RAM pico desconocida",
                     "Silencio: detener", "No confundir pesos"):
            self.assertIn(item, brief)
        self.assertEqual(harness.resume(self.base, "ensayo-1")["tarea"]["estado"], "preparado")

    def test_datos_ensayo_sin_declaracion_se_rechazan(self):
        with self.assertRaisesRegex(ValueError, "declarar --ensayo"):
            harness.prepare(self.base, "ensayo-1", "desarrollo", "Objetivo", "Entrega", "Control",
                            investigacion="reglas-comunes.md")
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
        self.assertIn("Demo disponible", result["tarea"]["briefing"]["contenido"])
        self.assertIn("Ficha y embudo", result["tarea"]["briefing"]["contenido"])
        orchestration = next(path for path in self.data["contexto_comun"] if path.endswith("ORQUESTACION.md"))
        self.assertIn(os.path.relpath(orchestration, "operacion/encargos").replace("\\", "/"),
                      result["tarea"]["briefing"]["contenido"])
        self.assertNotIn("briefing", result)
        self.assertIn("no crean agentes", result["nota_harness"])

    def test_routes_and_product_scope(self):
        expected = {"marketing": "preparar-oferta-y-embudo", "video": "producir-video",
                    "desarrollo": "desarrollar-y-verificar", "automatizaciones": "automatizar-n8n",
                    "organizacion": "planificar-dia", "producto": "desarrollar-y-verificar"}
        for area, skill in expected.items():
            with self.subTest(area=area):
                result = self.prepare(task_id="ruta-" + area, area=area)
                self.assertEqual(result["skill_directora"], skill)
                text = (self.base / result["briefing"]).read_text(encoding="utf-8")
                brief_dir = "operacion/encargos"
                self.assertIn(os.path.relpath(self.data["reglas"], brief_dir).replace("\\", "/"), text)
                self.assertIn(os.path.relpath(self.data["skills"][skill], brief_dir).replace("\\", "/"), text)
                for support in self.data["areas"][area].get("skills_apoyo", []):
                    self.assertIn(os.path.relpath(self.data["skills"][support], brief_dir).replace("\\", "/"), text)
                if area == "producto":
                    self.assertEqual(result["modo"], "briefing")
                    self.assertIn("Sólo briefing hasta identificar y leer", text)

    def test_apoyo_explicito_solo_en_contexto_del_area(self):
        research = "tercero-matt-research"
        for area in self.data["areas"]:
            with self.subTest(area=area):
                result = harness.prepare(self.base, "apoyo-" + area, area, "Objetivo", "Entrega", "Prueba",
                                         apoyos=[research, research])
                self.assertEqual(result["apoyos_seleccionados"], [research])
                brief = (self.base / result["briefing"]).read_text(encoding="utf-8")
                context = brief.split("## Contexto mínimo", 1)[1].split("## Skills de apoyo disponibles", 1)[0]
                self.assertIn(self.data["skills"][research], context)
                self.assertNotIn(self.data["skills"]["tercero-addy-context"], context)
                self.assertIn(self.data["skills"][research], harness.resume(self.base, "apoyo-" + area)["tarea"]["briefing"]["contenido"])

    def test_apoyo_ajeno_no_escribe_encargo(self):
        with self.assertRaisesRegex(ValueError, "Apoyo no habilitado"):
            harness.prepare(self.base, "apoyo-invalido", "marketing", "Objetivo", "Entrega", "Prueba",
                            apoyos=["tercero-superpowers-debug"])
        self.assertFalse((self.base / "operacion").exists())

    def test_referencia_tercera_no_sustituye_directora(self):
        with self.assertRaisesRegex(ValueError, "como apoyo"):
            harness.prepare(self.base, "director-ajeno", "video", "Objetivo", "Entrega", "Prueba",
                            skill="tercero-matt-research")
        self.assertFalse((self.base / "operacion").exists())

    def test_todas_las_referencias_terceras_son_solo_apoyo(self):
        for name, path in self.data["skills"].items():
            if "compartibles/terceros/" not in path:
                continue
            self.assertTrue(name.startswith("tercero-"), name)
            for area, route in self.data["areas"].items():
                if name in route.get("skills_apoyo", []):
                    with self.subTest(area=area, apoyo=name), self.assertRaisesRegex(ValueError, "como apoyo"):
                        harness.prepare(self.base, "tercero-" + area, area, "Objetivo", "Entrega", "Prueba",
                                        skill=name)
        self.assertFalse((self.base / "operacion").exists())

    def test_humanizer_limitado_a_apoyo_marketing(self):
        result = harness.prepare(self.base, "humanizer-marketing", "marketing", "Revisar texto",
                                 "Borrador", "Criterio comprobable",
                                 apoyos=["tercero-marketing-humanizer"])
        brief = (self.base / result["briefing"]).read_text(encoding="utf-8")
        context = brief.split("## Contexto mínimo", 1)[1].split("## Skills de apoyo disponibles", 1)[0]
        self.assertIn(self.data["skills"]["tercero-marketing-humanizer"], context)
        with self.assertRaisesRegex(ValueError, "Apoyo no habilitado"):
            harness.prepare(self.base, "humanizer-video", "video", "Objetivo", "Entrega", "Prueba",
                            apoyos=["tercero-marketing-humanizer"])
        self.assertFalse((self.base / "operacion/encargos/humanizer-video.md").exists())

    def test_apoyos_visuales_cargan_solo_su_area(self):
        for area, key in (("video", "tercero-visual-hyperframes-plan"),
                          ("producto", "tercero-visual-uiux")):
            with self.subTest(area=area):
                result = harness.prepare(self.base, "visual-" + area, area, "Objetivo", "Entrega", "Prueba",
                                         apoyos=[key])
                brief = (self.base / result["briefing"]).read_text(encoding="utf-8")
                context = brief.split("## Contexto mínimo", 1)[1].split("## Skills de apoyo disponibles", 1)[0]
                self.assertIn(self.data["skills"][key], context)
        with self.assertRaisesRegex(ValueError, "Apoyo no habilitado"):
            harness.prepare(self.base, "ui-desarrollo", "desarrollo", "Objetivo", "Entrega", "Prueba",
                            apoyos=["tercero-visual-uiux"])
        self.assertFalse((self.base / "operacion/encargos/ui-desarrollo.md").exists())

    def test_cli_apoyo_seleccionado_se_recupera(self):
        script = str(Path(harness.__file__).resolve())
        command = [sys.executable, script, "--base", str(self.base)]
        result = subprocess.run(command + ["preparar", "apoyo-cli", "--area", "video",
                                "--objetivo", "Objetivo", "--entregable", "Entrega", "--aceptacion", "Revisado",
                                "--apoyo", "tercero-matt-research"], capture_output=True,
                                text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout)["apoyos_seleccionados"], ["tercero-matt-research"])
        resumed = subprocess.run(command + ["retomar", "apoyo-cli"], capture_output=True,
                                 text=True, encoding="utf-8", check=True)
        self.assertIn(self.data["skills"]["tercero-matt-research"], json.loads(resumed.stdout)["tarea"]["briefing"]["contenido"])

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
        (self.base / "04-operacion-agentes/orquestacion.json").write_text(json.dumps(self.data), encoding="utf-8")
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

    def test_shared_brief_uses_one_canonical_record_and_rejects_changes(self):
        result = harness.prepare(self.base, "compartido", "desarrollo", "Objetivo", "Entrega", "Control",
                                 shared=True)
        record = trabajo.task_path(self.base, "compartido")
        self.assertEqual(record.relative_to(self.base).as_posix(), "04-operacion-agentes/tareas/compartido.json")
        self.assertFalse((self.base / "operacion/tareas/compartido.json").exists())
        path = self.base / result["briefing"]
        self.assertEqual(harness.resume(self.base, "compartido")["tarea"]["briefing"]["contenido"], path.read_text(encoding="utf-8"))
        path.write_text("Brief alterado", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Briefing cambió"):
            harness.resume(self.base, "compartido")

    def test_cli_views_are_explicit_and_briefing_is_not_duplicated(self):
        self.prepare()
        trabajo.update(self.base, "pieza-1", "en_curso", "Avance", "", "Seguir", [], revision=1)
        script = str(Path(harness.__file__).resolve())
        command = [sys.executable, script, "--base", str(self.base)]
        brief = json.loads(subprocess.check_output(command + ["retomar", "pieza-1"], encoding="utf-8"))
        full = json.loads(subprocess.check_output(command + ["retomar", "pieza-1", "--completo"], encoding="utf-8"))
        history = json.loads(subprocess.check_output(command + ["historial", "pieza-1", "--revision", "1"], encoding="utf-8"))
        self.assertNotIn("historial", brief["tarea"])
        self.assertNotIn("briefing", brief)
        self.assertNotIn("briefing", full)
        self.assertEqual(full["tarea"], trabajo.read_task(self.base, "pieza-1"))
        self.assertEqual(history["historial"][0]["estado"], "preparado")
        self.assertIn("Audio y dimensiones revisados", brief["tarea"]["briefing"]["contenido"])

    def test_profile_recommends_without_claiming_requested_or_effective_model(self):
        result = harness.prepare(self.base, "perfil-1", "desarrollo", "Objetivo", "Entrega", "Prueba", profile="cambio-acotado")
        execution = result["tarea"]["ejecucion"]
        self.assertEqual(execution["recomendado"]["modelo"], "gpt-6.1-terra")
        self.assertIsNone(execution["solicitado"])
        self.assertIsNone(execution["observado"])
        with self.assertRaisesRegex(ValueError, "Perfil"):
            harness.prepare(self.base, "perfil-2", "desarrollo", "Objetivo", "Entrega", "Prueba", profile="inventado")
        self.assertFalse(trabajo.task_path(self.base, "perfil-2").exists())


if __name__ == "__main__":
    unittest.main()
