# Anti-Patterns — WCAG Pack

## Div soup

**Detect:** `div`/`span` with click handlers, cursor styling, and no role/tabindex/keyboard handling.
**Cost:** invisible to the tree, unreachable by keyboard — the component doesn't exist for AT.
**Fix:** native `button`/`a`; if genuinely custom, the *complete* APG pattern. (WC1)

## ARIA confetti

**Detect:** `role`/`aria-*` sprinkled without the corresponding behavior — `role="button"` with no key handling, `aria-expanded` never updated, `role="menu"` on a nav list.
**Cost:** confident false promises; worse than silence (MP2).
**Fix:** remove decorative ARIA; implement full patterns where custom widgets are real.

## Placeholder-as-label

**Detect:** inputs whose only label is placeholder text.
**Cost:** label vanishes on input; fails 3.3.2; memory tax mid-form ([Miller](../laws-of-ux/principles.md)).
**Fix:** visible bound labels; placeholders only for format examples. (WC3)

## The vanishing focus

**Detect:** `outline: none` / `:focus { outline: 0 }` in global CSS with no replacement.
**Cost:** keyboard users navigate blind; single highest-frequency a11y sin in codebases.
**Fix:** WC12 — styled `:focus-visible` ring, ≥3:1.

## Contrast-by-vibes

**Detect:** gray-on-gray secondary text, white text on brand pastels, disabled-looking active controls.
**Fix:** WC16/WC17 tokens; check rendered pairs including hover/dark-mode variants.

## Color-only signaling

**Detect:** red/green as the sole status channel; links distinguished only by color in prose; required fields marked only red.
**Fix:** WC18 — add text, icons, patterns, underlines.

## Modal jail / modal amnesia

**Detect:** modals that Tab escapes into the page behind (amnesia) or that Escape can't close and focus can't leave properly (jail); focus not restored on close.
**Fix:** the modal gauntlet (heuristics); native `dialog` + `showModal()` gets most of it free. (WC11, WC15)

## Toast-only errors

**Detect:** validation/async errors as transient toasts, unannounced, unassociated with fields.
**Fix:** WC29, WC31 — persistent, located, announced, focus-managed.

## Keyboard-second custom widgets

**Detect:** shiny custom select/datepicker/slider that mouse-works but arrow keys do nothing.
**Fix:** APG keyboard map or a maintained accessible library; the keyboard walk in review catches these. (WC10)

## Zoom-hostile layouts

**Detect:** fixed-height containers clipping 200% text; horizontal scroll at 320px; "please use desktop".
**Fix:** WC19/WC20; same work as responsive design done right.

## The a11y-overlay bandage

**Detect:** third-party "accessibility widget" script promising instant conformance.
**Cost:** doesn't fix the tree; frequently interferes with real AT; legally unpersuasive.
**Fix:** fix the product. There is no CSS class for conformance.

## Motion maximalism

**Detect:** parallax, auto-playing carousels, scroll-jacking, entrance animations everywhere; no `prefers-reduced-motion` handling.
**Fix:** WC22, WC32; motion serves comprehension or gets a kill-switch.

## Audit theater

**Detect:** "we ran Lighthouse, score 100, we're accessible."
**Cost:** scanners see ~a third; keyboard flows, alt quality, and announcements unexamined.
**Fix:** WC36 as entry ticket; the three walks as the audit.
