# Scoring Rubric — Refactoring UI Pack (Visual Craft)

Contributes to UX/frontend scores as the polish component. Note: WCAG failures found during visual review are scored in the [accessibility rubric](../wcag/scoring-rubric.md), not here.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| No hierarchy: squint test finds no dominant element on key screens | −10 per screen, cap −30 (HIGH) |
| Undesigned states (missing hover/focus/empty/loading as a pattern) | −10 (HIGH) |
| No spacing/type system (pixel-picked throughout) | −10 (HIGH) |
| Accent inflation / multiple primary buttons | −4 per screen, cap −12 (MEDIUM) |
| Border fever / gray soup / radius roulette | −4 each pattern (MEDIUM) |
| Label-over-data inversion, stretched forms, raw text-on-image | −4 each (MEDIUM) |
| Off-scale one-offs, icon family mixing, missing tabular figures | −1 each, cap −8 (LOW) |

## Modifiers

- Tokenized system (spacing, type, ramps, shadows, radii) in code: +5.
- Systematic fix applied at token level during review: counts once, not per screen.

## Anchors

- **92** — reads designed; system tokens everywhere; states polished.
- **80** — solid system with local lapses.
- **70** — functional but visibly amateur (no system); fine for Prototype, schedule for MVP.
- **<60** — visual noise actively harming usability (hierarchy absent on primary flows) — at that point it's a Krug/NN-g finding too.
