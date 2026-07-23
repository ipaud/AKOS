#!/usr/bin/env bash
# Python 3.10+ is a mandatory dependency (schemas/, rules/, benchmarks/,
# history, config validation, freshness, the marker parser, and the update
# restore verifier all require it). Before bin/akos-common.sh existed,
# doctor.sh treated a missing python3 as a warning (never failed the build),
# install.sh/update.sh never checked at all, and bin/akos relied on `set -e`
# turning a missing python3 into a raw "command not found" deep inside
# whichever subcommand needed it first. This locks down the real fix:
# require_python runs BEFORE any mutation, and its failure is deterministic
# and simulated via AKOS_PYTHON_BIN — no need to uninstall/downgrade the
# real interpreter on the machine running this test.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

cp -R "$AKOS_HOME" "$TMP/akos-copy"
COPY="$TMP/akos-copy"
export HOME="$TMP/home"
mkdir -p "$HOME"

# A trivial fixture that only needs to answer `--version` correctly — it is
# never actually executed as a working interpreter (check_python's floor
# probe is --version-only by design), which is what makes this deterministic
# on every machine regardless of what's really installed.
OLD_PY="$TMP/python3-old"
cat > "$OLD_PY" <<'EOF'
#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "Python 3.8.0"; exit 0; fi
exit 1
EOF
chmod +x "$OLD_PY"

# 1. install.sh requires Python before any mutation — snapshot HOME before
#    and after a failed run and confirm zero mutation, not just a nonzero exit.
before_snapshot="$(find "$HOME" 2>/dev/null | sort)"
if AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/install.sh" >"$TMP/out1" 2>&1; then
  fail "install.sh should refuse to run without python3, but exited 0"
fi
after_snapshot="$(find "$HOME" 2>/dev/null | sort)"
[ "$before_snapshot" = "$after_snapshot" ] || fail "install.sh mutated \$HOME even though python3 was missing"
[ ! -e "$HOME/bin/akos" ] || fail "install.sh created ~/bin/akos despite missing python3"
grep -qi "requires python" "$TMP/out1" || fail "expected an actionable 'requires Python' message"
pass "install_requires_python_before_any_mutation"

# 2. install.sh rejects a python3 that resolves but is too old.
before_snapshot="$(find "$HOME" 2>/dev/null | sort)"
if AKOS_PYTHON_BIN="$OLD_PY" bash "$COPY/install.sh" >"$TMP/out2" 2>&1; then
  fail "install.sh should refuse Python 3.8, but exited 0"
fi
after_snapshot="$(find "$HOME" 2>/dev/null | sort)"
[ "$before_snapshot" = "$after_snapshot" ] || fail "install.sh mutated \$HOME with a too-old python3"
grep -qi "3\.8\.0" "$TMP/out2" || fail "expected the detected old version (3.8.0) in the error message"
pass "install_rejects_python_older_than_3_10"

# From here on, install a real copy once (with the real interpreter) so
# doctor.sh/bin/akos have something to check against.
bash "$COPY/install.sh" >/dev/null 2>&1 || fail "baseline install (real python3) must succeed"

# 3. doctor.sh reports missing python3 as a FAILURE (exit non-zero), not a warning.
if AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/doctor.sh" >"$TMP/out3" 2>&1; then
  fail "doctor.sh should exit non-zero when python3 is missing"
fi
grep -qi "not found or too old" "$TMP/out3" || fail "expected doctor.sh to name the python3 failure explicitly"
pass "doctor_missing_python_is_failure"

# 4. doctor.sh reports a too-old python3 as a FAILURE too.
if AKOS_PYTHON_BIN="$OLD_PY" bash "$COPY/doctor.sh" >"$TMP/out4" 2>&1; then
  fail "doctor.sh should exit non-zero when python3 is too old"
fi
pass "doctor_old_python_is_failure"

# 5. update.sh requires Python before backup/lock/pull.
if AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/update.sh" >"$TMP/out5" 2>&1; then
  fail "update.sh should refuse to run without python3"
fi
[ ! -d "$HOME/.akos-backups" ] || fail "update.sh created a backup despite missing python3"
grep -qi "requires python" "$TMP/out5" || fail "expected an actionable 'requires Python' message from update.sh"
pass "update_requires_python_before_backup_or_pull"

# 6. `akos help` works even without python3 (and -h/--help).
if ! AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/bin/akos" help >"$TMP/out6" 2>&1; then
  fail "akos help must work without python3"
fi
grep -q "AI Knowledge Operating System CLI" "$TMP/out6" || fail "akos help produced unexpected output"
AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/bin/akos" --help >/dev/null 2>&1 || fail "akos --help must work without python3"
pass "akos_help_works_without_python"

# 7. An operational command (one that actually needs python3) fails cleanly
#    without it — list-packs is pure bash today but is gated uniformly with
#    every other operational command; validate always needs it.
if AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/bin/akos" validate all >"$TMP/out7" 2>&1; then
  fail "akos validate should refuse to run without python3"
fi
grep -qi "requires python" "$TMP/out7" || fail "expected an actionable 'requires Python' message from akos validate"
pass "akos_operational_command_fails_without_python"

# 8. `akos doctor` itself must still RUN without python3 (it is the health
#    check that reports python3's absence as a finding, not a command that
#    can refuse to run because of it) — distinct from case 7 above.
if AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/bin/akos" doctor >"$TMP/out8" 2>&1; then
  fail "akos doctor should exit non-zero when python3 is missing (doctor.sh's own accounting), not silently pass"
fi
grep -qi "not found or too old" "$TMP/out8" || fail "expected akos doctor to surface the python3 finding"
pass "akos_doctor_runs_without_python_and_reports_it"

# 9. create-pack has NO silent date fallback when python3's computation
#    fails — it must fail loudly and leave no partial pack, since
#    require_python already guarantees a valid interpreter is present by the
#    time this runs (this simulates a python3 that PASSES the version floor
#    but still fails the actual computation — a genuine unexpected error,
#    distinct from "python3 is missing" which case 7 already covers).
BROKEN_PY="$TMP/python3-broken"
cat > "$BROKEN_PY" <<'EOF'
#!/usr/bin/env bash
if [ "$1" = "--version" ]; then echo "Python 3.11.0"; exit 0; fi
exit 1
EOF
chmod +x "$BROKEN_PY"
if AKOS_PYTHON_BIN="$BROKEN_PY" bash "$COPY/bin/akos" create-pack testdomain/no-fallback-pack >"$TMP/out9" 2>&1; then
  fail "create-pack should fail when its date computation fails, not silently fall back"
fi
[ ! -d "$COPY/packs/testdomain/no-fallback-pack" ] || fail "create-pack left a partial pack behind after a failed date computation"
grep -qi "no partial pack" "$TMP/out9" || fail "expected create-pack's failure message to confirm no partial pack was left"
pass "create_pack_has_no_date_fallback_when_python_fails"

# 10. The resolved interpreter is used CONSISTENTLY — a custom-named
#     AKOS_PYTHON_BIN wrapper (not literally on PATH as `python3`) must
#     actually be the binary create-pack's date computation invokes, not a
#     second, independently-resolved `python3` literal found on PATH.
REAL_PY="$(command -v python3)"
WRAPPER_PY="$TMP/python3-wrapper"
WRAPPER_LOG="$TMP/wrapper-invocations.log"
cat > "$WRAPPER_PY" <<EOF
#!/usr/bin/env bash
echo "invoked: \$*" >> "$WRAPPER_LOG"
exec "$REAL_PY" "\$@"
EOF
chmod +x "$WRAPPER_PY"
AKOS_PYTHON_BIN="$WRAPPER_PY" bash "$COPY/bin/akos" create-pack testdomain/wrapper-pack >"$TMP/out10" 2>&1 \
  || fail "create-pack should succeed through a working wrapper interpreter"
[ -f "$WRAPPER_LOG" ] || fail "the resolved wrapper interpreter was never invoked — a second python3 literal was used instead"
grep -q "timedelta" "$WRAPPER_LOG" || fail "the wrapper was invoked, but not for the date computation call site"
pass "resolved_python_binary_is_used_consistently"

# 11. The failure message names the requirement, the detected version (or
#     lack thereof), and confirms no changes were made — not just "error".
AKOS_PYTHON_BIN=/nonexistent/python3 bash "$COPY/bin/akos" validate all >"$TMP/out11" 2>&1 || true
grep -qi "3\.10" "$TMP/out11" || fail "error message must name the version floor (3.10)"
grep -qi "no changes were made" "$TMP/out11" || fail "error message must confirm no changes were made"
pass "python_error_message_is_actionable"

echo "PASS: test_python_required.sh"
