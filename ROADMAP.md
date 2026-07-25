# AKOS Roadmap

Living document, not a promise with dates. Reordered whenever priorities change.
Source of truth for *why* an item exists: `.akos/audit-2026-07-23.md` (full
integral audit) and `CHANGELOG.md` (what already shipped). This file only
tracks what's still open.

Last reviewed: 2026-07-25.

## Now

Ready to execute, no blockers.

- **Cut and tag the v1.12.0 release.** `VERSION` and `CHANGELOG.md` already
  describe it; CI is green on `main` (`5b81389`, run `30026634808`). No tag
  exists yet — `git tag -l` stops at `v1.9.0`. The audit was explicit: don't
  publish a version without green CI + an annotated/signed tag. CI condition
  is now met.
- **Merge the 3 open Dependabot PRs.** #32 (`actions/setup-python` → 7.0.0),
  #26 (`actions/checkout` → 7.0.1), #25 (`actions/upload-artifact` → 7.0.1).
  Low risk, unblocks Dependabot from re-opening stale diffs.

## Next

Concrete, scoped, unblocked by the above.

- **Centralize `metadata.yaml` reading.** Duplicated across
  `bin/akos`, `schemas/freshness.py`, `schemas/config_check.py`,
  `schemas/routing_check.py`, `schemas/validate.py`, each with slightly
  different parse-error semantics. Extract one canonical catalog/DTO.
- **Give rules a real schema.** `rules/runner.py`'s `Rule` class still
  consumes loose dicts; a scalar where a list is assumed (`glob`) throws
  outside the fail-closed path instead of inside it.
- **Move secret redaction out of the security-rules private path.**
  `schemas/history.py` imports `redact_secrets` from `rules/security/
  _secret_utils` — a neutral module has no business depending on a specific
  rule's internals. Extract to a shared location both can import.
- **Behavioral tests for `merge-pr.sh`.** It's the only mitigation for
  unprotected branches on the free/private repo tier, and currently has zero
  tests. Needs `gh`/`git` fakes covering every exit state.
- **Unified versioned JSON envelope.** CLI subcommands (`check-config`,
  `rules run`, `eval`, ...) each shape their JSON output differently; some
  return plain text with exit 0 where JSON + non-zero would be correct.

## Later

Real, but needs a decision before it's actionable — not just an implementation
task.

- **Define the first-adopter segment and growth hypothesis.** README targets
  "any AI coding agent"; CONTRIBUTING frames it as a personal system. Needs an
  explicit answer: who adopts first, what behavior changes, how they find it,
  what evidence would kill the hypothesis.
- **Run the activation baseline for real.** `docs/product/activation-baseline.md`
  defines the study (median time-to-first-review, 4/5 solo devs succeeding)
  but it hasn't been run blind against held-out repos yet. The README already
  states the target isn't measured — don't claim it until this runs.

## Won't do now

Explicitly deprioritized, with the reason, so it doesn't get re-litigated
every audit pass.

- **Four-ring Clean Architecture / framework adoption.** Audit's own
  tradeoff call: Bash + Python stdlib is proportional to what AKOS is. Add
  contracts at boundaries that have actually failed, not layers everywhere.
- **Web Performance / Frontend / Mobile runtime scoring for AKOS itself.**
  AKOS is a CLI with no deployed UI. These lenses correctly report `n/a`
  rather than inventing a score — that's the correct behavior, not a gap to
  close.

## Recently shipped (context for what's *not* on this list anymore)

v1.11.1 and v1.12.0 already closed the audit's two CRITICAL findings
(symlink-followable `history clean`, self-deleting E2E test) and most HIGH
findings: suppression can't silence security-floor rules, `uninstall.sh`
verifies symlink targets before removing them, RLS/policy detectors fold
state across migrations in order, CI no longer aborts before parsing
self-scan JSON, coverage is measured and gated at 80%, Mobile is a first-class
scoring dimension, and the README quickstart activates `PATH` in the current
shell before persisting it. Full list: `CHANGELOG.md` `[1.12.0]` and
`[1.11.1]` entries.
