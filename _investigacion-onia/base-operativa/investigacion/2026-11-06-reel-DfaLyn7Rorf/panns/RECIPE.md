# DfaLyn7Rorf / Aidan Murphy / @murphmaxxing: PANNs auxiliary audio result

Only this new directory was written. Cormac/pilot/ONIA/configuration/publication
unchanged. Current runtime skill/environment status/network policy checked before
network: current running managed instance, policy enforced unrestricted; executor
policy unrestricted/VPNfalse. No secret reads or environment/config changes.

Executed once, with reused own-group CPU1/AS3GiB/reserve6GiB supervisor:
```
python3 -B launch_transfer.py > transfer-launch.log 2>&1
python3 -B launch_inputs.py > inputs-launch.log 2>&1
python3 -B run_windows.py > inference-launch.log 2>&1
```
Transfer total120s, each track<=64MiB, retries0; inherited proxy/CA/TLS unchanged.
Only the TWO anonymously supplied CDN tracks, no extraction/search/formats/login.
HTML &amp; entities decoded in private-spec.json. That file and all signed URLs/
headers are excluded from export/logs. Closed-file SHA256 for both retained tracks.
FFmpeg remux -c copy, tracks retained, no media reencoding. Remux4019544B SHA
94af46ae425441fdf021bac0482be981a7225f2dacfbd713d707b8a39e3d7f74.
Different from supplied PC container4019553B/b2006a4f..., but BOTH ordered compressed
payload streamhashes match PC exactly (payload-comparison.json). No identical
container/timestamp claim. Video1126 frames/30fps,37.533333s; remux audio37.548005s
versus PC metadata37.545011s, a container/timestamp variant, not a payload mismatch.

PANNs and local checkpoint reused, actual327428481B/SHA verified before use:
dd3b4043a87d4ec13df8082c0fcfee3fb5084151808e47e060987a95eabdd142.
Existing CSV527classes SHA cdd1049833c4b86127c2773ac0d14a2754b6a6d0d1798002ed5c66e699708429.
Adapter byte-identical to prior frozen PANNs adapter; only orchestration/output
directory patches. No installation/new model/controls/battery.

FFmpeg decoded whole audio to mono PCM16LE32k,1201539 samples=37.54809375s.
All samples covered once: [0,10),[10,20),[20,30),[30,37.54809375). No VAD/crop/
padding. Tiny PCM/container rounding difference explicit, visual analysis0.
Inputs/adapter/parameters hashes frozen before any outputs. Model eval/no-grad,
batch1, backend workers1, affinity1CPU, AS3GiB virtual per process, CPU/wall120s
per window, reserve6GiB. Kernel sockets denied in each child, no auto-download.
Fresh process/model per window, one inference each; no retries.

Four entries exit0. Total entry wall71.77618684s, maximum30.76598745s<120s.
Sampled RSS maximum1251983360B, not exact peak. All own groups empty and parent
limits/affinity/handlers restored. Resources/CPU samples retained; CPU not exact.

Raw framewise arrays for ALL527 classes plus labels/maxima preserved. Full native
Speech/Music curves and1s derivative retained. Grid10ms is nearest-interpolated
model output, NOT validated temporal precision. Summary excludes duplicate final
window boundary rows; means from9-significant-digit CSV values. No thresholds,
independent event labels, emotion/music-absence/mix/words/AV-integral conclusions.
Speech peak0.5738525391, Music peak0.6796256304 are candidate scores only.

ASR omitted: coordinator confirms PC small CPU+Silero already done; no Cloud ASR
needed. Existing primary/system/PANNs interpreters also have no faster_whisper
distribution/module. No installation or local-weight search/download launched.

Compact export: receipt, selected scores, resources, source/patches, input manifest
and raw numeric hashes. Local numeric ZIP includes full raw curves/maxima, not
media/weights/private signed URLs or prior history. Text parts<=10000 characters,
UTF-8, concatenate without extra bytes. Persistence observed, not permanent.
