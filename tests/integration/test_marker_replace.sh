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

# install-project accepts zero or one project directory, and never creates the
# project root on the caller's behalf.
if "$AKOS_HOME/bin/akos" install-project "$TMP/missing-project" >"$TMP/missing_out" 2>&1; then
  fail "install-project should reject a project directory that does not exist"
fi
[ ! -e "$TMP/missing-project" ] || fail "install-project created a missing project root"
grep -qi "existing project directory" "$TMP/missing_out" \
  || fail "missing-project failure did not explain the existing-directory requirement"
pass "install_project_requires_existing_root"

if "$AKOS_HOME/bin/akos" install-project "$TMP" extra >"$TMP/extra_out" 2>&1; then
  fail "install-project should reject extra positional arguments"
fi
grep -q "Usage: akos install-project" "$TMP/extra_out" \
  || fail "extra-argument failure did not print the exact command usage"
help_out="$("$AKOS_HOME/bin/akos" install-project --help)"
printf '%s' "$help_out" | grep -q "^Usage: akos install-project \\[project-dir\\]$" \
  || fail "install-project --help did not print its exact usage"
if "$AKOS_HOME/bin/akos" install-project --help extra >"$TMP/help_extra_out" 2>&1; then
  fail "install-project should reject arguments after --help"
fi

link_help_out="$("$AKOS_HOME/bin/akos" link-project --help)"
printf '%s' "$link_help_out" | grep -q "^Usage: akos link-project$" \
  || fail "link-project --help did not print its exact usage"
if "$AKOS_HOME/bin/akos" link-project "$TMP" >"$TMP/link_extra_out" 2>&1; then
  fail "link-project should reject a project argument; it is current-directory only"
fi
pass "install_project_has_exact_args_and_help"

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

# The explicit project root may itself be a symlink and is resolved once. No
# symlink is accepted below that trust boundary, including .gitignore.
REAL_ROOT="$TMP/real-project"
ROOT_ALIAS="$TMP/project-alias"
mkdir -p "$REAL_ROOT"
ln -s "$REAL_ROOT" "$ROOT_ALIAS"
"$AKOS_HOME/bin/akos" install-project "$ROOT_ALIAS" >/dev/null 2>&1 \
  || fail "install-project should resolve an explicit root symlink"
[ -f "$REAL_ROOT/.akos/config.md" ] || fail "resolved root did not receive the installation"
pass "install_project_resolves_explicit_root"

CHILD_LINK_ROOT="$TMP/child-link-project"
OUTSIDE_AKOS="$TMP/outside-akos"
mkdir -p "$CHILD_LINK_ROOT" "$OUTSIDE_AKOS"
ln -s "$OUTSIDE_AKOS" "$CHILD_LINK_ROOT/.akos"
if "$AKOS_HOME/bin/akos" install-project "$CHILD_LINK_ROOT" >"$TMP/child_link_out" 2>&1; then
  fail "install-project should reject a symlinked .akos child"
fi
[ ! -f "$CHILD_LINK_ROOT/CLAUDE.md" ] || fail "child symlink rejection happened after another target was written"
[ -z "$(find "$OUTSIDE_AKOS" -mindepth 1 -print -quit)" ] || fail "install-project wrote through the .akos symlink"
grep -qi "symlink" "$TMP/child_link_out" || fail "child symlink rejection was not explained"

GITIGNORE_LINK_ROOT="$TMP/gitignore-link-project"
OUTSIDE_GITIGNORE="$TMP/outside.gitignore"
mkdir -p "$GITIGNORE_LINK_ROOT"
printf 'outside\n' > "$OUTSIDE_GITIGNORE"
ln -s "$OUTSIDE_GITIGNORE" "$GITIGNORE_LINK_ROOT/.gitignore"
if "$AKOS_HOME/bin/akos" install-project "$GITIGNORE_LINK_ROOT" >"$TMP/gitignore_link_out" 2>&1; then
  fail "install-project should reject a symlinked .gitignore"
fi
[ ! -f "$GITIGNORE_LINK_ROOT/CLAUDE.md" ] || fail ".gitignore symlink rejection happened after managed files were written"
[ "$(cat "$OUTSIDE_GITIGNORE")" = "outside" ] || fail "install-project wrote through the .gitignore symlink"
pass "install_project_rejects_all_child_symlinks_before_writing"

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

# profile use must never follow repository-controlled child symlinks. Both
# cases point at a valid config so the old path-based extract/write flow would
# pass its existence check and overwrite the outside target.
PROFILE_LINK_OUTSIDE="$TMP/profile-link-outside"
mkdir -p "$PROFILE_LINK_OUTSIDE"
printf 'before\n<!-- AKOS:START -->\npersonal_profile: old-profile\n<!-- AKOS:END -->\nafter\n' \
  > "$PROFILE_LINK_OUTSIDE/config.md"
PROFILE_LINK_SNAPSHOT="$(cksum "$PROFILE_LINK_OUTSIDE/config.md")"

PROFILE_AKOS_LINK_ROOT="$TMP/profile-akos-link-project"
mkdir -p "$PROFILE_AKOS_LINK_ROOT"
ln -s "$PROFILE_LINK_OUTSIDE" "$PROFILE_AKOS_LINK_ROOT/.akos"
if "$AKOS_HOME/bin/akos" profile use pau-avila "$PROFILE_AKOS_LINK_ROOT" \
    >"$TMP/profile_akos_link_out" 2>&1; then
  fail "profile use should reject a symlinked .akos parent"
fi
[ "$(cksum "$PROFILE_LINK_OUTSIDE/config.md")" = "$PROFILE_LINK_SNAPSHOT" ] \
  || fail "profile use wrote through a symlinked .akos parent"
grep -qi "symlink" "$TMP/profile_akos_link_out" \
  || fail "profile use did not explain the symlinked .akos refusal"

PROFILE_CONFIG_LINK_ROOT="$TMP/profile-config-link-project"
mkdir -p "$PROFILE_CONFIG_LINK_ROOT/.akos"
ln -s "$PROFILE_LINK_OUTSIDE/config.md" "$PROFILE_CONFIG_LINK_ROOT/.akos/config.md"
if "$AKOS_HOME/bin/akos" profile use pau-avila "$PROFILE_CONFIG_LINK_ROOT" \
    >"$TMP/profile_config_link_out" 2>&1; then
  fail "profile use should reject a symlinked config.md leaf"
fi
[ "$(cksum "$PROFILE_LINK_OUTSIDE/config.md")" = "$PROFILE_LINK_SNAPSHOT" ] \
  || fail "profile use wrote through a symlinked config.md leaf"
grep -qi "symlink" "$TMP/profile_config_link_out" \
  || fail "profile use did not explain the symlinked config.md refusal"
pass "profile_use_rejects_project_child_symlinks"

# A path containing spaces must work end to end through the real CLI.
SPACES_DIR="$TMP/a project with spaces"
mkdir -p "$SPACES_DIR"
"$AKOS_HOME/bin/akos" install-project "$SPACES_DIR" >/dev/null 2>&1 \
  || fail "install-project failed on a path containing spaces"
grep -q "AKOS:START" "$SPACES_DIR/CLAUDE.md" || fail "AKOS section missing for a path containing spaces"
pass "paths_with_spaces_still_work"

echo "PASS: test_marker_replace.sh"
