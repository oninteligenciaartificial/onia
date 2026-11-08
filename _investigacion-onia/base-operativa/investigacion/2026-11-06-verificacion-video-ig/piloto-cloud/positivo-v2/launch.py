from pathlib import Path
import sys,json,os,hashlib
R=Path('/workspace/onia-av-pilot-20261106');O=R/'positivo-v2'
sys.path.insert(0,str(R/'review-v2'));import supervisor
assert hashlib.sha256((R/'review-v2/supervisor.py').read_bytes()).hexdigest()=='bef18dcd8a5bef2b76a82d3502630e0bfb3aa5bc97c11cdc90deb4528ca152c8'
with open(O/'one-attempt.lock','x') as f:f.write('one real-positive attempt; no automatic retry\n')
report=supervisor.run([sys.executable,str(O/'run_driver.py')],'positive-v2',supervisor.Policy(os_thread_cap=16))
(O/'model-report.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'model-output.log').write_bytes((R/'run-positive-v2/output.log').read_bytes())
print(json.dumps(report,indent=2))
