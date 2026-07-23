# Scoring Rubric — Touch Ergonomics Pack

Primary input to the Mobile dimension (pipeline step 4,
[review-pipeline.md](../../../core/review-pipeline.md)), scored alongside
[responsive-web](../responsive-web/scoring-rubric.md) and fed directly into
[overall-score](../../../scoring/overall-score.md). Safety-floor findings also
feed [accessibility-score](../../../scoring/accessibility-score.md), and
task-completion findings also feed [ux-score](../../../scoring/ux-score.md);
deduplicate the underlying defect. Score = 100 − deductions, floor 0. Bands per
[core/scoring-model.md](../../../core/scoring-model.md).

Two classes of finding are scored as correctness defects rather than ergonomics: a mis-resolved hit area that activates the wrong control, and a numeric input that commits a value the user did not enter. Both change data; both are graded like a wrong calculation.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Hit area overlaps a **destructive** control's hit area (TEE11) | −25 (CRITICAL) |
| User-entered number reaches storage via `Number()`/`parseFloat()` with a `\|\| 0`-style fallback (TEE39, TEE40) | −25 (CRITICAL) |
| Unparseable or comma-decimal input silently commits a value instead of erroring (TEE42) | −25 (CRITICAL) |
| Meaning, control, or warning available only on hover or via `title` (TEE15, TEE16) | −25 (CRITICAL, safety floor) |
| Gesture-only action with no single-pointer equivalent, gesture not essential (TEE46, SC 2.5.1) | −25 (CRITICAL, safety floor) |
| Viewport meta suppresses zoom (`user-scalable=no`, `maximum-scale=1`) (TEE35) | −25 (CRITICAL, safety floor) |
| Interactive element under 24×24 with no applicable SC 2.5.8 exception (TEE1) | −25 (CRITICAL, safety floor) |
| Action fires on the down-event or cannot be cancelled before release (TEE53, SC 2.5.2) | −25 (CRITICAL, safety floor) |
| Overlapping hit areas between non-destructive controls (TEE9, TEE10) | −10 per cluster (HIGH) |
| Primary, destructive, repeated, or dismiss control under 44/48 (TEE2, TEE7) | −10 each (HIGH) |
| Form control under 16px on coarse pointers (TEE34) | −10 (HIGH) |
| 16px floor documented but bypassable — no primitive, lint, or backstop (TEE36, TEE37) | −10 (HIGH) |
| `type="number"` on a non-quantity field (phone, card, postal code, PIN, amount) (TEE31) | −10 each (HIGH) |
| State-advancing action reachable only above a scroll longer than one viewport (TEE23) | −10 (HIGH) |
| Destructive control adjacent to the primary action or in the bottom-third thumb zone (TEE24) | −10 (HIGH) |
| Sticky/fixed primary action covered by the virtual keyboard (TEE26) | −10 (HIGH) |
| Row actions or affordances visible only on hover (TEE16) | −10 per surface (HIGH) |
| Touch sizing or hover affordances gated on viewport width or UA sniffing (TEE19, TEE20) | −10 (HIGH) |
| Scrollable overlay without `overscroll-behavior: contain`, or missing body-scroll lock (TEE50, TEE52) | −10 (HIGH) |
| No undo on a consequential action, or undo out of thumb reach (TEE54) | −10 (HIGH) |
| Row-level actions below the floor in a dense table or list (TEE5) | −4 each (MEDIUM) |
| Adjacent targets meeting the floor but separated by under 8px (TEE12) | −4 per cluster (MEDIUM) |
| Missing `inputmode`, `autocomplete`, or `enterkeyhint` on a field that needs it (TEE28–TEE30) | −4 per field, cap −16 (MEDIUM) |
| Parsed money/quantity not echoed back before commit (TEE43) | −4 each (MEDIUM) |
| Locale-aware parser missing grouping separators, nbsp, currency symbols, or empty input (TEE41) | −4 (MEDIUM) |
| `touch-action: none` used as a scroll workaround (TEE49) | −4 each (MEDIUM) |
| Horizontal scroller without `overscroll-behavior-x: contain` (TEE51) | −4 each (MEDIUM) |
| Custom drag interaction inside a system-gesture edge strip (TEE48) | −4 each (MEDIUM) |
| Bottom bar ignoring `env(safe-area-inset-bottom)`, or `vh` where `dvh`/`svh` is needed (TEE25, TEE27) | −4 each (MEDIUM) |
| Feedback rendered under the contact point — validation, tooltip, or toast (TE2) | −4 per surface (MEDIUM) |
| Hover styling outside a `hover: hover` query, or sticky hover after tap (TEE18, TEE21) | −4 (MEDIUM) |
| Confirming button placed where the user's finger just landed (TEE54) | −4 each (MEDIUM) |
| Checkbox/radio label not part of the hit area (TEE6) | −4 each (MEDIUM) |
| Hit-expanding overlay used where padding would have worked; bleed undocumented (TEE13, TEE14) | −1 each, cap −5 (LOW) |
| Glyph scaled with the target instead of being sized independently (TEE4) | −1 each, cap −5 (LOW) |
| Custom control replacing a native picker with no stated advantage (TEE38) | −1 each, cap −5 (LOW) |
| Missing explicit `:active` feedback on touch (TEE21) | −1 each, cap −5 (LOW) |

## Hard caps

- Any open CRITICAL finding: score ≤ 59 (BLOCKED). An interface that activates the wrong control or commits a number the user did not enter fails this dimension regardless of how it looks.
- A documented touch rule that components can bypass, with no primitive/lint/backstop, Production profile: cap 79. Knowing the rule earns nothing.
- Product ships in a comma-locale with no locale-aware numeric parsing anywhere: cap 69.
- No touch review performed on a real device, Production profile: cap 84.

## Modifiers

- Hit-area arithmetic (`gap ≥ F − (wA + wB)/2`) computed and recorded for every cluster in the change: +3.
- Automated target-size check (client-rect sweep or equivalent) running in CI: +5 (cap 100).
- Numeric-input tests cover a dot-locale and a comma-locale: +3.
- Flow exercised on a real device, one-handed, with the keyboard open: +2.
- Repeat finding from a previous review, unfixed without a recorded tradeoff: double its deduction.
- Finding fixed at the instance only, when a primitive or lint rule was available: no credit — the finding remains open.

## Interpretation anchors

- **95** — targets built to the ergonomic target, gap arithmetic recorded, no hover-carried meaning, primary actions in thumb reach, locale-safe parsing enforced in a shared primitive with CI backing. Remaining findings are polish.
- **85** — sound and enforced; a cluster of MEDIUMs (missing `enterkeyhint`, a carousel without overscroll containment, feedback positioned by desktop habit) to schedule.
- **72** — usable on a phone but visibly ported from desktop: dense row actions at the floor, hover affordances behind a width query, no undo. Acceptable pre-PMF with fixes queued.
- **58** — a delete button owns eight pixels of its neighbour's hit area, or a comma-locale user's amount commits as zero. BLOCKED until the geometry or the parser is corrected — and until the fix is installed somewhere a future component cannot bypass.
