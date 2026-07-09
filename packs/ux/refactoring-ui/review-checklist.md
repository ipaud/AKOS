# Review Checklist — Refactoring UI Pack

Visual-craft review; runs after the [Krug](../steve-krug/review-checklist.md) and [WCAG](../wcag/review-checklist.md) checklists (their findings outrank these).

## High

- [ ] Squint test: one dominant element per screen; hierarchy survives grayscale. (RP1, RP2)
- [ ] Spacing from the scale; within-group < between-group everywhere. (RU1, RU10)
- [ ] Text colors collapsed to 3 tokens; labels subordinate to data. (RU3, RU12)
- [ ] One primary action style per screen; button hierarchy tokens only. (RU7)
- [ ] All token text/bg pairs pass contrast floors. (RU6)
- [ ] Hover/focus/active/disabled designed for all interactives. (RU14)
- [ ] Empty + loading states are designed compositions. (RU15)

## Medium

- [ ] ≤4 font sizes per screen, from the scale. (RU2)
- [ ] Borders justified; separation ladder applied. (RU18)
- [ ] Shadow ladder consistent; elevation meaningful. (RU8)
- [ ] One radius family. (RU9)
- [ ] Grays temperature-consistent with palette. (RU5)
- [ ] Prose ≤75ch, line-heights correct, table numerics right-aligned tabular. (RU11)
- [ ] Text over images has verified contrast treatment. (RU13)
- [ ] Forms/content constrained to natural width, not stretched. (RP9)

## Low

- [ ] Icons single-family, optically aligned. (RU17)
- [ ] All-caps labels letter-spaced; no thin weights in UI. (RP15, RU16)
- [ ] No one-off token overrides (variants added to the system instead).
- [ ] Personality dials consistent across screens (radius, tone, energy).
