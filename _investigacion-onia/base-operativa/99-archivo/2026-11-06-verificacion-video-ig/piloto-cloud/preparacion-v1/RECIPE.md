# Preparation only / review before build, weights or inference

Own workspace: /workspace/onia-av-pilot-20261106. Runtime origin:
https://github.com/tc-mb/llama.cpp-omni, detached at
d30f00feadb7ebce95bacd55b0d104e3ef501481. No upstream contribution,
commit or push. ONIA checkout/configuration untouched.

## Commands executed

```sh
test ! -e /workspace/onia-av-pilot-20261106 && mkdir /workspace/onia-av-pilot-20261106 && git clone --no-checkout https://github.com/tc-mb/llama.cpp-omni /workspace/onia-av-pilot-20261106/runtime && git -C /workspace/onia-av-pilot-20261106/runtime checkout --detach d30f00feadb7ebce95bacd55b0d104e3ef501481
cd /workspace/onia-av-pilot-20261106
python3 prepare_patch.py
python3 test_supervisor.py > synthetic-tests.log 2>&1
cd runtime
git apply --check --reverse ../runtime-review.patch
git diff --check
git rev-parse HEAD
```

Patch generator must be run ONLY in this owned clone pinned at the authorized
revision: it restores those seven paths from that revision and overlays the
review draft. No installer, build or model command is called. Inspect the diff
before invoking it in any other checkout.

Tests had four iterations: v1 passed before sampled affinity enforcement; v2
failed four tests on readiness; v3 failed three tests because readiness was read
after taking a process sample. Final version checks readiness BEFORE sampling,
and passed seven tests. Earlier outputs are preserved in validation-v1/v2/v3.
These are supervisor synthetic tests, not AV trials, model successes or repeated
negative controls. Final logs apply to the final supervisor.py.

To reconstruct the adapter in a clean checkout at the pinned revision, either
run prepare_patch.py with the two adjacent template files, or review and apply:

```sh
git apply --check /path/to/runtime-review.patch
git apply /path/to/runtime-review.patch
```

## Resource contract and limits of enforcement

Child launcher starts a new session/PGID and sets AS soft=hard=12 GiB and CPU
soft=hard=600 s PER PROCESS. AS is virtual address space, not RSS. CPU includes
process threads, is not an aggregate group quota. Descendants inherit rlimits;
multiple processes could collectively use more than 12 GiB/600 CPU seconds.
Parent limits/affinity are recorded before and after and remain unchanged.
Child affinity is two selected available CPUs; library thread settings are two.
Adapter explicitly configures LLM normal/batch and both encoders to two threads.
Supervisor additionally stops sampled per-process counts >2 or changed affinity.
This is sampled enforcement, not an atomic kernel thread quota.

Wall time is monotonic <=600 s, subject to sampling/cleanup latency. Each sample
checks min(MemAvailable, every visible finite memory.max-memory.current) >=8 GiB,
workspace disk >=30 GiB, owned tree apparent bytes <=16 GiB. Symlink targets are
not followed; children must remain cooperative and write only in the owned tree.
These polling guards may overshoot between samples and reserve no memory/disk.
Hidden host cgroup ancestors are unknowable; unreadable required stats fail closed.
Group RSS is sampled from /proc for SID=PGID=owned leader; sums can count shared
pages twice, and the recorded maximum is NOT an exact peak. All output is drained
into at most 256 KiB persisted log, with termination after >1 MiB observed output.
Samples/report files are bounded by time/interval for these cooperative tests.
Only the owned PGID is killed; the test witness is cleaned up individually.
No security sandbox: deliberate setsid/PGID escape or writes outside this tree
are unsupported. An uncatchable supervisor death (SIGKILL/OOM) cannot guarantee
group cleanup; no kernel aggregate memory/pids controller was created.

## Runtime correction and context accounting

Upstream stream_prefill sync ignores text and several injection returns; async
uses an else-if text branch after media, so text mixed with media is not reliable.
Upstream audio encoding failure can return true; both low-level injection paths
may slide KV, and stream_decode can evict with a 1024-position end reserve.

Review patch adds an OPT-IN synchronous/no-TTS/simplex route to the same public
stream_prefill/stream_decode functions. It avoids those permissive paths; all
non-pilot routes remain the pinned original except CPU encoder backend selection
now respects n_gpu_layers=0. It is NOT merely a parser of upstream logs.

Index0 carries no media, tokenizes/stages neutral system framing only. Index>=1
requires paired audio+image, no skip/fallback. Literal prompt is the sixth prefill
argument on the final chunk; common_tokenize(parse_special=false) actually handles
it. Images use the runtime decoder and encoder; audio uses its decoder/preprocess
and encoder, with a new optional decoded_samples output. No VAD is introduced.
Audio normalization/resampling to mono16k is the upstream decoder behavior;
implicit 100ms padding is rejected based on original decoded sample count.

All chunks are encoded and staged BEFORE ANY KV insertion. Then actual vision
slice positions, audio positions, text/control tokenization, system/assistant
framing and full response reserve are summed. Required total must be strictly
less than min(requested n_ctx, llama_n_ctx). n_ctx and response limit have no
implicit pilot default and must be explicitly reviewed; 1024 is not assumed.
Encoder success is separate from accepted embeddings: accepted_positions counts
only successful injection batches, checked using bool and n_past delta. A failure
aborts the case; no partly failed context can be reused. Low-level pilot guards
reject capacity errors instead of calling the automatic KV sliding helper.
The pilot response path checks token injection, reserves its finite token budget,
and returns false if it reaches the budget without EOS (no silent truncation).
One process/new context per case; index0 also rejects reused/dirty contexts.

Counters: expected/delivered/decoded/encoder_ok/accepted by chunk+audio/image;
encoded and accepted positions separately. Text uses real tokenization and its
token positions, not an audio/vision neural encoder; decoded/encoder_ok for text
are not applicable and remain zero. PILOT_ERROR/CHUNK/BUDGET/RESULT are structured
observability emitted by the code, not independent verification of the model.
No acceptance of semantics, perception, audio, vision or a candidate is claimed.

## Not executed / blockers for next review

- No C++ compilation or CMake installation/configuration, no weights, no AV media,
  no inference, no 1-second smoke and no actual 2-second negative trial.
- CMake absent. PyPI metadata only: cmake 4.4.4 Linux x86_64 wheel 30,245,729 bytes;
  URL/SHA and official project links in cmake-pypi.json. Wheel not downloaded.
- Patch passes reverse applicability/whitespace checks only. C++ type/link/build
  behavior and failure paths need review and later authorized compilation/tests.
- Staging holds encoder outputs simultaneously; runtime peak x86 RAM remains
  unknown. 6.32 GiB weight files and MemAvailable do not establish fit, especially
  with a 12 GiB virtual-address-space limit and mmapped weights/KV/staged vectors.
- Strict generation uses the existing sampler/token/injection helpers directly,
  bypassing TTS/hidden-state streaming cleanup; review must confirm the intended
  singleplex template/EOS and sampling semantics before build or model loading.
- No-past/monotonic accounting checks successful calls; a failed backend call may
  leave partially modified backend state. Such a case is failed and discarded,
  not rolled back or accepted.
- Review sampled thread-count enforcement against native threadpool behavior;
  exceeding two observed threads fails closed, even if harmless helper threads.

Illustrative commands for a LATER authorized build, NOT executed now:

```sh
cmake -S runtime -B build-cpu -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=OFF -DGGML_METAL=OFF -DENABLE_COREML=OFF -DGGML_OPENMP=OFF -DGGML_BLAS=OFF -DLLAMA_CURL=OFF
cmake --build build-cpu --target llama-omni-single-test-omni -j2
```

Any future candidate run requires independent review of supervisor+patch and a
new explicit authorization for weights/build/load. A neutral model-prompt.txt is
separate from control-truth.json. Neither has been passed to a model. Coordination
will choose ONE negative of 2 s later; no duplicated model successes are planned.

## Recovery

review-manifest.json hashes exact recoverable UTF-8 files; workspace-marker.json
identifies this preparation and binds a deterministic payload manifest hash.
Recheck both before any continuation; filesystem presence across turns is NOT
assumed. Tool-read emissions provide the actual contents in numbered <=10000
character chunks, without base64. A local ZIP is an optional copy, not an external
upload nor a promise of persistence or a native attachment mechanism.
