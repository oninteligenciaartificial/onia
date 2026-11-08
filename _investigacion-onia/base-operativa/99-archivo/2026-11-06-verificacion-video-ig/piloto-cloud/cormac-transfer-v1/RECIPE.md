# Selected two-track anonymous recovery, no reel inference

The two supplied signed CDN URLs were stored ONLY in private-spec.json in this
workspace. That file, its URL queries and headers are excluded from all exports.
No cookies/login, new formats/searches, installations, retries or uploads.
Public identity: Instagram reel DfWLWspIruU, account cormachdn.

Exact executed command in this directory:
```
python3 launch.py > launch-output.log 2>&1
```
launch.py invokes unchanged v2 supervisor with wall120s and existing AS12GiB /
CPU600s PER PROCESS, affinity2CPU/workers2/OS cap16, reserve8GiB/disk30GiB/tree16GiB,
log256KiB/output1MiB. transfer.py limits each response to64MiB, with socket timeout
<=20s and a shared110s internal deadline. No automatic retry. HTTP200 identity
responses had exact announced byte counts. Both files were closed before streaming
SHA256 reads, and retained. Supervisor ended exit0 in6.459325510999406s with no
live or zombie descendants; RSS maximum sampled59543552B, not exact peak.

FFmpeg remuxed only those files with explicit video/audio maps and -c copy.
Exact commands, probe codec/dimensions/duration/packet counts, URL-without-query
hashes and both streamhashes are in transfer-receipt.json. No signed URL is in a
subprocess command/log. The local MP4 is10749773B, SHA
2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5.
Its compressed video and audio streamhashes BOTH match those supplied from the
original PC file. This establishes matching ordered packet payload hashes, NOT
byte-identical containers or a measured equality of timestamps/side data.
The supplied original PC file was10749782B with different SHA; it was not touched.
Probe now reports video37.733333s/2264 packets and audio37.780000s/816 packets,
container37.780000s versus supplied original37.753991s. Treat as remux variant.

No Cormac inference, decoding for perception, ASR or model execution was performed.
The source tracks and remux remain local; no binary media exported. Persisting in
this workspace is observed availability, not permanent storage. ONIA/configuration,
old cuts and publication untouched. Wait for integration's decision before reel use.
