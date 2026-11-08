from pathlib import Path
import json,hashlib
import supervise
O=Path(__file__).resolve().parent;freeze=json.loads((O/'cormac-input-freeze.json').read_text())
assert hashlib.sha256((O/'infer.py').read_bytes()).hexdigest()==freeze['adapter_sha256']
for x in freeze['windows']:
 assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
 assert json.loads((O/(x['case']+'-input.json')).read_text())==x
with open(O/'cormac-once.lock','x') as f:f.write('four nonoverlapping windows, one attempt each, stop first failure\n')
for x in freeze['windows']:
 case=x['case'];assert not (O/(case+'-receipt.json')).exists()
 r=supervise.run(case,[str(O.parent/'panns-setup-v3/venv/bin/python'),'-B',str(O/'infer.py'),case],120,120)
 print(json.dumps({'case':case,'reason':r['reason'],'exit':r['exit_code'],'wall':r['wall_seconds']},indent=2),flush=True)
 if r['reason']!='exited' or r['exit_code']!=0 or r['pending_live'] or not json.loads((O/(case+'-receipt.json')).read_text())['complete']:raise SystemExit(1)
