# Executable rules

Deterministic (Level A) and heuristic (Level B) checks a script can run against real code — the counterpart to the knowledge packs' prose. Where a pack's `engineering-rules.md` says a rule *should* hold, a rule here can actually check whether it *does*.

## Structure — filesystem is the registry

```
rules/<domain>/<RULE_ID>.yaml    # metadata: severity, confidence, applies_to, recommendation
rules/<domain>/<rule-id>.py      # the detector: run(files: list[Path]) -> list[dict]
```

No central index file. Rules are discovered by globbing `rules/*/*.yaml`, the same way `packs/` is discovered by globbing `packs/*/*/` — a hand-maintained index would recreate the exact drift risk `doctor.sh`'s pack-routing-table guard exists to catch. Every discovered registry is validated against the strict v1 contract in `rules/rule_schema.py`; missing, mistyped, unknown, or invalid fields make discovery incomplete rather than silently falling back.

## Level A vs Level B

- **Level A** — deterministic, offline, no LLM. A script either finds the pattern or it doesn't.
- **Level B** — heuristic. The detection mechanism is still a deterministic script, but the underlying question can't be answered by text-matching alone (e.g. real HTML/JSX label association is a tree-structural relationship, not a regex). Level B rules are capped at MEDIUM severity regardless of profile and are excluded from CRITICAL-only exit-code gating.
- **Level C** (LLM-assisted) is not implemented as executable rules — see `benchmarks/` for how the harness handles optional LLM-assisted evaluation.

## The 8 rules shipped today

| Rule | Domain | Level | Default severity |
|---|---|---|---|
| `SUPABASE_RLS_DISABLED` | security | A | CRITICAL |
| `SUPABASE_POLICY_TOO_PERMISSIVE` | security | A | HIGH |
| `SECRET_IN_SOURCE` | security | A | HIGH |
| `SERVICE_ROLE_IN_CLIENT` | security | A | HIGH |
| `A11Y_INPUT_NO_LABEL` | accessibility | B | MEDIUM (capped) |
| `MIGRATION_NO_DOWN_FILE` | devops | A | HIGH |
| `DESTRUCTIVE_MIGRATION_NO_GUARD` | devops | A | HIGH |
| `PACK_EXPIRED` | meta | A | MEDIUM |

`PACK_EXPIRED` is different from the other seven: it scans AKOS's own `packs/`, not a consuming project's source (`applies_to.target: akos-packs`), and is dual-wired directly into `doctor.sh` for that reason.

## Suppression

A registry is suppressible by default. For those rules, a comment `akos:allow RULE_ID` on or within a few lines before a finding's evidence line suppresses it — checked centrally by the runner, so individual detectors never reimplement suppression logic.

Security-floor rules whose evidence always needs review declare `suppressible: false`. `SECRET_IN_SOURCE`, `SERVICE_ROLE_IN_CLIENT`, and `SUPABASE_RLS_DISABLED` use that policy: an in-source comment cannot waive a credential leak, a service-role client reference, or a missing RLS boundary.

## Running

```bash
akos rules list
akos rules run <dir> [--rule ID] [--domain D] [--target project-source|akos-packs|all]
                    [--profile NAME] [--max-files N] [--max-file-bytes N]
                    [--max-total-bytes N] [--format json]
akos rules explain <RULE_ID>
```

Exit codes (fail-closed): `0` ran to completion with no blocking finding; `2` ran to completion with a **blocking** finding (an open CRITICAL, or a finding a rule marks `blocking`); `1` the scan was **incomplete** (bad registry, unreadable input, exceeded resource budget, unloadable detector, detector with no `run()`, malformed detector output, or internal exception) or a usage/setup error. Errors and findings are separate: a detector that cannot run is an `ExecutionError`, never a finding, and never a clean pass — if both exist, `1` wins. Read failures use phase `read`. `--format json` preserves `{status, summary, findings, errors}`.

The default scan-wide budgets are 10,000 unique filesystem entries traversed, 10,000 unique matching files, 2 MiB per file, and 100 MiB total. Ignored and symlinked directories are pruned before descent; repeated globs/rules charge a resolved entry or file once. `--max-files` bounds both traversal work and matching inputs. Override the budgets explicitly with the three `--max-*` flags for a known larger repository; a limit breach fails closed and never returns a partial clean result. `--target all` is the compatibility default.

## Adding a rule

1. `rules/<domain>/<RULE_ID>.yaml` — copy the shape of an existing one in the same domain. The v1 contract requires `id`, `title`, `domain`, `level`, `severity`, `confidence`, `related_packs`, `detector`, `applies_to`, `recommendation`, `references`, `version: 1`, and `status`; `suppressible` is the only optional top-level field and defaults to `true`. Unknown fields fail discovery.
2. `rules/<domain>/<rule-id>.py` — export `run(files: list[Path]) -> list[dict]`. Each returned dict needs at least `evidence: [{path, line_start, line_end, snippet}]`. Optional per-finding overrides: `severity_override`, `confidence_override`, `detail` (replaces the registry's `recommendation` for this one finding), and `blocking`. Let input `OSError`s escape; swallowing one can turn an incomplete scan into a clean result.
3. Write a small fixture and verify BOTH the true positive and the realistic near-miss that shouldn't fire — every detector shipped here started with at least one bug a synthetic test caught (a JSX `htmlFor` vs. HTML `for`, a suppression-comment window too wide, a fixture-path exclusion matching too broadly). Don't skip this step.
4. Add a benchmark case under `benchmarks/cases/` (see `benchmarks/README.md`) so regressions show up in `akos benchmark`, not just in memory.
