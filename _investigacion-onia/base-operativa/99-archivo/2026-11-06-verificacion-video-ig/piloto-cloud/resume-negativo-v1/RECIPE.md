# One authorized Range continuation + one execution of the fixed first negative

## Continuity and unchanged cuts

Before transfer: v2 marker cf57ebcd-c598-496d-8987-8848bcdfc0f4 and manifest
c4211c3f120bbbeabd2c8abc57e88d08278b6ed3ccada230477a555e6e1bf088 (16 files),
build manifest d0a2dbabdd8abcc253040b21bb7bd5d4a3f5633cfda94ce7207f636dfc45457a
(7 files), and negativo-v1 manifest
8532f2ab6f0f90aed4e034813012675e17c6b625be8c9ec35d707fc774f70896 (24 files)
were verified. Frozen source and own linked-library hashes matched. LLM/audio
were streamed through SHA again, and the retained vision prefix matched exactly
171966464 bytes and fb749ab559817ef0a472e94104808e131f18f049fe7b22063f91c568aabfa8e0.
No tests, build, new family or service was started. continuity-before.json
records actual resource availability before the run.

All old manifested text files remain byte-exact after this stage. The ONLY old
data file modified was the explicitly authorized vision partial: valid bytes were
appended, then the same file was renamed to its complete GGUF name. No complete
weight copy/re-download. Old incomplete receipts/inventories remain historical.

## Exact commands and protocol

```sh
cd /workspace/onia-av-pilot-20261106/resume-negativo-v1
python3 launch_transfer.py > transfer-invocation.log 2>&1
python3 launch_model_once.py > model-supervisor-invocation.log 2>&1
```

Exactly one transfer continuation and one model invocation; no automatic retry.
The Range request was bytes=171966464-1095113183, Accept-Encoding=identity,
to the already-fixed official resolve/db25077c33951fe163b42986fba0132e279872a2/
vision/MiniCPM-o-4_5-vision-F16.gguf URL. Before opening for append, the program
required HTTP206, exact Content-Range bytes171966464-1095113183/1095113184,
Content-Length923146720, identity encoding and unchanged inode/size. A 200 or
invalid range would close without appending/consuming a full replacement file.
It appended923146720 bytes, closed the file, and streamed a second-pass SHA over
all1095113184 bytes. Final SHA is
1453678cc4e4fe18de241952962e234f265cb8dda780773526103ab8ba82f421.
No signed redirect URLs were persisted. No LLM/audio download and no TTS weights.

## Existing driver and two receipt paths

The existing negativo-v1/model_driver.py remains unchanged at SHA
6b8bbac1e3712acf51866f9bc2ec86fe10595f166ea39090d9b0fb773c422ceb.
Its hardcoded historical weight receipt still says complete=false, and must not
be overwritten. run_existing_driver.py executes its exact source bytes with ONLY
two child-process I/O mappings: read the complete weight receipt in this new stage,
and write its exclusive invocation receipt here instead of in negativo-v1.
driver-routing.json declares both paths. No other I/O, model argv, prompt, runtime
source or resource policy is changed. The unchanged driver's closed-file hash
checks run over all three weights again before os.execv replaces that same child
with the model. No extra smoke/process context is used.

The old control, generator, UUID, two JPEG/WAV pairs and their hashes were reused
unchanged; no new control or media was generated. model-invocation.json contains
the exact argv. Only the fixed signal pairs and canonical prompt reach the model,
not control truth or this recipe. CPU/no-TTS/no-VAD; n_ctx2048, response128,
temperature0, seed20261106; same frozen v2 ELF and own shared libraries.

## Resource contracts and observed result

Both phases: AS hard/soft12 GiB virtual address space PER PROCESS; CPU600 s
PER PROCESS, affinity2 CPUs, library workers2, OS-thread cap16, reserve
min(MemAvailable,visible memory.max-current)>=8 GiB, free disk>=30 GiB,
tree<=16 GiB, persisted log256 KiB/cut above1 MiB observed. Transfer wall300 s;
model wall600 s includes driver validation, load and the control together.
Supervisor v2 is unchanged. Its RSS maxima are sampled, not exact peaks; cgroup
memory includes cache. Parent limits/handler restored, own cleanup complete.

Transfer exited0 after173.0394700900015 s. Model exited0 after135.59645423999973 s.
Model RSS sampled maximum10784366592 bytes, observed OS threads at most3.
Actual CPU seconds were not captured; CPU600 s is a limit, not consumed time.
Native telemetry:210 input positions (including62 literal-text/control positions)
+128 response reserve=338 < effective_context2048 BEFORE any KV insertion.
Each of two chunks: audio decoded16000 samples, encoder1, accepted10 positions;
image decoded/encoder1, accepted64 positions. Literal prompt accepted29 positions.
Final n_past250, response41 sampled/40 accepted (EOS terminates), complete=true,
no chunk errors and no output truncation. Raw response is model-response.txt.

No sound is invented in this synthetic gray/silence response. This observation
is not general perception, temporal precision, acceptance of a positive or an
analysis of Cormac. Integration/review must assess this exact response. STOP here:
no positive/battery8/Cormac processing, alternate profile, further inference or
publication is performed automatically.

## Export/recovery and consumption

The stage manifest covers UTF-8 code, metadata and bounded logs only, no weights
or binary controls. Sources/old cuts/control/own ELF hashes were checked again
after the model ended. New inventory-storage.py only changes the output receipt
and complete-weight ledger locations of the prior read-only inventory, preserving
old inventories. inventory-storage.json measures actual own-workspace apparent
bytes and allocated filesystem blocks without following symlinks; RAM/cgroup are
separate in memory-observation.json. Persisting across these turns is an observed
fact, not permanent storage or guaranteed future recovery.

Tool readings emit each exported file/part with at most10000 characters, UTF-8,
without base64. Concatenate parts without extra bytes and verify the manifest.
No ONIA sources/state, environment configuration, snapshot, VPS or accounts were
modified. The new marker and manifest must be checked before any future stage.
