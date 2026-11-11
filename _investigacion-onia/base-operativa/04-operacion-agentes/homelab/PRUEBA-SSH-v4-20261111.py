import subprocess,json,uuid
from pathlib import Path
root=Path.home()/'operacion/homelab'
ssh=['ssh','-F','/dev/null','-T','-p','2224','-i',str(root/'ssh/id_ed25519'),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','HostKeyAlias=onia-homelab-worker-2224','-o','UserKnownHostsFile='+str(root/'ssh/known_hosts-worker-2224'),'-o','ConnectTimeout=10','-o','ServerAliveInterval=5','-o','ServerAliveCountMax=2','-o','ProxyCommand='+str(root/'tailscale/bin/tailscale')+' --socket '+str(root/'tailscale/tailscaled.sock')+' nc desktop-0gggnmf 2224','onia-worker@desktop-0gggnmf']
marker='ensayo-ssh-'+uuid.uuid4().hex
code='''import os,json,pathlib,socket,subprocess,shutil
s=dict(x.split(':',1) for x in pathlib.Path('/proc/self/status').read_text().splitlines() if ':' in x)
r={'uid':os.getuid(),'grupos':os.getgroups(),'sin_capacidades':int(s['CapEff'].strip(),16)==0,'no_new_privs':s['NoNewPrivs'].strip()=='1','seccomp':s['Seccomp'].strip()=='2','windows_ausente':not pathlib.Path('/mnt/c').exists(),'host_root_ausente':not pathlib.Path('/root').exists(),'interop_sin_entorno':not os.environ.get('WSL_INTEROP'),'modulos_vacios':not list(pathlib.Path('/usr/lib/modules').iterdir())}
for folder in ('/etc','/usr/lib/modules'):
 try:pathlib.Path(folder,'onia-prueba-escritura').write_text('test');r[folder+'_escritura_denegada']=False
 except OSError:r[folder+'_escritura_denegada']=True
try:socket.socket(socket.AF_INET,socket.SOCK_STREAM);r['socket_inet_denegado']=False
except OSError:r['socket_inet_denegado']=True
r['herramientas']={n:bool(shutil.which(n)) for n in ('python3','ffmpeg','git')}
p=pathlib.Path.home()/MARKER;p.write_text('prueba-controlada-ssh');r['marca_creada']=True
print(json.dumps(r))
'''.replace('MARKER',repr(marker))
r=subprocess.run(ssh+['python3 -I -B -'],input=code,text=True,capture_output=True,timeout=35)
if r.returncode: print('SSH falló, rc',r.returncode);print(r.stderr[:1500]);raise SystemExit(1)
a=json.loads(r.stdout);print(json.dumps({'conexion_1':a}))
code2='import pathlib,json; p=pathlib.Path.home()/'+repr(marker)+'; print(json.dumps({"persistencia_entre_conexiones":p.read_text()=="prueba-controlada-ssh"}))'
r2=subprocess.run(ssh+['python3 -I -B -'],input=code2,text=True,capture_output=True,timeout=25)
if r2.returncode:raise SystemExit('Segunda conexión falló')
b=json.loads(r2.stdout);print(json.dumps({'conexion_2':b}))
out={'huella_verificada':True,'conexion_1':a,'conexion_2':b,'limites':['No prueba cierre de WSL/reinicio','No prueba ASR ni scheduler','No cambia límite de sesiones']}
p=root/'ssh/resultado-ssh-v4.json';p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o600)
