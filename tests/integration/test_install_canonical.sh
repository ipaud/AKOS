#!/usr/bin/env bash
# Global install owns one canonical leaf, ~/DEV/AKOS. It must not replace a
# foreign collision and must fail before installing the other HOME links.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

cp -R "$AKOS_HOME" "$TMP/akos-copy"
COPY="$TMP/akos-copy"
export HOME="$TMP/home"
mkdir -p "$HOME"

bash "$COPY/install.sh" >"$TMP/fresh_out" 2>&1 \
  || fail "fresh install failed: $(tail -3 "$TMP/fresh_out")"
[ -d "$HOME/DEV" ] && [ ! -L "$HOME/DEV" ] || fail "fresh install should create a real ~/DEV directory"
[ -L "$HOME/DEV/AKOS" ] || fail "fresh install did not create the canonical ~/DEV/AKOS leaf symlink"
[ "$(readlink "$HOME/DEV/AKOS")" = "$COPY" ] || fail "canonical leaf points somewhere other than this checkout"
"$HOME/DEV/AKOS/install.sh" >"$TMP/canonical_rerun_out" 2>&1 \
  || fail "install invoked through the canonical leaf was not idempotent"
[ "$(readlink "$HOME/DEV/AKOS")" = "$COPY" ] \
  || fail "canonical rerun changed the owned leaf target"
pass "fresh install creates canonical leaf symlink"

rm -rf "$HOME"
mkdir -p "$HOME/DEV" "$TMP/foreign"
ln -s "$TMP/foreign" "$HOME/DEV/AKOS"
if bash "$COPY/install.sh" >"$TMP/collision_out" 2>&1; then
  fail "install should fail on a foreign canonical collision"
fi
[ "$(readlink "$HOME/DEV/AKOS")" = "$TMP/foreign" ] || fail "foreign canonical symlink was replaced"
[ ! -e "$HOME/bin/akos" ] || fail "install continued mutating HOME after canonical collision"
grep -qi "foreign.*~/DEV/AKOS\\|~/DEV/AKOS.*foreign\\|collision" "$TMP/collision_out" \
  || fail "canonical collision failure was not explained"
pass "foreign canonical collision fails before other HOME mutations"

echo "PASS: test_install_canonical.sh"
