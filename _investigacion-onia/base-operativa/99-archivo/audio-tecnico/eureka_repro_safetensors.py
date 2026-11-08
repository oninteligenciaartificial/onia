"""Diagnóstico sólo lectura: pesos pequeños de normalización desde el shard."""
import json
from pathlib import Path
from safetensors import safe_open

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
model=BASE/'operacion/referentes-20261105/audio/eureka-preflight'
index=json.loads((model/'model.safetensors.index.json').read_text(encoding='utf-8'))['weight_map']
keys=sorted(k for k in index if k.startswith('backbone.model.layers.') and k.endswith('input_layernorm.weight'))
for key in keys:
    print('leyendo',key,flush=True)
    with safe_open(str(model/index[key]),framework='pt',device='cpu') as f:
        weight=f.get_tensor(key)
        print('ok',key,list(weight.shape),str(weight.dtype),float(weight[0]),flush=True)
print('TERMINADO',len(keys),flush=True)
