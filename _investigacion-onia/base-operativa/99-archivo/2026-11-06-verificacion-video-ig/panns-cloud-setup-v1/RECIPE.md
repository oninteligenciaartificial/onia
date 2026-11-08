# PANNs setup v1: first technical failure, no screening

Exact command (one attempt):
```
cd /workspace/onia-av-pilot-20261106/panns-setup-v1
python3 -B launch_setup.py > preparation-launch.log 2>&1
```
Preflight manifest79a129ee5338c338205e2b5d0c3bd2139429d40160dd05ce5441145259b12a4a,
its8 files/marker and ONIA HEAD/clean state were verified before preparation.
No MiniCPM runtime or weight was opened. All writes are in this new folder.

The single preparation supervisor started BEFORE its child could make any network
or installation action; hard global wall300s, AS3GiB virtual per process,
RLIMIT_CPU300s per process, affinity ONE common CPU for all descendants,
workers1/batch1, reserve>=6GiB, no swap addition. Same-one-CPU descendants plus
global wall300 also bound aggregate scheduled CPU; reported CPU is only sampled.
Parent limits/affinity/handler unchanged. Monitor only own PGID23594 and memory
namespace visible in prior preflight. No services, permission/config changes,
compiler, fallback build, CUDA or package installation were invoked.

FAILURE: official CPU torch index HTTP request succeeded,431099 response bytes.
The script selected the torch2.5.1+cpu cp312 Linuxx86_64 wheel link from that
index, set stage download_wheel:torch, and failed fetch's initial hostname
allowlist assertion BEFORE opening a wheel file or making its HTTP request.
The local downloader's host restriction rejected that absolute link. Its actual
hostname was not persisted, so no hostname is invented here. This is our guard
failure, NOT evidence of denied network policy, absent official wheels, invalid
checkpoint, insufficient resources, incompatible framework or PANNs rejection.
The index body was not retained; no network rerun was made to recover its contents.

Child exit1, supervised wall0.6820892569994612s; child setup0.5297685580007965s.
Network metadata431099B, zero wheel files, no venv, no installed package/checkpoint,
no heavy imports/inference and no retries/reset of the300s clock. Parent launcher
itself prints the report and exits0; that is NOT the child result or a passed gate.
Sampled RSS23543808B and CPU0.18s are not exact peak/usage. Own group left no live
or zombie processes; reserve remained>31GB. Historical processes were untouched.

setup.py/source retained exactly, including failed guard. Its intended later
steps (NOT REACHED): binary-only PyPI/officialCPU downloads, METADATA inspection,
offline closure validation before install, isolated venv/offline installation,
explicit Zenodo checkpoint bytes/MD5/SHA validation. PANNs wheel and LICENSE.MIT
hash checks, including anomalous unmodified Google/Angular notice, also NOT
REACHED. No claim that a closure or installation was validated.

Screening entries0, no scores/curves. The requested paired diagnostic remains
unevaluated: Speech(voice)>Speech(zeros), and Speech(first voice segment)>
Speech(final silence). No0.5 event threshold or silence-pass claim is made.
Acoustic acceptance pending; technical guard failure is not a PANNs verdict.
No32k derivative generated; existing fixture/voice source bytes untouched.

Missing next units: corrected official-index link validation in a new cut while
retaining this failure, fixed wheel/transitive URL/hash closure, verified local
checkpoint, then frozen32k derived inputs/wrapper/criteria before any output.
Those are documented, NOT performed automatically after this first failure.

Export contains only new UTF-8 source/receipts/logs, each part<=10000 characters.
No wheels/weights/media/private URL/credentials/old artifact copies. Verify
manifest before later continuation; observed workspace persistence is not a
durability guarantee. ONIA/configuration/snapshot/publication unchanged.
