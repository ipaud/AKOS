#!/usr/bin/env bash
# update.sh must never lose packs/personal/ content — runs the REAL script
# against a scratch COPY of the repo (never the real one), with .git
# removed so it exercises the "not a git repository" branch, which still
# runs the backup/restore logic unconditionally.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

cp -R "$AKOS_HOME" "$TMP/akos-copy"
rm -rf "$TMP/akos-copy/.git"

# Scratch HOME: update.sh writes its durable backup under $HOME/.akos-backups,
# and the test must not touch the real one. Output goes in $TMP, not a
# predictable /tmp name (CWE-377, and it leaked on early exit).
export HOME="$TMP/home"
mkdir -p "$HOME"
OUT="$TMP/update-out"

MARKER="THIS-IS-A-TEST-MARKER-$(date +%s)"
echo "$MARKER" >> "$TMP/akos-copy/packs/personal/pau-avila/principles.md"

bash "$TMP/akos-copy/update.sh" >"$OUT" 2>&1 || true
grep -q "Not a git repository" "$OUT" \
  || fail "expected the no-git warning branch; update.sh's shape may have changed"
pass "update.sh correctly detected the non-git scratch copy"

grep -q "$MARKER" "$TMP/akos-copy/packs/personal/pau-avila/principles.md" \
  || fail "personal layer content was lost after running update.sh"
pass "personal layer marker survived a real update.sh run"

backup_dir="$(find "$HOME/.akos-backups" -maxdepth 1 -type d -name 'personal-*' | head -1)"
[ -n "$backup_dir" ] || fail "no durable backup was created under \$HOME/.akos-backups"
grep -q "$MARKER" "$backup_dir/pau-avila/principles.md" \
  || fail "the durable backup does not contain the personal content"
pass "durable backup created under \$HOME/.akos-backups with the personal content"

echo "PASS: test_update_preserves_personal.sh"
