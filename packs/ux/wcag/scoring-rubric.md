# Scoring Rubric — WCAG Pack (Accessibility Score)

Primary input to [scoring/accessibility-score.md](../../../scoring/accessibility-score.md).

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| ★ Floor violation on a primary task path (keyboard-incompletable, nameless primary controls, invisible focus app-wide, trap) | −25 each (CRITICAL) |
| ★ Floor violation off the primary path | −10 (HIGH) |
| Systemic component failure (library-level) | −15 once + component fix required (HIGH) |
| AA failure on primary path (contrast, reflow, error association, live regions, modal gauntlet) | −10 (HIGH) |
| AA failure off primary path | −4 (MEDIUM) |
| Missing autocomplete, tooltip behavior, table semantics, consistent-help placement | −1 each, cap −8 (LOW) |

## Hard caps

- Any open ★ CRITICAL: score ≤ 59 (Blocked) — mirrors the constitutional floor.
- No automated scan run (WC36): cap 69.
- Scanner-clean but no manual walks performed: cap 79 (audit theater guard).

## Modifiers

- All three walks documented with findings fixed: +5 (cap 100).
- Accessible component library adopted product-wide: +3.

## Anchors

- **95** — AA verified by walks; only polish remains.
- **83** — floor solid, a cluster of AA MEDIUMs off-path.
- **70** — floor holds on primary paths; AA gaps scheduled; acceptable for MVP only.
- **≤59** — a keyboard user or screen-reader user cannot complete the primary task; BLOCKED everywhere.
