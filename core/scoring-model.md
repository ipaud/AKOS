# Scoring Model

Scores make review verdicts comparable across time, projects, and agents. All AKOS scores run 0–100 with fixed bands. Per-dimension rubrics live in `scoring/`; this file defines the shared mechanics.

## Bands

| Range | Label | Meaning |
|-------|-------|---------|
| 90–100 | Excellent | Ship with pride. Findings are polish only. |
| 80–89 | Good | Ship. Minor known gaps, none user-harming. |
| 70–79 | Acceptable | Shippable under MVP/Prototype; schedule fixes. |
| 60–69 | Risky | Ship only with explicit owner sign-off; expect user pain. |
| 0–59 | Blocked | Do not ship. Maps to BLOCKED verdict. |

## Scoring mechanics

1. **Start from the rubric, not vibes.** Each `scoring/*.md` rubric defines deductions per finding severity and per checklist area. Score = 100 − deductions, floored at 0.
2. **Severity anchors.** Default deductions unless a rubric overrides: CRITICAL −25 each, HIGH −10, MEDIUM −4, LOW −1. Two CRITICALs in one dimension ⇒ that dimension ≤ 50 ⇒ Blocked band.
3. **Score what you assessed.** Dimensions not reviewed get `n/a`, never a courtesy 80.
4. **Confidence gates severity** ([confidence-model.md](confidence-model.md)) — so it gates deductions too. Hunches don't move scores.
5. **Consistency beats generosity.** A 75 that means the same thing next month is worth more than a flattering 88.

## Overall score

Weighted average of assessed dimensions, weights set by the active [reasoning profile](reasoning-profiles.md). Default weights per profile are defined in [scoring/overall-score.md](../scoring/overall-score.md). Two hard rules override arithmetic:

- Any dimension in Blocked band caps Overall at 59.
- Security or Accessibility in Risky band caps Overall at 69.

## Relationship to verdicts

- All assessed dimensions ≥ 80 and no HIGH open → **PASS**
- HIGHs open but nothing Blocked, profile permits → **PASS WITH FIXES**
- Any Blocked-band dimension or open CRITICAL → **BLOCKED**

Scores inform the verdict; the verdict rules in [review-pipeline.md](review-pipeline.md) win if they disagree.

## Reporting

Scores appear in the unified report's `## Scores` block. Always include the band label: `Security: 72 (Acceptable)`. Trends matter more than absolutes — when re-reviewing, include the previous score in parentheses.

The report's `## Coverage` block (see [review-pipeline.md](review-pipeline.md)) states what was actually inspected, so a score is read alongside how much of the surface it's based on — this is additive reporting, not a change to the bands, anchors, or verdict linkage above.
