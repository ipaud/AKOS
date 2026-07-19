# AKOS Changelog

All notable changes to AKOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows semver.

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
