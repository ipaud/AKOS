#!/usr/bin/env bash
# merge-pr.sh exists because PR #3 merged red (see the script's own header
# comment): mergeable was checked, checks were not. It had zero tests of its
# own before this file — this exercises every documented exit state (0
# merged/dry-run-clean, 1 usage/precondition, 2 refused-checks-not-green)
# against fake `gh` and `git` binaries, never the real GitHub API or the
# real git remote.
set -euo pipefail

AKOS_HOME="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MERGE_PR="$AKOS_HOME/merge-pr.sh"
# Resolved once, up front: several scenarios below restrict PATH down to
# just the fake-binary directory, and a bare `bash` word would otherwise
# fail to resolve through that same restricted PATH.
BASH_BIN="$(command -v bash)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

FAKE_BIN="$TMP/bin"
mkdir -p "$FAKE_BIN"

# Fake `gh`. Behavior is entirely env-var driven so each scenario below can
# set exactly the response it needs without a fixture file per case.
#   FAKE_GH_STATE           - `gh pr view --json state --jq .state` output.
#                              "FAIL" makes the view call itself fail (exit 1,
#                              no output) — simulates a bad PR number or an
#                              unauthenticated gh, which must not read as "no
#                              failing checks".
#   FAKE_GH_CHECKS_OUTPUT   - text `gh pr checks` prints.
#   FAKE_GH_CHECKS_RC       - exit code `gh pr checks` returns.
#   FAKE_GH_DEFAULT_BRANCH  - `gh repo view --json defaultBranchRef` output.
#   FAKE_GH_LOG             - every invocation's argv, one line each, so a
#                              scenario can assert the exact merge strategy
#                              and --delete-branch were passed, or that
#                              `pr merge` was never called at all (dry-run).
cat > "$FAKE_BIN/gh" <<'FAKE_GH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${FAKE_GH_LOG:-/dev/null}"
if [ "$1" = "pr" ] && [ "$2" = "view" ]; then
  [ "${FAKE_GH_STATE:-FAIL}" = "FAIL" ] && exit 1
  printf '%s\n' "$FAKE_GH_STATE"
  exit 0
fi
if [ "$1" = "pr" ] && [ "$2" = "checks" ]; then
  printf '%s\n' "${FAKE_GH_CHECKS_OUTPUT:-}"
  exit "${FAKE_GH_CHECKS_RC:-0}"
fi
if [ "$1" = "pr" ] && [ "$2" = "merge" ]; then
  exit "${FAKE_GH_MERGE_RC:-0}"
fi
if [ "$1" = "repo" ] && [ "$2" = "view" ]; then
  printf '%s\n' "${FAKE_GH_DEFAULT_BRANCH:-main}"
  exit 0
fi
exit 0
FAKE_GH
chmod +x "$FAKE_BIN/gh"

# Fake `git`. Only the four calls merge-pr.sh actually makes after a merge
# (current branch, tag existence, tag creation, push) are meaningful; the
# real repo and remote are never touched.
#   FAKE_GIT_BRANCH      - `rev-parse --abbrev-ref HEAD` output.
#   FAKE_GIT_TAG_EXISTS   - "1" makes `rev-parse vX.Y.Z` succeed (tag exists).
#   FAKE_GIT_LOG          - every invocation's argv, one line each.
cat > "$FAKE_BIN/git" <<'FAKE_GIT'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${FAKE_GIT_LOG:-/dev/null}"
if [ "$1" = "rev-parse" ] && [ "$2" = "--abbrev-ref" ]; then
  printf '%s\n' "${FAKE_GIT_BRANCH:-main}"
  exit 0
fi
if [ "$1" = "rev-parse" ]; then
  [ "${FAKE_GIT_TAG_EXISTS:-0}" = "1" ] && { echo deadbeef; exit 0; }
  exit 1
fi
exit 0
FAKE_GIT
chmod +x "$FAKE_BIN/git"

WORKDIR="$TMP/workdir"
mkdir -p "$WORKDIR"
printf '1.2.3\n' > "$WORKDIR/VERSION"
printf '## [1.2.3] — 2026-01-01\n\nstuff\n' > "$WORKDIR/CHANGELOG.md"

run() {
  # run <pr-args...> — invokes merge-pr.sh with the fakes on PATH, from
  # WORKDIR, capturing stdout+stderr into $OUT and the exit code into $RC.
  OUT="$TMP/out"
  set +e
  (cd "$WORKDIR" && PATH="$FAKE_BIN:$PATH" "$BASH_BIN" "$MERGE_PR" "$@") > "$OUT" 2>&1
  RC=$?
  set -e
}

reset_logs() {
  FAKE_GH_LOG="$TMP/gh.log"; FAKE_GIT_LOG="$TMP/git.log"
  : > "$FAKE_GH_LOG"; : > "$FAKE_GIT_LOG"
  export FAKE_GH_LOG FAKE_GIT_LOG
}

# --- usage / precondition errors: exit 1, never touch gh or git -----------

reset_logs
run
[ "$RC" -eq 1 ] || fail "no args should exit 1, got $RC"
grep -qi "usage" "$OUT" || fail "no args should print usage"
pass "no_args_exits_1_with_usage"

reset_logs
run -h
[ "$RC" -eq 0 ] || fail "-h should exit 0, got $RC"
grep -qi "usage" "$OUT" || fail "-h should print usage"
pass "help_flag_exits_0"

reset_logs
run --help
[ "$RC" -eq 0 ] || fail "--help should exit 0, got $RC"
pass "long_help_flag_exits_0"

reset_logs
run 42 --strategy
[ "$RC" -eq 1 ] || fail "--strategy with no value should exit 1, got $RC"
grep -qi "needs a value" "$OUT" || fail "expected the missing-value message"
pass "strategy_missing_value_exits_1"

reset_logs
run 42 --strategy bogus
[ "$RC" -eq 1 ] || fail "invalid --strategy should exit 1, got $RC"
grep -qi "Unknown strategy" "$OUT" || fail "expected the unknown-strategy message"
pass "strategy_invalid_value_exits_1"

reset_logs
run 42 --nosuchflag
[ "$RC" -eq 1 ] || fail "unknown flag should exit 1, got $RC"
grep -qi "Unknown flag" "$OUT" || fail "expected the unknown-flag message"
pass "unknown_flag_exits_1"

reset_logs
run 42 43
[ "$RC" -eq 1 ] || fail "two PR numbers should exit 1, got $RC"
grep -qi "Two PR numbers" "$OUT" || fail "expected the two-PR-numbers message"
pass "two_pr_numbers_exits_1"

reset_logs
run --dry-run
[ "$RC" -eq 1 ] || fail "no PR number should exit 1, got $RC"
grep -qi "No PR number" "$OUT" || fail "expected the no-PR-number message"
pass "missing_pr_number_exits_1"

reset_logs
run abc
[ "$RC" -eq 1 ] || fail "non-numeric PR should exit 1, got $RC"
grep -qi "must be a number" "$OUT" || fail "expected the non-numeric message"
pass "non_numeric_pr_exits_1"

# gh entirely absent from PATH: nothing before this check needs another
# binary, so an empty PATH is sufficient and deterministic on any machine
# (BASH_BIN is invoked directly, so it doesn't need to be on PATH either).
mkdir -p "$TMP/empty"
OUT="$TMP/out"; set +e
(cd "$WORKDIR" && PATH="$TMP/empty" "$BASH_BIN" "$MERGE_PR" 42) > "$OUT" 2>&1
RC=$?
set -e
[ "$RC" -eq 1 ] || fail "missing gh should exit 1, got $RC"
grep -qi "gh not found" "$OUT" || fail "expected the gh-not-found message"
pass "gh_not_found_exits_1"

reset_logs
FAKE_GH_STATE=FAIL run 42
[ "$RC" -eq 1 ] || fail "unreadable PR should exit 1, got $RC"
grep -qi "Cannot read PR" "$OUT" || fail "expected the cannot-read message"
pass "gh_pr_view_failure_exits_1"

reset_logs
FAKE_GH_STATE=MERGED run 42
[ "$RC" -eq 1 ] || fail "non-OPEN PR should exit 1, got $RC"
grep -q "MERGED" "$OUT" || fail "expected the actual state (MERGED) in the message"
pass "pr_not_open_exits_1"

# --- refused: exit 2, checks not green -------------------------------------

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="no checks reported on this pull request" \
  FAKE_GH_CHECKS_RC=8 run 42
[ "$RC" -eq 2 ] || fail "no checks reported should exit 2, got $RC"
grep -qi "no CI checks at all" "$OUT" || fail "expected the no-checks message"
! grep -q "^pr merge" "$TMP/gh.log" || fail "must not merge when there are no checks"
pass "no_checks_reported_exits_2"

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  fail  1m" FAKE_GH_CHECKS_RC=1 run 42
[ "$RC" -eq 2 ] || fail "failing checks should exit 2, got $RC"
grep -qi "failing or pending checks" "$OUT" || fail "expected the failing-checks message"
! grep -q "^pr merge" "$TMP/gh.log" || fail "must not merge when checks are red"
pass "failing_checks_exits_2"

# --- success: exit 0 --------------------------------------------------------

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=some-feature-branch run 42 --dry-run
[ "$RC" -eq 0 ] || fail "green dry-run should exit 0, got $RC"
grep -qi "Dry run" "$OUT" || fail "expected the dry-run notice"
! grep -q "^pr merge" "$TMP/gh.log" || fail "dry-run must never call gh pr merge"
pass "green_dry_run_exits_0_without_merging"

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=some-feature-branch run 42
[ "$RC" -eq 0 ] || fail "green real merge should exit 0, got $RC"
grep -qx "pr merge 42 --rebase --delete-branch" "$TMP/gh.log" \
  || fail "expected the default --rebase strategy with --delete-branch"
[ -s "$TMP/git.log" ] || fail "current-branch check should still run"
grep -q "^tag " "$TMP/git.log" && fail "must not tag when not on the default branch"
pass "green_merge_default_strategy_off_default_branch"

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=some-feature-branch run 99 --strategy squash
[ "$RC" -eq 0 ] || fail "squash merge should exit 0, got $RC"
grep -qx "pr merge 99 --squash --delete-branch" "$TMP/gh.log" \
  || fail "expected --squash to be passed through"
pass "squash_strategy_is_passed_through"

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=main FAKE_GH_DEFAULT_BRANCH=main FAKE_GIT_TAG_EXISTS=0 run 42
[ "$RC" -eq 0 ] || fail "on-default-branch merge should exit 0, got $RC"
grep -qx "tag -a v1.2.3 -m AKOS v1.2.3" "$TMP/git.log" \
  || fail "expected an annotated tag for the VERSION/CHANGELOG-matching release"
grep -qx "push origin v1.2.3" "$TMP/git.log" || fail "expected the new tag to be pushed"
grep -qi "Tagged and pushed" "$OUT" || fail "expected the tagged-and-pushed confirmation"
pass "tags_and_pushes_when_version_and_changelog_agree"

reset_logs
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=main FAKE_GH_DEFAULT_BRANCH=main FAKE_GIT_TAG_EXISTS=1 run 42
[ "$RC" -eq 0 ] || fail "existing-tag merge should exit 0, got $RC"
grep -q "^tag -a" "$TMP/git.log" && fail "must not recreate a tag that already exists"
grep -q "^push origin v1.2.3" "$TMP/git.log" && fail "must not push when the tag already existed"
grep -qi "already exists" "$OUT" || fail "expected the already-exists warning"
pass "leaves_an_existing_tag_alone"

reset_logs
printf '9.9.9\n' > "$WORKDIR/VERSION"
FAKE_GH_STATE=OPEN FAKE_GH_CHECKS_OUTPUT="ci  pass  1m" FAKE_GH_CHECKS_RC=0 \
  FAKE_GIT_BRANCH=main FAKE_GH_DEFAULT_BRANCH=main run 42
printf '1.2.3\n' > "$WORKDIR/VERSION"
[ "$RC" -eq 0 ] || fail "version/changelog mismatch merge should still exit 0, got $RC"
grep -q "^tag" "$TMP/git.log" && fail "must not tag when VERSION has no matching CHANGELOG heading"
pass "skips_tagging_when_version_and_changelog_disagree"

echo "PASS: $(basename "$0")"
