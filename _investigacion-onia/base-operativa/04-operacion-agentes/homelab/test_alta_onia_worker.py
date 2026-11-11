import importlib.util
import json
import hashlib
import errno
from contextlib import contextmanager, ExitStack
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
import stat
from types import SimpleNamespace
from unittest.mock import patch

SOURCE = Path(__file__).with_name('alta-onia-worker.py')
spec = importlib.util.spec_from_file_location('alta', SOURCE)
alta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alta)


class BootstrapSafety(unittest.TestCase):
    def test_sudo_classic_and_rs_exact_denial(self):
        message = 'User onia-worker is not allowed to run sudo on DESKTOP-0GGGNMF.\n'
        for code in (0, 1):
            for stdout, stderr in ((message, ''), ('', message)):
                self.assertTrue(alta.sudo_policy_denied(SimpleNamespace(
                    returncode=code, stdout=stdout, stderr=stderr), 'DESKTOP-0GGGNMF'))

    def test_sudo_denial_rejects_grants_errors_and_other_identity(self):
        denial = 'User onia-worker is not allowed to run sudo on DESKTOP-0GGGNMF.'
        for text, code in [(denial, 2), ('', 0), ('parse error', 1),
                           (denial+'\n(ALL) ALL', 0), (denial.replace('onia-worker', 'otro'), 0),
                           (denial.replace('DESKTOP-0GGGNMF', 'otro'), 1),
                           ('User onia-worker may run the following commands: (ALL) ALL', 0)]:
            self.assertFalse(alta.sudo_policy_denied(SimpleNamespace(
                returncode=code, stdout=text, stderr=''), 'DESKTOP-0GGGNMF'))

    def test_resume_closed_account_and_reject_any_changed_identity(self):
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001, pw_name=alta.USER,
            pw_dir=str(alta.ROOT/'login'), pw_shell='/usr/sbin/nologin')
        def data(path, *args, **kwargs):
            return 'onia-worker:*:1:0:99999:7:::\n' if str(path)=='/etc/shadow' else 'root:x:0:0:root:/root:/bin/bash\n'
        def info(path, *args, **kwargs):
            return SimpleNamespace(st_uid=0, st_mode=(stat.S_IFDIR|0o700) if path.name.startswith('onia-worker-originales-') else (stat.S_IFREG|0o600))
        with patch.object(alta.os, 'getgrouplist', return_value=[1001]), \
             patch.object(alta.grp, 'getgrnam', return_value=SimpleNamespace(gr_gid=1001, gr_mem=[])), \
             patch.object(alta.grp, 'getgrall', return_value=[SimpleNamespace(gr_name=alta.USER,gr_gid=1001)]), \
             patch.object(alta.os, 'access', return_value=True), \
             patch.object(alta.pwd, 'getpwall', return_value=[account]), \
             patch.object(Path, 'read_text', data), patch.object(Path, 'stat', info), \
             patch.object(Path, 'lstat', info):
            alta.validate_closed_account(account, '/root/onia-worker-originales-test')
            for changes in ({'pw_uid':0}, {'pw_gid':27}, {'pw_shell':'/bin/bash'}, {'pw_dir':'/home/otro'}):
                with self.subTest(changes=changes), self.assertRaises(RuntimeError):
                    alta.validate_closed_account(SimpleNamespace(**(vars(account)|changes)), '/root/onia-worker-originales-test')
            with patch.object(alta.os,'getgrouplist',return_value=[1001,27]), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')
            with patch.object(Path,'read_text',return_value='onia-worker:!hash:1:0:99999:7:::\n'), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')
            with self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/tmp/onia-worker-originales-test')
            with patch.object(Path,'is_symlink',return_value=True), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')
            with patch.object(alta.pwd,'getpwall',return_value=[account,SimpleNamespace(pw_name='otro',pw_uid=1002,pw_gid=1001)]), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')
            with patch.object(alta.grp,'getgrall',return_value=[SimpleNamespace(gr_name='alias',gr_gid=1001)]), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')
            with patch.object(alta.os,'access',return_value=False), self.assertRaises(RuntimeError):
                alta.validate_closed_account(account,'/root/onia-worker-originales-test')

    def test_default_never_applies(self):
        result = subprocess.run(['python3', str(SOURCE)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('no aplicado', result.stdout)

    def test_wrong_machine_refused_before_mutation(self):
        with patch('sys.argv', [str(SOURCE), '--apply']), patch.object(alta.os, 'geteuid', return_value=0), patch.object(alta.socket, 'gethostname', return_value='DESKTOP-ENV6SDA'), patch.object(alta, 'run') as run:
            with self.assertRaisesRegex(RuntimeError, 'no aplicar en VPS ni laptop'):
                alta.main()
            run.assert_not_called()

    def test_non_root_refused_before_mutation(self):
        with patch('sys.argv', [str(SOURCE), '--apply']), patch.object(alta.os, 'geteuid', return_value=1000), patch.object(alta, 'run') as run:
            with self.assertRaises(RuntimeError): alta.main()
            run.assert_not_called()

    def test_existing_file_or_link_preserved(self):
        folder = Path(tempfile.mkdtemp(prefix='onia-bootstrap-preservacion-'))
        path = folder/'original'; path.write_text('conservar')
        with self.assertRaises(FileExistsError): alta.write_new(path, 'cambio')
        link = folder/'enlace'; link.symlink_to(path)
        with self.assertRaises(FileExistsError): alta.write_new(link, 'cambio')
        self.assertEqual(path.read_text(), 'conservar')

    def test_wrapper_isolated_from_python_startup(self):
        self.assertTrue(alta.WRAPPER.startswith('#!/usr/bin/python3 -I\n'))
        compile(alta.WRAPPER, 'onia-worker-shell', 'exec')
        compile(alta.CHECK, 'check-isolation', 'exec')

    def test_mount_policy_rejects_nested_and_windows_filesystems(self):
        ns={'__name__':'import_only'};exec(compile(alta.WRAPPER,'wrapper','exec'),ns)
        root='1 0 8:1 / / rw - ext4 /dev/fake rw\n'
        with self.assertRaisesRegex(RuntimeError,'submontaje'):
            ns['mounts_safe'](['/usr'],root+'2 1 8:2 / /usr/share/personal rw - ext4 /dev/other rw\n')
        with self.assertRaisesRegex(RuntimeError,'filesystem'):
            ns['mounts_safe'](['/usr'], '1 0 9:1 / / rw - 9p drvfs rw\n')
        with self.assertRaisesRegex(RuntimeError,'montaje'):
            ns['mounts_safe'](['/usr'],root+'2 1 8:1 /personal /usr rw - ext4 /dev/fake rw\n')
        with self.assertRaisesRegex(RuntimeError,'montaje separado'):
            ns['mounts_safe'](['/usr/share'],root+'2 1 8:1 /personal /usr rw - ext4 /dev/fake rw\n')
        folder=Path(tempfile.mkdtemp(prefix='onia-mount-link-'))
        link=folder/'enlace';link.symlink_to('/usr')
        with self.assertRaisesRegex(RuntimeError,'fuente enlazada'):
            ns['mounts_safe']([str(link)],root)

    def test_files_created_without_writable_window_even_permissive_umask(self):
        folder=Path(tempfile.mkdtemp(prefix='onia-bootstrap-modo-'))
        before=os.umask(0)
        try: alta.write_new(folder/'control','publico',0o644)
        finally: os.umask(before)
        self.assertEqual((folder/'control').stat().st_mode & 0o777,0o644)

    def test_separate_sshd_config_parses_and_enforces_policy(self):
        folder=Path(tempfile.mkdtemp(prefix='onia-bootstrap-sshd-'))
        key=folder/'hostkey-sintetica'
        subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(key)],check=True,capture_output=True)
        config=folder/'sshd_config'
        config.write_text(alta.SSH_CONFIG.replace('/etc/ssh/ssh_host_ed25519_key',str(key)))
        with patch.object(alta,'SSH_RULE',config): alta.check_effective()

    def test_real_bubblewrap_isolation_and_persistence(self):
        if os.environ.get('ONIA_TEST_BWRAP') != '1':
            self.skipTest('Integration requires explicit host execution ONIA_TEST_BWRAP=1')
        folder = Path(tempfile.mkdtemp(prefix='onia-bootstrap-integracion-'))
        work=folder/'work'; work.mkdir(); config=folder/'etc'; config.mkdir()
        uid=os.getuid(); gid=os.getgid()
        (config/'passwd').write_text(f'onia-worker:x:{uid}:{gid}:worker:/home/onia-worker:/bin/bash\n')
        (config/'group').write_text(f'onia-worker:x:{gid}:\n')
        (config/'nsswitch.conf').write_text('passwd: files\ngroup: files\nhosts: files\n')
        ns={'__name__':'import_only'};exec(compile(alta.WRAPPER,'wrapper','exec'),ns)
        text='python3 - '+shlex.join([str(uid),os.readlink('/proc/self/ns/net'),os.readlink('/proc/self/ns/pid')])
        cmd=ns['command'](work,config,text);fd=int(cmd[cmd.index('--seccomp')+1])
        try: result=subprocess.run(cmd,pass_fds=(fd,),input=alta.CHECK,text=True,capture_output=True,timeout=15)
        finally: os.close(fd)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout);self.assertTrue(data['ok'])
        saved=work/data['persistencia']/'persistencia.txt'
        self.assertEqual(saved.read_text(),'aislamiento sintético\n')
        # A second process sees useful work without sharing host filesystem.
        cmd=ns['command'](work,config,'cat '+shlex.quote('/home/onia-worker/'+data['persistencia']+'/persistencia.txt'));fd=int(cmd[cmd.index('--seccomp')+1])
        try: again=subprocess.run(cmd,pass_fds=(fd,),text=True,capture_output=True,timeout=15)
        finally: os.close(fd)
        self.assertEqual(again.returncode,0,again.stderr)
        self.assertEqual(again.stdout,'aislamiento sintético\n')


class PERecovery(unittest.TestCase):
    def test_control_preserves_failure_kind_and_never_exposes_raw_output(self):
        cases = [
            (OSError(errno.ENOEXEC, 'private filename'), {'exception': 'OSError', 'errno': errno.ENOEXEC}),
            (PermissionError(errno.EACCES, 'private path'), {'exception': 'PermissionError', 'errno': errno.EACCES}),
            (subprocess.TimeoutExpired('private command', 5, stderr=b'secret'), {'exception': 'TimeoutExpired', 'timeout_s': 5}),
            (subprocess.CompletedProcess([], 193, b'private', b'\xffsecret CreateProcess'), {'returncode': 193}),
            (subprocess.CompletedProcess([], 0, b'', b''), {'returncode': 0}),
        ]
        with patch.object(alta, 'checked_pe', return_value=Path('/verified/canary')):
            for outcome, expected in cases:
                with self.subTest(expected=expected), patch.object(alta.subprocess, 'run') as run:
                    if isinstance(outcome, BaseException): run.side_effect = outcome
                    else: run.return_value = outcome
                    data = alta.pe_probe()
                    for key, value in expected.items(): self.assertEqual(data[key], value)
                    self.assertEqual(data['ok'], expected.get('returncode') == 0)
                    self.assertNotIn('secret', json.dumps(data))
                    self.assertNotIn('private', json.dumps(data))
                    self.assertEqual(run.call_args.kwargs['timeout'], 5)
                    self.assertEqual(run.call_args.kwargs['stdin'], subprocess.DEVNULL)

    def test_unverified_pe_never_executes(self):
        with patch.object(alta, 'checked_pe', side_effect=RuntimeError('bad hash')), \
             patch.object(alta.subprocess, 'run') as run:
            with self.assertRaises(RuntimeError): alta.pe_probe()
            run.assert_not_called()

    def test_diagnostic_is_separate_from_apply(self):
        with patch('sys.argv', [str(SOURCE), '--diagnose-pe']), \
             patch.object(alta.os, 'geteuid', return_value=0), \
             patch.object(alta.socket, 'gethostname', return_value=alta.MACHINE), \
             patch.object(Path, 'read_text', return_value='microsoft-wsl'), \
             patch.object(alta, 'diagnose_pe', return_value={'ok': True}) as diagnose, \
             patch.object(alta, 'run') as run, patch.object(alta, 'write_new') as write, \
             patch('builtins.print'):
            alta.main()
            diagnose.assert_called_once_with()
            run.assert_not_called()
            write.assert_not_called()

    def test_resume_flag_requires_explicit_apply_and_original_backup(self):
        for args in (['--resume-pe-control'], ['--apply', '--resume-pe-control'],
                     ['--diagnose-pe', '--apply'], ['--diagnose-pe', '--resume-backup', '/root/x']):
            with self.subTest(args=args), patch('sys.argv', [str(SOURCE)] + args), \
                 patch.object(alta, 'run') as run, patch('sys.stderr'):
                with self.assertRaises(SystemExit): alta.main()
                run.assert_not_called()

    def test_diagnostic_filters_configs_environment_and_exception_text(self):
        original = Path.read_text
        def read(path, *args, **kwargs):
            if path.name == 'status': return 'enabled\n'
            if path.name == 'WSLInterop': return 'enabled\ninterpreter /init\nprivate-data\n'
            return original(path, *args, **kwargs)
        import io
        with patch.object(Path, 'read_text', read), \
             patch('builtins.open', return_value=io.StringIO('[interop]\nenabled=true\nsecret=do-not-output\n')), \
             patch.dict(os.environ, {'WSL_INTEROP': '/private/do-not-output'}), \
             patch.object(alta, 'pe_probe', side_effect=RuntimeError('do-not-output')):
            data = alta.diagnose_pe()
        text = json.dumps(data)
        self.assertNotIn('do-not-output', text)
        self.assertNotIn('private-data', text)
        self.assertTrue(data['WSLInterop']['interpreter_init'])
        self.assertEqual(data['wsl_conf']['interop.enabled'], 'true')
        self.assertTrue(data['control_pe']['no_ejecutado'])

    def test_partial_resume_preserves_exact_tree_and_rejects_changes(self):
        root = Path(tempfile.mkdtemp(prefix='onia-pe-retoma-'))/'worker'
        root.mkdir(mode=0o755)
        for name in ('login', 'etc', 'work'): (root/name).mkdir(mode=0o700 if name == 'work' else 0o755)
        alta.write_new(root/'host-only', alta.HOST_CANARY)
        alta.write_new(root/'interop-canary.exe', alta.pe_canary(), 0o755)
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        original_lstat = Path.lstat
        ownership = {}
        def metadata(path, *args, **kwargs):
            st = original_lstat(path, *args, **kwargs)
            uid, gid = ownership.get(str(path), (1001, 1001) if path == root/'work' else (0, 0))
            mode = (stat.S_IFDIR | 0o755) if path in root.parents else st.st_mode
            return SimpleNamespace(st_mode=mode, st_uid=uid, st_gid=gid, st_nlink=st.st_nlink)
        with patch.object(alta, 'ROOT', root), patch.object(Path, 'lstat', metadata), \
             patch.object(Path, 'read_text', return_value='1 0 8:1 / / rw - ext4 /dev/fake rw\n'):
            before = {p.relative_to(root): (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob('*') if p.is_file()}
            alta.prepare_pe_partial(account, True)
            self.assertEqual(before, {p.relative_to(root): (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob('*') if p.is_file()})
            ownership[str(root)] = (1001, 0)
            with self.assertRaises(RuntimeError): alta.validate_pe_partial(account)
            ownership.clear()
            (root/'work').chmod(0o755)
            with self.assertRaises(RuntimeError): alta.validate_pe_partial(account)
            (root/'work').chmod(0o700)
            pe = root/'interop-canary.exe'
            pe.write_bytes(b'changed')
            with self.assertRaises(RuntimeError): alta.validate_pe_partial(account)
            pe.write_bytes(alta.pe_canary())
            os.link(pe, root.parent/'hardlink')
            with self.assertRaises(RuntimeError): alta.validate_pe_partial(account)
            # Leave all failed fixtures intact; no cleanup of real or synthetic evidence.

    def test_partial_resume_rejects_symlink_nonempty_and_extra_paths(self):
        for mutation in ('symlink', 'nonempty', 'extra'):
            root = Path(tempfile.mkdtemp(prefix='onia-pe-negative-'))/'worker'
            root.mkdir()
            for name in ('login', 'etc', 'work'):
                if name == 'work' and mutation == 'symlink': (root/name).symlink_to('/tmp')
                else: (root/name).mkdir()
            alta.write_new(root/'host-only', alta.HOST_CANARY)
            alta.write_new(root/'interop-canary.exe', alta.pe_canary(), 0o755)
            if mutation == 'nonempty': (root/'etc'/'unexpected').write_text('conservar')
            if mutation == 'extra': (root/'extra').write_text('conservar')
            # Metadata mocked only here: directory enumeration still rejects all extras,
            # and a real symlink rejection is separately checked below.
            def check(path, *args, **kwargs):
                if path.is_symlink(): raise RuntimeError('symlink')
            with self.subTest(mutation=mutation), patch.object(alta, 'ROOT', root), \
                 patch.object(alta, 'checked_metadata', side_effect=check), \
                 patch.object(Path, 'read_text', return_value='1 0 8:1 / / rw - ext4 /dev/fake rw\n'):
                with self.assertRaises(RuntimeError):
                    alta.validate_pe_partial(SimpleNamespace(pw_uid=1001, pw_gid=1001))

    def test_metadata_rejects_real_symlink_before_following_it(self):
        root = Path(tempfile.mkdtemp(prefix='onia-pe-link-'))
        (root/'link').symlink_to('/usr/bin/python3')
        with self.assertRaises(RuntimeError): alta.checked_metadata(root/'link', 0o755)

    def test_partial_resume_rejects_nested_mount(self):
        root = Path(tempfile.mkdtemp(prefix='onia-pe-mount-'))/'worker'
        root.mkdir()
        mountinfo = '1 0 8:1 / / rw - ext4 /dev/fake rw\n'
        mountinfo += f'2 1 8:2 / {root}/work rw - ext4 /dev/other rw\n'
        with patch.object(alta, 'ROOT', root), patch.object(alta, 'checked_metadata'), \
             patch.object(Path, 'read_text', return_value=mountinfo):
            with self.assertRaisesRegex(RuntimeError, 'submontaje'):
                alta.validate_pe_partial(SimpleNamespace(pw_uid=1001, pw_gid=1001))

    def test_pe_bytes_unchanged_from_v2(self):
        self.assertEqual(hashlib.sha256(alta.pe_canary()).hexdigest(),
                         '98ee1b89c5961a32ea860444715c306f8302cb380797ebab44f4f879e13e6055')


class MountRecovery(unittest.TestCase):
    root_mount = '1 0 8:1 / / rw - ext4 fake rw\n'
    modules = '/usr/lib/modules/6.18.33.2-microsoft-standard-WSL2'
    fixtures = SOURCE.parent/'fixtures'

    def wrapper_scope(self, old=False):
        ns = {'__name__': 'fixture'}
        exec((self.fixtures/'v3-wrapper.py.txt').read_text() if old else alta.WRAPPER, ns)
        return ns

    @contextmanager
    def module_paths(self, symlink=False, writable=False, uid=0):
        original = Path.lstat
        resolve = Path.resolve
        def info(path, *args, **kwargs):
            if str(path) in ('/usr/lib/modules', self.modules):
                return SimpleNamespace(st_mode=(stat.S_IFLNK if symlink else stat.S_IFDIR) |
                                       (0o777 if writable else 0o755), st_uid=uid, st_gid=0)
            return original(path, *args, **kwargs)
        def canonical(path, *args, **kwargs):
            if str(path) in ('/usr/lib/modules', self.modules):
                return Path('/other') if symlink else path
            return resolve(path, *args, **kwargs)
        exists = Path.exists
        def present(path):
            return True if str(path) in ('/usr/lib/modules', self.modules) else exists(path)
        with patch.object(Path, 'lstat', info), patch.object(Path, 'resolve', canonical), patch.object(Path, 'exists', present):
            yield

    def test_observed_mount_reproduces_v3_and_v4_masks_it_after_bind(self):
        mounts = self.root_mount + f'2 1 0:2 / {self.modules} ro - overlay overlay ro\n'
        with self.module_paths():
            with self.assertRaisesRegex(RuntimeError, 'submontaje'):
                self.wrapper_scope(old=True)['mounts_safe'](['/usr/lib'], mounts)
            ns = self.wrapper_scope()
            ns['mounts_safe'](['/usr/lib'], mounts)
            ns['filter_fd'] = lambda: 42
            with patch.object(Path, 'read_text', return_value=mounts):
                cmd = ns['command'](Path('/var/lib/onia-worker/work'), Path('/var/lib/onia-worker/etc'), 'id -u')
            mask = cmd.index('/usr/lib/modules')
            self.assertEqual(cmd[mask-1:mask+3], ['--tmpfs', '/usr/lib/modules', '--remount-ro', '/usr/lib/modules'])
            self.assertGreater(mask, cmd.index('--ro-bind'))

    def test_modules_reject_other_type_version_descendant_duplicate_or_noncanonical(self):
        valid = f'2 1 0:2 / {self.modules} ro - overlay overlay ro\n'
        invalid = [valid.replace('overlay overlay', 'ext4 fake'),
                   valid.replace('6.18.33.2', '6.18.33.3'),
                   valid.replace(self.modules, '/usr/lib/modules'),
                   valid.replace(self.modules, self.modules+'/child'), valid+valid,
                   valid+f'3 2 0:3 / {self.modules}/child ro - tmpfs tmpfs ro\n',
                   valid.replace('/usr/lib/modules/', '/usr/lib/../lib/modules/'),
                   valid.replace('/usr/lib/modules/', '/usr//lib/modules/'),
                   valid+'3 1 8:2 / /usr/share/private rw - ext4 fake rw\n']
        with self.module_paths():
            for mounts in invalid:
                with self.subTest(mounts=mounts), self.assertRaises(RuntimeError):
                    self.wrapper_scope()['mounts_safe'](['/usr/lib', '/usr/share'], self.root_mount+mounts)

    def test_modules_reject_symlink_unsafe_owner_or_permissions(self):
        mounts = self.root_mount + f'2 1 0:2 / {self.modules} ro - overlay overlay ro\n'
        for change in ({'symlink': True}, {'writable': True}, {'uid': 1001}):
            with self.subTest(change=change), self.module_paths(**change), self.assertRaises(RuntimeError):
                self.wrapper_scope()['mounts_safe'](['/usr/lib'], mounts)

    @contextmanager
    def partial(self):
        folder = Path(tempfile.mkdtemp(prefix='onia-mount-v4-'))
        root = folder/'worker'; root.mkdir(mode=0o755)
        for name in ('login', 'work', 'etc'): (root/name).mkdir(mode=0o700 if name == 'work' else 0o755)
        keydir = folder/'ssh'; keydir.mkdir(mode=0o755)
        shell = folder/'libexec'/'onia-worker-shell'; shell.parent.mkdir(mode=0o755)
        runtime = shell.with_name('onia-worker-runtime')
        contents = {'passwd': b'fixture-passwd\n', 'group': b'fixture-group\n',
                    'nsswitch.conf': b'passwd: files\n', 'ld.so.cache': b'host-cache', 'localtime': b'host-timezone'}
        for name, content in contents.items(): alta.write_new(root/'etc'/name, content)
        alta.write_new(shell, (self.fixtures/'v3-wrapper.py.txt').read_bytes(), 0o755)
        alta.write_new(runtime, alta.RUNTIME_SCRIPT, 0o755)
        alta.write_new(keydir/'sshd_config', alta.SSH_CONFIG, 0o600)
        alta.write_new(root/'check-isolation.py', (self.fixtures/'v3-check.py.txt').read_bytes())
        alta.write_new(root/'host-only', alta.HOST_CANARY)
        alta.write_new(root/'interop-canary.exe', alta.pe_canary(), 0o755)
        backup = folder/'backup'; backup.mkdir(mode=0o700)
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        original = Path.lstat
        read = Path.read_text
        def info(path, *args, **kwargs):
            st = original(path, *args, **kwargs)
            if path == folder or folder in path.parents or path in folder.parents:
                uid = 1001 if path == root/'work' else 0
                mode = (stat.S_IFDIR | 0o755) if path in folder.parents else st.st_mode
                return SimpleNamespace(st_mode=mode, st_uid=uid, st_gid=uid, st_nlink=st.st_nlink)
            return st
        def text(path, *args, **kwargs):
            return self.root_mount if str(path) == '/proc/self/mountinfo' else read(path, *args, **kwargs)
        with ExitStack() as stack:
            for name, value in {'ROOT': root, 'SHELL': shell, 'RUNTIME': runtime,
                                'KEY_DIR': keydir, 'SSH_RULE': keydir/'sshd_config', 'UNIT': folder/'unit'}.items():
                stack.enter_context(patch.object(alta, name, value))
            stack.enter_context(patch.object(Path, 'lstat', info))
            stack.enter_context(patch.object(Path, 'read_text', text))
            stack.enter_context(patch.object(alta, 'config_contents', return_value=contents))
            yield account, folder, backup

    def snapshot(self, folder):
        return {str(p.relative_to(folder)): (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns)
                for p in folder.rglob('*') if p.is_file() and not p.is_symlink()}

    def test_v3_exact_bytes_fixture_and_safe_resume_back_up_every_original(self):
        for filename, digest in [('v3-wrapper.py.txt', alta.V3_WRAPPER_SHA256), ('v3-check.py.txt', alta.V3_CHECK_SHA256)]:
            self.assertEqual(hashlib.sha256((self.fixtures/filename).read_bytes()).hexdigest(), digest)
        with self.partial() as (account, folder, backup):
            before = self.snapshot(folder)
            with patch.object(alta, 'isolation_probe', return_value={'ok': True}) as probe:
                alta.resume_mount_partial(account, backup)
            probe.assert_called_once_with(account, candidate=True, preflight=True)
            self.assertEqual(alta.SHELL.read_text(), alta.WRAPPER)
            self.assertEqual((alta.ROOT/'check-isolation-v4.py').read_text(), alta.CHECK)
            manifest = json.loads((backup/'estado-v3/manifest.json').read_text())
            self.assertEqual(len(manifest), 11)
            for entry in manifest:
                saved = backup/'estado-v3'/entry['copia']
                original = before[str(Path(entry['ruta']).relative_to(folder))]
                self.assertEqual(saved.read_bytes(), original[0])
                self.assertEqual(saved.stat().st_mtime_ns, original[2])
            # Todos los originales salvo wrapper permanecen en su sitio, con metadatos.
            after = self.snapshot(folder)
            for path, value in before.items():
                if path != str(alta.SHELL.relative_to(folder)): self.assertEqual(after[path], value)
            self.assertFalse(alta.UNIT.exists())
            self.assertFalse((alta.KEY_DIR/'authorized_keys').exists())
            with self.assertRaises(RuntimeError): alta.resume_mount_partial(account, backup)

    def test_failed_candidate_or_backup_does_not_replace_or_publish(self):
        for failure in ('probe', 'copy'):
            with self.subTest(failure=failure), self.partial() as (account, folder, backup):
                before = self.snapshot(folder)
                with patch.object(alta, 'isolation_probe', side_effect=RuntimeError('fixture failure') if failure == 'probe' else None), \
                     patch.object(alta.shutil, 'copy2', side_effect=OSError('copy failure') if failure == 'copy' else None):
                    with self.assertRaises((RuntimeError, OSError)): alta.resume_mount_partial(account, backup)
                after = self.snapshot(folder)
                for path, value in before.items(): self.assertEqual(after[path], value)
                self.assertFalse((alta.ROOT/'retoma-v4.json').exists())
                self.assertFalse(alta.UNIT.exists())
                self.assertFalse((alta.KEY_DIR/'authorized_keys').exists())

    def test_reject_modified_partial_content_permissions_links_publication_and_data(self):
        mutations = ('shell', 'runtime', 'check', 'ssh', 'cache', 'timezone', 'extra', 'work', 'login',
                     'symlink', 'hardlink', 'mode', 'key', 'unit', 'receipt')
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.partial() as (account, folder, backup):
                if mutation == 'shell': alta.SHELL.write_text('# altered\n')
                elif mutation == 'runtime': alta.RUNTIME.write_text('# altered\n')
                elif mutation == 'check': (alta.ROOT/'check-isolation.py').write_text('altered')
                elif mutation == 'ssh': alta.SSH_RULE.write_text('altered')
                elif mutation == 'cache': (alta.ROOT/'etc/ld.so.cache').write_bytes(b'different')
                elif mutation == 'timezone': (alta.ROOT/'etc/localtime').write_bytes(b'different')
                elif mutation == 'extra': (alta.ROOT/'extra').write_text('preserve')
                elif mutation in ('work', 'login'): (alta.ROOT/mutation/'data').write_text('preserve')
                elif mutation == 'symlink':
                    os.rename(alta.SHELL, folder/'original-shell')
                    alta.SHELL.symlink_to(folder/'original-shell')
                elif mutation == 'hardlink': os.link(alta.SHELL, folder/'shell-alias')
                elif mutation == 'mode': alta.RUNTIME.chmod(0o777)
                elif mutation == 'key': (alta.KEY_DIR/'authorized_keys.pending').write_text('preserve')
                elif mutation == 'unit': alta.UNIT.symlink_to(folder/'missing-unit')
                elif mutation == 'receipt': (alta.ROOT/'alta-local-v1.json').write_text('{}')
                before = self.snapshot(folder)
                with patch.object(alta, 'isolation_probe') as probe:
                    with self.assertRaises(RuntimeError): alta.resume_mount_partial(account, backup)
                    probe.assert_not_called()
                self.assertEqual(self.snapshot(folder), before)

    def test_v4_flag_requires_apply_backup_and_excludes_other_resume(self):
        for args in (['--resume-mount-control'], ['--apply', '--resume-mount-control'],
                     ['--diagnose-pe', '--resume-mount-control'],
                     ['--apply', '--resume-pe-control', '--resume-mount-control', '--resume-backup', '/root/x']):
            with self.subTest(args=args), patch('sys.argv', [str(SOURCE)]+args), patch('sys.stderr'):
                with self.assertRaises(SystemExit): alta.main()

    def test_check_failure_diagnostic_never_prints_arbitrary_child_output(self):
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        for outcome in (subprocess.CompletedProcess([], 1, b'secret-stdout', b'\xffsecret-stderr bwrap: namespace'),
                        subprocess.CompletedProcess([], 0, b'secret-stdout', b'private'),
                        subprocess.TimeoutExpired('private command', 20)):
            with self.subTest(outcome=type(outcome).__name__), patch.object(alta.subprocess, 'run') as run:
                if isinstance(outcome, BaseException): run.side_effect = outcome
                else: run.return_value = outcome
                with self.assertRaises(RuntimeError) as caught: alta.isolation_probe(account, candidate=True, preflight=True)
                self.assertNotIn('secret', str(caught.exception))
                self.assertNotIn('private', str(caught.exception))
                self.assertEqual(run.call_args.kwargs['timeout'], 20)

    def test_check_success_requires_all_flags_and_only_known_output(self):
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        data = dict.fromkeys(('ok', 'uid_no_root', 'sin_capacidades', 'no_new_privs',
                             'pid_y_red_aislados', 'windows_y_host_no_expuestos', 'etc_solo_lectura',
                             'sudo_rechazado', 'modulos_ocultos_solo_lectura'), True)
        data.update(persistencia=None, limite='Prueba local del aislamiento; no acredita SSH remoto, ASR ni WSL persistente.')
        with patch.object(alta.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(data).encode(), b'')) as run:
            self.assertEqual(alta.isolation_probe(account, candidate=True, preflight=True), data)
            self.assertIn(alta.WRAPPER, run.call_args.args[0])
            self.assertIn('--preflight', run.call_args.args[0][-1])
        for changed in (data | {'sudo_rechazado': False}, data | {'secret': 'never-print'},
                        data | {'persistencia': 'never-print'}, data | {'limite': 'never-print'}):
            with self.subTest(keys=set(changed)), patch.object(alta.subprocess, 'run',
                    return_value=subprocess.CompletedProcess([], 0, json.dumps(changed).encode(), b'')):
                with self.assertRaises(RuntimeError) as caught: alta.isolation_probe(account, preflight=True)
                self.assertNotIn('never-print', str(caught.exception))

    def test_v4_nested_mount_or_changed_parent_is_refused_before_probe(self):
        for mutation in ('mount', 'parent'):
            with self.subTest(mutation=mutation), self.partial() as (account, folder, backup):
                before = self.snapshot(folder)
                with ExitStack() as stack:
                    if mutation == 'parent': alta.SHELL.parent.chmod(0o777)
                    else:
                        read = Path.read_text
                        def text(path, *args, **kwargs):
                            return (self.root_mount + f'2 1 8:2 / {alta.ROOT}/work rw - ext4 fake rw\n') if str(path) == '/proc/self/mountinfo' else read(path, *args, **kwargs)
                        stack.enter_context(patch.object(Path, 'read_text', text))
                    probe = stack.enter_context(patch.object(alta, 'isolation_probe'))
                    with self.assertRaises(RuntimeError): alta.resume_mount_partial(account, backup)
                    probe.assert_not_called()
                self.assertEqual(self.snapshot(folder), before)

    def test_host_copied_config_validates_sources_and_preserves_their_bytes(self):
        source_data = {'/etc/ld.so.cache': b'cache-from-host', '/usr/share/zoneinfo/Etc/UTC': b'time-from-host'}
        exists = Path.exists; resolve = Path.resolve; read = Path.read_bytes
        def present(path): return True if str(path) in ('/etc/ld.so.cache', '/etc/localtime') else exists(path)
        def canonical(path, *args, **kwargs):
            if str(path) == '/etc/localtime': return Path('/usr/share/zoneinfo/Etc/UTC')
            if str(path) == '/etc/ld.so.cache': return path
            return resolve(path, *args, **kwargs)
        def contents(path): return source_data[str(path)] if str(path) in source_data else read(path)
        account = SimpleNamespace(pw_uid=1001, pw_gid=1001)
        with patch.object(Path, 'exists', present), patch.object(Path, 'resolve', canonical), \
             patch.object(Path, 'read_bytes', contents), patch.object(alta, 'checked_metadata') as metadata:
            result = alta.config_contents(account)
            self.assertEqual(result['ld.so.cache'], b'cache-from-host')
            self.assertEqual(result['localtime'], b'time-from-host')
            self.assertEqual(result['passwd'], b'onia-worker:x:1001:1001:worker:/home/onia-worker:/bin/bash\n')
            metadata.assert_any_call(Path('/usr/share/zoneinfo/Etc/UTC'), 0o644)
            with patch.object(Path, 'resolve', return_value=Path('/private/unapproved')), self.assertRaises(RuntimeError):
                alta.config_contents(account)
            with patch.object(alta, 'checked_metadata', side_effect=RuntimeError('bad metadata')), self.assertRaises(RuntimeError):
                alta.config_contents(account)


if __name__ == '__main__':
    unittest.main()
