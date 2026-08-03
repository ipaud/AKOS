# AKOS Roadmap

Living document, not a promise with dates. Reordered whenever priorities change.
Source of truth for *why* an item exists: `.akos/audit-2026-07-23.md` (full
integral audit) and `CHANGELOG.md` (what already shipped). This file only
tracks what's still open.

Last reviewed: 2026-08-01.

## Now

Nothing queued — see Next.

## Next

- **Propagate the `INCOMPLETE` decision state.** Added to
  `skills/akos-review/SKILL.md` only (v1.17.4); 13 other files enumerate
  PASS/PASS WITH FIXES/BLOCKED without it — `core/review-pipeline.md` (the file
  `core/constitution.md` names as canonical), `core/constitution.md`,
  `core/scoring-model.md`, `agents/ux-reviewer.md`, `scoring/overall-score.md`,
  `docs/scoring/evidence-confidence-coverage.md`, `workflows/new-feature.md`,
  `workflows/ui-screen-review.md`, `docs/architecture/current-system.md`,
  `docs/migration/v1.1-to-next.md`, three `templates/*.md` files.
- **Route confirmed detector gaps back to the rule.** The 2026-07-31 run's
  deterministic pass flagged 5 `A11Y_INPUT_NO_LABEL` inputs — all 5 confirmed
  by the accessibility lens — but the lens also found 2 unlabeled `<select>`
  elements the detector's `<input>`-only pattern cannot catch, which are
  strictly worse (no placeholder fallback, no accessible name in any
  modality). Nothing in the pipeline routes a lens's confirmed false-negative
  back into a rule-improvement item; it currently just gets absorbed into that
  one report and lost.
- **Add a "scope the target" step before lens dispatch.** Nothing instructs the
  orchestrator to look at the project before choosing lenses. In the first dry
  run the file inventory, line counts and CI read were the participant's own
  initiative.

**The routing table is full.** 60 packs, against a stated operating ceiling of
roughly 60 rows — past that, selection precision degrades faster than coverage
improves. The 2026-07-27 routing trial found no degradation *at 58*, which is
evidence for the current size and not for a larger one. A new pack now needs to
displace an existing one, and the case for it has to include which row it
replaces.

## Later

Real, but needs a decision before it's actionable — not just an implementation
task.

- **Reconcile Article 2's "keyboard reachability" with
  `accessibility-reviewer.md`'s "invisible focus" CRITICAL example.** Surfaced
  2026-08-01: the constitution's floor item is unreachability; the agent
  file's literal example is a narrower thing (focus present but not visible).
  A merger currently has to judge whether they mean the same thing — the
  2026-08-01 run did, correctly, and flagged it as overrulable, but that's a
  workaround, not a fix. Needs a decision: tighten Article 2's wording, narrow
  the agent file's example, or state explicitly in `core/constitution.md`
  that "basics" is intentionally broader than its four named examples.
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

- **The profile-inference contradiction is resolved — canonical ruling R14
  (2026-08-01, phase 1 of 4).** `core/reasoning-profiles.md` defaults unknown
  profiles to Startup MVP; `packs/personal/pau-avila/project-patterns.md`
  maps never-deployed projects to Prototype — both Level 0, so a literal
  authority reading could pick either. Resolution turned out not to need the
  full 7-step algorithm: `project-patterns.md`'s trigger is "never-deployed,"
  a claim about *intent* that the plain `Deployed: yes/no` field (and its
  v1.17.9 default of `no`) can't carry — not-currently-deployed isn't the
  same statement as never-will-be, so the trigger's condition isn't actually
  met by config silence. Backed by a second, independently sufficient reason:
  `scoring/overall-score.md`'s weight table has Startup MVP ≥ Prototype on
  every single scored dimension (verified, not assumed), so defaulting to it
  is the direction that never under-scrutinizes when genuinely unsure.
  Recorded as R14 in `core/conflict-resolution.md`. Also surfaced and fixed a
  smaller, adjacent gap while reading the source: `reasoning-profiles.md`
  itself already says "ask once, then default Startup MVP" when the profile
  is unset — `SKILL.md`'s bootstrap bullet silently defaulted without ever
  mentioning the ask, so the two files disagreed on procedure even before
  getting to this conflict. Now surfaced in `SKILL.md` §1.

- **§1 gained a configless default block (2026-08-01).** `Deployed`,
  `Primary surface`, and `Style direction` had no stated fallback when
  `.akos/config.md` is absent — which is every new user's first run, not an
  edge case, and the 2026-07-31 re-run confirmed the orchestrator had to
  improvise all three. Reading the actual agent files first changed the fix:
  `agents/frontend-reviewer.md` never literally depends on `Style direction`
  — it already has its own anti-template checklist and always-loaded
  `design-language.md` fallback — so "literally unexecutable" overstated the
  gap; the real defect was `SKILL.md` promising a behavior with no fallback
  wired to it. Defaults now stated: `Deployed` → no (report-only, never
  softens the floor below profile weight; code evidence overrides a missing
  declaration); `Primary surface` → web (mobile is already default-on per
  `agents/mobile-reviewer.md` and personal principle 7 — a missing config
  isn't the opt-out, an explicitly non-web target is); `Style direction` →
  fall back to the design-language checklist plus the screen's own internal
  consistency, and report the absence itself as a finding rather than
  reviewing as if a direction had been checked. All three defaults matched
  what real trial runs already improvised correctly — this made it written
  policy instead of per-run reinvention.

- **Fourth run confirmed v1.17.7's three fixes hold uncoached, and surfaced a
  real infrastructure lesson for free (2026-08-01).** Same held-out DKG trial,
  this time with an explicit rule against coaching any lens's dispatch prompt
  with hints about the merge rules (run 3's own honesty note had flagged that
  its copy-lens dispatch wasn't clean evidence). All three v1.17.7 clauses
  exercised correctly: subset-dedup applied cleanly to the textbook case and
  had to be generalized once more for a shape the wording didn't cover (two
  already-multi-instance findings partially overlapping, not one single
  instance inside another's broader pattern — fixed, one more sentence);
  score non-recomputation held exactly as written (UX score left untouched,
  the resulting mismatch stated in Tradeoffs rather than silently fixed);
  every CRITICAL got the floor-check explicitly, including the two nobody
  disputed — the specific gap v1.17.7 closed. Unplanned bonus finding: two of
  the five lens subagents failed mid-stream on genuine transport errors
  (connection closed, 600s stall) — infrastructure, not a pipeline defect.
  The orchestrator's first instinct, resuming both from their saved
  transcripts, **failed identically both times**; redispatching fresh instead
  of resuming succeeded immediately. That's now written into step 2: retry a
  transport failure once via resume, but redispatch fresh rather than
  re-attempting a resume that already failed.
  One open, deliberately unresolved question the run surfaced: `core/
  constitution.md` Article 2 enumerates "keyboard reachability" as a floor
  item; `agents/accessibility-reviewer.md` treats invisible focus (narrower
  than unreachability) as its own literal CRITICAL example. The two files
  don't use the same words for what's obviously the same intent, and step 6
  doesn't say which wins when they diverge. The run's own merger handled it
  correctly — made the call, flagged it as overrulable in Tradeoffs, didn't
  bury it — which is what a judgment-call clause is supposed to produce. Not
  fixed here: it's a wording-precision question between two source files, not
  a merge-algorithm defect, and forcing a resolution under this task would be
  answering a different question than the one asked.

- **The merge algorithm was re-tested against a live run, and mostly held
  (2026-07-31, same day it was written).** Third run of the same held-out-repo
  trial: dispatched five lenses on DKG, all five reported, and the merger
  followed step 6 as written rather than inventing rules from scratch. Real
  signal, not a rubber stamp — the dedup rule correctly caught 6 genuine
  cross-lens overlaps *and* correctly rejected a near-miss (same file,
  different failure mode); the ownership rule resolved the exact
  `frontend-reviewer`-scores-UX case named in its own text; the floor-check
  capped two CRITICAL/HIGH disagreements by checking Article 2's list rather
  than by eyeballing severity. Three real gaps surfaced and were closed the
  same day: (1) no rule for a finding that's a *subset* of a broader
  multi-instance finding from another lens — now merges at the instance
  level, leaving the umbrella finding's other instances untouched; (2) capping
  a CRITICAL to HIGH left the owning lens's own dimension score
  un-recomputed, with nothing telling the merger whether to fix that — now
  explicit that the merger never recomputes another lens's rubric arithmetic,
  and states the resulting mismatch rather than silently resolving it; (3) the
  floor-check read as conditional on active disagreement, so an uncontested
  CRITICAL from a single lens seemed to skip it — now explicit that every
  CRITICAL gets the same check regardless of coverage, and non-CRITICAL
  disagreements (MEDIUM vs. HIGH) are just Rule 1's plain "keep the higher
  severity," no floor-check involved. One honest caveat from the run itself:
  the copy-lens's compliant behavior (returning no standalone score) isn't
  clean evidence the rule works unprompted — the tester's own dispatch prompt
  cited the rule to it first.

- **The merge algorithm is written down (2026-07-31).** `skills/akos-review/
  SKILL.md` spent one sentence on the hardest step in the pipeline —
  "merge every returned summary into **one** Review Summary" — and the
  2026-07-31 re-run had to invent, unguided, exactly the three decisions a
  merge needs: a dedup rule (4 of 5 lens pairs found overlapping defects that
  run), which lens owns a score dimension when two fill it
  (`frontend-reviewer` returned its own UX number alongside `ux-reviewer`'s),
  and how to resolve a severity disagreement between lenses on the identical
  defect (mobile said CRITICAL, accessibility said HIGH, same code — resolved
  by `core/constitution.md` Article 2's *enumerated* floor: only security,
  accessibility basics, and data integrity are CRITICAL in every profile, so
  a reflow failure caps at HIGH regardless of which lens raised it). New
  step 6 in `SKILL.md` states all three as rules instead of leaving each
  merger to reinvent them, plus the copy-folds-into-UX and
  non-canonical-decision-string rules that were previously stuffed into the
  Scores block description rather than the merge step where they belong.
  Untested since writing — the same caution applies as to the v1.17.4/v1.17.5
  pipeline fixes: written guidance and exercised guidance are different
  claims, and only a re-run confirms the second one.

- **Onboarding dry run before the activation study, and it was worth doing
  (2026-07-31).** The five-participant study is a one-shot resource: if the
  install path is broken you learn it from participant 1 and the study is
  spent. Two agents ran first — one auditing the install path as a first-time
  user, one running a real five-lens frontend review on a held-out repo with
  only `skills/akos-review/SKILL.md` as its entry point. Both found blockers,
  and the review trial found something worse than friction.

  **The trial did not finish.** It dispatched five lens subagents, burned ~123k
  tokens, and never reached the merge step. The lenses themselves were
  excellent — four eventually returned reviews that found a real accessibility
  CRITICAL and two UX CRITICALs in the target — but their output never reached
  the orchestrator, and the run's own report was assembled from shell commands
  alone. **AKOS had no way to say the review did not happen.** §6's decision
  semantics are purely severity-driven, so a run where every lens silently
  failed emits the same string as a run where every lens passed. Fixed by
  adding an `INCOMPLETE` state that outranks the severity rules, written
  alongside the reason coverage still must not *soften* findings — the two
  rules pull in opposite directions and both are deliberate.

  Also fixed, all in the same class of defect — reporting success that was
  never verified:
  - **`akos rules run` exit `0` was documented as "no findings".** It means *no
    CRITICAL*. Confirmed by running it: exit 0 with five MEDIUM findings. An
    agent following the documentation checks `$?`, sees 0, and reports clean.
  - **`akos list-skills` printed "Linked into: …" unconditionally**, never
    stating either destination — byte-identical output whether the symlinks
    existed or not, while being the README's documented verification step. Now
    reports per skill and per tool.
  - **`doctor.sh` tested symlink existence, not identity.** Verified by
    cloning a throwaway checkout that had installed nothing and watching it
    print `✓ 69 ! 0 ✗ 0`. Now compares resolved targets via a shared
    `akos_link_status` helper, warning (not failing) on a foreign checkout,
    since several checkouts on one machine is legitimate. The helper resolves
    physically because `~/DEV` is commonly a symlink to somewhere else, so the
    final path component alone is not comparable.
  - **Eight detectors, seven documented.** `PACK_EXPIRED` (domain `meta`) was
    absent from both the prose and the routing table. It is a finding about
    AKOS's own freshness, not the project under review, and now says so.
  - **The plugin path told the skills to run a CLI it does not ship.** Both
    skills opened by mandating `akos check-config` and treating a non-zero exit
    as "do not proceed" — so a plugin user hit `command not found` on the
    second instruction they read. Both now carry a by-hand fallback that keeps
    the check's substance: absence of the CLI is not permission to skip it,
    because that check is what stops a hostile `.akos/config.md` from lowering
    the profile and silently skipping lenses.
  - **README:** SSH clone URL on a now-public repo (an evaluator without SSH
    keys cannot clone at all, and HTTPS works anonymously), macOS's Python 3.9
    floor with no stated remedy and the existing `AKOS_PYTHON_BIN` escape hatch
    documented nowhere, no "restart your agent session" step (skills are
    enumerated at session start, so an already-open session improvises a
    generic review — which the study would have recorded as a success), the 13
    subagents written into `~/.claude/agents/` undisclosed, `uninstall.sh`
    unmentioned, and PATH persistence assuming zsh.
  - **`LICENSE` was MIT plus an appended note**, which is why GitHub reported
    the repo's license as "Other" rather than "MIT". The note moved to
    `NOTICE.md`; the grant is unchanged.

  Estimated time-to-first-review before these fixes: 15–35 minutes for a
  realistic newcomer against a stated 10-minute median target, with two
  documentation defects each able to consume the whole budget alone.

- **CI is green on `main` — the six-release validation backlog is closed
  (2026-07-31).** The repo was made public, which lifted the Actions billing
  block (public repos get unlimited minutes on standard runners). Re-running
  the v1.17.3 `main` run passed all three jobs: Quality gates + coverage,
  Functional (Ubuntu / Python 3.10 floor), and Functional (macOS / current
  Python). The one genuinely open question — whether the `awk` added to
  `doctor.sh` in v1.13.0 behaves the same under GNU awk — is answered: it
  does. Everything merged between v1.13.0 and v1.17.3 on local evidence alone
  is now CI-validated.

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
