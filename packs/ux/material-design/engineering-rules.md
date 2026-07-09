# Engineering Rules — Material Design Pack

- MT1. Touch targets ≥48×48dp with ≥8dp spacing (visual size may be smaller; the target may not).
- MT2. Components consume system/component tokens only; no raw hex/dp in component code.
- MT3. Color used exclusively via role pairs (`X`/`on-X`); every `on-X` passes contrast against its `X` in light *and* dark schemes.
- MT4. Full state set implemented via state layers at standard opacities for every interactive component: enabled/hovered/focused/pressed/selected/disabled.
- MT5. Text uses the type-role ramp (display/headline/title/body/label); no ad-hoc sizes.
- MT6. One filled (primary) button per surface; ≤1 FAB per screen, reserved for the signature action.
- MT7. Elevation/tonal-surface levels from the defined ladder; dialogs > sheets > app bars > content; no random elevations.
- MT8. Motion uses duration/easing tokens; transitions match semantics (container transform = hierarchy, shared axis = peers, fade-through = unrelated); `prefers-reduced-motion`/Reduce Motion degrades to fades.
- MT9. Navigation morphs by width: bottom bar (compact) → rail (medium) → drawer (expanded); large canvases adopt canonical layouts (list-detail / feed / supporting pane), never stretched phone UI.
- MT10. Snackbars: transient, ≤1 action, auto-dismiss, never for errors requiring action ([NG31](../nielsen-norman-group/engineering-rules.md) governs those).
- MT11. Dialogs: title states the decision, actions are specific verbs, destructive styled as such, dismissible per platform norms.
- MT12. Text fields: floating labels per spec (visible label at all times — satisfies [WC3](../wcag/engineering-rules.md)), helper/error text in the reserved slot, error state + icon + text (not color-only).
- MT13. Density: comfortable default; compact only via density tokens on designated pro surfaces; MT1 targets hold regardless.
- MT14. Theming defined as: seed/brand color scheme + type ramp + shape scale, applied at token layer; default Material baseline theme does not ship to production ([MD12](principles.md)).
- MT15. TalkBack/keyboard semantics of stock components preserved after theming; custom components ship full anatomy sheets (states, semantics, motion) before use.
- MT16. Dynamic color (where adopted): all brand-critical surfaces verified under hue rotation; contrast guaranteed by role pairs, not by specific hues.
