# Examples — Refactoring UI Pack

Invented cases.

## Label subordination (RP3, RU12)

Bad:

```
NAME:    Ana Torres
EMAIL:   ana@studio.dev
PLAN:    Pro
```

(labels bold-caps, data plain — hierarchy inverted)

Good:

```
Ana Torres
ana@studio.dev
Pro plan · renews 12 Aug
```

(data leads; "plan" folded into the value; email self-identifies)

## Card separation ladder (RP22)

- v0: card with border + shadow + divider lines between rows.
- v1: drop border (shadow suffices), drop dividers (row spacing suffices).
- v2: on a gray-50 page background, drop shadow too — white card on gray separates itself.

## Emphasis by de-emphasis (RP2)

Nav where every item is `font-weight: 600; color: gray-900`. To highlight the active item, don't add a background pill first — set inactive items to `400 / gray-500`; active stays 600/900. Calmer, clearer.

## Spacing scale application (RU1, RU10)

Form field group, before: label 6px above input, 14px to next field. Label floats ambiguously (RP10). After (scale 4/8/12/16/24): label 8px above its input, 24px between fields — 3× ratio makes ownership unambiguous.

## Shade ramp (RU4) — sketch

```
blue-50  #EFF6FF   bg-subtle
blue-100 #DBEAFE   bg-hover
blue-200 #BFDBFE   border-subtle
blue-500 #3B82F6   icons, secondary buttons
blue-600 #2563EB   primary buttons (white text: 4.5:1 ✓)
blue-700 #1D4ED8   button hover
blue-900 #1E3A8A   headings on blue-50
```

Pairs precomputed: `blue-600 + white ✓`, `blue-500 + white ✗ (3.9:1) → large text only`.

## Colored background text (RP19)

Bad: `rgba(255,255,255,0.6)` on `blue-600` (muddy, 2.9:1).
Good: hand-picked `blue-100` on `blue-600` (5.2:1, harmonious).

## Empty state as composition (RU15)

Bad: "No projects found."
Good: small illustration consistent with icon family + "Your projects live here. Create your first one — takes about a minute." + primary button "New project". (Also satisfies [Krug ER25](../steve-krug/engineering-rules.md) and [NG35](../nielsen-norman-group/engineering-rules.md).)
