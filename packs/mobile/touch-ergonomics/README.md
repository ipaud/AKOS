# Pack: Touch Ergonomics — The Hand and the Device

**Domain:** Mobile · **Authority:** Level 2 (industry authorities, grounded in Level 1 standards) · **Version:** 1.0.0

Operationalizes what changes when the input device is a human finger instead of a mouse. The governing idea: a touchscreen is not a small desktop screen — it is a different input channel with different physics. The pointer is fat, imprecise, and attached to a hand that covers the screen; it has no hover, no resting position, and no separate "aim then commit" step. Interfaces that ignore that ship a specific, repeatable class of defect: targets too small to hit, meaning locked behind hover, actions placed where the thumb can't reach, and keyboards that hand the code a string it cannot parse.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors or standards bodies. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute. Standards requirements are restated operationally and cited by criterion number so the normative text is one click away.

## When to load this pack

- Building or reviewing any web surface that a phone or tablet will reach — which, per [Article 9](../../../core/constitution.md), is every web surface unless "desktop-only" was explicitly recorded.
- Reviewing dense interactive UI: tables with row actions, toolbars, icon-button clusters, editable grids.
- Any numeric or money input, any form the user fills on a phone, anything involving the virtual keyboard.
- Designing destructive actions, gestures, swipe interactions, or bottom sheets.
- Auditing a component library or design system for enforceable touch defaults.

## Scope boundary

This pack is about **the finger and the device**. Layout adaptation — breakpoints, fluid typography, container queries, reflow, viewport strategy — belongs to [responsive-web](../responsive-web/README.md). Load both: a layout that reflows perfectly to 320px and still ships 28px icon buttons has passed one review and failed this one. Screen-level clarity belongs to [steve-krug](../../ux/steve-krug/README.md); the words on the controls belong to [ux-writing](../../content/ux-writing/README.md); the normative accessibility criteria behind the target-size and gesture rules belong to [wcag](../../ux/wcag/README.md).

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Why the finger is a different device; touch as commitment; enforcement over documentation |
| [mental-models.md](mental-models.md) | Contact patch, occlusion cone, the two floors, contested strip, thumb arc, keyboard contract, capability matrix |
| [principles.md](principles.md) | TE1–TE16: always-true rules of touch interaction, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per surface — sizing, placement, forms, gestures, feedback |
| [engineering-rules.md](engineering-rules.md) | TEE1–TEE54: checkable in the artifact, including the gap formula and the locale parser |
| [decision-framework.md](decision-framework.md) | Which floor applies, enlarge visually vs. hit area, which keyboard, gesture or not, where the control goes |
| [anti-patterns.md](anti-patterns.md) | Contested strip, comma that ate the number, hover-only meaning, rule-in-a-doc, action above the fold |
| [review-checklist.md](review-checklist.md) | Binary pass/fail touch review, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases with the rule and the arithmetic |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents |
| [scoring-rubric.md](scoring-rubric.md) | Touch-ergonomics scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

The finger is a blunt, occluding, hover-less pointer attached to a hand that can only reach part of the screen — every rule in this pack is a consequence of those four facts, and every rule must be enforced in a primitive, because a rule a component can bypass is not a rule.

## Related packs

[responsive-web](../responsive-web/README.md) · [wcag](../../ux/wcag/README.md) · [apple-hig](../../ux/apple-hig/README.md) · [material-design](../../ux/material-design/README.md) · [ux-writing](../../content/ux-writing/README.md)
