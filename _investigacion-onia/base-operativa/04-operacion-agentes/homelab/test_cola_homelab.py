import fcntl
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import cola_homelab as cola
import worker_render as worker


class ColaHomelabTest(unittest.TestCase):
    def test_recovers_saved_remote_video_after_lost_response(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            local, home = root / "local", root / "home"
            home.mkdir(mode=0o700)
            queue = cola.Queue(local)
            first = queue.enqueue("piloto")
            self.assertEqual(queue.enqueue("piloto"), first)

            def build(_source, target, _lock):
                target.write_bytes(b"video de prueba")

            def lose_response(job):
                worker.execute(job, home)
                raise cola.RetryLater("sin_respuesta")

            with patch.object(worker, "render", side_effect=build) as render, patch.object(worker, "probe"):
                lost = queue.tick(lose_response)
                self.assertEqual(lost["estado"], "reintento")
                self.assertEqual(queue.tick()["estado"], "sin_trabajo")
                with patch.object(cola.time, "time", return_value=lost["proximo_intento"] + 1):
                    recovered = cola.Queue(local).tick(lambda job: worker.execute(job, home))
                self.assertEqual(recovered["estado"], "entregado")
                self.assertTrue(recovered["reutilizado"])
                self.assertEqual(recovered["intentos"], 2)
                self.assertEqual((local / "piloto.mp4").read_bytes(), b"video de prueba")
                self.assertEqual(render.call_count, 1)
            self.assertEqual(cola.Queue(local).tick()["estado"], "sin_trabajo")

    def test_job_interrupted_after_local_video_resumes_without_overwrite(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            local, home = root / "local", root / "home"
            home.mkdir(mode=0o700)
            queue = cola.Queue(local)
            record = queue.enqueue("piloto")
            with patch.object(worker, "render", side_effect=lambda _, target, lock: target.write_bytes(b"video")), \
                 patch.object(worker, "probe"):
                result = worker.execute(record["job"], home)
                queue.deliver(record, result)
                output = local / "piloto.mp4"
                before = output.stat()
                queue_record = json.loads((local / "piloto.json").read_text())
                queue_record.update(estado="en_curso", intentos=1)
                cola.save(local / "piloto.json", queue_record)
                resumed = cola.Queue(local).tick(lambda job: worker.execute(job, home))
                self.assertEqual(resumed["estado"], "entregado")
                self.assertEqual(output.stat().st_ino, before.st_ino)
                self.assertEqual(output.stat().st_mtime_ns, before.st_mtime_ns)

    def test_locks_exclude_overlapping_dispatch_and_render(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            queue = cola.Queue(root / "local")
            home = root / "home"
            home.mkdir(mode=0o700)
            spool = worker.private_directory(home / "cola-cpu-v1")
            with (queue.root / "cola.lock").open("a") as local_lock, (spool / "worker.lock").open("a") as remote_lock:
                fcntl.flock(local_lock, fcntl.LOCK_EX)
                fcntl.flock(remote_lock, fcntl.LOCK_EX)
                self.assertEqual(queue.tick(), {"estado": "ocupado"})
                job = {"id": "piloto", "tipo": "render-sintetico-v1"}
                self.assertEqual(worker.execute(job, home), {"estado": "ocupado"})
                self.assertFalse((spool / "piloto").exists())

    def test_corrupt_response_cannot_become_delivered(self):
        with TemporaryDirectory() as directory:
            queue = cola.Queue(Path(directory))
            queue.enqueue("piloto")
            record = queue.tick(lambda job: {
                "estado": "resultado", "id": job["id"], "reutilizado": False,
                "sha256": "incorrecto", "video": "Ynl0ZXM=",
            })
            self.assertEqual(record["estado"], "bloqueado")
            self.assertFalse((queue.root / "piloto.mp4").exists())
