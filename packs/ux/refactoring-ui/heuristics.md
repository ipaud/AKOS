# Heuristics — Refactoring UI Pack

## Diagnosing "it looks off"

- Squint: if nothing dominates → hierarchy failure; if borders dominate → over-separation; if it vibrates → too many saturated colors.
- Count font sizes on screen: >4 → collapse to the scale.
- Count borders: replace each with whitespace or background shift; keep only survivors that still earn their place.
- Grayscale the screen: hierarchy should survive without color; if not, weight/size work is missing.
- One accent audit: more than one accent-colored element competing → demote all but one.

## Quick wins ladder (polish pass order)

1. Apply the spacing scale; double the whitespace between groups.
2. Collapse text colors to three levels (primary/secondary/tertiary).
3. Kill borders; separate by space and background.
4. One primary button per screen; demote the rest.
5. Fix label/data hierarchy (labels quieter, or folded into data).
6. Align everything to fewer edges (fewer alignment lines = calmer).
7. Shadow ladder pass: consistent elevations.
8. Empty/loading states get real design.

This ladder fixes ~80% of amateur UI in an hour.

## Fast rules while building

- When two spacings look close, jump a scale step — ambiguity is worse than bigness. (RP7, RP10)
- When unsure of a gray, pick the *lighter* text gray and the *subtler* border.
- Emphasize by un-bolding neighbors before bolding the target.
- Numbers in tables: right-align, tabular figures.
- All-caps only for tiny labels, with letter-spacing.
- Icons slightly smaller and softer than they feel like they should be; label them anyway ([NG22](../nielsen-norman-group/engineering-rules.md)).
- Rounded corners: pick one radius family (e.g. 6/10/16) and never mix arbitrary radii.
- Text over image: always a scrim/overlay; never raw.
- Hover/focus/active states designed for every interactive element — not browser defaults ([ECC checklist item too](../wcag/engineering-rules.md) for focus).

## When density is right

Dashboards, tables, pro tools: reduce whitespace deliberately but *systematically* (a denser spacing scale, not squeezed ad-hoc); increase alignment discipline to compensate; hierarchy carries more load when space carries less.
