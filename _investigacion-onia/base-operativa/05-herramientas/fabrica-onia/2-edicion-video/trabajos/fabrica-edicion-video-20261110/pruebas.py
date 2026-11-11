#!/usr/bin/env python3
"""Pruebas sintéticas cortas del CLI. Sólo stdlib y FFmpeg presentes."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import lote

sys.dont_write_bytecode = True
import procesar as editor

BASE = Path(__file__).resolve().parent
EVIDENCE = {}


class EditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix="onia-edicion-fixture-"))
        # Tres segundos con cortes visual y sonoro conocidos.
        editor.run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-filter_complex_threads", "1",
                    "-f", "lavfi", "-i", "color=red:s=320x180:r=30:d=1",
                    "-f", "lavfi", "-i", "color=green:s=320x180:r=30:d=1",
                    "-f", "lavfi", "-i", "color=blue:s=320x180:r=30:d=1",
                    "-f", "lavfi", "-i", "aevalsrc=0.1*sin(2*PI*(440+220*floor(t))*t):s=48000:d=3",
                    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]",
                    "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-threads", "1",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", str(cls.root / "fuente.mp4")])
        editor.run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-f", "lavfi", "-i",
                    "color=yellow:s=180x320:r=30:d=1", "-c:v", "libx264", "-threads", "1",
                    "-pix_fmt", "yuv420p", str(cls.root / "apoyo.mp4")])
        cls.original_hash = editor.digest(cls.root / "fuente.mp4")
        cls.transcript = {"segments": [
            {"start": 0, "end": 1, "text": "Rojo"},
            {"start": 1, "end": 2, "text": "Verde"},
            {"start": 2, "end": 3, "text": "Azul"}]}
        (cls.root / "texto.json").write_text(json.dumps(cls.transcript))
        cls.plan = {"version": 1, "tipo": "reel", "entrada": "fuente.mp4",
                    "transcripcion": "texto.json",
                    "intervalos": [{"start": 0, "end": 1}, {"start": 2, "end": 3}],
                    "broll": [{"archivo": "apoyo.mp4", "start": 0.5, "end": 1,
                               "source_start": 0}]}

    @classmethod
    def tearDownClass(cls):
        # Conservar fixtures de esta comprobación; no borrar evidencia.
        pass

    def cli(self, plan, label, expected=0, extra=(), width=360):
        path = self.root / (label + ".json")
        path.write_text(json.dumps(plan, allow_nan=True), encoding="utf-8")
        output = self.root / label
        size = [] if width is None else ["--ancho", str(width)]
        result = subprocess.run([sys.executable, str(BASE / "procesar.py"), "--plan", str(path),
                                 "--salida", str(output), *size, *extra],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, expected, result.stderr)
        report = json.loads((output / "reporte.json").read_text())
        EVIDENCE[label] = {"rc": result.returncode, "resultado": report["resultado"],
                           "error": report.get("error")}
        return output, report

    def pixel(self, path, second, x=180, y=320):
        data = editor.run(["ffmpeg", "-v", "error", "-nostdin", "-ss", str(second),
                           "-i", str(path), "-frames:v", "1", "-vf", f"crop=2:2:{x}:{y}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-threads", "1", "pipe:1"])
        self.assertEqual(len(data), 12)
        return list(data[:3])

    def test_render_reproducible_cuts_broll_audio(self):
        first, report = self.cli(self.plan, "render-a")
        second, again = self.cli(self.plan, "render-b")
        self.assertEqual(report["sha256_salida"], again["sha256_salida"])
        self.assertEqual(editor.digest(first / "pieza.mp4"), editor.digest(second / "pieza.mp4"))
        self.assertEqual((report["salida"]["width"], report["salida"]["height"]), (360, 640))
        self.assertAlmostEqual(report["salida"]["duration"], 2, delta=0.034)
        self.assertEqual([c["output_start"] for c in report["intervalos"]], [0, 1])
        self.assertEqual(editor.digest(self.root / "fuente.mp4"), self.original_hash)
        pixels = [self.pixel(first / "pieza.mp4", t) for t in (0.2, 0.7, 1.1)]
        self.assertTrue(pixels[0][0] > 220 and pixels[0][1] < 25, pixels)
        self.assertTrue(pixels[1][0] > 220 and pixels[1][1] > 220, pixels)
        self.assertTrue(pixels[2][2] > 220 and pixels[2][0] < 25, pixels)
        probe = json.loads(editor.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                       "-count_frames", "-show_entries", "stream=nb_read_frames",
                                       "-of", "json", str(first / "pieza.mp4")]))
        self.assertEqual(int(probe["streams"][0]["nb_read_frames"]), 60)
        audio = editor.run(["ffmpeg", "-v", "error", "-i", str(first / "pieza.mp4"),
                            "-map", "0:a", "-t", "2", "-f", "s16le", "-ac", "1",
                            "-ar", "48000", "pipe:1"])
        import array
        samples = array.array("h", audio)
        self.assertAlmostEqual(len(samples) / 48000, 2, delta=0.03)
        self.assertGreater(max(samples), 500)
        frequencies = []
        for second, expected in ((0.2, 440), (0.7, 440), (1.2, 880)):
            section = samples[round(second * 48000):round((second + 0.2) * 48000)]
            crossings = sum(first <= 0 < last for first, last in zip(section, section[1:]))
            frequency = crossings / 0.2
            self.assertAlmostEqual(frequency, expected, delta=10)
            frequencies.append(frequency)
        EVIDENCE["render-a"].update(sha256=report["sha256_salida"], frames=60,
                                   duration=report["salida"]["duration"], center_pixels=pixels,
                                   audio_frequencies_hz=frequencies,
                                   original_preserved=True, identical_second_render=True)

    def test_default_resolution(self):
        plan = {**self.plan, "intervalos": [{"start": 0, "end": 1}], "broll": []}
        _, report = self.cli(plan, "default-resolution", width=None)
        self.assertEqual((report["salida"]["width"], report["salida"]["height"]), (720, 1280))

    def test_horizontal_and_batch_share_transcript_and_preserve_source(self):
        output, report = self.cli(self.plan, "horizontal", width=640, extra=("--formato", "horizontal"))
        self.assertEqual((report["salida"]["width"], report["salida"]["height"]), (640, 360))
        self.assertEqual(report["formato"], "horizontal")
        self.assertIn("PlayResX: 1280", (output/"subtitulos.ass").read_text())
        manifest = self.root/"lote.json"
        manifest.write_text(json.dumps({"version": 1, "entrada": str(self.root/"fuente.mp4"),
            "transcripcion": str(self.root/"texto.json"), "piezas": [
                {"id": "T01", "tipo": "reel", "intervalos": [{"start": 0, "end": 1}]}]}))
        dest = self.root/"lote"
        command = [sys.executable, str(BASE/"lote.py"), "--plan", str(manifest),
                   "--salida", str(dest), "--preview"]
        run = subprocess.run(command, capture_output=True, timeout=45)
        self.assertEqual(run.returncode, 0, run.stderr)
        receipt = json.loads((dest/"lote-reporte.json").read_text())
        self.assertEqual(receipt["asr_ejecuciones"], 0)
        self.assertEqual(len(receipt["piezas"]), 2)
        self.assertEqual(receipt["resultado"], "renderizado_pendiente_revision")
        self.assertEqual(receipt["sha256_entrada"], self.original_hash)
        for shape, dims in (("vertical", (360, 640)), ("horizontal", (640, 360))):
            info = editor.probe(dest/("T01-"+shape)/"pieza.mp4")
            self.assertEqual((info["width"], info["height"]), dims)
        retry = subprocess.run(command, capture_output=True, timeout=10)
        self.assertEqual(retry.returncode, 2)
        self.assertEqual(receipt, json.loads((dest/"lote-reporte.json").read_text()))
        EVIDENCE["lote-dos-formatos"] = {"salidas": 2, "asr_ejecuciones": 0,
            "entrada_preservada": True, "reintento_sin_sobrescritura": True}

    def test_batch_transcribes_once_for_multiple_pieces(self):
        manifest = self.root/"lote-asr.json"
        manifest.write_text(json.dumps({"version": 1, "entrada": str(self.root/"fuente.mp4"),
            "piezas": [{"id": ident, "tipo": "reel", "intervalos": [{"start": 0, "end": 1}]} for ident in ("T01", "T02")]}))
        dest = self.root/"lote-asr"
        calls = []
        original = editor.run
        def run(command, *args, **kwargs):
            if "--modelos" in command:
                calls.append(command)
                Path(command[command.index("--salida")+1]).write_text(json.dumps(self.transcript))
                return b''
            return original(command, *args, **kwargs)
        with patch.object(editor, 'run', side_effect=run):
            report = lote.process(SimpleNamespace(plan=manifest, salida=dest, preview=True,
                    timeout=60, asr_python=Path('/fixture/python'), modelos=Path('/fixture/model')))
        self.assertEqual(len(calls), 1)
        self.assertEqual(report['asr_ejecuciones'], 1)
        self.assertEqual(len(report['piezas']), 4)
        self.assertEqual(editor.digest(self.root/'fuente.mp4'), self.original_hash)
        EVIDENCE['lote-asr-unico'] = {'asr_simulado': True, 'render_real': True,
                                    'invocaciones_asr': 1, 'piezas': 2, 'salidas': 4}

    def test_bad_plan_inputs(self):
        variants = [
            ("vlog", {"tipo": "vlog"}),
            ("missing-source", {"entrada": "ausente.mp4"}),
            ("missing-transcript", {"transcripcion": "ausente.json"}),
            ("outside", {"intervalos": [{"start": 0, "end": 4}]}),
            ("overlap", {"intervalos": [{"start": 0, "end": 2}, {"start": 1, "end": 3}]}),
            ("nan", {"intervalos": [{"start": 0, "end": float("nan")}]}),
            ("boolean", {"intervalos": [{"start": False, "end": 1}]}),
            ("tiny", {"intervalos": [{"start": 0, "end": 0.001}]}),
            ("unknown", {"musica": "inventada"}),
            ("missing-broll", {"broll": [{"archivo": "ausente.mp4", "start": 0, "end": 1,
                                          "source_start": 0}]}),
            ("short-broll", {"broll": [{"archivo": "apoyo.mp4", "start": 0, "end": 2,
                                        "source_start": 0}]}),
            ("outside-broll", {"broll": [{"archivo": "apoyo.mp4", "start": 1.5, "end": 2.5,
                                          "source_start": 0}]})]
        for label, changes in variants:
            with self.subTest(label=label):
                plan = {**self.plan, **changes}
                output, report = self.cli(plan, label, expected=2)
                self.assertEqual(report["resultado"], "fallida")
                self.assertFalse((output / "pieza.mp4").exists())

    def test_invalid_json_and_missing_plan(self):
        invalid = self.root / "invalid.json"
        invalid.write_text("{")
        for index, path in enumerate((invalid, self.root / "missing-plan.json")):
            output = self.root / f"invalid-out-{index}"
            result = subprocess.run([sys.executable, str(BASE / "procesar.py"), "--plan", str(path),
                                     "--salida", str(output)], capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads((output / "reporte.json").read_text())["resultado"], "fallida")

    def test_existing_output_is_preserved(self):
        path = self.root / "occupied-plan.json"
        path.write_text(json.dumps(self.plan))
        output = self.root / "occupied"
        output.mkdir()
        original = output / "original.txt"
        original.write_text("preservar")
        result = subprocess.run([sys.executable, str(BASE / "procesar.py"), "--plan", str(path),
                                 "--salida", str(output)], capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(original.read_text(), "preservar")
        self.assertEqual(list(output.iterdir()), [original])

    def test_cut_through_sentence_rejected(self):
        plan = {**self.plan, "intervalos": [{"start": 0.5, "end": 1}], "broll": []}
        _, report = self.cli(plan, "partial-sentence", expected=2)
        self.assertIn("atraviesa", report["error"])

    def test_transcript_validation(self):
        for data in ({"segments": []}, {"segments": [{"start": 0, "end": 4, "text": "hola"}]},
                     {"segments": [{"start": 0, "end": 1, "text": "{\\pos(0,0)}"}]}):
            with self.assertRaises(ValueError):
                editor.segments(data, 3)

    def test_silent_source_explicit_transcript(self):
        plan = {"version": 1, "tipo": "reel", "entrada": "apoyo.mp4",
                "transcripcion": "texto.json", "intervalos": [{"start": 0, "end": 1}]}
        transcript = self.root / "silent-text.json"
        transcript.write_text(json.dumps({"segments": self.transcript["segments"][:1]}))
        plan["transcripcion"] = transcript.name
        _, report = self.cli(plan, "silent-source")
        self.assertTrue(any("sin audio" in str(x) for x in report["dudas"]))
        del plan["transcripcion"]
        _, report = self.cli(plan, "silent-needs-asr", expected=2)
        self.assertIn("requiere audio", report["error"])

    def test_missing_asr_python_and_model(self):
        plan = copy.deepcopy(self.plan)
        del plan["transcripcion"]
        self.cli(plan, "asr-python-absent", expected=2, extra=("--asr-python", "/missing/python"))
        self.cli(plan, "asr-model-absent", expected=2,
                 extra=("--modelos", str(self.root / "no-model")))

    def test_asr_offline_synthetic_voice(self):
        # Voz sintetizada por libflite ya presente. Sólo prueba de ejecución.
        # No se atribuye exactitud del español ni validación de una grabación real.
        source = self.root / "voz-sintetica.mp4"
        editor.run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-f", "lavfi", "-i",
                    "color=black:s=180x320:r=30:d=6", "-f", "lavfi", "-i",
                    "flite=text='Esta es una prueba de audio para el editor':voice=slt",
                    "-af", "apad", "-t", "6", "-c:v", "libx264", "-threads", "1",
                    "-c:a", "aac", "-pix_fmt", "yuv420p", str(source)])
        plan = {"version": 1, "tipo": "talking_head", "entrada": source.name,
                "intervalos": [{"start": 0, "end": 6}]}
        output, report = self.cli(plan, "asr-synthetic")
        transcript = json.loads((output / "transcripcion.json").read_text())
        self.assertTrue(transcript["segments"])
        self.assertEqual(report["asr"], "small_cpu_int8_offline")
        self.assertEqual(report["revision_humana"], "pendiente")
        EVIDENCE["asr-synthetic"].update(segments=len(transcript["segments"]),
                                          duration=report["salida"]["duration"],
                                          engine=transcript["motor"], real_media=False)

    def test_latin_subtitles_safe_bounds(self):
        text = "WWWWWWWWWWWWWW ÁÉÍÓÚ Ññ ¿Preguntas? UnaPalabraExtraordinariamenteLarga"
        rows = editor.segments({"segments": [{"start": 0, "end": 3, "text": text}]}, 3)
        cuts = editor.intervals([{"start": 0, "end": 3}], 3)
        cues, doubts = editor.subtitle_cues(rows, cuts)
        self.assertTrue(any(x["tipo"] == "tiempo_interno_estimado" for x in doubts))
        self.assertTrue(all(len(c["lines"]) <= 2 and all(len(s) <= 14 for s in c["lines"]) for c in cues))
        directory = self.root / "subtitle-bounds"
        directory.mkdir()
        editor.write_ass(directory / "subtitulos.ass", cues)
        mask = editor.run(["ffmpeg", "-v", "error", "-nostdin", "-f", "lavfi", "-i",
                           "color=black:s=360x640:r=10:d=3", "-vf", "ass=subtitulos.ass",
                           "-pix_fmt", "gray", "-f", "rawvideo", "-threads", "1", "pipe:1"], cwd=directory)
        coordinates = []
        frame_size = 360 * 640
        for offset in range(0, len(mask), frame_size):
            frame = mask[offset:offset + frame_size]
            white = [i for i, value in enumerate(frame) if value > 160]
            if white:
                coordinates += [(i % 360, i // 360) for i in white]
        self.assertTrue(coordinates)
        bounds = [min(x for x, y in coordinates), min(y for x, y in coordinates),
                  max(x for x, y in coordinates), max(y for x, y in coordinates)]
        self.assertGreaterEqual(bounds[0], 36)
        self.assertLess(bounds[2], 324)
        self.assertGreaterEqual(bounds[1], 490)
        self.assertLess(bounds[3], 570)
        EVIDENCE["subtitle-bounds"] = {"white_pixel_bbox_360x640": bounds,
                                      "frames_checked": len(mask) // frame_size}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidencia", type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EditorTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.evidencia:
        editor.write_json(args.evidencia, {"tests": result.testsRun,
                                          "failures": len(result.failures),
                                          "errors": len(result.errors), "casos": EVIDENCE})
    raise SystemExit(0 if result.wasSuccessful() else 1)
