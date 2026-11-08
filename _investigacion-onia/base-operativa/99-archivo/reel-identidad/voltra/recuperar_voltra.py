"""Recover public media locators from the exact Voltra product page; no cookies/login."""
import hashlib
import html
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

URL = "https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition"
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MEDIA = ROOT / "operacion/referentes-20261105/reel-identidad/voltra"


class MediaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag in ("video", "source", "iframe"):
            self.items.append({"tag": tag, "line": self.getpos()[0], "attrs": dict(attrs)})


def main():
    MEDIA.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
        final_url, status = response.url, response.status
    (MEDIA / "product-page.html").write_bytes(content)
    source = content.decode("utf-8")
    parser = MediaParser()
    parser.feed(source)
    expanded = html.unescape(source.replace("\\/", "/"))
    candidates = sorted(set(re.findall(r"https?://[^\s\"'<>]+?\.(?:mp4|webm|m3u8|m4v)(?:\?[^\s\"'<>]*)?", expanded)))
    candidates = sorted(set(candidates) | {
        ("https:" + value if value.startswith("//") else value)
        for item in parser.items for key, value in item["attrs"].items()
        if key in ("src", "data-src") and value and re.search(r"\.(mp4|m3u8|webm|m4v)(?:\?|$)", value)
    })
    result = {
        "source_url": URL, "final_url": final_url, "http_status": status,
        "html_file": str(MEDIA / "product-page.html"), "html_bytes": len(content),
        "html_sha256": hashlib.sha256(content).hexdigest(),
        "media_tags": parser.items, "candidate_media_urls": candidates,
        "method": "public HTTP GET; no cookies/login; normal TLS verification",
    }
    (OUT / "page-media.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
