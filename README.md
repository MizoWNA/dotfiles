# Obsidian rice — Arch + Hyprland

My daily-driver Hyprland setup: Waybar with a pill layout, Wofi/Rofi launchers,
Kitty, swaync notifications, and a centered fastfetch terminal greeting.
11 interchangeable Waybar/Wofi colour themes, hot-swappable with one keybind.

```
config/
  hypr/        Hyprland (split into modules/), hyprpaper, wallpaper script
  waybar/      bar config, style.css + styles/ (11 themes), scripts/
  wofi/        launcher config, style.css + themes/ (matching 11 themes)
  rofi/        rofi theme (config.rasi)
  kitty/       terminal config + colour schemes
  dunst/       dunstrc
  fastfetch/   terminal greeting (banner + responsive 1/2-column card)
  swaylock/    lockscreen
  htop/        htoprc
home/
  .zshrc       oh-my-zsh (bira theme) + fastfetch greeting hook
  .bashrc
```

## Install

```sh
git clone <this-repo> ~/rice
cd ~/rice
./install.sh          # symlinks config/* into ~/.config/ and home/* into ~
```

`install.sh` backs up anything it would overwrite to `~/.config-backup-<timestamp>/`.
It symlinks rather than copies, so `git pull` updates your live config.

## Dependencies

```sh
# core
sudo pacman -S hyprland waybar wofi rofi kitty dunst swaync swaylock \
               hyprpaper python python-psutil playerctl figlet fastfetch \
               nautilus htop zsh

# fonts
sudo pacman -S ttf-jetbrains-mono-nerd

# cursor theme (AUR)
yay -S bibata-cursor-theme

# oh-my-zsh (for home/.zshrc)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Hyprland plugins configured in `config/hypr/modules/plugins.conf` (install via
`hyprpm`, all optional — Hyprland ignores config for plugins you don't have):
`hyprexpo`, `hyprbars`, `hyprtrails`, `hyprscrolling`, `hyprgrass`,
`borders-plus-plus`, `split-monitor-workspaces`, `hyperfocus`.

## Read this before you apply it

- **`config/hypr/monitors.conf` is machine-specific.** Mine is a single 3840x2400
  laptop panel at scale 2:
  `monitor=eDP-1,3840x2400@60,0x0,2`
  Change it to `monitor=,preferred,auto,auto` (or your own output) or you'll get
  a wrong resolution / blank screen. Find your output name with `hyprctl monitors`.
- **The wallpaper** is set twice: `hyprpaper` (reads `config/hypr/hyprpaper.conf`)
  and `config/hypr/wallpaper.sh` (uses `awww`, from `exec-once` in
  `modules/autostart.conf`). Both point at the bundled `walls/obsidian.png`.
  Drop whichever one you don't want, and comment out its `exec-once` line.
- **`modules/autostart.conf` references `~/.config/hypr/scripts/gtk.sh`**, which
  isn't in this repo — Hyprland just logs a failed exec and carries on. Delete
  the line, or put your own GTK theme script there.
- `home/.zshrc` ends with two aliases for machine-specific helper scripts
  (`phonessh`, `fanctl`) that aren't part of this rice. Delete them.
- `config/swaylock/swaylock.config` points at a wallpaper under
  `/usr/share/backgrounds/`; `waybar/scripts/lock.sh` picks a random image from
  that directory. Point both at a directory you actually have.

## Keybinds (SUPER = mod)

| Bind | Action |
|---|---|
| `SUPER + Return` | kitty |
| `SUPER + E` | nautilus |
| `SUPER + R` | rofi (drun) |
| `SUPER + Q` | close window |
| `SUPER + V` | toggle floating |
| `SUPER + F` | fullscreen |
| `SUPER + P` | pseudo-tile |
| `SUPER + J` | toggle split |
| `SUPER + arrows` | move focus |
| `SUPER + 1-0` | switch workspace |
| `SUPER + SHIFT + 1-0` | move window to workspace |
| `SUPER + drag L/R` | move / resize window |
| `SUPER + SHIFT + M` | exit Hyprland |

## Theme switching

`waybar/scripts/theme.sh` cycles through the 11 styles, swapping both the Waybar
and the matching Wofi stylesheet, then restarts Waybar. The current index is kept
in `waybar/.current_style_index` (gitignored). Bind it to whatever you like:

```
bind = $mainMod, T, exec, ~/.config/waybar/scripts/theme.sh
```

## Waybar modules

Left pill: brand button (click → rofi) + workspaces.
Centre pill: media prev/play/next/info (`playerctl` via the `media_*.py` scripts).
Right: `sysstats.py` (RAM in the bar, CPU/iGPU/GPU in the tooltip) + a pill with
pulseaudio, network, battery and tray. Extra scripts in `waybar/scripts/`:
`power.sh`, `lock.sh`, `countdown/`, `todo/` (a small TUI todo list).

Note: `custom/sysstats` logs `argument not found` on start — the `tooltip-format`
uses a `{tooltip}` placeholder Waybar doesn't accept for custom modules. Harmless;
the tooltip still works off the script's JSON. Drop the `tooltip-format` line to
silence it.
