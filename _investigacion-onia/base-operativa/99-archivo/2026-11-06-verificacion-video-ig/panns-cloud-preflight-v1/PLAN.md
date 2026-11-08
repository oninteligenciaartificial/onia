# Phase1a metadata preflight, no execution authorization implied

Executed once:
```
cd /workspace/onia-av-pilot-20261106/panns-preflight-v1
python3 -B preflight.py
```
Only stdlib and importlib.metadata used. No network, pip, heavy framework import,
checkpoint, inference, fixture generation, service, model-family investigation or
license search. Previous18/7/17/21-file manifests and marker verified, ONIA clean
at e55812ce1bc8ef798fb370257ba887d07acccc53. MiniCPM weights/runtime not opened.
Fixture hashes include original flite source and PPM/JPEG/WAV sources. Positive-v2
uses positive-v1 fixture; accepted negative remains only an accepted negative.
Truth is deterministic generator metadata, not human audition.

Observed host RAM35743748096B, available34792882176B, swap0. Visible cgroup maximum
34359738368B/current2761736192B; effective reserve31598002176B >=6442450944B.
One namespace-visible cgroup level; no access/claims for hidden host ancestors.
cpu.max400000/100000=4 CPU equivalents; cpuset0-4, parent affinity0-4. Proposed
entry remains CPU1/batch1, not an increase to the2CPU ceiling. Free disk56903487488B.
Existing parent AS/CPU limits unchanged/unlimited. Own process metadata shows
historical zombies including build group8511, RSS0; none in the last positive,
transfer or failed-wrapper groups. No signal, cleanup or modification performed.

Versions read without importing frameworks:
- primary Python3.12.14: numpy2.3.5 only among six requested distributions.
- system Python3.13.5: numpy2.2.4 only among those distributions.
- no venv found in bounded pertinent search /workspace and /opt/codex/runtimes.
- torch, torchaudio, librosa, torchlibrosa, panns-inference absent in both.
This is not proof of absence in unsearched external locations or proof of CPU ABI.

Next missing items for integration's next decision:
1. A local isolated Python3.12 venv, no system-site-packages; leave both existing
   interpreters/packages unchanged. Creating it/installing anything was NOT done.
2. Proposed DIRECT pins for a minimal CPU-only candidate: torch==2.5.1+cpu,
   numpy==1.26.4, librosa==0.10.2.post1, torchlibrosa==0.1.0,
   panns-inference==0.1.1. Use official PyTorch CPU wheel source for torch and
   official PyPI for the rest. torchaudio is inventoried but not a default extra;
   only if the selected already-reviewed wrapper requires it, use matching
   torchaudio==2.5.1+cpu. No CUDA wheels, fallback builds or automatic upgrades.
   These are proposed pins, NOT a resolved/verified installation lock. Official
   wheel existence, transitive closure and SHA256/bytes remain to be fixed before
   downloads; no metadata network request was made in this unit.
3. PANNs checkpoint exact official revision/filename/bytes/SHA and local explicit
   path, with auto-download disabled; not downloaded or invented here.
4. An entry supervisor implementing AS3GiB virtual per process, CPU/wall120s per
   entry, affinity1CPU, backend workers1, batch1, reserve>=6GiB and no added swap.
   Existing MiniCPM supervisor requires2CPU/2workers, so do NOT silently reuse it
   or weaken it. A separate standard-library entry launcher needs review next.
5. Under those limits, imports/address-space viability and CPU ABI must be tested
   before inference. Free RAM alone does not prove fit under virtual AS3GiB.
   A guard/import failure is a technical limit, not a rejection of PANNs.
6. Verify chosen PANNs input sample-rate contract (commonly32k versus existing16k
   WAVs); if conversion is required, declare/generate NEW derived fixtures with
   hashes without replacing originals. No conversion/inference occurred here.

Integration decides next step. No installation command has been executed or
represented as fully reproducible. Export only this new folder's UTF-8 evidence,
parts<=10000 characters; no binary media, credentials, signed URLs or old cuts.
Persistence is observed, not guaranteed permanent storage. ONIA, configuration,
snapshot and publication remain untouched.
