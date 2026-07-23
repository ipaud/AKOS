#!/usr/bin/env bash
# End-to-end: doctor, validate, benchmark, profile, and history all invoked
# through bin/akos from an owned scratch checkout and scratch project.
set -euo pipefail

AKOS_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

AKOS_HOME="$TMP/akos-home"
PROJECT="$TMP/project"
cp -R "$AKOS_SOURCE" "$AKOS_HOME"
mkdir -p "$PROJECT"

# This nested scratch checkout is outside the source tree measured by the
# integration coverage wrapper. Use its actual interpreter so coverage output
# cannot contaminate doctor.sh's captured JSON protocols.
unset AKOS_PYTHON_BIN

AKOS="$AKOS_HOME/bin/akos"
FIXTURE_SUFFIX="$$-${RANDOM}"
PROFILE_NAME="e2e-test-profile-$FIXTURE_SUFFIX"
PACK_DOMAIN="e2e-test-domain-$FIXTURE_SUFFIX"

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

# doctor.sh — real command, scratch checkout, real exit code.
if ! "$AKOS_HOME/doctor.sh" >"$TMP/doctor.out" 2>&1; then
  cat "$TMP/doctor.out" >&2
  fail "doctor.sh exited non-zero"
fi
pass "doctor.sh exit 0"

# validate — real schema check against the scratch checkout.
if ! python3 "$AKOS_HOME/schemas/validate.py" packs >"$TMP/validate.out" 2>&1; then
  cat "$TMP/validate.out" >&2
  fail "akos validate exited non-zero"
fi
pass "akos validate packs: clean"

# benchmark — the real current corpus.
if ! python3 "$AKOS_HOME/benchmarks/runners/run.py" run >"$TMP/benchmark.out" 2>&1; then
  cat "$TMP/benchmark.out" >&2
  fail "akos benchmark exited non-zero"
fi
pass "akos benchmark: all cases pass"

# profile — create, use in a scratch project, verify the config line.
"$AKOS" profile create "$PROFILE_NAME" >/dev/null 2>&1
[ -d "$AKOS_HOME/packs/personal/$PROFILE_NAME" ] \
  || fail "profile create did not scaffold the directory"
pass "profile create scaffolded an isolated personal profile"

"$AKOS" install-project "$PROJECT" >/dev/null 2>&1
"$AKOS" profile use "$PROFILE_NAME" "$PROJECT" >/dev/null 2>&1
grep -q "personal_profile: $PROFILE_NAME" "$PROJECT/.akos/config.md" \
  || fail "profile use did not set personal_profile in .akos/config.md"
pass "profile use set personal_profile correctly"

# create-pack — metadata must carry schema_version: 1 and validate clean.
"$AKOS" create-pack "$PACK_DOMAIN/e2e-test-pack" >/dev/null 2>&1
grep -q "^schema_version: 1$" \
  "$AKOS_HOME/packs/$PACK_DOMAIN/e2e-test-pack/metadata.yaml" \
  || fail "create-pack did not scaffold schema_version: 1"
python3 "$AKOS_HOME/schemas/validate.py" packs --format json \
  >"$TMP/create-pack.json" 2>&1
python3 - "$TMP/create-pack.json" "$PACK_DOMAIN" <<'PY' \
  || fail "create-pack's scaffolded pack does not validate clean"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as report:
    data = json.load(report)
mine = [result for result in data if sys.argv[2] in result["file"]]
assert mine, "scaffolded pack not found by validate.py"
assert not mine[0]["errors"], f"scaffolded pack has schema errors: {mine[0]['errors']}"
PY
pass "create_pack_scaffolds_schema_version_1"

# history — record a review and read it back, in the scratch project.
echo "# Test Review" > "$TMP/report.md"
"$AKOS" history record --type e2e-test --decision PASS --profile "Startup MVP" \
  --report "$TMP/report.md" --scores-json '{"ux": 90}' --dir "$PROJECT" \
  >/dev/null 2>&1
count="$("$AKOS" history list --dir "$PROJECT" | wc -l | tr -d ' ')"
[ "$count" -ge 1 ] || fail "history record did not produce a listable review"
pass "history record + list: 1 review recorded"

echo "PASS: test_end_to_end_project.sh"
