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

MARKER="THIS-IS-A-TEST-MARKER-$(date +%s)"
echo "$MARKER" >> "$TMP/akos-copy/packs/personal/pau-avila/principles.md"

bash "$TMP/akos-copy/update.sh" >/tmp/update-test-out.$$ 2>&1 || true
grep -q "Not a git repository" /tmp/update-test-out.$$ \
  || fail "expected the no-git warning branch; update.sh's shape may have changed"
pass "update.sh correctly detected the non-git scratch copy"

grep -q "$MARKER" "$TMP/akos-copy/packs/personal/pau-avila/principles.md" \
  || fail "personal layer content was lost after running update.sh"
pass "personal layer marker survived a real update.sh run"

rm -f /tmp/update-test-out.$$
echo "PASS: test_update_preserves_personal.sh"
