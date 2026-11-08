# v2: frozen sources, review and authorized CPU build; NO AV/model load

Persistence verified this turn before changes: v1 marker
dc7c7e75-c719-49b3-ad42-78055f27430c; manifest SHA-256
f66dd70c99c435f02017e96bdda314a60415bc77bf0d8ce4093b837d2e6ff0ea;
12/12 file hashes and byte sizes matched. Flat review/ remains unchanged;
review/v1/ is an additional exact copy. v2 is in review-v2/.

Base: tc-mb/llama.cpp-omni d30f00feadb7ebce95bacd55b0d104e3ef501481.
runtime-review.patch is the complete diff against this commit, including v1.
source-freeze.json hashes the seven modified/added source paths. Frozen sources
are not changed during review or compilation. No commit, push, configuration,
snapshot, ONIA source/state edit or external upload.

## Corrections

1. SIGTERM raises a dedicated supervisor exception; cleanup sends SIGKILL only
   to its own session/PGID, records cut receipt, ignores repeated SIGTERM during
   cleanup, and restores the parent's exact previous SIGTERM handler in finally.
   Parent AS/CPU/affinity remain unchanged. SIGKILL/OOM of the supervisor cannot
   guarantee cleanup: this is a cooperative launcher, not a container sandbox.
2. A leader exiting zero with live descendants is incomplete_group_shutdown,
   not success. Live and zombie members are recorded separately before/after
   cleanup; pending live work is a failure, zombies await their actual reaper.
3. --vision-backend accepts only cpu, consistent with pilot mode.
4. Before omni_init: seed=20261106, temperature=0, dynamic range=0, mirostat=0,
   sampler chain=[TEMPERATURE] then the upstream dist(fixed seed), no extra filters,
   EOS respected. PILOT_SAMPLER records the fixed policy. This does not claim
   bitwise reproducibility across architectures or changes in floating point.
5. Decoder initializes frame_count/frames_read, records actual frames_read,
   resizes to actual read length and rejects empty/short/error reads. Strict
   pilot validates each RIFF/WAVE chunk BEFORE resampling/preprocess: exactly
   1 second, mono, 16000 Hz, PCM16 or IEEE float32, complete RIFF/chunk lengths,
   matching block alignment/rate and 16000 frames. RF64/extensible/other formats
   fail explicitly. This prevents mel_spec_chunks[0] silently dropping later
   seconds. A future single negative of 2 seconds must use two 1-second pairs.
6. model-prompt.txt is the sole neutral content prompt. control-truth.json from
   v1 stays separate and is NEVER an input to the model. No truth or expected
   perceptual answer is encoded in the prompt or system framing.
7. vision_n_mmproj_embd(ctx_vision)==LLM hidden is checked BEFORE encoding/staging,
   in addition to per-vector divisibility and audio projector dimension.

## Threads and unchanged resource budget

Two selected affinity CPUs, two backend workers and child library thread settings
remain fixed. They are not a guarantee of two total OS threads. Read-only source
inspection: ggml-cpu.c creates n_threads-1 helpers per pool (loop near 3278),
and frees disposable pools near 3373. Multiple backend/persistent pools can coexist.
Audio log-Mel preprocessing had a separate hardcoded FOUR workers; v2 fixes this
to TWO. The strict route uses sequential vision/audio/LLM stages and no duplex or
TTS workers, but actual native total threads remain unmeasured until authorized
runtime execution. j2 BUILD also has coordinator processes in addition to the two
compiler jobs. No aggregate OS-thread ceiling is inferred from backend workers.

Supervisor samples total-group OS threads independently. Default os_thread_cap
is explicitly null (observational); an explicit cap=2 is exercised in regression
and stops excess threads. This is the reviewed correction to the invalid global
2-thread assumption, not an automatic increase of CPUs, workers or other resources.
No runtime thread-count compatibility is claimed; review must decide any future
explicit OS-thread cap before AV. All group members retain affinity [0,1].

AS soft=hard=12 GiB and CPU soft=hard=600 seconds PER PROCESS; not RSS/group quotas.
Wall <=600 seconds, reserve min(MemAvailable, visible cgroup headrooms)>=8 GiB,
free disk>=30 GiB. Build additionally tightens owned tree from16 GiB to1 GiB and
wall to540 seconds. RSS/group sums are sampled, not exact peaks. Output cap remains
256 KiB persisted and termination above1 MiB observed. Guard latency can overshoot.

## Exact execution and omitted work

```sh
cd /workspace/onia-av-pilot-20261106/review-v2
python3 test_regressions.py > regressions.log 2>&1
cd ../runtime
git apply --check --reverse ../review-v2/runtime-review.patch
git diff --check
```

Five relevant supervisor regressions passed. Initial v2 run had one failure due
to a non-contractual 2-second setup timeout; that check was removed: startup is
still covered by total wall limit. Initial failure log is retained. Tests use
unique fixed run IDs; do not rerun into existing run directories or erase evidence.
No synthetic WAV/AV, no model success/negative trial and no inference was run.

CMake wheel URL from v1 cmake-pypi.json was downloaded ONLY into this workspace,
verified bytes=30245729 and SHA-256
f773a0544c66370408f451acd487c2c643b0dfebb48c5d64f3638bc1bb820238
BEFORE extracting. Zip paths and uncompressed size were checked; only the three
local tool executables had mode set to0700. No apt, sudo, global install or PATH
change. cmake-local-receipt.json records this. build_driver.py contains exact
version/configure/build argv and checks frozen sources before and after build.

Exact supervisor launch (executed from review-v2):

```sh
python3 - <<'PY' > build-invocation.log 2>&1
import dataclasses,json,sys
from pathlib import Path
import supervisor
p=dataclasses.replace(supervisor.Policy(),tree_bytes=1024**3,wall_seconds=540)
r=supervisor.run([sys.executable,str(Path('build_driver.py').resolve())],'v2-build',p)
print(json.dumps(r,indent=2))
sys.exit(0 if r['reason']=='exited' else 1)
PY
```

Only target llama-omni-single-test-omni is built, CPU/no-CoreML/no-OpenMP/no-BLAS,
with j2. Compile outcome/resources/log are separate artifacts; building does not
execute the target. No weights may be downloaded/loaded and no AV run may begin
until runtime review AND build outcome are assessed. Real peak RAM remains unknown.

Recover by applying the complete v2 patch to the pinned base, keeping v1 files.
Verify all manifest bytes/SHA and marker before resuming; do not assume this VM
persists. Tool emissions are numbered UTF-8 fragments <=10000 characters; join
without inserting newlines. Any later source correction must be a NEW diff,
never an unannounced edit of this frozen v2.
