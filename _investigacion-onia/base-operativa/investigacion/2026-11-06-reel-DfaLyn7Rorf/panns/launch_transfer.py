from pathlib import Path
import sys,json
import supervise
O=Path(__file__).resolve().parent
with open(O/'transfer-once.lock','x') as f:f.write('two supplied public tracks, one transfer phase, retries0\n')
r=supervise.run('transfer',[sys.executable,'-B',str(O/'transfer.py')],120,120)
print(json.dumps(r,indent=2))
