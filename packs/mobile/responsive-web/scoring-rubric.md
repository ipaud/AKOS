# Scoring Rubric — Responsive Web Pack (Layout & Adaptation)

Primary input to the Mobile dimension in lens 4 of the
[review pipeline](../../../core/review-pipeline.md), fed directly into
[overall-score](../../../scoring/overall-score.md). Its safety-floor findings
also feed [accessibility-score](../../../scoring/accessibility-score.md), and
its task-completion findings feed [ux-score](../../../scoring/ux-score.md).
Score = 100 − deductions, floor 0. Bands per
[core/scoring-model.md](../../../core/scoring-model.md).

Deduplicate across lenses: one defect, one deduction, cited by the pack that explains it deepest.

Co-visibility findings are scored as correctness defects, not layout polish: a user editing a value whose identifier has scrolled off-screen is being asked to act on information the interface removed.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Interactive control inside a horizontal scroll region with no pinned identity column (RWE19) | −25 (CRITICAL) |
| A value required for the action is not visible while the control is operated, at 320px (RW8) | −25 (CRITICAL) |
| Document-level horizontal scrolling at 320px (RWE3) | −25 (CRITICAL) |
| Two-dimensional scrolling required to read or operate content (RW3, WCAG 1.4.10) | −25 (CRITICAL, safety floor) |
| Zoom suppressed (`user-scalable=no`, `maximum-scale` < 5) (RWE2) | −25 (CRITICAL, safety floor) |
| A capability is unreachable at 320px (RWE8) | −25 (CRITICAL) |
| Focus order contradicts visual order after reflow (RWE34) | −25 (CRITICAL, safety floor) |
| Viewport-unit-only `clamp()` preferred value on text (RWE21) | −10 (HIGH) |
| Horizontal scroll region failing any other gate condition — not focusable, unnamed, no affordance, non-exempt content (RWE15–RWE18) | −10 per region (HIGH) |
| Editable wide table left scrolling instead of restructured (RWE31) | −10 per surface (HIGH) |
| Narrow view drops a capability the wide view has, unannotated (RWE32, RWE33) | −10 per capability (HIGH) |
| `overflow-x: hidden` on `html`/`body` (RWE4) | −10 (HIGH) |
| `100vh` on a container holding a control that must stay reachable (RWE36) | −10 (HIGH) |
| Dialog/drawer without height cap, internal scroll, or `overscroll-behavior: contain` (RWE37) | −10 each (HIGH) |
| Edge-anchored surface with no safe-area padding, or `viewport-fit=cover` missing (RWE39) | −10 (HIGH) |
| At 320px, no content visible before the first scroll (RWE41) | −10 (HIGH) |
| Money, dates, identifiers, or names truncated on an action surface (RWE35) | −10 each (HIGH) |
| Precedent reused across a difference in kind without restating its conditions (RW10) | −10 (HIGH) |
| Fixed `width`/`min-width` above 320px in normal flow (RWE5) | −4 each (MEDIUM) |
| Width-based media query inside a reusable component (RWE27) | −4 each (MEDIUM) |
| Device-named breakpoints, or breakpoints not declared as tokens (RWE9, RWE10) | −4 (MEDIUM) |
| Header wrapping to 3+ rows at 320px; >2 primary actions wrapping (RWE42, RWE43) | −4 each (MEDIUM) |
| Image, embed, or ad slot with no declared dimensions or reserved space (RWE46, RWE50) | −4 each (MEDIUM) |
| `sizes` disagreeing with the real CSS layout width (RWE47) | −4 each (MEDIUM) |
| Art direction done via CSS background swap instead of `<picture>` (RWE48) | −4 (MEDIUM) |
| LCP image lazy-loaded (RWE49) | −4 (MEDIUM) |
| Body text below 16px effective at any width (RWE24) | −4 (MEDIUM) |
| Nested scroll region without `overscroll-behavior` (RWE37) | −4 each (MEDIUM) |
| Breakpoints in px rather than em; >5 page-level breakpoints; conflicting or uncovered width range (RWE11–RWE14) | −1 each, cap −5 (LOW) |
| Per-component `clamp()` instead of tokens; fluid swing >2× (RWE20, RWE22) | −1 each, cap −5 (LOW) |
| Measure outside 45–75ch; desktop vertical rhythm unchanged at 320 (RWE23, RWE25) | −1 each, cap −5 (LOW) |
| Container thresholds undocumented; `vw` used inside a container instead of `cqi` (RWE28, RWE29) | −1 each, cap −5 (LOW) |

## Hard caps

- Any open CRITICAL co-visibility or 320-floor finding: score ≤ 59 (BLOCKED). A surface where the user acts on values the layout has removed fails this dimension regardless of how well it renders elsewhere.
- Surface never opened at 320px during this change: cap 69. The claim is unverified, and most findings here are only reachable by driving the page.
- Editable surface with no restructured narrow form and no recorded decision, Production profile: cap 69.
- No automated horizontal-overflow assertion in the test suite, Production profile: cap 89.

## Modifiers

- 320 task walk completed and recorded (a primary task finished, not observed): +5 (cap 100).
- Automated no-horizontal-overflow assertions at all five widths in CI: +3.
- Responsive patterns documented with their preconditions, so precedent carries its conditions: +3.
- Container queries used for component adaptation with a stacked default: +2.
- Repeat finding from a previous review, unfixed without a recorded tradeoff: double its deduction.

## Interpretation anchors

- **95** — narrow layout designed rather than derived; co-visibility verified with controls focused; wide content either restructured or gated correctly; fluid tokens and container queries throughout; overflow assertions in CI.
- **85** — sound and tested at all five widths; a cluster of MEDIUMs (image dimensions, a stray fixed width, a header that wraps to three rows) to schedule.
- **72** — works, but the narrow layout was derived from the wide one: density inherited, some truncation, a scroll container or two that pass the gate only partially. Acceptable pre-PMF with fixes queued.
- **58** — an editable surface scrolls sideways without a pinned identity column, or something is unreachable at 320. BLOCKED until the layout is restructured, not until it is tidied.
