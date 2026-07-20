#!/usr/bin/env bash
# doctor.sh must fail when AKOS's own rules report a CRITICAL against it.
#
# The claim "akos rules run . exits 0 on this repository" was written into two
# commit messages and was false once. A claim that needs to stay true belongs
# in a check; this asserts the check actually catches the thing.
set -euo pipefail
AKOS_HOME="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail() { echo "FAIL: $1" >&2; exit 1; }

planted="$AKOS_HOME/supabase/migrations/zz_self_scan_probe.sql"
cleanup() {
  rm -f "$planted"
  rmdir "$AKOS_HOME/supabase/migrations" "$AKOS_HOME/supabase" 2>/dev/null || true
}
trap cleanup EXIT

# Baseline: clean repository passes.
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh does not pass on a clean checkout"

# Plant a real CRITICAL outside any fixture path, so the central downgrade
# does not apply and the check has something to catch.
mkdir -p "$AKOS_HOME/supabase/migrations"
printf 'create table public.self_scan_probe (id uuid primary key);\n' > "$planted"

if bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1; then
  fail "doctor.sh still passed with a CRITICAL planted — the self-scan check is not gating"
fi

cleanup
trap - EXIT
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh did not recover after cleanup"

echo "PASS: $(basename "$0")"
