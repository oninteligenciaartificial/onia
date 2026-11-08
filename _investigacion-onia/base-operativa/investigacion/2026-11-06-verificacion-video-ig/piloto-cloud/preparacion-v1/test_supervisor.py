import dataclasses
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
import supervisor as s


class SupervisorTests(unittest.TestCase):
    def test_01_validation_before_launch(self):
        for p in (dataclasses.replace(s.Policy(), wall_seconds=float('nan')),
                  dataclasses.replace(s.Policy(), as_bytes=13*s.GIB),
                  dataclasses.replace(s.Policy(), reserve_bytes=1),
                  dataclasses.replace(s.Policy(), threads=3)):
            with self.assertRaises(ValueError):
                s.run([sys.executable, '-c', 'raise Exception("must not run")'], 'invalid', p)
        self.assertFalse((s.ROOT/'run-invalid').exists())

    def test_02_limits_effective_and_parent_unchanged(self):
        r=s.run([sys.executable,'-c','print("synthetic-no-model")'], 'effective')
        self.assertEqual(r['reason'], 'exited')
        self.assertEqual(r['effective']['rlimit_as'], [12*s.GIB]*2)
        self.assertEqual(r['effective']['rlimit_cpu'], [600]*2)
        self.assertEqual(len(r['effective']['affinity']), 2)
        self.assertEqual(r['effective']['pgid'], r['pgid'])
        self.assertTrue(r['parent_limits_unchanged'])

    def test_03_small_as_allocation_is_refused(self):
        code='import sys\ntry:\n x=bytearray(256*1024**2)\nexcept MemoryError:\n print("EXPECTED_MEMORY_ERROR",flush=True);sys.exit(23)\nraise RuntimeError("allocation unexpectedly passed")'
        r=s.run([sys.executable,'-c',code], 'allocation', dataclasses.replace(s.Policy(),as_bytes=96*1024**2))
        self.assertEqual(r['exit_code'],23)
        self.assertEqual(r['reason'],'child_failure')
        self.assertIn('EXPECTED_MEMORY_ERROR',(s.ROOT/'run-allocation/output.log').read_text())
        self.assertTrue(r['parent_limits_unchanged'])

    def test_04_timeout_group_and_external_witness(self):
        witness=subprocess.Popen([sys.executable,'-c','import time;time.sleep(15)'],start_new_session=True)
        try:
            code='import subprocess,sys,time\np=subprocess.Popen([sys.executable,"-c","import time;time.sleep(15)"])\nprint("DESCENDANT",p.pid,flush=True)\ntime.sleep(15)'
            r=s.run([sys.executable,'-c',code], 'timeout', dataclasses.replace(s.Policy(),wall_seconds=0.8))
            self.assertEqual(r['reason'],'wall_timeout')
            self.assertEqual(r['exit_code'],-9)
            self.assertGreaterEqual(len(r['killed_members']),2)
            self.assertIsNone(witness.poll())
            self.assertNotEqual(os.getpgid(witness.pid),r['pgid'])
            self.assertTrue(r['parent_limits_unchanged'])
            (s.ROOT/'witness.json').write_text(json.dumps({'pid':witness.pid,'pgid':os.getpgid(witness.pid),'alive_after_supervised_group_kill':True,'cleanup':'terminate only this witness process created by test'})+'\n')
            # Zombies awaiting init reaping have no running work/RSS.
            self.assertFalse([m for m in s.group_sample(r['pgid']) if m['state']!='Z'])
        finally:
            witness.terminate();witness.wait(timeout=5)

    def test_05_cpu_limit(self):
        r=s.run([sys.executable,'-c','while True: pass'], 'cpu',dataclasses.replace(s.Policy(),cpu_seconds=1,wall_seconds=5))
        self.assertEqual(r['exit_code'],-9)
        self.assertEqual(r['effective']['rlimit_cpu'],[1,1])
        self.assertNotEqual(r['reason'],'wall_timeout')

    def test_06_output_bound(self):
        r=s.run([sys.executable,'-c','import os\nwhile True: os.write(1,b"x"*65536)'], 'output')
        self.assertEqual(r['reason'],'output_limit')
        self.assertLessEqual((s.ROOT/'run-output/output.log').stat().st_size,256*1024)
        self.assertTrue(r['log_truncated'])

    def test_07_guard_boundaries(self):
        p=s.Policy(); snap={'reserve':p.reserve_bytes,'disk_free':p.disk_free_bytes,'tree_bytes':p.tree_bytes}
        self.assertIsNone(s.guard(snap,p))
        for key,value,reason in [('reserve',p.reserve_bytes-1,'memory_reserve'),('disk_free',p.disk_free_bytes-1,'disk_reserve'),('tree_bytes',p.tree_bytes+1,'tree_limit')]:
            self.assertEqual(s.guard(dict(snap,**{key:value}),p),reason)


if __name__=='__main__':
    unittest.main(verbosity=2)
