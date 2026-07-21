#!/usr/bin/env bash
#
# update.sh — Update AKOS safely.
# Preserves the personal layer (packs/personal/). If this is a git repo,
# pulls and reports changed files. Otherwise reports that manual update is needed.
# Never deletes personal packs.
#
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*"; }

printf '%sUpdating AKOS%s at %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

PERSONAL="$AKOS_HOME/packs/personal"

# Always back up the personal layer before any update operation.
# Durable location, not mktemp: macOS periodically purges /var/folders, and a
# recovery path the user must scroll back through terminal output to find, in
# a directory that may be gone, is not a backup. A failed backup ABORTS the
# update — proceeding after printing "backed up" was the data-loss path.
backup=""
if [ -d "$PERSONAL" ]; then
  backup="$HOME/.akos-backups/personal-$(date +%Y%m%dT%H%M%S)"
  mkdir -p "$(dirname "$backup")"
  if ! cp -R "$PERSONAL" "$backup"; then
    fail "could not back up $PERSONAL to $backup — aborting update"
    exit 1
  fi
  ok "backed up personal layer to $backup"
fi

restore_personal() {
  if [ -n "$backup" ] && [ -d "$backup" ]; then
    # Only restore files that were removed/changed by the update — never
    # clobber a newer personal file the user may have edited post-backup.
    cp -Rn "$backup/." "$PERSONAL/" 2>/dev/null || true
    ok "personal layer preserved"
  fi
}

if [ -d "$AKOS_HOME/.git" ]; then
  before="$(git -C "$AKOS_HOME" rev-parse HEAD 2>/dev/null || echo none)"
  if git -C "$AKOS_HOME" pull --ff-only 2>/dev/null; then
    after="$(git -C "$AKOS_HOME" rev-parse HEAD 2>/dev/null || echo none)"
    restore_personal
    if [ "$before" != "$after" ]; then
      printf '\n%sChanged files:%s\n' "$c_bold" "$c_reset"
      git -C "$AKOS_HOME" diff --name-only "$before" "$after" | sed 's/^/  /'
    else
      ok "already up to date"
    fi
  else
    warn "git pull failed (local changes or not fast-forwardable). Personal layer left intact."
    restore_personal
  fi
else
  warn "Not a git repository — no automatic update source configured."
  warn "To update: replace core/, packs/ (except packs/personal/), agents/, etc. from a fresh copy, then re-run ./install.sh."
  restore_personal
fi

# Re-chmod in case new scripts arrived.
for s in install.sh update.sh doctor.sh uninstall.sh merge-pr.sh bin/akos; do
  if [ -f "$AKOS_HOME/$s" ]; then chmod +x "$AKOS_HOME/$s"; fi
done

printf '\n'
ok "Update complete. Run ./doctor.sh to verify."
