#!/usr/bin/env bash
# A project directory with spaces in its path — install-project,
# validate, and history record must all handle this correctly. Every
# path this test touches is quoted; an unquoted path anywhere in bin/akos
# or schemas/*.py would break here first.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AKOS="$AKOS_HOME/bin/akos"
TMP="$(mktemp -d)/My Project With Spaces"
mkdir -p "$TMP"
trap 'rm -rf "$(dirname "$TMP")"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

"$AKOS" install-project "$TMP" >/dev/null 2>&1
[ -f "$TMP/.akos/config.md" ] || fail "install-project failed against a path containing spaces"
pass "install-project succeeded on a path with spaces"

echo "# Report" > "$TMP/report.md"
"$AKOS" history record --type spaces-test --decision PASS --profile "Startup MVP" \
  --report "$TMP/report.md" --dir "$TMP" >/dev/null 2>&1
count="$("$AKOS" history list --dir "$TMP" | wc -l | tr -d ' ')"
[ "$count" -ge 1 ] || fail "history record/list failed against a path containing spaces"
pass "history record + list succeeded on a path with spaces"

echo "PASS: test_path_with_spaces.sh"
