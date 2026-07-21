#!/usr/bin/env bash
# End-to-end: doctor, validate, benchmark, profile, and history all
# invoked for real through bin/akos, in a scratch project — the actual
# path a user takes, not individual functions called directly.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AKOS="$AKOS_HOME/bin/akos"
TMP="$(mktemp -d)"
# `akos profile create` always scaffolds under the real AKOS_HOME (there is
# no "scratch AKOS repo" mode for it) — clean it up on ANY exit path, not
# just the success path, so a failed assertion never leaves test cruft in
# the real repo.
trap 'rm -rf "$TMP" "$AKOS_HOME/packs/personal/e2e-test-profile"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

# doctor.sh — the real one, real repo, real exit code.
"$AKOS_HOME/doctor.sh" >/tmp/doctor-e2e.$$ 2>&1
rc=$?
[ "$rc" -eq 0 ] || fail "doctor.sh exited $rc"
pass "doctor.sh exit 0"
rm -f /tmp/doctor-e2e.$$

# validate — real schema check against the real repo.
python3 "$AKOS_HOME/schemas/validate.py" packs >/tmp/validate-e2e.$$ 2>&1
rc=$?
[ "$rc" -eq 0 ] || fail "akos validate exited $rc"
pass "akos validate packs: clean"
rm -f /tmp/validate-e2e.$$

# benchmark — the real 21-case suite.
python3 "$AKOS_HOME/benchmarks/runners/run.py" run >/tmp/bench-e2e.$$ 2>&1
rc=$?
[ "$rc" -eq 0 ] || { cat /tmp/bench-e2e.$$; fail "akos benchmark exited $rc"; }
pass "akos benchmark: all cases pass"
rm -f /tmp/bench-e2e.$$

# profile — create, use in a scratch project, verify the config line.
"$AKOS" profile create e2e-test-profile >/dev/null 2>&1
[ -d "$AKOS_HOME/packs/personal/e2e-test-profile" ] || fail "profile create did not scaffold the directory"
pass "profile create scaffolded packs/personal/e2e-test-profile"

"$AKOS" install-project "$TMP" >/dev/null 2>&1
"$AKOS" profile use e2e-test-profile "$TMP" >/dev/null 2>&1
grep -q "personal_profile: e2e-test-profile" "$TMP/.akos/config.md" \
  || fail "profile use did not set personal_profile in .akos/config.md"
pass "profile use set personal_profile correctly"

# history — record a review and read it back, in the scratch project.
echo "# Test Review" > "$TMP/report.md"
"$AKOS" history record --type e2e-test --decision PASS --profile "Startup MVP" \
  --report "$TMP/report.md" --scores-json '{"ux": 90}' --dir "$TMP" >/dev/null 2>&1
count="$("$AKOS" history list --dir "$TMP" | wc -l | tr -d ' ')"
[ "$count" -ge 1 ] || fail "history record did not produce a listable review"
pass "history record + list: 1 review recorded"

echo "PASS: test_end_to_end_project.sh"
