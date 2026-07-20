#!/usr/bin/env bash
# doctor.sh must catch VERSION disagreeing with the newest CHANGELOG entry.
#
# Version staleness recurred twice: work accumulated under an already-released
# heading while VERSION sat unchanged. Bumping fixed the instance both times
# and the class neither time. This asserts the class fix actually catches it.
set -euo pipefail
AKOS_HOME="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail() { echo "FAIL: $1" >&2; exit 1; }

backup="$(mktemp)"
cp "$AKOS_HOME/VERSION" "$backup"
restore() { cp "$backup" "$AKOS_HOME/VERSION"; rm -f "$backup"; }
trap restore EXIT

# Baseline: agreement passes.
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh does not pass on a clean checkout"

# Disagreement must fail. Manifests are left alone deliberately: this asserts
# the CHANGELOG check fires, and the manifest check firing too is fine — what
# must not happen is doctor passing.
printf '9.9.9\n' > "$AKOS_HOME/VERSION"
if bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1; then
  fail "doctor.sh passed with VERSION disagreeing with the newest CHANGELOG entry"
fi

# And the message has to name the disagreement, not only the manifest drift.
out="$(bash "$AKOS_HOME/doctor.sh" 2>&1 || true)"
printf '%s' "$out" | grep -q "newest CHANGELOG entry" \
  || fail "doctor.sh failed, but not with the CHANGELOG-disagreement message"

restore
trap - EXIT
bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1 || fail "doctor.sh did not recover after restore"

echo "PASS: $(basename "$0")"
