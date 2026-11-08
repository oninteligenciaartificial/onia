# PANNs v2: narrow guard correction passed; next resolver failure stopped

Exact executed command (one attempt):
```
python3 -B /workspace/onia-av-pilot-20261106/panns-setup-v2/launch_setup.py > /workspace/onia-av-pilot-20261106/panns-setup-v2/preparation-launch.log 2>&1
```
v1 failed cut and preflight were verified byte-exact; all old cuts stay intact.
An earlier tool request used a not-yet-created working directory and was rejected
before starting any process. It made no network request or installation action.

setup.patch changes ONLY provenance/hostname/redirect recording and the exact
authorized PyTorch CDN exception, plus aggregate v1 budget deductions. supervisor
and launch changes only relocate outputs and apply the remaining budget. Pins,
resolver selection, METADATA/install/checkpoint logic and inference criteria were
not changed in response to results. No inference occurred before or during v2.

Index HTTPS https://download.pytorch.org/whl/cpu/torch/ returned431099B, SHA256
c4c3b436926032f111d5ccc8faf2f9e69f2305285b493d29fdbea955681d5f2c.
Its exact selected cp312 LinuxCPU torch2.5.1 link used download-r2.pytorch.org.
Only that exact published wheel URL is allowed on this additional hostname;
HTTPS/TLS unchanged. Every request, redirect-before-follow and final response host
is checked and recorded. No arbitrary hostname/path exception or bypass.
Torch wheel174642530B matched index SHA
4856f9d6925121d13c2df07aa7580b767f449dfe71ae5acde9c27535d5da4840.
PANNs0.1.1 wheel matched supplied SHA97f6b56b6c9467cf00e21f041e1f88933188c65c1b5ca64eeb3c92e37fb27fc2.
LICENSE.MIT matched supplied SHA and remains literal, including anomalous
Copyright (c) 2010-2017 Google, Inc. http://angularjs.org. Not corrected/researched.

NEXT FAILURE: while enumerating official PyPI SymPy versions, unchanged own
resolver called Version(v) on historical release0.5.13-hg and raised InvalidVersion.
Required SymPy from torch METADATA was==1.13.1 on Python>=3.9. Last guard-trace
path hash matches /pypi/sympy/json (HTTP200); stage label still names the previously
finished setuptools wheel. This is a resolver implementation failure, NOT network
denial, a wheel incompatibility claim, a resource limit or PANNs semantic rejection.
No additional fix, selection, network retry or automatic continuation performed.

Eleven verified wheels retained; no venv/installation/checkpoint/framework import,
32k derivatives or screening. Scores absent; paired diagnostic/acoustic acceptance
pending. No0.5 threshold or silence-pass claim. No corpus/Praat/MiniCPM execution.

Aggregate v1+v2 wall10.837333277999278s of300; downloaded203178853B of1610612736,
including metadata. v2 started with431099B already consumed and wall299.317910743s
remaining. Global clock not reset; child CPUhard299s, AS3GiB, one common affinity
CPU, workers1/batch1; reserve>=6GiB monitored, no swap added. Reserve after31.39GB.
Child exit1; parent launcher prints report and exits0, NOT a passed technical gate.
Own group cleaned completely, parent limits/handler unchanged. RSS47591424B and
CPU3.25s are sampled, not exact peak/usage. No hidden cgroup ancestor claims.

Small export includes new code/diffs, host trace, compact verified downloads,
exact license/report/result. Large raw receipt/log/index and wheels remain local
with hashes in artifact-references.json, not duplicated into text export. No
binary/model/media files exported. Each read part<=10000 characters. ONIA clean,
configuration/snapshot/publication unchanged. Workspace persistence is observed,
not guaranteed durable. STOP after this next failure; no correction chain.
