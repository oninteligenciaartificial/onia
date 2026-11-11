#!/usr/bin/python3
"""Alta local WSL autorizada. Sin descargas; --apply sólo por Sergio como root.

No ejecuta sudo, no borra, no cambia red/WSL/AppArmor. Si falla aislamiento,
no instala la llave ni habilita la shell. Conserva originales en /root.
"""
import argparse
import configparser
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
import stat
import sys

# Sólo el montaje observado en DESKTOP-0GGGNMF; otro kernel requiere diagnóstico.
MODULE_MOUNT = Path('/usr/lib/modules/6.18.33.2-microsoft-standard-WSL2')

def mounts_safe(sources, mountinfo=None):
    text = Path('/proc/self/mountinfo').read_text() if mountinfo is None else mountinfo
    mounts = []
    for line in text.splitlines():
        left, right = line.split(' - ', 1)
        target = re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1],8)), left.split()[4])
        if not target.startswith('/') or str(Path(target)) != target or '..' in Path(target).parts:
            raise RuntimeError('DENEGADO: destino de montaje no canónico')
        mounts.append((Path(target), right.split()[0]))
    module_mounts = [(p, fs) for p, fs in mounts
                     if p == Path('/usr/lib/modules') or Path('/usr/lib/modules') in p.parents]
    if module_mounts and module_mounts != [(MODULE_MOUNT, 'overlay')]:
        raise RuntimeError('DENEGADO: montaje de módulos distinto del observado')
    for path in (Path('/usr/lib/modules'), MODULE_MOUNT):
        if path.exists() or path.is_symlink():
            info = path.lstat()
            if (path.resolve() != path or not stat.S_ISDIR(info.st_mode)
                    or (module_mounts and (info.st_uid != 0 or info.st_gid != 0 or info.st_mode & 0o022))):
                raise RuntimeError('DENEGADO: ruta de módulos no segura')
        elif module_mounts:
            raise RuntimeError('DENEGADO: montaje de módulos sin directorio')
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
            if (path == mount or path in mount.parents) and not (mount == Path('/usr/lib/wsl') or Path('/usr/lib/wsl') in mount.parents or (mount, fs) == (MODULE_MOUNT, 'overlay')):
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
    # Después del bind de /usr/lib: nunca exponer el árbol de módulos del host.
    args += ['--tmpfs', '/usr/lib/modules', '--remount-ro', '/usr/lib/modules']
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
assert pathlib.Path('/usr/lib/modules').is_dir(), 'máscara de módulos ausente'
assert not any(pathlib.Path('/usr/lib/modules').iterdir()), 'módulos del host expuestos'
try:
    with open('/usr/lib/modules/escritura-prohibida', 'x') as stream: stream.write('test')
except OSError: pass
else: raise AssertionError('máscara de módulos escribible')
assert set(p.name for p in pathlib.Path('/home').iterdir()) == {'onia-worker'}
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
tag = None
if '--preflight' not in sys.argv[4:]:
    tag = 'prueba-' + uuid.uuid4().hex
    work = pathlib.Path.home() / tag
    work.mkdir(mode=0o700)
    (work / 'persistencia.txt').write_text('aislamiento sintético\n')
    (work / 'enlace-windows').symlink_to('/mnt/c')
    assert not (work / 'enlace-windows' / 'Windows').exists()
print(json.dumps({'ok': True, 'uid_no_root': True, 'sin_capacidades': True,
                  'no_new_privs': True, 'pid_y_red_aislados': True,
                  'windows_y_host_no_expuestos': True, 'etc_solo_lectura': True,
                  'sudo_rechazado': True, 'persistencia': tag,
                  'modulos_ocultos_solo_lectura': True,
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

HOST_CANARY = 'Canario sintético fuera del sandbox, sin datos privados.\n'
# Bytes exactos del instalador v3 SHA256 3e640659…656be; no se adopta otro wrapper.
V3_WRAPPER_SHA256 = '15bb695532d1d433ee6a8bf5e94e296b7f813328214039a24045d3279f8a41bd'
V3_CHECK_SHA256 = 'a5b29f52275be780ac5bbbfedf5633325a9a6fb56c3a81cfdff54b10c54e5ed2'


def checked_metadata(path, mode, uid=0, gid=0, directory=False):
    info = path.lstat()
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if (not kind(info.st_mode) or info.st_uid != uid or info.st_gid != gid or
            stat.S_IMODE(info.st_mode) != mode or
            (not directory and info.st_nlink != 1)):
        raise RuntimeError('Metadatos distintos del corte PE revisado: ' + path.name)
    for parent in path.parents:
        st = parent.lstat()
        if not stat.S_ISDIR(st.st_mode) or st.st_uid != 0 or st.st_mode & 0o022:
            raise RuntimeError('Padre no controlado por root; conservar y revisar')


def checked_pe():
    path = ROOT/'interop-canary.exe'
    checked_metadata(path, 0o755)
    if path.stat().st_size != len(pe_canary()) or path.read_bytes() != pe_canary():
        raise RuntimeError('Canario PE distinto del generado; no ejecutar')
    return path


def validate_pe_partial(account):
    """Sólo el árbol exacto dejado ANTES del control PE v2; nunca adopta datos nuevos."""
    checked_metadata(ROOT, 0o755, directory=True)
    scope = {'__name__': 'validate_mounts'}
    exec(compile(WRAPPER, 'worker-mount-validation', 'exec'), scope)
    scope['mounts_safe']([str(ROOT)])
    expected = {'login', 'work', 'etc', 'host-only', 'interop-canary.exe'}
    if set(x.name for x in ROOT.iterdir()) != expected:
        raise RuntimeError('Árbol parcial distinto del corte PE; no retomar')
    for name in ('login', 'work', 'etc'):
        path = ROOT/name
        worker = name == 'work'
        checked_metadata(path, 0o700 if worker else 0o755,
                         account.pw_uid if worker else 0,
                         account.pw_gid if worker else 0, directory=True)
        if any(path.iterdir()):
            raise RuntimeError('Directorio del corte PE no vacío: ' + name)
    checked_metadata(ROOT/'host-only', 0o644)
    if (ROOT/'host-only').read_bytes() != HOST_CANARY.encode():
        raise RuntimeError('Canario host distinto; no retomar')
    checked_pe()


def config_contents(account):
    contents = {
        'passwd': f'onia-worker:x:{account.pw_uid}:{account.pw_gid}:worker:/home/onia-worker:/bin/bash\n'.encode(),
        'group': f'onia-worker:x:{account.pw_gid}:\n'.encode(),
        'nsswitch.conf': b'passwd: files\ngroup: files\nhosts: files\n',
    }
    # v3 copió estos archivos desde el host. Un cambio del host obliga a parar;
    # ni se inventa su contenido ni se acepta cualquier archivo con ese nombre.
    for name in ('ld.so.cache', 'localtime'):
        source = Path('/etc')/name
        if not source.exists():
            if source.is_symlink(): raise RuntimeError('Fuente de configuración colgante')
            continue
        resolved = source.resolve(strict=True)
        if resolved != source and not (name == 'localtime' and resolved.is_relative_to('/usr/share/zoneinfo')):
            raise RuntimeError('Fuente de configuración enlazada no aprobada')
        checked_metadata(resolved, 0o644)
        if resolved.stat().st_size > 8 * 1024 * 1024:
            raise RuntimeError('Fuente de configuración supera el límite')
        contents[name] = resolved.read_bytes()
    return contents


def check_absent_publication():
    for path in (UNIT, Path('/run/systemd/system/onia-worker-sshd.service'),
                 Path('/usr/lib/systemd/system/onia-worker-sshd.service'),
                 Path('/etc/systemd/system/multi-user.target.wants/onia-worker-sshd.service'),
                 Path('/run/onia-worker-sshd')):
        if os.path.lexists(path):
            raise RuntimeError('Unidad o runtime ya publicado; no retomar v3')


def validate_mount_partial(account):
    """Corte v3 ANTES de CHECK: lectura estricta, sin adoptar pruebas ni datos nuevos."""
    checked_metadata(ROOT, 0o755, directory=True)
    scope = {'__name__': 'validate_mounts'}
    exec(compile(WRAPPER, 'worker-mount-validation', 'exec'), scope)
    scope['mounts_safe']([str(ROOT), str(SHELL), str(RUNTIME), str(KEY_DIR)])
    expected = {'login', 'work', 'etc', 'host-only', 'interop-canary.exe', 'check-isolation.py'}
    if set(p.name for p in ROOT.iterdir()) != expected:
        raise RuntimeError('Árbol distinto del corte de montaje v3; conservar y diagnosticar')
    for name in ('login', 'work', 'etc'):
        worker = name == 'work'
        checked_metadata(ROOT/name, 0o700 if worker else 0o755,
                         account.pw_uid if worker else 0,
                         account.pw_gid if worker else 0, directory=True)
        if name != 'etc' and any((ROOT/name).iterdir()):
            raise RuntimeError('Datos o pruebas previas en el corte v3; no retomar')
    contents = config_contents(account)
    if set(p.name for p in (ROOT/'etc').iterdir()) != set(contents):
        raise RuntimeError('Configuración parcial v3 distinta; no retomar')
    for name, content in contents.items():
        path = ROOT/'etc'/name
        checked_metadata(path, 0o644)
        if path.read_bytes() != content:
            raise RuntimeError('Bytes de configuración distintos del host revisado: ' + name)
    checked_metadata(KEY_DIR, 0o755, directory=True)
    if set(p.name for p in KEY_DIR.iterdir()) != {'sshd_config'}:
        raise RuntimeError('Llave u otro archivo SSH ya presente; no retomar')
    files = ((SHELL, 0o755, V3_WRAPPER_SHA256),
             (ROOT/'check-isolation.py', 0o644, V3_CHECK_SHA256),
             (RUNTIME, 0o755, hashlib.sha256(RUNTIME_SCRIPT.encode()).hexdigest()),
             (SSH_RULE, 0o600, hashlib.sha256(SSH_CONFIG.encode()).hexdigest()),
             (ROOT/'host-only', 0o644, hashlib.sha256(HOST_CANARY.encode()).hexdigest()))
    for path, mode, digest in files:
        checked_metadata(path, mode)
        if path.stat().st_size > 128 * 1024 or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError('Archivo distinto de los bytes v3 revisados: ' + path.name)
    checked_pe()
    check_absent_publication()


def isolation_probe(account, candidate=False, preflight=False):
    """CHECK con timeout y diagnóstico acotado; nunca vuelca stdout/stderr del hijo."""
    text = 'python3 - ' + shlex.join([str(account.pw_uid), os.readlink('/proc/self/ns/net'),
                                    os.readlink('/proc/self/ns/pid')] + (['--preflight'] if preflight else []))
    entry = ['/usr/bin/python3', '-I', '-c', WRAPPER] if candidate else [str(SHELL)]
    command = ['/usr/bin/setpriv', '--reuid', str(account.pw_uid), '--regid', str(account.pw_gid),
               '--init-groups', '/usr/bin/env', '-i'] + entry + ['-c', text]
    try:
        result = subprocess.run(command, input=CHECK.encode(), capture_output=True, timeout=20, cwd='/')
    except subprocess.TimeoutExpired:
        raise RuntimeError('CHECK detenido: TimeoutExpired (20s); conservar cuenta cerrada') from None
    report = {'returncode': result.returncode, 'stdout_bytes': len(result.stdout),
              'stderr_bytes': len(result.stderr), 'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
              'indicios': [label for token, label in (
                  (b'submontaje', 'submontaje'), (b'montaje de m', 'modulos_montaje'),
                  (b'bwrap:', 'bwrap'), (b'AssertionError', 'CHECK_assert'),
                  (b'Permission denied', 'permisos'), (b'namespace', 'namespace')) if token in result.stderr]}
    if result.returncode != 0 or len(result.stdout) > 8192:
        raise RuntimeError('CHECK no aprobado: ' + json.dumps(report))
    try: data = json.loads(result.stdout)
    except (ValueError, UnicodeError):
        raise RuntimeError('CHECK sin JSON válido: ' + json.dumps(report)) from None
    flags = {'ok', 'uid_no_root', 'sin_capacidades', 'no_new_privs', 'pid_y_red_aislados',
             'windows_y_host_no_expuestos', 'etc_solo_lectura', 'sudo_rechazado',
             'modulos_ocultos_solo_lectura'}
    if (not isinstance(data, dict) or set(data) != flags | {'persistencia', 'limite'}
            or any(data.get(key) is not True for key in flags)):
        raise RuntimeError('CHECK sin aprobación de aislamiento y módulos')
    tag = data['persistencia']
    import re
    if (preflight and tag is not None) or (not preflight and
            (not isinstance(tag, str) or not re.fullmatch(r'prueba-[0-9a-f]{32}', tag))):
        raise RuntimeError('CHECK sin resultado de persistencia válido')
    if data['limite'] != 'Prueba local del aislamiento; no acredita SSH remoto, ASR ni WSL persistente.':
        raise RuntimeError('CHECK con campos no reconocidos; conservar salida privada')
    return data


def resume_mount_partial(account, backup):
    # La candidata se ejecuta en Python aislado como worker, sin instalarla.
    # Preflight no escribe pruebas en work: cualquier rechazo deja v3 intacta.
    validate_mount_partial(account)
    isolation_probe(account, candidate=True, preflight=True)
    validate_mount_partial(account)
    saved = backup/'estado-v3'
    saved.mkdir(mode=0o700)
    paths = [SHELL, RUNTIME, SSH_RULE, ROOT/'check-isolation.py', ROOT/'host-only',
             ROOT/'interop-canary.exe'] + sorted((ROOT/'etc').iterdir())
    manifest = []
    for index, path in enumerate(paths):
        data = path.read_bytes()
        original = saved/str(index)
        shutil.copy2(path, original, follow_symlinks=False)
        if original.read_bytes() != data:
            raise RuntimeError('Respaldo v3 incompleto; no sustituir wrapper')
        with original.open('rb') as stream: os.fsync(stream.fileno())
        st = path.lstat()
        manifest.append({'ruta': str(path), 'copia': str(index), 'sha256': hashlib.sha256(data).hexdigest(),
                         'modo': oct(stat.S_IMODE(st.st_mode)), 'uid': st.st_uid, 'gid': st.st_gid})
    write_new(saved/'manifest.json', json.dumps(manifest, indent=2)+'\n', 0o600)
    directory_fd = os.open(saved, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(directory_fd)
    finally: os.close(directory_fd)
    validate_mount_partial(account)
    # Estado de intento inmutable: incluso un corte posterior exige diagnóstico,
    # no una segunda ejecución que sobrescriba archivos parcialmente actualizados.
    candidate = SHELL.with_name('onia-worker-shell.v4-pending')
    if os.path.lexists(candidate): raise RuntimeError('Candidata v4 existente; conservar y diagnosticar')
    write_new(ROOT/'retoma-v4.json', json.dumps({'respaldo_v3': str(saved), 'preflight': 'OK'})+'\n', 0o600)
    write_new(ROOT/'check-isolation-v4.py', CHECK)
    write_new(candidate, WRAPPER, 0o755)
    # Sólo reemplaza el wrapper autenticado; runtime, etc y CHECK v3 se conservan.
    checked_metadata(SHELL, 0o755)
    if hashlib.sha256(SHELL.read_bytes()).hexdigest() != V3_WRAPPER_SHA256:
        raise RuntimeError('Wrapper cambió durante la retoma; no sustituir')
    os.replace(candidate, SHELL)


def pe_probe():
    """Una ejecución inocua, cinco segundos, bytes; nunca imprime stderr/entorno crudos."""
    path = checked_pe()
    started = time.monotonic()
    try:
        result = subprocess.run([str(path)], stdin=subprocess.DEVNULL,
                                capture_output=True, timeout=5, cwd='/')
        report = {'ok': result.returncode == 0, 'returncode': result.returncode,
                  'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr),
                  'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
                  'indicios': [label for token, label in (
                      (b'CreateProcess', 'CreateProcess'), (b'execvpe', 'execvpe'),
                      (b'Exec format error', 'exec_format'),
                      (b'Permission denied', 'permission_denied'),
                      (b'No such file', 'missing_file'),
                      (b'invalid', 'invalid')) if token in result.stderr]}
    except subprocess.TimeoutExpired:
        report = {'ok': False, 'exception': 'TimeoutExpired', 'timeout_s': 5}
    except OSError as exc:
        report = {'ok': False, 'exception': type(exc).__name__, 'errno': exc.errno}
    report['elapsed_s'] = round(time.monotonic() - started, 3)
    return report


def diagnose_pe():
    """No configura ni escribe: indicadores acotados y canario existente verificado."""
    report = {'diagnostico_sin_cambios': True, 'instalacion': 'no ejecutada'}
    for name in ('status', 'WSLInterop'):
        path = Path('/proc/sys/fs/binfmt_misc')/name
        try:
            lines = path.read_text().splitlines()
            report[name] = {'presente': True,
                'estado': lines[0] if lines and lines[0] in ('enabled', 'disabled') else 'unknown',
                'interpreter_init': 'interpreter /init' in lines}
        except OSError as exc:
            report[name] = {'presente': False, 'errno': exc.errno}
    config = configparser.ConfigParser(interpolation=None)
    try:
        with open('/etc/wsl.conf') as stream: config.read_file(stream)
        report['wsl_conf'] = {}
        for section, key in (('interop', 'enabled'), ('interop', 'appendWindowsPath'), ('boot', 'systemd')):
            raw = config.get(section, key, fallback='unspecified').lower()
            report['wsl_conf'][section + '.' + key] = raw if raw in ('true', 'false', 'unspecified') else 'unknown'
    except (OSError, configparser.Error) as exc:
        report['wsl_conf'] = {'lectura': type(exc).__name__}
    endpoint = os.environ.get('WSL_INTEROP')
    report['WSL_INTEROP'] = {'presente': bool(endpoint), 'socket': False}
    if endpoint:
        try: report['WSL_INTEROP']['socket'] = stat.S_ISSOCK(os.stat(endpoint).st_mode)
        except OSError: pass
    try: report['mount_noexec'] = bool(os.statvfs(ROOT/'interop-canary.exe').f_flag & os.ST_NOEXEC)
    except OSError: report['mount_noexec'] = None
    try:
        canary = ROOT/'interop-canary.exe'
        info = canary.lstat()
        report['canario'] = {'regular': stat.S_ISREG(info.st_mode),
            'uid': info.st_uid, 'gid': info.st_gid, 'modo': oct(stat.S_IMODE(info.st_mode)),
            'bytes': info.st_size, 'enlaces': info.st_nlink,
            'sha256_esperado': hashlib.sha256(pe_canary()).hexdigest()}
    except OSError as exc:
        report['canario'] = {'errno': exc.errno}
    try: report['control_pe'] = pe_probe()
    except (OSError, RuntimeError) as exc:
        # The only RuntimeErrors here are our fixed metadata/content diagnostics.
        report['control_pe'] = {'ok': False, 'no_ejecutado': True,
                                'exception': type(exc).__name__,
                                'errno': getattr(exc, 'errno', None)}
    report['causa_en_pc'] = 'pendiente de interpretar; este diagnóstico no acepta el homelab'
    return report


def prepare_pe_partial(account, resume):
    if resume:
        validate_pe_partial(account)
        return
    ROOT.mkdir(mode=0o755)
    for name in ('login', 'work', 'etc'):
        (ROOT/name).mkdir(mode=0o755 if name != 'work' else 0o700)
    os.chown(ROOT/'work', account.pw_uid, account.pw_gid)
    write_new(ROOT/'host-only', HOST_CANARY)
    write_new(ROOT/'interop-canary.exe', pe_canary(), 0o755)


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
    """Valida identidad cerrada y respaldo original; el árbol se valida por separado."""
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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true', help='Sergio ejecuta localmente como root en la PC autorizada')
    mode.add_argument('--diagnose-pe', action='store_true', help='Sólo lectura y canario PE existente verificado; no instala')
    resume = parser.add_mutually_exclusive_group()
    resume.add_argument('--resume-pe-control', action='store_true', help='Sólo el árbol parcial exacto de ALTA-DETENIDA-v2')
    resume.add_argument('--resume-mount-control', action='store_true', help='Sólo el corte exacto de montaje v3; preflight y respaldo antes de sustituir')
    parser.add_argument('--resume-backup', type=Path,
                        help='Retoma sólo la cuenta cerrada uid/gid1001; respaldo original privado en /root')
    args = parser.parse_args()
    if (args.resume_pe_control or args.resume_mount_control) and (not args.apply or args.resume_backup is None):
        parser.error('La retoma del árbol requiere --apply y --resume-backup ORIGINAL')
    if args.diagnose_pe and args.resume_backup is not None:
        parser.error('El diagnóstico no retoma ni necesita respaldo')
    if not args.apply and not args.diagnose_pe:
        print('Preparado; no aplicado. Requiere --apply local como root en DESKTOP-0GGGNMF/Ubuntu.')
        return
    if os.geteuid() != 0 or socket.gethostname().upper() != MACHINE:
        raise RuntimeError('Requiere root LOCAL en DESKTOP-0GGGNMF; no aplicar en VPS ni laptop')
    if 'microsoft' not in Path('/proc/sys/kernel/osrelease').read_text().lower():
        raise RuntimeError('No se identificó WSL')
    if args.diagnose_pe:
        print(json.dumps(diagnose_pe(), ensure_ascii=False))
        return
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
    if args.resume_pe_control:
        validate_pe_partial(existing)
    if args.resume_mount_control:
        validate_mount_partial(existing)
    os.umask(0o022)
    for path in (ROOT, SHELL, KEY_DIR, UNIT, RUNTIME):
        if path == ROOT and args.resume_pe_control:
            continue  # Exact tree/metadata verified above, not an overwrite allowance.
        if args.resume_mount_control and path in (ROOT, SHELL, KEY_DIR, RUNTIME):
            continue  # Exact v3 bytes, parents and metadata verified above.
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
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
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
    if not args.resume_mount_control:
        prepare_pe_partial(account, args.resume_pe_control)
    # Positive control remains mandatory; a diagnostic is not a bypass.
    control = pe_probe()
    if not control['ok']:
        raise RuntimeError('Control PE fuera del sandbox falló; cuenta cerrada: ' + json.dumps(control))
    if args.resume_mount_control:
        check_effective()  # Rechazar configuración/host key antes de sustituir v3.
        resume_mount_partial(account, backup)
    else:
        for filename, content in config_contents(account).items():
            write_new(ROOT/'etc'/filename, content)
        SHELL.parent.mkdir(parents=True,exist_ok=True)
        write_new(SHELL,WRAPPER,0o755)
        write_new(RUNTIME,RUNTIME_SCRIPT,0o755)
        write_new(ROOT/'check-isolation.py',CHECK)
        KEY_DIR.mkdir(mode=0o755)
        write_new(SSH_RULE,SSH_CONFIG,0o600)
    check_effective()
    local_result = isolation_probe(account)
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
