# UX Score (0–100)

Measures usability clarity. Mechanics per [core/scoring-model.md](../core/scoring-model.md); bands: 90–100 excellent, 80–89 good, 70–79 acceptable, 60–69 risky, <60 blocked.

## Inputs

Aggregates the pack rubrics for whatever surface is under review:

- [steve-krug](../packs/ux/steve-krug/scoring-rubric.md) — usability clarity (primary)
- [nielsen-norman-group](../packs/ux/nielsen-norman-group/scoring-rubric.md) — ten-heuristic sum
- [laws-of-ux](../packs/ux/laws-of-ux/scoring-rubric.md) — cognitive cost
- [don-norman](../packs/ux/don-norman/scoring-rubric.md) — interaction quality
- [refactoring-ui](../packs/ux/refactoring-ui/scoring-rubric.md) — visual craft
- [universal-principles-of-design](../packs/ux/universal-principles-of-design/scoring-rubric.md)

When multiple apply, score each and average; deduplicate overlapping findings (one defect, one deduction, deepest-explaining pack cites it).

## Severity anchors

CRITICAL −25 (task not completable / dead-end error / unguarded destruction), HIGH −10, MEDIUM −4, LOW −1. Confidence gates severity ([confidence-model](../core/confidence-model.md)).

## Interpretation

- **95** — tested, obvious, conventional; findings are polish.
- **85** — solid; a handful of MEDIUMs to schedule.
- **72** — usable but users visibly hesitate; ship pre-PMF with fixes queued.
- **<60** — first-time users fail tasks; BLOCKED.

Production profile with no usability test ever: capped at 79.
