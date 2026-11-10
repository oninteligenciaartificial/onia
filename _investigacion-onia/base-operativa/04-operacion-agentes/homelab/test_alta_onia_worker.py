import importlib.util
import json
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


if __name__ == '__main__':
    unittest.main()
