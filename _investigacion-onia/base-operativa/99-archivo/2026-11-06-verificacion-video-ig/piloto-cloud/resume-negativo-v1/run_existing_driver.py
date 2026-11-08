"""Execute the byte-exact existing driver; relocate TWO receipt paths only.

This preserves negativo-v1's historical incomplete weight receipt and its cuts.
No runtime source, prompt, model argv, resource limit or weight hash is replaced.
"""
from pathlib import Path
import builtins
import hashlib
import json
from unittest.mock import patch

ROOT=Path('/workspace/onia-av-pilot-20261106')
OUT=ROOT/'resume-negativo-v1'
DRIVER=ROOT/'negativo-v1/model_driver.py'
source=DRIVER.read_bytes()
assert hashlib.sha256(source).hexdigest()=='6b8bbac1e3712acf51866f9bc2ec86fe10595f166ea39090d9b0fb773c422ceb'
old_receipt=ROOT/'negativo-v1/weights-receipt.json'
new_receipt=OUT/'weights-receipt.json'
old_invocation=ROOT/'negativo-v1/model-invocation.json'
new_invocation=OUT/'model-invocation.json'
assert not old_invocation.exists() and not new_invocation.exists()
assert json.loads(new_receipt.read_bytes())['complete']
real_read=Path.read_bytes
real_open=builtins.open
def routed_read(path):
    return real_read(new_receipt if path==old_receipt else path)
def routed_open(path,*args,**kwargs):
    try: mapped=new_invocation if Path(path)==old_invocation else path
    except TypeError: mapped=path
    return real_open(mapped,*args,**kwargs)
mapping={'existing_driver':str(DRIVER),'driver_sha256':hashlib.sha256(source).hexdigest(),
         'source_unchanged':True,'receipt_read':{'from':str(old_receipt),'to':str(new_receipt)},
         'exclusive_invocation_write':{'from':str(old_invocation),'to':str(new_invocation)},
         'all_other_io':'unchanged','model_argv_and_prompt':'unchanged'}
with open(OUT/'driver-routing.json','x') as f:json.dump(mapping,f,indent=2);f.write('\n')
with patch.object(Path,'read_bytes',routed_read),patch('builtins.open',routed_open):
    exec(compile(source,str(DRIVER),'exec'),{'__name__':'__main__','__file__':str(DRIVER)})
