#!/usr/bin/env python3
import glob
import json
import subprocess
import time


def cpu_times():
    with open("/proc/stat") as f:
        parts = f.readline().split()[1:]
    nums = list(map(int, parts))
    idle = nums[3] + nums[4]
    total = sum(nums)
    return idle, total


def ram_percent():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            info[k] = int(v.strip().split()[0])
    total = info["MemTotal"]
    avail = info.get("MemAvailable", total)
    return round((total - avail) / total * 100)


def gpu_amd():
    for p in glob.glob("/sys/class/drm/card*/device/gpu_busy_percent"):
        try:
            with open(p) as f:
                return int(f.read().strip())
        except Exception:
            continue
    return 0


def gpu_nvidia():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=1,
        ).stdout.strip()
        return int(out.splitlines()[0]) if out else 0
    except Exception:
        return 0


idle1, total1 = cpu_times()
time.sleep(0.15)
idle2, total2 = cpu_times()
total_delta = total2 - total1
cpu = round((1 - (idle2 - idle1) / total_delta) * 100) if total_delta else 0

tooltip = f"CPU  {cpu}%\niGPU {gpu_amd()}%\nGPU  {gpu_nvidia()}%"
print(json.dumps({"text": f"RAM {ram_percent()}%", "tooltip": tooltip}))
