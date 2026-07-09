# Scoring Rubric — Krug Pack (UX Clarity)

Feeds the UX dimension in [scoring/ux-score.md](../../../scoring/ux-score.md). Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

## Deductions

| Finding | Deduction |
|---------|-----------|
| Primary task requires figuring out (no-think failure on main flow) | −25 (CRITICAL) |
| Dead-end error state / input destroyed on validation failure | −25 (CRITICAL) |
| Unguarded destructive action | −25 (CRITICAL) |
| Five-second test failure on a key screen | −10 each (HIGH) |
| Trunk-test failure (interior page, no orientation) | −10 (HIGH) |
| Missing async state (empty/loading/error/success) per surface | −10 (HIGH) |
| Hover-only or ambiguous clickability on a primary path | −10 (HIGH) |
| Mobile breakage (320px overflow, unreachable primary action) | −10 (HIGH) |
| Vague primary button label ("Submit"/"OK" on meaningful action) | −4 (MEDIUM) |
| Happy talk / instruction blocks on task screens | −4 (MEDIUM) |
| Placeholder-only labels, format-picky inputs | −4 each (MEDIUM) |
| Squint-test hierarchy failure on a screen | −4 (MEDIUM) |
| "Click here" links, clever nav labels | −1 each, cap −5 (LOW) |
| Missing breadcrumbs at depth, narrow-measure violations | −1 each, cap −5 (LOW) |

## Modifiers

- Recent think-aloud test round with fixes applied: +5 (cap 100).
- No usability test ever, Production profile: score capped at 79.
- Repeat finding from previous review, unfixed without recorded tradeoff: double its deduction.

## Interpretation anchors

- **95** — tested, obvious, conventional; findings are polish.
- **85** — solid; a handful of MEDIUMs (labels, copy) to schedule.
- **72** — usable but users visibly hesitate; ship only pre-PMF with fixes queued.
- **55** — first-time users fail tasks; BLOCKED.
