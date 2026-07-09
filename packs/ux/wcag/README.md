# Pack: WCAG — Web Accessibility as Pass/Fail Engineering

**Domain:** UX/Accessibility · **Authority:** Level 1 (official W3C standard) · **Version:** 1.0.0

Operationalizes the Web Content Accessibility Guidelines (2.2, level AA as the working target) into concrete pass/fail checks for building and reviewing. This is AKOS's accessibility floor: per the [constitution](../../../core/constitution.md), no reasoning profile and no personal preference may drop below it.

This pack restates requirements operationally and cites success criteria by number — the normative text at w3.org is always the authority ([source-policy](../../../core/source-policy.md)).

## When to load this pack

- Any UI build or review (the [accessibility-reviewer](../../../agents/accessibility-reviewer.md) always loads it).
- Color/palette decisions (contrast floors).
- Form, focus, keyboard, and error design.
- Resolving "personality vs accessibility" conflicts — this pack wins ([Ruling R1](../../../core/conflict-resolution.md)).

## Structure: POUR

WCAG organizes everything under four principles — content must be **Perceivable**, **Operable**, **Understandable**, **Robust**. The pack's [principles.md](principles.md) maps each to engineering reality; [engineering-rules.md](engineering-rules.md) gives the checkable rules; [review-checklist.md](review-checklist.md) is the audit.

## Conformance stance

- **Floor (every profile, even Prototype):** keyboard reachability, accessible names, visible labels, basic contrast, no keyboard traps, honest error identification.
- **Target (Production/Enterprise):** WCAG 2.2 AA across the product.
- **AAA:** adopted selectively where cheap (e.g. enhanced contrast in a dark theme), never claimed globally.

## Related packs

[steve-krug](../steve-krug/README.md) · [nielsen-norman-group](../nielsen-norman-group/README.md) · [apple-hig](../apple-hig/README.md) · [material-design](../material-design/README.md) · [frontend/html](../../frontend/html/README.md)
