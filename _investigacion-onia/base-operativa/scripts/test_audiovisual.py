"""Contrato de ingesta: mocks y medios sintéticos propios, nunca reels reales."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import audiovisual


PUBLIC_URL = "https://www.instagram.com/reel/Test_01-/"
PRIVATE_MARKER = "private-marker-do-not-publish"


class IngestTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="onia-av-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.media = self.root / "private-input.mp4"
        self.media.write_bytes(b"synthetic-placeholder")
        self.output = self.root / "receipt.json"

    def probe(self):
        return {
            "format": {"duration": "1.0", "start_time": "0.0",
                       "size": str(self.media.stat().st_size),
                       "filename": str(self.media), "tags": {"comment": PRIVATE_MARKER}},
            "streams": [
                {"index": 0, "codec_type": "video", "codec_name": "h264",
                 "width": 32, "height": 32, "duration": "1", "start_time": "0",
                 "r_frame_rate": "10/1", "avg_frame_rate": "10/1",
                 "tags": {"title": PRIVATE_MARKER}, "private_data": str(self.root)},
                {"index": 1, "codec_type": "audio", "codec_name": "aac",
                 "sample_rate": "44100", "channels": 1, "duration": "1"}],
            "filename": str(self.media), "tags": {"artist": PRIVATE_MARKER}}

    def result(self, raw=None, *, returncode=0, stdout=None):
        if stdout is None:
            stdout = json.dumps(self.probe() if raw is None else raw).encode("utf-8")
        return subprocess.CompletedProcess([], returncode, stdout, PRIVATE_MARKER.encode())

    def ingest(self, **kwargs):
        return audiovisual.ingest(self.root, self.media.name, PUBLIC_URL, **kwargs)

    def cli(self, **overrides):
        values = {"raiz-medios": self.root, "archivo": self.media.name,
                  "url": PUBLIC_URL, "raiz-salida": self.root, "salida": self.output.name}
        values.update(overrides)
        args = [item for key, value in values.items() for item in ("--" + key, str(value))]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = audiovisual.main(args)
        return code, out.getvalue(), err.getvalue()

    def assert_private_absent(self, value):
        serialized = json.dumps(value, ensure_ascii=False)
        for forbidden in (PRIVATE_MARKER, self.media.name, str(self.root), "filename", "tags"):
            self.assertNotIn(forbidden, serialized)

    def assert_failed_cli(self, **overrides):
        code, out, err = self.cli(**overrides)
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIsInstance(json.loads(err)["error"], str)
        self.assert_private_absent(err)
        self.assertFalse(self.output.exists())

    def test_receipt_is_instrumental_and_sanitized_without_copy(self):
        before = self.media.read_bytes()
        with patch.object(audiovisual.subprocess, "run", return_value=self.result()) as run:
            receipt = self.ingest()
        self.assertIs(receipt["capacidad_av_acreditada"], False)
        self.assertEqual(receipt["original"], {"sha256": hashlib.sha256(before).hexdigest(),
                                              "bytes": len(before)})
        self.assertTrue(receipt["metadata"]["audio_presente"])
        self.assertIs(receipt["metadata"]["pts_decodificados"], False)
        self.assertIs(receipt["metadata"]["decodificacion_completa"], False)
        self.assertTrue(all(row == {"estado": "pendiente", "observaciones": []}
                            for row in receipt["atributos"].values()))
        self.assertEqual(receipt["afirmaciones_contrastadas"], [])
        self.assertEqual(receipt["conocimiento_aceptado"], [])
        self.assert_private_absent(receipt)
        self.assertEqual(self.media.read_bytes(), before)
        self.assertEqual(list(self.root.iterdir()), [self.media])
        args, kwargs = run.call_args
        command = args[0]
        self.assertEqual(command[command.index("-protocol_whitelist") + 1], "file")
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertGreater(kwargs["timeout"], 0)
        self.assertFalse(kwargs.get("shell", False))

    def test_valid_public_urls_are_canonical_and_only_declared(self):
        for url in (PUBLIC_URL, "https://instagram.com/reel/Test_01-",
                    "https://www.instagram.com/reel/A/"):
            with self.subTest(url=url):
                result = audiovisual.public_identity(url)
                self.assertEqual(result["plataforma"], "instagram")
                self.assertTrue(result["url"].startswith("https://www.instagram.com/reel/"))
                self.assertEqual(result["asociacion"], "declarada_por_operador_no_verificada_en_red")

    def test_private_or_wrong_public_urls_are_rejected(self):
        for url in ("http://instagram.com/reel/A/", "https://user:secret@instagram.com/reel/A/",
                    "https://instagram.com/reel/A/?token=secret", "https://instagram.com/reel/A/#x",
                    "https://instagram.com.attacker.invalid/reel/A/",
                    "https://instagram.com@attacker.invalid/reel/A/",
                    "https://instagram.com:443/reel/A/", "https://instagram.com/p/A/",
                    "https://instagram.com/reel/", "https://instagram.com/reel/A/extra",
                    "https://instagram.com/reel/A%2FB/", "https://instagram.com/reel/" + "A" * 65):
            with self.subTest(url=url), self.assertRaises(ValueError):
                audiovisual.public_identity(url)

    def test_invalid_roots_and_relative_paths_never_probe(self):
        with patch.object(audiovisual.subprocess, "run") as run:
            for root in (self.root / "missing", self.media):
                with self.subTest(root=root), self.assertRaises((ValueError, OSError)):
                    audiovisual.ingest(root, self.media.name, PUBLIC_URL)
            for relative in ("../outside.mp4", "..\\outside.mp4", str(self.media),
                             "C:\\outside.mp4", "", "missing.mp4", "privado/a.mp4",
                             "ONIA-CENTRAL/a.mp4", ".env.mp4"):
                with self.subTest(relative=relative), self.assertRaises((ValueError, OSError)):
                    audiovisual.ingest(self.root, relative, PUBLIC_URL)
            run.assert_not_called()

    def test_root_and_input_reparse_points_are_rejected(self):
        real_lstat = Path.lstat
        for target in (self.root, self.media):
            def flagged(path, *args, **kwargs):
                if path == target:
                    return SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
                return real_lstat(path, *args, **kwargs)
            with self.subTest(target=target), patch.object(Path, "lstat", flagged):
                with patch.object(audiovisual.subprocess, "run") as run:
                    with self.assertRaisesRegex(ValueError, "enlace|reparse"):
                        self.ingest()
                    run.assert_not_called()

    def test_real_symlink_input_and_root_are_rejected_if_host_allows(self):
        link = self.root / "linked.mp4"
        root_link = self.root / "linked-root"
        try:
            link.symlink_to(self.media)
            root_link.symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("Host no permite crear symlinks: " + type(exc).__name__)
        with patch.object(audiovisual.subprocess, "run") as run:
            for root, relative in ((self.root, link.name), (root_link, self.media.name)):
                with self.subTest(root=root), self.assertRaisesRegex(ValueError, "enlace|reparse"):
                    audiovisual.ingest(root, relative, PUBLIC_URL)
            run.assert_not_called()

    def test_empty_oversized_directory_and_wrong_suffix_are_rejected(self):
        empty = self.root / "empty.mp4"
        empty.write_bytes(b"")
        directory = self.root / "directory.mp4"
        directory.mkdir()
        wrong = self.root / "file.txt"
        wrong.write_bytes(b"abc")
        with patch.object(audiovisual.subprocess, "run") as run:
            for candidate in (empty, directory, wrong):
                with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                    audiovisual.ingest(self.root, candidate.name, PUBLIC_URL)
            with patch.object(audiovisual, "MAX_BYTES", self.media.stat().st_size - 1):
                with self.assertRaisesRegex(ValueError, "límite"):
                    self.ingest()
            run.assert_not_called()

    def test_invalid_bytes_and_nonfinite_durations_fail_without_receipt(self):
        cases = []
        for value in (0, -1, True, "2.5", "NaN", "Infinity", "-Infinity", "99999"):
            raw = self.probe()
            raw["format"]["size"] = value
            cases.append(("bytes", value, raw))
        for key in ("duration", "start_time"):
            for value in ("NaN", "Infinity", "-Infinity", True):
                raw = self.probe()
                raw["format"][key] = value
                cases.append((key, value, raw))
        for value in (0, -1, None):
            raw = self.probe()
            raw["format"]["duration"] = value
            cases.append(("duration", value, raw))
        for field, value, raw in cases:
            with self.subTest(field=field, value=value):
                with patch.object(audiovisual.subprocess, "run", return_value=self.result(raw)):
                    self.assert_failed_cli()

    def test_invalid_stream_metadata_is_rejected(self):
        changes = (("index", True), ("index", -1), ("codec_name", "../../private"),
                   ("duration", -1), ("duration", "NaN"), ("start_time", "Infinity"),
                   ("width", 1.5), ("height", True), ("r_frame_rate", "NaN"))
        for key, value in changes:
            raw = self.probe()
            raw["streams"][0][key] = value
            with self.subTest(key=key, value=value):
                with patch.object(audiovisual.subprocess, "run", return_value=self.result(raw)):
                    self.assert_failed_cli()
        for streams in ([], self.probe()["streams"] * 17,
                        [self.probe()["streams"][1]], [self.probe()["streams"][0]] * 2):
            raw = self.probe()
            raw["streams"] = streams
            with self.subTest(streams_count=len(streams)):
                with patch.object(audiovisual.subprocess, "run", return_value=self.result(raw)):
                    self.assert_failed_cli()

    def test_malformed_nested_probe_structure_is_a_clean_failure(self):
        cases = [{"format": None, "streams": self.probe()["streams"]},
                 {"format": [], "streams": self.probe()["streams"]}]
        for entry in (None, "unexpected", []):
            raw = self.probe()
            raw["streams"] = [entry]
            cases.append(raw)
        for raw in cases:
            with self.subTest(raw=raw):
                with patch.object(audiovisual.subprocess, "run", return_value=self.result(raw)):
                    self.assert_failed_cli()

    def test_missing_audio_and_unknown_stream_duration_remain_explicit(self):
        raw = self.probe()
        raw["streams"] = raw["streams"][:1]
        raw["streams"][0]["duration"] = "N/A"
        raw["streams"][0].pop("start_time")
        with patch.object(audiovisual.subprocess, "run", return_value=self.result(raw)):
            receipt = self.ingest()
        self.assertIs(receipt["metadata"]["audio_presente"], False)
        self.assertIsNone(receipt["metadata"]["pistas"][0]["duracion_s"])
        self.assertIsNone(receipt["metadata"]["pistas"][0]["inicio_s"])
        self.assertIs(receipt["capacidad_av_acreditada"], False)

    def test_mutation_with_same_size_and_restored_mtime_is_rejected(self):
        original_stat = self.media.stat()
        result = self.result()
        def mutate(*args, **kwargs):
            self.media.write_bytes(b"X" * original_stat.st_size)
            os.utime(self.media, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
            return result
        with patch.object(audiovisual.subprocess, "run", side_effect=mutate):
            self.assert_failed_cli()

    def test_size_mutation_during_probe_is_rejected(self):
        result = self.result()
        def mutate(*args, **kwargs):
            self.media.write_bytes(b"changed")
            return result
        with patch.object(audiovisual.subprocess, "run", side_effect=mutate):
            self.assert_failed_cli()

    def test_timeouts_and_probe_failures_do_not_leak_stderr_or_create_output(self):
        for exc in (subprocess.TimeoutExpired([PRIVATE_MARKER], 1,
                                              output=PRIVATE_MARKER.encode(), stderr=PRIVATE_MARKER.encode()),
                    FileNotFoundError(PRIVATE_MARKER)):
            with self.subTest(error=type(exc).__name__):
                with patch.object(audiovisual.subprocess, "run", side_effect=exc):
                    self.assert_failed_cli()
        for result in (self.result(returncode=1), self.result(stdout=b"x" * (1024 * 1024 + 1)),
                       self.result(stdout=PRIVATE_MARKER.encode()), self.result(stdout=b"\xff"),
                       self.result(stdout=b"[]"), self.result(stdout=b"null")):
            with self.subTest(returncode=result.returncode, output_size=len(result.stdout)):
                with patch.object(audiovisual.subprocess, "run", return_value=result):
                    self.assert_failed_cli()

    def test_invalid_timeouts_do_not_start_probe(self):
        with patch.object(audiovisual.subprocess, "run") as run:
            for value in (0, -1, True, float("nan"), float("inf"), 61):
                with self.subTest(timeout=value), self.assertRaises(ValueError):
                    self.ingest(timeout=value)
            run.assert_not_called()

    def test_cli_writes_new_sanitized_receipt_and_preserves_original(self):
        original = self.media.read_bytes()
        with patch.object(audiovisual.subprocess, "run", return_value=self.result()):
            code, out, err = self.cli()
        self.assertEqual((code, err), (0, ""))
        self.assertIs(json.loads(out)["capacidad_av_acreditada"], False)
        receipt = json.loads(self.output.read_text(encoding="utf-8"))
        self.assert_private_absent(receipt)
        self.assertIs(receipt["capacidad_av_acreditada"], False)
        self.assertEqual(self.media.read_bytes(), original)
        self.assertEqual(set(self.root.iterdir()), {self.media, self.output})

    def test_existing_output_is_preserved_before_any_probe(self):
        self.output.write_bytes(b"previous-evidence")
        with patch.object(audiovisual.subprocess, "run") as run:
            code, out, err = self.cli()
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("no se sobrescribió", json.loads(err)["error"])
        self.assertEqual(self.output.read_bytes(), b"previous-evidence")
        run.assert_not_called()

    def test_save_new_rejects_overwrite_and_invalid_output_paths(self):
        self.output.write_bytes(b"previous-evidence")
        with self.assertRaises(FileExistsError):
            audiovisual.save_new(self.root, self.output.name, {"schema": 1})
        self.assertEqual(self.output.read_bytes(), b"previous-evidence")
        for relative in ("../escape.json", "out.txt", "missing/out.json", str(self.output)):
            with self.subTest(relative=relative), self.assertRaises((ValueError, OSError)):
                audiovisual.save_new(self.root, relative, {"schema": 1})

    def test_save_new_nonfinite_data_creates_no_output(self):
        for value in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                audiovisual.save_new(self.root, self.output.name, {"invalid": value})
            self.assertFalse(self.output.exists())

    def test_output_created_during_probe_is_not_overwritten(self):
        result = self.result()
        def publish(*args, **kwargs):
            self.output.write_bytes(b"concurrent-evidence")
            return result
        with patch.object(audiovisual.subprocess, "run", side_effect=publish):
            code, out, err = self.cli()
        self.assertEqual((code, out), (2, ""))
        self.assertEqual(json.loads(err)["error"], "FileExistsError")
        self.assertEqual(self.output.read_bytes(), b"concurrent-evidence")

    def test_partial_output_write_failure_leaves_no_receipt(self):
        real_open = os.fdopen

        class PartialWriteFailure:
            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                return self

            def write(self, data):
                self.stream.write(data[:12])
                raise OSError(28, PRIVATE_MARKER)

            def __exit__(self, *args):
                self.stream.close()

        def failing_open(descriptor, mode="r", *args, **kwargs):
            return PartialWriteFailure(real_open(descriptor, mode, *args, **kwargs))

        with patch.object(audiovisual.subprocess, "run", return_value=self.result()):
            with patch.object(audiovisual.os, "fdopen", failing_open):
                self.assert_failed_cli()
        self.assertEqual(list(self.root.glob(".av-ingesta-*")), [])

    def test_atomic_publication_failure_removes_only_own_temporary(self):
        with patch.object(audiovisual.subprocess, "run", return_value=self.result()):
            with patch.object(audiovisual.os, "link", side_effect=OSError(28, PRIVATE_MARKER)):
                self.assert_failed_cli()
        self.assertEqual(list(self.root.glob(".av-ingesta-*")), [])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                     "FFmpeg/ffprobe existentes no disponibles; no instalar")
class SyntheticMediaTests(unittest.TestCase):
    def test_one_second_tone_and_silent_video_with_real_ffprobe(self):
        with tempfile.TemporaryDirectory(prefix="onia-av-synthetic-") as directory:
            root = Path(directory).resolve()
            for audio in (True, False):
                with self.subTest(audio=audio):
                    media = root / ("synthetic-av.mp4" if audio else "synthetic-silent.mp4")
                    args = [shutil.which("ffmpeg"), "-nostdin", "-v", "error", "-n",
                            "-f", "lavfi", "-i", "color=c=blue:s=32x32:r=10:d=1"]
                    if audio:
                        args += ["-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                                 "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac"]
                    args += ["-c:v", "mpeg4", "-q:v", "5", "-t", "1",
                             "-metadata", "comment=" + PRIVATE_MARKER, str(media)]
                    generated = subprocess.run(args, stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
                    self.assertEqual(generated.returncode, 0, generated.stderr.decode(errors="replace"))
                    before = media.read_bytes()
                    receipt = audiovisual.ingest(root, media.name, PUBLIC_URL, ffprobe=shutil.which("ffprobe"))
                    self.assertIs(receipt["capacidad_av_acreditada"], False)
                    self.assertIs(receipt["metadata"]["audio_presente"], audio)
                    self.assertAlmostEqual(receipt["metadata"]["duracion_contenedor_s"], 1, delta=0.1)
                    self.assertEqual(receipt["metadata"]["pistas"][0]["ancho"], 32)
                    self.assertEqual(receipt["original"]["sha256"], hashlib.sha256(before).hexdigest())
                    self.assertEqual(media.read_bytes(), before)
                    serialized = json.dumps(receipt)
                    for forbidden in (PRIVATE_MARKER, str(root), media.name, "filename", "tags"):
                        self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
