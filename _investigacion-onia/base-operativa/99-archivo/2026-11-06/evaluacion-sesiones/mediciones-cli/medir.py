"""Mide bytes reales de CLI en fixtures; no evalúa conducta, tokens ni compacción."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parents[4]
REPO = BASE.parents[1]
BASELINE = "99da0bff96f289dc01fc10a20f745dc146f77427"
sys.path.insert(0, str(BASE / "scripts"))
import trabajo


def capture(script, fixture, args):
    return subprocess.check_output([sys.executable, "-B", str(script), "--base", str(fixture), *args])


def measure(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {"baseline": BASELINE, "runtime_sha256": {}, "mediciones": [],
              "tokens": None, "contexto_total_del_modelo": None,
              "limite": "Bytes/caracteres de archivos y salidas CLI; no tokens, conducta LLM, ahorro facturado ni compacción.",
              "informacion_necesaria": "Objetivo, restricciones/briefing y próximo paso idénticos en todos los tamaños; sólo se agregan snapshots operativos redundantes."}
    for name in ("trabajo.py", "harness.py"):
        report["runtime_sha256"][name] = trabajo.digest((BASE / "scripts" / name).read_bytes())
    with tempfile.TemporaryDirectory(prefix="onia-medicion-") as temporary:
        owned = Path(temporary).resolve()
        old = owned / "baseline"
        old.mkdir()
        for name in ("trabajo.py", "harness.py"):
            data = subprocess.check_output(["git", "show", BASELINE + ":_investigacion-onia/base-operativa/scripts/" + name], cwd=REPO)
            (old / name).write_bytes(data)
        for revisions in (1, 6, 60):
            fixture = owned / ("fixture-" + str(revisions))
            fixture.mkdir()
            briefing = ("# Encargo sintético\nObjetivo: resumir datos suministrados.\n"
                        "Restricciones: no red, no datos externos, conservar entradas, no autoaceptarse.\n"
                        "Decisión vigente de esta medición: sólo filas activas.\n"
                        "Siguiente paso: calcular y verificar antes de entregar para revisión.\n")
            trabajo.create(fixture, "medicion", "Resumir datos suministrados", "Calcular y verificar", briefing=briefing)
            for revision in range(1, revisions):
                trabajo.update(fixture, "medicion", "preparado", "", "", "Calcular y verificar", [], revision=revision)
            canonical = trabajo.task_path(fixture, "medicion")
            before = canonical.read_bytes()
            samples = {
                "anterior": capture(old / "harness.py", fixture, ["retomar", "medicion"]),
                "breve": capture(BASE / "scripts/harness.py", fixture, ["retomar", "medicion"]),
                "completa": capture(BASE / "scripts/harness.py", fixture, ["retomar", "medicion", "--completo"]),
                "consulta_revision_1": capture(BASE / "scripts/harness.py", fixture, ["historial", "medicion", "--revision", "1"])}
            brief = json.loads(samples["breve"])
            full = json.loads(samples["completa"])
            assert full["tarea"] == json.loads(before)
            for key in ("id", "revision", "estado", "objetivo", "proximo_paso", "resultado", "comprobacion", "verificacion", "evidencias", "aceptacion", "briefing"):
                assert brief["tarea"][key] == full["tarea"][key], key
            assert "historial" not in brief["tarea"] and "briefing" not in brief
            assert canonical.read_bytes() == before
            row = {"revisiones": revisions, "archivo_canonico_bytes": len(before),
                   "archivo_canonico_caracteres": len(before.decode("utf-8")), "campos_criticos_iguales": True,
                   "lecturas_sin_mutacion": True, "salidas": {}}
            directory = output / ("revision-" + str(revisions))
            directory.mkdir()
            for label, content in samples.items():
                path = directory / (label + ".json")
                path.write_bytes(content)
                row["salidas"][label] = {"archivo": path.relative_to(output).as_posix(), "bytes": len(content),
                    "caracteres": len(content.decode("utf-8")), "sha256": hashlib.sha256(content).hexdigest()}
            row["reduccion_inicial_bytes"] = len(samples["anterior"]) - len(samples["breve"])
            row["total_breve_mas_consulta_bytes"] = len(samples["breve"]) + len(samples["consulta_revision_1"])
            report["mediciones"].append(row)
    (output / "resultados.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("salida", type=Path, help="Directorio NUEVO para evidencia; no se sobreescribe.")
    report = measure(parser.parse_args().salida)
    print(json.dumps({"mediciones": report["mediciones"], "limite": report["limite"]}, ensure_ascii=False, indent=2))
