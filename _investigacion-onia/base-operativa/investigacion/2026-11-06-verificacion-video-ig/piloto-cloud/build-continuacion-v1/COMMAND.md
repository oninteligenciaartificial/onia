# One explicitly authorized incremental continuation

Persistence checked before launch: marker cf57ebcd-c598-496d-8987-8848bcdfc0f4;
manifest c4211c3f120bbbeabd2c8abc57e88d08278b6ed3ccada230477a555e6e1bf088,
16/16 hashes/bytes; seven source-freeze entries and supervisor hash matched.
Previous 540-second cut preserved in review-v2/build-report.json:
reason=wall_timeout, cleanup_pending_live=[], os_thread_cap=null.

Exact launch, once:

```sh
cd /workspace/onia-av-pilot-20261106/build-continuacion-v1
python3 launch.py > invocation.log 2>&1
```

launch.py imports the unchanged, frozen review-v2/supervisor.py. New run ID:
build-continuacion-v1. wall=300 s, AS hard/soft=12 GiB PER PROCESS,
CPU hard/soft=600 s PER PROCESS, affinity=two CPUs, workers=2,
memory reserve=8 GiB, disk reserve=30 GiB, tree cap=1 GiB,
output/log limits unchanged. os_thread_cap=16 is EXPLICIT FOR THIS RUN;
it is not attributed to the previous build, whose value was null.

The driver's sole subprocess command is:

```sh
/workspace/onia-av-pilot-20261106/cmake-local/cmake/data/bin/cmake --build /workspace/onia-av-pilot-20261106/build-v2 --target llama-omni-single-test-omni -j2
```

No clean, configure, source edit, installation, weight download, model load,
AV run, target execution or publication. Frozen sources are checked before and
after the subprocess and independently after the supervisor closes. If this
attempt fails or hits a guard, report it without a third automatic execution.

report.json is the exact supervisor receipt; output.log is its exact bounded
merged stdout/stderr. result.json records final verification. RSS maxima are
sampled and group sums may double-count shared pages, not exact memory peaks.
SIGKILL of the supervisor cannot guarantee cleanup; the recorded cleanup is
the observed result of this continuation, not a promise about other runs.

All emitted files are UTF-8; concatenate numbered <=10000-character parts
without adding bytes, then verify manifest.json. This directory is not assumed
durable across turns. A completed link proves compilation only, not AV ability.
