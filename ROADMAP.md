# AKOS Roadmap

Living document, not a promise with dates. Reordered whenever priorities change.
Source of truth for *why* an item exists: `.akos/audit-2026-07-23.md` (full
integral audit) and `CHANGELOG.md` (what already shipped). This file only
tracks what's still open.

Last reviewed: 2026-07-25.

## Now

Nothing queued. The previous "Now" batch (tag v1.12.0, merge the 3 open
Dependabot PRs) shipped today — see Recently shipped. Pull the top of Next
when picking up work.

## Next

Concrete, scoped, unblocked by the above.

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

- **`merge-pr.sh` has behavioral tests.** `tests/integration/test_merge_pr.sh`,
  20 scenarios against fake `gh`/`git` (never the real API or remote): every
  usage/precondition error, both refused states (no checks, failing checks),
  and every success path including all three tagging branches. Confirmed the
  suite catches a real regression before trusting it (sabotaged a copy,
  watched the right assertion fail). Runs automatically — the CI integration
  runner glob-discovers `test_*.sh`, no wiring needed.
- **Secret redaction moved out of `rules/security/`.** `rules/security/
  _secret_utils.py` → `schemas/secret_utils.py` (renamed, no leading
  underscore — it's shared infrastructure now, alongside `yaml_subset`,
  `cli_args`, `pack_metadata`). Updated all 6 consumers: `schemas/history.py`,
  `rules/runner.py`, the `SECRET_IN_SOURCE` and `SERVICE_ROLE_IN_CLIENT`
  detectors, `A11Y_INPUT_NO_LABEL`'s comment masker, and
  `test_secret_contract.py`. 460 unit tests, 12 integration suites,
  shellcheck, and `doctor.sh` self-scan (which exercises the moved detectors
  for real, not just imports them) all green after the move.
- **Rule schema was already real, this roadmap was stale.** The "give rules a
  real schema" item carried over from the audit unchanged, but v1.12.0's
  "Strict executable-rule contract" (`rules/rule_schema.py`,
  `require_valid_rule_registry`) already rejects a scalar `applies_to.glob`
  before `Rule.__init__` ever runs — verified directly: a registry with
  `glob: '**/*.py'` (string, not list) raises `RuleContractError` at
  discovery, never reaches the `Rule` constructor. No code change needed;
  removed from Next.
- **`metadata.yaml` reading centralized.** New `schemas/pack_metadata.py`
  (`discover_pack_metadata_paths`, `load_pack_metadata`) replaces 5 open-coded
  copies in `bin/akos`, `freshness.py`, `config_check.py`, `routing_check.py`,
  `validate.py`. Behavior at each call site unchanged — `validate.py` still
  surfaces a parse failure as a finding, the rest still fall back to `{}`.
  New unit tests in `test_pack_metadata.py`; full suite (460 unit +
  integration + doctor.sh) green after the change.
- **v1.12.0 tagged.** Annotated tag pushed, pointing at the CI-green state
  (`e9cff00`).
- **3 Dependabot PRs merged.** #26 (`actions/checkout` → 7.0.1), #25
  (`actions/upload-artifact` → 7.0.1), both green on first try. #32
  (`actions/setup-python` → 7.0.0) needed a real fix: `tests/unit/
  test_ci_contract.py` hardcoded the old v6.2.0 action SHA as part of the
  "immutable pin" contract test, so it broke the moment the pin moved to the
  new SHA (`5fda3b95a4ea91299a34e894583c3862153e4b97`). Updated the test to
  the new SHA — the pin-immutability check is doing its job correctly, it just
  needs updating on every intentional bump, same as any pinned-hash contract.

v1.11.1 and v1.12.0 already closed the audit's two CRITICAL findings
(symlink-followable `history clean`, self-deleting E2E test) and most HIGH
findings: suppression can't silence security-floor rules, `uninstall.sh`
verifies symlink targets before removing them, RLS/policy detectors fold
state across migrations in order, CI no longer aborts before parsing
self-scan JSON, coverage is measured and gated at 80%, Mobile is a first-class
scoring dimension, and the README quickstart activates `PATH` in the current
shell before persisting it. Full list: `CHANGELOG.md` `[1.12.0]` and
`[1.11.1]` entries.
