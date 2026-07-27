# Changelog — experimentation

## [1.0.0] — 2026-07-27

### Added

- First complete version. Authority level 3 (a book), review cadence 270 days
  (`review_after: 2027-04-23`). Cleared the source intake gate on a verified gap:
  `Kohavi`, `statistical significance`, `statistical power`, `p-value`, `OEC`,
  `novelty effect`, `sample ratio`, `peeking`, `multiple comparison`,
  `minimum detectable` and `confidence interval` all returned zero across the 59-pack
  corpus. `A/B` returned five hits, every one in passing —
  `product/lean-startup` supplies the hypothesis loop and none of the statistics, which is
  precisely the gap.
- Principles P1–P17 across whether to run one at all, what to measure, running honestly,
  reading honestly, and the people in it. Engineering rules EXP1–EXP45 across pre-launch
  planning, assignment and instrumentation, running, reading, deciding and shipping, what
  to do when you cannot experiment, and ethics.

### The pack opens by talking most readers out of it

Its first three principles and its decision framework's first section exist to prevent the
rest from being used. The required sample per arm for a conversion comparison is
approximately `16·p·(1−p)/δ²`; on a 3% baseline that is ~52,000 per arm to detect a 10%
relative lift, and ~207,000 to detect a 5% one. Halving the effect quadruples the
requirement.

**Under roughly 5,000 weekly users into the funnel, conversion is not experimentable, and
that is the finding.** Running an underpowered test is worse than running none: it converts
"we don't know" into a number people will quote. The pack therefore ships:

- a traffic table giving a verdict per scale, and a list of what to do instead —
  usability testing, interviews, staged rollout with instrumentation, or deciding on
  judgement and recording it;
- EXP38–EXP41, a rules section for the case where experimentation is unavailable, including
  that "we tested it" must never be claimed for an underpowered test;
- a scoring rubric that returns `n/a` rather than a low score for a surface without the
  traffic, and in which **not running experiments is never a deduction** — a team that did
  the arithmetic, concluded it could not experiment, and recorded the judgement has done
  this correctly;
- a review-checklist gate placed before the checklist proper, because reviewing the
  methodology of a test that should not exist legitimizes it;
- an anti-pattern, *experimentation theatre on a small product*, for the platform-and-
  process build-out that cannot produce a valid answer.

This is the Level 3 failure mode named directly: the source's context is large-scale
consumer products, and `core/authority-model.md` is explicit that methodologies encode the
setting they came from.

### Other choices

- **Only two rules are starred, and neither is methodology.** EXP42 (no arm withholds
  safety, accessibility, or security — the floor is not contingent on whether users are
  observed to want it) and EXP43 (experiment data is personal data). Both apply at any
  scale, including where the rest of the pack does not.
- **Diagnostics before outcomes** is stated as a sequencing rule rather than a checklist
  item, because once the result has been seen it cannot be unseen — a sample-ratio mismatch
  noticed afterwards is much harder to act on.
- **"Not significant" may never be reported as "no effect"** (EXP27). The pack requires the
  detectable threshold to be stated alongside, which is the single change that makes flat
  results honest.
- **A program reporting mostly wins is treated as a finding, not a success** (P11, and the
  *suspiciously successful program* anti-pattern), with an A/A test as the diagnostic.
- The arithmetic is labelled an approximation in `references.md`, with the note that
  anything needing a precise number should use a real power calculation rather than this
  pack.

### Scope boundary

Recorded against `packs/product/inspired` (deciding what to build),
`packs/product/lean-startup` (the hypothesis and learning loop this supplies statistics
for), `packs/product/continuous-discovery-habits` (the qualitative half an experiment
cannot supply — an experiment says what happened, never why),
`packs/devops/observability` (the instrumentation the numbers come from),
`packs/ai-engineering/agent-evals` (the same discipline for non-deterministic model
output), and `packs/security/privacy` (what the measurement data itself obliges you to).
