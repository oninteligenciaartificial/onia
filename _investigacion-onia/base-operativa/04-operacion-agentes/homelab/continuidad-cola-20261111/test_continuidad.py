import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pasada
import preparar
from pasada import cola
import worker_render as worker


class ContinuidadTest(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "cola"
        self.stop = self.base / "STOP"

    def test_empty_without_ssh_configuration_or_process(self):
        with patch.object(cola, "ssh_command", side_effect=AssertionError("SSH prohibido")), \
             patch.object(cola.subprocess, "run", side_effect=AssertionError("Proceso prohibido")):
            self.assertEqual(pasada.run(self.root, self.stop, ssh=True), {"estado": "sin_trabajo"})

    def test_stop_including_broken_link_before_creating_queue(self):
        self.stop.symlink_to(self.base / "ausente")
        with patch.object(cola, "Queue", side_effect=AssertionError("No abrir cola")):
            self.assertEqual(pasada.run(self.root, self.stop), {"estado": "detenido"})
        self.assertFalse(self.root.exists())

    def test_no_ssh_pending_backs_off_without_network(self):
        cola.Queue(self.root).enqueue("sintetico")
        with patch.object(cola, "remote", side_effect=AssertionError("SSH prohibido")):
            result = pasada.run(self.root, self.stop)
            self.assertEqual(result["motivo"], "ssh_deshabilitado")
            self.assertEqual(result["estado"], "reintento")
            self.assertEqual(pasada.run(self.root, self.stop)["estado"], "sin_trabajo")

    def test_recovery_same_id_after_offline_lost_response_and_restart(self):
        queue = cola.Queue(self.root)
        original = queue.enqueue("sintetico")
        home = self.base / "worker"
        home.mkdir(mode=0o700)
        with patch.object(cola.time, "time", return_value=100):
            offline = pasada.run(self.root, self.stop,
                                 transport=lambda _: (_ for _ in ()).throw(cola.RetryLater("conexion_no_disponible")))
        self.assertEqual(offline["proximo_intento"], 102)

        def lose(job):
            worker.execute(job, home)
            raise cola.RetryLater("sin_respuesta")

        with patch.object(worker, "render", side_effect=lambda _, target, lock: target.write_bytes(b"fixture")) as render, \
             patch.object(worker, "probe"):
            with patch.object(cola.time, "time", return_value=103):
                lost = pasada.run(self.root, self.stop, transport=lose)
            self.assertEqual(lost["proximo_intento"], 107)
            self.assertFalse((self.root / "sintetico.mp4").exists())
            with patch.object(cola.time, "time", return_value=108):
                result = pasada.run(self.root, self.stop, transport=lambda job: worker.execute(job, home))
            self.assertEqual(render.call_count, 1)
        self.assertEqual(result["estado"], "entregado")
        self.assertEqual(result["job"], original["job"])
        self.assertEqual(result["intentos"], 3)
        self.assertTrue(result["reutilizado"])
        self.assertEqual(result["sha256"], hashlib.sha256(b"fixture").hexdigest())
        before = (self.root / "sintetico.mp4").stat()
        self.assertEqual(pasada.run(self.root, self.stop)["estado"], "sin_trabajo")
        self.assertEqual((self.root / "sintetico.mp4").stat().st_mtime_ns, before.st_mtime_ns)

    def test_backoff_caps_at_300_seconds(self):
        queue = cola.Queue(self.root)
        record = queue.enqueue("sintetico")
        record["intentos"] = 20
        cola.save(self.root / "sintetico.json", record)
        with patch.object(cola.time, "time", return_value=100):
            result = pasada.run(self.root, self.stop)
        self.assertEqual(result["proximo_intento"], 400)

    def test_stop_checked_again_before_transport(self):
        queue = cola.Queue(self.root)
        queue.enqueue("sintetico")
        save = cola.save

        def stop_on_dispatch(path, record):
            save(path, record)
            self.stop.touch()

        with patch.object(cola, "save", side_effect=stop_on_dispatch), \
             patch.object(cola, "remote", side_effect=AssertionError("SSH prohibido")):
            result = pasada.run(self.root, self.stop, ssh=True)
        self.assertEqual(result["motivo"], "parada_solicitada")

    def test_queue_and_worker_locks_remain_exclusive(self):
        queue = cola.Queue(self.root)
        queue.enqueue("sintetico")
        with (self.root / "cola.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            self.assertEqual(pasada.run(self.root, self.stop, ssh=True), {"estado": "ocupado"})
        home = self.base / "worker"
        home.mkdir(mode=0o700)
        spool = worker.private_directory(home / "cola-cpu-v1")
        with (spool / "worker.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            result = pasada.run(self.root, self.stop, transport=lambda job: worker.execute(job, home))
        self.assertEqual(result["motivo"], "worker_ocupado")
        self.assertFalse((spool / "sintetico").exists())

    def test_bad_hash_is_blocked_and_cli_fails_safely(self):
        cola.Queue(self.root).enqueue("sintetico")
        result = pasada.run(self.root, self.stop, transport=lambda job: {
            "estado": "resultado", "id": job["id"], "reutilizado": False,
            "video": "Ynl0ZXM=", "sha256": "malo"})
        self.assertEqual(result["estado"], "bloqueado")
        self.assertFalse((self.root / "sintetico.mp4").exists())
        self.root.joinpath("corrupto.json").write_text("{")
        child = self.cli()
        self.assertEqual(child.returncode, 1)
        self.assertEqual(json.loads(child.stdout)["estado"], "fallo_local")
        self.assertNotIn(str(self.root), child.stdout + child.stderr)

    def cli(self, *extra, app=None, env=None):
        return subprocess.run([sys.executable, "-I", "-B", str(app or preparar.HERE / "pasada.py"),
                               "--root", str(self.root), "--stop", str(self.stop), *extra],
                              text=True, capture_output=True, check=False, timeout=5, env=env)

    def test_bundle_hashes_and_isolated_cli_and_no_overwrite(self):
        bundle = self.base / "paquete"
        hashes = preparar.prepare(bundle)
        self.assertTrue((bundle / "STOP").is_file())
        self.assertEqual((bundle / "config.env").read_text(), "ONIA_HOMELAB_SSH=0\n")
        for name, expected in hashes.items():
            self.assertEqual(hashlib.sha256((bundle / name).read_bytes()).hexdigest(), expected)
            self.assertEqual((bundle / name).stat().st_mode & 0o077, 0)
        self.assertEqual(hashes["app/cola_homelab.py"],
                         hashlib.sha256((preparar.HERE.parent / "cola_homelab.py").read_bytes()).hexdigest())
        child = self.cli("--sin-ssh", app=bundle / "app/pasada.py")
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(json.loads(child.stdout), {"estado": "sin_trabajo"})
        with self.assertRaises(FileExistsError):
            preparar.prepare(bundle)

    def test_cli_explicit_no_ssh_overrides_environment(self):
        cola.Queue(self.root).enqueue("sintetico")
        child = self.cli("--sin-ssh", env={**os.environ, "ONIA_HOMELAB_SSH": "1"})
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(json.loads(child.stdout)["motivo"], "ssh_deshabilitado")

    def test_non_private_queue_rejected(self):
        self.root.mkdir(mode=0o755)
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            pasada.run(self.root, self.stop)


if __name__ == "__main__":
    unittest.main(verbosity=2)
