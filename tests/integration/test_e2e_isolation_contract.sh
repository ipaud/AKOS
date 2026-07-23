#!/usr/bin/env bash
# The E2E harness must be safe to run from any checkout, including one where
# its historical fixed fixture names already belong to the operator. Exercise
# the real test from a throwaway repo copy so a regression can never damage the
# working checkout that launched this contract test.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

cp -R "$AKOS_HOME" "$TMP/akos-copy"
COPY="$TMP/akos-copy"

cp -R \
  "$COPY/packs/personal/_template" \
  "$COPY/packs/personal/e2e-test-profile"
mkdir -p "$COPY/packs/e2e-test-domain"
printf 'operator-owned profile\n' > "$COPY/packs/personal/e2e-test-profile/SENTINEL"
printf 'operator-owned domain\n' > "$COPY/packs/e2e-test-domain/SENTINEL"

set +e
bash "$COPY/tests/integration/test_end_to_end_project.sh" >"$TMP/e2e.out" 2>&1
rc=$?
set -e

[ "$rc" -eq 0 ] || {
  tail -40 "$TMP/e2e.out" >&2
  fail "the E2E harness could not run beside pre-existing fixture names"
}
[ -f "$COPY/packs/personal/e2e-test-profile/SENTINEL" ] \
  || fail "the E2E harness deleted a pre-existing personal profile"
[ -f "$COPY/packs/e2e-test-domain/SENTINEL" ] \
  || fail "the E2E harness deleted a pre-existing pack domain"

echo "PASS: test_e2e_isolation_contract.sh"
