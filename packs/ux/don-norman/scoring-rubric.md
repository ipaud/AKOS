# Scoring Rubric — Norman Pack (Interaction Quality)

Feeds the UX dimension ([scoring/ux-score.md](../../../scoring/ux-score.md)) alongside the [Krug rubric](../steve-krug/scoring-rubric.md); when both apply, score each and average.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Invisible mode that changes behavior | −25 (CRITICAL) |
| Irreversible destruction without proportional forcing function | −25 (CRITICAL) |
| Silent destruction of unsaved work | −25 (CRITICAL) |
| Primary action without visible signifier | −10 (HIGH) |
| No feedback within 100ms / no progress >1s on a main flow | −10 (HIGH) |
| Key state (account/sync/unsaved) discoverable only by acting | −10 (HIGH) |
| No undo on reversible mutations in a main flow | −10 (HIGH) |
| Destructive adjacent/identical to frequent action | −10 (HIGH) |
| Validation where a constraint was feasible | −4 (MEDIUM) |
| Vocabulary drift (multi-name concept) | −4 (MEDIUM) |
| Implementation leakage in user-facing copy | −4 (MEDIUM) |
| Feedback miscalibration (modal trivia, toast storms) | −4 (MEDIUM) |
| Unlabeled similar controls, missing drag cues, effect-order mismatch | −1 each, cap −5 (LOW) |

## Modifiers

- Slip/mistake misdiagnosis in shipped remedies (confirmation patching a model failure): treat as HIGH even if the surface looks guarded.
- Documented conceptual model (one-sentence, tested): +3.

## Anchors

- **95** — coherent model, visible state, calibrated feedback, error-proofed.
- **80** — sound interactions; a few constraint/vocabulary gaps.
- **70** — works but silent: sparse feedback, recall-heavy, confirmation-wallpapered.
- **<60** — invisible modes or unguarded destruction; BLOCKED.
