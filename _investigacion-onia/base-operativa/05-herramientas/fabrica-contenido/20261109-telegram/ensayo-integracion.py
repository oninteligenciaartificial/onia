#!/usr/bin/env python3
"""Verifica la entrega previa y conecta el recibo seco con trabajo.py aislado."""
import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
PRIOR = HERE.parent / "20261108"
TASK_ID = "ficcion-fabrica-001"
EVIDENCE = "04-operacion-agentes/evidencias/ficcion-fabrica-001/"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", required=True, type=Path)
    args = parser.parse_args()
    root = args.salida.resolve()
    if not root.is_relative_to(HERE / "evidencia") or root == HERE / "evidencia" or root.exists():
        parser.error("Elegir carpeta NUEVA bajo evidencia/ de esta entrega")
    root.mkdir(parents=True)
    trabajo = load("trabajo_integracion", BASE / "05-herramientas/scripts/trabajo.py")
    prior = load("ensayo_previo", PRIOR / "ensayo.py")
    prior_root = PRIOR / "ensayos/ejecucion-02"
    prior_task = trabajo.read_task(prior_root, TASK_ID)
    trabajo.verify(prior_root, prior_task)
    prior_report = json.loads((prior_root / "resultado.json").read_text())
    assert prior_report["resultado"] == "OK" and len(prior_report["checks"]) == 6
    assert prior_report["fixture_sha256"] == hashlib.sha256((PRIOR / "fixture.json").read_bytes()).hexdigest()
    assert prior_report["trabajo_py_sha256"] == hashlib.sha256(prior.SOURCE.read_bytes()).hexdigest()
    fixture = json.loads((HERE / "fixture.json").read_text())
    assert all(prior.sha(script) == fixture["snapshot"]["reviews"][name]["guion_sha256"]
               for name, script in fixture["snapshot"]["scripts"].items())
    before_prior = trabajo.task_path(prior_root, TASK_ID).read_bytes()
    output = subprocess.run(["node", str(HERE / "pruebas.cjs")], check=True, capture_output=True, text=True)
    tests = json.loads(output.stdout)
    (root / "adaptador-resultados.json").write_bytes(prior.encoded(tests))
    receipt = tests["receipt"]
    # El ID técnico lleva namespace. trabajo.py admite como máximo 64 caracteres.
    assert re.fullmatch(r"telegram-[a-f0-9]{64}", receipt["decision_id"])
    decision_id = receipt["decision_id"].removeprefix("telegram-")
    checks = [{"caso": "ensayo_20261108_verificado", "resultado": "6 controles previos e integridad vigentes"}]

    def preserve_lock(path, *unused, **kwargs):
        if path.parent != root / "operacion/bloqueos" or path.suffix != ".lock":
            raise RuntimeError("Borrado inesperado rechazado")
        archive = root / "locks-conservados"
        archive.mkdir(exist_ok=True)
        path.rename(archive / (str(len(list(archive.iterdir())) + 1) + ".json"))

    def reject(label, operation):
        path = trabajo.task_path(root, TASK_ID)
        before = path.read_bytes()
        try:
            operation()
        except ValueError:
            assert path.read_bytes() == before
            checks.append({"caso": label, "resultado": "rechazado_sin_mutacion"})
        else:
            raise AssertionError(label)

    with ExitStack() as stack:
        stack.enter_context(patch.object(Path, "unlink", preserve_lock))
        stack.enter_context(patch("socket.socket", side_effect=RuntimeError("Red prohibida")))
        trabajo.create(root, TASK_ID, "FICTICIO. Adaptador seco sobre contrato 20261108",
                       "Decisión sintética", shared=True)
        source = root / EVIDENCE / "decision-seca.json"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(prior.encoded(receipt))
        row = trabajo.update(root, TASK_ID, "en_curso", "Snapshot sintético", "Sin efectos", "Adaptar decisión",
                             [EVIDENCE + "decision-seca.json"], revision=1)
        assert row["revision"] == fixture["snapshot"]["task"]["revision"] == receipt["revision_esperada"]
        row = trabajo.decide(root, TASK_ID, receipt["revision_esperada"], decision_id,
                             "SIMULADO " + receipt["veredicto"], EVIDENCE + "decision-seca.json", receipt["autor"])
        assert row["revision"] == 3 and len(row["decisiones"]) == 1 and row["aceptacion"] is None
        checks.append({"caso": "recibo_a_trabajo_decide", "resultado": "una decisión sintética; revisión 2 a 3"})
        reject("CAS_revision_vieja", lambda: trabajo.decide(root, TASK_ID, 2, "otro-id", "SIMULADO",
                                                           EVIDENCE + "decision-seca.json", receipt["autor"]))
        reject("duplicado_id_harness", lambda: trabajo.decide(root, TASK_ID, 3, decision_id, "SIMULADO",
                                                              EVIDENCE + "decision-seca.json", receipt["autor"]))
        # Reconciliar tras reinicio sin otro almacén canónico ni segunda escritura.
        reread = trabajo.read_task(root, TASK_ID)
        saved = next(item for item in reread["decisiones"] if item["id"] == decision_id)
        saved_receipt = json.loads((root / saved["fuente"]["archivo"]).read_text())
        assert saved_receipt == receipt
        checks.append({"caso": "conciliacion_tras_reinicio", "resultado": "recibo recuperado de decisiones[].fuente"})
        trabajo.verify(root, reread)
    assert trabajo.task_path(prior_root, TASK_ID).read_bytes() == before_prior
    report = {"resultado": "OK", "simulacion": True, "casos_adaptador": tests["casos"], "checks_harness": checks,
              "fuentes": {"ensayo_20261108": hashlib.sha256((PRIOR / "ensayo.py").read_bytes()).hexdigest(),
                          "fixture_20261108": prior_report["fixture_sha256"],
                          "trabajo_py": prior_report["trabajo_py_sha256"],
                          "adaptador": hashlib.sha256((HERE / "adaptador.cjs").read_bytes()).hexdigest(),
                          "workflow": hashlib.sha256((HERE / "workflow-n8n.json").read_bytes()).hexdigest()},
              "registro_aislado": trabajo.task_path(root, TASK_ID).relative_to(root).as_posix(),
              "aceptacion": None, "anterior_sin_cambios": True,
              "limites": ["sin escritura en registro canónico", "sin decisión humana real",
                          "sin concurrencia distribuida", "locks archivados como en ensayo previo"]}
    (root / "resultado.json").write_bytes(prior.encoded(report))
    print(json.dumps({"resultado": "OK", "casos_adaptador": tests["casos"], "checks_harness": len(checks)}))


if __name__ == "__main__":
    main()
