"""Pruebas con fixtures temporales; nunca modifica .agents del workspace."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("preparar-cloud.py")
spec = importlib.util.spec_from_file_location("preparar_cloud", SCRIPT)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class CloudBootstrapTests(unittest.TestCase):
    def setUp(self):
        # En Windows sandbox el TMP del sistema puede no ser escribible.
        fixture_parent = SCRIPT.parent.parent / "operacion/cloud-bootstrap-test"
        fixture_parent.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=fixture_parent)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.source = self.root / bootstrap.SOURCE
        for name in ("alpha", "beta"):
            skill = self.source / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")

    def require_symlink(self):
        probe = self.root / "symlink-probe"
        try:
            os.symlink("_investigacion-onia", probe, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Sistema sin permiso de symlink: {exc}")
        probe.unlink()

    def test_check_is_read_only_when_links_missing(self):
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        result, code = bootstrap.prepare(self.root)
        self.assertEqual(code, 1)
        self.assertEqual(result["created"], [])
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")))

    def test_conflict_preserves_foreign_file_and_creates_no_other_link(self):
        destination = self.root / bootstrap.DESTINATION
        destination.mkdir(parents=True)
        foreign = destination / "beta"
        foreign.write_text("trabajo ajeno", encoding="utf-8")
        result, code = bootstrap.prepare(self.root, install=True)
        self.assertEqual(code, 2)
        self.assertEqual(result["created"], [])
        self.assertFalse((destination / "alpha").exists())
        self.assertEqual(foreign.read_text(encoding="utf-8"), "trabajo ajeno")

    def test_install_failure_is_reported_without_copy_fallback(self):
        with patch.object(bootstrap.os, "symlink", side_effect=PermissionError("denegado")):
            result, code = bootstrap.prepare(self.root, install=True)
        self.assertEqual(code, 2)
        self.assertTrue(result["errors"])
        self.assertEqual(list((self.root / bootstrap.DESTINATION).iterdir()), [])

    def test_invalid_source_does_not_create_destination(self):
        (self.source / "invalid").mkdir()
        with self.assertRaises(ValueError):
            bootstrap.prepare(self.root, install=True)
        self.assertFalse((self.root / ".agents").exists())

    def test_relative_links_are_idempotent_and_keep_one_source(self):
        self.require_symlink()
        result, code = bootstrap.prepare(self.root, install=True)
        self.assertEqual(code, 0)
        self.assertEqual(len(result["created"]), 2)
        again, code = bootstrap.prepare(self.root, install=True)
        self.assertEqual(code, 0)
        self.assertEqual(again["created"], [])
        (self.source / "alpha/SKILL.md").write_text("cambio canónico", encoding="utf-8")
        link = self.root / bootstrap.DESTINATION / "alpha"
        self.assertEqual((link / "SKILL.md").read_text(encoding="utf-8"), "cambio canónico")
        self.assertFalse(os.path.isabs(os.readlink(link)))
        self.assertEqual(bootstrap.prepare(self.root)[1], 0)

    def test_broken_link_is_a_conflict(self):
        self.require_symlink()
        destination = self.root / bootstrap.DESTINATION
        destination.mkdir(parents=True)
        os.symlink("missing", destination / "beta", target_is_directory=True)
        result, code = bootstrap.prepare(self.root, install=True)
        self.assertEqual(code, 2)
        self.assertTrue(os.path.lexists(destination / "beta"))
        self.assertEqual(result["created"], [])

    def test_destination_parent_link_is_rejected(self):
        self.require_symlink()
        foreign = self.root / "foreign"
        foreign.mkdir()
        os.symlink("foreign", self.root / ".agents", target_is_directory=True)
        with self.assertRaises(ValueError):
            bootstrap.prepare(self.root, install=True)
        self.assertEqual(list(foreign.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
