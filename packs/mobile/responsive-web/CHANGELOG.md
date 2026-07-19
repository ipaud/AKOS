# Changelog — responsive-web

## [1.0.0] — 2026-07-19

### Added

- First complete version: all 17 schema files populated with operational content.
- Principles RW1–RW16, each with an operational corollary, covering mobile-first as a constraint order, the 320px floor, content-driven breakpoints, container-scoped component adaptation, fluid-vs-stepped adaptation, the reflow/restructure ladder, capability parity, chrome budget, density as a per-size decision, the viewport as a range, reserved space, and testing as the only proof.
- RW8 (co-visibility: anything read while acting must be visible while acting) and RW10 (precedent transfers only with its conditions) established as the pack's distinguishing rules.
- Engineering rules RWE1–RWE52, grouped into the 320 floor, breakpoints, horizontal overflow and scroll regions, fluid type and spacing, container queries, restructure thresholds, viewport units and safe areas, chrome and density budget, responsive images, and testing.
- The horizontal-scroll gate: five conditions (exempt content type, region-scoped, pinned identity column, keyboard-operable and named, no unanchored interactive cells) formalized across principles, decision framework, checklist, and rubric.
- Anti-patterns derived from a production audit of an editable data-entry surface: blind editing, precedent laundering, overflow-auto as an answer, overflow suppression, the chrome avalanche, the 100vh trap, display-none as responsive design, notch blindness, truncation as adaptation, and the untested middle. The correctly-implemented dialog pattern (`dvh` cap + internal scroll + `overscroll-contain` + safe-area padding) is encoded as a positive example rather than only its inverse.
- Review checklist and scoring rubric that treat co-visibility loss as a correctness defect, with a hard cap at 59 for any open co-visibility or 320-floor finding, and a cap at 69 when the surface was never opened at 320px.
- Scope boundary recorded against `packs/mobile/touch-ergonomics` (touch, gestures, keyboard, pointer), `packs/ux/wcag` (normative criteria), `packs/frontend/css` (CSS mechanics), and `packs/performance/core-web-vitals` (CLS measurement).
