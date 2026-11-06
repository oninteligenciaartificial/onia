"""Eureka CPU con SDPA: prueba ciega supervisada, sin VAD ni red."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
MODEL=MEDIA/'eureka-preflight'
SOURCE=MEDIA/'eureka-source-cpu'
TMP=MEDIA/'midasheng-tmp'
PROMPT='Describe the audio.'
MAPPING={'a':'control-tono440.wav','b':'control-voz.wav','c':'control-silencio.wav','d':'control-patron.wav'}
SELECTION=os.environ.get('ONIA_CASES','a,b,c,d').split(',')
if not SELECTION or len(set(SELECTION))!=len(SELECTION) or any(k not in MAPPING for k in SELECTION):
    raise ValueError('ONIA_CASES requiere IDs únicos entre a,b,c,d')
SUFFIX='' if SELECTION==['a','b','c','d'] else '-'+''.join(SELECTION)


def worker():
    import soundfile as sf
    import torch
    from eureka_safe_loader import install
    install()
    torch.set_num_threads(4)
    sys.path.insert(0,str(SOURCE))
    import eureka_infer.api.eureka as api
    # torchaudio 2.11 exige torchcodec; leer WAV local con soundfile conserva
    # la forma de onda y evita instalar un backend adicional.
    def load_local(path):
        data,sr=sf.read(path,dtype='float32',always_2d=True)
        return torch.from_numpy(data.T.copy()),sr
    api.load_audio_data=load_local
    model=api.EurekaAudio(model_path=str(MODEL),device='cpu')
    result={'revision':'219761da53c9c6c5900a84a723d88ccc29db66d3',
       'prompt':PROMPT,'device':'cpu','threads':4,'vad':False,'dtype':'float32',
       'adaptation':'SDPA; Accelerate CPU 2GiB/disk; local numpy BF16 loader; WAV via soundfile', 'cases':[]}
    for name in SELECTION:
        source=MAPPING[name]
        path=TMP/f'eureka-{name}.wav'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(MEDIA/source),
                        '-ac','1','-ar','16000','-c:a','pcm_s16le',str(path)],check=True)
        messages=[{'role':'user','content':[{'type':'audio_url','audio_url':{'url':str(path)}},
                                          {'type':'text','text':PROMPT}]}]
        start=time.monotonic()
        answer=model.generate(messages,max_new_tokens=80,temperature=0.0,top_p=1.0,top_k=0,do_sample=False)
        result['cases'].append({'case':name,'source_after_blind_run':source,'answer':answer,
                                'elapsed_s':round(time.monotonic()-start,3)})
        (OUT/f'eureka-resultados{SUFFIX}.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(json.dumps(result['cases'][-1],ensure_ascii=False),flush=True)


def supervise():
    import psutil
    before=psutil.virtual_memory().available
    if before<7.5*1024**3:
        print('ABORT: menos de 7.5 GiB disponibles al inicio'); return 2
    env=os.environ.copy()
    env.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HOME':str(TMP/'hf-eureka-fp32'),
                'HF_MODULES_CACHE':str(TMP/'hf-eureka-fp32'/'modules'),'TEMP':str(TMP),'TMP':str(TMP),
                'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','PYTHONUTF8':'1',
                'ONIA_OFFLOAD_DIR':str(MEDIA/'eureka-offload-fp32-2g')})
    proc=subprocess.Popen([sys.executable,'-B',__file__,'worker'],env=env)
    p=psutil.Process(proc.pid); start=time.monotonic(); peak=0; minimum=before; reason=None
    while proc.poll() is None:
        try:
            rss=p.memory_info().rss
            for c in p.children(recursive=True):
                try: rss+=c.memory_info().rss
                except psutil.Error: pass
            peak=max(peak,rss); minimum=min(minimum,psutil.virtual_memory().available)
            if minimum<2*1024**3: reason='available memory below 2 GiB'
            if rss>5.5*1024**3: reason='process RSS above 5.5 GiB'
            if time.monotonic()-start>900: reason='time above 900 seconds'
            if reason: proc.kill(); break
        except psutil.Error: pass
        time.sleep(1)
    code=proc.wait()
    data={'exit':code,'stop_reason':reason,'elapsed_s':round(time.monotonic()-start,2),
          'rss_peak_bytes':peak,'minimum_available_bytes':minimum,'before_available_bytes':before,
          'limits':'CPU weights <=2GiB plus disk offload; initial >=7.5GiB; available >=2GiB; RSS <=5.5GiB; <=900s'}
    (OUT/f'eureka-recursos{SUFFIX}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data),flush=True)
    return code


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='worker': worker()
    else: sys.exit(supervise())
