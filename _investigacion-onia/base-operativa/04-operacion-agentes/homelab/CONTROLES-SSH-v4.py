import ast,subprocess,json,os
from pathlib import Path
root=Path.home()/'operacion/homelab'
tree=ast.parse(Path(__file__).with_name('PRUEBA-SSH-v4-20261111.py').read_text()); node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ssh' for t in n.targets)); ns={'root':root};exec(compile(ast.Module(body=[node],type_ignores=[]),'ssh','exec'),ns);ssh=ns['ssh']
results={}
def run(args,code=None):return subprocess.run(args,input=code,capture_output=True,text=True,timeout=25)
r=run(ssh[:-1]+['-tt',ssh[-1],'true']);results['tty_denegado']='PTY allocation request failed' in r.stderr
r=run(ssh[:-1]+['-o','ExitOnForwardFailure=yes','-R','0:localhost:2224',ssh[-1],'true']);results['forward_remoto_denegado']=r.returncode!=0 and 'remote port forwarding failed' in r.stderr
noauth=ssh.copy();noauth[noauth.index('-i')+1]='/dev/null';r=run(noauth+['true']);results['sin_llave_denegado']=r.returncode!=0 and 'Permission denied' in r.stderr
code='''import pathlib,subprocess,os,json,uuid
r={}
for path in ('/mnt/c/Windows','/proc/1/root/mnt/c/Windows','/proc/self/root/mnt/c/Windows','/run/WSL','/home/onia-codex-worker'):
 r[path]=not pathlib.Path(path).exists()
p=pathlib.Path.home()/('enlace-prueba-'+uuid.uuid4().hex);p.symlink_to('/mnt/c/Windows');r['enlace_windows_denegado']=not p.exists()
try:
 x=subprocess.run(['sudo','-n','true'],capture_output=True);r['sudo_denegado']=x.returncode!=0
except FileNotFoundError:r['sudo_ausente']=True
try:
 x=subprocess.run(['/opt/onia/interop-canary.exe'],capture_output=True,timeout=5);r['pe_denegado']=x.returncode!=0
except OSError:r['pe_denegado']=True
r['sin_fds_mayores_2']=all(int(x)<=2 or not pathlib.Path('/proc/self/fd',x).exists() for x in os.listdir('/proc/self/fd'))
print(json.dumps(r))
'''
r=run(ssh+['python3 -I -B -'],code)
if r.returncode:print('diagnostico rc',r.returncode,r.stderr[:1200]);raise SystemExit(1)
results['aislamiento_adicional']=json.loads(r.stdout)
print(json.dumps(results,indent=2));(root/'ssh/controles-adicionales.json').write_text(json.dumps(results,indent=2)+'\n')
