# Personal profiles

AKOS's Level 0 layer — the owner's own conventions, always applied, outranking every external source but never the safety floor (`core/constitution.md` Article 2) — lives at `packs/personal/<name>/`. Multiple profiles can coexist as siblings; a project picks one via `.akos/config.md`'s `personal_profile` field.

## Why this exists

Before this, `packs/personal/pau-avila/` was the only profile, and its path was hardcoded across 8 load-bearing files (both skills, the constitution's loading order, `core/reasoning-engine.md`, `core/knowledge-schema.md`, `prompts/load-akos.md`, and 4 project-integration templates). `doctor.sh`, `update.sh`, and `uninstall.sh` were already generic — they glob `packs/personal/*` and never named a specific profile — so the only work was in the *prose* agents read, not the scripts.

## Location — deliberately not a new `profiles/` tree

Personal profiles stay under `packs/personal/<name>/`, not a parallel top-level directory. `doctor.sh`'s pack-contract check, `update.sh`'s preservation logic, and `uninstall.sh`'s backup-on-delete all already operate on this path generically — moving it would mean rewriting three working scripts to fragment "packs" as a concept, for no gain. `core/authority-model.md` already defines Level 0 structurally ("Location: `packs/personal/`"), not by name, so it required no change at all.

## The 10-file contract

Different from the standard knowledge-pack contract (`core/knowledge-schema.md`) — a personal profile encodes one person's preferences, not a distillation of an external source, so it has no `metadata.yaml`, no `philosophy.md`, no `scoring-rubric.md`.

| File | Purpose |
|---|---|
| `README.md` | What this profile is, in one screen |
| `principles.md` | Durable working principles — write this first |
| `ai-agent-rules.md` | How you want an agent to behave: tone, defaults, what NOT to do |
| `coding-preferences.md` | Stack, style, and pattern preferences |
| `ux-preferences.md` | UX/copy defaults applied without being asked |
| `design-language.md` | Visual identity, for projects with UI |
| `project-patterns.md` | Recurring structural choices across your projects |
| `supabase-rules.md` | Only relevant if you use Supabase |
| `VERSION`, `CHANGELOG.md` | Same as every pack |

## Using a profile

Every project's `.akos/config.md` (written by `akos install-project`) has a `## Personal profile` section:

```markdown
## Personal profile
personal_profile: pau-avila
```

**Absent or unset defaults to `pau-avila`** — every project scaffolded before this field existed keeps working identically; nothing to migrate.

## CLI

```bash
akos profile list                    # what's available under packs/personal/
akos profile show <name>             # README.md + principles.md
akos profile create <name>           # scaffold a new 10-file profile from packs/personal/_template/
akos profile use <name> [project-dir]  # set personal_profile in .akos/config.md (default: current dir)
```

`akos profile create` copies `packs/personal/_template/` and fills in the `<your name>` placeholder across all 10 files. `akos profile use` rewrites just the `personal_profile:` line inside the project's existing `.akos/config.md`, via the same marker-safe helper `install-project` uses — it requires `.akos/config.md` to already exist (run `akos install-project` first).

## What did *not* change

The ~30 citation-style references across `agents/*.md`, `workflows/*.md`, `graphs/*.md`, and a handful of pack cross-links (e.g. "per pau-avila principle 2") were **deliberately left as-is**. They cite specific principle *numbers* of `pau-avila`'s actual content — a different profile wouldn't share that numbering, so genericizing the prose would misrepresent what's being cited. Revisit this only if a second profile is actually created and put into real use.
