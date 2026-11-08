from pathlib import Path
import json,sys,hashlib
import supervise
O=Path(__file__).resolve().parent;R=O.parent
p=R/'panns-setup-v1'
assert hashlib.sha256((p/'manifest.json').read_bytes()).hexdigest()=='e9427c70225d72538c39e09b0d8ba94b99a2cb2c00e74e1dd2d80af3e12e6230'
for x in json.loads((p/'manifest.json').read_text())['files']:
 f=p/x['path'];assert f.stat().st_size==x['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256']
with open(O/'preparation-once.lock','x') as f:f.write('one global300s budget; no retry or clock reset\n')
r=supervise.run('preparation',[sys.executable,'-B',str(O/'setup.py')],300-0.6820892569994612,299)
print(json.dumps(r,indent=2))
