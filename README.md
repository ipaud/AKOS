# AKOS — AI Knowledge Operating System

AKOS turns senior-level expertise — UX, product, architecture, security, accessibility, performance, testing, devops — into operational Markdown knowledge that any AI coding agent can load and act on. It lives once on your Mac at `~/DEV/AKOS` and plugs into every project.

AKOS is **not** a prompt collection, a notes folder, or a pile of book summaries. It is a reusable knowledge system: distilled principles, heuristics, engineering rules, checklists, decision frameworks, anti-patterns, review pipelines, and scoring rubrics — written in original wording, never copied from source material.

## Why it exists

AI coding agents write plausible code but make junior decisions: unclear navigation, inaccessible forms, leaky auth, feature-factory product thinking. The knowledge to prevent that exists in books, standards, and industry practice — but agents can't use knowledge they can't read. AKOS distills that knowledge into files agents *can* read, with an authority model so they know which source wins when advice conflicts.

## How it works

1. **Knowledge packs** (`packs/`) distill one source or domain each (e.g. `packs/ux/steve-krug/`, `packs/security/owasp-top-10/`). Every pack has the same 16-file structure — see [core/knowledge-schema.md](core/knowledge-schema.md).
2. **The core layer** (`core/`) defines how agents reason with the packs: [authority hierarchy](core/authority-model.md), [conflict resolution](core/conflict-resolution.md), [reasoning profiles](core/reasoning-profiles.md) (Prototype → Enterprise), and the [review pipeline](core/review-pipeline.md).
3. **Agents** (`agents/`) are reviewer role definitions — which packs to load, what to check, severity levels, and a unified report format.
4. **Workflows** (`workflows/`) chain agents for concrete tasks: new project, new feature, pre-release review.
5. **Scoring** (`scoring/`) provides 0–100 rubrics per dimension plus an overall score weighted by reasoning profile.
6. **Graphs** (`graphs/`) cross-link concepts across packs so agents can follow ideas between sources.
7. **The `akos` CLI** (`bin/akos`) wires AKOS into any project with marker-based, non-destructive file updates.

## Tool-agnostic by design

Everything is plain Markdown + Bash. Works with Claude Code, Codex CLI, Cursor, Gemini CLI, Continue, Cline, Roo Code, Windsurf, and any LLM agent that can read files.

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
./install.sh      # verifies structure, chmods scripts, symlinks ~/DEV/AKOS + ~/bin/akos
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

The generated files tell agents to read:

- `~/DEV/AKOS/core/constitution.md`
- `~/DEV/AKOS/core/authority-model.md`
- `~/DEV/AKOS/core/reasoning-profiles.md`
- `~/DEV/AKOS/core/review-pipeline.md`
- `~/DEV/AKOS/agents/` (as needed)
- `~/DEV/AKOS/packs/` (as needed)
- `~/DEV/AKOS/packs/personal/pau-avila/` (always)

## Use with specific tools

- **Claude Code** — `akos install-project` writes the AKOS section into `CLAUDE.md`. Claude reads it automatically. To run a review: paste `prompts/run-ux-review.md` or ask "run the AKOS UX review on this screen".
- **Codex CLI** — copy `templates/codex-instructions.md` into the project (or `AGENTS.md`, which Codex reads).
- **Cursor** — `akos install-project` creates `.cursor/rules/akos.mdc` (always-on rule pointing at AKOS).
- **Gemini CLI** — use `templates/gemini-instructions.md` as `GEMINI.md`.
- **Anything else** — `templates/generic-agent-instructions.md`.

## Run a review

Ask your agent, in any project with AKOS installed:

> Load AKOS. Act as `agents/ux-reviewer.md` with the Production profile and review the checkout screen.

Or use prompts in `prompts/` (`run-full-review.md`, `run-ux-review.md`, `run-security-review.md`, `run-architecture-review.md`). Every review agent produces the same report format with severity levels, scores, and a PASS / PASS WITH FIXES / BLOCKED decision.

## Add a new pack

```bash
akos create-pack ux/my-new-source
```

This scaffolds the 16-file structure. Fill it following [core/knowledge-schema.md](core/knowledge-schema.md) and the copyright rules in [core/source-policy.md](core/source-policy.md): distill, never copy; cite by title/author/URL only. `prompts/create-new-pack.md` is a ready prompt to have an agent draft it.

## Add personal rules

Edit files under `packs/personal/pau-avila/`. They are authority Level 0 — the highest — bounded only by law, security, and accessibility. `update.sh` never touches `packs/personal/`.

## Update safely

```bash
./update.sh    # preserves packs/personal/, prints changed files
./doctor.sh    # verify after update
```

## Repository layout

```
core/        how agents reason (constitution, authority, profiles, pipeline, scoring model)
packs/       knowledge packs by domain + personal layer
agents/      13 reviewer role definitions
workflows/   task-level review flows
templates/   per-tool integration templates
prompts/     ready-to-paste prompts
graphs/      concept cross-links between packs
scoring/     0–100 rubrics per dimension
bin/akos     CLI
```

## Copyright

AKOS distills ideas; it does not reproduce sources. No copied paragraphs, no long quotes, no chapter recreations. References cite title, author, organization, and official URL only. Full policy: [core/source-policy.md](core/source-policy.md).
