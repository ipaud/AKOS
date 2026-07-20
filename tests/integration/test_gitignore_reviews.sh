#!/usr/bin/env bash
# install-project must add .akos/reviews/ to the project's .gitignore.
# Review reports quote the defects they find, including credentials on a
# security lens; history record redacts known shapes at write time, but
# pattern-based redaction will miss things, so the reports should not be
# pushed by default.
set -euo pipefail
AKOS_HOME="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }

# 1. No pre-existing .gitignore
mkdir -p "$tmp/fresh" && cd "$tmp/fresh"
"$AKOS_HOME/bin/akos" install-project >/dev/null 2>&1
grep -qxF ".akos/reviews/" .gitignore || fail "did not add .akos/reviews/ to a new .gitignore"

# 2. Rerun must not duplicate
"$AKOS_HOME/bin/akos" install-project >/dev/null 2>&1
count="$(grep -cxF ".akos/reviews/" .gitignore)"
[ "$count" -eq 1 ] || fail "duplicated the entry on rerun (found $count)"

# 3. Existing .gitignore content must survive
mkdir -p "$tmp/existing" && cd "$tmp/existing"
printf 'node_modules/\ndist/\n' > .gitignore
"$AKOS_HOME/bin/akos" install-project >/dev/null 2>&1
grep -qxF "node_modules/" .gitignore || fail "clobbered an existing .gitignore"
grep -qxF "dist/" .gitignore || fail "clobbered an existing .gitignore"
grep -qxF ".akos/reviews/" .gitignore || fail "did not append to an existing .gitignore"

# 4. An entry already present must be left alone
mkdir -p "$tmp/already" && cd "$tmp/already"
printf '.akos/reviews/\n' > .gitignore
"$AKOS_HOME/bin/akos" install-project >/dev/null 2>&1
count="$(grep -cxF ".akos/reviews/" .gitignore)"
[ "$count" -eq 1 ] || fail "added a second copy when one was already present (found $count)"

echo "PASS: $(basename "$0")"
