from pathlib import Path
import hashlib,json,sys
R=Path('/workspace/onia-av-pilot-20261106');O=R/'positivo-v1'
sys.path.insert(0,str(R/'review-v2'));import supervisor
assert hashlib.sha256((R/'review-v2/supervisor.py').read_bytes()).hexdigest()=='bef18dcd8a5bef2b76a82d3502630e0bfb3aa5bc97c11cdc90deb4528ca152c8'
assert 'cf57ebcd-c598-496d-8987-8848bcdfc0f4' in (R/'resume-negativo-v1/workspace-marker.json').read_text()
for x in json.loads((O/'input-freeze.json').read_text())['files']:
 p=O/x['path'];assert p.stat().st_size==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
p=supervisor.Policy(os_thread_cap=16,wall_seconds=600,tree_bytes=16*1024**3)
report=supervisor.run([sys.executable,str(O/'model_driver.py')],'positive-v1',p)
(O/'model-report.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'model-output.log').write_bytes((R/'run-positive-v1/output.log').read_bytes())
print(json.dumps(report,indent=2))
