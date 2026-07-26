# AKOS Roadmap

Living document, not a promise with dates. Reordered whenever priorities change.
Source of truth for *why* an item exists: `.akos/audit-2026-07-23.md` (full
integral audit) and `CHANGELOG.md` (what already shipped). This file only
tracks what's still open.

Last reviewed: 2026-07-26.

## Now

Nothing queued. v1.14.0 (`architecture/philosophy-of-software-design` + ruling
R13) shipped on top of v1.13.0 — see Recently shipped. Pull the top of Next
when picking up work; `devops/observability` is now at the top of it.

## Next

The rest of the second knowledge-pack batch. Each closed gap below was verified
by grep against the corpus, not assumed; each was put through the [source
intake gate](core/source-policy.md) before landing here. Budget matters as much
as content: routing selects 2-5 packs from one flat table, so growth past
roughly 60 rows costs selection precision faster than it buys coverage. The
corpus is at 57 after `philosophy-of-software-design` shipped. Three packs
remain in this batch, and then the table is full until something earns its way
in by displacing something else.

- **`devops/observability`** (OpenTelemetry spec L1 + *Observability Engineering*
  L3). `OpenTelemetry` returns zero hits. `devops/sre` sets SLOs and error
  budgets but nothing says how to instrument in order to meet them. Deferred
  behind the item above because Prototype/MVP projects rarely reach the
  question.
- **`frontend/seo`** (Google Search Central + schema.org, L1). `schema.org` and
  `sitemap` return zero; `SEO` appears once, in passing, in `frontend/html`.
  Landing pages are a recurring surface here, but nothing is currently blocked
  on it.
- **`product/experimentation`** (Kohavi, Tang & Xu, L3). `Kohavi` and
  `statistical significance` return zero. `product/lean-startup` supplies the
  hypothesis and none of the statistics — sample size, power, guardrail metrics,
  p-hacking. Only pays off with real traffic, so it sits last.

Two process items the pack work surfaced:

- **Backfill graph coverage, or state the rule.** 19 packs are absent from
  `graphs/knowledge-graph.md`. Most are absent correctly — it indexes
  cross-cutting *concepts*, and `testing/playwright` has no cross-cutting
  concept — which is why `doctor.sh` deliberately does not require a link.
  But nobody has checked which of the 19 are genuine omissions versus correct
  absences. Decide per pack, then either add the node or record that the file
  is concept-scoped and pack coverage was never the goal.
- **Split the oversized `ai-engineering` files.**
  `agent-security/engineering-rules.md` is ~18 KB with 95 `ASE` rules, well past
  the 40-200 line guidance in `core/knowledge-schema.md`. Promotion to stable
  deliberately did not require splitting — the content is correct, just long —
  but a rule file nobody finishes reading is a rule file that gets skimmed.

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
- **Packs waiting on a stack trigger, not on a decision.** Each is a real gap
  with a real source; none is worth a routing-table row until the trigger
  fires. `frontend/tailwind` (L2) — only if `frontend/css` + `design-systems`
  are shown to fall short in an actual review. `games/godot` (L2) — when a
  Godot project reaches an AKOS review; today Godot appears once, in the
  personal layer. `content/i18n` (Unicode CLDR + W3C, L1) — when a project goes
  multi-language. `architecture/legacy-code` (Feathers, L3) — zero hits today,
  but it overlaps `martin-fowler-refactoring`, so it waits for a real
  inherited codebase. `backend/payments` (Stripe's published practice, L2,
  named explicitly in `core/authority-model.md`) — when something is monetized.

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
- **Knowledge packs rejected by the intake gate**, so the same candidates
  don't get re-proposed every few months. Each was checked against the corpus
  before being turned down:
  - `security/threat-modeling` (STRIDE, Shostack) — `threat model` returns 29
    hits across `nist-ssdf`, `owasp-asvs`, `owasp-api-top-10` and
    `agent-security`. Already covered; a pack would duplicate.
  - `design/motion` — `motion` returns 64 hits, `easing` 13, spread across
    `material-design`, `frontend/css` and `design-systems`.
  - `design/typography`, `design/color` — partly covered by `refactoring-ui`
    and `wcag`; the remainder is preference, and preference lives at Level 0 in
    [design-language.md](packs/personal/pau-avila/design-language.md), where it
    wins anyway.
  - `architecture/data-intensive` (DDIA, Kleppmann) — excellent book, wrong
    context. Distributed systems at scale versus React + Supabase in
    Prototype/MVP. Fails intake question 2.
  - `architecture/pragmatic-programmer`, `testing/goos` — more than half
    overlapping `martin-fowler-refactoring`, `solid` and `tdd`.
  - `devops/dora` (*Accelerate*) — team delivery metrics; the owner is a solo
    developer. Fails intake question 1 in practice.
  - Any "MDN" or API-reference pack — reference, not doctrine. Fails intake
    question 1 by definition.
  - Any pack named after a paper — papers enter as `sources[]` inside a pack.
    Three packs already cite arXiv work that way; none is named after one.

## Recently shipped (context for what's *not* on this list anymore)

- **`architecture/philosophy-of-software-design`, v1.14.0.** First pack from this
  backlog, and the first through the intake gate that shipped with v1.13.0 — the
  gate worked as designed, turning "is Ousterhout worth a pack" into eight greps
  and a stated position. P1–P19, PSD1–PSD36. Notable for two firsts: no starred
  rule and no CRITICAL scoring band anywhere in the pack (a Level 3 design
  opinion must not acquire floor authority), and a reviewer-discipline rule
  requiring every finding to name what a caller stops needing to know — the
  pack's own likely failure mode is a reviewer wielding "that's shallow" as an
  unanswerable objection.
- **Canonical ruling R13.** The pack disputes the common reading of `solid` and
  `clean-architecture` on decomposition granularity, L3 against L3 in the same
  domain, so the resolution algorithm's authority and proximity steps both tie.
  R13 settles it — ask what the split hides — and `CONTRIBUTING.md` directs
  exactly this case to `core/conflict-resolution.md` rather than to patching one
  pack. The Level 0 file-size convention in `packs/personal/pau-avila/` was left
  untouched: it outranks both packs, and reading PSD as being about interface
  depth rather than file length dissolves most of the conflict anyway.
- **Corpus expansion, v1.13.0.** Two packs closing verified zero-coverage gaps:
  `security/auth` (L1, AU1–AU60 — OAuth/OIDC flow, token validation, session
  lifecycle, passwords, with a Supabase mapping) and `security/privacy` (L1,
  PR1–PR49 — lawful basis, minimization at the schema, retention as an enforced
  job, subject rights, processors). Before them, `OAuth`, `OpenID`, `GDPR`, and
  `consent-as-legal-basis` returned zero hits across all 54 packs. Both wired
  into `security-reviewer`; privacy also into `database-reviewer`.
- **The six `ai-engineering` packs are stable.** They had been `draft` since
  authoring — readable but excluded from automatic routing — with no documented
  promotion criterion, so ~7,000 lines of written content was unreachable
  unless a user named the pack. `core/knowledge-schema.md` now carries a
  draft→stable criterion built from checks that already existed (citations,
  source grounding, prefix uniqueness, the disclaimer) rather than new ones, all
  six were assessed against it, and their rows moved into the stable routing
  table.
- **Source intake gate.** `core/source-policy.md` now answers "does this source
  deserve a pack at all" before scaffolding: a pack is doctrine, not reference;
  the gap must be shown by grep rather than asserted; a Level 4 source can never
  be a pack's primary source. It also records two recurring answers — papers
  enter as `sources[]` inside packs and are never packs themselves, and a
  website earns a pack only as a platform owner's normative documentation.
- **Two authoring steps became checks.** `doctor.sh` now verifies every pack
  README carries an independent-distillation line (this caught
  `packs/ux/wcag/README.md`, which had shipped without one) and that every
  `metadata.yaml` `related:` path resolves — schema-typed as plain strings, so a
  typo silently pointed nowhere. Both were confirmed to fail when deliberately
  sabotaged before being trusted.
- **A graph-link check was designed, then rejected.** The plan called for
  requiring every pack to appear in `graphs/knowledge-graph.md`. Checking first
  showed 19 packs absent — because that file indexes cross-cutting *concepts*,
  not packs, and `testing/playwright` correctly has no node. The check would
  have encoded a rule the graph doesn't follow, so it was dropped and the
  `related:` check took its slot. The open question is in Next.
- **JSON envelope unification was already decided against, deliberately.**
  `docs/cli/exit-codes.md` has a "Stable JSON contracts (v1.12)" section
  documenting all 9 commands' shapes as intentionally different, plus a "Why
  not unify everything under one scheme" section: extending one binary
  0/1/2-shaped envelope to every command would lose the "ran fine, but found
  a real problem" signal CI depends on, and any shape change is explicitly
  defined as a breaking change requiring a new contract version. This is a
  documented team decision, not an oversight — implementing "unify the
  envelope" would mean overriding it unasked. Removed from Next without a
  code change.
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
