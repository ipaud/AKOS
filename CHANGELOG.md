# AKOS Changelog

All notable changes to AKOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows semver.

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
