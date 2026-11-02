#!/usr/bin/env bash
# Symlink this rice into place, backing up whatever is already there.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP="$HOME/.config-backup-$(date +%Y%m%d_%H%M%S)"

link() {
    local src="$1" dest="$2"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
        mkdir -p "$BACKUP"
        mv "$dest" "$BACKUP/"
        echo "  backed up $dest -> $BACKUP/"
    fi
    mkdir -p "$(dirname "$dest")"
    ln -s "$src" "$dest"
    echo "  linked $dest"
}

echo "Linking ~/.config entries:"
for dir in "$REPO"/config/*; do
    link "$dir" "$HOME/.config/$(basename "$dir")"
done

echo "Linking home dotfiles:"
for f in "$REPO"/home/.*; do
    base="$(basename "$f")"
    [ "$base" = "." ] || [ "$base" = ".." ] && continue
    link "$f" "$HOME/$base"
done

chmod +x "$REPO"/config/hypr/wallpaper.sh \
         "$REPO"/config/fastfetch/greeting.sh \
         "$REPO"/config/waybar/scripts/*.sh \
         "$REPO"/config/waybar/scripts/*/*.sh 2>/dev/null || true

[ -d "$BACKUP" ] && echo && echo "Previous config backed up to: $BACKUP"
echo
echo "Done. Edit config/hypr/monitors.conf for your display, then re-login to Hyprland."
