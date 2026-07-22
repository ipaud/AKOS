#!/usr/bin/env bash
# doctor.sh's self-scan must fail when AKOS's own rule engine cannot RUN TO
# COMPLETION — a detector or registry that fails to execute.
#
# The invariant changed in the P0 hardening: the old self-scan asserted "no
# CRITICAL in this repository", which was only ever true because a central
# path-based downgrade turned AKOS's own deliberately-vulnerable corpus
# (benchmarks/cases/**, evals/cases/**) into LOW. That downgrade is gone
# (P0-4), so the corpus legitimately reports CRITICAL/HIGH findings and the
# honest, checkable invariant is that the scan COMPLETES with no operational
# error (the fail-closed contract from P0-3). This asserts the check catches a
# broken detector, which is the thing a real regression would look like.
set -euo pipefail
AKOS_HOME="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail() { echo "FAIL: $1" >&2; exit 1; }

reg="$AKOS_HOME/rules/security/zz_self_scan_probe.yaml"
det="$AKOS_HOME/rules/security/zz_self_scan_probe.py"
cleanup() { rm -f "$reg" "$det"; }
trap cleanup EXIT

# Baseline: a clean checkout passes (corpus findings and all).
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh does not pass on a clean checkout"

# Plant a rule whose detector raises: the runner must record an ExecutionError,
# report status 'error', and exit 1 — an incomplete scan, which doctor's
# self-scan must not read as clean.
cat > "$reg" <<'YAML'
id: ZZ_SELF_SCAN_PROBE
title: Self-scan probe — detector always raises
domain: security
level: A
severity:
  default: LOW
confidence: Low
detector: rules/security/zz_self_scan_probe.py
applies_to:
  glob: ["**/*.py"]
  target: project-source
recommendation: Remove this probe.
version: 1
status: stable
YAML
printf 'def run(files):\n    raise RuntimeError("self-scan probe: detector cannot run")\n' > "$det"

if bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1; then
  fail "doctor.sh still passed with a broken detector planted — the self-scan check is not fail-closed"
fi

cleanup
trap - EXIT
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh did not recover after cleanup"

echo "PASS: $(basename "$0")"
