"""Freeze authorized synthetic 2-second negative; never calls the model."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import uuid
import wave

ROOT=Path('/workspace/onia-av-pilot-20261106/negativo-v1')
identity=str(uuid.uuid4())
directory=ROOT/'signals'/identity
directory.mkdir(parents=True)
prefix=directory/(uuid.uuid4().hex+'_')
commands=[]
def call(argv,**kwargs):
    commands.append(argv)
    result=subprocess.run(argv,capture_output=True,check=True,**kwargs)
    return result.stdout
image=Path(str(prefix)+'0000.jpg')
call(['ffmpeg','-hide_banner','-loglevel','error','-filter_threads','2',
      '-f','rawvideo','-pixel_format','rgb24','-video_size','224x224','-framerate','1',
      '-i','pipe:0','-frames:v','1','-c:v','mjpeg','-pix_fmt','yuvj444p','-threads','2',str(image)],
     input=bytes([128])*(224*224*3))
shutil.copyfile(image,Path(str(prefix)+'0001.jpg'))
records=[]
for i in range(2):
    jpg=Path(str(prefix)+f'{i:04d}.jpg')
    wav=Path(str(prefix)+f'{i:04d}.wav')
    with wave.open(str(wav),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(bytes(32000))
    with wave.open(str(wav),'rb') as w:
        assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,16000,16000)
        data=w.readframes(16001);assert len(data)==32000 and not any(data)
    dimensions=json.loads(call(['ffprobe','-v','error','-select_streams','v:0',
                                '-show_entries','stream=width,height','-of','json',str(jpg)]))['streams'][0]
    assert dimensions=={'width':224,'height':224}
    pixels=call(['ffmpeg','-hide_banner','-loglevel','error','-threads','2','-i',str(jpg),
                 '-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-threads','2','pipe:1'])
    assert len(pixels)==224*224*3 and len(set(pixels))==1
    for modality,path in [('image',jpg),('audio',wav)]:
        records.append({'chunk':i,'modality':modality,'path':str(path),
                        'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'pts_declared_seconds':i,'duration_declared_seconds':1,
                        'interval_declared':[i,i+1],
                        'verification':dimensions if modality=='image' else {'pcm':'s16le','channels':1,'rate':16000,'samples':16000,'all_zero':True}})
receipt={'opaque_id':identity,'prefix':str(prefix),'chunks':2,'total_duration_declared_seconds':2,
         'frames_represent_their_chunks':True,'files':records,'generator_commands':commands,
         'decoded_uniform_rgb_value':pixels[0],'timing_scope':'declared stimulus PTS, not measured model temporal precision'}
(ROOT/'control-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
(ROOT/'control-truth.json').write_text(json.dumps({'opaque_id':identity,'truth':'uniform static gray image and digital silence throughout both consecutive seconds','intervals':[[0,1],[1,2]],'never_pass_to_model':True},indent=2)+'\n')
print(json.dumps({'control_frozen':True,'opaque_id':identity,'files_verified':4,'model_executed':False}))
