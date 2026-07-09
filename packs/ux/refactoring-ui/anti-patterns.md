# Anti-Patterns — Refactoring UI Pack

## Border fever

Every element boxed, every section ruled, tables gridded both axes. The UI reads as a cage. Fix: separation ladder (RP22, RU18) — most borders dissolve into spacing.

## Gray soup

Seven ad-hoc grays, none intentional; labels darker than data; disabled indistinguishable from secondary. Fix: three text tokens (RU3), ramps (RU4), label subordination (RU12).

## Size-only hierarchy

Headings at 36px screaming over 12px body; emphasis attempted exclusively via font-size jumps. Fix: RP1 — weight and color first; collapse the size range.

## Accent inflation

Brand color on buttons, links, icons, borders, headings, badges — everywhere and therefore nowhere. Fix: accent budget; most of the brand's presence should come from neutrals-with-personality + one confident accent.

## The unstyled-state ghost

Default browser focus ring erased, no hover states, spinner-only loading, blank empty states. The UI feels dead or broken at its edges. Fix: RU14, RU15 — states are the product most of the time.

## Pixel-picked spacing

`margin: 13px 7px 11px`; every gap negotiated individually. Inconsistency users feel but can't name. Fix: RU1 scale; round to steps.

## Pure-decoration shadows

Random blur/spread per component, shadows on flat elements, glow abuse. Fix: RU8 ladder; elevation means something.

## Radius roulette

4px buttons, 12px cards, 999px inputs, 2px badges in one view. Fix: RU9 family.

## Transparency-as-de-emphasis on color

50%-opacity white text on colored backgrounds (muddy, contrast-failing). Fix: RP19 — hand-picked tint of the background hue, contrast-checked.

## The stretched form

A 6-field form spanning 1400px, fields grabbing full width. Fix: RP9 — content width, centered; forms ~640px.

## Mockup maximalism

Designing every screen pixel-perfect before building anything; polish promised that engineering can't pay. Fix: fidelity-as-commitment (mental models); design a little, build a little.

## Copy-the-pixels theft

Duplicating an admired UI's exact values without extracting its system — breaks on first novel screen. Fix: RP27 — steal the *system* (scale, ramps, ladder), regenerate the pixels.
