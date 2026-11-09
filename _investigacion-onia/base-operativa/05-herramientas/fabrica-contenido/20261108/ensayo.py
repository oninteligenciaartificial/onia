#!/usr/bin/env python3
"""Ensayo descartable, sin red ni LLM; reutiliza trabajo.py, no es un servicio."""
import argparse
from contextlib import ExitStack
from datetime import datetime
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
SOURCE = BASE / "05-herramientas/scripts/trabajo.py"
ID = "ficcion-fabrica-001"
EVIDENCE = "04-operacion-agentes/evidencias/ficcion-fabrica-001/"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def sha(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", required=True, type=Path,
                        help="Carpeta NUEVA dentro de ensayos/; se conserva completa.")
    args = parser.parse_args()
    root = args.salida.resolve()
    if not root.is_relative_to(HERE / "ensayos") or root == HERE / "ensayos":
        parser.error("La salida debe estar dentro de la carpeta asignada, bajo ensayos/.")
    if root.exists():
        parser.error("La salida ya existe: elegir otro nombre; no se borra ni sobrescribe.")
    root.mkdir(parents=True)
    fixture = json.loads((HERE / "fixture.json").read_text())
    assert fixture["simulacion"] is True
    spec = importlib.util.spec_from_file_location("trabajo_fabrica_ensayo", SOURCE)
    trabajo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(trabajo)
    checks = []

    # El API conserva O_EXCL y la comprobación de revisión originales. Su unlink
    # final del lock se convierte en rename para respetar NO BORRAR, aun temporales.
    # No se altera el código del harness. Estos locks archivados no están activos.
    def preserve_lock(path, *unused, **kwargs):
        if path.parent != root / "operacion/bloqueos" or path.suffix != ".lock":
            raise RuntimeError("Borrado inesperado rechazado: " + str(path))
        archive = root / "locks-conservados"
        archive.mkdir(exist_ok=True)
        path.rename(archive / (str(len(list(archive.iterdir())) + 1) + ".json"))

    def current():
        return trabajo.read_task(root, ID)

    def update(state, result, check, following, names=(), verification="pendiente"):
        return trabajo.update(root, ID, state, result, check, following,
                              [EVIDENCE + n for n in names], revision=current()["revision"],
                              verification=verification)

    def rejected(label, operation):
        before = trabajo.task_path(root, ID).read_bytes()
        try:
            operation()
        except ValueError as exc:
            assert trabajo.task_path(root, ID).read_bytes() == before
            checks.append({"caso": label, "resultado": "rechazado_sin_mutacion", "detalle": str(exc)})
        else:
            raise AssertionError("No se rechazó: " + label)

    with ExitStack() as stack:
        stack.enter_context(patch.object(Path, "unlink", preserve_lock))
        stack.enter_context(patch("socket.socket", side_effect=RuntimeError("Red prohibida en ensayo")))
        trabajo.create(root, ID, "FICTICIO: dos ideas y guiones con revisión y decisión simuladas",
                       "Clasificar fuentes ficticias", shared=True)
        update("en_curso", "Comienza ensayo sin sesiones ni servicios", "Fixture declarada ficticia", "Ingestión")
        usable, duplicates, pending, failed, seen = [], [], [], [], {}
        for source in fixture["fuentes"]:
            assert source["ficticia"] and urlsplit(source["url"]).hostname.endswith(".invalid")
            if source.get("error_simulado"):
                failed.append(source["id"])
            elif not all(source.get(k) for k in ("autor", "fecha_hecho", "fecha_publicacion", "fecha_consulta", "hecho")):
                pending.append(source["id"])
            else:
                happened = datetime.fromisoformat(source["fecha_hecho"])
                published = datetime.fromisoformat(source["fecha_publicacion"])
                consulted = datetime.fromisoformat(source["fecha_consulta"].replace("Z", "+00:00"))
                assert happened.date() <= published.date() <= consulted.date()
                parsed = urlsplit(source["url"])
                key = (parsed.hostname.lower(), parsed.path.rstrip("/"))
                if key in seen:
                    duplicates.append({"id": source["id"], "duplicado_de": seen[key]})
                else:
                    seen[key] = source["id"]
                    usable.append(source["id"])
        assert usable == ["noticia-a", "noticia-b"]
        assert duplicates == [{"id": "noticia-a-repetida", "duplicado_de": "noticia-a"}]
        assert pending == ["noticia-pendiente"] and failed == ["noticia-fallo"]
        ingest = {"simulado": True, "fuentes": fixture["fuentes"], "utilizables": usable,
                  "duplicados": duplicates, "pendientes": pending, "fallos": failed}
        write(root / EVIDENCE / "ingesta.json", ingest)
        checks.append({"caso": "ingesta_y_duplicado", "resultado": "2 utilizables, 1 duplicado, 1 pendiente, 1 fallo"})
        update("en_espera", "Fuente sin fecha retenida", "No entra en ningún guion",
               "Coordinador: resolver fecha antes de usar esa fuente", ["ingesta.json"])
        update("en_curso", "Continuar con fuentes completas", "Pendiente conservado en evidencia", "Evaluar fallo")
        update("en_espera", "Fallo de fuente simulado", "Sin acceso real ni reintento de red",
               "Coordinador: recuperar fuente o descartarla; no rellenar su contenido")
        update("en_curso", "Continuar lote independiente", "Dos fuentes utilizables", "Preparar ideas")

        ideas = {i["id"]: i for i in fixture["ideas"]}
        scripts = {s["id"]: s for s in fixture["guiones"]}
        for idea in ideas.values():
            assert idea["ficticia"] and set(idea["fuentes"]) <= set(usable)
            assert idea["patron"] in fixture["patrones"] and idea["propuesta_onia"]
        for script in scripts.values():
            idea = ideas[script["idea_id"]]
            assert script["ficticio"] and script["fuentes"] == idea["fuentes"]
            assert script["patron"] == idea["patron"] and script["propuesta_onia"]
            assert all(b["respaldo"] in script["fuentes"] + ["propuesta_onia"] for b in script["bloques"])
        write(root / EVIDENCE / "ideas.json", {"simulado": True, "ideas": fixture["ideas"], "patrones": fixture["patrones"]})
        write(root / EVIDENCE / "guiones.json", {"simulado": True, "guiones": fixture["guiones"]})
        update("en_curso", "Dos ideas trazables convertidas en guiones", "Cada bloque distingue fuente y propuesta OnIA",
               "Revisión individual", ["ideas.json", "guiones.json"])
        reviews = {}
        for review in fixture["revisiones"]:
            assert review["simulada"] and review["guion_id"] in scripts
            review = dict(review, guion_sha256=sha(scripts[review["guion_id"]]))
            assert review["veredicto"] == ("bueno" if all(review["controles"].values()) else "cambios")
            reviews[review["guion_id"]] = review
        assert set(reviews) == set(scripts)
        write(root / EVIDENCE / "revisiones.json", {"simulado": True, "revisiones": list(reviews.values())})
        row = update("para_revision", "Lote editorial con revisiones simuladas", "A bueno; B cambios; no revisión independiente real",
                     "Decisión simulada por guion", ["revisiones.json"], "correcta")
        rejected("revision_obsoleta", lambda: trabajo.update(root, ID, "en_curso", "viejo", "", "conciliar", [], revision=row["revision"] - 1))
        rejected("decision_en_entrega_cerrada", lambda: trabajo.decide(root, ID, current()["revision"], "prematura", "no",
                  EVIDENCE + "guiones.json", "Sergio SIMULADO"))
        # Decisión editorial es distinta de aceptar el encargo del harness.
        update("en_curso", "Abrir fase de decisión editorial simulada", "Se conserva evidencia anterior", "Registrar decisiones")
        for decision in fixture["decisiones"]:
            target = decision["guion_id"]
            review = reviews[target]
            assert decision["simulada"] and decision["autor"] == "Sergio SIMULADO"
            assert review["guion_sha256"] == sha(scripts[target])
            if decision["veredicto"] == "elegir_para_preparar":
                assert review["veredicto"] == "bueno" and all(review["controles"].values())
            else:
                assert decision["veredicto"] == "pedir_cambios"
            receipt = dict(decision, guion_sha256=review["guion_sha256"], revision_sha256=sha(review))
            name = "decision-" + target + ".json"
            write(root / EVIDENCE / name, receipt)
            trabajo.decide(root, ID, current()["revision"], "decision-" + target,
                           "SIMULADO: " + decision["veredicto"], EVIDENCE + name, decision["autor"])
        rejected("decision_duplicada", lambda: trabajo.decide(root, ID, current()["revision"], "decision-guion-a-v1",
                  "SIMULADO: repetida", EVIDENCE + "decision-guion-a-v1.json", "Sergio SIMULADO"))
        assert reviews["guion-b-v1"]["veredicto"] == "cambios"
        checks.append({"caso": "revision_por_guion_y_decisiones", "resultado": "A elegido para preparar; B requiere cambios; cero aceptaciones de harness"})
        tampered = json.loads(encoded(current()))
        tampered["evidencias"][0]["sha256"] = "0" * 64
        rejected("evidencia_alterada_en_memoria", lambda: trabajo.verify(root, tampered))
        update("para_revision", "Ensayo completo; A elegido, B con cambios (todo simulado)",
               "Trazabilidad, duplicado, pendiente, fallo y conflictos comprobados",
               "Revisión real del encargo por coordinador; Telegram/panel/scheduler siguen sin integración", verification="correcta")
        row = current()
        trabajo.verify(root, row)
        assert row["aceptacion"] is None and len(row["decisiones"]) == 2

    # Vista desechable derivada de la lectura canónica y sus fuentes de decisión.
    cards = []
    for decision in row["decisiones"]:
        receipt = json.loads((root / decision["fuente"]["archivo"]).read_text())
        cards.append("<li>" + html.escape(receipt["guion_id"] + ": " + receipt["veredicto"]) + "</li>")
    markup = ('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
              '<title>OnIA · Ensayo ficticio</title><style>body{font:18px system-ui;max-width:850px;margin:3rem auto;padding:1rem;'
              'background:#10222a;color:#e6f3f3}aside{padding:1rem;background:#57441d}li{margin:1rem 0}</style>'
              '<h1>OnIA · Ideas y guiones</h1><aside>FICTICIO · sin conexión · sin envíos · sin autenticación</aside>'
              '<p>Tarea ' + html.escape(row["id"]) + ' · revisión ' + str(row["revision"]) + ' · ' + row["estado"] + '</p><ul>'
              + ''.join(cards) + '</ul><p>2 fuentes utilizables · 1 duplicado · 1 pendiente · 1 fallo.</p>'
              '<p>Proyección estática del JSON aislado. Las decisiones son simuladas; no se ha aceptado el encargo real.</p>'
              '<p>Próximo paso: ' + html.escape(row["proximo_paso"]) + '</p></html>')
    with (root / "panel.html").open("x") as stream:
        stream.write(markup)
    report = {"simulacion": True, "resultado": "OK", "checks": checks,
              "fixture_sha256": hashlib.sha256((HERE / "fixture.json").read_bytes()).hexdigest(),
              "trabajo_py_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "tarea_aislada": str(trabajo.task_path(root, ID).relative_to(root)),
              "revision_final": row["revision"], "estado": row["estado"],
              "sin_aceptacion_real": row["aceptacion"] is None,
              "red": "socket bloqueado en el ensayo; sin clientes API ni subprocess",
              "limites": ["sin sesiones harness lanzadas", "sin Telegram ni autenticación", "sin scheduler", "revisiones y Sergio simulados"]}
    write(root / "resultado.json", report)
    print(json.dumps({"resultado": "OK", "casos": len(checks), "salida": str(root)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
