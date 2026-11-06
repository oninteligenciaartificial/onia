"""Verifica sólo la preparación CPU de una muestra, sin cargar pesos."""
import json
import sys
from pathlib import Path
import soundfile as sf
import torch
from transformers import Qwen3OmniMoeProcessor

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
MODEL=MEDIA/'eureka-preflight'
sys.path.insert(0,str(MEDIA/'eureka-source-cpu'))
import eureka_infer.api.eureka as api

def load_local(path):
    data,sr=sf.read(path,dtype='float32',always_2d=True)
    return torch.from_numpy(data.T.copy()),sr

api.load_audio_data=load_local
obj=api.EurekaAudio.__new__(api.EurekaAudio)
obj.processor=Qwen3OmniMoeProcessor.from_pretrained(str(MODEL),local_files_only=True)
obj.tokenizer=obj.processor.tokenizer
vocab=obj.tokenizer.get_vocab()
obj.audio_placeholder_id=vocab.get('<|audio_pad|>')
obj.audio_start_id=vocab.get('<|audio_start|>')
obj.audio_end_id=vocab.get('<|audio_end|>')
obj.mel_filter_path=str(MODEL/'mel_filters.npz')
obj.device='cpu'
obj.vocab_size=len(vocab)
messages=[{'role':'user','content':[{'type':'audio_url','audio_url':{'url':str(MEDIA/'control-silencio.wav')}},
                                  {'type':'text','text':'Describe the audio.'}]}]
inputs=obj._prepare_inputs(messages)
result={'scope':'preprocesado real de silencio; sin modelo/pesos ni inferencia',
        'input_ids_shape':list(inputs['input_ids'].shape),'token_type_ids_shape':list(inputs['token_type_ids'].shape),
        'mel_shape':list(inputs['mels'].shape) if inputs['mels'] is not None else None,
        'audio_tokens':int((inputs['token_type_ids']==3).sum().item()),
        'vad':False,'mel_is_finite':bool(torch.isfinite(inputs['mels']).all().item())}
(OUT/'eureka-preprocesado.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
