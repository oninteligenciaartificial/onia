"""Check objetivo congelado: importar solution.py desde directorio de brazo indicado."""
import copy
import importlib.util
import json
import pathlib
import sys
spec = importlib.util.spec_from_file_location("candidate_solution", pathlib.Path(sys.argv[1]) / "solution.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
scenarios = [([], None), ([{"id":"nine","seq":9},{"id":"ten","seq":10}], "ten"), ([{"id":"a","seq":12},{"id":"b","seq":12},{"id":"c","seq":2}], "b"), ([{"id":"zero","seq":0}], "zero"), ([{"id":"large","seq":100},{"id":"small","seq":11}], "large")]
results=[]
for events, expected in scenarios:
    original=copy.deepcopy(events)
    answer=m.select_latest(events)
    actual=answer["id"] if answer is not None else None
    results.append({"expected":expected,"actual":actual,"correct":actual==expected,"input_unchanged":events==original})
print(json.dumps({"checks":results,"passed":all(r["correct"] and r["input_unchanged"] for r in results)}))

