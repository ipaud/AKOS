#!/usr/bin/env bash
#
# install.sh — Install AKOS globally on this Mac.
# Idempotent. Verifies structure, chmods scripts, creates the ~/DEV symlink
# (if the repo lives elsewhere) and the ~/bin/akos symlink. Never destroys content.
#
set -uo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }

printf '%sInstalling AKOS%s from %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# 1. chmod scripts.
for s in install.sh update.sh doctor.sh uninstall.sh bin/akos; do
  if [ -f "$AKOS_HOME/$s" ]; then chmod +x "$AKOS_HOME/$s"; ok "chmod +x $s"; fi
done

# 2. Ensure ~/DEV/AKOS resolves. If the repo isn't already under ~/DEV,
#    create a ~/DEV symlink to its parent so the canonical path works.
canonical="$HOME/DEV/AKOS"
if [ -e "$canonical" ] || [ -L "$canonical" ]; then
  ok "~/DEV/AKOS already resolves"
else
  parent="$(dirname "$AKOS_HOME")"          # e.g. ~/Desktop/DEV
  if [ ! -e "$HOME/DEV" ]; then
    ln -s "$parent" "$HOME/DEV" && ok "symlinked ~/DEV → $parent"
  else
    warn "~/DEV exists but ~/DEV/AKOS does not; leaving it untouched (repo at $AKOS_HOME)"
  fi
fi

# 3. Create ~/bin and the akos symlink.
mkdir -p "$HOME/bin"
if [ -L "$HOME/bin/akos" ] || [ -e "$HOME/bin/akos" ]; then
  ln -sf "$AKOS_HOME/bin/akos" "$HOME/bin/akos" && ok "refreshed ~/bin/akos → $AKOS_HOME/bin/akos"
else
  ln -s "$AKOS_HOME/bin/akos" "$HOME/bin/akos" && ok "symlinked ~/bin/akos"
fi

# 4. PATH hint.
case ":$PATH:" in
  *":$HOME/bin:"*) ok "~/bin is on PATH" ;;
  *) warn "~/bin is not on PATH. Add:  export PATH=\"\$HOME/bin:\$PATH\"  to your shell profile." ;;
esac

# 5. Structure verification (non-fatal report).
printf '\n%sVerifying structure%s\n' "$c_bold" "$c_reset"
if bash "$AKOS_HOME/doctor.sh" >/tmp/akos_doctor.$$  2>&1; then
  ok "doctor: all checks passed"
else
  warn "doctor reported issues — run ./doctor.sh for detail"
fi
rm -f /tmp/akos_doctor.$$

# 6. Summary.
packs="$(find "$AKOS_HOME/packs" -mindepth 2 -maxdepth 2 -type d | wc -l | tr -d ' ')"
agents="$(find "$AKOS_HOME/agents" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
cat <<EOF

${c_bold}AKOS installed.${c_reset}
  Packs:   $packs
  Agents:  $agents
  CLI:     akos help   (via ~/bin/akos)

Next:
  akos doctor                  # health check
  cd <your-project> && akos install-project   # wire AKOS into a project
EOF
