import dataclasses
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest
import supervisor as s


class Regressions(unittest.TestCase):
    def test_sigterm_owned_group_receipt_and_external_witness(self):
        witness = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'], start_new_session=True)
        code = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import time;time.sleep(20)"]); time.sleep(20)'
        proc = subprocess.Popen([sys.executable, str(Path(s.__file__).resolve()), '--name', 'v2b-sigterm', '--', sys.executable, '-c', code],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, start_new_session=True)
        try:
            effective = s.ROOT/'run-v2b-sigterm/effective.json'
            until = time.monotonic()+5
            pgid = None
            while time.monotonic()<until:
                if effective.exists():
                    try: pgid=json.loads(effective.read_text())['pgid']
                    except json.JSONDecodeError: pass
                    if pgid and len([m for m in s.group_sample(pgid) if m['state']!='Z'])>=2: break
                time.sleep(0.02)
            self.assertIsNotNone(pgid)
            self.assertIsNone(proc.poll())
            proc.send_signal(signal.SIGTERM)
            self.assertEqual(proc.wait(timeout=5),1)
            r=json.loads((s.ROOT/'run-v2b-sigterm/report.json').read_text())
            self.assertEqual(r['reason'],'interrupted_by_sigterm')
            self.assertEqual(r['cut_receipt']['signal_number'],15)
            self.assertGreaterEqual(len(r['killed_members']),2)
            self.assertTrue(r['parent_limits_unchanged'])
            self.assertTrue(r['parent_sigterm_restored'])
            self.assertFalse(r['cleanup_pending_live'])
            self.assertIsNone(witness.poll())
            self.assertNotEqual(os.getpgid(witness.pid),pgid)
            (Path(__file__).parent/'sigterm-witness.json').write_text(json.dumps({'pid':witness.pid,'alive_after_sigterm_cleanup':True,'only_owned_group_killed':True})+'\n')
        finally:
            if proc.poll() is None: proc.send_signal(signal.SIGTERM);proc.wait(timeout=5)
            proc.stderr.close()
            witness.terminate();witness.wait(timeout=5)

    def test_leader_zero_with_live_descendant_is_not_success(self):
        before=signal.getsignal(signal.SIGTERM)
        code='import subprocess,sys;subprocess.Popen([sys.executable,"-c","import time;time.sleep(20)"]);sys.exit(0)'
        r=s.run([sys.executable,'-c',code],'v2b-earlyexit')
        self.assertEqual(r['exit_code'],0)
        self.assertEqual(r['reason'],'incomplete_group_shutdown')
        self.assertTrue(r['live_descendants_at_leader_exit'])
        self.assertFalse(r['cleanup_pending_live'])
        self.assertTrue(r['parent_limits_unchanged'])
        self.assertEqual(signal.getsignal(signal.SIGTERM),before)

    def test_clean_exit_and_handler_restoration(self):
        r=s.run([sys.executable,'-c','print("V2_NO_MODEL")'],'v2b-clean')
        self.assertEqual(r['reason'],'exited')
        self.assertTrue(r['parent_sigterm_restored'])
        self.assertTrue(r['parent_limits_unchanged'])
        self.assertEqual(r['effective']['rlimit_as'],[12*s.GIB]*2)

    def test_small_virtual_limit_regression(self):
        code='import sys\ntry: x=bytearray(256*1024**2)\nexcept MemoryError: print("EXPECTED_MEMORY_ERROR");sys.exit(23)'
        r=s.run([sys.executable,'-c',code],'v2b-as',dataclasses.replace(s.Policy(),as_bytes=96*1024**2))
        self.assertEqual(r['exit_code'],23)
        self.assertEqual(r['reason'],'child_failure')

    def test_workers_and_os_cap_are_separate_and_not_auto_raised(self):
        self.assertEqual(s.Policy().threads,2)
        self.assertIsNone(s.Policy().os_thread_cap)
        with self.assertRaises(ValueError): s.validate(dataclasses.replace(s.Policy(),os_thread_cap=0))
        code='import threading,time\nfor _ in range(3): threading.Thread(target=time.sleep,args=(10,),daemon=True).start()\ntime.sleep(10)'
        r=s.run([sys.executable,'-c',code],'v2b-threads',dataclasses.replace(s.Policy(),os_thread_cap=2))
        self.assertEqual(r['reason'],'os_thread_cap_exceeded_pending_review')
        self.assertGreater(r['sampled_max_group_os_threads'],2)


if __name__=='__main__': unittest.main(verbosity=2)
