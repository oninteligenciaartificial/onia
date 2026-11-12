import ast,subprocess,json
from pathlib import Path
root=Path.home()/'operacion/homelab'
t=ast.parse(Path(__file__).with_name('PRUEBA-SSH-v4-20261111.py').read_text());n=next(n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='ssh' for x in n.targets));ns={'root':root};exec(compile(ast.Module(body=[n],type_ignores=[]),'ssh','exec'),ns)
code='''import subprocess,json,time,uuid,pathlib,hashlib
p=pathlib.Path.home()/('piloto-render-'+uuid.uuid4().hex);p.mkdir();out=p/'muestra.mp4'
cmd=['ffmpeg','-nostdin','-v','error','-f','lavfi','-i','testsrc2=size=640x360:rate=24','-t','2','-c:v','libx264','-threads','2','-pix_fmt','yuv420p',str(out)]
t=time.monotonic();r=subprocess.run(cmd,capture_output=True,timeout=30);elapsed=time.monotonic()-t
if r.returncode:raise SystemExit('FFmpeg fallo rc='+str(r.returncode))
r=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames:format=duration','-of','json',str(out)],capture_output=True,text=True,check=True,timeout=10)
d=json.loads(r.stdout);assert d['streams'][0]['width']==640 and d['streams'][0]['height']==360 and d['streams'][0]['nb_frames']=='48'
assert abs(float(d['format']['duration'])-2)<0.1
print(json.dumps({'ok':True,'duracion_s':2,'fotogramas':48,'resolucion':'640x360','hilos':2,'tiempo_render_s':round(elapsed,3),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'archivo_conservado':str(out.relative_to(pathlib.Path.home())),'limite':'Muestra sintetica, no benchmark ni video comercial'}))
'''
r=subprocess.run(ns['ssh']+['python3 -I -B -'],input=code,capture_output=True,text=True,timeout=50)
if r.returncode:print(r.stderr[:1000]);raise SystemExit(r.returncode)
d=json.loads(r.stdout);print(json.dumps(d));(root/'ssh/render-piloto.json').write_text(json.dumps(d,indent=2)+'\n')
