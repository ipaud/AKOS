# AKOS Changelog

All notable changes to AKOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows semver.

## [1.4.0] — 2026-07-20

Quality infrastructure: AKOS gains a verification layer around its
knowledge — schemas, executable rules, benchmarks, evidence-aware
scoring, freshness tracking, review history, personal-profile
decoupling, CI, and tests. No pack content, no agent prose, no reasoning
profile, and no review-pipeline decision logic changed — everything here
is additive, verified against the pre-existing corpus at every step.
Full detail in `docs/architecture/target-system.md` (design decisions
and alternatives considered) and `docs/migration/v1.1-to-next.md`
(what a consuming project needs to know — nothing breaks).

### Added

- **Contracts** — `schemas/{knowledge-pack,agent,workflow}.schema.json`,
  a ~350-line stdlib-only YAML parser (`schemas/yaml_subset.py`, no
  PyYAML/ruamel), and `bin/migrate-pack-metadata.py` (idempotent,
  append-only, already run against all 48 pre-existing packs).
- **`akos validate [packs|agents|workflows]`** — schema validation,
  `0`/`1`/`2` exit codes, `--format json`. Wired into `doctor.sh`'s new
  advisory Schema validation section.
- **`akos profile list|show|create|use`** — decouples the Level-0
  personal layer from a single hardcoded name (`pau-avila` stays the
  default; `.akos/config.md` gained a `personal_profile` field).
  `packs/personal/_template/` scaffolds new profiles.
- **Executable rules** (`rules/`) — 8 detectors (`SUPABASE_RLS_DISABLED`,
  `SUPABASE_POLICY_TOO_PERMISSIVE`, `SECRET_IN_SOURCE`,
  `SERVICE_ROLE_IN_CLIENT`, `A11Y_INPUT_NO_LABEL`,
  `MIGRATION_NO_DOWN_FILE`, `DESTRUCTIVE_MIGRATION_NO_GUARD`,
  `PACK_EXPIRED`), filesystem-discovered like `packs/` itself.
  `akos rules list|run|explain`.
- **Evidence-aware scoring** — the Review Summary template gained a
  `## Coverage` section and per-finding `(Confidence: ...)` tags.
  Additive only: no band, anchor, cap, or decision rule changed.
- **`akos freshness`** — full band report (fresh/review-due-soon/
  review-due/expired/unknown) over pack `review_after` dates.
- **Benchmarks** (`benchmarks/`) — 21 reproducible cases, a
  provider-agnostic Level-C interface (mock provider required and the
  only one CI uses; an optional local `claude`/`codex` CLI passthrough
  is documented, not wired by default). `akos benchmark run|list`.
- **`akos history record|list|show|latest|compare|clean`** — project-
  local (`.akos/reviews/`) review history; `akos-review`'s skill
  instructions record every review's decision and scores automatically.
- **CI** (`.github/workflows/`) — PR checks, main-branch benchmark +
  artifact upload, weekly freshness check.
- **Tests** (`tests/`) — 79 unit tests (stdlib `unittest`, no pytest) +
  4 integration scripts (bash, `mktemp -d`).
- **Docs** — `docs/architecture/`, `docs/contracts/`, `docs/rules/`,
  `docs/benchmarks/`, `docs/scoring/`, `docs/profiles/`,
  `docs/reviews/`, `docs/maintenance/`, `docs/cli/`, `docs/migration/`.

### Fixed

- **`write_marked_section`** (the helper `install-project` depends on
  for every rerun) silently failed on this machine's BSD awk whenever it
  needed to *replace* an already-marked section — `awk -v` cannot accept
  a multi-line value, exits nonzero with no output, and `set -e` aborted
  before the file was ever rewritten. A prior "rerun idempotency" check
  had passed by coincidence (the target content hadn't changed between
  runs, so a silently-failed no-op looked identical to a successful one).
  Replaced with a portable sed-line-range splice.
- The 16-vs-17-file pack contract inconsistency finally fully closed
  (VERSION/CHANGELOG references were the last stragglers).

Five more real bugs were found and fixed by testing each new component
against a real or synthetic case before trusting it — not hypothetical,
all reproduced and fixed in this range: a suppression-comment window too
narrow (checked only the exact evidence line), a fixture-path exclusion
matching "test" as a substring instead of a path segment, an anon-role
JWT wrongly flagged as a secret, a `freshness --fail-on` severity
comparison inverted, and a benchmark harness resolving fixture paths
against the wrong base directory. Each is documented in its own commit
and cross-referenced in the relevant `docs/` page — the point isn't that
bugs happened, it's that testing before trusting caught every one of
them before they shipped.

## [1.3.0] — 2026-07-19

Closes the second of the two lenses that had no domain of their own, and validates the first against a real production screen.

### Added

- **New `mobile/` domain — 2 packs, 2618 lines.** `mobile-reviewer` was running on borrowed platform-design and usability packs while Article 9 makes responsive review mandatory for every web surface.
  - `mobile/responsive-web` (L2) — layout and adaptation: breakpoint strategy from content, fluid type, container queries, the 320px floor and WCAG reflow, and a five-rung **reflow→restructure ladder** whose rule is that "we made it scroll" is not a rung. Two distinguishing principles: anything the user must read *while acting* must be visible while they act, and precedent transfers only with its conditions (read-only → editable voids the exemption).
  - `mobile/touch-ergonomics` (L2) — the hand and the device: a computable non-overlap rule `gap ≥ F − (wA + wB)/2`, thumb zones, hover-free design, the virtual keyboard, and locale input parsing. Silent coercion of a locale decimal into `0` is scored as a correctness defect, not an ergonomics nit. Its **enforcement-surface** model ranks where a rule lives — primitive, build check, runtime backstop, review, doc — and caps a documented-but-bypassable rule at 79.
- **`scoring/mobile-score.md`** — pipeline step 4 had no score file, unlike every other scored lens. Now it has one, with caps for untested viewports and unenforceable rules.
- `agents/mobile-reviewer.md` loads both packs as primary and scores against the new file.

### Changed

- `agents/copy-reviewer.md`: `content/gov-uk-content-design` is now **conditional, not a default load**. Validated on a real control-dense editor where it fired on one finding out of nineteen while `ux-writing` produced the rest — loading it there costs context and returns almost nothing.

### Validated

The `content/` packs were re-run against the same production screen reviewed before they existed: **69 / PASS WITH FIXES → 52 / BLOCKED**. The packs found defects judgment alone had missed — six confirmations fired before their mutation settles, two of which fire when the handler provably did nothing, one of them navigating to a URL built from `undefined`. The prior review had seen only the visible symptom, "a double toast". The difference was not insight but insistence: the rubric prices a confirmation that can fire on a failed operation as a correctness defect and refuses the trade a human reviewer would have negotiated.

## [1.2.0] — 2026-07-19

### Added

- **New `content/` domain — 2 packs, 2073 lines.** `copy-reviewer` was one of the twelve pipeline lenses running entirely on borrowed UX packs, with no domain of its own. It now has one.
  - `content/ux-writing` (L3) — interface words: labels, error anatomy, empty states, voice and tone, confirmation copy, writing for translation. Its spine is that a label is a promise the code must keep, so the truthfulness pass reads the handler rather than the string. Anti-patterns are a named taxonomy: the lying label, phantom confirmation, capability cosplay, synonym drift, tooltip-only meaning, the dead-end empty state.
  - `content/gov-uk-content-design` (L2) — content design as meeting a user need: plain language, front-loading, readability targets, scanning, and retiring stale content. Numeric targets are checkable rules rather than advice.
  - Both grounded in real production-audit findings so they catch defects instead of reading as editorial taste. Scope boundary is explicit in each README, and they cross-link rather than overlap.
- `agents/copy-reviewer.md` loads them as primary, ahead of the borrowed UX packs.
- Both listed in the `akos` routing table with their "reach for it when" clause.

### Changed

- Routing hints, subagents, config-reading and the technical-pack fragments shipped since 1.1.0 were never versioned. This release carries them.

## [1.1.0] — 2026-07-19

AKOS is now directly invocable as a skill in Claude Code and Codex CLI, instead of relying on an instruction block telling the agent to go read files.

### Added

- `skills/akos` — build mode. Bootstraps the constitution, sets the reasoning profile from `.akos/config.md`, loads the Level-0 personal layer, and routes to the 2-5 relevant packs via an inline domain→pack table.
- `skills/akos-review` — review mode. Resolves a targeted or full run of the twelve-lens pipeline and emits the unified Review Summary.
- Both skills use the open agent-skills format read by **both** Claude Code and Codex CLI — one set of files, two tools.
- Plugin manifests for both ecosystems: `.claude-plugin/{plugin,marketplace}.json` and `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`. AKOS is installable with `/plugin marketplace add ipaud/AKOS` or `codex plugin marketplace add ipaud/AKOS`.
- `akos list-skills`.
- `doctor.sh` skill checks: frontmatter validity, name/directory agreement, JSON manifest parsing, manifest-version/VERSION agreement, symlink presence, and — the anti-drift guard — that **every pack appears in the `akos` routing table**.

### Changed

- `install.sh` links both skills into `~/.claude/skills/` and `~/.agents/skills/` as symlinks, so pack edits are live in both tools with no reinstall. `uninstall.sh` removes only links that point back into this repo.
- `akos install-project` now writes a four-line block into `CLAUDE.md` and `AGENTS.md` instead of a twenty-line bootstrap — the skills carry the bootstrap and load on demand. The Cursor rule keeps the long form (Cursor has no skills).
- `templates/{CLAUDE,AGENTS,codex-instructions}.md` document the skill-based integration. `templates/{cursor-rule.mdc,gemini-instructions.md,generic-agent-instructions.md}` keep the long-form bootstrap for tools without skill support.
- `prompts/load-akos.md` is now labelled as the manual fallback for those tools.

### Fixed

- The pack contract is documented as **17 files** everywhere. It was described as 16 in `README.md`, `core/knowledge-schema.md`, `core/source-policy.md`, `CONTRIBUTING.md`, `prompts/create-new-pack.md`, `doctor.sh`, and `bin/akos`, while the schema table, `doctor.sh`'s own checks, `create-pack`'s output, and all 44 packs on disk were always 17.

## [1.0.0] — 2026-07-09

### Added

- Core reasoning layer: constitution, authority model, conflict resolution, reasoning profiles, review pipeline, decision framework, confidence model, knowledge schema, scoring model, reasoning engine, source policy.
- 44 knowledge packs across ux, architecture, product, security, performance, frontend, backend, testing, devops.
- Deep Tier-1 UX packs: steve-krug, don-norman, nielsen-norman-group, laws-of-ux, wcag.
- Personal layer: packs/personal/pau-avila.
- 13 review agents with unified output format and severity levels.
- 9 workflows mapping the review pipeline to concrete tasks.
- 7 scoring rubrics (0–100, banded).
- 5 knowledge graphs cross-linking packs by concept.
- Templates for Claude Code, Codex, Cursor, Gemini, and generic agents.
- Prompts for loading AKOS and running reviews.
- Installer, doctor, updater, uninstaller, and `akos` CLI with marker-based project integration.
