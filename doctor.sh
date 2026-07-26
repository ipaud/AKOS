#!/usr/bin/env bash
#
# doctor.sh — AKOS health check.
# Verifies directory structure, the 12-file pack contract, pack provenance,
# executable bits, symlinks, and empty files. Exits non-zero on any failure.
#
# Deliberately no `set -e` (unlike install/update/uninstall): this script is a
# report accumulator — individual checks failing IS the data, counted into the
# summary, and must not abort the remaining checks.
set -uo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=bin/akos-common.sh
source "$AKOS_HOME/bin/akos-common.sh"
c_green=$'\033[32m'; c_yellow=$'\033[33m'; c_red=$'\033[31m'; c_bold=$'\033[1m'; c_reset=$'\033[0m'
pass=0; warnc=0; failc=0
ok()   { printf '%s✓%s %s\n' "$c_green" "$c_reset" "$*"; pass=$((pass+1)); }
warn() { printf '%s!%s %s\n' "$c_yellow" "$c_reset" "$*"; warnc=$((warnc+1)); }
fail() { printf '%s✗%s %s\n' "$c_red" "$c_reset" "$*"; failc=$((failc+1)); }

printf '%sAKOS Doctor%s — %s\n\n' "$c_bold" "$c_reset" "$AKOS_HOME"

# Python 3.10+ is a hard, mandatory dependency (schemas/, rules/, benchmarks/,
# history, config validation, freshness, the marker parser, and the update
# restore verifier all require it) — its absence or an out-of-date version is
# a real FAILURE here, not a soft-degrade warning. A doctor run that reports
# "clean" on a machine that cannot actually run schema validation, rules, or
# history was worse than no check at all: it looked healthy while its core
# integrity guarantees were silently inoperative.
if check_python; then
  HAVE_PYTHON3=1
else
  HAVE_PYTHON3=0
  fail "python3 (3.10+) not found or too old — detected: $(_akos_python_version_report). Schema validation, rules, freshness, and history are NOT operative without it."
fi
# Resolved once, used everywhere below — never a second, independently
# resolved `python3` literal that could point at a different interpreter
# than the one just verified above.
AKOS_PYTHON="$(resolve_python)"

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

# --- Pack file contract ---
# REQUIRED: the files every consumer (agents, skills, scoring) actually loads,
# plus the identity/lifecycle files. OPTIONAL: present when the source has
# something distinct to say — a pack with nothing unique in philosophy.md gains
# an agent nothing and costs a maintainer a file. Enforced as presence-only, so
# these are the floor, not a quality bar.
# OPTIONAL (not checked here): philosophy.md, mental-models.md, examples.md,
# prompt-fragments.md, glossary.md — present when the source has something
# distinct to say.
printf '\n%sPacks (required-file contract)%s\n' "$c_bold" "$c_reset"
pack_files=(README.md metadata.yaml principles.md heuristics.md \
  engineering-rules.md decision-framework.md anti-patterns.md \
  review-checklist.md scoring-rubric.md references.md CHANGELOG.md VERSION)
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

# --- Pack provenance & metadata links ---
# Two authoring steps nothing verified before. Both are cheap greps and both
# close a real gap: an audit found packs/ux/wcag/README.md shipping with no
# independence claim at all, and `related:` is schema-typed as a list of plain
# strings — a typo there resolves to nothing and no check noticed.
#
# NOT checked here: presence in graphs/knowledge-graph.md. That file indexes
# cross-cutting *concepts*, not packs — a single-domain pack like
# testing/playwright legitimately has no node, and 19 packs are absent by
# design. Requiring a link would encode a rule the graph does not follow.
printf '\n%sPack provenance & links%s\n' "$c_bold" "$c_reset"
prov_issues=0; related_issues=0
for pack in "$AKOS_HOME"/packs/*/*/; do
  [ -d "$pack" ] || continue
  rel="${pack#"$AKOS_HOME/packs/"}"; rel="${rel%/}"
  # The personal layer distills nobody — it encodes the owner's own rules, so
  # it carries neither a source disclaimer nor a `related:` list.
  case "$rel" in personal/*) continue ;; esac
  # Substring, not the canonical sentence: core/source-policy.md sanctions a
  # terse variant for sources with no "originals to buy" (a standards body).
  # What's required is the claim of independence, not one exact wording.
  if [ -f "$pack/README.md" ] && ! grep -qi 'independent distillation' "$pack/README.md"; then
    fail "pack '$rel': README.md has no independent-distillation line (core/source-policy.md)"
    prov_issues=$((prov_issues+1))
  fi
  if [ -f "$pack/metadata.yaml" ]; then
    related_targets="$(awk '
      /^related:/ {inlist=1; next}
      /^[a-zA-Z_-]+:/ {inlist=0}
      inlist && /^[[:space:]]*-[[:space:]]/ {
        sub(/^[[:space:]]*-[[:space:]]*/, ""); gsub(/["\r]/, ""); print
      }' "$pack/metadata.yaml")"
    # Unquoted on purpose: pack paths never contain whitespace, and word
    # splitting is what turns the awk output into one target per iteration.
    # shellcheck disable=SC2086
    for target in $related_targets; do
      [ -d "$AKOS_HOME/$target" ] || {
        fail "pack '$rel': related '$target' does not exist"
        related_issues=$((related_issues+1))
      }
    done
  fi
done
if [ "$prov_issues" -eq 0 ]; then ok "all packs carry an independent-distillation line"; fi
if [ "$related_issues" -eq 0 ]; then ok "all metadata 'related:' paths resolve"; fi

# --- Empty file check ---
printf '\n%sEmpty files%s\n' "$c_bold" "$c_reset"
empty="$(find "$AKOS_HOME/packs" "$AKOS_HOME/core" "$AKOS_HOME/agents" \
  "$AKOS_HOME/workflows" "$AKOS_HOME/scoring" "$AKOS_HOME/graphs" \
  "$AKOS_HOME/prompts" "$AKOS_HOME/templates" -type f -empty 2>/dev/null || true)"
if [ -z "$empty" ]; then ok "no empty files"; else fail "empty files found:"; printf '%s\n' "$empty" | sed 's/^/   /'; fi

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
  if "$AKOS_PYTHON" -m json.tool "$AKOS_HOME/$m" >/dev/null 2>&1; then ok "$m parses"
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
  if [ "$ver_issues" -eq 0 ]; then ok "manifest versions match VERSION ($ver)"; fi

  # Version is not the only duplicated field across the four manifests. A
  # one-line edit to the description in one file ships two different product
  # descriptions to two marketplaces with a green build. Compare the
  # user-visible descriptive fields too (plugin.json at top level,
  # marketplace.json at plugins[0]).
  if [ "$HAVE_PYTHON3" -eq 1 ]; then
    if "$AKOS_PYTHON" - "$AKOS_HOME" <<'PY'
import json, sys
home = sys.argv[1]
def fields(path, at_plugin):
    d = json.load(open(f"{home}/{path}"))
    src = d["plugins"][0] if at_plugin else d
    return {k: src.get(k) for k in ("displayName", "description", "license")}
manifests = [
    (".claude-plugin/plugin.json", False),
    (".codex-plugin/plugin.json", False),
    (".claude-plugin/marketplace.json", True),
    (".agents/plugins/marketplace.json", True),
]
vals = {p: fields(p, a) for p, a in manifests}
ref_path, ref = next(iter(vals.items()))
bad = False
for field in ("displayName", "description", "license"):
    seen = {p: v[field] for p, v in vals.items() if v[field] is not None}
    if len(set(seen.values())) > 1:
        bad = True
        print(f"{field} disagrees across manifests: {seen}")
sys.exit(1 if bad else 0)
PY
    then ok "manifest displayName/description/license agree"
    else fail "manifest descriptive fields drifted (see above)"
    fi
  fi

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

    # A plugin install resolves whatever is on the default branch at fetch
    # time, so the version a user runs must be tied to an immutable ref. Warn
    # when the current VERSION has no matching tag — merge-pr.sh creates it on
    # a release merge, but a local build or a bypassed merge can miss it.
    if git -C "$AKOS_HOME" rev-parse "v$ver" >/dev/null 2>&1; then
      ok "release tag v$ver exists"
    else
      warn "no git tag v$ver — releases should be tagged (merge-pr.sh does this; 'git tag -a v$ver' to backfill)"
    fi
  fi
fi

# --- Schema validation (advisory) ---
# Non-breaking by construction: schemas/v1/knowledge-pack.schema.json's required
# fields are exactly the 7 already universal across every pack, so this
# reports 0 errors against the existing corpus without any migration gate.
# Errors here fail the build; recommended-field warnings don't.
printf '\n%sSchema validation%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping schema validation (packs/agents/workflows)"
else
  validate_out="$("$AKOS_PYTHON" "$AKOS_HOME/schemas/validate.py" packs agents workflows --format json 2>&1)"
  validate_rc=$?
  if [ "$validate_rc" -gt 1 ]; then
    schema_errors="$(printf '%s' "$validate_out" | "$AKOS_PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['errors']) for r in d))" 2>/dev/null || echo "?")"
    schema_warnings="$(printf '%s' "$validate_out" | "$AKOS_PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['warnings']) for r in d))" 2>/dev/null || echo "?")"
    fail "schema validation: $schema_errors error(s) — run 'akos validate' for detail"
    [ "$schema_warnings" != "0" ] && [ "$schema_warnings" != "?" ] && warn "schema validation: $schema_warnings recommended-field warning(s)"
  elif [ "$validate_rc" -eq 0 ]; then
    schema_warnings="$(printf '%s' "$validate_out" | "$AKOS_PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(sum(len(r['warnings']) for r in d))" 2>/dev/null || echo "0")"
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

# --- Draft-pack routing isolation ---
# A pack's lifecycle status must have a real consequence: a draft pack must
# never silently become part of the stable "2-5 packs closest to the task"
# routing table, and no stable agent/workflow may depend on one.
printf '\n%sDraft-pack routing%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping draft-pack routing check"
else
  routing_out="$("$AKOS_PYTHON" "$AKOS_HOME/schemas/routing_check.py" 2>&1)"
  routing_rc=$?
  if [ "$routing_rc" -eq 0 ]; then
    ok "stable routing contains only stable packs; drafts are Experimental-only"
  elif [ "$routing_rc" -eq 2 ]; then
    fail "draft-pack routing violation(s):"
    printf '%s\n' "$routing_out" | sed 's/^/    /'
  else
    fail "routing check failed to execute (exit $routing_rc)"
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
  expired_out="$("$AKOS_PYTHON" "$AKOS_HOME/rules/runner.py" "$AKOS_HOME" --rule PACK_EXPIRED --format json 2>&1)"
  expired_rc=$?
  if [ "$expired_rc" -eq 1 ]; then
    fail "PACK_EXPIRED rule failed to run (exit $expired_rc)"
  else
    expired_count="$(printf '%s' "$expired_out" | "$AKOS_PYTHON" -c "import json,sys; print(len(json.load(sys.stdin)['findings']))" 2>/dev/null || echo "?")"
    if [ "$expired_count" = "0" ]; then
      ok "no packs past their review_after date"
    else
      warn "$expired_count pack(s) past review_after — run 'akos freshness --expired' for detail"
    fi
  fi
fi

# --- AKOS's own rule engine runs to completion ---
# The invariant that must hold is that the scan COMPLETES — every registry
# parses and every detector loads and runs (status != "error", zero
# ExecutionErrors). It is NOT "the repo has no CRITICAL": AKOS deliberately
# ships a vulnerable detector corpus under benchmarks/cases/** and
# evals/cases/** (SECURITY.md scopes it out) so the detectors have something
# to catch. Those fixtures legitimately produce CRITICAL/HIGH findings; a
# broken detector or registry does not. This checks the second thing, which
# is the one a path-based severity downgrade used to hide.
printf '\n%sSelf-scan%s\n' "$c_bold" "$c_reset"
if [ "$HAVE_PYTHON3" -eq 0 ]; then
  warn "python3 not found — skipping self-scan"
else
  self_out="$("$AKOS_PYTHON" "$AKOS_HOME/rules/runner.py" "$AKOS_HOME" --format json 2>&1)"
  self_status="$(printf '%s' "$self_out" | "$AKOS_PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(d['status'], d['summary']['errors'])" 2>/dev/null || echo "parse-error")"
  case "$self_status" in
    "error"*) fail "akos rules run did not complete — a detector or registry failed to run (run 'akos rules run .' for detail); this is not a clean result" ;;
    "parse-error") fail "akos rules run produced unparseable output; this is not a clean result" ;;
    *) ok "akos rules run completed — every detector and registry ran (findings on the vulnerable corpus are by design)" ;;
  esac
fi

# --- Executable bits ---
printf '\n%sExecutables%s\n' "$c_bold" "$c_reset"
for s in install.sh update.sh doctor.sh uninstall.sh merge-pr.sh bin/akos; do
  if [ -x "$AKOS_HOME/$s" ]; then ok "$s executable"; else warn "$s not executable (run ./install.sh)"; fi
done

# --- Symlinks ---
printf '\n%sSymlinks%s\n' "$c_bold" "$c_reset"
if [ -e "$HOME/DEV/AKOS" ]; then ok "$HOME/DEV/AKOS resolves"; else warn "$HOME/DEV/AKOS not found (run ./install.sh)"; fi
if [ -L "$HOME/bin/akos" ]; then ok "$HOME/bin/akos symlink present"; else warn "$HOME/bin/akos symlink absent (run ./install.sh)"; fi
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
