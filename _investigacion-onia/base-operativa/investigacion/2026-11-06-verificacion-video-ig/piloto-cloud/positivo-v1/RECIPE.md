# Positive v1: preserved technical failure before inference

Commands actually executed, in this directory:
```
python3 prepare.py
python3 launch.py > invocation.log 2>&1
python3 close.py
```
No repeat preparation/tests/build/install/download. prepare.py verified the prior
21-file manifest and marker, all frozen runtime sources/own ELFs and three weights
with bounded streaming SHA. Budget passed. flite is included in existing FFmpeg;
listing voices returned awb/kal/kal16/rms/slt. kal16 generated the complete phrase
one two:13823 samples at16kHz,0.8639375s. Zero-padded to1s, then one separate1s
silence chunk. The generator made224x224 white/red-square-left first and
white/blue-circle-right last; JPEGs were decoded back to224x224 RGB. Source voice,
PPM sources, exact commands and hashes remain local in control-manifest.json.
No media binary is exported. Generator truth is not human audition.

input-freeze.json froze generator/driver/control manifest/truth before launch.
Only signals and the intended neutral prompt would reach the model. Truth is
never in argv. Runtime, models, sampler and supervisor remain unchanged.

IMPORTANT FAILURE: adapting the new driver, I pointed its prompt read at the
older workspace ROOT/model-prompt.txt instead of the canonical file used by the
negative, negativo-v1/model-prompt.txt. The literal assertion rejected it before
os.execv. The failed frozen source remains exact. No model was loaded or invoked,
no context or modality telemetry exists, no response or semantic verdict exists.
There was one supervised child attempt, exit1 after8.326250243000686s; sampled
RSS11755520B, not an exact peak. No retry or silent source fix was performed.
Canonical prompt remains exact and unchanged. A next authorized correction would
only select negativo-v1/model-prompt.txt; this recipe does NOT perform it.

Existing supervisor v2 policy: hard AS12GiB virtual address space and CPU600s
per process, wall600s including validation/load/control; affinity2CPU, workers2,
explicit sampled OS-thread cap16; reserve8GiB/free disk30GiB/tree16GiB,
log256KiB/output1MiB. It restored parent limits/handler, left no live/zombie
descendants, did not truncate output. Actual CPU usage was not captured.

Cormac access check: only pertinent nonhidden workspace media file metadata was
inventoried, excluding credential/configuration folders and build/runtime trees;
no media files found. The exact ONIA reference document records a prior anonymous
yt-dlp download, but that is not proof of this Cloud transfer. Neither yt-dlp PATH
nor Python module exists here. curl/FFmpeg exist, but no direct media URL is known.
No request/download/authentication/upload/permission expansion was performed.
cormac-access.json records this concrete transfer limitation before more controls.

cormac-estimate.json uses ONLY the retained negative log/report. Loading8.907s,
two image encoders39.00135s, overall135.59645424s. Separate prefill/decode timings
are unavailable; do not label the unseparated remainder as either. A38-entry
224x224/1s scheme estimates3182 positions including128 response, exceeding2048;
image encoding alone extrapolates741.02565s. Linear total extrapolation is only
a single synthetic-point estimate, not measured reel cost. Proposed [0,3) sample
has417 estimated positions and198.941s estimated wall, not whole-reel coverage.
No Cormac execution was launched and positive acceptance cannot be claimed.

Export contains only NEW scripts/receipts/logs, no copied runtime/negative files,
weights or media. Each tool-read part is <=10000 characters; reconstruct UTF-8
bytes without extra separators and check manifest.json. Local workspace presence
does not guarantee durability; verify marker/manifest before continuation.
ONIA/configuration/snapshot/publication untouched. STOP at this failed attempt.
