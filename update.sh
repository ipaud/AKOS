#!/usr/bin/env bash
#
# update.sh — Update AKOS safely.
# Manifest-backed backup/verify/restore of the personal layer
# (packs/personal/) around a `git pull --ff-only`. The personal layer is
# NEVER silently changed by an update — even a legitimate upstream commit to
# the shipped default profile is treated as drift and restored to the
# pre-update snapshot, because "personal" means it's the operator's layer to
# change, not update.sh's. A failed backup, a failed restore, a failed pull,
# a non-git checkout, or a failing final doctor.sh all make this script exit
# non-zero — "Update complete" is only ever printed after every one of those
# has been checked, not assumed.
#
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=bin/akos-common.sh
source "$AKOS_HOME/bin/akos-common.sh"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*"; }

printf '%sUpdating AKOS%s at %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# Mandatory before touching the lock, backup, or pull.
require_python || exit 1

PLI="$AKOS_HOME/bin/personal_layer_integrity.py"
PERSONAL="$AKOS_HOME/packs/personal"
overall_rc=0

# --- Concurrency guard ---
# `mkdir` is atomic — two concurrent updates racing on the same
# backup/restore/pull sequence could otherwise interleave in ways neither
# run's own logic accounts for. Released on every exit path via trap.
LOCK="$AKOS_HOME/.akos-update.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  fail "another update.sh is already running (lock held at $LOCK)."
  fail "If you're sure none is actually running, remove that directory and re-run."
  exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

# --- Backup + manifest, verified immediately ---
# Durable location, not mktemp: macOS periodically purges /var/folders, and a
# recovery path the user must scroll back through terminal output to find, in
# a directory that may be gone, is not a backup. Timestamp + random suffix
# (never PID/ms alone) so two updates in the same second never collide,
# mirroring schemas/history.py's own id scheme. A failed backup, or a backup
# that fails its own immediate verify against the live source, ABORTS the
# update before git is ever touched.
backup=""
manifest=""
if [ -d "$PERSONAL" ]; then
  suffix="$("$AKOS_PYTHON" -c 'import secrets; print(secrets.token_hex(4))')"
  backup="$HOME/.akos-backups/personal-$(date -u +%Y%m%dT%H%M%SZ)-${suffix}"
  manifest="${backup}.manifest.json"
  if ! "$AKOS_PYTHON" "$PLI" backup --source "$PERSONAL" --dest "$backup"; then
    fail "could not back up $PERSONAL to $backup — aborting update; nothing was pulled"
    exit 1
  fi
  if ! "$AKOS_PYTHON" "$PLI" verify --manifest "$manifest" --against "$PERSONAL" >/dev/null 2>&1; then
    fail "backup at $backup does not verify against $PERSONAL immediately after backup — aborting update; nothing was pulled"
    exit 1
  fi
  ok "backed up personal layer to $backup (verified)"
fi

# --- Update the source tree ---
pull_failed=0
no_git=0
if [ -d "$AKOS_HOME/.git" ]; then
  before="$(git -C "$AKOS_HOME" rev-parse HEAD 2>/dev/null || echo none)"
  if git -C "$AKOS_HOME" pull --ff-only 2>/dev/null; then
    after="$(git -C "$AKOS_HOME" rev-parse HEAD 2>/dev/null || echo none)"
    if [ "$before" != "$after" ]; then
      printf '\n%sChanged files:%s\n' "$c_bold" "$c_reset"
      git -C "$AKOS_HOME" diff --name-only "$before" "$after" | sed 's/^/  /'
    else
      ok "already up to date"
    fi
  else
    warn "git pull failed (local changes or not fast-forwardable)."
    pull_failed=1
  fi
else
  warn "Not a git repository — no automatic update source configured."
  warn "To update: replace core/, packs/ (except packs/personal/), agents/, etc. from a fresh copy, then re-run ./install.sh."
  no_git=1
fi

# --- Personal layer: verify unchanged, or restore and say so ---
# Unconditional — runs whether the pull succeeded, failed, or there was no
# git repo at all. "personal layer preserved" is never printed without this
# check having actually run.
if [ -n "$backup" ]; then
  if "$AKOS_PYTHON" "$PLI" verify --manifest "$manifest" --against "$PERSONAL" >/dev/null 2>&1; then
    ok "personal layer verified unchanged"
  else
    warn "personal layer drifted from its pre-update snapshot — restoring"
    if "$AKOS_PYTHON" "$PLI" restore --backup "$backup" --manifest "$manifest" --dest "$PERSONAL"; then
      ok "personal layer restored and verified"
    else
      fail "personal layer restore FAILED — manual recovery needed. Backup preserved at $backup"
      overall_rc=1
    fi
  fi
fi

# Re-chmod in case new scripts arrived.
for s in install.sh update.sh doctor.sh uninstall.sh merge-pr.sh bin/akos; do
  if [ -f "$AKOS_HOME/$s" ]; then chmod +x "$AKOS_HOME/$s"; fi
done

if [ "$pull_failed" -eq 1 ] || [ "$no_git" -eq 1 ]; then
  overall_rc=1
fi

# --- Final verification: doctor.sh must actually run and pass ---
# Only meaningful when nothing above already failed — a failed backup/pull
# means the source tree and/or personal layer are in a state doctor.sh
# either can't usefully assess yet or would report on stale grounds.
printf '\n%sFinal verification%s\n' "$c_bold" "$c_reset"
if [ "$overall_rc" -eq 0 ]; then
  doctor_rc=0
  bash "$AKOS_HOME/doctor.sh" || doctor_rc=$?
  if [ "$doctor_rc" -ne 0 ]; then
    fail "doctor.sh reported failures after update (exit $doctor_rc) — see above."
    overall_rc=1
  fi
else
  warn "skipped — an earlier step already failed (see above)"
fi

printf '\n'
if [ "$overall_rc" -eq 0 ]; then
  ok "Update complete and verified."
else
  fail "Update did NOT complete cleanly — see the failures above before trusting this install."
fi

exit "$overall_rc"
