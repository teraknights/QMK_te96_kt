#!/usr/bin/env bash
# Build te96 (rev1_inverted) firmware from this repo's keymaps.
# Usage: scripts/build.sh [via|via_custom|mapcheck]   (default: all)
# Requires: avr-gcc / avr-libc, python3, git, make
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
QMK_DIR="${QMK_DIR:-$REPO_DIR/.qmk_e3w2q}"
FORK_URL="https://github.com/e3w2q/qmk_firmware.git"
FORK_COMMIT="228a26bf181e6dc89e1cbb8233984621ae8d5b63"   # e3w2q branch, 2021-12-11
KB="e3w2q/te96/rev1_inverted"

if [ ! -d "$QMK_DIR/.git" ]; then
  git clone --depth 1 -b e3w2q "$FORK_URL" "$QMK_DIR"
  git -C "$QMK_DIR" submodule update --init --depth 1 lib/lufa lib/printf lib/vusb
fi
test "$(git -C "$QMK_DIR" rev-parse HEAD)" = "$FORK_COMMIT" || echo "warning: fork HEAD differs from $FORK_COMMIT" >&2

# Old QMK CLI needs an isolated venv (old jsonschema / milc); 'halo' is stubbed.
VENV="$REPO_DIR/.venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q appdirs argcomplete colorama dotty-dict hjson "jsonschema<4.18" pygments spinners log_symbols termcolor
  "$VENV/bin/pip" install -q --no-deps "milc==1.4.2"
  SP="$("$VENV/bin/python" -c 'import site;print(site.getsitepackages()[0])')"
  mkdir -p "$SP/halo"
  printf 'class Halo:\n    def __init__(s,*a,**k): pass\n    def __getattr__(s,n): return lambda *a,**k: s\n    def __enter__(s): return s\n    def __exit__(s,*a): pass\n' > "$SP/halo/__init__.py"
fi
# shellcheck disable=SC1091
. "$VENV/bin/activate"

KEYMAPS=("$@"); [ ${#KEYMAPS[@]} -eq 0 ] && KEYMAPS=(via via_custom mapcheck)
mkdir -p "$REPO_DIR/firmware"
for km in "${KEYMAPS[@]}"; do
  rm -rf "$QMK_DIR/keyboards/$KB/keymaps/$km"
  cp -r "$REPO_DIR/keymaps/$km" "$QMK_DIR/keyboards/$KB/keymaps/$km"
  make -C "$QMK_DIR" "$KB:$km"
  cp "$QMK_DIR/e3w2q_te96_rev1_inverted_$km.hex" "$REPO_DIR/firmware/te96_$km.hex"
done
