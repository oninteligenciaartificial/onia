# One authorized first negative; no positives or automatic retry

Prerequisite persistence was verified before preparation: v2 marker
cf57ebcd-c598-496d-8987-8848bcdfc0f4; 16/16 manifest entries under SHA
c4211c3f120bbbeabd2c8abc57e88d08278b6ed3ccada230477a555e6e1bf088;
build continuation 7/7 entries under manifest SHA
d0a2dbabdd8abcc253040b21bb7bd5d4a3f5633cfda94ce7207f636dfc45457a.
Seven source-freeze entries and supervisor v2 were checked. No prior group's
live processes remained. v2 source code, ONIA and environment config stay unchanged.

The executable SHA is 9e93dec5eafa79172827df6afcd3d51abb2bb79123c4000a86dcbfc62e449f47,
55680 bytes. runtime-libraries.json inventories its recursive own DT_NEEDED
dependencies and CPU backend (possible dlopen), resolved real paths, sizes and
SHA-256. Their combined deduplicated size including the executable is13047280
bytes. The small executable is NOT a complete runtime fingerprint; system
library SONAMEs are listed separately, not claimed hashed host dependencies.

## Exact phase launch commands

```sh
cd /workspace/onia-av-pilot-20261106/negativo-v1
python3 launch_download.py > download-invocation.log 2>&1
python3 launch_control.py > control-invocation.log 2>&1
```

Control preparation may proceed while download runs. Model launch is permitted
only after successful download supervisor receipt, complete three-file hash
receipt, and successful control preparation:

```sh
python3 launch_model.py > model-supervisor-invocation.log 2>&1
```

This last command is invoked at most ONCE. A unique supervisor run directory and
exclusive model-invocation.json prevent silent overwrite/retry. model_driver.py
validates closed files again by streaming SHA, frozen source hashes and own ELF
hashes, writes exact argv/configuration, then os.execv replaces the same child
with the target: one fresh process/context, not an extra smoke. The control
truth/recipe are not passed as argv or text; only audio/image signals and the
canonical content prompt reach the model. No positive, alternate profile, prompt
retouch, escalation or further invocation is authorized by this stage.

## Transfer and control

Only the three fixed-revision files named in download_weights.py are requested
from openbmb/MiniCPM-o-4_5-gguf at db25077c33951fe163b42986fba0132e279872a2.
Expected sizes/hashes come from the coordinator's official LFS metadata, not a
previous download. Streaming chunks<=1 MiB, exact maximum bytes before write,
25 s network timeout, supervisor phase wall600 s. Internal deadline590 s leaves
cleanup margin. No retry/resume. Each file is closed, re-read by chunks for SHA,
and renamed without full-file duplication only after size/hash verification.
No weight read_bytes or export, no TTS. Receipts omit signed redirect URLs.

generate_control.py freezes a UUID opaque control. Two consecutive chunks have
declared intervals[0,1),[1,2), each with one JPEG224x224 and PCM16LE mono16k WAV
of exactly16000 zero samples. Frames represent their complete 1 s chunk; no
extra 1 s clip or perceptual smoke. ffmpeg encodes the uniform gray image and
decodes each JPEG to verify dimensions and uniform RGB; wave verifies each
WAV's header/sample bytes. control-manifest.json records exact generator/decoder
argv, hashes/bytes and declared PTS/duration. These timing declarations do not
establish model temporal precision. control-truth.json remains separate.

## Requested model configuration and guards

CPU, no TTS, no VAD, fresh context, explicit n_ctx2048, response_tokens128.
v2 fixes seed20261106, temperature0, temperature-only sampler then fixed-seed
distribution. model-prompt.txt is copied byte-exact from frozen v2; trailing
file newline is omitted from the CLI string. No control truth is added.
The reviewed adapter stages actual decoded/encoded signal, tokenized literal
text and framing, then checks total+128 < min(2048,llama_n_ctx) BEFORE KV
insertion. No context enlargement, clipping, eviction or failed-audio fallback.
PILOT_* telemetry distinguishes delivered/decoded/encoder/accepted work per
modality, and exits false on insertion/context/decode/response-budget failure.

The unchanged supervisor applies to the child only: AS hard/soft12 GiB virtual
address space PER PROCESS, CPU hard/soft600 s PER PROCESS, affinity2 CPUs and
library workers2; OS thread cap16 explicit, not a claim of16 active workers.
Download and model phases each have wall600 s. The model wall includes input
verification, weight loading and the control together. Fixture setup has a
tighter60 s wall. All use min(MemAvailable, visible memory.max-current)>=8 GiB,
disk>=30 GiB, owned tree<=16 GiB, persisted merged log<=256 KiB and stop above
1 MiB observed output. RSS maxima are sampled, not exact peaks; group sums may
double-count shared pages. No new kernel aggregate memory/thread cgroup exists.
Only the owned group is killed. Parent limits/handlers are restored; SIGKILL
of the supervisor itself cannot guarantee cleanup. No production VPS/services.

## Evaluation boundary and recovery

Technical failure in transfer, resources, decoder, context or runtime ends this
stage. If output invents sound, retain it as the negative's semantic result and
stop. Preserve complete output within the stated cap and identify any truncation.
Integration/review judge the raw output and counts; compilation or this single
negative does not certify audiovisual perception generally.

Export scripts, metadata/configuration, hash manifests and bounded logs only;
weights and binary media are excluded. Reconstruct control via generator and
verify hashes before any separately authorized reuse. Filesystem persistence
is not assumed; verify this stage's marker/manifest on later continuation.
