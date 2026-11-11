import importlib.util
import json
import hashlib
import errno
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


if __name__ == '__main__':
    unittest.main()
