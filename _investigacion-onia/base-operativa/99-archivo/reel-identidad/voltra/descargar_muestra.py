"""Download one observed video source from Voltra's product-page carousel."""
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
MEDIA = ROOT / "operacion/referentes-20261105/reel-identidad/voltra"
SOURCE_ID = "a081891a8e224825ac38370d1b22d62c"

evidence = json.loads((OUT / "page-media.json").read_text(encoding="utf-8"))
sources = []
for item in evidence["media_tags"]:
    for key in ("src", "data-src"):
        value = item["attrs"].get(key)
        if value and (".mp4" in value or ".m3u8" in value):
            sources.append("https:" + value if value.startswith("//") else value)
evidence["candidate_media_urls"] = sorted(set(sources))
(OUT / "page-media.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
url = next(url for url in sources if SOURCE_ID in url and ".mp4" in url)
path = MEDIA / ("voltra-black-edition-carousel-01-" + SOURCE_ID + ".mp4")
request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
limit = 100 * 1024 * 1024
with urllib.request.urlopen(request, timeout=30) as response:
    declared = response.headers.get("Content-Length")
    if declared and int(declared) > limit:
        raise RuntimeError("Source exceeds the bounded 100 MiB sample download")
    content = response.read(limit + 1)
    if len(content) > limit:
        raise RuntimeError("Source exceeds the bounded 100 MiB sample download")
    status, final_url = response.status, response.url
    mime = response.headers.get("Content-Type")
path.write_bytes(content)
probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels,duration", "-of", "json", str(path)], capture_output=True, text=True, check=True)
decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True)
result = {
    "date": "2026-11-05", "page_url": evidence["source_url"],
    "page_html_sha256": evidence["html_sha256"],
    "section_id": "shopify-section-template--20317438410812__image_slider_YEFPbi",
    "selection": "First video source in the product-page carousel; commercial publication by store, original creator not established",
    "source_html_lines": [9405, 9426], "source_url": url, "resolved_url": final_url,
    "http_status": status, "content_type": mime, "file": str(path), "bytes": len(content),
    "sha256": hashlib.sha256(content).hexdigest(), "ffprobe": json.loads(probe.stdout),
    "decode": {"exit_code": decode.returncode, "stderr": decode.stderr},
    "coverage": "recovery and complete technical decoding only; no vision or listening",
}
(OUT / "sample-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=True))
