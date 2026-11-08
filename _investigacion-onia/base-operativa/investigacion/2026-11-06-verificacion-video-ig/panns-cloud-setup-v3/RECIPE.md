# Final PANNs test: one known-control pair and complete Cormac audio coverage

Practical result: useful as auxiliary candidate Speech-activity scoring on the
measured inputs. This does NOT establish a validated acoustic detector or integral
reel analysis. No calibrated event threshold, music-absence, exact event boundaries,
transcription, emotion, mixture or audiovisual synchronization claims.

Only missing static labels were added after v3's preserved offline import failure.
Original package config was inspected, not edited. Official Google AudioSet CSV
was pinned to generation1488737428851815 over HTTPS,14675B, SHA256
cdd1049833c4b86127c2773ac0d14a2754b6a6d0d1798002ed5c66e699708429.
All527 ordered indices0..526,527 unique MIDs and expected columns validated.
Namespaces g/m/t are present. Speech index0, Music137. File installed ONLY at
panns-setup-v3/runtime-home/panns_data/class_labels_indices.csv, matching the
already-isolated Path.home used by the child. No global HOME/config/package code
change or auto-wget. Two mistaken namespace validations were preserved; retained
raw bytes were then validated/installed OFFLINE without another fetch.

No package/checkpoint reinstallation or new model. Same verified Zenodo checkpoint
SHA dd3b4043a87d4ec13df8082c0fcfee3fb5084151808e47e060987a95eabdd142.
Existing supervisor reused with only output directory changed. All model entries
CPU1/workers1/batch1, AS3GiB virtual per process, CPU/wall120s per entry,
reserve>=6GiB; no swap added. Kernel network denial and shell-download guard apply
only in each child. No automatic downloads/inference retries. Parent restored.

Successful model commands, each launched through supervise.run (exact specs in
commands-and-limits.json):
```
python3 -B run_entry.py zeros-real zeros
python3 -B run_entry.py voice-real voice
python3 -B run_windows.py
```
A prior relative-interpreter launcher failed before exec of adapter/model and is
retained separately. Six REAL inferences total: zeros once, voice once, Cormac
four windows once each. No repeated real inference or semantic tuning.

input-freeze.json fixed adapter/input hashes/parameters/criterion BEFORE scores.
Known fixtures were concatenated/resampled16k->32k with existing FFmpeg, no VAD,
truncation, extra padding or change to original files. Entire flite phrase remains.
Known-control Speech maximum voice0.2354815751 > zeros0.0020532431; first voice
segment mean0.2171106189 > final silence0.0210686009. Both paired diagnostics pass;
these known controls are calibration/screening, NOT retained independent validation.
Voice maximum is below0.5; no invented0.5 event-acceptance rule was used.

Same Cormac remux, source SHA2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5,
already matched both original compressed streamhashes, container variant37.78s.
Audio decoded without -t into1208968 samples at32k. Windows cover first1208960
samples exactly: [0,10),[10,20),[20,30),[30,37.78), no padding.8 decoded samples
beyond declared container duration (0.00025s) retained in full decoded WAV but
excluded from declared37.78s coverage. Visual coverage0. New process/model for
each window, no VAD. Window boundaries/receptive-field edge effects acknowledged.

All527 raw framewise curves, class labels and maxima retained for all6 entries.
NPZ plus full Speech/Music CSV files are hashed in numeric-artifacts.json and
included in local numeric bundle. Grid10ms is nearest-interpolated model output,
NOT validated temporal precision. Raw window output includes boundary-touching
frames; aggregate timeline excludes each final boundary row to avoid duplication.
1s summary is derivative, means calculated from9-significant-digit CSV values.
Exact single-entry maxima remain in receipts and NPZ, no raw scores overwritten.

Resource/exit/cleanup receipts are in entry-resources.json. Maximum entry wall
27.131465192s; maximum sampled RSS1267875840B (not exact peak). No inference failed.
Preparation including prior failed import/static-recovery/preprocessing costs
194.59816909s total under300s. Application-layer received accounting678616455B,
including new HTTP headers/metadata/body; TLS/IP/proxy overhead/unread buffering
not observable, not claimed exact wire traffic. Same budget, no reset/increase.

Runtime skill/current attached environment status and executor network policy were
checked before CSV network work: observations current, running, HTTP enforced
unrestricted, local VPNfalse. No credential reads/config edits/new VM/services.
Old v1/v2/v3 failed cuts and fixtures retained; ONIA clean and no publication.
Local persistence is observed, never called permanent storage.

Compact handoff excludes packages/checkpoint/media/history bodies. It contains
current adapter, reproducible commands/freeze/provenance, score/resource summaries
and numeric artifact hashes. Local ZIP holds raw numeric outputs/static CSV plus
this handoff, no media/weights/credentials or signed CDN URLs. Text read parts
<=10000 characters, concatenate without separators, verify manifest before reuse.
