#!/usr/bin/env python3
"""Merge two fastfetch outputs into side-by-side columns, preserving
color codes and correctly accounting for fastfetch's absolute cursor-jump
key alignment (ESC[nG) when measuring/padding column widths."""
import re
import sys
from pathlib import Path

SGR = re.compile(r"\x1b\[[0-9;]*m")
CSI = re.compile(r"\x1b\[([0-9;]*)([a-zA-Z])")


def derelativize(line: str) -> str:
    out = []
    pos = 0
    i = 0
    for m in CSI.finditer(line):
        out.append(line[i:m.start()])
        pos += len(line[i:m.start()])
        i = m.end()
        if m.group(2) == "G" and m.group(1):
            target = int(m.group(1).split(";")[0]) - 1
            if target > pos:
                out.append(" " * (target - pos))
                pos = target
        else:
            out.append(m.group(0))
    out.append(line[i:])
    return "".join(out)


def visual_len(line: str) -> int:
    return len(SGR.sub("", line))


def read_block(path: str):
    return [derelativize(l) for l in Path(path).read_text().splitlines()]


def main():
    left_path, right_path = sys.argv[1], sys.argv[2]
    gap = int(sys.argv[3]) if len(sys.argv) > 3 else 6

    left = read_block(left_path)
    right = read_block(right_path)

    left_width = max((visual_len(l) for l in left), default=0)
    rows = max(len(left), len(right))
    left += [""] * (rows - len(left))
    right += [""] * (rows - len(right))

    for l, r in zip(left, right):
        pad = left_width - visual_len(l)
        sys.stdout.write(l + " " * pad + " " * gap + r + "\n")


if __name__ == "__main__":
    main()
