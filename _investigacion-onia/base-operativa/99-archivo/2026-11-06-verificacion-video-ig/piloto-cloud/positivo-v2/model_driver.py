"""Verify frozen inputs, then exec ONE new-context invocation. No retry."""
from pathlib import Path
import hashlib
import json
import os

ROOT=Path('/workspace/onia-av-pilot-20261106')
OUT=ROOT/'positivo-v1'
WEIGHTS=ROOT/'negativo-v1/weights'
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while data:=f.read(1024*1024): h.update(data)
    return h.hexdigest()
freeze=json.loads((ROOT/'review-v2/source-freeze.json').read_bytes())
for item in freeze['sources']:
    path=ROOT/'runtime'/item['path']
    assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256']
libraries=json.loads((ROOT/'negativo-v1/runtime-libraries.json').read_bytes())
for item in libraries['own_elfs']:
    path=Path(item['real_path'])
    assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256']
weights=json.loads((ROOT/'resume-negativo-v1/weights-receipt.json').read_bytes())
assert weights['complete'] and len(weights['verified'])==3
for item in weights['verified']:
    path=WEIGHTS/item['path']
    assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256']
control=json.loads((OUT/'control-manifest.json').read_bytes())
assert control['chunks']==2 and control['chunks']==2
for item in control['files']:
    path=Path(item['path'])
    assert path.stat().st_size==item['bytes'] and digest(path)==item['sha256']
prompt=(ROOT/'negativo-v1/model-prompt.txt').read_text().rstrip('\n')
assert prompt=='Describe qué aparece y qué se oye, en orden; indica qué cambios coinciden. Si algo no puede determinarse, dilo.'
command=[str(ROOT/'build-v2/bin/llama-omni-single-test-omni'),
 '-m',str(WEIGHTS/'MiniCPM-o-4_5-Q4_K_M.gguf'),
 '--audio',str(WEIGHTS/'audio/MiniCPM-o-4_5-audio-F16.gguf'),
 '--vision',str(WEIGHTS/'vision/MiniCPM-o-4_5-vision-F16.gguf'),
 '--test',control['prefix'],'2','-c','2048','--response-tokens','128',
 '--prompt',prompt,'--vision-backend','cpu','--no-tts','-ngl','0']
receipt={'command':command,'model_invocation_attempt':1,'fresh_process_context':True,
         'requested_context':2048,'response_tokens':128,'temperature':0,'seed':20261106,
         'prefill_budget_rule':'actual signal+literal prompt+control+128 < min(2048,llama_n_ctx)',
         'truth_passed_to_model':False,'validated_closed_weights_again_before_exec':True}
with open(OUT/'model-invocation.json','x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print('ONE_MODEL_INVOCATION '+json.dumps(receipt,ensure_ascii=False),flush=True)
os.execv(command[0],command)
