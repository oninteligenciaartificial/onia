from pathlib import Path
import sys,json
import supervise
O=Path(__file__).resolve().parent
assert json.loads((O/'transfer/report.json').read_text())['exit_code']==0
r=supervise.run('prepare-inputs',[sys.executable,'-B',str(O/'prepare_inputs.py')],120,120)
print(json.dumps(r,indent=2))
