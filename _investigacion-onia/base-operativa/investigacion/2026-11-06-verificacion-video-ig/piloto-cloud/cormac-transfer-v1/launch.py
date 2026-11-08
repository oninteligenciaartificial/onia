from pathlib import Path
import sys,json
R=Path('/workspace/onia-av-pilot-20261106');O=R/'cormac-transfer-v1'
sys.path.insert(0,str(R/'review-v2'));import supervisor
with open(O/'one-attempt.lock','x') as f:f.write('one two-track transfer; no retry\n')
report=supervisor.run([sys.executable,str(O/'transfer.py')],'cormac-transfer-v1',supervisor.Policy(wall_seconds=120,os_thread_cap=16))
(O/'supervisor-report.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'transfer-output.log').write_bytes((R/'run-cormac-transfer-v1/output.log').read_bytes())
print(json.dumps(report,indent=2))
