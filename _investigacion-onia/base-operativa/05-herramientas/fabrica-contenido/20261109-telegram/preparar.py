#!/usr/bin/env python3
"""Genera fixture y workflow desde el ensayo conservado y el adaptador único."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "20261108"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def build():
    fixture = json.loads((PRIOR / "fixture.json").read_text())
    scripts = {row["id"]: row for row in fixture["guiones"]}
    reviews = {}
    for review in fixture["revisiones"]:
        script_id = review["guion_id"]
        reviews[script_id] = dict(review, guion_sha256=hashlib.sha256(encoded(scripts[script_id])).hexdigest())
    snapshot = {"verified": True, "task": {"id": "ficcion-fabrica-001", "revision": 2, "estado": "en_curso"},
                "scripts": scripts, "reviews": reviews}
    policy = {"mode": "fixture", "transportVerified": True, "botAlias": "bot-sintetico",
              "userId": 900001, "chatId": 900002, "taskIds": [snapshot["task"]["id"]]}
    script_id = "guion-a-v1"
    command = "/elegir ficcion-fabrica-001 guion-a-v1 2 " + reviews[script_id]["guion_sha256"]
    event = {"synthetic": True, "update_id": 1,
             "message": {"from": {"id": 900001, "is_bot": False},
                         "chat": {"id": 900002, "type": "private"}, "text": command}}
    data = {"aviso": "FICTICIO. Identidades, transporte y decisión simulados. Sin conexión a panel o Telegram.",
            "policy": policy, "snapshot": snapshot, "events": [event, event]}
    source = (HERE / "adaptador.cjs").read_text()
    # Sólo el núcleo común entra en Code. CLI y sus accesos fs quedan fuera.
    core = source.split("module.exports =")[0]
    code = (core + "\nconst receipts = { transport: {}, business: {} };\n"
            "const input = $input.first().json;\n"
            "return input.events.map(event => ({ json: adapt(event, input.policy, () => input.snapshot, receipts) }));\n")
    workflow = {
        "name": "ONIA · PILOTO NOCTURNO 20261109 · SIN ENVIOS", "active": False,
        "nodes": [
            {"id": "manual", "name": "Manual", "type": "n8n-nodes-base.manualTrigger",
             "typeVersion": 1, "position": [0, 0], "parameters": {}},
            {"id": "fixture", "name": "Fixture FICTICIO", "type": "n8n-nodes-base.code",
             "typeVersion": 2, "position": [240, 0], "parameters": {
                 "mode": "runOnceForAllItems", "language": "javaScript",
                 "jsCode": "return [{ json: " + json.dumps(data, ensure_ascii=False) + " }];"}},
            {"id": "adapter", "name": "Adaptador SECO", "type": "n8n-nodes-base.code",
             "typeVersion": 2, "position": [500, 0], "parameters": {
                 "mode": "runOnceForAllItems", "language": "javaScript", "jsCode": code}},
        ],
        "connections": {"Manual": {"main": [[{"node": "Fixture FICTICIO", "type": "main", "index": 0}]]},
                        "Fixture FICTICIO": {"main": [[{"node": "Adaptador SECO", "type": "main", "index": 0}]]}},
        "settings": {"executionOrder": "v1", "saveDataErrorExecution": "none",
                     "saveDataSuccessExecution": "none", "saveManualExecutions": False},
    }
    return data, workflow


if __name__ == "__main__":
    data, workflow = build()
    for name, value in (("fixture.json", data), ("workflow-n8n.json", workflow)):
        with (HERE / name).open("x") as stream:
            stream.write(encoded(value).decode())
    print("Fixture y workflow preparados")
