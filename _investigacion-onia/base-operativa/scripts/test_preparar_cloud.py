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
        self.workspace = Path(self.tmp.name).resolve()
        self.root = self.workspace / "onia"
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

    @unittest.skipUnless(os.name == "nt", "Junctions requieren Windows")
    def test_explicit_windows_junctions_keep_one_source_and_are_idempotent(self):
        result, code = bootstrap.prepare(self.root, install=True, windows_junctions=True)
        self.assertEqual(code, 0, result)
        self.assertEqual(len(result["created"]), 2)
        (self.source / "alpha/SKILL.md").write_text("fuente única", encoding="utf-8")
        link = self.root / bootstrap.DESTINATION / "alpha"
        self.assertEqual(link.resolve(), self.source / "alpha")
        self.assertEqual((link / "SKILL.md").read_text(encoding="utf-8"), "fuente única")
        repeated, code = bootstrap.prepare(self.root, install=True, windows_junctions=True)
        self.assertEqual(code, 0)
        self.assertEqual(repeated["created"], [])

    def test_windows_junctions_are_explicit_and_not_a_check_side_effect(self):
        with self.assertRaises(ValueError):
            bootstrap.prepare(self.root, windows_junctions=True)
        self.assertFalse((self.root / ".agents").exists())

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
        self.assertFalse((self.workspace / ".agents").exists())

    def test_discovery_check_is_read_only(self):
        result, code = bootstrap.prepare(self.root, discovery_root=self.workspace)
        self.assertEqual(code, 1)
        self.assertEqual(len(result["skills"]), 2)
        self.assertEqual(len(result["discovery_skills"]), 2)
        self.assertEqual(result["created"], [])
        self.assertFalse((self.root / ".agents").exists())
        self.assertFalse((self.workspace / ".agents").exists())

    def test_workspace_aliases_are_relative_idempotent_and_share_source(self):
        self.require_symlink()
        result, code = bootstrap.prepare(self.root, install=True, discovery_root=self.workspace)
        self.assertEqual(code, 0)
        self.assertEqual(len(result["created"]), 4)
        for location in (self.root, self.workspace):
            for name in ("alpha", "beta"):
                link = location / bootstrap.DESTINATION / name
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), self.source / name)
                self.assertFalse(os.path.isabs(os.readlink(link)))
        (self.source / "alpha/SKILL.md").write_text("fuente única", encoding="utf-8")
        self.assertEqual((self.workspace / bootstrap.DESTINATION / "alpha/SKILL.md").read_text(encoding="utf-8"), "fuente única")
        repeated, code = bootstrap.prepare(self.root, install=True, discovery_root=self.workspace)
        self.assertEqual(code, 0)
        self.assertEqual(repeated["created"], [])
        self.assertEqual(bootstrap.prepare(self.root, discovery_root=self.workspace)[1], 0)

    def test_workspace_conflict_blocks_all_writes(self):
        destination = self.workspace / bootstrap.DESTINATION
        destination.mkdir(parents=True)
        foreign = destination / "beta"
        foreign.write_text("ajeno", encoding="utf-8")
        result, code = bootstrap.prepare(self.root, install=True, discovery_root=self.workspace)
        self.assertEqual(code, 2)
        self.assertEqual(result["created"], [])
        self.assertFalse((self.root / ".agents").exists())
        self.assertFalse(os.path.lexists(destination / "alpha"))
        self.assertEqual(foreign.read_text(encoding="utf-8"), "ajeno")

    def test_discovery_root_must_be_explicit_absolute_and_direct_parent(self):
        other = self.workspace / "other"
        other.mkdir()
        for invalid in (Path(".."), self.root, other, self.workspace.parent):
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                bootstrap.prepare(self.root, install=True, discovery_root=invalid)
        self.assertFalse((self.root / ".agents").exists())
        self.assertFalse((self.workspace / ".agents").exists())

    def test_workspace_destination_parent_link_is_rejected(self):
        self.require_symlink()
        foreign = self.workspace / "foreign"
        foreign.mkdir()
        os.symlink("foreign", self.workspace / ".agents", target_is_directory=True)
        with self.assertRaises(ValueError):
            bootstrap.prepare(self.root, install=True, discovery_root=self.workspace)
        self.assertEqual(list(foreign.iterdir()), [])
        self.assertFalse((self.root / ".agents").exists())

    def test_workspace_skill_link_to_foreign_source_is_not_replaced(self):
        self.require_symlink()
        foreign = self.workspace / "foreign"
        foreign.mkdir()
        destination = self.workspace / bootstrap.DESTINATION
        destination.mkdir(parents=True)
        os.symlink(foreign, destination / "alpha", target_is_directory=True)
        result, code = bootstrap.prepare(self.root, install=True, discovery_root=self.workspace)
        self.assertEqual(code, 2)
        self.assertEqual(result["created"], [])
        self.assertEqual((destination / "alpha").resolve(), foreign)
        self.assertFalse((self.root / ".agents").exists())

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
