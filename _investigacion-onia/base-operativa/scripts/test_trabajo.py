import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import trabajo


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        trabajo.create(self.base, "caso-1", "Entregar una pieza", "Preparar pieza")

    def test_cannot_complete_without_evidence(self):
        with self.assertRaises(ValueError):
            trabajo.update(self.base, "caso-1", "terminado", "Listo", "Revisado", "Nada", [])
        self.assertEqual(trabajo.read_task(self.base, "caso-1")["estado"], "preparado")

    def test_resume_in_new_process_and_detect_change(self):
        (self.base / "pieza.txt").write_text("Versión revisada", encoding="utf-8")
        trabajo.update(self.base, "caso-1", "terminado", "Pieza entregada", "Contenido revisado", "Medir resultado", ["pieza.txt"])
        out = subprocess.run([sys.executable, str(Path(trabajo.__file__)), "--base", str(self.base), "retomar", "caso-1"],
                             capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertIn('"estado": "terminado"', out.stdout)
        self.assertEqual(trabajo.resume(self.base, "caso-1")["advertencias"], [])
        (self.base / "pieza.txt").write_text("Otra versión", encoding="utf-8")
        self.assertTrue(trabajo.resume(self.base, "caso-1")["advertencias"])

    def test_duplicate_does_not_overwrite(self):
        with self.assertRaises(ValueError):
            trabajo.create(self.base, "caso-1", "Otro objetivo", "Otro paso")
        self.assertEqual(trabajo.read_task(self.base, "caso-1")["objetivo"], "Entregar una pieza")

    def test_paths_and_private_context_rejected(self):
        with self.assertRaises(ValueError):
            trabajo.task_path(self.base, "../escape")
        with self.assertRaises(ValueError):
            trabajo.evidence(self.base, "../escape.txt")
        (self.base / "privado").mkdir()
        (self.base / "privado" / "contexto.md").write_text("privado", encoding="utf-8")
        with self.assertRaises(ValueError):
            trabajo.evidence(self.base, "privado/contexto.md")

    def test_parallel_writer_does_not_destroy_lock(self):
        lock = trabajo.task_path(self.base, "caso-1").with_suffix(".lock")
        lock.touch()
        with self.assertRaises(ValueError):
            trabajo.update(self.base, "caso-1", "en_curso", "Trabajo", "", "Seguir", [])
        self.assertTrue(lock.exists())


if __name__ == "__main__":
    unittest.main()
