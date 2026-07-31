# AKOS Changelog

All notable changes to AKOS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows semver.

## [1.17.6] — 2026-07-31

The last open item from the v1.17.4/v1.17.5 dry runs that didn't need another
run to fix — it needed writing down.

### Added

- **`skills/akos-review/SKILL.md` gets a new step 6, "Merge the lens
  reports."** One sentence — "merge every returned summary into one Review
  Summary" — used to stand in for the hardest step in the pipeline. The
  2026-07-31 re-run (v1.17.5) had to invent all three of the following
  unguided, and a different merger would have produced a different score
  block from the identical five lens reports:
  - **Dedup rule.** Two findings are the same defect, not two, when they cite
    overlapping file:line ranges *and* the same failure mode. Keep the higher
    severity, union the fix guidance, cite every contributing lens, deduct
    once even if two rubrics would each deduct.
  - **Same-dimension ownership.** The step-2 lens table already maps each
    scored dimension to one owning lens; a second lens's number for that
    dimension becomes a named sub-score inside the finding, never a sibling
    or an addendum. Copy is stated as a specific case of this rather than a
    separate rule, since `agents/copy-reviewer.md` already says lens 5 feeds
    UX rather than owning a dimension.
  - **Cross-lens severity disagreement**, resolved by citing
    `core/constitution.md` Article 2's *enumerated* safety floor — security,
    accessibility basics, data integrity — rather than by either lens's
    unaided judgment. A defect outside that list caps at HIGH no matter which
    lens raised it or how it reads; the adjudication is recorded in
    Tradeoffs, naming both lenses and both severities, so a reader can
    overrule it.
  - The non-canonical-decision-string rule (a lens returning something other
    than PASS/PASS WITH FIXES/BLOCKED/INCOMPLETE) moved here from the Scores
    block description, where it was stranded next to output formatting
    instead of merge instructions.
- Steps renumbered 1–8 to fit (`Output` → 7, `Record it` → 8); two stale
  cross-references to the old numbering (`step 5`, `step 6`) fixed in the
  same pass.

### Not yet verified

Written guidance and exercised guidance are different claims — the same
caution v1.17.5 raised about its own fixes applies here unchanged. This has
not been re-tested against a live multi-lens run yet; that's the next honest
check, not this release.

## [1.17.5] — 2026-07-31

The v1.17.4 fixes were instructions, unexecuted since writing them. Re-ran the
same task — full frontend review on the same held-out repo, through nothing
but the revised `skills/akos-review/SKILL.md` — to find out whether they
worked.

### Confirmed

- **The pipeline reaches the merge step and produces a decided report.** Five
  lenses dispatched, five reported, one merged Review Summary with a single
  BLOCKED decision — four real CRITICALs found in the target (a keyboard-
  unreachable graph canvas, an unexitable first-run onboarding trap, errors
  swallowed and rendered as false success, a privacy badge that read "local"
  while sending data to OpenAI). The previous run's failure mode — five
  subagents completing work that never reached the orchestrator — did not
  recur.

### Fixed

Root-caused why the run succeeded, which was not fully the reason the v1.17.4
fix targeted — and fixed what that surfaced:

- **The checkpoint-to-file instruction was circular, and cost tokens for no
  benefit.** Lens subagents hold `tools: Read, Grep, Glob` — no Write — so a
  lens cannot checkpoint its own summary; the orchestrator has to receive the
  full text into context before it can write it anywhere, which means the
  "protects the orchestrator from running out of room" rationale was false.
  Considered giving reviewer subagents Write so they could checkpoint
  themselves — declined; read-only reviewers that cannot touch the project
  under review, or anything else, is the correct security posture and stays.
  `SKILL.md` now states the honest benefit — crash/resume durability across a
  killed session, not context economy within one run.
- **Wave-dispatch guidance named the wrong lens numbers.** "(2 accessibility, 3
  mobile, 8 security)" against the file's own table two paragraphs up (2=UX,
  3=Accessibility, 4=Mobile, 8=Security). Also scoped for a twelve-lens run
  regardless of how many lenses the actual workflow contains; now says so and
  gives the smaller-workflow case an explicit answer (one wave, five lenses or
  fewer).
- **Step 7 (`akos history record`) had no exemption for a read-only review of
  a project you don't own.** It writes `.akos/reviews/` into the reviewed
  project; the only stated exemption was "explicitly asked for a one-off,
  throwaway check", which doesn't cover a read-only audit of someone else's
  repo. The re-run skipped it on that basis and said so — now an explicit rule
  rather than an inference.
- **A lens returning a decision string outside the four canonical ones had no
  handling.** The frontend lens returned `"CHANGES REQUESTED — one blocking
  issue"`; the orchestrator mapped it to BLOCKED from the lens's own stated
  reasoning and recorded both strings. That judgment call is now the written
  rule — map only when the lens states its reasoning in AKOS's terms,
  otherwise report the mismatch rather than silently absorb it.
- **The copy lens's score had no home in the merged report.** `agents/
  copy-reviewer.md` already says lens 5 "feeds the UX score" — it isn't meant
  to be a standalone dimension — but nothing told the merger what to do when
  the lens returns one anyway (it did: "Interface copy: 55"). Rather than add
  a Copy row to `scoring/overall-score.md`'s weight table (which has none, by
  design, and would double-count against UX), `SKILL.md` now tells the merger
  to fold a standalone copy score into UX via the rubric copy-reviewer.md
  already cites, not record it as a sibling or an addendum.

### Still open (tracked in `ROADMAP.md`)

The merge algorithm remains one sentence for the hardest step in the pipeline
— the re-run still had to invent a dedup rule, a same-dimension tiebreak, and
a cross-lens severity adjudication, unguided. Configless defaults for
`Deployed`/`Primary surface`/`Style direction`, the Startup-MVP-vs-Prototype
profile contradiction, `INCOMPLETE` not yet propagated past `skills/
akos-review/SKILL.md` to the 13 other files enumerating decision states, no
route from a lens's confirmed detector false-negative back to the rule, and no
"scope the target" step before lens dispatch.

## [1.17.4] — 2026-07-31

Onboarding dry run, prompted by the repo going public. Two agents ran first —
one auditing the install path as a first-time user, one running a real
five-lens frontend review on a held-out repo through nothing but
`skills/akos-review/SKILL.md`. Both surfaced real defects; the review trial
surfaced one worse than friction.

### Fixed

- **The review pipeline had no way to say a review did not happen.** The trial
  dispatched five lens subagents, spent ~123k tokens, and never reached the
  merge step — the lenses' output never reached the orchestrator, and the
  run's own report was assembled from shell commands alone. `core/
  review-pipeline.md`'s decision semantics are purely severity-driven, so a run
  where every lens silently failed would have emitted the same PASS/BLOCKED
  string as a run where every lens passed. `skills/akos-review/SKILL.md`
  gained an `INCOMPLETE` state that outranks the severity rules, plus
  checkpoint-to-disk and wave-dispatch guidance so the orchestrator's own
  context is less likely to fill before the merge. **Not yet propagated to the
  12 other files that enumerate PASS/PASS WITH FIXES/BLOCKED** (`core/
  review-pipeline.md`, `core/constitution.md`, `core/scoring-model.md`,
  `agents/ux-reviewer.md`, `scoring/overall-score.md`,
  `docs/scoring/evidence-confidence-coverage.md`, `workflows/new-feature.md`,
  `workflows/ui-screen-review.md`, `docs/architecture/current-system.md`,
  `docs/migration/v1.1-to-next.md`, three `templates/*.md` files) — tracked in
  `ROADMAP.md`.
- **`akos rules run` exit `0` was documented as "no findings"; it means no
  CRITICAL.** Confirmed by running it against a real project: exit 0 with five
  MEDIUM findings. An agent following the old wording checks `$?`, sees 0, and
  reports clean without reading the findings array.
- **`akos list-skills` printed "Linked into: …" unconditionally** — identical
  output whether the symlinks existed or not, while being the README's
  documented verification step. Now reports per skill, per tool.
- **`doctor.sh` tested symlink existence, not identity — confirmed by
  reproducing it.** A throwaway checkout that had installed nothing printed
  `✓ 69 ! 0 ✗ 0`, because the links belonging to a *different* checkout
  exist. New `akos_link_status` helper in `bin/akos-common.sh` compares
  resolved targets; `doctor.sh` and `akos list-skills` now warn (not fail) on
  a foreign checkout, since several checkouts on one machine is legitimate.
  The resolver walks symlinks at any depth rather than checking only the final
  path component, because `~/DEV` is commonly itself a symlink
  (`~/DEV` → `~/Desktop/DEV` on the maintainer's own machine) — a first version
  of this check flagged the maintainer's own healthy install as foreign.
  Covered by 10 cases in new `tests/integration/test_link_status.sh`, verified
  to actually catch the regression by sabotaging a copy back to the
  final-component-only check and confirming it fails.
- **Eight detectors ship, seven were documented.** `PACK_EXPIRED` (domain
  `meta`) was absent from `skills/akos-review/SKILL.md`'s prose and routing
  table. It is a finding about a knowledge pack's own freshness, not the
  project under review, and the routing table now says so explicitly.
- **The plugin path told both skills to run a CLI the plugin does not ship.**
  `akos` and `akos-review` opened by mandating `akos check-config` and told the
  agent to treat a non-zero exit as "do not proceed" — so a plugin install (no
  `bin/akos` on PATH) hits `command not found` on the second instruction it
  reads. Both skills now carry a by-hand fallback that verifies the same five
  config properties without the CLI, because the check exists to stop a
  hostile `.akos/config.md` from lowering the profile and silently skipping
  lenses — the CLI's absence is not license to skip that check, only to run it
  differently.
- **`LICENSE` was the canonical MIT text plus an appended note**, which is why
  GitHub reported this repo's license as "Other" rather than "MIT" the moment
  it went public — the detector only recognizes the unmodified body. The note
  moved to new `NOTICE.md`; the grant itself is unchanged.
- **README install path**, audited against the code rather than assumed
  correct: SSH clone URL on a now-public repo (confirmed anonymous HTTPS works
  against it; an evaluator without SSH keys configured cannot clone at all),
  macOS's Python 3.9 floor with no stated remedy (the existing
  `AKOS_PYTHON_BIN` escape hatch was documented only in the error message, now
  also in Prerequisites), no "restart your agent session" step (skills are
  enumerated at session start, so an already-open session improvises a generic
  review instead — which the planned activation-baseline study would have
  recorded as a false success), the 13 reviewer subagents written into
  `~/.claude/agents/` left undisclosed, `uninstall.sh` never mentioned, and
  PATH persistence assuming zsh with no note for bash/fish users.
- **`skills/{akos,akos-review}/SKILL.md`'s AKOS-root fallback was ambiguous
  to the letter.** "the directory two levels above this file" resolves to
  `skills/` under a literal per-file-not-per-directory reading — the exact
  case a plugin install depends on, since it lands outside `~/DEV/AKOS`. Now
  states it as `../..` from the file, i.e. the parent of `skills/`.

### Added

- `tests/integration/test_link_status.sh` — 10 cases for `akos_link_status`:
  missing/linked/foreign/dangling/real-directory, a symlinked ancestor
  (resolving correctly *and* still catching a real mismatch through one),
  relative targets, file targets, and chained symlinks.

Estimated time-to-first-review before this release, measured against the
stated 10-minute median target: 15–35 minutes for a realistic newcomer, with
two of the documentation defects above each individually able to consume the
whole budget. Not yet re-measured after the fixes; that is the next open item
in `ROADMAP.md`.

## [1.17.3] — 2026-07-27

Documentation catch-up. `README.md` and `CONTRIBUTING.md` had fallen behind the v1.13.0–
v1.17.2 work; neither described the corpus or the two mechanics added to guard it.

### Added

- **`README.md` now states what the corpus actually contains** — 60 packs across 12
  domains, with a table naming the sources per domain. It previously gave two examples and
  no scope, which left the most useful fact for a reader deciding whether AKOS covers their
  stack entirely unstated.
- **The bound is stated with it.** Routing selects 2–5 packs from one flat table, and past
  roughly 60 rows selection precision degrades faster than coverage improves — so a new
  pack has to displace one. Readers were otherwise free to assume the corpus grows
  indefinitely, which is the opposite of the design.
- **`CONTRIBUTING.md` gained the two steps that became mandatory in v1.13.0 and were never
  written into the human-facing guide:** the source intake gate as a *first* section before
  scaffolding (four questions, plus the two settled answers — papers become `sources[]`
  inside packs and never packs themselves; a website earns a pack only as a platform
  owner's normative documentation), and the draft→stable promotion procedure as a final
  one.
- CONTRIBUTING also records the graph rule from v1.17.1 — `graphs/` indexes concepts, not
  packs; 9 of 60 are absent by design; quote the line in the pack or the link is padding.

### Changed

- `README.md`'s quality-infrastructure guarantees gained the two `doctor.sh` checks added
  in v1.13.0: every pack README carries an independent-distillation line, and every
  `metadata.yaml` `related:` path resolves.
- The "Add a new pack" section now opens with the intake gate rather than with
  `akos create-pack`, matching the order the process actually runs in, and notes that new
  packs start at `status: draft`.
- Rollback example moved from `v1.7.0` to `v1.16.0` — ten releases had passed.
- `CONTRIBUTING.md` step 7 lists what `doctor.sh` now actually enforces.

### Checked and left alone

- `akos rules run` is documented as "8 executable checks" and there are exactly 8. Verified
  rather than assumed after the same class of claim proved wrong in `[1.17.2]`.
- `docs/architecture/current-system.md` still says "49 packs, 17-file contract". That file
  self-declares as a dated v1.3.0 baseline kept as history, so the numbers are correct *as
  history* and were not touched. `README.md` describes it accurately as such.

## [1.17.2] — 2026-07-27

Correction release. No pack content changed, and no files were split.

### Corrected

- **The `[1.13.0]` entry's claim that `agent-security/engineering-rules.md` "runs ~18 KB /
  95 rules against a 40–200-line guideline" is false, and is corrected here rather than
  rewritten there** — shipped entries are a record, and quietly editing one would hide the
  error instead of fixing it.

  The 18 KB is real. The conclusion is not. The file is **139 lines**, comfortably inside
  the guidance, because 95 rules at one dense line each is exactly the format the contract
  asks for. `core/knowledge-schema.md` says *lines*; the claim measured bytes.

  The same false claim was carried through three `ROADMAP.md` revisions as an open item
  before anyone ran `wc -l` on the file.

### Changed

- **`core/knowledge-schema.md` now states how the 40–200 guidance is measured**, since the
  ambiguity is what produced the error:
  - it counts **lines of prose** — what a reader actually reads linearly;
  - **fenced blocks are excluded.** A `prompt-fragments.md` is a set of copy-paste blocks
    selected from, not a document read end to end; count blocks there;
  - it is **not a byte count**.
- **Corpus audited against the corrected reading.** Four files exceed 200 raw lines —
  `agent-security/prompt-fragments.md` (225), `mobile/touch-ergonomics/examples.md` (224),
  `tool-design/prompt-fragments.md` (210), `agent-foundations/prompt-fragments.md` (206) —
  and all four are 75–96% fenced blocks, the prompt fragments carrying 7–8 lines of prose
  apiece. **No file in the corpus exceeds 200 lines of prose.** Nothing was split because
  nothing needed splitting.

### Not done, deliberately

- **No file was split.** Beyond the measurement being wrong, a rule file divided into two
  rule files hides nothing from its reader — the shallow split that
  `architecture/philosophy-of-software-design` exists to name. Even had the file genuinely
  been long, "it is long" would not have been sufficient grounds; PSD's own test is what
  the split lets the caller stop knowing, and the answer here is nothing.

## [1.17.1] — 2026-07-27

Graph curation pass. No pack content changed.

### Changed

- **`graphs/knowledge-graph.md` audited for coverage, and the criterion written into the
  file.** 17 of 60 packs had no node and nobody had checked which of them were genuine
  omissions. All 17 were read for a cross-cutting claim, with the link label required to
  quote the pack's own line:
  - **8 linked.** `mobile/responsive-web` (RW2 — 320px is simultaneously a small phone and
    a 1280px page at 400% zoom, so one effort serves both) and `mobile/touch-ergonomics`
    joined *accessibility as a floor*; `content/ux-writing` joined *the four states*, since
    it supplies the strings the other packs only require; `architecture/martin-fowler-refactoring`
    joined *complexity as a cost* via the rule of three; `frontend/typescript` (TS4 —
    validate against a schema at the boundary, not cast) joined *untrusted content is data*;
    and `testing/testing-pyramid` (TP4 — a flaky test is worse than no test),
    `testing/playwright` (PW1) and `performance/core-web-vitals` (CW13 — field data is the
    verdict, lab tools debug) joined *a number you cannot act on is worse than no number*.
  - **1 genuine hole found.** No perceived-performance concept existed anywhere in the
    graph. New node: *perceived speed is designed, not measured into existence*, linking
    web.dev WD6, Core Web Vitals CW8, and Laws of UX on waiting and errors as the negative
    peaks worth disproportionate investment.
  - **9 absent by design**, listed in the file with the audit date:
    `architecture/twelve-factor-app`, `backend/graphql`, `backend/postgres`, `backend/rest`,
    `devops/ci-cd`, `devops/git`, `frontend/design-systems`, `frontend/react`,
    `performance/network-performance`. Each is mechanics for one protocol, tool, or
    platform.
- **`frontend/design-systems` was the closest call and was deliberately not linked.** Design
  tokens look like the "one owner per decision" idea that `philosophy-of-software-design`
  and `security/privacy` both carry — but the pack does not make that claim, and linking it
  would have been inventing a node to improve a count.
- **A new `## What belongs here` section states the rule** the file had been following
  without recording: this indexes concepts, not packs; pack coverage is not a goal;
  `doctor.sh` deliberately does not check it (a check requiring it was designed in v1.13.0
  and dropped on discovering it would encode a rule the graph does not follow). The test
  before adding a link is *quote the line in the pack that says the concept* — if you
  cannot, the link is padding, and every spurious link is a source an agent will pull and
  find nothing transferable in.

## [1.17.0] — 2026-07-27

Last pack of the v1.13.0 backlog. The routing table is now at its stated ceiling.

### Added

- **`packs/product/experimentation`** (Level 3 — Kohavi, Tang & Xu, *Trustworthy Online
  Controlled Experiments*). Principles P1–P17 and engineering rules EXP1–EXP45 across
  pre-launch planning, assignment and instrumentation, running, reading, deciding and
  shipping, what to do when you cannot experiment, and ethics. Cleared the intake gate on a
  verified gap: `Kohavi`, `statistical significance`, `statistical power`, `p-value`,
  `OEC`, `novelty effect`, `sample ratio`, `peeking`, `multiple comparison`,
  `minimum detectable` and `confidence interval` all returned zero across the 59-pack
  corpus. `A/B` returned five hits, all in passing — `product/lean-startup` supplies the
  hypothesis loop and none of the statistics, which is exactly the gap.

### The pack opens by talking most readers out of it

Required sample per arm is approximately `16·p·(1−p)/δ²`. On a 3% baseline that is ~52,000
per arm to detect a 10% relative lift and ~207,000 for a 5% one — halve the effect,
quadruple the requirement. **Under roughly 5,000 weekly users into the funnel, conversion
is not experimentable, and that is the finding.** An underpowered test does not produce a
weaker answer; it converts "we don't know" into a number people will quote.

So the pack ships a refusal with teeth: a traffic table with a verdict per scale and a list
of what to do instead; a rules section (EXP38–EXP41) for when experimentation is
unavailable, including that "we tested it" may never be claimed for an underpowered test; a
scoring rubric returning `n/a` rather than a low score for a surface without the traffic,
in which **not running experiments is never a deduction**; a checklist gate placed before
the checklist proper, because reviewing the methodology of a test that should not exist
legitimizes it; and an anti-pattern for the platform-and-process build-out that cannot
produce a valid answer.

This is the Level 3 failure mode named directly — the source's context is large-scale
consumer products, and `core/authority-model.md` is explicit that methodologies encode the
setting they came from.

### Other choices

- **Only two rules are starred, and neither is methodology.** EXP42 (no arm withholds
  safety, accessibility, or security — the floor is not contingent on whether users are
  observed to want it) and EXP43 (experiment data is personal data). Both apply at any
  scale, including where the rest of the pack does not.
- **"Not significant" may never be reported as "no effect"** (EXP27); the detectable
  threshold must be stated alongside. One rule, and it is what makes a flat result honest.
- **A program reporting mostly wins is a finding, not a success**, with an A/A test as the
  diagnostic.
- `graphs/knowledge-graph.md` gains a concept node — *a number you cannot act on is worse
  than no number* — linking this pack, `agent-evals`, the knowledge schema's "if a check
  can't fail, it isn't a check", and the confidence model.

### Backlog closed

`security/auth`, `security/privacy`, `architecture/philosophy-of-software-design`,
`devops/observability`, `frontend/seo` and `product/experimentation` — six packs across
v1.13.0–v1.17.0, plus six `ai-engineering` packs promoted out of draft. The corpus is at 60
and the routing table is at the ceiling stated in `ROADMAP.md`: nothing new enters without
displacing something.

## [1.16.0] — 2026-07-27

Third pack off the v1.13.0 backlog. One left.

### Added

- **`packs/frontend/seo`** (Level 1 — Google Search Central, IETF RFC 9309, schema.org,
  sitemaps.org). Principles P1–P17 and engineering rules SEO1–SEO50 across crawl and index
  control, rendering and indexability, URL identity, metadata, structured data,
  internationalization, migrations, monitoring, and a React/Next-class framework mapping.
  Cleared the intake gate on a verified gap: `schema.org`, `sitemap`, `robots.txt`,
  `structured data`, `rich result`, `hreflang`, `noindex`, `open graph`, `title tag`, and
  `page experience` all returned zero across the 58-pack corpus. `canonical` returned 41
  hits, every one in the "canonical ruling" sense rather than `rel=canonical`.

### The organising decision is what the pack refuses to contain

**Ranking is excluded entirely — not demoted to Level 4, excluded.** How results are
ordered is unpublished, so every claim about it is a Level 4 assertion about a system
nobody outside the search engine can inspect, and `core/source-policy.md` bars a Level 4
source from being a pack's basis. There is no honest version of this pack containing that
material.

This is the corpus's widest gap between how much advice exists in a domain and how much of
it is verifiable, so the line is enforced in five places rather than asserted once: two
principles, a reviewer rule requiring every finding to **name the pipeline stage** it
breaks (discover / crawl / render / index / serve — a finding that cannot name one is
folklore and is dropped), a second reviewer rule forbidding ranking claims outright, a
scoring rule that no deduction may rest on one, and an anti-pattern naming the review
comment that triggers it.

`references.md` states exactly what Level 1 covers: documented, enforceable mechanisms —
crawl directives, indexing controls, canonicalization, structured-data eligibility
requirements, and spam policies carrying real penalties. Google is the platform owner for
appearing in Google Search, the same basis on which `performance/web-dev`,
`ux/material-design` and `ux/apple-hig` are Level 1.

### Other choices worth recording

- **Only two rules are starred, and neither is discoverability.** SEO27 (structured data
  describes only what the page visibly shows — the one actively enforced rule in the
  domain) and SEO44 (nothing applied at the cost of accessibility, honesty, or
  performance). Hidden text and keyword-stuffed alt attributes fail the safety floor before
  they fail any search policy.
- **The pipeline is the diagnostic method, not a description.** A five-stage ladder worked
  top-down to the first failure. Naming the failing stage *is* the diagnosis; skipping it is
  how teams add tags to a page a crawler never fetched.
- **`n/a` for surfaces with no public pages.** An app behind a login scores `n/a`, not a low
  number, and the decision framework calls it a five-minute exclusion check rather than an
  audit. The matching anti-pattern names the failure of producing a report about pages no
  crawler will fetch.
- **Migrations get their own procedure.** Everything else in the domain is incremental; a
  URL change is not, and it is where organic traffic is actually lost. Four rules
  (SEO36–SEO40), a decision-framework section, and a prompt fragment, all built around
  capturing a baseline *before* the change.
- `graphs/knowledge-graph.md` gains a concept node — *semantic markup serves more than one
  reader* — linking WCAG, `frontend/html`, this pack, and gov.uk content design, since the
  same structure serves a screen reader, a crawler, and the next developer.
  `agents/frontend-reviewer.md` and `agents/release-reviewer.md` both load it conditionally.

## [1.15.0] — 2026-07-27

Second pack off the v1.13.0 backlog.

### Added

- **`packs/devops/observability`** (Level 2 — OpenTelemetry, W3C Trace Context, and
  published practice). Principles P1–P16 and engineering rules OBS1–OBS44 across signal
  choice, tracing, metrics, logs, naming and resource identity, cost control, what
  telemetry may carry, working method, and a small-stack mapping. Cleared the intake gate
  on a verified gap: `OpenTelemetry`, `distributed tracing`, `cardinality`,
  `semantic convention`, `RED method`, `USE method`, and `golden signal` all returned zero
  across the 57-pack corpus.
- **The boundary against `devops/sre` is the pack's organising decision.** `SLO` returned
  111 hits and `error budget` 10, all in `sre` — which confirmed a boundary rather than an
  overlap. SRE owns the targets, alerting, and incident process; this pack owns the signals
  those targets are measured from and the debugging that starts once an alert fires. Both
  packs state it, and the glossary marks the terms that belong to the other.
- **Only two rules are starred, and neither is about observability.** OBS31 (no credential
  or token in telemetry) and OBS32 (personal data in telemetry is personal data —
  inventoried, pseudonymized, retained deliberately, reachable by the deletion path) are
  the safety floor arriving through this pack, since telemetry leaves the system into a
  third party's store with long retention and broad team access. The rubric says to score
  those findings here **or** in `security/privacy`, never both.
- **A small-stack mapping (OBS41–OBS44), stated before the rest rather than as a
  footnote.** Most of this domain assumes you operate services; a managed-platform MVP does
  not. The decision framework opens with a "do you need this pack yet" table whose honest
  trigger is *"we could not answer a question about production"* — not headcount or an
  architecture diagram. For a small stack the answer is platform logs, a request identifier
  generated at the edge and returned to the client, and error tracking with release
  identifiers. The matching anti-pattern is "the observability platform nobody needed", the
  prompt fragments include a block that explicitly tells an agent not to propose a
  collector for such a project, and the rubric refuses to deduct a small stack for having
  no distributed tracing — calling that a rubric error rather than a finding.
- `graphs/knowledge-graph.md` gains a concept node — *questions the system must be able to
  answer about itself* — linking observability, SRE targets, agent evals, and the
  executed-evidence discipline in `coding-agents`. `agents/release-reviewer.md` loads the
  pack to check whether a change ships debuggable.

### Authority level: 2, not the 1 the roadmap proposed

The backlog entry queued this at Level 1 on the strength of the OpenTelemetry
specification. Reconsidered while writing and recorded in the pack's `references.md`:
OpenTelemetry is a CNCF project, authoritative about itself and broadly adopted, but not a
normative standard in the sense of the IETF RFCs behind `security/auth` or of WCAG. The
reasoning half of the pack — unknown-unknowns, wide events, high cardinality as a feature,
the narrowing debug loop — is book-derived, which is Level 3 territory. Claiming Level 1
would lend book judgment the deference owed to normative requirements. Level 2 matches the
sibling `devops/sre`. W3C Trace Context genuinely is Level 1 and is cited as the authority
where the pack restates it.

## [1.14.0] — 2026-07-26

First pack from the v1.13.0 backlog, and the first to go through the source
intake gate that shipped with it.

### Added

- **`packs/architecture/philosophy-of-software-design`** (Level 3 — John Ousterhout,
  *A Philosophy of Software Design*). Principles P1–P19 and engineering rules PSD1–PSD36
  across module depth, information hiding, interfaces, errors and special cases, naming,
  comments, and working method. Cleared the intake gate on a verified gap: `Ousterhout`,
  `deep module`, `shallow module`, `information hiding`, `change amplification`,
  `temporal decomposition`, `tactical programming`, and `define errors out of existence`
  all returned zero hits across the 56-pack corpus. `information hiding` returning zero was
  the deciding signal — a foundational concept that no architecture pack covered.
- **The corpus's first pack with no starred rule and no CRITICAL scoring band.** Both
  absences are deliberate: this is a Level 3 design opinion, and a rubric that let it push
  a score into the Blocked band would make aesthetics outrank the things that genuinely
  block. Total deduction is capped at −40, and the pack scores `n/a` under the Prototype
  profile, where tactical programming is the correct mode.
- **A reviewer-discipline rule, carried in three places** (review checklist, scoring
  rubric, review-lens prompt fragment): a finding must name what a caller or the next
  reader stops having to know, or it is dropped, and a finding without that sentence does
  not score at all. "This module is shallow" with nothing after it is unanswerable — it
  either blocks work arbitrarily or teaches people to ignore design feedback, and the
  second costs more than the shallow module did. The pack's own `anti-patterns.md` lists
  that failure, and design theatre on a prototype, as failure modes of *applying* the pack.

### Changed

- **`core/conflict-resolution.md` gains canonical ruling R13.** This pack disputes the
  common reading of `solid` and `clean-architecture` on decomposition granularity — Level 3
  against Level 3, both architecture sources, so resolution steps 4 (authority) and 5
  (proximity) both tie and the existing rulings did not cover it. R13: **ask what the split
  hides.** A boundary that lets the caller stop knowing something wins; one that only
  reduces line count does not. State the tradeoff; a Level 0 file-size convention outranks
  both (R4); the packs agree far more than they differ, so this applies only at the margin.
  Added per `CONTRIBUTING.md`, which directs uncovered pack conflicts to this file rather
  than to patching one pack.
- **`packs/personal/pau-avila/coding-preferences.md` is untouched.** Its 200–400 line
  convention stands. The accurate reading of this pack — and the one that dissolves most of
  the conflict — is that it concerns *interface* depth, not file length.
- `agents/architecture-reviewer.md` loads the pack, with the MEDIUM ceiling and the
  name-the-beneficiary requirement stated at the point of loading rather than left in the
  pack. `graphs/architecture-graph.md` gains three concept edges, including the
  SOLID-versus-depth disagreement, and now describes seven packs.

## [1.13.0] — 2026-07-26

Corpus expansion release. Two new Level 1 packs closing verified zero-coverage
gaps, the six `ai-engineering` packs promoted out of `draft`, and the authoring
path hardened so the next batch is mechanical rather than archaeological.

### Added

- **`packs/security/auth`** (Level 1 — IETF RFC 9700 and RFC 6749, OpenID
  Connect Core, NIST SP 800-63B). Principles P1–P16 and engineering rules
  AU1–AU60 covering flow selection, the round trip, redirects, token validation,
  token storage and transport, session lifecycle, passwords and recovery,
  multi-factor, and enumeration. `★` marks the safety floor, which no reasoning
  profile modulates. Before this pack, `grep -ril 'OAuth\|OpenID'` across all 54
  packs returned nothing: `backend/supabase` covered row-level authorization and
  `owasp-asvs` covered stating a verification level, but nothing covered
  designing the login itself.
- **A Supabase mapping inside that pack** (AU54–AU60), so it does not
  re-litigate the stack it will most often load against — it names where the
  platform already satisfies a rule and where the rule is a setting shipped
  switched off. AU54 is the one most likely violated in practice: `getSession()`
  returns unverified cookie contents, and authorizing from it server-side is a
  client-trusted claim wearing server-side clothing.
- **`packs/security/privacy`** (Level 1 — Regulation (EU) 2016/679, EDPB
  guidelines on consent and on Article 25, AEPD cookie guidance). Principles
  P1–P18 and engineering rules PR1–PR49 covering inventory and purpose, lawful
  basis and consent, minimization and design defaults, retention and deletion,
  subject rights, processors and transfers, incidents and high-risk processing,
  and a Supabase/Postgres mapping. `GDPR` and consent-as-a-legal-basis returned
  zero hits before this. The pack carries a second disclaimer beside the
  standard distillation line: engineering guidance, not legal advice.
- **A source intake gate** in `core/source-policy.md`, answered before
  scaffolding: what position does this source hold that yields 10+ checkable
  rules, what gap does it close (shown by grep, not asserted), what authority
  level and why, and for a Level 3 paper or Level 4 web source, what corroborates
  it. States the rule the corpus had been following implicitly — **a pack is
  doctrine, not reference** — plus two recurring answers: papers enter as
  `sources[]` inside packs and are never packs themselves, and a website earns a
  pack only when it is the platform owner's normative documentation.
- **A draft→stable criterion** in `core/knowledge-schema.md`, built deliberately
  from checks that already existed (in-pack citation resolution, source grounding
  in `references.md`, prefix uniqueness, the README disclaimer) rather than new
  ones — a promotion bar nothing enforces is a bar that drifts.
- **Two `doctor.sh` checks** covering authoring steps nothing verified before:
  every non-personal pack README carries an independent-distillation line, and
  every `metadata.yaml` `related:` path resolves to a real directory. Both were
  confirmed to fail against a deliberately sabotaged copy before being trusted.

### Changed

- **The six `ai-engineering` packs are now `stable`** (`agent-foundations`,
  `context-engineering`, `coding-agents`, `agent-security`, `agent-evals`,
  `tool-design`). They had been `draft` since authoring — readable, but excluded
  from automatic routing and loadable only when a user named them — leaving
  roughly 7,000 lines of written content unreachable in normal use. Each was
  assessed against the new criterion, re-stamped (`last_reviewed: 2026-07-26`,
  `review_after` recomputed from the authority-level cadence), patch-bumped, and
  moved from the Experimental table into the stable routing catalog.
- **The Experimental section in `skills/akos/SKILL.md` is now empty by state, not
  removed.** The mechanism is permanent — `akos create-pack` still writes
  `status: draft`, and `schemas/routing_check.py` still fails the build on a
  draft pack appearing in the stable catalog.
- **`security-reviewer` loads `security/auth`, `security/privacy`, and
  `ai-engineering/agent-security`**; `database-reviewer` loads
  `security/privacy`. The agent-security dependency only became legal once that
  pack was stable — `routing_check.py` bars a stable agent from depending on a
  draft pack.
- **`packs/ux/wcag/README.md` carries the mandatory disclaimer.** It had shipped
  without any independence claim, which is what the new `doctor.sh` check caught
  on its first run. `core/source-policy.md` now requires *a* line opening with
  "Independent distillation" and pointing at `references.md` rather than one
  exact sentence — the terse variant several packs already use is legitimate for
  a standards body with no "originals to buy", and enforcing literal wording
  would have meant rewriting ~49 READMEs to fix one real bug.
- **`tests/unit/test_pack_lifecycle_routing.py` skips instead of passing
  vacuously** when the corpus holds no draft packs — now a reachable state. A
  green tick there would have claimed the draft mechanism was verified while
  nothing exercised it; `TestRoutingCheckSabotage` still covers the mechanism
  unconditionally against synthetic packs, and a new test asserts `list-packs`
  produces real output so the skips can't hide a broken command.

### Not done, deliberately

- **No graph-link check.** The plan called for `doctor.sh` to require every pack
  to appear in `graphs/knowledge-graph.md`. Checking first showed 19 packs
  absent — that file indexes cross-cutting *concepts*, not packs, and
  `testing/playwright` correctly has no node. The check would have encoded a rule
  the graph does not follow. Dropped, with the open question recorded in
  `ROADMAP.md`.
- **The oversized `ai-engineering` rule files were not split.**
  `agent-security/engineering-rules.md` runs ~18 KB / 95 rules against a
  40–200-line guideline. The content is correct, just long; promotion did not
  require restructuring it. Recorded in `ROADMAP.md`.
- **No bulk import.** Routing selects 2–5 packs from one flat table, so the
  corpus grew by two, not twenty. The evaluated catalog — four packs queued,
  five waiting on a stack trigger, eight rejected with the reason and the
  supporting grep — lives in `ROADMAP.md` so it isn't re-derived.

## [1.12.0] — 2026-07-23

Testing and CI reliability release. Versions 1.10.0 and 1.11.0 were internal
mainline milestones and were never tagged or published; 1.12.0 is the next
planned release version. No retroactive tags are created by this change.

### Added

- **Strict executable-rule contract.** Rule registries now validate required
  fields, types, enums, detector paths, non-empty globs, unknown fields and the
  optional `suppressible` flag. Security-floor rules are explicitly
  non-suppressible.
- **Bounded, fail-closed scanning.** Configurable file, per-file and total-byte
  budgets cover pruned traversal and auxiliary inputs. Unreadable inputs,
  malformed detector output and incomplete detector execution are structured
  operational errors, never false clean scans.
- **Expanded credential coverage.** Detection and history redaction share
  patterns for GitHub fine-grained PATs and common private-key blocks, plus a
  non-blocking high-entropy fallback with hash/SRI exclusions.
- **Mobile as an explicit score.** Review summaries and overall scoring include
  Mobile with profile weights `1/2/3/2/1/1`, and the full frontend route now
  executes UX, Accessibility, Mobile, Copywriting and Frontend quality.
- **Measured branch coverage.** `coverage.py` 7.15.2 is pinned as a development-
  only dependency, measures the Python unit, benchmark, subprocess, and
  integration paths, and fails CI below 80%. AKOS keeps no runtime Python
  package dependency.
- **Supported-runtime functional matrix.** CI now exercises the declared
  Python 3.10 floor on Ubuntu and current Python on macOS, while Ubuntu-only
  lint, validation, benchmark, and coverage gates remain in a separate quality
  job. Both jobs have bounded 12-minute timeouts.
- **Executable CI contracts.** Unit checks lock the job split, immutable
  `setup-python` pin, platform/runtime matrix, coverage threshold, and self-scan
  semantics. The self-scan helper accepts complete scans at exit 0 or 2,
  rejects operational exit 1, cross-checks the JSON status and errors, and
  permits blocking findings only for exact reviewed `rule_id` + fixture-case
  pairs. Secret findings have no self-scan exception.

### Fixed

- **Supabase analysis follows final ordered state.** SQL detectors preserve
  schema-qualified identities and fold CREATE/DROP, RLS enable/disable,
  table/schema grants and revokes, plus policy create/alter/drop in lexical
  migration order. `supabase/config.toml` supplies exposed API schemas.
- **CLI contracts match their documentation.** `eval` requires `--case`,
  `rules run --target` selects project, pack or all surfaces, usage errors
  return 1, and absent config emits `[]` in JSON mode.
- **Review evidence is honest about tooling.** Mobile measurements require
  browser/device evidence; otherwise the result is provisional and Coverage
  names what was not verified. Accessibility ignores commented markup and
  rejects empty ARIA names, while the amount-parser example rejects trailing
  junk and ambiguous grouping.
- **CI no longer aborts on expected self-scan findings.** AKOS's deliberately
  vulnerable fixtures produce blocking findings and exit 2 by contract. The
  prior `bash -e` step stopped there, before parsing the JSON and before every
  later test gate; the new helper preserves the 0/1/2 contract explicitly.
- **The CLI E2E test is isolated and parallel-safe.** It now runs from a
  temporary AKOS checkout, writes all reports into its owned temp directory,
  uses unique pack/profile names, and removes only that temp root. It cannot
  delete a pre-existing profile or pack from the working repository.

## [1.11.1] — 2026-07-23

Mandatory filesystem-integrity hotfix. This is the first release candidate
intended for tagging after v1.9.0; the 1.10.0 and 1.11.0 entries below describe
internal mainline milestones and are intentionally not retroactively tagged.
No tag or remote release is created by this source change.

### Fixed

- **Review history is fail-closed at every filesystem boundary.** Project and
  review roots are resolved once; symlinked path components, review entries,
  internal files, and `.gitignore` are rejected. `clean` validates the complete
  review set before deleting anything and accepts only real directories
  containing exactly the three regular review artifacts.
- **Project installation is prevalidated and transactional.** The project must
  already exist as a real directory, all four managed destinations and their
  parents reject symlinks, malformed CLI invocations return usage code 1, and
  prepared writes restore every original if any replacement fails.
- **Profile selection uses the same filesystem trust boundary.** `profile use`
  now updates `.akos/config.md` through an fd-relative, no-follow transaction
  and rejects a linked `.akos` parent instead of writing outside the project.
- **Uninstall preserves foreign launchers.** `~/bin/akos` is removed only when
  it belongs to this checkout or another recognizable AKOS installation.
- **Integration tests no longer share repository or `/tmp` state.** E2E runs
  use an owned `mktemp` tree containing a full checkout copy and remain safe
  under concurrent execution.
- **The CI self-scan distinguishes findings from incomplete execution.** Exit
  0 and 2 are validated against the JSON result; exit 1, malformed output,
  reported errors, or code/status drift fail the gate immediately.

## [1.11.0] — 2026-07-23

P1 integrity hardening. Six places where a real gap remained after v1.10.0's
P0 pass, closed with real code, a full corpus migration, and adversarial
tests — not a plan. `schemas/history.py`'s atomic-publish write path was
already correct going into this release (staged writes, `secrets`-based
unique ids, no-clobber `os.rename`); the remaining P0-adjacent gap was on
the *reader* side only.

### Added

- **`bin/marked_sections.py`** — single shared parser for `AKOS:START`/`END`
  managed sections, replacing two independent, first-match-only
  implementations (`write_marked_section`'s `grep -nF | head -n1`, and
  `cmd_profile_use`'s separate awk state machine). A file is now classified
  `ABSENT` / `PRESENT` / `INVALID` (multiple starts, multiple ends, one-sided,
  out of order); `INVALID` refuses to write rather than silently guessing
  which pair to touch. Atomic via `tempfile.mkstemp` + `os.replace`, mode
  and newline-style (LF/CRLF) preserving. `akos install-project` now
  preflights all 4 managed targets (`CLAUDE.md`, `AGENTS.md`,
  `.cursor/rules/akos.mdc`, `.akos/config.md`) before writing any of them.

- **`bin/akos-common.sh`** — shared `resolve_python`/`check_python`/
  `require_python`, the one place that resolves and version-floors Python
  (3.10+) for `install.sh`, `update.sh`, `doctor.sh`, and `bin/akos`.
  `install.sh`/`update.sh`/every operational `akos` subcommand now refuse to
  run at all without a valid interpreter — `doctor` and `help` are the two
  documented exceptions, since `doctor` is the command that *reports*
  Python's absence as a finding. `doctor.sh`'s own missing/old-Python check
  changed from a warning to a build failure. Removed the one silent
  fallback this uncovered (`create-pack`'s `review_after` date computation
  now fails loudly instead of silently substituting today's date).

- **`schemas/routing_check.py`** — a pack's lifecycle status now has a real
  operational consequence. `skills/akos/SKILL.md`'s single routing table
  (which held all 6 `ai-engineering/*` draft packs identically formatted to
  the 48 stable ones, one labeled "Safety floor") is split into a Stable
  routing catalog and a separate Experimental section; the checker verifies
  every stable pack is in the former and every draft pack only in the
  latter (by table line-position, not a whole-file text search, so the
  file's own illustrative prose mention of a draft pack doesn't
  false-positive), and that no `status: stable` agent or workflow depends
  on a draft pack. `schemas/config_check.py` now flags a draft or deprecated
  pack listed in a project's `.akos/config.md` "Packs to always load" —
  advisory (draft is readable, just not promised-stable), not a hard block,
  and there is no `allow_draft_packs` escape hatch. `bin/akos list-packs`
  gained `--all` and `--status stable|draft|deprecated` (default: stable
  only), backed by the real YAML parser instead of a directory walk.

- **`bin/personal_layer_integrity.py`** — manifest-backed backup, verify,
  and restore for `packs/personal/`. `update.sh`'s restore path was still
  `cp -Rn ... || true` followed by an unconditional "personal layer
  preserved," and the script always exited 0 even when `git pull` failed —
  both fixed. `update.sh` now: acquires an atomic `mkdir` lock (concurrent
  runs are rejected); backs up personal/ and immediately verifies the
  backup against the live source; runs `git pull --ff-only`; unconditionally
  diffs the personal layer against the pre-update manifest and, on any
  drift — even from a legitimate upstream commit — performs a full-tree
  staged swap back to the snapshot (not a partial fill; a file the pull
  *added* is reverted too, because "personal" means the operator's layer to
  change, not the pull's); and actually invokes `doctor.sh` as a final gate
  instead of only suggesting it. The exit code now reflects every one of
  those steps: a failed backup, failed restore, failed pull, non-git
  checkout, or failing final `doctor.sh` all make the script exit non-zero,
  and "Update complete" is only ever printed after all of them passed.

### Changed

- **Schemas are versioned and strict.** `schemas/registry.json` resolves
  each contract kind (`knowledge-pack`, `agent`, `workflow`) to its current
  version; the 3 schema files moved to `schemas/v1/` (no alias — 8 internal
  references updated in the same change; nothing external depended on the
  old flat paths). Every schema now requires `schema_version: 1` and sets
  `additionalProperties: false` at the root and every nested object
  (`sources[]`, `conflicts[]`, `profiles` for packs) — an unknown or
  mistyped field (`maintaner`) is now a validation error, not silently
  ignored. `schema_version: 1` was backfilled onto all 54 non-personal
  packs (`bin/migrate-pack-metadata.py`, idempotent, append-only) and all 13
  agents. Workflow frontmatter, previously optional and universally absent,
  is now required by `schema_version: 1` — all 9 `workflows/*.md` were
  migrated to carry `id`, `description`, `agents`, `packs`, `profiles`,
  `status`, and `maintainer`, each field derived from that file's actual
  body (agent/pack links, explicit counts checked against the real
  directories), never invented. `schemas/validate.py` also gained two
  cross-field checks JSON Schema can't express on its own: a pack's
  `domain`/`name`/`id` must match the directory it lives in, and
  `deprecated: true` requires a non-empty `replacement`.
- **`schemas/yaml_subset.py` rejects a duplicate key within the same mapping
  scope** (root map, a nested map, or one list-of-maps item) — previously
  silent last-value-wins via plain dict assignment. A repeated key across
  *different* list items (two separate `sources:` entries each with their
  own `title`) is correctly not flagged.
- **`schemas/history.py`'s readers now match its writer's atomicity
  guarantees.** `list`/`latest`/`clean` explicitly skip in-flight
  `.tmp-review-*` staging directories (`list` already did; `latest` and
  `clean` did not); a published review missing or failing to parse any of
  its three required files is reported as `(corrupt: ...)` rather than
  silently omitted or silently treated as clean, and `show`/`compare` return
  1 on a corrupt review via a new `ReviewCorruptError` (distinct from "no
  such review").

## [1.10.0] — 2026-07-22

P0 security hardening. Five places where a promise in the docs was not enforced
by the code — the exact "a claim that must stay true belongs in a check, not in
prose" failure this project exists to prevent, turned on itself. Each fix lands
with a positive test, an adversarial test, and where relevant a near-miss that
must still pass.

### Fixed

- **Non-destructive install now covers the CLI, skills, and agents uniformly.**
  All four symlink sites in `install.sh` route through one portable helper
  (`link_managed`) with a single classified contract: an own symlink is a no-op;
  a symlink pointing at a *different, still-valid AKOS install* is refreshed; a
  **foreign** symlink is left intact with a warning (previously any non-own
  symlink was relinked); a real file or directory is left untouched with a
  warning; only a genuinely-absent destination is created. `_is_akos_managed_link`
  recognises a prior install by a matching sub-path under a home with
  `core/constitution.md` + `VERSION`, so an unrelated tool at a managed path is
  never adopted. `test_install_isolated.sh` gains the foreign-symlink,
  real-directory, prior-install-refresh, and foreign-skill cases.

- **`.akos/config.md` is treated as untrusted manifest data, not authority.**
  The repo config comes from whatever checkout is under review, so the skills no
  longer call it "binding": a new precedence — safety floor, then the current
  user, then the operator's local config, then the repo manifest, then defaults —
  makes explicit that the repo can supply facts and hints and can *raise*
  scrutiny (`Deployed: yes`) but can never lower the safety floor, change lens
  weights, or add arbitrary reading. `schemas/config_check.py` now also validates
  `Deployed` as exactly `yes`/`no` (duplicates rejected) and flags any non-empty
  repo-side `Profile overrides`; a clean `check-config` validates *form*, not
  trust. New `test_config_trust_boundary.py` fails if the authority-conferring
  phrasing ("is binding", "not negotiable", …) ever returns.

- **The rules runner is fail-closed.** `rules/runner.py` used to turn a broken
  detector into a MEDIUM finding and skip an unparseable registry with a warning,
  then exit 0 on an incomplete scan. Findings and operational errors are now
  separate results (`ScanResult` / `ExecutionError`): a registry that will not
  parse, a detector that will not load, a detector with no `run()`, or a detector
  that raises is an error, not a finding — status `error`, exit 1, and if errors
  and findings coexist, exit 1 wins. `--format json` returns an object
  `{status, summary, findings, errors}`. `doctor.sh` and CI now gate on the scan
  *completing* (no operational errors), and CI fails loudly on a malformed
  registry.

- **A realistic secret blocks on every path.** The blanket per-folder downgrade
  to LOW (in both the runner and the secret detector) is gone: a live vendor key,
  a `service_role` JWT, or a high-entropy generic secret is marked `blocking` and
  gates the exit code wherever it sits — `tests/`, `fixtures/`, `docs/`, or
  shipping source. Severity is decided per rule and evidence, never by directory.
  AKOS's own synthetic corpus stays clean not by a path exception but by keeping
  credential-shaped literals out of version control: benchmark fixtures store
  non-detectable placeholders that the harness materialises into a throwaway temp
  copy at scan time, and unit-test tokens are assembled at runtime. The
  fixture-downgrade tests are rewritten to the new contract (detected and
  blocking, not LOW).

- **Review history ids are unique and published atomically.** `schemas/history.py`
  keyed reviews by `timestamp-type` at second precision with
  `mkdir(exist_ok=True)`, so two records in the same second collided and the
  second overwrote the first, and the three files were written straight into the
  final directory, so a crash left a partial review. Ids now carry a
  `secrets.token_hex(4)` suffix (a sortable prefix, not the identity), and a
  record is staged in a sibling temp dir and published by an atomic
  `os.rename` — a published review is never overwritten (rename onto it fails and
  the id is regenerated), and a mid-write failure leaves no partial review and no
  orphan staging dir. Concurrent records all survive. Malformed review JSON is
  handled on read instead of crashing `list`/`compare`.

## [1.9.1] — 2026-07-22

A data-loss fix in `install.sh`. The 1.8.0 remediation added no-clobber guards
to the skill and agent link steps, but step 3 — the `~/bin/akos` CLI symlink —
was left on the old code path.

### Fixed

- **`install.sh` no longer destroys a real `~/bin/akos`.** The guard folded
  symlinks and regular files into one branch (`[ -L … ] || [ -e … ]`) and ran
  `ln -sf`, silently replacing any real file a user kept at that path — directly
  contradicting the script header's "Never destroys content" promise and the
  no-clobber discipline every other link step already followed. Step 3 now uses
  the same three-branch shape as `link_skill()`: an own symlink is a no-op, a
  foreign symlink is relinked (a symlink holds no content), and a **real file is
  left untouched with a warning**. `test_install_isolated.sh` gained two cases —
  a real file at `~/bin/akos` survives with the warning, and a foreign symlink
  is relinked — the first of which failed against the pre-fix script.

## [1.9.0] — 2026-07-21

Audit follow-ups: consistency guards and a right-sized pack contract. Four
findings the 1.8.0 remediation left for a considered pass, each landed on its
own with the same discipline — a claim that must stay true became a check.

### Added

- **Sources are grounded in the reading list.** `metadata.yaml`'s `sources[]` and `references.md` are two lists of the same citations, and they had drifted — 18 packs named a structured source that did not appear in the pack's own reading list (a renamed or invented title). Aligned all 18 to their `references.md` bullet verbatim, and added `test_sources_references_integrity.py`: every `sources[].title` must appear in `references.md`. The audit's "52/54 disagree" was a raw-count overcount; the real integrity violation was 18, now 0.
- **Every rule-code prefix is defined by exactly one pack.** Nine prefixes were owned by two packs (an ambiguous `AP1` — which pack?). Four were genuine dual-definition, resolved by renaming the pack with zero external citations: apple-hig `AP→AHE`, escaping-the-build-trap `BE→BTE`, css `CE→CSE`, continuous-discovery `CE→CDE`, deployment `DP/DP-E→DPL/DPL-E`. The other five (OW, ER, NR, NG, WC) were citation artifacts — one pack defines the series, others cite it — so `test_pack_prefix_uniqueness` now counts definitions only (a code at a list-item start), not citations, and asserts zero collisions with no baseline to grandfather.
- **The Maintainability rubric that the template required but never had.** `Maintainability` is a scored line in all four Review Summary copies and carries a profile weight, but no `scoring/maintainability-score.md` existed. Added it (naming, unit size, nesting, error handling, coverage, dead code; distinct from Architecture).
- **`doctor.sh` cross-checks manifest descriptive fields**, not just `version` — `displayName`/`description`/`license` must agree across all four plugin manifests, so a one-line edit can't ship two product descriptions to two marketplaces with a green build.

### Changed

- **The 17-file pack contract is now 12 required + 5 optional.** The optional file-types (`philosophy`, `mental-models`, `examples`, `prompt-fragments`, `glossary`) are present only when the source has something distinct to say; `doctor.sh` enforces the required 12, and `akos create-pack` scaffolds only those rather than emitting empty stubs that make "the template ran" look like content. A read-based audit of all 162 optional files (not a line-count heuristic) found the file-types are overwhelmingly NOT ceremony — every `philosophy.md` is a genuine worldview, every `mental-models.md` names a real framework — so only **3** glossaries that pure-re-index a numbered principle catalog were removed (twelve-factor-app, continuous-discovery-habits, universal-principles-of-design). The audit's premise that these files are mass ceremony did not survive reading them.

## [1.8.0] — 2026-07-21

Audit remediation. A multi-lens audit (self-run plus an external report) found
that AKOS applied its own "a claim that must stay true belongs in a check, not
in prose" discipline to its packs and rules but not to its own detectors,
lifecycle scripts, or release mechanics. This release closes the load-bearing
gaps. Two of them were CRITICAL and reproduced in a live harness.

### Fixed

- **The generic secret detector was blind to prefixed env-var names.** `SECRET_IN_SOURCE`'s catch-all keyed on `\b(api_key|secret|token|password|...)` — but `_` is a word character, so `\b` never fired between `STRIPE_` and `API_KEY`. `STRIPE_API_KEY`, `OPENAI_API_KEY`, `DB_PASSWORD`, `myApiKey` — the dominant naming convention — all slipped past while the benchmark stayed green. The keyword may now be the suffix of a longer name; the `[:=]`-plus-quoted-value requirement still carries precision. Locked down in `test_rules_detectors.py` with prefixed and negative cases.
- **Fixture/server-path downgrades keyed on the absolute path, so ancestors above the project voted.** A repo checked out under `.../test/proj/` or `/tmp/fixtures/proj/` had every real secret downgraded CRITICAL→LOW, and a `service_role` reference under an ancestor named `api/` produced zero findings. Detectors now classify on the path relative to the scanned root; the absolute path is still what gets read. `runner.py` passes the scan root through, and both detectors take it.
- **Rule detectors followed symlinks out of the scanned tree.** Scanning an untrusted repository that planted `link -> ~/.ssh/id_rsa` made the secret detectors read the host's private key — which a review report then quotes as evidence. `collect_files` now skips symlinks and any path whose real location escapes the scanned root.
- **`uninstall.sh` could delete the personal layer while reporting it preserved.** Under `set -uo pipefail` (no `-e`), a failed backup `cp` did not abort — `rm -rf` ran anyway and printed "personal layer preserved". Now `set -e`, the backup covers all of `packs/` (not just `personal/` — `create-pack` writes user packs elsewhere), a failed backup aborts, and the script refuses to `rm -rf` a directory that does not look like an AKOS root. The confirmation prompt now enumerates what is lost.
- **`update.sh` reported a backup that might not exist, in a purgeable location.** Same missing-`set -e` shape; the backup also went to `mktemp -d` under `/var/folders`, which macOS purges. Now a durable `$HOME/.akos-backups/` location, and a failed backup aborts the update.
- **Path traversal and code injection in the CLI.** `akos create-pack "../../evil"` scaffolded outside `packs/` (verified), and a quote in a profile name broke out of an inline `python3 -c` script into arbitrary Python. Names are now validated against the schema's pack-name charset, and values travel to Python as argv, never interpolated into the script text.
- **`yaml_subset.py` silently mis-parsed several constructs its own contract says it rejects.** An escaped quote before a `#` truncated the value mid-string; nested flow lists (`[a, [b, c]]`) and nested block lists (`- -`) returned raw strings; unterminated quotes were accepted with the quote embedded. The comment-stripper now honours `\` escapes, and the four silent mis-parses raise `YamlSubsetError`. New adversarial test class.
- **`discover_rules` crashed the whole run on one broken rule registry.** One unparseable `rules/*/*.yaml` took down discovery for every rule with a raw traceback; the three sibling call-sites already guarded this. Now it skips the broken file with a warning.
- **Committed Python bytecode.** `schemas/__pycache__/*.pyc` was tracked despite `.gitignore`; it regenerated locally and broke `git pull --ff-only` in `update.sh`. Untracked, with a CI guard so it cannot recur.

### Added

- **shellcheck now gates CI** (was `|| true`, permanently green), at `-S warning`, over all six scripts including `merge-pr.sh`, which was absent from every protective loop. `merge-pr.sh` added to the CI syntax check, the install/update chmod loops, and the `doctor.sh` executable check.
- **Release traceability.** `merge-pr.sh` tags `vX.Y.Z` on a release merge to the default branch (only when VERSION and the CHANGELOG agree and no such tag exists); `doctor.sh` warns when the current VERSION has no matching tag; README documents rollback via `git checkout vX.Y.Z && ./install.sh`. A retroactive `v1.7.0` tag marks the prior release.
- **Supply-chain hardening.** `permissions: contents: read` on all three workflows; `actions/checkout` and `actions/upload-artifact` pinned to commit SHAs; `.github/dependabot.yml` keeps the (SHA-pinned) actions current; `SECURITY.md` documents private disclosure.
- **Isolated lifecycle-script tests.** `test_install_isolated.sh` and `test_uninstall_isolated.sh` run the real scripts against a scratch `$HOME` and cover the no-clobber guards and the backup-abort path — previously untested, the highest-blast-radius code in the repo. `test_update_preserves_personal.sh` now also exercises the durable-backup path.

## [1.7.0] — 2026-07-20

Version staleness, made into a check after recurring.

### Added

- **Eval cases for the last four lenses — product, UX, performance and database — completing one case per lens across all twelve.** A floor rather than a claim of depth: most lenses have exactly one case, so a green run means "did not regress on one known artifact per lens" and nothing more. The README says so.

  The traps carry the weight, as before. `ux-async-states` pairs a component missing the empty and error branches with one that has all four, so a review that flags both has matched on the query hook instead of reading the branches. `db-missing-index` puts a performance defect on a correctly secured table, because conflating the two buries the real finding under a wrong one. `perf-budget-not-enforced` ships a budget script that reports and exits 0 — the masked-gate shape reached by omission rather than by `2>/dev/null` — and traps a review that recommends adding what already exists. `product-output-not-outcome` sets two briefs side by side so the difference is checkable against the documents rather than a matter of taste: one names a measured problem, two metrics and an explicit out-of-scope; the other defines success as shipping six charts by a date.

### Added

- **Eval cases for the testing, release, accessibility, architecture, mobile, copy and frontend lenses** — coverage goes from one lens to eight. Every fixture is a shape read by hand in a real repository. The traps matter more than the finds: reporting a `Field`-wrapped input as unlabelled, flagging an advisory `|| true` as a gate, translating away strings the project's own style direction commits to, calling a `forwardRef` primitive an anti-pattern.
- **`doctor.sh` runs AKOS's own rules against this repository** and fails on a CRITICAL, so "AKOS passes its own rules" is a check rather than a sentence. It distinguishes exit 0, 2, and *anything else* — a run that broke is not a clean result. Covered by its own integration script, because a gate nobody tests is a gate nobody knows works.
- **`doctor.sh` warns when VERSION has drifted behind the work.** Two checks: VERSION must agree with the newest CHANGELOG entry, and — the one that would have caught what actually happened — a warning when commits touching source have landed since VERSION last changed.
- **Proximity matching in the eval grader.** Terms must fall inside one 240-character span rather than anywhere in the document.

### Fixed

- **Fixture-path downgrading moved into the runner**, applied to every rule, so a detector cannot opt out by omission — which is how `SECRET_IN_SOURCE` came to apply it to one of its three branches and left AKOS unable to scan itself without reporting itself. Downgrade, never suppress: a real key or migration parked under `tests/` is still real.
- **Both known detector gaps closed**: a table protected by `REVOKE ALL` rather than RLS, and the fixture-exclusion asymmetry above. A *partial* revoke is still reported.

### Corrected

- **"`akos rules run .` exits 0 on this repository" was false when written** in the previous release's commits. `--rule SECRET_IN_SOURCE` was verified and the whole run asserted from it. The same shape as the CI misdiagnosis recorded in 1.6.0 — verify the specific, assert the general — repeated the same day, in a commit whose subject was verification discipline. It is now a check, which is the only fix that holds, and the failure mode is written into `coding-agents` as CAE53 and the "narrower check" anti-pattern.
- **Version staleness recurred.** 1.6.0 was bumped after ten commits had accumulated under 1.4.0's heading; eight more then accumulated under 1.6.0's. Bumping fixed the instance twice and the class neither time. The warning above is the class.

## [1.6.0] — 2026-07-20

Everything here came from *using* AKOS rather than reading it. Two real
reviews were run against real repositories for the first time, and doing
so found defects that six static reviews had missed — including one
already sitting in `main`.

### Added

- **`evals/` — the first thing that measures AKOS's actual output.** `benchmarks/` measures the deterministic rules engine; nothing measured the review, which is what AKOS produces. `packs/ai-engineering/agent-evals` scored that dimension around 18/100 and was right to.

  Each case is a small fixture built from **real code shapes taken from repositories reviewed by hand**, plus an `expected.yaml` naming the findings a competent review must surface and — more valuable — the ones a careless review wrongly reports. All three `must_not_find` traps are false positives that actually happened: the `private` schema table protected by `REVOKE ALL`, the policy a later migration drops, the optional-auth chain.

  The design decision that makes it honest: **it grades a report, it does not produce one.** Generating the review inside the grader would make the suite depend on a provider and on run-to-run variance, and there is no defensible way to gate on that. Grading is deterministic; producing is not. Matching is concept-based rather than exact — every `match_all` term plus at least one `match_any` term, case-insensitive — because exact-match grading on prose measures phrasing, not correctness.

  Thresholds are constants in the runner, stated before any run: recall 1.0, false positives 0. Recall is all-or-nothing because every `must_find` is a defect a hand-verified read confirmed is really there.

  `akos eval --report PATH --case ID`. `--case` is required, not a filter — see below.

### Added

- **Seven benchmark cases carrying shapes from real repositories** (`real-` prefix), closing the gap that made the suite's own precision number misleading. The 21 synthetic cases were written alongside the detectors they exercise, so they reported **precision 100%** while three real repositories each produced a *distinct* set of false positives the corpus could not contain. Six of the new cases are `must_not_detect`: RLS enabled by a dynamic `execute format` loop, `<Input>` the React component versus `<input>` the element, `service_role` inside the comment warning against it, a `drop column` documented in a comment, a policy a later migration drops, and a key in a gitignored `.env`. The seventh is the anti-amnesty pair — a table created *outside* the dynamic loop's array must still be reported, so a fix for a false positive cannot become a blanket pass.

  **Each was sabotage-verified**: the corresponding fix was reverted one at a time and the case confirmed to go red, then restored. That caught a real defect in the first draft of the accessibility case — it left `must_not_detect` empty, so it passed with the bug reintroduced. Split across two fixture files, because `LINE_TOLERANCE` is 3 and a `must_detect` and `must_not_detect` in the same file can match each other's finding and pass either way.

  The runner's summary line now states the ratio rather than a bare percentage: *"7 of 28 cases carry shapes taken from real repositories; the rest are synthetic and were written alongside the detectors they exercise. This number read 100% while every Level-A finding on three real repositories was a false positive."*

### Corrected

- **The previous entry's claim that `akos rules run .` exits 0 on this repository was false when written.** Only `--rule SECRET_IN_SOURCE` had been checked; the full run still exited 2 on the RLS fixtures, which are deliberately vulnerable because that is their job. Verified the specific case and asserted the general one — the same mistake as the CI-history misdiagnosis recorded above, made again in the same day.

### Fixed

- **Fixture-path downgrading moved into the runner, applied to every rule.** It had been per-detector, which is how `SECRET_IN_SOURCE` came to apply it to one of its three branches. Now a rule cannot opt out by omission. Behaviour is unchanged for real code — a missing RLS policy in `supabase/migrations/` is still CRITICAL — and a deliberately-vulnerable file under a fixture path drops to LOW while **still being reported**. `akos rules run .` on this repository now exits 0, verified on the full run this time.
- Known limitation, recorded rather than discovered later: every benchmark fixture lives under a `fixture/` path, so every benchmark finding is now downgraded and **the benchmark corpus can no longer catch a severity regression**. Severity is covered instead by unit tests that call detectors directly and by three new runner-level tests.


- **AKOS failed its own security rule.** `akos rules run .` on this repository exited 2, reporting its own benchmark fixtures as CRITICAL leaks. `is_fixture_or_doc_path` was applied only before the generic high-entropy branch, so the vendor-pattern and JWT branches never saw it. Fixtures now **downgrade to LOW rather than suppress** — a real credential pasted into a test file is still committed, so the finding survives and says why, but it stops gating a deploy. Suppressing outright would hide a real leak in any directory someone names `tests/`. Verified in both directions: the same AWS key reads HIGH in `src/` and LOW in `tests/`.
- **A table closed by `REVOKE ALL` rather than by RLS is no longer reported as unprotected.** Revoking every API-reachable role is stronger than a policy — there is nothing to mis-write later. This was recorded as a known gap when the schema-awareness fix landed and is now closed. A **partial** revoke (one role, not all) is still reported, which is the correct direction, and an unrelated table's revoke does not cover its neighbour.


- **Detector precision, round two — measured on a third real repository.** A Production Supabase app with 471 files and 65 migrations produced **162 findings including 32 CRITICALs, and none of the 40 non-accessibility findings held.** Five more causes, each now fixed with a regression test asserting both directions:
  - `A11Y_INPUT_NO_LABEL` matched `<input\b` with `re.IGNORECASE`, so it matched **`<Input>`** — the React component, which JSX capitalises precisely to distinguish it from the element. 110 of 122 findings pointed at components whose label comes from the `<Field label="…">` wrapper, burying the 12 genuine `<input>` elements underneath. The tag name is now matched case-sensitively.
  - `SUPABASE_RLS_DISABLED` could not see RLS enabled through `execute format('alter table %I enable row level security', t)` over an array literal — a pattern *stronger* than per-table DDL, since a table added to the list cannot be half-protected. It reported 31 CRITICALs against tables protected exactly that way. The table list is now read from the array literal; a dynamic loop whose list cannot be parsed still degrades to a false negative, which is the correct direction for a gating rule. Its docstring called dynamic SQL a known blind spot causing false *negatives* — it was producing false positives, the more damaging direction, and the note is corrected.
  - `SERVICE_ROLE_IN_CLIENT` did not mask TypeScript comments, so it flagged `src/lib/supabase.ts` for a comment reading *"A service_role key must NEVER be a `VITE_*` variable"* — the warning against the defect, reported as the defect. New `mask_js_comments` (offset-preserving, string-literal aware, the same contract as `mask_sql_comments`).
  - `DESTRUCTIVE_MIGRATION_NO_GUARD` searched raw text and never called `mask_sql_comments`, unlike its siblings, so a comment documenting *planned* debt read as a destructive statement.
  - The guard vocabulary is five English words, so a `drop table` justified across fourteen lines of Catalan reads as unguarded. **Not loosened** — a destructive migration asking for an explicit marker is the rule working. The recommendation now names the language limit and points at the language-neutral `-- akos:allow` escape.
  - Net on that repository: **162 findings → 14**, all 32 CRITICALs gone, and the survivors are real: 12 genuine unlabelled `<input>` elements, one real `drop table`, and one `using (true)` on a global catalogue that is correct by design.
- Three real repositories have now each produced a **distinct** set of false positives that the 21 synthetic benchmark fixtures do not contain, while `benchmarks/` reported precision 100% throughout. The fixtures are not wrong; they measure a corpus written by the same process that wrote the detectors.


- Two defects in the eval suite, both found by running it rather than reading it:
  - **Grading a report against every case produced a confidently wrong answer.** A real review of one project scored 0% recall against another project's case — "missing" findings that describe a different codebase — and tripped a trap because it happened to use the words. `--case` is now required, so a report is only ever graded against the fixture it reviewed.
  - **A generic match term matched a section heading.** `notes` in `match_all` was satisfied by a `## Notes` heading in a report that never mentioned the table, giving 100% recall to a report that found nothing. Now qualified (`public.notes`) — the same generic-term precision bug the detectors had, in the tool built to catch it.
- Deliberately **not** added: a CI step for the eval suite. CI has no review reports to grade, so a step iterating the cases would report green while doing nothing — the vacuous pass two Level C benchmark cases shipped with. What CI does run is `tests/unit/test_evals.py`, including `test_every_case_can_fail`, which asserts every case goes red on an empty report.


- **Detector precision, measured on real repositories instead of fixtures.** The first two real runs put the rules engine against code nobody had written it against. On a well-built Supabase app it produced 30 findings including two CRITICALs, and **every one of the nine Level-A findings was a false positive**. Five distinct causes, each now fixed with a regression test built from the real shape rather than a synthetic one:
  - `SUPABASE_POLICY_TOO_PERMISSIVE` read `CREATE POLICY` but not the 26 `DROP POLICY` statements elsewhere in the same migration set, so policies the author had already removed were still reported. It is now migration-order aware, tracking the live policy set across files — the asymmetry is that `SUPABASE_RLS_DISABLED` already did this and its sibling did not.
  - `SUPABASE_RLS_DISABLED` parsed `CREATE TABLE IF NOT EXISTS private.app_secrets` as a table named `private` (the pattern only stripped a literal `public.` prefix), and reported CRITICAL against a secrets table deliberately kept in a non-exposed schema behind `REVOKE ALL` — stronger than the RLS it was accused of lacking. Now schema-aware, and only tables in API-exposed schemas are considered. A table in `public` protected by `REVOKE` rather than RLS is still reported; that is recorded as a known gap rather than silently handled.
  - `SECRET_IN_SOURCE` flagged a `service_role` key in a **gitignored** `.env` — the one place it belongs — for a rule titled "committed to source". It now resolves git-ignore status once per batch and skips ignored files.
  - `A11Y_INPUT_NO_LABEL` matched input tags with `[^>]*`, which stops at the `>` inside `onChange={(e) => …}`. The tag was truncated at the arrow and every attribute after it, usually including `aria-label`, went unseen: 8 of 21 findings were correctly-labelled inputs. The matcher is now brace- and quote-aware.
  - `DESTRUCTIVE_MIGRATION_NO_GUARD` accepted only a guard *comment*, so a `DROP COLUMN` immediately preceded by the `INSERT … SELECT` that moved its data — expand-contract, done in the right order — was reported as unguarded. A preceding statement that preserves the specific table and column now counts; an unrelated `INSERT` above a `DROP` still does not.
  - Net on the same repository: 30 findings → 10, both CRITICALs gone, and the survivors verified by hand as genuine (4 intentional public-read policies, for which the suppression comment exists, and 6 real unlabelled inputs).
- **What this says about the benchmark.** `benchmarks/` reported **precision 100%** throughout, and still does — it is measured against 21 synthetic fixtures written by the same process that wrote the detectors, in the same session. `packs/ai-engineering/agent-evals` names that as contamination by iteration and warns the corpus "cannot surface a failure mode the detector's author did not already have in mind". This is that prediction coming true, with a number attached: 100% on the curated corpus, 0 of 9 on the first real repository. The 21 cases were not wrong; they were measuring something narrower than their headline implied.


- **Seven deterministic detectors were wired to nothing.** `rules/` shipped working checks for committed secrets, `service_role` in client code, tables without RLS, always-true policies, missing rollback migrations, unguarded destructive SQL and unlabelled inputs — and no skill, agent or workflow referenced them. The security lens was instructed to hunt for committed secrets by hand while `SECRET_IN_SOURCE` sat unused, and, holding only `Read, Grep, Glob`, could not have run it if told to. The review skill now runs `akos rules run` as step 3, before dispatching any lens, and routes each finding to the lens that owns it; the receiving agents start from those findings and say so in Coverage if they were not handed them. `A11Y_INPUT_NO_LABEL` is passed through labelled Level B and capped at MEDIUM, a lead rather than a finding.
- **`backend-reviewer` had profile weights in all six profiles and no route.** It appeared in no lens table, no workflow and no prompt — a registered subagent nothing could reach, shipped that way since 1.0.0. Now routed explicitly alongside `database-reviewer` as an agent that sits outside the twelve, invoked from lens 7 and alongside lens 8 on API surfaces. The `akos-review` skill description also listed `database` in place of lens 11 (personal rules); corrected.
- **Five agents still loaded `packs/personal/pau-avila/` hardcoded.** The 1.4.0 decoupling covered skills, core and templates but missed `agents/`, so a project running `akos profile use alice` got Alice's Level-0 layer nowhere and Pau's in five lenses. The load paths are now `packs/personal/<personal_profile>/`. The three `pau-avila principle N` citations stay, per the scope decision recorded then: a second profile would not share this one's numbering.
- `tests/unit/test_wiring.py` locks all three. Each was individually valid — an unrouted agent file parses, an uninvoked detector passes its own tests, a hardcoded path works — so only the *relationship* was wrong, which is exactly what no existing check looked at.


- **Safety floor: nothing told a reviewing agent that project content is data, not instruction.** A repo-wide search found zero such language in `skills/`, `agents/`, `core/`, `templates/`, `prompts/` or `workflows/` — while thirteen subagents read arbitrary third-party repositories with `Read`, `Grep` and `Glob`, and `skills/akos/SKILL.md` declared every section of a project's `.akos/config.md` "binding", including a pack list and free-text Notes that "override your assumptions". A cloned repo could therefore lower the review profile (Prototype skips five lenses), add its own files to the agent's mandatory reading as authoritative knowledge, and pre-authorize its own conclusions. Now: **`akos check-config`** — a new command that verifies the profile is one of the six, `personal_profile` is a plain name, and every listed pack resolves inside AKOS's own `packs/`, exiting 2 otherwise; plus a provenance rule in both skills' safety-floor sections. The split is stated rather than blurred: the value checking is a **control** (deterministic, a model cannot be argued out of it), the instruction to run it and to hold the data/instruction line is **prose, and therefore a mitigation**.
- **Safety floor: review reports were copied to disk verbatim, secrets included.** `history record` did `write_text(read_text())` with no redaction, and `install-project` added no `.gitignore` entry — so a security lens quoting a `service_role` key (the report format *requires* concrete evidence) wrote it into `.akos/reviews/` in the consuming project, where it could be committed. No attacker required; normal operation did it. Now redacted at write time, reusing the detector's own patterns rather than a second copy that would drift, and `install-project` appends `.akos/reviews/` to the project's `.gitignore`. The redactor keeps the finding — file, line, and prose survive; only the credential value is replaced — and preserves `anon`/`authenticated` JWTs, which are public by design and are evidence a reviewer needs. It prints what it removed, since a silent redaction is the same class of defect as none.


### Corrected — claims this project made about itself that were not true

Found by pointing the new `ai-engineering/` packs at AKOS itself, as the first real use of them. Each was established by running a command, not by re-reading the prose.

- **CI was red for the entire 1.4.0 release, and the 1.4.0 entry below announces it as delivered.** `gh run list` shows three consecutive failures on the `akos rules registry sanity` step: run `29733824899` on the 1.4.0 PR at 10:05:44Z, run `29733878337` on the `main` push at 10:06:35Z, and run `29739121045` at 11:36:02Z — 2h15m red across two merges. The 1.4.0 PR was merged with its own check failing, because the merge was gated on `mergeable`, never on `gh pr checks`.
- **The fix commit `d1a55c0` misdiagnosed the incident it fixed.** It states the workflows "had never actually run on GitHub" and that "the first real run failed in 12s". Both are false: they had run three times, and the 12s run was the third. The repair itself was verified by execution; the causal story around it was asserted from inference. A single `gh run list` would have settled it before the sentence was written. The real lesson is not "an unrun workflow slipped through" but "a visible red check was merged past" — which calls for branch protection, a control this repo still lacks.
- **`benchmarks/README.md` claimed every case was sabotage-verified.** One was (`supabase-rls-basic`, recorded in `b9e0b93`); the claim was generalized to all 21. A whole-engine sabotage pass has since confirmed the 19 deterministic cases genuinely go red — so they are live — but also found that **the 2 Level C cases cannot fail at all**: their `must_mention` phrases sit in their own `prompt`, the mock provider echoes the prompt, and the assertion checks that echo. Both pass with the fixture removed entirely. The defect was introduced by the M8 "fix" that made canned responses repeat their trigger phrases verbatim — closing the loop it was meant to open.
- `tests/README.md` said 79 tests; 82 run. `CHANGELOG` said the YAML parser is ~350 lines; it is 303, and was 303 at every commit.

None of these were caught by `doctor.sh`, the 82 unit tests, the 21 benchmark cases, or CI. Every one of them is a claim in prose that no check reads.

## [1.5.0] — 2026-07-20

Opens a new top-level family. Until now AKOS packaged senior judgment about *software* — but when an agent builds the software, the result also depends on what it was given to see, which tools it could call, what it was allowed to do, and whether anything was actually verified. None of that had a home.

### Added

- **New `ai-engineering/` domain — 6 packs, 7649 lines.** Fase 1 of an AI-native expansion, scoped deliberately: six packs that change how AKOS works with coding agents, rather than fifty that restate the same articles.
  - `ai-engineering/context-engineering` (L2) — context as a finite resource, not a container: CE1–CE16, CEE1–CEE58, covering minimum sufficient context, progressive disclosure, just-in-time retrieval, poisoning and rot, instruction hierarchy, memory tiers, what must survive a compaction boundary, and why "load the whole repo" fails small as well as large. Self-referential: `skills/akos/SKILL.md`'s own routing table is critiqued as a worked example.
  - `ai-engineering/agent-foundations` (L2) — which shape a task warrants and how to bound it: AF1–AF18, AFE1–AFE72 across shape selection, routing, parallelization, orchestrator–worker, evaluator–optimizer, termination, budgets, error recovery, escalation, and idempotency. Spine: the agent is the *last* shape to reach for. Three anti-patterns are graded as correctness defects — silent truncation, double-charged retry, and action taken outside stated authority.
  - `ai-engineering/tool-design` (L2) — a tool built for a human is not automatically a good tool for an agent: TD1–TD16, TDE1–TDE86 on naming, structured input and output, actionable errors, idempotency, dry-run and destructive confirmation, result bounds, stable references, and MCP's tool/resource/prompt distinction.
  - `ai-engineering/coding-agents` (L2) — the process discipline of the edit itself: CA1–CA18, CAE1–CAE80 on orientation before editing, search before changing an interface, minimal patches that match existing conventions, testing before and after, and atomic reviewable commits. Spine: plausible is not correct.
  - `ai-engineering/agent-evals` (L2) — proving a change actually helped: AE1–AE18, AEE1–AEE76 on golden datasets, the four eval altitudes, the grader ladder, groundedness, cost and recovery as first-class dimensions, regression thresholds, flakiness, contamination, and baseline discipline.
  - `ai-engineering/agent-security` (**L1**) — the surface that appears when a model reads external content and then acts: AS1–AS18, ASE1–ASE95, 19 named anti-patterns. Spine: retrieved text, documents, web content and tool output are untrusted data, never instructions. Level 1 places it in the safety floor the constitution never waives, so its floor rules hold even in Prototype. Original models include the provenance ladder, the exfiltration triangle, and a control-vs-mitigation test that caps a score at 49 when prompt hardening is the whole defense.
- Five new cross-cutting nodes in `graphs/knowledge-graph.md` — untrusted content as data, executed evidence over plausible output, blast radius and least privilege, bounded work, plus `agent-security` joining the security floor and `agent-foundations` joining complexity-as-a-cost. Every link verified to resolve.

### Changed

- `core/authority-model.md` names two source kinds it previously left ambiguous: Anthropic/OpenAI engineering practice as published sits at **L2** (the same footing as the existing Google/Stripe entry), and replicated agent methodology papers such as ReAct and Reflexion at **L3**, once cross-verified per the source policy. Additive — no renumbering, no schema change, and no existing pack's cited level changes.

### Fixed

- **The schema validator declared a bound it never enforced.** `knowledge-pack.schema.json` has specified `minimum: 0, maximum: 4` on `authority-level` since the contract shipped, but `schemas/validate.py` implemented neither keyword — they were the schema's only use of them. Any pack could ship `authority-level: 9` and validate clean at exit 0. Reproduced first, then fixed, with three regression tests locking both directions and both boundaries; `bool` is excluded from the numeric check since it subclasses `int`. Unit suite 79 → 82.
- The bug was found while authoring `coding-agents`, by deliberately trying to make the validator fail rather than trusting its green — the discipline that pack exists to teach, so it is now also its own worked example.

### Validated — the six packs run against AKOS itself

The packs had never been used for anything. Six reviews were run, one per pack, against the AKOS surface each one governs — AKOS is an agent system (skills, 13 subagents, a routing table, a CLI, project-local memory), so it is a legitimate target for its own knowledge. Every finding below was re-verified here by execution before being acted on.

**What the packs found.** Fixed in this release: `history record` applied partially on malformed JSON, leaving an orphan review that `history list` cannot see; `history clean` deleted with no preview and no confirmation, `--keep` defaulting to 20; and a mistyped `--pack`/`--rule`/`--case` filter reported a clean run and exited 0 in three separate tools, so `freshness --pack no/such --fail-on expired` was a CI gate that could never fire. Also fixed: the two Level C benchmark cases could not fail.

**Everything the reviews found is now fixed** — the two safety-floor CRITICALs and the three HIGH wiring defects (see Fixed below). What remains open is not a defect list but a coverage limit, stated below.

**What the packs got wrong about themselves.** Two worked examples under-applied their own rules — see `tool-design` 1.1.0 and `coding-agents` 1.1.0. Three of the six reviews independently reported that their scoring rubric is miscalibrated for its target: applied mechanically, `agent-foundations` yields 2/100 on a system where ~45 of its 72 rules have no referent, and `context-engineering`'s uncapped per-drift deduction pushes a documentation-heavy repo two bands below what the evidence supports. Each reviewer declined to report the mechanical number and said why. One flagged a genuine methodological problem: `context-engineering`'s own `examples.md` already contained a critique of `skills/akos/SKILL.md`, the file at the centre of its review, making that portion circular by construction.

**Coverage, stated plainly.** All six reviews are static reads of instruction artifacts. No AKOS review has ever been run and recorded in an inspectable form, so every pack's CRITICAL tier — the transcript checks — went unexercised. "No CRITICALs found" in those tiers means "not testable with what was available", not "clean".


### Deferred, not dropped

Fase 2 (`memory-and-retrieval`, `governance-and-risk`, `human-agent-interaction`, `long-running-agents`) and Fase 3 (data-intensive systems, continuous delivery, evolutionary architecture, Shape Up) are scoped but unwritten. No reviewer lens or scoring file was added for `ai-engineering/` — these are build-mode packs routed through `skills/akos/SKILL.md`, exactly as `frontend/`, `backend/` and `devops/` are today. A dedicated review lens is a larger change this repo has not attempted, and it waits for a real review need rather than being invented ahead of one.

## [1.4.0] — 2026-07-20

Quality infrastructure: AKOS gains a verification layer around its
knowledge — schemas, executable rules, benchmarks, evidence-aware
scoring, freshness tracking, review history, personal-profile
decoupling, CI, and tests. No pack content, no agent prose, no reasoning
profile, and no review-pipeline decision logic changed — everything here
is additive, verified against the pre-existing corpus at every step.
Full detail in `docs/architecture/target-system.md` (design decisions
and alternatives considered) and `docs/migration/v1.1-to-next.md`
(what a consuming project needs to know — nothing breaks).

### Added

- **Contracts** — `schemas/{knowledge-pack,agent,workflow}.schema.json`,
  a 303-line stdlib-only YAML parser (`schemas/yaml_subset.py`, no
  PyYAML/ruamel), and `bin/migrate-pack-metadata.py` (idempotent,
  append-only, already run against all 48 pre-existing packs).
- **`akos validate [packs|agents|workflows]`** — schema validation,
  `0`/`1`/`2` exit codes, `--format json`. Wired into `doctor.sh`'s new
  advisory Schema validation section.
- **`akos profile list|show|create|use`** — decouples the Level-0
  personal layer from a single hardcoded name (`pau-avila` stays the
  default; `.akos/config.md` gained a `personal_profile` field).
  `packs/personal/_template/` scaffolds new profiles.
- **Executable rules** (`rules/`) — 8 detectors (`SUPABASE_RLS_DISABLED`,
  `SUPABASE_POLICY_TOO_PERMISSIVE`, `SECRET_IN_SOURCE`,
  `SERVICE_ROLE_IN_CLIENT`, `A11Y_INPUT_NO_LABEL`,
  `MIGRATION_NO_DOWN_FILE`, `DESTRUCTIVE_MIGRATION_NO_GUARD`,
  `PACK_EXPIRED`), filesystem-discovered like `packs/` itself.
  `akos rules list|run|explain`.
- **Evidence-aware scoring** — the Review Summary template gained a
  `## Coverage` section and per-finding `(Confidence: ...)` tags.
  Additive only: no band, anchor, cap, or decision rule changed.
- **`akos freshness`** — full band report (fresh/review-due-soon/
  review-due/expired/unknown) over pack `review_after` dates.
- **Benchmarks** (`benchmarks/`) — 21 reproducible cases, a
  provider-agnostic Level-C interface (mock provider required and the
  only one CI uses; an optional local `claude`/`codex` CLI passthrough
  is documented, not wired by default). `akos benchmark run|list`.
- **`akos history record|list|show|latest|compare|clean`** — project-
  local (`.akos/reviews/`) review history; `akos-review`'s skill
  instructions record every review's decision and scores automatically.
- **CI** (`.github/workflows/`) — PR checks, main-branch benchmark +
  artifact upload, weekly freshness check.
- **Tests** (`tests/`) — 79 unit tests (stdlib `unittest`, no pytest) +
  4 integration scripts (bash, `mktemp -d`).
- **Docs** — `docs/architecture/`, `docs/contracts/`, `docs/rules/`,
  `docs/benchmarks/`, `docs/scoring/`, `docs/profiles/`,
  `docs/reviews/`, `docs/maintenance/`, `docs/cli/`, `docs/migration/`.

### Fixed

- **`write_marked_section`** (the helper `install-project` depends on
  for every rerun) silently failed on this machine's BSD awk whenever it
  needed to *replace* an already-marked section — `awk -v` cannot accept
  a multi-line value, exits nonzero with no output, and `set -e` aborted
  before the file was ever rewritten. A prior "rerun idempotency" check
  had passed by coincidence (the target content hadn't changed between
  runs, so a silently-failed no-op looked identical to a successful one).
  Replaced with a portable sed-line-range splice.
- The 16-vs-17-file pack contract inconsistency finally fully closed
  (VERSION/CHANGELOG references were the last stragglers).

Five more real bugs were found and fixed by testing each new component
against a real or synthetic case before trusting it — not hypothetical,
all reproduced and fixed in this range: a suppression-comment window too
narrow (checked only the exact evidence line), a fixture-path exclusion
matching "test" as a substring instead of a path segment, an anon-role
JWT wrongly flagged as a secret, a `freshness --fail-on` severity
comparison inverted, and a benchmark harness resolving fixture paths
against the wrong base directory. Each is documented in its own commit
and cross-referenced in the relevant `docs/` page — the point isn't that
bugs happened, it's that testing before trusting caught every one of
them before they shipped.

## [1.3.0] — 2026-07-19

Closes the second of the two lenses that had no domain of their own, and validates the first against a real production screen.

### Added

- **New `mobile/` domain — 2 packs, 2618 lines.** `mobile-reviewer` was running on borrowed platform-design and usability packs while Article 9 makes responsive review mandatory for every web surface.
  - `mobile/responsive-web` (L2) — layout and adaptation: breakpoint strategy from content, fluid type, container queries, the 320px floor and WCAG reflow, and a five-rung **reflow→restructure ladder** whose rule is that "we made it scroll" is not a rung. Two distinguishing principles: anything the user must read *while acting* must be visible while they act, and precedent transfers only with its conditions (read-only → editable voids the exemption).
  - `mobile/touch-ergonomics` (L2) — the hand and the device: a computable non-overlap rule `gap ≥ F − (wA + wB)/2`, thumb zones, hover-free design, the virtual keyboard, and locale input parsing. Silent coercion of a locale decimal into `0` is scored as a correctness defect, not an ergonomics nit. Its **enforcement-surface** model ranks where a rule lives — primitive, build check, runtime backstop, review, doc — and caps a documented-but-bypassable rule at 79.
- **`scoring/mobile-score.md`** — pipeline step 4 had no score file, unlike every other scored lens. Now it has one, with caps for untested viewports and unenforceable rules.
- `agents/mobile-reviewer.md` loads both packs as primary and scores against the new file.

### Changed

- `agents/copy-reviewer.md`: `content/gov-uk-content-design` is now **conditional, not a default load**. Validated on a real control-dense editor where it fired on one finding out of nineteen while `ux-writing` produced the rest — loading it there costs context and returns almost nothing.

### Validated

The `content/` packs were re-run against the same production screen reviewed before they existed: **69 / PASS WITH FIXES → 52 / BLOCKED**. The packs found defects judgment alone had missed — six confirmations fired before their mutation settles, two of which fire when the handler provably did nothing, one of them navigating to a URL built from `undefined`. The prior review had seen only the visible symptom, "a double toast". The difference was not insight but insistence: the rubric prices a confirmation that can fire on a failed operation as a correctness defect and refuses the trade a human reviewer would have negotiated.

## [1.2.0] — 2026-07-19

### Added

- **New `content/` domain — 2 packs, 2073 lines.** `copy-reviewer` was one of the twelve pipeline lenses running entirely on borrowed UX packs, with no domain of its own. It now has one.
  - `content/ux-writing` (L3) — interface words: labels, error anatomy, empty states, voice and tone, confirmation copy, writing for translation. Its spine is that a label is a promise the code must keep, so the truthfulness pass reads the handler rather than the string. Anti-patterns are a named taxonomy: the lying label, phantom confirmation, capability cosplay, synonym drift, tooltip-only meaning, the dead-end empty state.
  - `content/gov-uk-content-design` (L2) — content design as meeting a user need: plain language, front-loading, readability targets, scanning, and retiring stale content. Numeric targets are checkable rules rather than advice.
  - Both grounded in real production-audit findings so they catch defects instead of reading as editorial taste. Scope boundary is explicit in each README, and they cross-link rather than overlap.
- `agents/copy-reviewer.md` loads them as primary, ahead of the borrowed UX packs.
- Both listed in the `akos` routing table with their "reach for it when" clause.

### Changed

- Routing hints, subagents, config-reading and the technical-pack fragments shipped since 1.1.0 were never versioned. This release carries them.

## [1.1.0] — 2026-07-19

AKOS is now directly invocable as a skill in Claude Code and Codex CLI, instead of relying on an instruction block telling the agent to go read files.

### Added

- `skills/akos` — build mode. Bootstraps the constitution, sets the reasoning profile from `.akos/config.md`, loads the Level-0 personal layer, and routes to the 2-5 relevant packs via an inline domain→pack table.
- `skills/akos-review` — review mode. Resolves a targeted or full run of the twelve-lens pipeline and emits the unified Review Summary.
- Both skills use the open agent-skills format read by **both** Claude Code and Codex CLI — one set of files, two tools.
- Plugin manifests for both ecosystems: `.claude-plugin/{plugin,marketplace}.json` and `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`. AKOS is installable with `/plugin marketplace add ipaud/AKOS` or `codex plugin marketplace add ipaud/AKOS`.
- `akos list-skills`.
- `doctor.sh` skill checks: frontmatter validity, name/directory agreement, JSON manifest parsing, manifest-version/VERSION agreement, symlink presence, and — the anti-drift guard — that **every pack appears in the `akos` routing table**.

### Changed

- `install.sh` links both skills into `~/.claude/skills/` and `~/.agents/skills/` as symlinks, so pack edits are live in both tools with no reinstall. `uninstall.sh` removes only links that point back into this repo.
- `akos install-project` now writes a four-line block into `CLAUDE.md` and `AGENTS.md` instead of a twenty-line bootstrap — the skills carry the bootstrap and load on demand. The Cursor rule keeps the long form (Cursor has no skills).
- `templates/{CLAUDE,AGENTS,codex-instructions}.md` document the skill-based integration. `templates/{cursor-rule.mdc,gemini-instructions.md,generic-agent-instructions.md}` keep the long-form bootstrap for tools without skill support.
- `prompts/load-akos.md` is now labelled as the manual fallback for those tools.

### Fixed

- The pack contract is documented as **17 files** everywhere. It was described as 16 in `README.md`, `core/knowledge-schema.md`, `core/source-policy.md`, `CONTRIBUTING.md`, `prompts/create-new-pack.md`, `doctor.sh`, and `bin/akos`, while the schema table, `doctor.sh`'s own checks, `create-pack`'s output, and all 44 packs on disk were always 17.

## [1.0.0] — 2026-07-09

### Added

- Core reasoning layer: constitution, authority model, conflict resolution, reasoning profiles, review pipeline, decision framework, confidence model, knowledge schema, scoring model, reasoning engine, source policy.
- 44 knowledge packs across ux, architecture, product, security, performance, frontend, backend, testing, devops.
- Deep Tier-1 UX packs: steve-krug, don-norman, nielsen-norman-group, laws-of-ux, wcag.
- Personal layer: packs/personal/pau-avila.
- 13 review agents with unified output format and severity levels.
- 9 workflows mapping the review pipeline to concrete tasks.
- 7 scoring rubrics (0–100, banded).
- 5 knowledge graphs cross-linking packs by concept.
- Templates for Claude Code, Codex, Cursor, Gemini, and generic agents.
- Prompts for loading AKOS and running reviews.
- Installer, doctor, updater, uninstaller, and `akos` CLI with marker-based project integration.
