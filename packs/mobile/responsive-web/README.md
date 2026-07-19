# Pack: Responsive Web — Layout & Adaptation

**Domain:** Mobile · **Authority:** Level 2 (industry authority + W3C specifications) · **Version:** 1.0.0

Operationalizes how a web layout adapts across widths: the constraint order mobile-first actually imposes, breakpoints derived from content rather than device names, fluid type and spacing, container queries as the correct unit of component adaptation, the 320px floor and WCAG 1.4.10 reflow, the narrow list of things that may legitimately scroll sideways, the untrustworthy viewport, and responsive images that don't cost layout stability.

The governing idea: **adaptation is a decision made per size, not a squeeze.** A layout that "survives" 320px by shrinking is not responsive — it is a desktop layout with the evidence pushed off-screen.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Building or reviewing any web surface — [constitution](../../../core/constitution.md) Article 9 makes this default, not optional.
- Any table, grid, dashboard, or editor wider than a phone.
- Choosing breakpoints; writing media or container queries; setting type and spacing scales.
- Full-height layouts, dialogs, sticky bars, anything touching `vh` or a device notch.
- Responsive images and art direction, when bandwidth or layout stability is in scope.
- Reviewing a diff that adds `overflow-x`, a `display: none` at a breakpoint, or a fixed pixel width.

## Scope boundary

This pack covers **layout and adaptation** — how much space there is, and what the interface does about it.

Touch target sizing, gestures, hover and pointer realities, the virtual keyboard, and input ergonomics belong to [touch-ergonomics](../touch-ergonomics/README.md). Normative accessibility criteria belong to [wcag](../../ux/wcag/README.md) — this pack restates SC 1.4.10 operationally and defers on everything else. CSS mechanics, tokens, and animation belong to [frontend/css](../../frontend/css/README.md). CLS budgets and field measurement belong to [core-web-vitals](../../performance/core-web-vitals/README.md). Load them alongside rather than duplicating them here.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Narrow-first as a constraint order; the squeeze fallacy; adaptation as editing |
| [mental-models.md](mental-models.md) | Read-while-acting pair, reflow/restructure ladder, the 320 floor, container-is-the-world, chrome budget, precedent's conditions |
| [principles.md](principles.md) | RW1–RW16, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults for breakpoints, type, wide content, chrome, media, testing |
| [engineering-rules.md](engineering-rules.md) | RWE1–RWE52: checkable in the artifact |
| [decision-framework.md](decision-framework.md) | Reflow vs restructure · media vs container query · the horizontal-scroll gate · which viewport unit |
| [anti-patterns.md](anti-patterns.md) | Blind editing, device-name breakpoints, overflow-auto as an answer, precedent laundering, chrome avalanche |
| [review-checklist.md](review-checklist.md) | Binary pass/fail, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases with the rule applied |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents |
| [scoring-rubric.md](scoring-rubric.md) | Responsive-layout scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Every value a user must read while acting on it has to be visible while they act — the rest of this pack is the layout discipline that keeps that promise all the way down to 320 pixels.

## Related packs

[touch-ergonomics](../touch-ergonomics/README.md) · [wcag](../../ux/wcag/README.md) · [frontend/css](../../frontend/css/README.md) · [core-web-vitals](../../performance/core-web-vitals/README.md)
