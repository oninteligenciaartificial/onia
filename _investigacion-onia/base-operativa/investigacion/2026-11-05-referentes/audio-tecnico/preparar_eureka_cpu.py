"""Adapta copias locales para CPU SDPA; conserva originales y diff."""
import difflib
import shutil
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
MODEL=MEDIA/'eureka-preflight'
ORIGINAL=MEDIA/'eureka-source/eureka_infer'
COPY=MEDIA/'eureka-source-cpu/eureka_infer'
if COPY.exists():
    raise SystemExit('Ya existe copia CPU; revisar antes de reemplazarla')
shutil.copytree(ORIGINAL,COPY,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
diffs=[]
for path,old,new in [
    (MODEL/'modeling_eureka_audio.py','flash_attention_2','sdpa'),
    (MODEL/'config.json','flash_attention_2','sdpa'),
    (COPY/'api/eureka.py',"device_type='cuda'","device_type='cpu'"),
]:
    text=path.read_text(encoding='utf-8')
    if old not in text: raise RuntimeError('No existe cadena esperada: '+str(path))
    backup=path.with_name(path.name+'.original.txt')
    backup.write_text(text,encoding='utf-8')
    changed=text.replace(old,new)
    path.write_text(changed,encoding='utf-8')
    diffs.extend(difflib.unified_diff(text.splitlines(True),changed.splitlines(True),fromfile=path.name+'.original',tofile=path.name+'.cpu'))
(OUT/'eureka-adaptacion-cpu.diff').write_text(''.join(diffs),encoding='utf-8')
print('Copias CPU y diff preparados; no se cargaron pesos ni se ejecutó inferencia.')
