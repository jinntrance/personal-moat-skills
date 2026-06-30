#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SKILL_DIR/scripts/sleep_reminder.py"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$PLIST_DIR/com.codex.sleep-quality-coach.plist"
LOG_DIR="$HOME/Library/Logs/sleep-quality-coach"

mkdir -p "$PLIST_DIR" "$LOG_DIR"
if [ ! -f "$HOME/.config/sleep-quality-coach/config.json" ]; then
  python3 "$SCRIPT_PATH" --init-config
fi

cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.codex.sleep-quality-coach</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$SCRIPT_PATH</string>
    <string>--due</string>
  </array>
  <key>StartInterval</key>
  <integer>900</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$LOG_DIR/out.log</string>
  <key>StandardErrorPath</key>
  <string>$LOG_DIR/err.log</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl kickstart -k "gui/$(id -u)/com.codex.sleep-quality-coach"

echo "Installed $PLIST_PATH"
echo "Config: $HOME/.config/sleep-quality-coach/config.json"
