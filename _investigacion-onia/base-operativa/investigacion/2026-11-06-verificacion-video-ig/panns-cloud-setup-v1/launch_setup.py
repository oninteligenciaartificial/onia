from pathlib import Path
import json,sys,hashlib
import supervise
O=Path(__file__).resolve().parent;R=O.parent
p=R/'panns-preflight-v1'
assert hashlib.sha256((p/'manifest.json').read_bytes()).hexdigest()=='79a129ee5338c338205e2b5d0c3bd2139429d40160dd05ce5441145259b12a4a'
for x in json.loads((p/'manifest.json').read_text())['files']:
 f=p/x['path'];assert f.stat().st_size==x['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256']
with open(O/'preparation-once.lock','x') as f:f.write('one global300s budget; no retry or clock reset\n')
r=supervise.run('preparation',[sys.executable,'-B',str(O/'setup.py')],300,300)
print(json.dumps(r,indent=2))
