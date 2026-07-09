# Principles — Refactoring UI Pack

## Hierarchy

- **RP1 — Size is the weakest hierarchy tool.** Prefer weight and color first: primary content in dark/high-contrast text, secondary in softer gray, tertiary lighter still. Two or three text "loudness" levels handle most screens; font size varies less than beginners think.
- **RP2 — De-emphasize to emphasize.** To make something stand out, quiet its neighbors instead of amplifying it. One accent per surface ([LX14](../laws-of-ux/engineering-rules.md)).
- **RP3 — Labels are a last resort.** Data often self-identifies (an email looks like an email) or the label folds into the value ("12 left in stock" not "Stock: 12"). When labels are needed, they're the supporting cast: smaller, softer, never bolder than the data.
- **RP4 — Semantic markup ≠ visual hierarchy.** An `h1` needn't be huge; section titles often work *smaller* than body-loud content because they're signposts, not content. Keep semantics for the tree ([WCAG WC5](../wcag/engineering-rules.md)), style for the eye.
- **RP5 — Actions have a hierarchy too.** Per screen: one primary (solid, high contrast), secondaries (outline/soft), tertiaries (link-styled). Destructive isn't automatically big-red-solid — usually a secondary until it's the screen's point ([Norman NR19](../don-norman/engineering-rules.md) still applies).

## Layout & spacing

- **RP6 — Start with too much whitespace, then remove.** Dense-by-default reads cramped; generous-by-default reads designed. Density is then a deliberate choice for data-heavy surfaces.
- **RP7 — Use a spacing/sizing scale.** Geometric-ish progression (e.g. 4, 8, 12, 16, 24, 32, 48, 64…): adjacent steps differ ≥ ~25% so choices are visibly distinct. No arbitrary pixel values.
- **RP8 — Space groups louder than items.** Within-group spacing < between-group spacing, always — spacing *is* the grouping signal ([proximity](../universal-principles-of-design/principles.md), Krug ER13).
- **RP9 — You don't have to fill the screen.** Constrain content to the width it needs (forms ~ 640px, prose ~ 75ch); columns and centering beat stretching. Shrink the canvas when designing small components.
- **RP10 — Avoid ambiguous spacing.** When spacing between related and unrelated elements is equal, relationships vanish (e.g. a form label floating equidistant between two fields).

## Typography

- **RP11 — A type scale, not ad-hoc sizes.** Hand-picked scale (e.g. 12, 14, 16, 18, 20, 24, 30, 36, 48) beats modular-ratio fractions for UI. Stick to it.
- **RP12 — Two weights are usually enough** (normal 400/500, bold 600/700). Never use <400 for UI text at small sizes; de-emphasize with color/size instead.
- **RP13 — Line height is inversely proportional to size** (body ~1.5, headings ~1.1–1.25) and proportional to line length.
- **RP14 — Align with reading.** Left-align prose (LTR); center only short blocks; right-align numbers in tables; don't justify.
- **RP15 — Letter-spacing:** tighten large headings slightly; widen all-caps labels slightly.

## Color

- **RP16 — You need more colors than you think, from fewer hues than you think.** Per hue: 8–10 shades defined up front (a near-white to a near-black). Typical system: 1 primary hue, 1–2 accents, warm or cool grays, plus semantic red/yellow/green — each as a full shade ramp.
- **RP17 — Grays are never pure.** Saturate grays slightly (cool blue-grays or warm ones) to match the palette's temperature.
- **RP18 — Don't rely on hue alone for states** — pair with contrast shifts, icons, text ([WCAG WC18](../wcag/engineering-rules.md) is the hard floor).
- **RP19 — On colored backgrounds, don't use gray text** — use a lighter/less-saturated tint of the background hue instead of transparency or literal gray.
- **RP20 — Accessibility floors are palette inputs**, not afterthoughts: define token pairs that pass 4.5:1 so failing combinations are unrepresentable ([WCAG decision ladder](../wcag/decision-framework.md)).

## Depth & polish

- **RP21 — A shadow ladder, not ad-hoc shadows.** ~5 elevation steps (subtle card → dropdown → modal); smaller = closer to surface. Use elevation to mean something (interactivity, layering), not decoration.
- **RP22 — Borders are the loudest separator — use them last.** Separation ladder: whitespace → background-color shift → subtle shadow → border. Most UIs over-border.
- **RP23 — Light comes from above.** Raised elements: lighter top edge, shadow below. Inset elements: the reverse. Get this wrong and depth reads broken.
- **RP24 — Overlap creates layers.** Cards crossing section boundaries, offset avatars, images breaking their container — cheap perceived depth.
- **RP25 — Images need art direction:** consistent treatment (overlay, tint, crop discipline); text over images requires a scrim; user-generated images get contained sizes and background fills.
- **RP26 — Sweat the empty, loading, and edge states** — they're most of what users see early ([Krug ER25](../steve-krug/engineering-rules.md) makes them mandatory; this pack makes them *good*).
- **RP27 — Steal like a professional.** Keep a swipe file; decompose interfaces you admire into their systems (scale, palette, shadow ladder) rather than copying pixels.
