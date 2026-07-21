# AKOS — Architecture Baseline (v1.3.0, historical)

> **This is a dated baseline, not the current state.** It captures the
> repository as of **v1.3.0** and is kept as the starting point the
> quality-infrastructure work (`schemas/`, `rules/`, `benchmarks/`, `evals/`,
> `tests/`, `.github/`, `docs/` — all of which **now exist**, contrary to the
> "Not present today" note below) was layered onto. Counts below (49 packs, 10
> commands, six config sections, …) are the v1.3.0 numbers and have since
> drifted — for live counts run `./doctor.sh`. Do not read this as an
> inventory of the system as it stands.

Snapshot as of v1.3.0, written from a direct audit of the repository (not from memory or aspiration). This is the baseline the quality-infrastructure work (schemas, validation, rules, benchmarks, CI, tests — see `docs/migration/v1.1-to-next.md`) builds on top of, additively.

## Components

| Directory | What it is | Count | Machine-readable today? |
|---|---|---|---|
| `core/` | How agents reason: constitution, authority model, conflict resolution, confidence model, scoring model, decision framework, reasoning engine, reasoning profiles, review pipeline, knowledge schema, source policy | 11 files | No — prose, read by LLM agents only |
| `packs/<domain>/<name>/` | Distilled knowledge, one source or domain each | 49 packs, 17-file contract | Partial — `metadata.yaml` is YAML, hand-written, never schema-validated |
| `packs/personal/pau-avila/` | Level-0 personal rules — the one sanctioned exception to the 17-file contract | 10 files, no `metadata.yaml` | No |
| `agents/*.md` | 13 review-lens role definitions | 13 files, YAML frontmatter (`name`, `description`, `tools`) + prose body | Frontmatter only |
| `skills/{akos,akos-review}/SKILL.md` | The Claude Code / Codex CLI entry points — bootstrap + build mode, and the 12-lens review pipeline | 2 files | No — LLM-read only |
| `workflows/*.md` | Chained-agent task recipes | 9 files | No frontmatter at all today |
| `scoring/*.md` | 0–100 rubrics per dimension | 8 files (ux, accessibility, architecture, security, performance, product, overall, mobile) | No |
| `graphs/*.md` | Concept cross-links between packs | 5 files | No |
| `templates/*` | Per-tool integration snippets (Claude, Codex, Cursor, Gemini, generic) | 7 files | No |
| `prompts/*.md` | Ready-to-paste bootstrap/review prompts | 6 files | No |
| `bin/akos` | The CLI | 1 file, 266 lines | Bash |
| `install.sh` / `update.sh` / `doctor.sh` / `uninstall.sh` | Lifecycle scripts | 4 files | Bash |
| `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Plugin manifests for both tools' marketplaces | 4 JSON files | Yes — the only JSON in the repo before this work |

**Not present today**: `tests/`, `.github/`, `schemas/`, `benchmarks/`, `rules/`, `docs/` (beyond what this work adds). This is a from-scratch build for all of those, not an extension of partial infrastructure.

## Flows

### Build mode (an agent writing code)
`akos` skill loads → constitution + authority model + reasoning profile → reads `.akos/config.md` in the target project (profile, context, overrides, always-load packs, style direction, notes) → Level-0 personal layer → 2-5 task-routed packs (inline "reach for it when" table in `skills/akos/SKILL.md`) → applies pack principles as constraints, cites authority level, emits tradeoff statements on conflict.

### Review mode (an agent judging an artifact)
`akos-review` skill loads → same config read → resolves one lens or the full 12-step pipeline → for a full run, delegates independent lenses (1–10) to Claude Code subagents in parallel (`akos-<lens>-reviewer`, real subagents since v1.3.0 via YAML frontmatter on `agents/*.md`), runs lenses 11 (personal rules) and 12 (release readiness) inline last, merges into **one** Review Summary → severity/weight-driven decision: PASS / PASS WITH FIXES / BLOCKED.

### CLI (`bin/akos`)
`main()` dispatches on `case "$cmd"` to `cmd_<name>()` functions. Ten commands exist today: `help, doctor, install-project, link-project, list-packs, list-agents, list-skills, show-profile, review, create-pack`. Exit convention: functions `return 1` on their own validation failure (propagates via `set -e`); only the top-level unknown-command branch does explicit `exit 1`. No other exit codes exist anywhere.

### `.akos/config.md` — project-local state
Scaffolded by `akos install-project` into a *consuming* project (never this repo). Six sections today: Reasoning profile, Project context, Profile overrides, Packs to always load, Style direction, Notes. Read only by LLM agents per skill instructions — no script in this repo parses it programmatically.

## Contracts that exist today

- **The 17-file pack contract** (`core/knowledge-schema.md`) — file-presence only, enforced by `doctor.sh`'s glob-and-check loop. Never validates YAML *content* (is `authority-level` an integer 0–4? is `sources` really a list of `{title,author,url}`?).
- **`metadata.yaml`** — 7 fields universal across all 48 non-personal packs, confirmed by direct inspection: `name, domain, authority-level, version, tags, sources, related`. 2 packs additionally carry `platform-scope`. No schema; hand-written; never structurally validated.
- **Agent frontmatter** — `name` (pattern `akos-<lens>-reviewer`), `description`, `tools` (a comma-joined **string**, not a YAML list — confirmed across all 13, not assumed). Checked today only by `doctor.sh`'s hand-rolled `awk`/`sed` extraction (not a real YAML parser).
- **The Review Summary template** — one canonical copy embedded verbatim in `agents/ux-reviewer.md` and mirrored in `core/review-pipeline.md`; the other 12 agents reference it by name with an agent-specific one-line addendum about which score line they fill.
- **The akos routing table anti-drift guard** — `doctor.sh` fails if any pack under `packs/` doesn't appear in `skills/akos/SKILL.md`'s routing table. The one place AKOS already enforces "the index must not silently drift," and the design precedent this work's rules registry follows (filesystem-discovered, not a second hand-maintained index).

## Extension points (where this work attaches)

1. **`metadata.yaml`** — additively extensible; every field this work adds is optional-with-default, so the schema validates all 48 existing packs with zero errors on day one.
2. **`bin/akos`'s `cmd_<name>()` + `case` dispatch** — the exact pattern every new command (`validate`, `rules`, `benchmark`, `freshness`, `profile`, `history`) follows.
3. **`doctor.sh`'s `ok()/warn()/fail()` counter pattern** — the exact pattern the new advisory sections (schema validation, pack expiry) fold into, ending on the same bare `[ "$failc" -eq 0 ]` exit convention.
4. **`packs/personal/*` glob-generic handling** in `doctor.sh`/`update.sh`/`uninstall.sh` — already multi-profile-safe; only the *prose* (skills, constitution, templates) hardcodes `pau-avila` by name.

## Known limitations / risks carried forward, not fixed by this work

- No `command -v` guard exists anywhere for `python3` — the repo's one external dependency. `doctor.sh` would throw a raw "command not found" rather than a graceful degrade on a machine without Python 3. (Addressed in M10 — CI workflow — as a small, separate fix.)
- Scripts assume `set -e` semantics differ intentionally between `bin/akos` (`-euo pipefail`) and the four lifecycle scripts (`-uo pipefail`, no `-e`, because `doctor.sh` must keep tallying failures rather than abort on the first one). Any new script joining this family must pick the right one deliberately, not by copy-paste.
- Portability is unstressed-but-intact: no `sed -i`, no GNU-only flags, no bash 4+ features anywhere — works on macOS's stock bash 3.2. New scripts must preserve this.

## Decisions to conserve (do not relitigate without new facts)

- Distill, never copy (`core/source-policy.md`) — packs contain original operational writing, sources cited by pointer only. This is a legal/ethical constraint, not a style preference.
- The safety floor (Constitution Article 2: security, accessibility basics, data integrity) is never waived by any reasoning profile, at any authority level. Any new scoring/decision logic must preserve this.
- Level 0 (`packs/personal/`) outranks every external source but sits below the safety floor (Article 2) — this ordering must survive the personal-profile decoupling work unchanged.
