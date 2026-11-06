"""Reproduce sólo la inicialización del encoder Eureka sin bajar pesos."""
import json
import traceback
from pathlib import Path
import torch

from transformers.models.whisper.configuration_whisper import WhisperConfig
from transformers.models.whisper.modeling_whisper import WhisperEncoder

cfg=WhisperConfig(d_model=64,encoder_layers=1,decoder_layers=1,encoder_attention_heads=4,
                  decoder_attention_heads=4,encoder_ffn_dim=128,decoder_ffn_dim=128)
cfg._attn_implementation='flash_attention_2'  # misma asignación que el código oficial
result={'scope':'constructor con configuración reducida y sin pesos; no inferencia acústica',
        'source':'https://huggingface.co/cslys1999/Eureka-Audio-Instruct',
        'revision':'219761da53c9c6c5900a84a723d88ccc29db66d3'}
try:
    WhisperEncoder(cfg)
    result['outcome']='constructor succeeded'
except Exception as exc:
    result.update(outcome='constructor failed',error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc())
try:
    cfg._attn_implementation='sdpa'
    encoder=WhisperEncoder(cfg).eval()
    with torch.inference_mode():
        value=encoder(torch.zeros(1,80,3000)).last_hidden_state
    result['sdpa_alternative']={'status':'small synthetic encoder forward succeeded','shape':list(value.shape),
        'scope':'untrained tiny encoder; not Eureka weights, not acoustic inference'}
except Exception as exc:
    result['sdpa_alternative']={'status':'failed','type':type(exc).__name__,'error':str(exc)}
Path(__file__).with_name('eureka-preflight.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='traceback'},ensure_ascii=False))
