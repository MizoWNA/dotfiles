#!/usr/bin/env bash
# Obsidian terminal greeting: centered banner + centered fastfetch card,
# responsive to terminal width (works fine tiled at half-width).
# Above the 2-column threshold, system info splits into two side-by-side
# columns (OS..TERM on the left, CPU..DISK on the right) for a nicer layout.

FF_DIR="$HOME/.config/fastfetch"
cols=$(tput cols 2>/dev/null || echo 80)

orange=$'\033[38;2;224;96;42m'
muted=$'\033[38;2;138;138;130m'
reset=$'\033[0m'

TWO_COLUMN_MIN=90

if (( cols >= TWO_COLUMN_MIN )); then
    banner_font="block"
elif (( cols >= 50 )); then
    banner_font="small"
else
    banner_font="mini"
fi

figlet -f "$banner_font" "WELCOME" \
    | while IFS= read -r line; do printf '%s%s%s\n' "$orange" "$line" "$reset"; done \
    | python3 "$FF_DIR/center.py" "$cols"

short_pwd="${PWD/#$HOME/~}"
printf '%s%s%s • %s%s%s\n' "$muted" "$USER" "$reset" "$muted" "$short_pwd" "$reset" \
    | python3 "$FF_DIR/center.py" "$cols"
echo

if (( cols >= TWO_COLUMN_MIN )); then
    tmp_left=$(mktemp)
    tmp_right=$(mktemp)
    trap 'rm -f "$tmp_left" "$tmp_right"' EXIT

    fastfetch --config "$FF_DIR/greeting-left.jsonc" > "$tmp_left"
    fastfetch --config "$FF_DIR/greeting-right.jsonc" > "$tmp_right"

    python3 "$FF_DIR/columns.py" "$tmp_left" "$tmp_right" \
        | python3 "$FF_DIR/center.py" "$cols"
else
    fastfetch --config "$FF_DIR/greeting.jsonc" \
        | python3 "$FF_DIR/center.py" "$cols"
fi

echo
fastfetch --config "$FF_DIR/greeting-colors.jsonc" \
    | python3 "$FF_DIR/center.py" "$cols"
