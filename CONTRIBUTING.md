# Contributing to AKOS

AKOS is a personal, reusable knowledge system, but it's structured so contributions (yours or others') stay consistent. This guide covers how to add or change packs, agents, and core rules.

## Ground rules

1. **Copyright discipline is absolute.** Distill ideas into original operational writing. Never copy paragraphs, reproduce long quotes, or mirror a book's chapter structure. Invented examples only. Cite sources by title/author/organization/URL only. See [core/source-policy.md](core/source-policy.md). A PR that reproduces source text will be rejected.
2. **The safety floor is non-negotiable.** Security, accessibility basics, and data integrity can't be relaxed by any pack. See [core/constitution.md](core/constitution.md).
3. **Every file ships meaningful content.** No placeholders, no "TBD". `doctor.sh` enforces the file contract but not quality — reviewers enforce quality.

## Adding a knowledge pack

```bash
akos create-pack <domain>/<name>     # scaffolds the 17-file structure
```

Then, per [core/knowledge-schema.md](core/knowledge-schema.md):

1. Set `metadata.yaml` — name, domain, authority level (0–4 per [core/authority-model.md](core/authority-model.md)), sources, tags, related packs.
2. Write `principles.md` **first** — it forces the distillation.
3. Derive `review-checklist.md` and `engineering-rules.md` from the principles.
4. Fill the rest: philosophy, mental-models, heuristics, decision-framework, anti-patterns, examples (invented), prompt-fragments, scoring-rubric, glossary, references, README.
5. Link the pack in the relevant [graphs/](graphs/) file.
6. Add the pack to the routing table in [skills/akos/SKILL.md](skills/akos/SKILL.md) — a pack that isn't listed there is a pack agents can't route to.
7. Run `./doctor.sh` — the 17-file contract must pass, every pack must appear in the routing table, no empty files.

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

`packs/personal/<name>/` holds Level-0 profiles — `pau-avila` ships as the default. Forks should `akos profile create <name>` their own rather than editing someone else's; don't PR changes to another person's personal conventions. See [docs/profiles/personal-profiles.md](docs/profiles/personal-profiles.md).

## Adding an executable rule

`rules/<domain>/<ID>.yaml` + a sibling `.py` exporting `run(files: list[Path]) -> list[dict]`. Full walkthrough: [docs/rules/authoring-rules.md](docs/rules/authoring-rules.md). The one rule that matters most: **write the true-positive test AND the realistic near-miss that shouldn't fire, in the same sitting, before trusting either.** Every one of the 8 shipped rules had a real bug this step caught — none would have been caught by the positive case alone.

## Adding a benchmark case

`benchmarks/cases/<id>/{fixture/,expected.yaml}`, then add it to `benchmarks/manifest.yaml`. See [benchmarks/README.md](benchmarks/README.md) and [docs/benchmarks/overview.md](docs/benchmarks/overview.md). Confirm the case can actually fail — deliberately break the detector, rerun, confirm the case fails, restore — before trusting that it's testing anything.

## Updating a source

A pack going stale: `akos freshness --pack <domain>/<name>` shows if it's due. Re-verify `principles.md` and `engineering-rules.md` against `references.md`'s sources, update the pack content per the copyright discipline above if anything changed, then bump `last_reviewed`/`review_after` in `metadata.yaml` (or just re-run `python3 bin/migrate-pack-metadata.py --pack <domain>/<name> --apply` to recompute `review_after` from today). See [docs/maintenance/freshness.md](docs/maintenance/freshness.md).

## Modifying scoring

`core/scoring-model.md`'s bands, anchors, and hard caps, and `core/review-pipeline.md`'s decision semantics, are load-bearing — changes ripple through every agent and every score. Prefer additive changes (see [docs/scoring/evidence-confidence-coverage.md](docs/scoring/evidence-confidence-coverage.md) for how the Coverage/confidence-tag addition stayed additive) over changing an existing formula. If a formula genuinely must change, update the one canonical Review Summary template copy in `agents/ux-reviewer.md` and its mirror in `core/review-pipeline.md` together — the other 12 agents reference the template by name and inherit automatically.

## Running tests

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
for t in tests/integration/test_*.sh; do bash "$t"; done
```

No pytest — stdlib `unittest` only, matching the project's one-accepted-dependency (`python3` itself) constraint. See [tests/README.md](tests/README.md). Every new detector or schema-affecting change needs a test that would have caught the bug it's fixing, not just a happy-path assertion — see `docs/rules/authoring-rules.md` for what that looks like in practice.

## Before opening a PR

- [ ] `./doctor.sh` passes (structure, schema validation, pack freshness, no empty files)
- [ ] `akos validate all` passes
- [ ] No copied source text; sources cited by pointer only
- [ ] New packs linked in the relevant graph and listed in `skills/akos/SKILL.md`
- [ ] Content is operational — an agent reading it can *act*
- [ ] New/changed rules have a benchmark case and a unit test covering the near-miss, not just the positive case
- [ ] `python3 -m unittest discover -s tests/unit` and every `tests/integration/test_*.sh` pass

## Versioning

Packs carry their own `VERSION` + `CHANGELOG.md`. The repo root carries the overall AKOS version. Bump per semver on meaningful changes. See [docs/migration/](docs/migration/) for version-range migration notes when a change affects how consuming projects use AKOS.
