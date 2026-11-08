from pathlib import Path
import sys,json
import supervise
O=Path(__file__).resolve().parent;python=O.parent/'panns-setup-v3/venv/bin/python'
assert python.is_file() and (O/'infer.py').is_file()
name,case=sys.argv[1:];receipt=O/(case+'-receipt.json');assert not receipt.exists()
r=supervise.run(name,[str(python),'-B',str(O/'infer.py'),case],120,120)
print(json.dumps(r,indent=2))
