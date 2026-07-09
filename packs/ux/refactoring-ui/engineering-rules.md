# Engineering Rules — Refactoring UI Pack

- RU1. All spacing values come from a defined scale (e.g. 4/8/12/16/24/32/48/64px); no arbitrary margins/paddings in code review.
- RU2. All font sizes come from a defined type scale (≤9 steps); per-screen usage ≤4 sizes.
- RU3. Text color uses exactly three tokens per surface (primary/secondary/tertiary); no ad-hoc grays.
- RU4. Palette defined as shade ramps (8–10 shades per hue) in tokens; components reference tokens, never raw hex.
- RU5. Gray ramp is temperature-consistent (warm or cool, matching palette), never pure `#808080`-family throughout.
- RU6. Accessibility pairs precomputed: every text-token/background-token combination in use passes 4.5:1 (3:1 large) — enforced at token level. (WCAG WC16)
- RU7. One primary-styled action per screen; button hierarchy tokens (primary/secondary/tertiary/destructive) exist and are the only button styles.
- RU8. Shadow system: ≤5 named elevations; components use named elevations only.
- RU9. One border-radius family (≤3 values) app-wide.
- RU10. Within-group spacing < between-group spacing on every composite; label sits closer to its field than to the previous field.
- RU11. Prose measure ≤ ~75ch; body line-height ≥1.5; headings 1.1–1.25; table numerics right-aligned with tabular figures.
- RU12. Labels visually subordinate to data (smaller and/or softer), or folded into the value.
- RU13. Text over images always has a contrast treatment (scrim, overlay, text shadow) verified against WC16.
- RU14. Hover, focus-visible, active, and disabled states explicitly designed for every interactive component.
- RU15. Empty and loading states are designed compositions (illustration/guidance/skeleton), not blank or default-spinner surfaces.
- RU16. UI font weights ≥400; de-emphasis via color/size, not thin weights.
- RU17. Icon set is single-family, consistent stroke/size; icons accompanying text are optically aligned and sized to the text.
- RU18. Border count justified: any border removable by whitespace or background-shift without losing grouping is removed.
