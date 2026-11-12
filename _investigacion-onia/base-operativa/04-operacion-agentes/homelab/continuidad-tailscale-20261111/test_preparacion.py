import errno
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import preparar
import no_duplicar


class Preparacion(unittest.TestCase):
    def argv(self):
        root = Path('/home/synthetic/operacion/homelab/tailscale')
        return [str(root / 'bin/tailscaled'), '--tun=userspace-networking', '--state='+str(root/'tailscaled.state'), '--socket='+str(root/'tailscaled.sock'), '--port=0']

    def test_exact_args(self):
        a = self.argv()
        self.assertEqual(preparar.validate(a, Path('/home/synthetic')), a)
        a[1:2] = ['--tun', 'userspace-networking']
        self.assertEqual(preparar.validate(a, Path('/home/synthetic')), a)

    def test_reject_unknown_and_changed_paths(self):
        for extra in [['--auth-key=secret'], ['--state=/tmp/other'], ['--tun=tailscale0'], ['--port=99999']]:
            with self.assertRaises(ValueError):
                preparar.validate(self.argv()+extra, Path('/home/synthetic'))

    def test_socket_guard(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'test.sock'
            self.assertTrue(no_duplicar.socket_free(path))
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(str(path))
                server.listen(1)
                self.assertFalse(no_duplicar.socket_free(path))
            self.assertTrue(no_duplicar.socket_free(path))

    def test_unknown_socket_error(self):
        with patch('socket.socket.connect', side_effect=PermissionError(errno.EACCES, 'denied')):
            with self.assertRaises(PermissionError):
                no_duplicar.socket_free('/synthetic')

    def test_namespace_rejected(self):
        with patch('pathlib.Path.read_text', return_value='codex\n'):
            self.assertEqual(no_duplicar.check(), 255)
        with patch('subprocess.check_output', return_value='999999999\n'):
            with self.assertRaises(ValueError):
                preparar.capture(1)

    def test_escaping(self):
        self.assertEqual(preparar.quote('a%$"\\'), '"a%%$$\\"\\\\"')
        with self.assertRaises(ValueError):
            preparar.quote('x\ny')

    def test_unit_syntax_without_service(self):
        # Sólo parser de systemd, nunca systemctl start ni daemon sintético.
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'onia-tailscaled.service'
            p.write_text(preparar.render(['/usr/bin/true', 'a%$"\\'], Path(d)/'guard.py', Path(d)))
            result = subprocess.run(['systemd-analyze', '--user', 'verify', str(p)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('@EXEC@', p.read_text())


if __name__ == '__main__':
    unittest.main()
