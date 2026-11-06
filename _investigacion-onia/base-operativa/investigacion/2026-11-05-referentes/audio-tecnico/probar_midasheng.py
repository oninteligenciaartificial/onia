"""Prueba local ciega, sin VAD ni acceso a red, supervisada por memoria."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
MODEL=MEDIA/'midasheng-model'
TMP=MEDIA/'midasheng-tmp'
OUTPUT=OUT/'midasheng-resultados.json'
MAPPING={'a':'control-tono440.wav','b':'control-voz.wav','c':'control-silencio.wav','d':'control-patron.wav'}
PROMPT='Write a detailed caption about this audio within 1-2 sentences.'


def write(data):
    OUTPUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def worker():
    import torch
    from transformers import AutoModelForCausalLM,AutoProcessor,AutoTokenizer
    torch.set_num_threads(4)
    model=AutoModelForCausalLM.from_pretrained(str(MODEL),trust_remote_code=True,local_files_only=True,
             torch_dtype=torch.float16,low_cpu_mem_usage=True).eval()
    # El frontend acústico produce float32; dejar encoder y proyector en esa
    # precisión evita mezclar su Conv2d con pesos float16. El decoder queda fp16.
    model.audio_encoder.float()
    model.audio_projector.float()
    processor=AutoProcessor.from_pretrained(str(MODEL),trust_remote_code=True,local_files_only=True)
    tokenizer=AutoTokenizer.from_pretrained(str(MODEL),local_files_only=True)
    data={'revision':'3969e451d1c62618089c1135fe4c58ed33af2457','prompt':PROMPT,
          'device':'cpu','threads':4,'dtype':'audio_encoder/projector float32; decoder float16','vad':False,'cases':[]}
    for name,source in MAPPING.items():
        # Filename and prompt convey no expected identity to the model.
        path=TMP/f'sample-{name}.wav'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(MEDIA/source),
                        '-ac','1','-ar','16000','-c:a','pcm_s16le',str(path)],check=True)
        messages=[{'role':'user','content':[{'type':'text','text':PROMPT},{'type':'audio','path':str(path)}]}]
        start=time.monotonic()
        inputs=processor.apply_chat_template(messages,tokenize=True,add_generation_prompt=True,
                    add_special_tokens=True,return_dict=True,return_tensors='pt').to(device='cpu',dtype=torch.float32)
        with torch.inference_mode():
            generated=model.generate(**inputs,max_new_tokens=80,do_sample=False)
        raw=tokenizer.batch_decode(generated,skip_special_tokens=True)[0]
        # La implementación personalizada devuelve sólo los tokens generados,
        # no concatena los tokens del prompt como el generate estándar.
        answer=raw
        data['cases'].append({'case':name,'source_after_blind_run':source,'raw_full':raw,'answer':answer,
                              'seconds':round(time.monotonic()-start,3)})
        write(data)
        print(json.dumps(data['cases'][-1],ensure_ascii=False),flush=True)


def supervise():
    import psutil
    env=os.environ.copy()
    env.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HOME':str(TMP/'hf'),
                'HF_MODULES_CACHE':str(TMP/'hf'/'modules'),'TEMP':str(TMP),'TMP':str(TMP),
                'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','PYTHONUTF8':'1'})
    before=psutil.virtual_memory().available
    if before < 4.75*1024**3:
        print('ABORT: menos de 4.75 GiB disponibles antes de iniciar'); return 2
    proc=subprocess.Popen([sys.executable,'-B',__file__,'worker'],env=env)
    p=psutil.Process(proc.pid)
    start=time.monotonic(); peak=0; minimum=before; reason=None
    while proc.poll() is None:
        try:
            rss=p.memory_info().rss
            for child in p.children(recursive=True):
                try: rss+=child.memory_info().rss
                except psutil.Error: pass
            peak=max(peak,rss); minimum=min(minimum,psutil.virtual_memory().available)
            if minimum<1.8*1024**3: reason='available memory below 1.8 GiB'
            if rss>3.6*1024**3: reason='process RSS above 3.6 GiB'
            if time.monotonic()-start>900: reason='time above 900 s'
            if reason:
                proc.kill(); break
        except psutil.Error: pass
        time.sleep(1)
    code=proc.wait()
    (OUT/'midasheng-recursos.json').write_text(json.dumps({'exit':code,'stop_reason':reason,
       'elapsed_s':round(time.monotonic()-start,2),'rss_peak_bytes':peak,'minimum_available_bytes':minimum,
       'before_available_bytes':before,'limits':'initial >=4.75GiB; available >=1.8GiB; RSS <=3.6GiB; <=900s'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'exit':code,'stop_reason':reason,'peak_gib':round(peak/1024**3,2),
                      'min_free_gib':round(minimum/1024**3,2)}),flush=True)
    return code


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='worker': worker()
    else: sys.exit(supervise())
