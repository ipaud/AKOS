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
  a 303-line stdlib-only YAML parser (`schemas/yaml_subset.py`, no
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

## [1.5.0] — 2026-07-20

Opens a new top-level family. Until now AKOS packaged senior judgment about *software* — but when an agent builds the software, the result also depends on what it was given to see, which tools it could call, what it was allowed to do, and whether anything was actually verified. None of that had a home.

### Added

- **New `ai-engineering/` domain — 6 packs, 7649 lines.** Fase 1 of an AI-native expansion, scoped deliberately: six packs that change how AKOS works with coding agents, rather than fifty that restate the same articles.
  - `ai-engineering/context-engineering` (L2) — context as a finite resource, not a container: CE1–CE16, CEE1–CEE58, covering minimum sufficient context, progressive disclosure, just-in-time retrieval, poisoning and rot, instruction hierarchy, memory tiers, what must survive a compaction boundary, and why "load the whole repo" fails small as well as large. Self-referential: `skills/akos/SKILL.md`'s own routing table is critiqued as a worked example.
  - `ai-engineering/agent-foundations` (L2) — which shape a task warrants and how to bound it: AF1–AF18, AFE1–AFE72 across shape selection, routing, parallelization, orchestrator–worker, evaluator–optimizer, termination, budgets, error recovery, escalation, and idempotency. Spine: the agent is the *last* shape to reach for. Three anti-patterns are graded as correctness defects — silent truncation, double-charged retry, and action taken outside stated authority.
  - `ai-engineering/tool-design` (L2) — a tool built for a human is not automatically a good tool for an agent: TD1–TD16, TDE1–TDE86 on naming, structured input and output, actionable errors, idempotency, dry-run and destructive confirmation, result bounds, stable references, and MCP's tool/resource/prompt distinction.
  - `ai-engineering/coding-agents` (L2) — the process discipline of the edit itself: CA1–CA18, CAE1–CAE80 on orientation before editing, search before changing an interface, minimal patches that match existing conventions, testing before and after, and atomic reviewable commits. Spine: plausible is not correct.
  - `ai-engineering/agent-evals` (L2) — proving a change actually helped: AE1–AE18, AEE1–AEE76 on golden datasets, the four eval altitudes, the grader ladder, groundedness, cost and recovery as first-class dimensions, regression thresholds, flakiness, contamination, and baseline discipline.
  - `ai-engineering/agent-security` (**L1**) — the surface that appears when a model reads external content and then acts: AS1–AS18, ASE1–ASE95, 19 named anti-patterns. Spine: retrieved text, documents, web content and tool output are untrusted data, never instructions. Level 1 places it in the safety floor the constitution never waives, so its floor rules hold even in Prototype. Original models include the provenance ladder, the exfiltration triangle, and a control-vs-mitigation test that caps a score at 49 when prompt hardening is the whole defense.
- Five new cross-cutting nodes in `graphs/knowledge-graph.md` — untrusted content as data, executed evidence over plausible output, blast radius and least privilege, bounded work, plus `agent-security` joining the security floor and `agent-foundations` joining complexity-as-a-cost. Every link verified to resolve.

### Changed

- `core/authority-model.md` names two source kinds it previously left ambiguous: Anthropic/OpenAI engineering practice as published sits at **L2** (the same footing as the existing Google/Stripe entry), and replicated agent methodology papers such as ReAct and Reflexion at **L3**, once cross-verified per the source policy. Additive — no renumbering, no schema change, and no existing pack's cited level changes.

### Fixed

- **The schema validator declared a bound it never enforced.** `knowledge-pack.schema.json` has specified `minimum: 0, maximum: 4` on `authority-level` since the contract shipped, but `schemas/validate.py` implemented neither keyword — they were the schema's only use of them. Any pack could ship `authority-level: 9` and validate clean at exit 0. Reproduced first, then fixed, with three regression tests locking both directions and both boundaries; `bool` is excluded from the numeric check since it subclasses `int`. Unit suite 79 → 82.
- The bug was found while authoring `coding-agents`, by deliberately trying to make the validator fail rather than trusting its green — the discipline that pack exists to teach, so it is now also its own worked example.

### Validated — the six packs run against AKOS itself

The packs had never been used for anything. Six reviews were run, one per pack, against the AKOS surface each one governs — AKOS is an agent system (skills, 13 subagents, a routing table, a CLI, project-local memory), so it is a legitimate target for its own knowledge. Every finding below was re-verified here by execution before being acted on.

**What the packs found.** Fixed in this release: `history record` applied partially on malformed JSON, leaving an orphan review that `history list` cannot see; `history clean` deleted with no preview and no confirmation, `--keep` defaulting to 20; and a mistyped `--pack`/`--rule`/`--case` filter reported a clean run and exited 0 in three separate tools, so `freshness --pack no/such --fail-on expired` was a CI gate that could never fire. Also fixed: the two Level C benchmark cases could not fail.

**Still open, recorded rather than quietly carried:** nothing in `skills/`, `agents/`, or `core/` tells a reviewing agent that the project content it reads is data rather than instruction, while `.akos/config.md` from any cloned repo is treated as binding configuration; `history record` copies review reports verbatim with no redaction, into a directory `install-project` does not gitignore; `rules/`'s seven deterministic detectors are wired to no agent, and `security-reviewer` has no Bash tool so it cannot run its own safety-floor check deterministically; `backend-reviewer` carries profile weights but appears in no lens table; five agents still load `packs/personal/pau-avila/` hardcoded, which the 1.4.0 personal-profile decoupling missed.

**What the packs got wrong about themselves.** Two worked examples under-applied their own rules — see `tool-design` 1.1.0 and `coding-agents` 1.1.0. Three of the six reviews independently reported that their scoring rubric is miscalibrated for its target: applied mechanically, `agent-foundations` yields 2/100 on a system where ~45 of its 72 rules have no referent, and `context-engineering`'s uncapped per-drift deduction pushes a documentation-heavy repo two bands below what the evidence supports. Each reviewer declined to report the mechanical number and said why. One flagged a genuine methodological problem: `context-engineering`'s own `examples.md` already contained a critique of `skills/akos/SKILL.md`, the file at the centre of its review, making that portion circular by construction.

**Coverage, stated plainly.** All six reviews are static reads of instruction artifacts. No AKOS review has ever been run and recorded in an inspectable form, so every pack's CRITICAL tier — the transcript checks — went unexercised. "No CRITICALs found" in those tiers means "not testable with what was available", not "clean".

### Corrected — claims this project made about itself that were not true

Found by pointing the new `ai-engineering/` packs at AKOS itself, as the first real use of them. Each was established by running a command, not by re-reading the prose.

- **CI was red for the entire 1.4.0 release, and the 1.4.0 entry below announces it as delivered.** `gh run list` shows three consecutive failures on the `akos rules registry sanity` step: run `29733824899` on the 1.4.0 PR at 10:05:44Z, run `29733878337` on the `main` push at 10:06:35Z, and run `29739121045` at 11:36:02Z — 2h15m red across two merges. The 1.4.0 PR was merged with its own check failing, because the merge was gated on `mergeable`, never on `gh pr checks`.
- **The fix commit `d1a55c0` misdiagnosed the incident it fixed.** It states the workflows "had never actually run on GitHub" and that "the first real run failed in 12s". Both are false: they had run three times, and the 12s run was the third. The repair itself was verified by execution; the causal story around it was asserted from inference. A single `gh run list` would have settled it before the sentence was written. The real lesson is not "an unrun workflow slipped through" but "a visible red check was merged past" — which calls for branch protection, a control this repo still lacks.
- **`benchmarks/README.md` claimed every case was sabotage-verified.** One was (`supabase-rls-basic`, recorded in `b9e0b93`); the claim was generalized to all 21. A whole-engine sabotage pass has since confirmed the 19 deterministic cases genuinely go red — so they are live — but also found that **the 2 Level C cases cannot fail at all**: their `must_mention` phrases sit in their own `prompt`, the mock provider echoes the prompt, and the assertion checks that echo. Both pass with the fixture removed entirely. The defect was introduced by the M8 "fix" that made canned responses repeat their trigger phrases verbatim — closing the loop it was meant to open.
- `tests/README.md` said 79 tests; 82 run. `CHANGELOG` said the YAML parser is ~350 lines; it is 303, and was 303 at every commit.

None of these were caught by `doctor.sh`, the 82 unit tests, the 21 benchmark cases, or CI. Every one of them is a claim in prose that no check reads.

### Deferred, not dropped

Fase 2 (`memory-and-retrieval`, `governance-and-risk`, `human-agent-interaction`, `long-running-agents`) and Fase 3 (data-intensive systems, continuous delivery, evolutionary architecture, Shape Up) are scoped but unwritten. No reviewer lens or scoring file was added for `ai-engineering/` — these are build-mode packs routed through `skills/akos/SKILL.md`, exactly as `frontend/`, `backend/` and `devops/` are today. A dedicated review lens is a larger change this repo has not attempted, and it waits for a real review need rather than being invented ahead of one.

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
