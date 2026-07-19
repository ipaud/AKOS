# Mobile Score (0–100)

Measures whether a web surface actually works on a phone, in a hand, on a real network. Mechanics per [core/scoring-model.md](../core/scoring-model.md); bands: 90–100 excellent, 80–89 good, 70–79 acceptable, 60–69 risky, <60 blocked.

Pipeline step 4 ([review-pipeline.md](../core/review-pipeline.md)), owned by [mobile-reviewer](../agents/mobile-reviewer.md). Article 9 makes this a default review for every web surface, not an opt-in.

## Inputs

Aggregates the pack rubrics for whatever surface is under review:

- [mobile/responsive-web](../packs/mobile/responsive-web/scoring-rubric.md) — layout, reflow, adaptation (primary)
- [mobile/touch-ergonomics](../packs/mobile/touch-ergonomics/scoring-rubric.md) — targets, input, gestures, keyboard (primary)
- [ux/wcag](../packs/ux/wcag/scoring-rubric.md) — SC 1.4.10 Reflow and 2.5.8 Target Size, where mobile meets the floor
- [ux/apple-hig](../packs/ux/apple-hig/scoring-rubric.md) / [ux/material-design](../packs/ux/material-design/scoring-rubric.md) — platform ergonomics when the target is native
- [performance/network-performance](../packs/performance/network-performance/scoring-rubric.md) — behaviour on a slow or intermittent connection

Score each that applies and average; deduplicate overlapping findings — one defect, one deduction, cited by the pack that explains it deepest.

## Severity anchors

CRITICAL −25, HIGH −10, MEDIUM −4, LOW −1. Confidence gates severity ([confidence-model](../core/confidence-model.md)); an unverified claim about a viewport you did not test is at most MEDIUM.

CRITICAL is reserved for a task a phone user cannot complete, or completes wrongly without knowing:

- The primary task is not completable at 320px.
- A value the user must read while acting is off-screen while they act on it.
- Input is silently coerced — a locale keypad producing a value the parser turns into `0`.
- A destructive control's hit area overlaps a neighbour's.
- Meaning exists only on hover, on a path the user must follow.

## Interpretation anchors

| Score | What it describes |
|---|---|
| 92 | Restructures rather than scrolls; targets and spacing computed, not eyeballed; input parsed per locale; tested at the stated widths. |
| 83 | Sound layout and targets; a documented rule that a component can still bypass; minor density issues off the primary path. |
| 72 | Works, but the phone case was adapted rather than designed — horizontal scroll on a path that should have restructured, or chrome crowding the content. |
| 58 | The primary task is technically reachable but the user is working blind, panning, or fighting the keyboard. |
| 35 | The surface was built for a desktop and made to fit. |

## Caps

- Any open CRITICAL: **≤59**.
- Never tested below 375px: **≤79**. A claim about 320px behaviour that was not observed is not a pass.
- A rule that lives only in documentation and can be bypassed by a component: **≤79** (see the enforcement-surface model in [touch-ergonomics](../packs/mobile/touch-ergonomics/mental-models.md)).

## Feeding the overall score

Mobile findings that are safety-floor violations (reflow, target size) also feed [accessibility-score](accessibility-score.md); findings about task completion also feed [ux-score](ux-score.md). Deduplicate across the three — a finding counts once in the overall weighting per [overall-score.md](overall-score.md).
