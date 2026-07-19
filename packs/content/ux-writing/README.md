# Pack: UX Writing — Interface Copy

**Domain:** Content · **Authority:** Level 3 (books & methodologies) · **Version:** 1.0.0

Operationalizes the craft of the words *inside* a product: button labels, error messages, empty states, form hints, confirmations, toasts, notifications, and the terminology holding them together. The governing idea: interface copy is not decoration applied after the build — it is the part of the interface that states what the system will do, and it must be true.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — buy/read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Writing or reviewing any string a user will read: labels, messages, states, notifications.
- Reviewing a diff where the copy and the handler might disagree — the most expensive defect this pack catches.
- Designing error handling, empty states, or destructive-action flows.
- Establishing voice and tone, or a terminology list for a product.
- Preparing a product for translation.

## Scope boundary

This pack covers **interface writing** — words attached to controls and states. Long-form content, plain-language rewriting, user-need framing, and content lifecycle belong to [gov-uk-content-design](../gov-uk-content-design/README.md). Screen-level clarity, hierarchy, and whether the screen should exist belong to [steve-krug](../../ux/steve-krug/README.md). Load those alongside this one rather than duplicating them here.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Copy as the honesty layer; why words are the cheapest lever and the easiest place to lie |
| [mental-models.md](mental-models.md) | Label-behavior contract, voice/tone dial, three questions, microcopy ladder, four zero states |
| [principles.md](principles.md) | UW1–UW16: always-true rules of interface writing |
| [heuristics.md](heuristics.md) | Fast defaults per surface — buttons, errors, empties, toasts, forms |
| [engineering-rules.md](engineering-rules.md) | UWE1–UWE45: checkable in the artifact |
| [decision-framework.md](decision-framework.md) | Cut vs write, confirm vs undo, toast vs inline, tone under stress |
| [anti-patterns.md](anti-patterns.md) | Lying labels, phantom confirmations, synonym drift, dead-end empty states |
| [review-checklist.md](review-checklist.md) | Binary pass/fail copy review, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases with the rule applied |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents |
| [scoring-rubric.md](scoring-rubric.md) | Interface-copy scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

A label is a promise the code has to keep — the rest of this pack is about making promises worth reading, in one consistent voice, at the moment the user needs them.

## Related packs

[gov-uk-content-design](../gov-uk-content-design/README.md) · [steve-krug](../../ux/steve-krug/README.md) · [nielsen-norman-group](../../ux/nielsen-norman-group/README.md) · [wcag](../../ux/wcag/README.md)
