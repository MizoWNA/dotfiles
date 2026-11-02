#!/usr/bin/env python3
import json
import subprocess


def pc(*args):
    r = subprocess.run(["playerctl", *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def fmt_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


status = pc("status")

if status != "Playing":
    now = subprocess.run(["date", "+%H:%M:%S"], capture_output=True, text=True).stdout.strip()
    print(json.dumps({"text": now, "tooltip": "No media playing", "class": "clock"}))
else:
    title = pc("metadata", "title") or "Unknown"
    artist = pc("metadata", "artist")

    try:
        position = float(pc("position") or 0)
    except ValueError:
        position = 0.0

    length_raw = pc("metadata", "mpris:length")
    try:
        length = float(length_raw) / 1_000_000 if length_raw else 0.0
    except ValueError:
        length = 0.0

    bar_width = 12
    filled = int((position / length) * bar_width) if length > 0 else 0
    filled = max(0, min(bar_width, filled))
    bar = "─" * filled + "●" + "─" * (bar_width - filled)

    label = title if len(title) <= 28 else title[:27] + "…"
    text = f"{label}  {bar}  {fmt_time(position)}"
    tooltip = f"{title} — {artist}" if artist else title

    print(json.dumps({"text": text, "tooltip": tooltip, "class": "playing"}))
