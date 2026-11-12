import subprocess,json,uuid,hashlib,base64,datetime
from pathlib import Path
root=Path.home()/'operacion/homelab'
ssh=['ssh','-F','/dev/null','-T','-p','2224','-i',str(root/'ssh/id_ed25519'),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','HostKeyAlias=onia-homelab-worker-2224','-o','UserKnownHostsFile='+str(root/'ssh/known_hosts-worker-2224'),'-o','ConnectTimeout=10','-o','ServerAliveInterval=5','-o','ServerAliveCountMax=2','-o','ProxyCommand='+str(root/'tailscale/bin/tailscale')+' --socket '+str(root/'tailscale/tailscaled.sock')+' nc desktop-0gggnmf 2224','onia-worker@desktop-0gggnmf']
def validate_controls(a, b):
    required = ('sin_capacidades', 'no_new_privs', 'seccomp', 'windows_ausente',
                'host_root_ausente', 'interop_sin_entorno', 'modulos_vacios',
                '/etc_escritura_denegada', '/usr/lib/modules_escritura_denegada',
                'socket_inet_denegado', 'marca_creada')
    if a.get('uid') != 1001 or a.get('grupos') != [1001]:
        raise ValueError('Identidad remota distinta')
    if any(a.get(k) is not True for k in required):
        raise ValueError('Control de aislamiento ausente o fallido')
    if b.get('persistencia_entre_conexiones') is not True:
        raise ValueError('Persistencia entre conexiones no comprobada')

known = (root/'ssh/known_hosts-worker-2224').read_text().strip().split()
if len(known) != 3 or known[:2] != ['onia-homelab-worker-2224', 'ssh-ed25519']:
    raise SystemExit('Known_hosts inesperado')
fp = 'SHA256:' + base64.b64encode(hashlib.sha256(base64.b64decode(known[2], validate=True)).digest()).decode().rstrip('=')
if fp != 'SHA256:4ClsP1NH8JWxBWUNjW2DP7Egn4UcHcqMUYBUu3sL1Gk':
    raise SystemExit('Huella fijada distinta: no autenticar')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
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
validate_controls(a,b)
out={'fecha_inicio':started,'fecha_fin':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'huella':fp,'retornos':[r.returncode,r2.returncode],'huella_verificada':True,'conexion_1':a,'conexion_2':b,'limites':['No prueba cierre de WSL/reinicio','No prueba ASR ni scheduler','No cambia límite de sesiones']}
p=root/'ssh/resultado-ssh-v4.json';p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o600)
