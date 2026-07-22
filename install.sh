#!/usr/bin/env bash
#
# install.sh — Install AKOS globally on this Mac.
# Idempotent. Verifies structure, chmods scripts, creates the ~/DEV symlink
# (if the repo lives elsewhere) and the ~/bin/akos symlink. Never destroys content.
#
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; }

printf '%sInstalling AKOS%s from %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# 1. chmod scripts.
for s in install.sh update.sh doctor.sh uninstall.sh merge-pr.sh bin/akos; do
  if [ -f "$AKOS_HOME/$s" ]; then chmod +x "$AKOS_HOME/$s"; ok "chmod +x $s"; fi
done

# 2. Ensure ~/DEV/AKOS resolves. If the repo isn't already under ~/DEV,
#    create a ~/DEV symlink to its parent so the canonical path works.
canonical="$HOME/DEV/AKOS"
if [ -e "$canonical" ] || [ -L "$canonical" ]; then
  ok "~/DEV/AKOS already resolves"
else
  parent="$(dirname "$AKOS_HOME")"          # e.g. ~/Desktop/DEV
  if [ ! -e "$HOME/DEV" ]; then
    ln -s "$parent" "$HOME/DEV" && ok "symlinked ~/DEV → $parent"
  else
    warn "~/DEV exists but ~/DEV/AKOS does not; leaving it untouched (repo at $AKOS_HOME)"
  fi
fi

# 3. Create ~/bin and the akos symlink. Never clobbers a real file.
mkdir -p "$HOME/bin"
if [ -L "$HOME/bin/akos" ]; then
  if [ "$(readlink "$HOME/bin/akos")" = "$AKOS_HOME/bin/akos" ]; then
    ok "~/bin/akos already linked"
  else
    ln -sfn "$AKOS_HOME/bin/akos" "$HOME/bin/akos" && ok "refreshed ~/bin/akos → $AKOS_HOME/bin/akos"
  fi
elif [ -e "$HOME/bin/akos" ]; then
  warn "~/bin/akos is a real file — leaving it untouched (the 'akos' CLI won't be linked; move it aside and re-run)"
else
  ln -s "$AKOS_HOME/bin/akos" "$HOME/bin/akos" && ok "symlinked ~/bin/akos"
fi

# 3b. Link skills into Claude Code (~/.claude/skills) and Codex CLI
#     (~/.agents/skills). Symlinks, not copies — edits to packs go live in both
#     tools immediately. Never clobbers a real directory.
link_skill() {
  local skill="$1" dest_dir="$2" tool="$3"
  local src="$AKOS_HOME/skills/$skill" dest="$dest_dir/$skill"
  [ -d "$src" ] || { warn "skill '$skill' not found at $src"; return; }
  mkdir -p "$dest_dir"
  if [ -L "$dest" ]; then
    if [ "$(readlink "$dest")" = "$src" ]; then ok "$tool: $skill already linked"; return; fi
    ln -sfn "$src" "$dest" && ok "$tool: relinked $skill"
  elif [ -e "$dest" ]; then
    warn "$tool: $dest is a real directory — leaving it untouched (link manually if intended)"
  else
    ln -s "$src" "$dest" && ok "$tool: linked $skill"
  fi
}

for skill in akos akos-review; do
  link_skill "$skill" "$HOME/.claude/skills" "Claude Code"
  link_skill "$skill" "$HOME/.agents/skills" "Codex CLI"
done

# 3c. Link the 13 reviewers as Claude Code subagents, so a full pipeline run
#     can fan out in parallel with isolated context. Claude-only: Codex
#     subagents use TOML, and the skills already cover Codex.
agent_linked=0; agent_skipped=0
mkdir -p "$HOME/.claude/agents"
for src in "$AKOS_HOME"/agents/*.md; do
  [ -f "$src" ] || continue
  dest="$HOME/.claude/agents/akos-$(basename "$src")"
  if [ -L "$dest" ]; then
    [ "$(readlink "$dest")" = "$src" ] || ln -sfn "$src" "$dest"
    agent_linked=$((agent_linked+1))
  elif [ -e "$dest" ]; then
    warn "agents: $dest is a real file — leaving it untouched"
    agent_skipped=$((agent_skipped+1))
  else
    ln -s "$src" "$dest" && agent_linked=$((agent_linked+1))
  fi
done
if [ "$agent_skipped" -gt 0 ]; then
  ok "Claude Code: $agent_linked reviewer subagents linked ($agent_skipped skipped)"
else
  ok "Claude Code: $agent_linked reviewer subagents linked"
fi

# 4. PATH hint.
case ":$PATH:" in
  *":$HOME/bin:"*) ok "~/bin is on PATH" ;;
  *) warn "~/bin is not on PATH. Add:  export PATH=\"\$HOME/bin:\$PATH\"  to your shell profile." ;;
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
