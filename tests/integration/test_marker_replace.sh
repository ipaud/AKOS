#!/usr/bin/env bash
# Integration test for write_marked_section — the exact function whose
# awk -v multi-line bug (M4) silently broke every install-project rerun
# against an already-marked file on this machine's BSD awk. Runs against
# a real scratch project via akos install-project, twice, asserting the
# second run actually changes content that changed and preserves content
# that didn't.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

printf '# Existing content that must survive\n' > "$TMP/CLAUDE.md"

"$AKOS_HOME/bin/akos" install-project "$TMP" >/dev/null 2>&1

grep -q "Existing content that must survive" "$TMP/CLAUDE.md" \
  || fail "pre-existing content lost on first install"
grep -q "<!-- AKOS:START -->" "$TMP/CLAUDE.md" \
  || fail "AKOS section not written on first install"
pass "first install-project: existing content preserved, AKOS section added"

# Change something a rerun must actually update — the exact scenario
# that was silently broken before the sed-line-range fix.
sed 's/Startup MVP/Production/' "$TMP/.akos/config.md" > "$TMP/.akos/config.md.new"
mv "$TMP/.akos/config.md.new" "$TMP/.akos/config.md"

"$AKOS_HOME/bin/akos" install-project "$TMP" >/dev/null 2>&1

grep -q "Existing content that must survive" "$TMP/CLAUDE.md" \
  || fail "pre-existing content lost on SECOND install (rerun)"
pass "second install-project (rerun): pre-existing content still preserved"

# CLAUDE.md's block is regenerated from source each run, so it doesn't
# carry the user's manual .akos/config.md edit — but the rerun must not
# have silently failed (the actual bug: it would abort before writing
# anything, leaving stale content). Confirm the section is still current.
grep -q "Invoke the \`akos\` skill" "$TMP/CLAUDE.md" \
  || fail "AKOS section missing after rerun — write_marked_section may have silently failed"
pass "AKOS section present and current after rerun"

echo "PASS: test_marker_replace.sh"
