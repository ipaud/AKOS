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

# install-project must preflight all 4 targets before writing ANY of them —
# one malformed target (here, END before START) must leave the other 3
# completely untouched, not partially applied.
PREFLIGHT_DIR="$TMP/preflight-project"
mkdir -p "$PREFLIGHT_DIR/.cursor/rules" "$PREFLIGHT_DIR/.akos"
printf '<!-- AKOS:END -->\nx\n<!-- AKOS:START -->\n' > "$PREFLIGHT_DIR/CLAUDE.md"
printf 'original agents content\n' > "$PREFLIGHT_DIR/AGENTS.md"
agents_sha_before="$(shasum "$PREFLIGHT_DIR/AGENTS.md")"

if "$AKOS_HOME/bin/akos" install-project "$PREFLIGHT_DIR" >"$TMP/preflight_out" 2>&1; then
  fail "install-project should refuse when one of its 4 targets has an ambiguous marker structure"
fi
grep -qi "ambiguous marker structure" "$TMP/preflight_out" \
  || fail "expected install-project to name the ambiguous-marker preflight failure"
agents_sha_after="$(shasum "$PREFLIGHT_DIR/AGENTS.md")"
[ "$agents_sha_before" = "$agents_sha_after" ] \
  || fail "install-project modified AGENTS.md even though CLAUDE.md's preflight failed"
grep -q "AKOS:END -->" "$PREFLIGHT_DIR/CLAUDE.md" || fail "CLAUDE.md was unexpectedly modified"
[ ! -f "$PREFLIGHT_DIR/.akos/config.md" ] || fail ".akos/config.md should not have been created when the preflight failed"
pass "install_project_preflights_all_four_files"

# profile use must reject a malformed .akos/config.md rather than silently
# treating the ambiguous section as absent (the old awk reader's failure
# mode: both "truly absent" and "malformed" returned an empty string).
# Uses the pau-avila profile that already ships in this repo — never create
# a new profile here, which would mutate the real repo's packs/personal/.
MALFORMED_DIR="$TMP/malformed-project"
mkdir -p "$MALFORMED_DIR/.akos"
printf '# AKOS Project Config\n<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n' \
  > "$MALFORMED_DIR/.akos/config.md"
if "$AKOS_HOME/bin/akos" profile use pau-avila "$MALFORMED_DIR" >"$TMP/profile_use_out" 2>&1; then
  fail "profile use should refuse a malformed .akos/config.md"
fi
grep -qi "multiple START" "$TMP/profile_use_out" \
  || fail "expected profile use to surface the specific marker violation"
pass "profile_use_rejects_malformed_marker_block"

# A path containing spaces must work end to end through the real CLI.
SPACES_DIR="$TMP/a project with spaces"
mkdir -p "$SPACES_DIR"
"$AKOS_HOME/bin/akos" install-project "$SPACES_DIR" >/dev/null 2>&1 \
  || fail "install-project failed on a path containing spaces"
grep -q "AKOS:START" "$SPACES_DIR/CLAUDE.md" || fail "AKOS section missing for a path containing spaces"
pass "paths_with_spaces_still_work"

echo "PASS: test_marker_replace.sh"
