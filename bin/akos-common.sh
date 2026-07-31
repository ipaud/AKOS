#!/usr/bin/env bash
#
# bin/akos-common.sh — shared Python resolution and version-floor check.
# Sourced by install.sh, update.sh, doctor.sh, and bin/akos — never executed
# directly. Defines functions only; sourcing this file has no side effects
# and mutates nothing until a caller invokes require_python().
#
# AKOS requires Python 3.10+ (schemas/, rules/, benchmarks/, history, config
# validation, freshness, the marker parser, and the update-restore verifier
# all depend on it). Before this helper existed, a missing python3 degraded
# doctor.sh checks to warnings, install.sh/update.sh never checked at all,
# and bin/akos relied on `set -e` turning a missing python3 into a raw
# "command not found" deep inside whichever subcommand happened to need it
# first — never a clean, up-front, actionable failure.

AKOS_PYTHON_MIN_MAJOR=3
AKOS_PYTHON_MIN_MINOR=10

# Resolve which python3 binary to use — resolution only, no validation, no
# side effects. AKOS_PYTHON_BIN (if set) is the test-injection point: it lets
# tests simulate "missing" or "too old" python3 deterministically, without
# touching the real interpreter on the machine running the tests.
resolve_python() {
  if [ -n "${AKOS_PYTHON_BIN:-}" ]; then
    printf '%s\n' "$AKOS_PYTHON_BIN"
    return 0
  fi
  command -v python3 2>/dev/null
}

# Check the resolved candidate meets the 3.10+ floor. Prints nothing, only
# returns 0/1, so callers with different reporting conventions (doctor.sh's
# fail/warn accumulator vs. install.sh/update.sh's abort-on-failure) decide
# how to react. Reads the floor via `--version` output rather than executing
# arbitrary Python through the candidate — that's what makes a trivial,
# non-functional shell-script fixture sufficient to stand in for "old
# python3" in tests: it only has to answer --version correctly.
check_python() {
  local py
  py="$(resolve_python)"
  if [ -z "$py" ] || ! command -v "$py" >/dev/null 2>&1; then
    return 1
  fi
  local ver_out
  ver_out="$("$py" --version 2>&1)" || return 1
  if [[ ! "$ver_out" =~ Python\ ([0-9]+)\.([0-9]+) ]]; then
    return 1
  fi
  local major="${BASH_REMATCH[1]}" minor="${BASH_REMATCH[2]}"
  if [ "$major" -gt "$AKOS_PYTHON_MIN_MAJOR" ]; then
    return 0
  fi
  [ "$major" -eq "$AKOS_PYTHON_MIN_MAJOR" ] && [ "$minor" -ge "$AKOS_PYTHON_MIN_MINOR" ]
}

# Human-readable detected-version string for error messages. Never fails —
# worst case it reports "not found" or "unknown".
_akos_python_version_report() {
  local py
  py="$(resolve_python)"
  if [ -z "$py" ]; then echo "not found"; return; fi
  if ! command -v "$py" >/dev/null 2>&1; then echo "not found ($py does not exist)"; return; fi
  "$py" --version 2>&1 || echo "unknown (--version failed)"
}

# Require a valid python3 >= 3.10 or fail with an actionable, self-contained
# message (no dependency on the caller's own ok/warn/err helpers, so this
# works identically regardless of which script sources it). On success,
# exports AKOS_PYTHON so every later call site in the calling script uses
# the SAME resolved interpreter — the whole point being that no script ever
# falls back to a second, independently-resolved `python3` literal after
# this check has run.
require_python() {
  if check_python; then
    AKOS_PYTHON="$(resolve_python)"
    export AKOS_PYTHON
    return 0
  fi
  {
    printf 'AKOS requires Python %s.%s or newer.\n' "$AKOS_PYTHON_MIN_MAJOR" "$AKOS_PYTHON_MIN_MINOR"
    printf '  Detected: %s\n' "$(_akos_python_version_report)"
    printf '  Check your version:   python3 --version\n'
    printf '  Point at a specific interpreter with AKOS_PYTHON_BIN if needed.\n'
    printf '  No changes were made.\n'
  } >&2
  return 1
}

# --- Symlink identity ---------------------------------------------------
#
# Existence is not identity. A machine with two AKOS checkouts has links that
# exist but belong to the other one, so `[ -e ]` reports a healthy install for
# a tree that installed nothing. install.sh and uninstall.sh already compare
# targets before writing or removing; doctor.sh and `akos list-skills` report
# to the user, so they need the same test or they report success they never
# verified.

# Resolve a path to its physical location, following symlinks at any depth —
# including a symlinked ancestor, which is why the final component alone is not
# enough to compare: ~/DEV is commonly a symlink to ~/Desktop/DEV, so
# ~/DEV/AKOS is a real directory reached through a link, not a link itself.
# Both spellings must compare equal. Returns non-zero on a dangling link.
_akos_resolve() {
  local p="$1" hops=0 tgt d
  while [ -L "$p" ] && [ "$hops" -lt 10 ]; do
    tgt="$(readlink "$p")"
    case "$tgt" in /*) p="$tgt" ;; *) p="$(dirname "$p")/$tgt" ;; esac
    hops=$((hops+1))
  done
  [ -e "$p" ] || return 1
  if [ -d "$p" ]; then
    (cd -P "$p" 2>/dev/null && pwd) || return 1
  else
    d="$(cd -P "$(dirname "$p")" 2>/dev/null && pwd)" || return 1
    printf '%s/%s\n' "${d%/}" "$(basename "$p")"
  fi
}

# Echo the state of $1 as a path that should lead to $2:
#   linked  — resolves to $2, whether directly or through a symlinked ancestor
#   foreign — exists but resolves somewhere else, or dangles
#   missing — nothing there
akos_link_status() {
  local dest="$1" want="$2" rd rw
  if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then printf 'missing\n'; return 0; fi
  rd="$(_akos_resolve "$dest")" || { printf 'foreign\n'; return 0; }
  rw="$(_akos_resolve "$want")" || { printf 'foreign\n'; return 0; }
  if [ "$rd" = "$rw" ]; then printf 'linked\n'; else printf 'foreign\n'; fi
}
