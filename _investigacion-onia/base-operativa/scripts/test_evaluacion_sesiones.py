"""Pruebas mecánicas de fixtures; no son ejecuciones ni evaluación de un LLM."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
CASES = BASE / "continuidad/2026-11-06/evaluacion-sesiones/casos"


class EvaluationFixtureTests(unittest.TestCase):
    def test_frozen_sources_still_match_hash_and_bytes(self):
        manifest = json.loads((CASES / "congelacion.json").read_text(encoding="utf-8"))
        for relative, ref in manifest["archivos"].items():
            with self.subTest(path=relative):
                content = (CASES / relative).read_bytes()
                self.assertEqual(len(content), ref["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), ref["sha256"])

    def test_recovery_fixture_is_independent_and_preserves_hidden_rubric(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "caso"
            command = [sys.executable, "-B", str(CASES / "preparar.py"), "recuperacion", str(root)]
            prepared = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(prepared.returncode, 0, prepared.stderr)
            self.assertFalse(any(root.rglob("rubrica.json")))
            cli = [sys.executable, "-B", str(root / "scripts/harness.py"), "--base", str(root)]
            incomplete = subprocess.run(cli + ["retomar", "pedido-incompleto"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(incomplete.returncode, 0, incomplete.stderr)
            view = json.loads(incomplete.stdout)
            self.assertEqual(view["tarea"]["revision"], 4)
            self.assertEqual([d["id"] for d in view["tarea"]["decisiones"]], ["decision-v2"])
            self.assertNotIn("historial", view["tarea"])
            self.assertNotIn("briefing", view)
            missing = subprocess.run(cli + ["retomar", "pedido-completo"], capture_output=True)
            self.assertEqual(missing.returncode, 2)
            record = root / "continuidad/tareas/pedido-completo.json"
            before = record.read_bytes()
            repair = subprocess.run([sys.executable, "-B", str(root / "scripts/trabajo.py"), "--base", str(root),
                                     "recuperar", "pedido-completo", "--revision-esperada", "4", "--actor", "ejecutor"], capture_output=True)
            self.assertEqual(repair.returncode, 0, repair.stderr)
            self.assertEqual(record.read_bytes(), before)
            resumed = subprocess.run(cli + ["retomar", "pedido-completo"], capture_output=True)
            self.assertEqual(resumed.returncode, 0, resumed.stderr)
            # Existing destinations cannot be silently overwritten.
            repeated = subprocess.run(command, capture_output=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual(record.read_bytes(), before)

    def test_other_fixtures_copy_only_inputs_and_prompt(self):
        for case in ("codigo", "extraccion"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve() / "caso"
                subprocess.run([sys.executable, "-B", str(CASES / "preparar.py"), case, str(root)],
                               check=True, capture_output=True)
                expected = {p.relative_to(CASES / case / "entrada").as_posix()
                            for p in (CASES / case / "entrada").rglob("*") if p.is_file()} | {"ENCARGO.md"}
                self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}, expected)
                self.assertEqual((root / "ENCARGO.md").read_bytes(), (CASES / case / "prompt.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
