#!/usr/bin/python3
"""Alta local WSL autorizada. Sin descargas; --apply sólo por Sergio como root.

No ejecuta sudo, no borra, no cambia red/WSL/AppArmor. Si falla aislamiento,
no instala la llave ni habilita la shell. Conserva originales en /root.
"""
import argparse
import glob
import datetime
import hashlib
import json
import os
from pathlib import Path
import pwd
import grp
import shlex
import shutil
import socket
import stat
import struct
import subprocess
import sys
import time

MACHINE = 'DESKTOP-0GGGNMF'
HOST_FP = 'SHA256:4ClsP1NH8JWxBWUNjW2DP7Egn4UcHcqMUYBUu3sL1Gk'
PUBLIC_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICF3iY+5cqZ2iJaAWtiGs/VWSYDIDTmwT5EHQ4h20g2U onia-homelab-worker-20261109'
USER = 'onia-worker'
ROOT = Path('/var/lib/onia-worker')
SHELL = Path('/usr/local/libexec/onia-worker-shell')
SSH_RULE = Path('/etc/ssh/onia-worker/sshd_config')
KEY_DIR = Path('/etc/ssh/onia-worker')
UNIT = Path('/etc/systemd/system/onia-worker-sshd.service')
RUNTIME = Path('/usr/local/libexec/onia-worker-runtime')

# Python isolated mode avoids PYTHONPATH, PYTHONHOME and user site before confinement.
WRAPPER = r'''#!/usr/bin/python3 -I
import ctypes
import os
from pathlib import Path
import pwd
import re
import sys

def mounts_safe(sources, mountinfo=None):
    text = Path('/proc/self/mountinfo').read_text() if mountinfo is None else mountinfo
    mounts = []
    for line in text.splitlines():
        left, right = line.split(' - ', 1)
        target = re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1],8)), left.split()[4])
        mounts.append((Path(target), right.split()[0]))
    for source in sources:
        path = Path(source).resolve()
        if path != Path(source):
            raise RuntimeError('DENEGADO: fuente enlazada')
        parent_mount, parent_fs = max(((p,fs) for p,fs in mounts if path == p or p in path.parents), key=lambda item:len(str(item[0])))
        if parent_mount != Path('/'):
            raise RuntimeError('DENEGADO: fuente sobre montaje separado no aprobado')
        if parent_fs not in {'ext4','xfs','btrfs','overlay','tmpfs'}:
            raise RuntimeError('DENEGADO: filesystem no aprobado')
        for mount, fs in mounts:
            if (path == mount or path in mount.parents) and not (mount == Path('/usr/lib/wsl') or Path('/usr/lib/wsl') in mount.parents):
                raise RuntimeError('DENEGADO: submontaje no aprobado')

def filter_fd():
    lib = ctypes.CDLL('libseccomp.so.2')
    class Cmp(ctypes.Structure):
        _fields_=[('arg',ctypes.c_uint),('op',ctypes.c_int),('a',ctypes.c_uint64),('b',ctypes.c_uint64)]
    lib.seccomp_init.argtypes=[ctypes.c_uint32];lib.seccomp_init.restype=ctypes.c_void_p
    lib.seccomp_release.argtypes=[ctypes.c_void_p]
    lib.seccomp_syscall_resolve_name.argtypes=[ctypes.c_char_p];lib.seccomp_syscall_resolve_name.restype=ctypes.c_int
    lib.seccomp_rule_add_array.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_int,ctypes.c_uint,ctypes.POINTER(Cmp)]
    lib.seccomp_export_bpf.argtypes=[ctypes.c_void_p,ctypes.c_int]
    ctx=lib.seccomp_init(0x7fff0000)  # ALLOW; unknown ABI remains killed by libseccomp.
    if not ctx: raise RuntimeError('seccomp no disponible')
    fd=os.memfd_create('onia-worker-seccomp',0)
    try:
        for name in (b'socket',b'socketpair',b'io_uring_setup'):
            syscall=lib.seccomp_syscall_resolve_name(name)
            if syscall < 0: raise RuntimeError('syscall desconocido')
            # Only local UNIX sockets. VSOCK, Hyper-V, INET and other families denied.
            cmp=Cmp(0,1,1,0)  # arg0 != AF_UNIX
            count=0 if name==b'io_uring_setup' else 1
            if lib.seccomp_rule_add_array(ctx,0x00050001,syscall,count,ctypes.byref(cmp) if count else None)<0:
                raise RuntimeError('No se pudo construir seccomp')
        if lib.seccomp_export_bpf(ctx,fd)<0: raise RuntimeError('No se pudo exportar seccomp')
        os.lseek(fd,0,os.SEEK_SET);os.set_inheritable(fd,True)
        return fd
    except Exception:
        os.close(fd);raise
    finally: lib.seccomp_release(ctx)

def command(work, config, text, canary=None):
    sources=[str(work),str(config)]+['/usr/'+n for n in ('bin','sbin','lib','lib64','share') if Path('/usr/'+n).exists()]
    mounts_safe(sources)
    fd=filter_fd()
    args = ['/usr/bin/bwrap', '--unshare-user', '--unshare-pid',
            '--unshare-net', '--unshare-ipc', '--unshare-uts',
            '--die-with-parent', '--new-session', '--cap-drop', 'ALL',
            '--seccomp', str(fd),
            '--hostname', 'onia-worker', '--clearenv',
            '--setenv', 'PATH', '/usr/bin:/bin',
            '--setenv', 'HOME', '/home/onia-worker',
            '--setenv', 'USER', 'onia-worker', '--setenv', 'LOGNAME', 'onia-worker',
            '--setenv', 'LANG', 'C.UTF-8', '--setenv', 'LC_ALL', 'C.UTF-8',
            '--setenv', 'SHELL', '/bin/bash']
    # Deliberate allowlist: never bind the host /, /home, /run, /mnt or /usr/local.
    for name in ('bin', 'sbin', 'lib', 'lib64', 'share'):
        source = '/usr/' + name
        if Path(source).exists():
            args += ['--ro-bind', source, source]
    for name in ('bin', 'sbin', 'lib', 'lib64'):
        if Path('/usr/' + name).exists():
            args += ['--symlink', 'usr/' + name, '/' + name]
    if Path('/usr/lib/wsl').exists():
        args += ['--tmpfs', '/usr/lib/wsl']
    if canary is not None:
        args += ['--ro-bind', str(canary), '/opt/onia/interop-canary.exe']
    args += ['--ro-bind', str(config), '/etc', '--proc', '/proc', '--dev', '/dev',
             '--tmpfs', '/tmp', '--tmpfs', '/run',
             '--bind', str(work), '/home/onia-worker',
             '--chdir', '/home/onia-worker',
             '/bin/bash', '--noprofile', '--norc', '-c', text]
    return args

def main():
    account = pwd.getpwnam('onia-worker')
    if os.geteuid() != account.pw_uid or os.geteuid() == 0:
        raise SystemExit('DENEGADO: identidad worker requerida')
    work = Path('/var/lib/onia-worker/work')
    config = Path('/var/lib/onia-worker/etc')
    for path in (Path('/var/lib/onia-worker'), config):
        st = path.lstat()
        if path.is_symlink() or st.st_uid != 0 or st.st_mode & 0o022:
            raise SystemExit('DENEGADO: control de rutas modificado')
    if work.is_symlink() or work.stat().st_uid != account.pw_uid:
        raise SystemExit('DENEGADO: workspace no válido')
    text = os.environ.get('SSH_ORIGINAL_COMMAND')
    if text is None and len(sys.argv) == 3 and sys.argv[1] == '-c':
        text = sys.argv[2]
    if not text or text == '/usr/local/libexec/onia-worker-shell':
        raise SystemExit('DENEGADO: usar un comando explícito, sin sesión interactiva')
    os.chdir('/')
    # Drop inherited descriptors before creating the mount/pid namespaces.
    for name in os.listdir('/proc/self/fd'):
        fd = int(name)
        if fd > 2:
            try: os.close(fd)
            except OSError: pass
    os.umask(0o077)
    os.execve('/usr/bin/bwrap', command(work, config, text, Path('/var/lib/onia-worker/interop-canary.exe')),
              {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'})

if __name__ == '__main__':
    main()
'''

CHECK = r'''import json, os, pathlib, socket, subprocess, sys, uuid
uid, host_net, host_pid = int(sys.argv[1]), sys.argv[2], sys.argv[3]
assert os.getuid() == uid and os.geteuid() == uid and uid != 0
status = dict(x.split(':', 1) for x in pathlib.Path('/proc/self/status').read_text().splitlines() if ':' in x)
assert status['NoNewPrivs'].strip() == '1'
assert status['Seccomp'].strip() == '2'
assert int(status['CapEff'].strip(), 16) == 0
assert os.readlink('/proc/self/ns/net') != host_net
assert os.readlink('/proc/self/ns/pid') != host_pid
assert not os.environ.get('WSL_INTEROP') and not os.environ.get('WSLENV')
for family in (2,10,40,43):
    try: sock=socket.socket(family,socket.SOCK_STREAM)
    except PermissionError: pass
    else:
        sock.close();raise AssertionError('familia socket no bloqueada: '+str(family))
if pathlib.Path('/opt/onia/interop-canary.exe').exists():
    try:
        pe=subprocess.run(['/opt/onia/interop-canary.exe'],capture_output=True,timeout=5)
    except OSError: pass
    else: assert pe.returncode != 0, 'PE Windows pudo ejecutarse'
for name in ('/mnt/c', '/mnt/wsl', '/init', '/run/WSL', '/root',
             '/var/lib/onia-worker/host-only', '/etc/shadow', '/etc/ssh',
             '/proc/1/root/mnt/c', '/proc/1/root/var/lib/onia-worker/host-only'):
    assert not pathlib.Path(name).exists(), 'ruta expuesta: ' + name
if pathlib.Path('/usr/lib/wsl').exists():
    assert not any(pathlib.Path('/usr/lib/wsl').iterdir())
assert set(p.name for p in pathlib.Path('/home').iterdir()) == {'onia-worker'}
tag = 'prueba-' + uuid.uuid4().hex
work = pathlib.Path.home() / tag
work.mkdir(mode=0o700)
(work / 'persistencia.txt').write_text('aislamiento sintético\n')
(work / 'enlace-windows').symlink_to('/mnt/c')
assert not (work / 'enlace-windows' / 'Windows').exists()
denied = False
try:
    with open('/etc/onia-escritura-prohibida', 'x') as stream: stream.write('test')
except OSError: denied = True
assert denied, '/etc debe ser sólo lectura'
result = subprocess.run(['/usr/bin/sudo', '-n', 'true'], capture_output=True) if pathlib.Path('/usr/bin/sudo').exists() else None
assert result is None or result.returncode != 0
# /proc is the private pid namespace; no outside process descriptors are reachable.
for path in pathlib.Path('/proc/self/fd').iterdir():
    try: target = os.readlink(path)
    except FileNotFoundError: continue
    assert not target.startswith(('/mnt/', '/var/lib/onia-worker/', '/root/'))
print(json.dumps({'ok': True, 'uid_no_root': True, 'sin_capacidades': True,
                  'no_new_privs': True, 'pid_y_red_aislados': True,
                  'windows_y_host_no_expuestos': True, 'etc_solo_lectura': True,
                  'sudo_rechazado': True, 'persistencia': tag,
                  'limite': 'Prueba local del aislamiento; no acredita SSH remoto, ASR ni WSL persistente.'}))
'''

SSH_CONFIG = '''# Servidor separado, sólo loopback; no hereda Include/Match/PAM del SSH personal.
Port 2224
ListenAddress 127.0.0.1
HostKey /etc/ssh/ssh_host_ed25519_key
PidFile /run/onia-worker-sshd/sshd.pid
AllowUsers onia-worker
PermitRootLogin no
UsePAM no
PermitUserEnvironment no
StrictModes yes
PrintMotd no
UseDNS no
LoginGraceTime 20
MaxSessions 3
MaxStartups 3:30:5
TrustedUserCAKeys none
    AuthenticationMethods publickey
    PubkeyAuthentication yes
    PasswordAuthentication no
    KbdInteractiveAuthentication no
    AuthorizedKeysFile /etc/ssh/onia-worker/authorized_keys
    AuthorizedKeysCommand none
    AuthorizedPrincipalsFile none
    AuthorizedPrincipalsCommand none
    ForceCommand /usr/local/libexec/onia-worker-shell
    DisableForwarding yes
    AllowTcpForwarding no
    AllowAgentForwarding no
    X11Forwarding no
    PermitTunnel no
    PermitTTY no
    PermitUserRC no
'''

SYSTEMD_UNIT = '''[Unit]
Description=OnIA worker SSH aislado (loopback)
After=network.target
[Service]
Type=simple
RuntimeDirectory=onia-worker-sshd
ExecStartPre=/usr/local/libexec/onia-worker-runtime
ExecStart=/usr/sbin/sshd -D -e -f /etc/ssh/onia-worker/sshd_config
Restart=on-failure
RestartSec=5
UMask=0077
[Install]
WantedBy=multi-user.target
'''

RUNTIME_SCRIPT = '''#!/usr/bin/python3 -I
import os
from pathlib import Path
p=Path('/run/sshd')
os.umask(0o022)
if not p.exists() and not p.is_symlink(): p.mkdir(mode=0o755)
s=p.lstat()
if p.is_symlink() or not p.is_dir() or s.st_uid!=0 or s.st_mode & 0o022:
    raise SystemExit('Privsep /run/sshd no seguro; conservar y revisar')
'''

def personal_ssh_safe():
    # Conservative baseline: never reconfigure the personal daemon to make this pass.
    visited=set()
    def inspect(path):
        path=Path(path)
        if path in visited: return
        visited.add(path)
        if not path.resolve().is_relative_to('/etc/ssh'):
            raise RuntimeError('Include SSH personal fuera de /etc/ssh; revisar')
        for line in path.read_text().splitlines():
            fields=shlex.split(line,comments=True)
            if not fields: continue
            key, sep, value=fields[0].partition('=')
            if sep: fields=[key]+([value] if value else [])+fields[1:]
            name=fields[0].lower()
            if name=='match': raise RuntimeError('SSH personal tiene Match: requiere comprobar sus rutas de autenticación')
            if name=='include':
                for pattern in fields[1:]:
                    if not pattern.startswith('/'): pattern='/etc/ssh/'+pattern
                    for child in glob.glob(pattern): inspect(child)
    inspect('/etc/ssh/sshd_config')
    values=dict(line.split(' ',1) for line in run(['/usr/sbin/sshd','-T'],capture_output=True).stdout.splitlines() if ' ' in line)
    for name in ('trustedusercakeys','authorizedkeyscommand'):
        if values.get(name)!='none': raise RuntimeError('Autenticación SSH personal externa: '+name)
    for name in ('hostbasedauthentication','gssapiauthentication','kerberosauthentication','kbdinteractiveauthentication'):
        if values.get(name)!='no': raise RuntimeError('Método SSH personal no auditado: '+name)
    keys=values.get('authorizedkeysfile','').split()
    if not keys or any(k not in ('.ssh/authorized_keys','.ssh/authorized_keys2') for k in keys):
        raise RuntimeError('SSH personal usa llaves compartidas; revisar')
    # Detect daemon overrides instead of pretending default sshd -T covers them.
    defaults=Path('/etc/default/ssh')
    if defaults.exists():
        for line in defaults.read_text().splitlines():
            fields=shlex.split(line,comments=True)
            if fields and fields[0].startswith('SSHD_OPTS=') and fields!=['SSHD_OPTS=']:
                raise RuntimeError('SSHD_OPTS personal no vacío; revisar')
    for comm in Path('/proc').glob('[0-9]*/comm'):
        try:
            if comm.read_text().strip()!='sshd': continue
            cmd=(comm.parent/'cmdline').read_bytes().replace(b'\0',b' ')
        except (FileNotFoundError,ProcessLookupError): continue
        import re
        if any(re.match(rb'^-[^-]*[fo]',arg) for arg in cmd.split()):
            raise RuntimeError('Daemon SSH personal con argumentos alternativos; revisar')

def verify_listener():
    expected='0100007F:'+format(2224,'04X')
    for _ in range(15):
        pid=run(['systemctl','show','-p','MainPID','--value','onia-worker-sshd.service'],capture_output=True).stdout.strip()
        if pid.isdigit() and pid!='0':
            inodes=set()
            for fd in Path('/proc',pid,'fd').glob('*'):
                try: target=os.readlink(fd)
                except FileNotFoundError: continue
                if target.startswith('socket:['): inodes.add(target[8:-1])
            for line in Path('/proc/net/tcp').read_text().splitlines()[1:]:
                cols=line.split()
                if cols[1]==expected and cols[3]=='0A' and cols[9] in inodes:
                    scan=run(['ssh-keyscan','-T','3','-p','2224','-t','ed25519','127.0.0.1'],capture_output=True)
                    fingerprint=run(['ssh-keygen','-lf','-'],input=scan.stdout,capture_output=True).stdout.split()[1]
                    if fingerprint!=HOST_FP: raise RuntimeError('Huella del listener distinta')
                    return
        time.sleep(0.2)
    raise RuntimeError('Listener no confirmado como propiedad del servicio worker')

def pe_canary():
    # Synthetic AMD64 PE: entry point only returns zero; no imports or file/network I/O.
    data=bytearray(1024);data[:2]=b'MZ';struct.pack_into('<I',data,0x3c,0x80)
    data[0x80:0x84]=b'PE\0\0'
    struct.pack_into('<HHIIIHH',data,0x84,0x8664,1,0,0,0,240,0x23)
    o=0x98;struct.pack_into('<H',data,o,0x20b)
    struct.pack_into('<I',data,o+4,512);struct.pack_into('<I',data,o+16,0x1000)
    struct.pack_into('<I',data,o+20,0x1000);struct.pack_into('<Q',data,o+24,0x140000000)
    struct.pack_into('<II',data,o+32,0x1000,0x200)
    struct.pack_into('<HH',data,o+40,6,0);struct.pack_into('<HH',data,o+48,6,0)
    struct.pack_into('<II',data,o+56,0x2000,0x200);struct.pack_into('<H',data,o+68,3)
    struct.pack_into('<QQQQ',data,o+72,0x100000,0x1000,0x100000,0x1000)
    struct.pack_into('<I',data,o+108,16)
    section=o+240;data[section:section+8]=b'.text\0\0\0'
    struct.pack_into('<IIII',data,section+8,3,0x1000,512,512)
    struct.pack_into('<I',data,section+36,0x60000020);data[512:515]=b'\x31\xc0\xc3'
    return bytes(data)

def run(args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)

def write_new(path, content, mode=0o644):
    # Exclusive creation, including rejection of existing symlinks.
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    with os.fdopen(fd,'wb') as stream:
        stream.write(content.encode() if isinstance(content,str) else content)
        stream.flush();os.fsync(stream.fileno())

def check_effective():
    run(['/usr/sbin/sshd', '-t','-f',str(SSH_RULE)])
    result = run(['/usr/sbin/sshd', '-T','-f',str(SSH_RULE)], capture_output=True)
    values = dict(line.split(' ', 1) for line in result.stdout.splitlines() if ' ' in line)
    required = {'authenticationmethods':'publickey', 'pubkeyauthentication':'yes',
                'passwordauthentication':'no', 'kbdinteractiveauthentication':'no',
                'authorizedkeysfile':str(KEY_DIR/'authorized_keys'),
                'authorizedkeyscommand':'none', 'forcecommand':str(SHELL),
                'disableforwarding':'yes', 'allowtcpforwarding':'no',
                'allowagentforwarding':'no', 'x11forwarding':'no', 'permittunnel':'no',
                'permittty':'no', 'permituserrc':'no', 'permituserenvironment':'no',
                'trustedusercakeys':'none','usepam':'no','allowusers':'onia-worker'}
    for key, expected in required.items():
        if values.get(key) != expected:
            raise RuntimeError('sshd efectivo no cumple: ' + key)
    if values.get('acceptenv') or values.get('setenv'):
        raise RuntimeError('No se acepta entorno externo en el SSH worker')

def sudo_policy_denied(policy, hostname):
    # sudo clásico y sudo-rs difieren en rc. Una frase exacta de denegación
    # sin líneas adicionales es obligatoria; rc=0 solo nunca acredita seguridad.
    expected = f'User {USER} is not allowed to run sudo on {hostname}.'
    return (policy.returncode in (0, 1) and
            (policy.stdout + policy.stderr).strip() == expected)


def validate_closed_account(account, backup):
    """Sólo retoma el corte documentado previo a crear ROOT/llaves/servicio."""
    if (account.pw_uid != 1001 or account.pw_gid != 1001 or
            account.pw_dir != str(ROOT/'login') or
            account.pw_shell != '/usr/sbin/nologin' or
            os.getgrouplist(USER, account.pw_gid) != [account.pw_gid]):
        raise RuntimeError('Cuenta previa distinta del intento cerrado revisado; no retomar')
    group = grp.getgrnam(USER)
    if group.gr_gid != account.pw_gid or group.gr_mem:
        raise RuntimeError('Grupo previo no exclusivo; no retomar')
    if any(a.pw_name != USER and (a.pw_uid == account.pw_uid or a.pw_gid == account.pw_gid)
           for a in pwd.getpwall()):
        raise RuntimeError('UID o grupo primario compartido; no retomar')
    if any(g.gr_name != USER and g.gr_gid == account.pw_gid for g in grp.getgrall()):
        raise RuntimeError('Alias de grupo compartido; no retomar')
    if not os.access('/usr/bin/sudo', os.X_OK):
        raise RuntimeError('Falta sudo observado en el intento previo; no retomar')
    entries = [line.split(':') for line in Path('/etc/shadow').read_text().splitlines()
               if line.split(':', 1)[0] == USER]
    if len(entries) != 1 or entries[0][1] != '*':
        raise RuntimeError('Password previa no coincide con cuenta cerrada; no retomar')
    backup = Path(backup)
    if (backup.parent != Path('/root') or not backup.name.startswith('onia-worker-originales-')
            or any(p.is_symlink() for p in (backup, *backup.parents))):
        raise RuntimeError('Respaldo de retoma inválido')
    info = backup.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o077:
        raise RuntimeError('Respaldo no privado de root')
    for name in ('passwd', 'group', 'shadow', 'gshadow'):
        original = backup/name
        info = original.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise RuntimeError('Original de respaldo no seguro')
        if any(line.split(':', 1)[0] == USER for line in original.read_text().splitlines()):
            raise RuntimeError('La cuenta ya existía antes del intento; no retomar')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Sergio ejecuta localmente como root en la PC autorizada')
    parser.add_argument('--resume-backup', type=Path,
                        help='Retoma sólo la cuenta cerrada uid/gid1001; respaldo original privado en /root')
    args = parser.parse_args()
    if not args.apply:
        print('Preparado; no aplicado. Requiere --apply local como root en DESKTOP-0GGGNMF/Ubuntu.')
        return
    if os.geteuid() != 0 or socket.gethostname().upper() != MACHINE:
        raise RuntimeError('Requiere root LOCAL en DESKTOP-0GGGNMF; no aplicar en VPS ni laptop')
    if 'microsoft' not in Path('/proc/sys/kernel/osrelease').read_text().lower():
        raise RuntimeError('No se identificó WSL')
    fingerprint = run(['ssh-keygen','-lf','/etc/ssh/ssh_host_ed25519_key.pub'],capture_output=True).stdout.split()[1]
    if fingerprint != HOST_FP:
        raise RuntimeError('Huella host distinta: detener y verificar, no aceptar automáticamente')
    for binary in ('/usr/bin/bwrap','/usr/bin/python3','/usr/bin/setpriv','/usr/sbin/sshd','/usr/sbin/useradd','/usr/sbin/usermod'):
        if not os.access(binary, os.X_OK): raise RuntimeError('Falta dependencia: ' + binary)
    try: existing = pwd.getpwnam(USER)
    except KeyError: existing = None
    if existing:
        if args.resume_backup is None:
            raise RuntimeError('onia-worker ya existe; conservar y revisar antes de modificarlo')
        validate_closed_account(existing, args.resume_backup)
    elif args.resume_backup is not None:
        raise RuntimeError('Retoma solicitada sin cuenta previa; detener')
    os.umask(0o022)
    for path in (ROOT, SHELL, KEY_DIR, UNIT, RUNTIME):
        if os.path.lexists(path): raise RuntimeError('Ruta existente; no sobrescribir: ' + str(path))
        for parent in path.parents:
            if parent.is_symlink(): raise RuntimeError('Padre enlazado: ' + str(parent))
            if parent.exists() and (parent.stat().st_uid != 0 or parent.stat().st_mode & 0o022):
                raise RuntimeError('Padre no controlado por root: '+str(parent))
    if Path('/etc/ssh/sshrc').exists():
        raise RuntimeError('Existe sshrc global: necesita revisión antes del alta')
    exec(compile(RUNTIME_SCRIPT,'privsep-preflight','exec'),{'__name__':'preflight'})
    personal_ssh_safe()
    listener=socket.socket()
    try:listener.bind(('127.0.0.1',2224))
    finally:listener.close()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = Path('/root') / ('onia-worker-originales-' + stamp)
    backup.mkdir(mode=0o700)
    for original in ('/etc/passwd','/etc/group','/etc/shadow','/etc/gshadow','/etc/ssh/sshd_config'):
        if Path(original).exists(): shutil.copy2(original,backup/Path(original).name)
    # Until ALL local checks pass the account has no key and a nologin shell.
    if existing is None:
        run(['/usr/sbin/useradd','--no-create-home','--user-group','--home-dir',str(ROOT/'login'),
             '--shell','/usr/sbin/nologin','--password','*',USER])
    account = pwd.getpwnam(USER)
    groups = os.getgrouplist(USER,account.pw_gid)
    if groups != [account.pw_gid]: raise RuntimeError('Worker con grupos suplementarios; no habilitar')
    if Path('/usr/bin/sudo').exists():
        # Root's local policy query only; never executes a sudo command as worker.
        policy=subprocess.run(['/usr/bin/sudo','-n','-l','-U',USER],capture_output=True,text=True,
                              env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'})
        if not sudo_policy_denied(policy, socket.gethostname()):
            raise RuntimeError('Política sudo del worker requiere revisión; no habilitar')
    ROOT.mkdir(mode=0o755)
    for name in ('login','work','etc'):
        (ROOT/name).mkdir(mode=0o755 if name != 'work' else 0o700)
    os.chown(ROOT/'work',account.pw_uid,account.pw_gid)
    write_new(ROOT/'host-only','Canario sintético fuera del sandbox, sin datos privados.\n')
    write_new(ROOT/'interop-canary.exe',pe_canary(),0o755)
    # Positive control must work outside confinement; otherwise this test proves nothing.
    try: control=run([str(ROOT/'interop-canary.exe')],capture_output=True,timeout=5)
    except Exception as exc:
        raise RuntimeError('No funciona el control PE inocuo fuera del sandbox; conservar cuenta cerrada') from exc
    write_new(ROOT/'etc/passwd',f'onia-worker:x:{account.pw_uid}:{account.pw_gid}:worker:/home/onia-worker:/bin/bash\n')
    write_new(ROOT/'etc/group',f'onia-worker:x:{account.pw_gid}:\n')
    write_new(ROOT/'etc/nsswitch.conf','passwd: files\ngroup: files\nhosts: files\n')
    for filename in ('ld.so.cache','localtime'):
        source=Path('/etc')/filename
        if source.exists(): shutil.copyfile(source,ROOT/'etc'/filename)
    SHELL.parent.mkdir(parents=True,exist_ok=True)
    write_new(SHELL,WRAPPER,0o755)
    write_new(RUNTIME,RUNTIME_SCRIPT,0o755)
    write_new(ROOT/'check-isolation.py',CHECK)
    KEY_DIR.mkdir(mode=0o755)
    write_new(SSH_RULE,SSH_CONFIG,0o600)
    check_effective()
    text='python3 - '+shlex.join([str(account.pw_uid),os.readlink('/proc/self/ns/net'),os.readlink('/proc/self/ns/pid')])
    probe=run(['/usr/bin/setpriv','--reuid',str(account.pw_uid),'--regid',str(account.pw_gid),
               '--init-groups','/usr/bin/env','-i',str(SHELL),'-c',text],input=CHECK,capture_output=True)
    local_result=json.loads(probe.stdout)
    if local_result.get('ok') is not True: raise RuntimeError('Prueba local no aprobada')
    write_new(ROOT/'alta-local-v1.json',json.dumps({'fecha':stamp,'host_fingerprint':fingerprint,
              'grupos_solo_worker':True,'prueba_local':local_result,'ssh_remoto':'pendiente',
              'red_del_worker':'aislada; transferencia por stdin/stdout SSH, sin red API/browser',
              'wsl_persistente':'pendiente'},ensure_ascii=False,indent=2)+'\n')
    # Dedicated loopback listener: existing SSH and its users are untouched.
    write_new(UNIT,SYSTEMD_UNIT)
    run(['systemctl','daemon-reload'])
    run(['systemctl','enable','--now','onia-worker-sshd.service'])
    run(['systemctl','is-active','--quiet','onia-worker-sshd.service'])
    verify_listener()
    run(['/usr/sbin/usermod','--shell',str(SHELL),USER])
    pending=KEY_DIR/'authorized_keys.pending'
    write_new(pending,'restrict,command="'+str(SHELL)+'" '+PUBLIC_KEY+'\n')
    os.link(pending,KEY_DIR/'authorized_keys')  # atomic publish, fail if target exists; retain pending copy.
    print(json.dumps({'alta_local':'OK','pruebas_locales':local_result,'host_fingerprint':fingerprint,
                      'ssh_remoto':'PENDIENTE','wsl_persistencia':'PENDIENTE',
                      'respaldo_privado':str(backup)},ensure_ascii=False))

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        # Do not include arbitrary command stdout, configs, password databases or secrets.
        print('ALTA DETENIDA: '+str(exc),file=sys.stderr)
        print('Conservar lo creado; no desactivar protecciones ni repetir a ciegas. Avisar a Codex.',file=sys.stderr)
        raise SystemExit(1)
