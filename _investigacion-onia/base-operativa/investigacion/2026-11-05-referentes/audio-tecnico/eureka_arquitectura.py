"""Comprueba construcción sin pesos usando meta tensors; no es inferencia."""
import json
import traceback
from pathlib import Path
from accelerate import init_empty_weights
from transformers import AutoConfig,AutoModelForCausalLM

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
model=BASE/'operacion/referentes-20261105/audio/eureka-preflight'
data={'scope':'construcción sin pesos con meta tensors; no valida memoria o inferencia real'}
try:
    config=AutoConfig.from_pretrained(str(model),trust_remote_code=True,local_files_only=True)
    with init_empty_weights():
        obj=AutoModelForCausalLM.from_config(config,trust_remote_code=True)
    data.update(outcome='constructed',parameters=sum(p.numel() for p in obj.parameters()))
except Exception as e:
    data.update(outcome='failed',error_type=type(e).__name__,error=str(e),traceback=traceback.format_exc())
(OUT/'eureka-arquitectura.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in data.items() if k!='traceback'}))
