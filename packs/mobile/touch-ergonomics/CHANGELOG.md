# Changelog — touch-ergonomics

## [1.0.0] — 2026-07-19

### Added

- First complete version: all 17 schema files populated with operational content.
- Principles TE1–TE16, each with an operational corollary, covering finger imprecision, occlusion, the absent hover channel, commitment-on-contact, the two target-size floors, spacing as part of the target, the thumb-reach gradient, consequence-vs-reachability, gestures as accelerators, the virtual keyboard as layout and as contract, locale-dependent parsing, capability-not-width, enforcement over documentation, recovery, and field context.
- Engineering rules TEE1–TEE54, grouped into target size, spacing and non-overlap, hover/focus/pointer capability, placement and reach, the virtual keyboard and input attributes, locale-safe parsing, gestures and scrolling, and accidental activation.
- The non-overlap gap formula `gap ≥ F − (wA + wB)/2` as a computable engineering rule (TEE10), with worked arithmetic in `examples.md`.
- A locale-aware numeric parser returning `number | null`, with separators derived from `Intl.NumberFormat.formatToParts`, and a ban on `|| 0` fallbacks in persisting paths (TEE39–TEE45).
- Anti-patterns derived from a real production audit: the contested strip, the comma that ate the number, the rule that lives in a doc, hover-only meaning, and the action at the top of the scroll — plus twelve further named failure modes covering desktop density, gesture-only actions, edge-strip conflicts, `touch-action: none` misuse, scroll chaining, keyboard-covered actions, zoom suppression, `type="number"` misuse, occluded feedback, down-event activation, sticky hover, and width-as-capability.
- Review checklist and scoring rubric that treat mis-resolved hit areas and silently coerced numeric input as correctness defects, with a hard cap at 59 for any open CRITICAL, a cap at 79 for a documented-but-bypassable rule, and no credit for instance-only fixes.
- Standards restated operationally and cited by criterion number: WCAG 2.2 SC 2.5.8, 2.5.5, 2.5.1, 2.5.2, 2.5.4, 1.4.4.
- Scope boundary recorded against `packs/mobile/responsive-web` (layout, breakpoints, reflow); cross-links to `packs/ux/wcag`, `packs/ux/apple-hig`, `packs/ux/material-design`, and `packs/content/ux-writing`.
