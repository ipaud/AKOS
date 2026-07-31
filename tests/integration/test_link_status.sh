#!/usr/bin/env bash
# akos_link_status decides whether a path in the user's HOME leads to THIS
# checkout. doctor.sh and `akos list-skills` report to the user off its answer,
# so the case this file exists to lock down is the one that shipped broken: a
# second checkout that installed nothing printed a fully green health report,
# because existence was tested and identity was not.
#
# The inverse matters just as much. ~/DEV is commonly a symlink to somewhere
# else (~/Desktop/DEV), which makes ~/DEV/AKOS a real directory reached through
# a link rather than a link itself. A first attempt at this helper only looked
# at the final path component and reported the owner's own install as foreign.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck source=bin/akos-common.sh
source "$AKOS_HOME/bin/akos-common.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "${TMP:?}"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

expect() {
  local got want="$1" dest="$2" target="$3" what="$4"
  got="$(akos_link_status "$dest" "$target")"
  [ "$got" = "$want" ] || fail "$what: expected '$want', got '$got'"
  pass "$what"
}

mkdir -p "$TMP/checkout/skills/akos" "$TMP/other-checkout/skills/akos" "$TMP/home"

# 1. Nothing there at all.
expect missing "$TMP/home/nope" "$TMP/checkout/skills/akos" \
  "absent path reports missing"

# 2. The ordinary healthy install: a symlink pointing at this checkout.
ln -s "$TMP/checkout/skills/akos" "$TMP/home/akos"
expect linked "$TMP/home/akos" "$TMP/checkout/skills/akos" \
  "symlink to this checkout reports linked"

# 3. The bug this helper was written for: a link owned by a DIFFERENT checkout.
# Existence tests pass here, which is exactly why they were not enough.
ln -s "$TMP/other-checkout/skills/akos" "$TMP/home/foreign"
expect foreign "$TMP/home/foreign" "$TMP/checkout/skills/akos" \
  "symlink to another checkout reports foreign"

# 4. A real directory sitting where the link belongs — install.sh refuses to
# overwrite these, so the user must be told rather than shown a green check.
mkdir -p "$TMP/home/real-dir"
expect foreign "$TMP/home/real-dir" "$TMP/checkout/skills/akos" \
  "real directory in the link's place reports foreign"

# 5. A dangling symlink is foreign, not missing: something IS there, and
# reporting "missing (run ./install.sh)" would describe the wrong problem.
ln -s "$TMP/checkout/skills/deleted" "$TMP/home/dangling"
expect foreign "$TMP/home/dangling" "$TMP/checkout/skills/akos" \
  "dangling symlink reports foreign"

# 6. Symlinked ANCESTOR, the ~/DEV -> ~/Desktop/DEV shape. The destination is
# not itself a link; the path merely travels through one. Both spellings name
# the same directory and must compare equal.
ln -s "$TMP/checkout" "$TMP/home/via-link"
expect linked "$TMP/home/via-link/skills/akos" "$TMP/checkout/skills/akos" \
  "path through a symlinked ancestor reports linked"

# ...and the same shape must still catch a genuine mismatch, so 6 is not
# passing by resolving everything to equality.
expect foreign "$TMP/home/via-link/skills/akos" "$TMP/other-checkout/skills/akos" \
  "path through a symlinked ancestor still detects a different target"

# 7. Relative link target, resolved against the link's own directory rather
# than the caller's cwd.
ln -s "../checkout/skills/akos" "$TMP/home/relative"
expect linked "$TMP/home/relative" "$TMP/checkout/skills/akos" \
  "relative symlink target resolves correctly"

# 8. Files, not just directories — ~/bin/akos is a symlink to a file, and the
# resolver takes a different branch for those.
mkdir -p "$TMP/checkout/bin"
printf '#!/bin/sh\n' > "$TMP/checkout/bin/akos"
ln -s "$TMP/checkout/bin/akos" "$TMP/home/akos-bin"
expect linked "$TMP/home/akos-bin" "$TMP/checkout/bin/akos" \
  "symlink to a file reports linked"

# 9. A symlink chain. install.sh does not create these, but ~/bin or ~/DEV on a
# user's machine may already be one, so the resolver must not stop at hop one.
ln -s "$TMP/home/akos" "$TMP/home/chained"
expect linked "$TMP/home/chained" "$TMP/checkout/skills/akos" \
  "chained symlink resolves through every hop"

printf '\nall link-status checks passed\n'
