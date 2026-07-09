# Mental Models — Refactoring UI Pack

## The systems-first designer

Amateur: designs elements (picks this button's blue, that gap's pixels). Professional: designs *systems* (the blues that exist, the gaps that exist), then assembles. Every visual decision made twice is a system waiting to be extracted. This is design's DRY.

## Visual loudness budget

Every property has volume: size, weight, color contrast, saturation, borders, shadows, motion. A screen's total loudness is budgeted; spending everywhere = white noise. Hierarchy = deliberate loudness allocation, mostly achieved by *turning things down*. Audit tool: squint test ([Krug](../steve-krug/heuristics.md)).

## The separation ladder

To separate two things, climb only as high as needed: whitespace → background shift → shadow → border → divider+label. Each rung adds noise. Over-bordered UI = a ladder always climbed to the top.

## Shade ramps as infrastructure

A color isn't a value, it's a ramp of 8–10 shades serving different jobs (backgrounds, borders, icons, text, hover states). Defining ramps up front converts a thousand ad-hoc choices into lookups — and lets accessibility pairs be precomputed (RP20).

## Personality dials

Every product sits on dials: serif↔sans↔rounded (tone), muted↔vivid (energy), sharp↔rounded corners (formality), sparse↔dense (seriousness), still↔animated (playfulness). Set the dials once, encode in tokens, and personality emerges consistently. Random dial positions per screen = brand incoherence.

## Fidelity as commitment

A pixel-perfect mockup is a contract you haven't priced. Design at the fidelity of the decision being made: grayscale boxes for layout, real type for hierarchy, full color only when the system exists. This keeps design throwaway-cheap during discovery ([Lean Startup](../../product/lean-startup/README.md) energy at the pixel level).
