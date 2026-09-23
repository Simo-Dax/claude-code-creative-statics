#!/usr/bin/env bash
# Copyright (c) 2026 Simone Dassereto. All rights reserved. See LICENSE.
# Route A - rasterizza ogni .html del batch in PNG 1080x1350 con Chrome headless.
# Uso: ./render.sh [batch_dir] [WxH]   (default: cartella corrente, 1080x1350)
set -euo pipefail
DIR="${1:-.}"
SIZE="${2:-1080,1350}"

find_chrome() {
  [ -n "${CHROME_BIN:-}" ] && { echo "$CHROME_BIN"; return; }
  for c in chromium chromium-browser google-chrome google-chrome-stable; do
    command -v "$c" >/dev/null && { echo "$c"; return; }
  done
  local mac="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  [ -x "$mac" ] && { echo "$mac"; return; }
  return 1
}
CHROME="$(find_chrome)" || { echo "Chrome/Chromium non trovato - imposta CHROME_BIN"; exit 1; }

EXTRA=(--disable-dev-shm-usage)
[ "$(id -u)" = "0" ] && EXTRA+=(--no-sandbox)

cd "$DIR"
shopt -s nullglob
for f in *.html; do
  "$CHROME" "${EXTRA[@]}" --headless=new --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size="$SIZE" \
    --screenshot="${f%.html}.png" "file://$PWD/$f" 2>/dev/null
  echo "rendered ${f%.html}.png"
done
