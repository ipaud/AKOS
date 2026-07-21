# AKOS — AI Knowledge Operating System

AKOS turns senior-level expertise — UX, product, architecture, security, accessibility, performance, testing, devops — into operational Markdown knowledge that any AI coding agent can load and act on. It lives once on your Mac at `~/DEV/AKOS` and plugs into every project.

AKOS is **not** a prompt collection, a notes folder, or a pile of book summaries. It is a reusable knowledge system: distilled principles, heuristics, engineering rules, checklists, decision frameworks, anti-patterns, review pipelines, and scoring rubrics — written in original wording, never copied from source material.

## Why it exists

AI coding agents write plausible code but make junior decisions: unclear navigation, inaccessible forms, leaky auth, feature-factory product thinking. The knowledge to prevent that exists in books, standards, and industry practice — but agents can't use knowledge they can't read. AKOS distills that knowledge into files agents *can* read, with an authority model so they know which source wins when advice conflicts.

## How it works

1. **Knowledge packs** (`packs/`) distill one source or domain each (e.g. `packs/ux/steve-krug/`, `packs/security/owasp-top-10/`). Domain packs share a required-file structure (12 required files, 5 optional); personal packs under `packs/personal/` use a 10-file layout — see [core/knowledge-schema.md](core/knowledge-schema.md).
2. **The core layer** (`core/`) defines how agents reason with the packs: [authority hierarchy](core/authority-model.md), [conflict resolution](core/conflict-resolution.md), [reasoning profiles](core/reasoning-profiles.md) (Prototype → Enterprise), and the [review pipeline](core/review-pipeline.md).
3. **Agents** (`agents/`) are reviewer role definitions — which packs to load, what to check, severity levels, and a unified report format.
4. **Workflows** (`workflows/`) chain agents for concrete tasks: new project, new feature, pre-release review.
5. **Scoring** (`scoring/`) provides 0–100 rubrics per dimension plus an overall score weighted by reasoning profile.
6. **Graphs** (`graphs/`) cross-link concepts across packs so agents can follow ideas between sources.
7. **The `akos` CLI** (`bin/akos`) wires AKOS into any project with marker-based, non-destructive file updates.

## Tool-agnostic by design

The knowledge is plain Markdown; the CLI and lifecycle scripts are Bash, and the validation, rules, benchmark and eval tooling is dependency-free Python (stdlib only). Works with Claude Code, Codex CLI, Cursor, Gemini CLI, Continue, Cline, Roo Code, Windsurf, and any LLM agent that can read files.

## Authority model (short version)

| Level | Source | Wins when |
|-------|--------|-----------|
| 0 | Personal project rules (`packs/personal/`) | Always — unless it violates law, security, or accessibility |
| 1 | Official standards (WCAG, OWASP, NIST, Apple HIG, Material, RFCs) | Over everything below |
| 2 | Industry authorities (NN/g, Krug, Norman, Fowler) | Over books and community |
| 3 | Books & methodologies (Inspired, Lean Startup, Clean Architecture) | Over community |
| 4 | Community knowledge (blogs, repos, forums) | Only when nothing above speaks |

Security and accessibility form a floor that even Level 0 cannot override. Full model: [core/authority-model.md](core/authority-model.md). Conflicts: [core/conflict-resolution.md](core/conflict-resolution.md).

## Reasoning profiles

Reviews adapt to context via profiles: **Prototype**, **Startup MVP**, **Production**, **Enterprise**, **Game Dev**, **Internal Tool**. A prototype skips ceremony but never ships a security leak; production enforces the full pipeline. See [core/reasoning-profiles.md](core/reasoning-profiles.md).

## Install globally

Clone it anywhere — `install.sh` symlinks the canonical `~/DEV/AKOS` path for you:

```bash
git clone git@github.com:ipaud/AKOS.git ~/DEV/AKOS
cd ~/DEV/AKOS
./install.sh      # verifies structure, chmods scripts, symlinks ~/DEV/AKOS + ~/bin/akos,
                  # and links the skills into Claude Code and Codex CLI
./doctor.sh       # health check
```

(If you clone elsewhere, `install.sh` creates a `~/DEV` symlink so the canonical path still resolves.)

Add `~/bin` to your PATH if it isn't already:

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
```

## Integrate into a project

From any project folder:

```bash
akos install-project
```

This creates or updates `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/akos.mdc`, and `.akos/config.md` — appending AKOS sections between `<!-- AKOS:START -->` / `<!-- AKOS:END -->` markers. Existing content is never overwritten; reruns replace only the marked section.

On tools with skills (Claude Code, Codex CLI) the block is four lines — it just marks the project as AKOS-governed and points at `.akos/config.md`. The skills carry the bootstrap and load on demand, so nothing sits in context until it's needed. On Cursor and other rule-file tools the block keeps the full long-form bootstrap.

## Skills

AKOS ships two skills in `skills/`, using the open agent-skills format that **both Claude Code and Codex CLI** read — the same files serve both tools.

| Skill | What it does |
|---|---|
| `akos` | Build mode. Loads the constitution, sets the reasoning profile, loads the Level-0 personal layer, and routes to the 2-5 relevant packs. |
| `akos-review` | Review mode. Runs the twelve-lens pipeline (full or a single targeted lens) and emits the unified Review Summary. |

`./install.sh` links them into `~/.claude/skills/` and `~/.agents/skills/` as symlinks, so edits to your packs are live in both tools immediately. Check with:

```bash
akos list-skills
```

## Use with specific tools

- **Claude Code** — invoke `akos` or `akos-review`; both also fire automatically when the task matches. `akos install-project` marks the project and sets the profile.
- **Codex CLI** — same two skills via `~/.agents/skills/`. `/skills` lists them; `$akos` invokes explicitly. Details in `templates/codex-instructions.md`.
- **Cursor** — `akos install-project` creates `.cursor/rules/akos.mdc` (always-on rule with the full bootstrap; Cursor has no skills).
- **Gemini CLI** — use `templates/gemini-instructions.md` as `GEMINI.md`.
- **Anything else** — `templates/generic-agent-instructions.md`, or paste `prompts/load-akos.md`.

## Install as a plugin

Instead of cloning, AKOS can be installed as a plugin in either tool:

```bash
# Claude Code
/plugin marketplace add ipaud/AKOS
/plugin install akos@akos

# Codex CLI
codex plugin marketplace add ipaud/AKOS
```

A plugin install is a **copy** in a cache directory. That is right for trying AKOS or sharing it; for your own working copy prefer the clone + `install.sh` symlinks above, so edits to your packs take effect immediately.

## Run a review

Ask your agent, in any project with AKOS installed:

> Run the AKOS UX review on the checkout screen.

That fires `akos-review`, which resolves the lens, loads `agents/ux-reviewer.md` and its packs, and reports. Say "run the full AKOS review" for all twelve lenses.

On tools without skills, use the prompts in `prompts/` (`run-full-review.md`, `run-ux-review.md`, `run-security-review.md`, `run-architecture-review.md`). Every review agent produces the same report format with severity levels, scores, and a PASS / PASS WITH FIXES / BLOCKED decision.

## Add a new pack

```bash
akos create-pack ux/my-new-source
```

This scaffolds the required files (optional file-types are added by hand when the source has something distinct to say). Fill it following [core/knowledge-schema.md](core/knowledge-schema.md) and the copyright rules in [core/source-policy.md](core/source-policy.md): distill, never copy; cite by title/author/URL only. `prompts/create-new-pack.md` is a ready prompt to have an agent draft it.

## Add personal rules

Edit files under `packs/personal/pau-avila/` (the shipped default profile). They are authority Level 0 — the highest — bounded only by law, security, and accessibility. `update.sh` never touches `packs/personal/`.

Want your own profile instead of forking pau-avila's? `akos profile create <name>` scaffolds a sibling under `packs/personal/`, and `akos profile use <name>` points the current project's `.akos/config.md` at it (`personal_profile:` field — see [`docs/profiles/personal-profiles.md`](docs/profiles/personal-profiles.md)).

## Update safely

```bash
./update.sh    # preserves packs/personal/, prints changed files
./doctor.sh    # verify after update
```

`update.sh` backs up `packs/personal/` to `~/.akos-backups/` before pulling and
aborts if that backup can't be written.

**Rolling back.** Releases are git-tagged (`vX.Y.Z`). To return to an earlier
one:

```bash
git checkout v1.7.0 && ./install.sh
```

`git tag -l` lists available versions; `./doctor.sh` reports the running one.

## Quality infrastructure

Beyond the knowledge itself, AKOS validates and tests its own consistency:

```bash
akos validate all              # schema-check packs/agents/workflows
akos rules run <project-dir>   # 8 executable checks: RLS, secrets, a11y, migrations...
akos benchmark run             # regression suite for the rules above
akos freshness                 # which packs are due for a re-read
akos profile create|use <name> # your own Level-0 layer instead of the shipped default
akos history compare <a> <b>   # score/decision deltas across two recorded reviews
```

Full docs: [`docs/architecture/`](docs/architecture/) (a dated v1.3.0 baseline + target system), [`docs/contracts/`](docs/contracts/) (pack/agent/workflow schemas), [`docs/rules/`](docs/rules/authoring-rules.md), [`docs/benchmarks/`](docs/benchmarks/overview.md), [`docs/scoring/`](docs/scoring/evidence-confidence-coverage.md), [`docs/profiles/`](docs/profiles/personal-profiles.md), [`docs/reviews/`](docs/reviews/history-and-comparison.md), [`docs/maintenance/`](docs/maintenance/freshness.md), [`docs/cli/`](docs/cli/exit-codes.md), [`docs/migration/`](docs/migration/v1.1-to-next.md). Tests: [`tests/README.md`](tests/README.md). CI: `.github/workflows/`.

## Repository layout

```
core/         how agents reason (constitution, authority, profiles, pipeline, scoring model)
packs/        knowledge packs by domain + personal layer(s)
agents/       13 reviewer role definitions
skills/       akos + akos-review (Claude Code and Codex CLI)
workflows/    task-level review flows
templates/    per-tool integration templates
prompts/      ready-to-paste prompts (fallback for tools without skills)
graphs/       concept cross-links between packs
scoring/      0–100 rubrics per dimension
schemas/      JSON Schema contracts + the validator + the YAML parser
rules/        executable checks (Level A/B) — the rules registry + runner
benchmarks/   reproducible regression cases for rules/
tests/        unit (Python unittest) + integration (bash) test suites
docs/         architecture, contracts, rules, benchmarks, scoring, profiles,
              reviews, maintenance, cli, and migration documentation
bin/akos      CLI
```

## Copyright

AKOS distills ideas; it does not reproduce sources. No copied paragraphs, no long quotes, no chapter recreations. References cite title, author, organization, and official URL only. Full policy: [core/source-policy.md](core/source-policy.md).
