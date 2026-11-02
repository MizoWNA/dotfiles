#!/usr/bin/env python3
"""Center a block of text (optionally containing ANSI SGR color codes and
fastfetch's absolute cursor-jump key alignment, ESC[nG) within the current
terminal width. Reads lines from stdin, writes centered lines to stdout.

ESC[nG (jump to absolute column n) is converted to relative spaces first,
since blindly left-padding a line containing an absolute jump would make
the jump land at the wrong column and break alignment.
"""
import os
import re
import shutil
import sys

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


def main():
    cols = shutil.get_terminal_size((80, 24)).columns
    if len(sys.argv) > 1:
        try:
            cols = int(sys.argv[1])
        except ValueError:
            pass

    lines = [derelativize(l.rstrip("\n")) for l in sys.stdin]
    max_len = max((visual_len(l) for l in lines), default=0)
    pad = max(0, (cols - max_len) // 2)

    for line in lines:
        sys.stdout.write(" " * pad + line + "\n")


if __name__ == "__main__":
    main()
