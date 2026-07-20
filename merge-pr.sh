#!/usr/bin/env bash
#
# merge-pr.sh — merge a pull request only after its CI checks are green.
#
# Why this exists: on 2026-07-20 PR #3 was merged while its own `ci` check was
# failing, because the merge was gated on `mergeable` (can git combine these?)
# and never on `gh pr checks` (did the tests pass?). v1.4.0 shipped red and
# stayed red across three runs. See CHANGELOG [1.5.0] "Corrected".
#
# This is a MITIGATION, not a control. GitHub's server-side branch protection
# is the real control, and it is unavailable on a private repo on the free
# plan. Anyone can still run `gh pr merge` directly and bypass this entirely.
# It only works if it is the merge path you actually use.
#
# Exit codes (matching docs/cli/exit-codes.md's scheme for new commands):
#   0  merged
#   1  usage error, or a precondition could not be established
#   2  refused — checks are not green
#
set -euo pipefail

BOLD=$'\033[1m'; RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RESET=$'\033[0m'
fail() { printf '%s✗%s %s\n' "$RED" "$RESET" "$1" >&2; }
ok()   { printf '%s✓%s %s\n' "$GREEN" "$RESET" "$1"; }
warn() { printf '%s!%s %s\n' "$YELLOW" "$RESET" "$1"; }

usage() {
  cat <<EOF
${BOLD}merge-pr.sh${RESET} — merge a PR only if its CI checks are green.

Usage:
  ./merge-pr.sh <pr-number> [--strategy rebase|squash|merge] [--dry-run]

  --strategy   How to merge. Default: rebase (this repo's convention).
  --dry-run    Report what would happen and exit 0 without merging.

Exit codes: 0 merged (or dry-run clean) · 1 usage/precondition error · 2 refused, checks not green.
EOF
}

[ $# -eq 0 ] && { usage; exit 1; }

pr=""; strategy="rebase"; dry_run="no"
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --dry-run) dry_run="yes"; shift ;;
    --strategy)
      [ $# -ge 2 ] || { fail "--strategy needs a value: rebase, squash, or merge."; exit 1; }
      strategy="$2"
      case "$strategy" in
        rebase|squash|merge) ;;
        *) fail "Unknown strategy '$strategy'. Valid: rebase, squash, merge."; exit 1 ;;
      esac
      shift 2 ;;
    -*) fail "Unknown flag '$1'. Run './merge-pr.sh --help' for the accepted flags."; exit 1 ;;
    *)
      [ -n "$pr" ] && { fail "Two PR numbers given ('$pr' and '$1'). Pass exactly one."; exit 1; }
      pr="$1"; shift ;;
  esac
done

[ -n "$pr" ] || { fail "No PR number given. Usage: ./merge-pr.sh <pr-number>"; exit 1; }
case "$pr" in
  ''|*[!0-9]*) fail "PR must be a number, got '$pr'. Find it with 'gh pr list'."; exit 1 ;;
esac

command -v gh >/dev/null 2>&1 || { fail "gh not found. Install the GitHub CLI: https://cli.github.com"; exit 1; }

# A PR that does not exist must not read as "no failing checks".
state="$(gh pr view "$pr" --json state --jq .state 2>/dev/null)" || {
  fail "Cannot read PR #$pr. Check the number with 'gh pr list', and that gh is authenticated ('gh auth status')."
  exit 1
}
[ "$state" = "OPEN" ] || { fail "PR #$pr is $state, not OPEN. Nothing to merge."; exit 1; }

# gh pr checks exits non-zero when checks fail OR when there are none at all.
# Those are different situations and must not collapse into one message.
checks_out="$(gh pr checks "$pr" 2>&1)" && checks_rc=0 || checks_rc=$?

if printf '%s' "$checks_out" | grep -qi "no checks reported"; then
  fail "PR #$pr has no CI checks at all. Refusing — a PR with no checks is not a PR with passing checks."
  echo "  If that is expected for this PR, merge deliberately with: gh pr merge $pr --$strategy --delete-branch" >&2
  exit 2
fi

printf '%s\n' "$checks_out"

if [ "$checks_rc" -ne 0 ]; then
  fail "PR #$pr has failing or pending checks (gh pr checks exit $checks_rc). Refusing to merge."
  echo "  Watch them finish:  gh pr checks $pr --watch" >&2
  echo "  Read a failure:     gh run view <run-id> --log-failed" >&2
  exit 2
fi

ok "All checks green on PR #$pr."

if [ "$dry_run" = "yes" ]; then
  warn "Dry run — not merging. Would run: gh pr merge $pr --$strategy --delete-branch"
  exit 0
fi

gh pr merge "$pr" --"$strategy" --delete-branch
ok "Merged PR #$pr with --$strategy and deleted the branch."
