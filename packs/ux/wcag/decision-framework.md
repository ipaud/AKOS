# Decision Framework — WCAG Pack

## Native vs ARIA widget

1. Native element exists (`select`, `dialog`, `details`, `input[type=…]`) → use it. Restyle within limits.
2. Native exists but can't be styled to requirements → first challenge the requirement ([R1](../../../core/conflict-resolution.md): aesthetics adapt); if the interaction pattern is genuinely beyond native (combobox with rich options, multi-select tags) →
3. Adopt a maintained accessible component library implementing APG patterns →
4. Hand-roll the full APG pattern (keyboard map + roles + states + focus management) — budget 3–5× the visual build cost. Partial ARIA is not a fallback; it's a defect (MP2).

## AA vs floor vs AAA, per profile

| Profile | Requirement |
|---------|-------------|
| Prototype | Floor rules (★ in [engineering-rules.md](engineering-rules.md)) |
| Startup MVP | Floor + WC36 scanner-clean + keyboard walk on primary flows |
| Production | WCAG 2.2 AA (full checklist) |
| Enterprise | AA + documented conformance statement (VPAT-style) + audit trail |
| Game Dev | Floor for menus/UI; remappable inputs; motion/flash safety; captions for speech |
| Internal Tool | Floor + keyboard completeness (internal users include disabled colleagues; legal exposure remains) |

## Brand color fails contrast — what order to try

1. Darken/lighten the brand shade until 4.5:1 (usually imperceptible to brand).
2. Restrict the failing pair to large text / non-text uses (3:1 zone).
3. Swap roles: brand as background with white text often passes where the inverse fails.
4. Add a duplicate "on-X" token so the failing combination becomes unrepresentable.
Never: ship the failing pair with a "brand consistency" justification — R1 forecloses it.

## Motion/animation decisions

- Decorative → wrap in `prefers-reduced-motion: no-preference`.
- Communicative (state transitions) → keep, shorten, and ensure the end state reads without the motion.
- Essential (the product is the motion — games, viz) → provide reduce/disable controls in-app.

## When a fix conflicts with usability advice

Rare, but occurs (e.g. NN/g minimalism vs visible labels; platform pattern vs WCAG). Resolution per [R12](../../../core/conflict-resolution.md): WCAG wins on substance, platform/usability wins on idiom — and a design satisfying both almost always exists; find it before invoking the ruling.

## Retrofit prioritization (inherited inaccessible codebase)

1. Component library first (buttons, inputs, modals, toasts) — every fix multiplies.
2. Primary task paths end-to-end (sign-in → core action → save/submit).
3. Templates/layout (landmarks, headings, skip links, titles).
4. Long tail by traffic.
Track with WC36 in CI so the debt only shrinks.
