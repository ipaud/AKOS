# Contributing to AKOS

AKOS is a personal, reusable knowledge system, but it's structured so contributions (yours or others') stay consistent. This guide covers how to add or change packs, agents, and core rules.

## Ground rules

1. **Copyright discipline is absolute.** Distill ideas into original operational writing. Never copy paragraphs, reproduce long quotes, or mirror a book's chapter structure. Invented examples only. Cite sources by title/author/organization/URL only. See [core/source-policy.md](core/source-policy.md). A PR that reproduces source text will be rejected.
2. **The safety floor is non-negotiable.** Security, accessibility basics, and data integrity can't be relaxed by any pack. See [core/constitution.md](core/constitution.md).
3. **Every file ships meaningful content.** No placeholders, no "TBD". `doctor.sh` enforces the file contract but not quality — reviewers enforce quality.

## Adding a knowledge pack

```bash
akos create-pack <domain>/<name>     # scaffolds the 16-file structure
```

Then, per [core/knowledge-schema.md](core/knowledge-schema.md):

1. Set `metadata.yaml` — name, domain, authority level (0–4 per [core/authority-model.md](core/authority-model.md)), sources, tags, related packs.
2. Write `principles.md` **first** — it forces the distillation.
3. Derive `review-checklist.md` and `engineering-rules.md` from the principles.
4. Fill the rest: philosophy, mental-models, heuristics, decision-framework, anti-patterns, examples (invented), prompt-fragments, scoring-rubric, glossary, references, README.
5. Link the pack in the relevant [graphs/](graphs/) file.
6. Run `./doctor.sh` — the 16-file contract must pass, no empty files.

## Distinguishing content types

- **Principle** — always true in the domain ("users scan, they don't read").
- **Heuristic** — default with exceptions ("three clear clicks beat one ambiguous click").
- **Engineering rule** — checkable in an artifact ("touch targets ≥ 44×44pt").

If a linter could check it → engineering rule. "Usually" → heuristic. "Always" → principle.

## Adding or changing an agent

Agents in [agents/](agents/) follow a fixed shape: purpose, when-to-use, packs-to-load, review checklist, severity levels, scoring rubric, refusal/limits, and the unified Review Summary output format. Match the existing agents.

## Changing core rules

Core files ([core/](core/)) govern how every agent reasons. Changes here ripple everywhere — open an issue describing the reasoning change before a PR. If two packs conflict and the conflict isn't covered, extend [core/conflict-resolution.md](core/conflict-resolution.md) rather than patching one pack.

## The personal layer

`packs/personal/` is the owner's Level-0 layer. Forks should replace it with their own — don't PR changes to someone else's personal conventions.

## Before opening a PR

- [ ] `./doctor.sh` passes (structure + no empty files)
- [ ] No copied source text; sources cited by pointer only
- [ ] New packs linked in the relevant graph
- [ ] Content is operational — an agent reading it can *act*

## Versioning

Packs carry their own `VERSION` + `CHANGELOG.md`. The repo root carries the overall AKOS version. Bump per semver on meaningful changes.
