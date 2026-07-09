# Accessibility Score (0–100)

Measures WCAG 2.2 AA conformance. Safety-floor dimension — any open floor-level CRITICAL caps the score at 59 (Blocked), mirroring the [constitution](../core/constitution.md).

## Input

Driven by the [WCAG rubric](../packs/ux/wcag/scoring-rubric.md).

## Deductions

- ★ Floor violation on a primary path (keyboard-incompletable, nameless primary controls, invisible focus app-wide, trap): −25 each (CRITICAL)
- ★ Floor violation off primary path: −10 (HIGH)
- Systemic component failure (library-level): −15 once + component fix
- AA failure on primary path: −10 (HIGH); off path: −4 (MEDIUM)
- Minor (autocomplete, tooltip behavior, table semantics): −1 each, cap −8

## Hard caps

- Any open ★ CRITICAL → ≤ 59 (Blocked).
- No automated scan run → cap 69.
- Scanner-clean but no manual walks → cap 79 (audit-theater guard).

## Interpretation

- **95** — AA verified by the three walks; only polish remains.
- **83** — floor solid, a cluster of off-path MEDIUMs.
- **70** — floor holds on primary paths; AA gaps scheduled; MVP-acceptable.
- **≤59** — a keyboard or screen-reader user cannot complete the primary task; BLOCKED everywhere.
