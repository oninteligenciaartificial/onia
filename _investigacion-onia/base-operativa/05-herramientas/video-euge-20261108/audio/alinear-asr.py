#!/usr/bin/env python3
"""Alinea un ASR privado con PTS y ventanas de contenido ya verificadas."""

import argparse
from bisect import bisect_right
import csv
import hashlib
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("asr", type=Path, help="JSON de asr-local.py")
parser.add_argument("audio_packets", type=Path, help="CSV ffprobe pts_time,duration_time de audio")
parser.add_argument("map", type=Path, help="Ventanas de contenido y offsets frente al reloj")
parser.add_argument("output", type=Path, help="JSON privado nuevo")
args = parser.parse_args()
raw = json.loads(args.asr.read_text())
alignment = json.loads(args.map.read_text())
if raw["source_sha256"] != alignment["capture_sha256"]:
    parser.error("El ASR y el mapa no corresponden al mismo WebM.")

pcm_starts = []
packet_pts = []
duration = 0.0
with args.audio_packets.open(newline="") as handle:
    for row in csv.reader(handle):
        if not row or not row[0]:
            continue
        packet_start, packet_duration = map(float, row[:2])
        pcm_starts.append(duration)
        packet_pts.append(packet_start)
        duration += packet_duration
if not pcm_starts or abs(duration - raw["audio_duration_s"]) > 0.1:
    parser.error("El total de paquetes no concuerda con el audio decodificado.")

def pts(seconds):
    index = max(0, bisect_right(pcm_starts, seconds) - 1)
    return packet_pts[index] + (seconds - pcm_starts[index])

windows = alignment["windows"]
ad_ranges = alignment["ad_or_boundary_exclusions_pts_s"]
source_max = alignment.get("source_max_s", float("inf"))
rows = []
excluded_count = 0
outside_count = 0
for segment in raw["segments"]:
    start = pts(segment["start_s"])
    end = pts(segment["end_s"])
    if any(start < right and end > left for left, right in ad_ranges):
        excluded_count += 1
        continue
    for index, window in enumerate(windows):
        left, right = window["pts_s"]
        if end <= left or start >= right:
            continue
        if (start < left and index != 0) or (end > right and index != len(windows) - 1):
            continue
        offset = sum(window["offset_s"]) / 2
        rows.append({
            **segment,
            "pts_start_s": round(start, 3),
            "pts_end_s": round(end, 3),
            "source_approx_start_s": round(min(source_max, max(0, max(start, left) - offset)), 1),
            "source_approx_end_s": round(min(source_max, max(0, min(end, right) - offset)), 1),
        })
        break
    else:
        outside_count += 1

content_gaps = []
for index in range(1, len(packet_pts)):
    previous_duration = pcm_starts[index] - pcm_starts[index - 1]
    previous_end = packet_pts[index - 1] + previous_duration
    next_start = packet_pts[index]
    gap = round(next_start - previous_end, 6)
    if gap >= 0.040 and any(
        left <= previous_end < next_start <= right
        for left, right in (window["pts_s"] for window in windows)
    ):
        content_gaps.append({"pts_s": [round(previous_end, 3), next_start], "duration_s": gap})

summary = {
    "source_sha256": raw["source_sha256"],
    "source_id": alignment["source_id"],
    "audio_packets_csv_sha256": hashlib.sha256(args.audio_packets.read_bytes()).hexdigest(),
    "source_map_sha256": hashlib.sha256(args.map.read_bytes()).hexdigest(),
    "private_asr_sha256": hashlib.sha256(args.asr.read_bytes()).hexdigest(),
    "pcm_duration_s": raw["audio_duration_s"],
    "pcm_to_pts_final_delta_s": round(packet_pts[-1] - pcm_starts[-1], 3),
    "audio_pts_gaps_at_least_40ms_within_content": content_gaps,
    "asr_segments_total": len(raw["segments"]),
    "asr_segments_content": len(rows),
    "asr_segments_excluded_ad_or_boundary": excluded_count,
    "asr_segments_outside_content": outside_count,
    "first_content_approx_s": rows[0]["source_approx_start_s"] if rows else None,
    "last_content_approx_s": rows[-1]["source_approx_end_s"] if rows else None,
    "auditory_observation": False,
}
os.umask(0o077)
with args.output.open("x", encoding="utf-8") as handle:
    json.dump({**summary, "segments": rows}, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
print(json.dumps(summary, ensure_ascii=False, indent=2))
