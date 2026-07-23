#!/usr/bin/env bash
#
# uninstall.sh — Remove AKOS symlinks. Does NOT delete knowledge packs
# unless the user explicitly confirms with a typed phrase.
#
set -euo pipefail

resolve_akos_home() {
  local src="${BASH_SOURCE[0]}"
  while [ -h "$src" ]; do
    local dir
    dir="$(cd -P "$(dirname "$src")" >/dev/null 2>&1 && pwd)"
    src="$(readlink "$src")"
    [[ "$src" != /* ]] && src="$dir/$src"
  done
  local script_dir
  script_dir="$(cd "$(dirname "$src")" >/dev/null 2>&1 && pwd)"
  if [ -L "$script_dir" ]; then
    local target
    target="$(readlink "$script_dir")"
    if [[ "$target" = /* ]]; then
      printf '%s\n' "$target"
    else
      cd "$(dirname "$script_dir")/$target" >/dev/null 2>&1 && pwd
    fi
  else
    printf '%s\n' "$script_dir"
  fi
}
AKOS_HOME="$(resolve_akos_home)"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*"; }

usage() {
  printf 'Usage: ./uninstall.sh\n'
}

if [ "$#" -gt 0 ]; then
  case "${1:-}" in
    -h|--help) [ "$#" -eq 1 ] || { usage >&2; exit 1; }; usage; exit 0 ;;
    *) usage >&2; exit 1 ;;
  esac
fi

printf '%sUninstalling AKOS%s\n\n' "$c_bold" "$c_reset"

# 1. Remove ~/bin/akos only when its target proves this checkout owns it.
if [ -L "$HOME/bin/akos" ]; then
  target="$(readlink "$HOME/bin/akos")"
  if [ "$target" = "$AKOS_HOME/bin/akos" ]; then
    rm -f "$HOME/bin/akos" && ok "removed $HOME/bin/akos symlink"
  else
    warn "$HOME/bin/akos is a foreign symlink (→ $target) — leaving it"
  fi
else
  warn "$HOME/bin/akos is not a symlink (or absent) — leaving it"
fi

# 1b. Remove the skill symlinks from Claude Code and Codex CLI.
#     Only removes links that point back into this repo.
for dir in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  for skill in akos akos-review; do
    link="$dir/$skill"
    if [ -L "$link" ] && [ "$(readlink "$link")" = "$AKOS_HOME/skills/$skill" ]; then
      rm -f "$link" && ok "removed $link"
    elif [ -e "$link" ]; then
      warn "$link is not an AKOS symlink — leaving it"
    fi
  done
done

# 1c. Remove the reviewer subagent symlinks (Claude Code only).
agents_removed=0
for src in "$AKOS_HOME"/agents/*.md; do
  [ -f "$src" ] || continue
  link="$HOME/.claude/agents/akos-$(basename "$src")"
  if [ -L "$link" ] && [ "$(readlink "$link")" = "$src" ]; then
    rm -f "$link" && agents_removed=$((agents_removed+1))
  fi
done
if [ "$agents_removed" -gt 0 ]; then ok "removed $agents_removed reviewer subagent symlinks"; fi

# 2. Remove the canonical leaf only when it points to this checkout. A legacy
#    or user-owned ~/DEV parent is never removed.
canonical="$HOME/DEV/AKOS"
if [ -L "$canonical" ]; then
  target="$(readlink "$canonical")"
  if [ "$target" = "$AKOS_HOME" ]; then
    rm -f "$canonical" && ok "removed owned $HOME/DEV/AKOS symlink"
  else
    warn "$HOME/DEV/AKOS is a foreign symlink (→ $target) — leaving it"
  fi
elif [ -e "$canonical" ]; then
  warn "$HOME/DEV/AKOS is not an owned symlink — leaving it untouched"
fi

ok "Symlinks handled. Knowledge packs at $AKOS_HOME are UNTOUCHED."

# 3. Optional content deletion — requires explicit typed confirmation.
printf '\n%sTo also DELETE all AKOS content at %s%s%s:\n' "$c_bold" "$c_red" "$AKOS_HOME" "$c_reset"
printf 'This removes EVERYTHING there: git history, unpushed commits, and every\n'
printf 'pack — including any you authored outside packs/personal/ (only packs/\n'
printf 'is backed up first).\n'
printf 'Type exactly:  DELETE AKOS  (or press Enter to keep everything): '
read -r answer || answer=""
if [ "$answer" = "DELETE AKOS" ]; then
  # Refuse to rm -rf a directory that doesn't look like an AKOS root — a
  # failed cd in the AKOS_HOME derivation, or running a stray copy of this
  # script, must not delete an arbitrary directory.
  if [ ! -f "$AKOS_HOME/VERSION" ] || [ ! -d "$AKOS_HOME/packs" ] || [ ! -d "$AKOS_HOME/core" ]; then
    fail "$AKOS_HOME does not look like an AKOS root (VERSION/packs/core missing) — refusing to delete"
    exit 1
  fi
  # Back up the whole packs/ tree, not just personal/ — `akos create-pack`
  # writes user-authored packs under packs/<domain>/, and those are just as
  # unrecoverable. The backup is verified BEFORE anything is removed: a
  # failed cp (disk full, permissions) must abort, not print "preserved"
  # and delete anyway.
  keep="$HOME/akos-packs-backup-$(date +%Y%m%d%H%M%S)"
  if ! cp -R "$AKOS_HOME/packs" "$keep"; then
    fail "could not back up $AKOS_HOME/packs to $keep — aborting, nothing deleted"
    exit 1
  fi
  ok "packs (including personal layer) preserved at $keep"
  rm -rf "$AKOS_HOME"
  ok "AKOS content deleted (packs backed up above)."
else
  ok "Kept all AKOS content. Nothing deleted."
fi
