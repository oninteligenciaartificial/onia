#!/usr/bin/env python3
"""Describe pistas, cobertura de paquetes y decodificación de una grabación local."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("webm", type=Path)
args = parser.parse_args()
source = args.webm.resolve(strict=True)
if not source.is_file() or source.suffix.lower() != ".webm":
    parser.error("Se necesita un archivo WebM local.")
base = ["-protocol_whitelist", "file,pipe", "-i", str(source)]
metadata = subprocess.run(
    ["ffprobe", "-v", "error", "-threads", "1", *base, "-show_entries",
     "stream=index,codec_type,codec_name,width,height,sample_rate,channels:"
     "format=duration", "-of", "json"],
    check=True, capture_output=True, text=True,
)
media = json.loads(metadata.stdout)
streams = media.get("streams", [])
if sorted(stream.get("codec_type") for stream in streams) != ["audio", "video"]:
    raise SystemExit("Se esperaba exactamente una pista de audio y una de video.")

tracks = {
    stream["index"]: {
        **stream, "packets": 0, "first_pts_s": None, "last_pts_s": None,
        "end_pts_s": None, "max_step_s": 0.0, "pts_regressions": 0,
        "packets_without_pts": 0,
    } for stream in streams
}
packet_cmd = [
    "ffprobe", "-v", "error", "-threads", "1", *base, "-show_packets", "-show_entries",
    "packet=stream_index,pts_time,duration_time", "-of", "compact=p=0",
]
packets = subprocess.run(packet_cmd, capture_output=True, text=True)
for line in packets.stdout.splitlines():
    packet = dict(field.split("=", 1) for field in line.strip().split("|") if "=" in field)
    if "stream_index" not in packet:
        continue
    track = tracks[int(packet["stream_index"])]
    track["packets"] += 1
    if packet.get("pts_time", "N/A") == "N/A":
        track["packets_without_pts"] += 1
        continue
    pts = float(packet["pts_time"])
    previous = track["last_pts_s"]
    if previous is None:
        track["first_pts_s"] = pts
    else:
        track["max_step_s"] = max(track["max_step_s"], round(pts - previous, 6))
        track["pts_regressions"] += int(pts < previous)
    track["last_pts_s"] = pts
    packet_duration = packet.get("duration_time", "N/A")
    track["end_pts_s"] = round(pts + (float(packet_duration) if packet_duration != "N/A" else 0), 6)

with source.open("rb") as handle:
    sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
decoded = subprocess.run(
    ["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-loglevel", "level+info",
     "-xerror", "-threads", "2",
     *base, "-filter_threads", "1",
     "-vf", "scale=360:-2,format=gray,freezedetect=n=0.001:d=2",
     "-af", "silencedetect=n=-45dB:d=0.8,volumedetect",
     "-map", "0:v:0", "-map", "0:a:0", "-threads:v", "1", "-threads:a", "1",
     "-fps_mode", "passthrough", "-enc_time_base:v", "demux", "-f", "null", "-"],
    capture_output=True, text=True,
)
diagnostics = {}
for line in decoded.stderr.splitlines():
    matches = re.finditer(
        r"(silence_start|silence_end|silence_duration|freeze_start|freeze_end|"
        r"freeze_duration|mean_volume|max_volume|n_samples):\s*([-0-9.einf]+)",
        line,
    )
    for match in matches:
        key, value = match.groups()
        diagnostics.setdefault(key, []).append(value)

demuxer_error = bool(metadata.stderr.strip() or packets.stderr.strip() or packets.returncode)
decoder_error = bool(decoded.returncode or re.search(r"\[(?:error|fatal|panic)\]", decoded.stderr))
track_empty = any(track["last_pts_s"] is None for track in tracks.values())
decoded_to_eof = not (demuxer_error or decoder_error or track_empty)
report = {
    "sha256": sha256,
    "bytes": source.stat().st_size,
    "container_duration_s": media.get("format", {}).get("duration"),
    "tracks": list(tracks.values()),
    "decoded_to_eof": decoded_to_eof,
    "input_or_packet_error": demuxer_error,
    "decode_error": decoder_error,
    "track_without_timed_packets": track_empty,
    "ffmpeg_exit": decoded.returncode,
    "diagnostics": diagnostics,
    "measurement": {
        "silence": "threshold -45 dBFS, >=0.8 s",
        "freeze": "scaled grayscale width 360, threshold 0.001, >=2 s",
        "clock": "timestamps del archivo; no mapean automáticamente al reproductor",
        "auditory_observation": False,
    },
}
print(json.dumps(report, ensure_ascii=False, indent=2))
if not decoded_to_eof:
    raise SystemExit(1)
