#!/usr/bin/env bash
#
# install.sh — Install AKOS globally on this Mac.
# Idempotent. Verifies structure, chmods scripts, creates the ~/DEV/AKOS leaf
# and ~/bin/akos symlinks. Never destroys content.
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
# shellcheck source=bin/akos-common.sh
source "$AKOS_HOME/bin/akos-common.sh"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*" >&2; }

usage() {
  printf 'Usage: ./install.sh\n'
}

if [ "$#" -gt 0 ]; then
  case "${1:-}" in
    -h|--help) [ "$#" -eq 1 ] || { usage >&2; exit 1; }; usage; exit 0 ;;
    *) usage >&2; exit 1 ;;
  esac
fi

printf '%sInstalling AKOS%s from %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# Python 3.10+ is mandatory before ANY mutation — schemas, rules, benchmarks,
# history, and config validation all depend on it. Checked here, first,
# before a single chmod/mkdir/symlink runs, so a missing/old interpreter
# fails cleanly with zero side effects instead of an install that "succeeds"
# but ships a system unable to run its own validation.
require_python || exit 1

# 1. Own one canonical leaf. Never replace a foreign object at ~/DEV/AKOS:
#    the rest of AKOS and its skills treat that path as authoritative.
canonical_parent="$HOME/DEV"
canonical="$canonical_parent/AKOS"
if [ -L "$canonical" ]; then
  canonical_target="$(readlink "$canonical")"
  if [ "$canonical_target" = "$AKOS_HOME" ]; then
    ok "$HOME/DEV/AKOS already linked to this checkout"
  else
    fail "foreign collision at $HOME/DEV/AKOS (→ $canonical_target) — refusing to install"
    exit 1
  fi
elif [ -e "$canonical" ]; then
  canonical_physical="$(cd -P "$canonical" 2>/dev/null && pwd || true)"
  if [ "$canonical_physical" = "$AKOS_HOME" ]; then
    ok "$HOME/DEV/AKOS already resolves to this checkout"
  else
    fail "foreign collision at $HOME/DEV/AKOS — refusing to replace existing content"
    exit 1
  fi
else
  if [ -e "$canonical_parent" ] && [ ! -d "$canonical_parent" ]; then
    fail "$HOME/DEV exists but is not a directory — refusing to install"
    exit 1
  fi
  mkdir -p "$canonical_parent"
  ln -s "$AKOS_HOME" "$canonical"
  ok "symlinked $HOME/DEV/AKOS → $AKOS_HOME"
fi

# 2. chmod scripts.
for s in install.sh update.sh doctor.sh uninstall.sh merge-pr.sh bin/akos; do
  if [ -f "$AKOS_HOME/$s" ]; then chmod +x "$AKOS_HOME/$s"; ok "chmod +x $s"; fi
done

# A foreign symlink counts as AKOS-managed — and so is safe to refresh toward
# this install — only when it points at the SAME sub-path inside a DIFFERENT,
# still-valid AKOS checkout (one that has core/constitution.md + VERSION). That
# is the "moved the repo, re-run install" case. Anything else (a link to an
# unrelated tool, or a dangling link into a deleted repo) is foreign and left
# untouched. POSIX parameter expansion + case only — no GNU realpath/sed.
_is_akos_managed_link() {
  local src="$1" target="$2"
  local subpath="${src#"$AKOS_HOME"/}"          # e.g. bin/akos, skills/akos, agents/x.md
  case "$target" in
    */"$subpath")
      local other_home="${target%/"$subpath"}"
      [ -f "$other_home/core/constitution.md" ] && [ -f "$other_home/VERSION" ]
      ;;
    *) return 1 ;;
  esac
}

# Install or refresh an AKOS-managed symlink without ever clobbering foreign
# content. Classifies the destination BEFORE touching it — no `ln -sf`/`-sfn`
# runs against an unclassified path. `quiet` suppresses the per-item ok line
# (used by the 13-agent loop) but never suppresses a warning.
link_managed() {
  local src="$1" dest="$2" label="$3" quiet="${4:-}"
  if [ -L "$dest" ]; then
    local target; target="$(readlink "$dest")"
    if [ "$target" = "$src" ]; then
      [ -n "$quiet" ] || ok "$label already linked"
    elif _is_akos_managed_link "$src" "$target"; then
      ln -sfn "$src" "$dest" && { [ -n "$quiet" ] || ok "$label refreshed → $src (migrated from a prior AKOS install)"; }
    else
      warn "$label is a foreign symlink (→ $target) — leaving it untouched"
    fi
  elif [ -e "$dest" ]; then
    if [ -d "$dest" ]; then
      warn "$label is a real directory — leaving it untouched (link manually if intended)"
    else
      warn "$label is a real file — leaving it untouched (move it aside and re-run to link)"
    fi
  else
    ln -s "$src" "$dest" && { [ -n "$quiet" ] || ok "$label linked"; }
  fi
}

# 3. Create ~/bin and the akos CLI symlink.
mkdir -p "$HOME/bin"
link_managed "$AKOS_HOME/bin/akos" "$HOME/bin/akos" "$HOME/bin/akos"

# 3b. Link skills into Claude Code (~/.claude/skills) and Codex CLI
#     (~/.agents/skills). Symlinks, not copies — edits to packs go live in both
#     tools immediately. Never clobbers a real directory.
link_skill() {
  local skill="$1" dest_dir="$2" tool="$3"
  local src="$AKOS_HOME/skills/$skill" dest="$dest_dir/$skill"
  [ -d "$src" ] || { warn "skill '$skill' not found at $src"; return; }
  mkdir -p "$dest_dir"
  link_managed "$src" "$dest" "$tool: $skill"
}

for skill in akos akos-review; do
  link_skill "$skill" "$HOME/.claude/skills" "Claude Code"
  link_skill "$skill" "$HOME/.agents/skills" "Codex CLI"
done

# 3c. Link the 13 reviewers as Claude Code subagents, so a full pipeline run
#     can fan out in parallel with isolated context. Claude-only: Codex
#     subagents use TOML, and the skills already cover Codex.
mkdir -p "$HOME/.claude/agents"
for src in "$AKOS_HOME"/agents/*.md; do
  [ -f "$src" ] || continue
  dest="$HOME/.claude/agents/akos-$(basename "$src")"
  link_managed "$src" "$dest" "agents: akos-$(basename "$src")" quiet
done
agent_linked="$(find "$HOME/.claude/agents" -type l -name 'akos-*.md' 2>/dev/null | wc -l | tr -d ' ')"
agent_srcs="$(find "$AKOS_HOME/agents" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
agent_skipped=$((agent_srcs - agent_linked))
if [ "$agent_skipped" -gt 0 ]; then
  ok "Claude Code: $agent_linked reviewer subagents linked ($agent_skipped skipped)"
else
  ok "Claude Code: $agent_linked reviewer subagents linked"
fi

# 4. PATH hint.
case ":$PATH:" in
  *":$HOME/bin:"*) ok "$HOME/bin is on PATH" ;;
  *) warn "$HOME/bin is not on PATH. Add:  export PATH=\"\$HOME/bin:\$PATH\"  to your shell profile." ;;
esac

# 5. Structure verification (non-fatal report). Output is discarded — no
#    predictable /tmp path (a pre-planted symlink at a guessable name would
#    be followed by the > redirection, CWE-377).
printf '\n%sVerifying structure%s\n' "$c_bold" "$c_reset"
if bash "$AKOS_HOME/doctor.sh" >/dev/null 2>&1; then
  ok "doctor: all checks passed"
else
  warn "doctor reported issues — run ./doctor.sh for detail"
fi

# 6. Summary.
packs="$(find "$AKOS_HOME/packs" -mindepth 2 -maxdepth 2 -type d | wc -l | tr -d ' ')"
agents="$(find "$AKOS_HOME/agents" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
cat <<EOF

${c_bold}AKOS installed.${c_reset}
  Packs:   $packs
  Skills:  akos · akos-review            (Claude Code + Codex CLI)
  Agents:  akos-*-reviewer × $agents        (Claude Code subagents)
  CLI:     akos help                     (via ~/bin/akos)

Next:
  akos doctor                  # health check
  cd <your-project> && akos install-project   # wire AKOS into a project

Skills are live in both tools — start a new session and invoke 'akos'
(Codex: '\$akos') or 'akos-review'.
EOF
