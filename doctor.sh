#!/usr/bin/env bash
#
# doctor.sh — AKOS health check.
# Verifies directory structure, the 17-file pack contract, executable bits,
# symlinks, and empty files. Exits non-zero on any failure.
#
set -uo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
pass=0; warnc=0; failc=0
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; pass=$((pass+1)); }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; warnc=$((warnc+1)); }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*"; failc=$((failc+1)); }

printf '%sAKOS Doctor%s — %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# python3 is the repo's one non-coreutils dependency (JSON manifest parsing,
# schema validation). Checked once, up front, so its absence degrades
# gracefully (a warning, once) instead of a raw "command not found" at every
# call site below.
if command -v python3 >/dev/null 2>&1; then
  HAVE_PYTHON3=1
else
  HAVE_PYTHON3=0
fi

# --- Required top-level directories ---
printf '%sStructure%s\n' "$c_bold" "$c_reset"
for d in core packs agents workflows templates prompts graphs scoring bin; do
  if [ -d "$AKOS_HOME/$d" ]; then ok "dir $d/"; else fail "missing dir $d/"; fi
done

# --- Required root files ---
for f in README.md VERSION CHANGELOG.md install.sh update.sh doctor.sh uninstall.sh; do
  if [ -f "$AKOS_HOME/$f" ]; then ok "file $f"; else fail "missing file $f"; fi
done

# --- Required core files ---
printf '\n%sCore layer%s\n' "$c_bold" "$c_reset"
core_files=(constitution authority-model reasoning-engine conflict-resolution \
  decision-framework confidence-model knowledge-schema review-pipeline scoring-model \
  reasoning-profiles source-policy)
for cf in "${core_files[@]}"; do
  if [ -f "$AKOS_HOME/core/$cf.md" ]; then ok "core/$cf.md"; else fail "missing core/$cf.md"; fi
done

# --- Pack 17-file contract ---
printf '\n%sPacks (17-file contract)%s\n' "$c_bold" "$c_reset"
pack_files=(README.md metadata.yaml philosophy.md mental-models.md principles.md \
  heuristics.md engineering-rules.md decision-framework.md anti-patterns.md \
  review-checklist.md examples.md prompt-fragments.md scoring-rubric.md glossary.md \
  references.md CHANGELOG.md VERSION)
pack_count=0; pack_issues=0
for pack in "$AKOS_HOME"/packs/*/*/; do
  [ -d "$pack" ] || continue
  pack_count=$((pack_count+1))
  rel="${pack#"$AKOS_HOME/"}"
  # personal layer uses its own file set — check it separately.
  if [[ "$rel" == packs/personal/* ]]; then
    for pf in README.md principles.md design-language.md project-patterns.md \
      coding-preferences.md ux-preferences.md supabase-rules.md ai-agent-rules.md VERSION CHANGELOG.md; do
      [ -f "$pack$pf" ] || { fail "missing $rel$pf"; pack_issues=$((pack_issues+1)); }
    done
    continue
  fi
  for pf in "${pack_files[@]}"; do
    [ -f "$pack$pf" ] || { fail "missing $rel$pf"; pack_issues=$((pack_issues+1)); }
  done
done
if [ "$pack_issues" -eq 0 ]; then ok "$pack_count packs all satisfy the file contract"; fi

# --- Empty file check ---
printf '\n%sEmpty files%s\n' "$c_bold" "$c_reset"
empty="$(find "$AKOS_HOME/packs" "$AKOS_HOME/core" "$AKOS_HOME/agents" \
  "$AKOS_HOME/workflows" "$AKOS_HOME/scoring" "$AKOS_HOME/graphs" \
  "$AKOS_HOME/prompts" "$AKOS_HOME/templates" -type f -empty 2>/dev/null || true)"
if [ -z "$empty" ]; then ok "no empty files"; else fail "empty files found:"; printf '   %s\n' $empty; fi

# --- Agents / workflows / scoring / graphs counts ---
printf '\n%sComponents%s\n' "$c_bold" "$c_reset"
count_check() { local dir="$1" want="$2" label="$3"
  local n; n="$(find "$AKOS_HOME/$dir" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$n" -ge "$want" ]; then ok "$label: $n"; else warn "$label: $n (expected ≥$want)"; fi
}
count_check agents 13 "agents"
count_check workflows 9 "workflows"
count_check scoring 7 "scoring rubrics"
count_check graphs 5 "graphs"
count_check prompts 6 "prompts"
count_check templates 6 "templates"

# --- Skills (Claude Code + Codex CLI, same open agent-skills format) ---
printf '\n%sSkills%s\n' "$c_bold" "$c_reset"
akos_skill="$AKOS_HOME/skills/akos/SKILL.md"
for skill in akos akos-review; do
  sf="$AKOS_HOME/skills/$skill/SKILL.md"
  if [ ! -f "$sf" ]; then fail "missing skills/$skill/SKILL.md"; continue; fi
  if [ "$(head -n 1 "$sf")" != "---" ]; then
    fail "skills/$skill/SKILL.md does not open with YAML frontmatter"
    continue
  fi
  # Frontmatter is everything up to the second '---'.
  fm="$(awk 'NR==1 && $0=="---" {next} $0=="---" {exit} {print}' "$sf")"
  fm_name="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -n 1)"
  fm_desc="$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -n 1)"
  if [ "$fm_name" = "$skill" ]; then ok "skills/$skill: name matches directory"
  else fail "skills/$skill: frontmatter name '$fm_name' != directory '$skill'"; fi
  if [ -n "$fm_desc" ]; then ok "skills/$skill: description present"
  else fail "skills/$skill: empty or missing description"; fi
done

# Every pack must appear in the akos skill's routing table, or the model
# cannot route to it. This replaces a generated index — fail loudly on drift.
# packs/personal/* is deliberately excluded: those are never task-routed
# (step 4's "pick 2-5" table) — they're always loaded generically in step 3
# via the `personal_profile` config field, so enumerating each one here would
# just recreate the drift problem this guard exists to prevent.
if [ -f "$akos_skill" ]; then
  missing_packs=0
  for pack in "$AKOS_HOME"/packs/*/*/; do
    [ -d "$pack" ] || continue
    rel="${pack#"$AKOS_HOME/packs/"}"; rel="${rel%/}"
    case "$rel" in personal/*) continue ;; esac
    # Match the full domain/pack path, so a pack filed under the wrong domain
    # in the table is caught too.
    grep -qF "$rel" "$akos_skill" || {
      fail "pack '$rel' is not listed in skills/akos/SKILL.md routing table"
      missing_packs=$((missing_packs+1))
    }
  done
  [ "$missing_packs" -eq 0 ] && ok "all packs listed in skills/akos/SKILL.md"
fi

# --- Reviewer subagents (Claude Code) ---
printf '\n%sReviewer subagents%s\n' "$c_bold" "$c_reset"
agent_issues=0; agent_n=0
for a in "$AKOS_HOME"/agents/*.md; do
  [ -f "$a" ] || continue
  agent_n=$((agent_n+1))
  base="$(basename "$a" .md)"
  if [ "$(head -n 1 "$a")" != "---" ]; then
    fail "agents/$base.md has no YAML frontmatter"; agent_issues=$((agent_issues+1)); continue
  fi
  afm="$(awk 'NR==1 && $0=="---" {next} $0=="---" {exit} {print}' "$a")"
  aname="$(printf '%s\n' "$afm" | sed -n 's/^name:[[:space:]]*//p' | head -n 1)"
  adesc="$(printf '%s\n' "$afm" | sed -n 's/^description:[[:space:]]*//p' | head -n 1)"
  # Names are akos-prefixed so they never shadow the user's own reviewers.
  [ "$aname" = "akos-$base" ] || { fail "agents/$base.md: name '$aname' should be 'akos-$base'"; agent_issues=$((agent_issues+1)); }
  [ -n "$adesc" ] || { fail "agents/$base.md: missing description"; agent_issues=$((agent_issues+1)); }
done
[ "$agent_issues" -eq 0 ] && ok "$agent_n reviewer subagents have valid frontmatter"

# --- Plugin manifests ---
printf '\n%sPlugin manifests%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping JSON manifest parse checks"
else
for m in .claude-plugin/plugin.json .claude-plugin/marketplace.json \
         .codex-plugin/plugin.json .agents/plugins/marketplace.json; do
  if [ ! -f "$AKOS_HOME/$m" ]; then fail "missing $m"; continue; fi
  if python3 -m json.tool "$AKOS_HOME/$m" >/dev/null 2>&1; then ok "$m parses"
  else fail "$m is not valid JSON"; fi
done
fi
# Manifest versions must track VERSION, or installs ship a stale label.
if [ -f "$AKOS_HOME/VERSION" ]; then
  ver="$(tr -d '[:space:]' < "$AKOS_HOME/VERSION")"
  ver_issues=0
  for m in .claude-plugin/plugin.json .claude-plugin/marketplace.json \
           .codex-plugin/plugin.json .agents/plugins/marketplace.json; do
    [ -f "$AKOS_HOME/$m" ] || continue
    grep -qF "\"version\": \"$ver\"" "$AKOS_HOME/$m" || {
      fail "$m version does not match VERSION ($ver)"; ver_issues=$((ver_issues+1)); }
  done
  [ "$ver_issues" -eq 0 ] && ok "manifest versions match VERSION ($ver)"

  # VERSION must not drift behind the CHANGELOG's newest entry. Twice now the
  # version has sat stale while a day's work accumulated under it — the first
  # time by ten commits, the second by eight, describing features that shipped
  # after the label was written. Both were fixed by bumping, which fixed the
  # instance and left the class open. This is the class.
  if [ -f "$AKOS_HOME/CHANGELOG.md" ]; then
    top_entry="$(grep -m1 -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' "$AKOS_HOME/CHANGELOG.md" | tr -d '#[] ')"
    if [ -z "$top_entry" ]; then
      warn "no versioned entry found at the top of CHANGELOG.md"
    elif [ "$top_entry" != "$ver" ]; then
      fail "VERSION is $ver but the newest CHANGELOG entry is $top_entry — bump one or the other"
    else
      ok "VERSION matches the newest CHANGELOG entry ($ver)"
    fi
  fi

  # The check above catches disagreement. It does NOT catch what actually
  # happened twice: work appended UNDER an already-released heading, so
  # VERSION and the CHANGELOG agreed while the entry described things that
  # shipped after the label. The signal for that is commits touching source
  # since VERSION last changed. A warning, not a failure — unreleased commits
  # are normal mid-development; the point is that nobody noticed for a day.
  if [ -d "$AKOS_HOME/.git" ] && command -v git >/dev/null 2>&1; then
    last_bump="$(git -C "$AKOS_HOME" log -1 --format=%H -- VERSION 2>/dev/null || true)"
    if [ -n "$last_bump" ]; then
      since="$(git -C "$AKOS_HOME" rev-list --count "$last_bump..HEAD" \
                 -- packs rules schemas evals benchmarks bin skills core 2>/dev/null || echo 0)"
      if [ "$since" -gt 0 ]; then
        warn "$since commit(s) touching source since VERSION last changed — is $ver still the right label?"
      else
        ok "no source commits since VERSION was last set"
      fi
    fi
  fi
fi

# --- Schema validation (advisory) ---
# Non-breaking by construction: schemas/knowledge-pack.schema.json's required
# fields are exactly the 7 already universal across every pack, so this
# reports 0 errors against the existing corpus without any migration gate.
# Errors here fail the build; recommended-field warnings don't.
printf '\n%sSchema validation%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping schema validation (packs/agents/workflows)"
else
  validate_out="$(python3 "$AKOS_HOME/schemas/validate.py" packs agents workflows --format json 2>&1)"
  validate_rc=$?
  if [ "$validate_rc" -gt 1 ]; then
    schema_errors="$(printf '%s' "$validate_out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['errors']) for r in d))" 2>/dev/null || echo "?")"
    schema_warnings="$(printf '%s' "$validate_out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['warnings']) for r in d))" 2>/dev/null || echo "?")"
    fail "schema validation: $schema_errors error(s) — run 'akos validate' for detail"
    [ "$schema_warnings" != "0" ] && [ "$schema_warnings" != "?" ] && warn "schema validation: $schema_warnings recommended-field warning(s)"
  elif [ "$validate_rc" -eq 0 ]; then
    schema_warnings="$(printf '%s' "$validate_out" | python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['warnings']) for r in d))" 2>/dev/null || echo "0")"
    if [ "$schema_warnings" = "0" ]; then
      ok "packs/agents/workflows validate clean against their schemas"
    else
      ok "packs/agents/workflows validate clean (0 errors)"
      warn "schema validation: $schema_warnings recommended-field warning(s) — run 'akos validate' for detail"
    fi
  else
    fail "schema validation runner failed to execute (exit $validate_rc)"
  fi
fi

# --- Pack freshness (advisory) ---
# Same PACK_EXPIRED detector `akos rules` uses, called directly — repo
# self-maintenance a maintainer should see on a routine health check, not
# only when explicitly running the rules command.
printf '\n%sPack freshness%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping pack freshness check"
else
  expired_out="$(python3 "$AKOS_HOME/rules/runner.py" "$AKOS_HOME" --rule PACK_EXPIRED --format json 2>&1)"
  expired_rc=$?
  if [ "$expired_rc" -eq 1 ]; then
    fail "PACK_EXPIRED rule failed to run (exit $expired_rc)"
  else
    expired_count="$(printf '%s' "$expired_out" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")"
    if [ "$expired_count" = "0" ]; then
      ok "no packs past their review_after date"
    else
      warn "$expired_count pack(s) past review_after — run 'akos freshness --expired' for detail"
    fi
  fi
fi

# --- AKOS passes its own rules ---
# The claim "akos rules run . exits 0 on this repository" was made twice in
# commit messages and was false once — verified against a single rule and
# asserted for the whole run. A claim that needs to stay true belongs in a
# check, not in prose. Exit 2 means an open CRITICAL; 1 means the run itself
# broke, which is not a clean result and must not read as one.
printf '\n%sSelf-scan%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping self-scan"
else
  self_out="$(python3 "$AKOS_HOME/rules/runner.py" "$AKOS_HOME" 2>&1)"
  self_rc=$?
  case "$self_rc" in
    0) ok "akos rules run finds no CRITICAL in this repository" ;;
    2) fail "akos rules run reports a CRITICAL in this repository — run 'akos rules run .' for detail" ;;
    *) fail "akos rules run failed to complete (exit $self_rc); this is not a clean result" ;;
  esac
fi

# --- Executable bits ---
printf '\n%sExecutables%s\n' "$c_bold" "$c_reset"
for s in install.sh update.sh doctor.sh uninstall.sh bin/akos; do
  if [ -x "$AKOS_HOME/$s" ]; then ok "$s executable"; else warn "$s not executable (run ./install.sh)"; fi
done

# --- Symlinks ---
printf '\n%sSymlinks%s\n' "$c_bold" "$c_reset"
if [ -e "$HOME/DEV/AKOS" ]; then ok "~/DEV/AKOS resolves"; else warn "~/DEV/AKOS not found (run ./install.sh)"; fi
if [ -L "$HOME/bin/akos" ]; then ok "~/bin/akos symlink present"; else warn "~/bin/akos symlink absent (run ./install.sh)"; fi
for dir in "$HOME/.claude/skills:Claude Code" "$HOME/.agents/skills:Codex CLI"; do
  d="${dir%%:*}"; label="${dir##*:}"
  for skill in akos akos-review; do
    if [ -e "$d/$skill" ]; then ok "$label: $skill linked"
    else warn "$label: $skill not linked (run ./install.sh)"; fi
  done
done
linked_agents=0
for a in "$AKOS_HOME"/agents/*.md; do
  [ -e "$HOME/.claude/agents/akos-$(basename "$a")" ] && linked_agents=$((linked_agents+1))
done
if [ "$linked_agents" -eq "$agent_n" ]; then ok "Claude Code: $linked_agents reviewer subagents linked"
else warn "Claude Code: $linked_agents/$agent_n reviewer subagents linked (run ./install.sh)"; fi

# --- Summary ---
printf '\n%sSummary%s  %s✓ %d%s  %s! %d%s  %s✗ %d%s\n' \
  "$c_bold" "$c_reset" "$c_green" "$pass" "$c_reset" "$c_yellow" "$warnc" "$c_reset" "$c_red" "$failc" "$c_reset"
[ "$failc" -eq 0 ]
