# Principles — Material Design Pack

- **MD1 — Components before customs:** use the Material vocabulary (buttons, chips, sheets, nav bar/rail/drawer, text fields, dialogs, snackbars) as shipped, themed via tokens; custom components only for genuinely novel needs, built to the same anatomy/state/motion standards.
- **MD2 — Emphasis levels are the button system:** filled (highest emphasis, one per surface — [Von Restorff](../laws-of-ux/principles.md)) → filled tonal → elevated → outlined → text. Choose by importance, not looks.
- **MD3 — Tonal surfaces convey hierarchy:** in M3, surface containers (lowest→highest) and elevation express layering; dark theme uses tonal shifts, not just shadows. One elevation logic app-wide.
- **MD4 — Every interactive component implements the full state set:** enabled, hovered, focused, pressed, dragged, selected, disabled — via state layers (consistent opacity overlays), not ad-hoc colors. ([NN/g NG12](../nielsen-norman-group/engineering-rules.md); [Refactoring UI RU14](../refactoring-ui/engineering-rules.md))
- **MD5 — Token pyramid discipline:** components consume component/system tokens; raw hex appears only in reference palettes. Dynamic color and dark theme then come nearly free.
- **MD6 — Color roles, not colors:** `primary/on-primary`, `surface/on-surface`, `error/on-error` pairs guarantee contrast pairings by construction ([WCAG WC16](../wcag/engineering-rules.md) enforced at the token level).
- **MD7 — Type scale as roles:** display/headline/title/body/label ramps; UI text picks a role, never a size.
- **MD8 — Motion with a job:** container transform for hierarchy, shared axis for peers, fade-through for unrelated; duration/easing from tokens; Reduce Motion degrades gracefully.
- **MD9 — Navigation morphs by canvas:** bottom navigation bar (compact) → navigation rail (medium) → drawer (expanded); canonical layouts (list-detail, feed, supporting pane) for larger canvases.
- **MD10 — Density with limits:** comfortable default; compact density for pro/data surfaces — applied via density tokens, never by squeezing ([Refactoring UI density mode](../refactoring-ui/decision-framework.md)); touch targets ≥48dp regardless.
- **MD11 — Accessibility is built into the components — keep it:** 48dp targets, TalkBack semantics, contrast-safe role pairs. Custom theming must not break what the components guarantee.
- **MD12 — Theme it or it's a template:** M3 expects brand expression via color scheme, type ramp, and shape scale. Default-theme shipping is a design decision *not taken* ([anti-template policy](../../personal/pau-avila/design-language.md)).
