# AKOS Roadmap

Living document, not a promise with dates. Reordered whenever priorities change.
Source of truth for *why* an item exists: `.akos/audit-2026-07-23.md` (full
integral audit) and `CHANGELOG.md` (what already shipped). This file only
tracks what's still open.

Last reviewed: 2026-07-27.

## Now

Nothing queued. v1.17.0 (`product/experimentation`) shipped and **the
knowledge-pack batch is closed** — see Recently shipped. The corpus is at 60
and the routing table is at the ceiling this file set: nothing new enters
without displacing something. Pull from Next.

## Next

The knowledge-pack batch is closed. What remains is the process work the pack
work surfaced, plus one standing constraint.

**The routing table is full.** 60 packs, against a stated operating ceiling of
roughly 60 rows — past that, selection precision degrades faster than coverage
improves. The 2026-07-27 routing trial found no degradation *at 58*, which is
evidence for the current size and not for a larger one. A new pack now needs to
displace an existing one, and the case for it has to include which row it
replaces.

- **Get CI running again.** Six releases (v1.13.0–v1.17.0 plus the routing-trial
  commit) have merged on local evidence alone because GitHub Actions is blocked
  on account billing. Local gates cover everything except the Ubuntu runner, so
  the one genuinely open question is whether the `awk` added to `doctor.sh` in
  v1.13.0 behaves the same under GNU awk. One green CI run on `main` closes all
  six at once.

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

- **"Split the oversized `ai-engineering` files" was wrong, and is closed
  without a split (2026-07-27).** The item claimed
  `agent-security/engineering-rules.md` was "~18 KB with 95 `ASE` rules, well
  past the 40-200 line guidance". The 18 KB is real; the conclusion is not. The
  file is **139 lines** — inside the guidance — because 95 rules at one dense
  line each is exactly the intended format. The guidance says *lines*, and this
  was read as bytes.
  Measuring the whole corpus: four files exceed 200 raw lines
  (`agent-security/prompt-fragments.md` 225, `touch-ergonomics/examples.md` 224,
  `tool-design/prompt-fragments.md` 210, `agent-foundations/prompt-fragments.md`
  206) and all four are 75-96% fenced blocks — 7-8 lines of prose in the prompt
  fragments. **No file in the corpus exceeds 200 lines of prose.** Nothing to
  split.
  `core/knowledge-schema.md` now says the guidance measures prose, excludes
  fenced blocks, and is not a byte count — with the audit recorded, because this
  item survived three roadmap revisions and a shipped CHANGELOG entry before
  anyone ran `wc -l`. The `[1.13.0]` CHANGELOG entry still carries the false
  claim; it is corrected in `[1.17.2]` rather than rewritten, since shipped
  entries are a record.
  Worth noting the second reason not to split: a rule file divided into two rule
  files hides nothing from its reader, which
  [philosophy-of-software-design](packs/architecture/philosophy-of-software-design/decision-framework.md)
  calls a shallow split. Even had the measurement been right, "it is long" would
  not have been sufficient grounds.

- **Graph coverage audited and the rule written down (2026-07-27).** 17 packs
  had no node in `graphs/knowledge-graph.md` and nobody had checked which were
  omissions. Read all 17 for a cross-cutting claim: 8 had one and were linked,
  9 did not and are recorded as absent by design. One genuine hole turned up —
  no perceived-performance concept existed at all — now a node linking web.dev
  WD6, Core Web Vitals CW8, and Laws of UX on waiting as a negative peak.
  `frontend/design-systems` was the closest call and was **not** linked: tokens
  look like the "one owner per decision" idea but the pack does not make that
  claim. The file now carries the criterion, the test ("quote the line in the
  pack that says the concept — if you cannot, the link is padding"), and the
  audited absent list, so the question is answered rather than re-derived.

- **`product/experimentation`, v1.17.0 — batch closed.** The last of six packs.
  Its organising decision is the same shape as `observability`'s and `seo`'s but
  sharper, because here it is arithmetic: required sample per arm is
  ~16·p·(1−p)/δ², so under ~5,000 weekly users into a funnel you cannot A/B test
  conversion, and that is the finding rather than a reason to lower a threshold.
  The refusal ships with teeth — a rules section for when you cannot experiment,
  a rubric returning `n/a` instead of a low score and never deducting for not
  running experiments, and a checklist gate before the checklist, because
  reviewing the methodology of a test that should not exist legitimizes it.

- **`frontend/seo`, v1.16.0.** Third pack off this backlog. Its organising
  decision is a refusal: ranking is excluded from the pack entirely, not
  demoted, because result ordering is unpublished and every claim about it is a
  Level 4 assertion about a system nobody outside the search engine can
  inspect. This is the corpus's widest gap between how much advice a domain has
  and how much is verifiable, so the line is enforced in five places rather
  than stated once — including a reviewer rule that drops any finding which
  cannot name the pipeline stage it breaks. Only two of its 50 rules are
  starred and neither is discoverability: markup must not misrepresent the
  page, and nothing is applied at the cost of accessibility or honesty.

- **Routing verified against the four new packs (2026-07-27).** The corpus grew
  54 → 58 across v1.13.0–v1.15.0 with nothing confirming the new rows were
  actually reachable. Three trials, predictions pre-registered before running,
  three independent agents given only a scratch project and
  `skills/akos/SKILL.md` — no hint which packs existed or which were under test.
  Result: 3/3 MUST, 2/2 MUST NOT, 3/4 SHOULD, 3/3 SHOULD NOT. No defect.
  - The skip-in-Prototype guards on `philosophy-of-software-design` and
    `devops/observability` both held; the first was rejected quoting its own
    routing row back.
  - Cited rule codes (AU12–AU57, PSD4–PSD34) all resolve to the rule they
    actually state, so the new packs are usable by an agent that had never seen
    them — the strongest signal in the run.
  - The three trials selected genuinely different pack sets, overlapping only on
    the two mandatory-when-deployed packs. The feared "58 rows and the table
    stops discriminating" did not appear on these tasks.
  - The single miss was mine: I predicted `security/privacy` would load for a
    login review. The agent declined it — *"one line inside a finding already
    made, not a data-lifecycle review"* — which is better reasoning than the
    prediction. Widening that row would make it over-trigger. No change made.
  - Limits, stated: three trials, one model, one synthetic project. A smoke
    test for gross failure, not a measure of ranking quality across 58 packs.
- **`devops/observability`, v1.15.0.** Second pack off this backlog. The gate's
  most useful output was a negative: `SLO` returned 111 hits and `error budget`
  10, all in `devops/sre`, which turned "does this overlap SRE" into a stated
  boundary — SRE owns the targets, observability owns the signals they are
  measured from. Only two of its 44 rules are starred, and both are data
  protection rather than observability: telemetry leaves the system into a
  vendor's store, so secrets and personal data in it are the floor arriving
  through a devops pack.
- **Level assignment corrected against this roadmap.** The entry above queued
  observability at Level 1 on the OpenTelemetry spec. Writing it changed the
  answer to Level 2: OTel is a CNCF project authoritative about itself, not a
  normative standard like the IETF RFCs or WCAG, and half the pack's reasoning
  is book-derived. Recorded in the pack's `references.md` — a roadmap entry is a
  hypothesis about a pack, not a specification of it.

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
