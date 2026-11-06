import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import trabajo


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        trabajo.create(self.base, "caso-1", "Entregar una pieza", "Preparar pieza")
        (self.base / "pieza.txt").write_text("Versión revisada", encoding="utf-8")

    def change(self, **kwargs):
        data = dict(status="en_curso", result="Trabajo", check="", next_step="Seguir", files=[], revision=1)
        data.update(kwargs)
        return trabajo.update(self.base, "caso-1", **data)

    def ready(self):
        return self.change(status="para_revision", result="Pieza preparada", check="Contenido revisado",
                           files=["pieza.txt"], verification="correcta")

    def test_acceptance_requires_review_and_success(self):
        for fields in (dict(status="para_revision"), dict(status="aceptado"),
                       dict(status="para_revision", files=["pieza.txt"], verification="fallo", check="Falló")):
            with self.assertRaises(ValueError):
                self.change(**fields)
        with self.assertRaises(ValueError):
            trabajo.accept(self.base, "caso-1", 1, "Revisor", "Criterio")
        row = self.ready()
        self.assertEqual(row["estado"], "para_revision")
        row = trabajo.accept(self.base, "caso-1", 2, "Revisor", "Resultado cotejado")
        self.assertEqual(row["estado"], "aceptado")
        self.assertEqual(row["revision"], 3)
        self.assertEqual(len(row["historial"]), 2)

    def test_resume_in_new_process_and_reject_corruption(self):
        self.ready()
        args = [sys.executable, str(Path(trabajo.__file__)), "--base", str(self.base), "retomar", "caso-1"]
        good = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)["tarea"]["estado"], "para_revision")
        (self.base / "pieza.txt").write_text("Otra versión", encoding="utf-8")
        before = trabajo.task_path(self.base, "caso-1").read_bytes()
        bad = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(bad.returncode, 2)
        with self.assertRaisesRegex(ValueError, "Evidencia cambió"):
            self.change(revision=2)
        self.assertEqual(before, trabajo.task_path(self.base, "caso-1").read_bytes())

    def test_revision_required_and_stale_writer_cannot_overwrite(self):
        self.change()
        before = trabajo.task_path(self.base, "caso-1").read_bytes()
        for revision in (1, None, True):
            with self.assertRaisesRegex(ValueError, "Revisión"):
                self.change(revision=revision)
        self.assertEqual(before, trabajo.task_path(self.base, "caso-1").read_bytes())

    def test_previous_evidence_remains_checked(self):
        self.ready()
        self.change(revision=2, files=[], result="Nueva etapa")
        (self.base / "pieza.txt").unlink()
        with self.assertRaises(ValueError):
            trabajo.resume(self.base, "caso-1")

    def test_duplicate_and_ambiguous_ids_preserve_data(self):
        with self.assertRaises(ValueError):
            trabajo.create(self.base, "caso-1", "Otro", "Seguir", shared=True)
        local, shared = trabajo.paths(self.base, "caso-1")
        shared.parent.mkdir(parents=True)
        shared.write_bytes(local.read_bytes())
        with self.assertRaisesRegex(ValueError, "ambiguo"):
            trabajo.resume(self.base, "caso-1")
        self.assertEqual(local.read_bytes(), shared.read_bytes())

    def test_paths_and_private_context_rejected(self):
        for name in ("../escape.txt", "privado/contexto.md", "PRIVADO/x", ".env", "cert.key", "ONIA-CENTRAL/x", "C:\\escape"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                trabajo.evidence(self.base, name)
        with self.assertRaises(ValueError):
            trabajo.task_path(self.base, "../escape")

    def test_symlinked_evidence_and_storage_rejected(self):
        try:
            os.symlink(self.base / "pieza.txt", self.base / "enlace.txt")
        except OSError as exc:
            self.skipTest(str(exc))
        with self.assertRaises(ValueError):
            trabajo.evidence(self.base, "enlace.txt")
        target = self.base / "otro"
        target.mkdir()
        os.symlink(target, self.base / "continuidad", target_is_directory=True)
        with self.assertRaises(ValueError):
            trabajo.create(self.base, "nuevo", "Objetivo", "Seguir", shared=True)
        self.assertEqual(list(target.iterdir()), [])

    def test_shared_task_survives_copy_without_private_operation(self):
        trabajo.create(self.base, "compartida", "Objetivo recuperable", "Próximo paso", shared=True, briefing="# Alcance\n")
        evidence = self.base / "continuidad/evidencias/a.txt"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b"evidencia ficticia\n")
        trabajo.update(self.base, "compartida", "para_revision", "Resultado ficticio", "Cotejado", "Revisar",
                       ["continuidad/evidencias/a.txt"], revision=1, verification="correcta")
        with tempfile.TemporaryDirectory() as target:
            shutil.copytree(self.base / "continuidad", Path(target) / "continuidad")
            row = trabajo.resume(Path(target), "compartida")["tarea"]
            self.assertEqual(row["revision"], 2)
            self.assertEqual(row["objetivo"], "Objetivo recuperable")
            self.assertFalse((Path(target) / "operacion").exists())
        with self.assertRaises(ValueError):
            trabajo.update(self.base, "compartida", "en_curso", "x", "", "Seguir",
                           ["operacion/tareas/caso-1.json"], revision=2)

    def test_creation_interruption_recovers_from_canonical_record(self):
        with patch.object(trabajo, "materialize", side_effect=OSError("Interrupción simulada")):
            with self.assertRaises(OSError):
                trabajo.create(self.base, "interrumpida", "Objetivo", "Continuar", briefing="# Canónico\n")
        before = trabajo.task_path(self.base, "interrumpida").read_bytes()
        with self.assertRaises(ValueError):
            trabajo.resume(self.base, "interrumpida")
        trabajo.recover(self.base, "interrumpida", 1)
        trabajo.recover(self.base, "interrumpida", 1)
        self.assertEqual(before, trabajo.task_path(self.base, "interrumpida").read_bytes())
        self.assertEqual(trabajo.resume(self.base, "interrumpida")["tarea"]["briefing"]["contenido"], "# Canónico\n")

    def test_modified_brief_is_not_rehashed_or_overwritten(self):
        trabajo.create(self.base, "con-brief", "Objetivo", "Continuar", briefing="# Canónico\n")
        path = trabajo.brief_path(self.base, "con-brief")
        path.write_text("# Alterado\n", encoding="utf-8")
        for action in (lambda: trabajo.resume(self.base, "con-brief"),
                       lambda: trabajo.recover(self.base, "con-brief", 1)):
            with self.assertRaises(ValueError):
                action()
        self.assertEqual(path.read_text(encoding="utf-8"), "# Alterado\n")

    def test_schema_identity_and_revision_validation(self):
        path = trabajo.task_path(self.base, "caso-1")
        original = json.loads(path.read_text(encoding="utf-8"))
        for key, value in (("id", "otro"), ("schema", 9), ("schema", True), ("revision", True), ("evidencias", {})):
            row = dict(original, **{key: value})
            path.write_text(json.dumps(row), encoding="utf-8")
            with self.assertRaises(ValueError):
                trabajo.resume(self.base, "caso-1")

    def test_legacy_remains_readable_and_migration_does_not_accept(self):
        row = trabajo.read_task(self.base, "caso-1")
        for key in ("revision", "compartible", "verificacion", "briefing", "aceptacion"):
            row.pop(key)
        row.update(schema=1, estado="terminado")
        path = trabajo.task_path(self.base, "caso-1")
        path.write_text(json.dumps(row), encoding="utf-8")
        before = path.read_bytes()
        self.assertTrue(trabajo.resume(self.base, "caso-1")["advertencias"])
        self.assertEqual(before, path.read_bytes())
        with self.assertRaises(ValueError):
            self.change(revision=0)
        migrated = trabajo.migrate(self.base, "caso-1", 0)
        self.assertEqual(migrated["estado"], "en_espera")
        self.assertIsNone(migrated["aceptacion"])
        self.assertEqual(migrated["historial"][-1]["estado"], "terminado")

    def test_original_v1_fixture_with_reused_path_migrates_without_losing_history(self):
        fixture = json.loads((Path(__file__).parent / "fixtures/legacy-v1.json").read_text(encoding="utf-8"))
        path = trabajo.task_path(self.base, "legacy-v1")
        path.write_text(json.dumps(fixture["registro"]), encoding="utf-8")
        (self.base / "informe.txt").write_bytes(fixture["evidencia_actual"].encode("utf-8"))
        self.assertEqual(trabajo.resume(self.base, "legacy-v1")["tarea"]["estado"], "terminado")
        migrated = trabajo.migrate(self.base, "legacy-v1", 0)
        self.assertEqual(migrated["historial"][:-1], fixture["registro"]["historial"])
        self.assertEqual(migrated["evidencias"], fixture["registro"]["evidencias"])
        self.assertEqual(trabajo.resume(self.base, "legacy-v1")["tarea"]["estado"], "en_espera")

    def test_improved_delivery_preserves_both_versions_and_next_step(self):
        self.ready()
        blocked = self.change(revision=2, status="en_espera", result="Falta revisión", next_step="Mejorar")
        self.assertEqual(len(blocked["evidencias"]), 1)
        (self.base / "pieza-v2.txt").write_bytes(b"Version mejorada\n")
        row = self.change(revision=3, status="para_revision", result="Segunda entrega",
                          check="Ambas versiones cotejadas", files=["pieza-v2.txt"],
                          verification="correcta", next_step="Aceptar segunda entrega")
        resumed = trabajo.resume(self.base, "caso-1")["tarea"]
        self.assertEqual([e["archivo"] for e in resumed["evidencias"]], ["pieza.txt", "pieza-v2.txt"])
        self.assertEqual(resumed["proximo_paso"], "Aceptar segunda entrega")
        self.assertEqual(row["revision"], 4)

    def test_parallel_writer_does_not_destroy_lock(self):
        lock = self.base / "operacion/bloqueos/caso-1.lock"
        lock.touch()
        with self.assertRaises(ValueError):
            self.change()
        self.assertTrue(lock.exists())

    def test_two_processes_same_revision_only_one_wins(self):
        command = [sys.executable, str(Path(trabajo.__file__)), "--base", str(self.base),
                   "actualizar", "caso-1", "--estado", "en_curso", "--resultado", "Avance",
                   "--siguiente", "Seguir", "--revision-esperada", "1"]
        children = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for child in children:
            child.communicate(timeout=20)
        self.assertEqual(sorted(c.returncode for c in children), [0, 2])
        self.assertEqual(trabajo.read_task(self.base, "caso-1")["revision"], 2)

    def test_two_independent_shared_tasks_can_be_created_in_parallel(self):
        prefix = [sys.executable, str(Path(trabajo.__file__)), "--base", str(self.base), "crear"]
        children = [subprocess.Popen(prefix + [task_id, "--compartible", "--objetivo", task_id,
                    "--siguiente", "Continuar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    for task_id in ("paralelo-a", "paralelo-b")]
        for child in children:
            child.communicate(timeout=20)
        self.assertEqual([c.returncode for c in children], [0, 0])
        for task_id in ("paralelo-a", "paralelo-b"):
            self.assertEqual(trabajo.resume(self.base, task_id)["tarea"]["objetivo"], task_id)

    def test_failed_atomic_replace_keeps_previous_record(self):
        before = trabajo.task_path(self.base, "caso-1").read_bytes()
        with patch.object(trabajo.os, "replace", side_effect=OSError("Disco simulado")):
            with self.assertRaises(OSError):
                self.change()
        self.assertEqual(before, trabajo.task_path(self.base, "caso-1").read_bytes())


if __name__ == "__main__":
    unittest.main()
