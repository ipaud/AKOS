# Prompt Fragments — Refactoring UI Pack

## Fragment: build-mode constraint block

```text
Apply visual-craft constraints (Refactoring UI school, AKOS L3):
- Systems before elements: spacing scale (4/8/12/16/24/32/48/64), type
  scale (≤9 steps, ≤4 per screen), 3 text-color tokens, shade ramps per
  hue, ≤5 named shadows, one radius family.
- Hierarchy via weight and color before size; de-emphasize neighbors
  before emphasizing targets; labels subordinate to data or folded in.
- One primary action per screen; button hierarchy tokens only.
- Separation ladder: whitespace → background shift → shadow → border;
  justify every border.
- Whitespace generous by default; within-group < between-group always.
- Palette: grays temperature-matched; contrast pairs precomputed to pass
  4.5:1; on colored bg use hue tints, never gray/transparency.
- Design hover/focus/active/disabled for everything; empty and loading
  states are designed compositions.
- Text over images gets a scrim; prose ≤75ch; table numerics right-aligned.
```

## Fragment: polish-pass lens

```text
Run a visual polish review (Refactoring UI ladder). In order:
1. Squint test — name the dominant element; if none, hierarchy findings first.
2. Count font sizes and text grays; flag >4 sizes / >3 grays.
3. Border audit — list every border replaceable by spacing/background shift.
4. Accent audit — count accent-colored elements; >1 competing = demote.
5. Spacing audit — off-scale values, ambiguous group spacing.
6. State audit — hover/focus/active/disabled/empty/loading designed?
7. Depth audit — shadow consistency, radius family, light direction.
For each finding: the smallest token-level fix. Never suggest a redesign
where a token correction suffices. WCAG contrast floors override any
aesthetic suggestion.
```

## One-liner

```text
Visual craft: pick from systems (spacing/type/color/shadow scales), never
per-element; hierarchy = weight+color before size; de-emphasize to
emphasize; whitespace before borders; one accent, one primary, one radius
family; ramps with precomputed accessible pairs; design all states
including empty/loading.
```
