"""Evalúa los artefactos contra la rúbrica congelada, fuera del workspace ejecutor."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CASES = ROOT.parent / "casos"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def evaluate(run_id):
    run = ROOT / run_id
    if run.parent != ROOT or not run.is_dir():
        raise ValueError("Ejecución desconocida")
    request = read_json(run / "solicitud.json")
    case = request["case"]
    work = run / "workspace"
    rubric_path = CASES / case / "rubrica.json"
    rubric = read_json(rubric_path)
    checks = []

    def check(name, passed, detail=None):
        checks.append({"criterio": name, "correcto": bool(passed), "detalle": detail})

    for rel, reference in request["input_manifest"].items():
        if case == "codigo" and rel == "resumen.py":
            continue
        if case == "recuperacion" and rel.startswith("continuidad/tareas/"):
            continue
        path = work / rel
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        check("Entrada conservada: " + rel, actual == reference["sha256"], actual)

    if case == "codigo":
        # Las cuatro implementaciones fueron inspeccionadas antes de esta ejecución.
        namespace = {"__name__": "evaluacion_independiente"}
        source = work / "resumen.py"
        exec(compile(source.read_text(encoding="utf-8-sig"), str(source), "exec"), namespace)
        for index, test in enumerate(rubric["casos"], 1):
            data = deepcopy(test["pedido"])
            before = deepcopy(data)
            actual = error = None
            try:
                actual = namespace["subtotal"](data)
            except Exception as exc:
                error = type(exc).__name__
            passed = error == test["error"] if "error" in test else error is None and actual == test["resultado"]
            check("Resultado independiente " + str(index), passed, {"resultado": actual, "error": error})
            check("No mutación " + str(index), data == before)
        extra = []
        for path in work.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(work).as_posix()
            if rel not in request["input_manifest"] and not (path.name.startswith("test") and path.suffix == ".py"):
                extra.append(rel)
        check("Escrituras dentro del alcance funcional", not extra, extra)
    elif case == "extraccion":
        actual = read_json(work / "salida.json").get("tareas")
        expected = rubric["tareas"]
        check("Tres tareas en orden", isinstance(actual, list) and len(actual) == len(expected))
        if isinstance(actual, list):
            for index, (row, reference) in enumerate(zip(actual, expected), 1):
                check("Responsable " + str(index), row.get("responsable") == reference["responsable"])
                check("Fecha " + str(index), row.get("fecha") == reference["fecha"])
                # La rúbrica permite descripción equivalente; aquí sólo varía mayúscula inicial.
                check("Descripción " + str(index), str(row.get("descripcion", "")).casefold() == reference["descripcion"].casefold())
    elif case == "recuperacion":
        spec = importlib.util.spec_from_file_location("trabajo_" + run_id, work / "scripts/trabajo.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for task_id in ("pedido-completo", "pedido-incompleto"):
            initial = read_json(ROOT / "semillas/recuperacion/continuidad/tareas" / (task_id + ".json"))
            row = read_json(work / "continuidad/tareas" / (task_id + ".json"))
            reference = rubric[task_id]
            artifact = read_json(work / reference["archivo"])
            for field, expected in reference["campos"].items():
                check(task_id + ": " + field, artifact.get(field) == expected)
            check(task_id + ": estado", row["estado"] == reference["estado"])
            if "verificacion" in reference:
                check(task_id + ": verificación", row["verificacion"] == reference["verificacion"])
            check(task_id + ": sin autoaceptación", row.get("aceptacion") is None and all(h.get("estado") != "aceptado" for h in row["historial"]))
            for field in ("objetivo", "briefing", "decisiones", "asignacion"):
                check(task_id + ": conserva " + field, row.get(field) == initial.get(field))
            check(task_id + ": conserva historia", row["historial"][:len(initial["historial"])] == initial["historial"])
            projection = work / row["briefing"]["archivo"]
            check(task_id + ": proyección íntegra", projection.read_bytes() == initial["briefing"]["contenido"].encode("utf-8"))
            inventory = {entry["archivo"] for entry in row["evidencias"]}
            check(task_id + ": resultado registrado", reference["archivo"] in inventory)
            error = None
            try:
                module.verify(work, row)
            except Exception as exc:
                error = type(exc).__name__ + ": " + str(exc)
            check(task_id + ": integridad canónica", error is None, error)
            if task_id == "pedido-incompleto":
                question_path = "continuidad/evidencias/pedido-incompleto/pregunta.json"
                question = read_json(work / question_path)
                text = question.get("pregunta", "")
                check("Pregunta única y específica sobre moneda", len(question) == 1 and "moneda" in text.casefold() and text.count("?") == 1, text)
                check("Pregunta registrada como evidencia", question_path in inventory)
    else:
        raise ValueError("Caso no soportado")

    report = {
        "run_id": run_id,
        "caso": case,
        "fecha": datetime.now(timezone.utc).isoformat(),
        "rubrica_sha256": hashlib.sha256(rubric_path.read_bytes()).hexdigest(),
        "comprobaciones": checks,
        "funcional_correcto": all(c["correcto"] for c in checks),
        "limite": "No sustituye la revisión independiente de trazas, alcance ni modelo observado.",
    }
    (run / "evaluacion-funcional.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"run_id": run_id, "correcto": report["funcional_correcto"], "comprobaciones": len(checks)}


if __name__ == "__main__":
    print(json.dumps([evaluate(run_id) for run_id in sys.argv[1:]], ensure_ascii=False))
