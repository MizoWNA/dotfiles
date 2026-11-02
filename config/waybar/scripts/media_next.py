#!/usr/bin/env python3
import json
import subprocess

status = subprocess.run(["playerctl", "status"], capture_output=True, text=True).stdout.strip()
text = "⏭" if status == "Playing" else ""
print(json.dumps({"text": text, "tooltip": "Next"}))
