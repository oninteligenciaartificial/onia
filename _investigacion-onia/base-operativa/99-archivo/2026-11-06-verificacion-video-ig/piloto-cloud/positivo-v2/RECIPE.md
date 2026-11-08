# First real positive inference, canonical prompt reference correction only

positivo-v1 and its17-file manifest/failure remain byte-exact. Its failed child
never exec'd a model. This directory contains a copy of its driver with exactly
ONE source-line change: ROOT/model-prompt.txt -> ROOT/negativo-v1/model-prompt.txt.
driver.patch is the complete diff. Before starting, the canonical file matched
SHA d7722f2df0a045f636450edf38e1769beb0bb30d0e78502ec3a8779e0f167b4a
and the exact accepted neutral Spanish text. No prompt bytes, fixture, truth,
models, frozen runtime, sampler, context or resource policy changed.

run_driver.py routes only the old exclusive model-invocation.json write into
positivo-v2. All other reads use existing files, notably the unchanged positive-v1
fixture and truth manifest; truth itself is never passed to the model. New runID
positive-v2, fresh process/context, exclusive one-attempt.lock, no retry.

Exact executed command in this directory:
```
python3 launch.py > launch-output.log 2>&1
```
The existing v2 supervisor enforces hard AS12GiB virtual address space/CPU600s
PER PROCESS, wall600s for validation/load/control combined, affinity2CPU,
backend workers2, sampled explicit OS-thread policy cap16, reserve8GiB,
free disk30GiB/tree16GiB, log256KiB/output1MiB. Limits apply only to children;
parent limits/handler restoration and own-group cleanup appear in model-report.
Model CPU/noTTS/noVAD, context2048/response128, temperature0/seed20261106 unchanged.

The reused control is2s: complete included-flite kal16 voice one two (13823 samples,
0.8639375s), zero padded to1s with red square left on white, then exactly1s of
silence with blue circle right on white. Both input WAVs16000 samples,224x224 JPEGs.
The previous generator/source/hash receipts are referenced, not re-exported.
Truth is generator truth, NOT human audition. No fixture regenerated.

Model response/telemetry/report are literal evidence, not semantic autoacceptance
from exit0. result.json records the outcome; integration/reviewer assess voice,
words, figure/color/order and final silence. No retry, second positive, Cormac,
new benchmark or publication. The simultaneous two-track transfer is separately
documented in cormac-transfer-v1 and contains no exported signed URL.

finalize.py verifies old manifests and frozen sources/own ELFs after the run and
extracts existing log telemetry; it does not run a model. RAM/RSS are separate
from disk; RSS maxima sampled, not exact peak; actual CPU usage not captured.
Each exported UTF-8 part <=10000 characters, no weights/media/runtime copies.
Verify new manifest and marker for future continuation; no durability guarantee.
