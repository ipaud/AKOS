# Anti-Patterns — Responsive Web Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers defects that make a surface *wrong* rather than merely awkward — they cost users correctness, not comfort.

## Blind editing

**Detect:** an editable table or wide form inside a horizontal scroll container with no pinned identity column. Found by focusing a control at 320px and checking whether the row's label is still on screen — never by looking at the page.
**Why it fails:** reaching the control is what removes the label. The user types a value into an unlabelled cell and confirms it, which on a money, quantity, or scheduling surface is a data-integrity defect, not a layout complaint. It is also invisible in static screenshots, so it survives review.
**Fix:** pin the identity column (`position: sticky; left: 0`, opaque background, `z-index`). If pinning plus one data column won't fit at the narrowest width, restructure into per-record cards. Never leave inputs in an unanchored scroll region.

## Precedent laundering

**Detect:** a diff justified as "consistent with our other tables" where this instance differs in kind — wider, or editable where the others were read-only, or carrying decisions where the others carried display.
**Why it fails:** precedent compresses reasoning, and reuse without decompressing it discards the conditions that made the pattern acceptable. Every reviewer nods at the consistency argument, so the check that would have caught it never runs.
**Fix:** restate the preconditions of the pattern and test each against the new case. Read-only → editable, and near-viewport-width → much wider, are both differences in kind that void the exemption. Record the conditions next to the pattern.

## Overflow-auto as an answer

**Detect:** `overflow-x: auto` (or a utility class equivalent) added to make an element "fit", with no sticky column, no focusable region, no affordance, and no note about why the content qualifies for the exemption.
**Why it fails:** it converts a layout problem into a navigation problem and calls it solved. Keyboard users often can't scroll the region at all; touch users don't know it scrolls; everyone loses the row relationships.
**Fix:** treat every new `overflow-x` as a reviewable event that must pass the scroll gate — exempt content type, pinned identity, focusable labelled region, visible affordance, no unanchored controls. Otherwise climb to restructure.

## Overflow suppression

**Detect:** `overflow-x: hidden` on `html` or `body`, usually added the day a mysterious horizontal scrollbar appeared.
**Why it fails:** it hides the evidence rather than the cause. The offending element is still there, off-screen and unreachable; the page can no longer be zoomed usefully; and `position: sticky` descendants can silently stop working.
**Fix:** find the overflowing element (binary-search by outlining children, or assert `scrollWidth > clientWidth` per node). It is almost always a missing `min-width: 0` on a flex/grid child, a fixed pixel width, or an unbroken string.

## The device-name breakpoint

**Detect:** breakpoints named or valued after hardware — `$iphone`, `$ipad`, `768px because iPad`.
**Why it fails:** it ties the CSS to a device census that changes yearly, and it encodes the assumption that width implies context. The layout ends up correct on the four devices someone had in 2019 and wrong in the gaps.
**Fix:** resize until the layout breaks, put the breakpoint there, and name it after the change (`--bp-two-column`). Express it in `em` so user font size participates.

## The breakpoint cliff

**Detect:** a design that looks composed at exactly 375, 768, and 1440, and stretched or cramped everywhere between. Usually accompanied by fixed pixel type and spacing.
**Why it fails:** users' viewports are continuous. Most sessions happen at a width nobody designed for.
**Fix:** fluid type and spacing tokens with `clamp()` handling the continuum; breakpoints reserved for arrangement changes.

## Clamp without a rem term

**Detect:** `font-size: clamp(1rem, 2.5vw, 2rem)` — a preferred value made only of viewport units.
**Why it fails:** the value stops responding to the user's font-size preference and to zoom across most of its range, which fails the resize-text criterion. It looks fine to everyone who never changes their settings.
**Fix:** include a `rem`-relative term in the preferred value: `clamp(1rem, 0.92rem + 0.4vw, 1.25rem)`. Same visual result, and it scales with the user.

## Media queries inside a component

**Detect:** `@media (min-width: …)` inside a card, table, or widget that is used in more than one place.
**Why it fails:** the component is asking about the window when it needs to know about its box. It renders wide inside a 300px sidebar on a large monitor, and narrow inside a full-width panel on a small laptop — both wrong, both hard to attribute.
**Fix:** `container-type: inline-size` on the wrapper and `@container` inside. Keep media queries for page composition and for environment features (pointer, hover, preferences, print).

## The chrome avalanche

**Detect:** at 320px, a page header wrapping to three or four rows — title, breadcrumbs, filter chips, and a cluster of buttons each taking a line — with the actual content below the fold.
**Why it fails:** every action was primary at desktop width, so nothing was ranked, and wrapping made the ranking decision by string length. The user scrolls before seeing what they came for, on the device with the least screen to spare.
**Fix:** rank the actions. Two primaries stay; the rest go into an overflow menu or a sticky action bar. Filters collapse into one control with an active count.

## Display-none as responsive design

**Detect:** breakpoint-conditional `display: none` (or `hidden md:block`) with no alternative route and no comment.
**Why it fails:** it deletes capability for everyone at that width. It reads as a layout tweak in a diff and lands as a missing feature in production — and the users who lost it are the ones least able to switch devices.
**Fix:** provide the capability another way at that width (menu, detail view, expandable row), or record an explicit decision that it is desktop-only. Reviewers treat unannotated instances as missing features.

## The 100vh trap

**Detect:** `height: 100vh` or `min-height: 100vh` on anything containing a control; a dialog, drawer, or full-screen pane sized in `vh`.
**Why it fails:** on phones the visible area shrinks when browser chrome returns and when the keyboard opens, so the bottom of a `100vh` box — usually where the confirm button lives — ends up under the chrome or off-screen entirely.
**Fix:** `dvh` for panes that should reflow with chrome, `svh` where content must never be clipped, an internal scroll region with `overscroll-behavior: contain`, and never a control pinned to the exact computed bottom.

## Notch blindness

**Detect:** full-bleed headers, bottom bars, or side drawers with no `env(safe-area-inset-*)` padding — or with the padding present but `viewport-fit=cover` missing, which silently zeroes the insets.
**Why it fails:** content lands under the notch, the home indicator, or a rounded corner. The affected controls are usually the persistent ones, so the damage is on every screen.
**Fix:** `viewport-fit=cover` plus inset-aware padding on every edge-anchored surface; verify on a device or an emulator with a cutout, since desktop browsers show nothing.

## Fixed-width islands

**Detect:** a stray `width: 480px`, a `min-width` on a table or dialog, an SVG with hardcoded dimensions, a third-party embed with its own idea of width.
**Why it fails:** one element wider than the viewport gives the whole document a horizontal scrollbar, and the culprit is invisible because the visible layout looks fine.
**Fix:** `max-width: 100%` as the default posture for embedded content, `min-width: 0` on flex/grid children, and an automated assertion at 320 so the next one is caught the day it lands.

## Truncation as adaptation

**Detect:** ellipsized prices, dates, names, or IDs on a surface where the user acts on them; a design that "fits" because every string is cut.
**Why it fails:** ellipsis makes the editing decision based on string length rather than importance, and it removes exactly the distinguishing tail — the cents, the year, the surname, the last digits of an invoice number.
**Fix:** rank fields per size and cut the least important ones outright, put secondary detail behind disclosure, wrap or reformat where the value matters. Truncate only where the full value is reachable and nothing is decided on it.

## Squeeze, don't rethink

**Detect:** a narrow layout produced entirely by scaling: smaller type, tighter padding, the same eleven columns, the same six toolbar buttons.
**Why it fails:** nothing was prioritized, so the small screen carries the full desktop information load at reduced legibility. It passes a screenshot review and fails the first real task.
**Fix:** decide what this screen is *for* at this width, then build that. The reflow/restructure ladder exists to make the climb explicit.

## The scroll trap

**Detect:** a nested scrollable pane — dialog body, drawer, map, inner list — without `overscroll-behavior: contain`.
**Why it fails:** reaching the end of the inner scroll hands the gesture to the page behind, which scrolls away underneath the open pane. On touch it feels like the interface lost the user's place.
**Fix:** `overscroll-behavior: contain` on every nested scroll region; `none` where the pane must also suppress pull-to-refresh.

## Zoom hostility

**Detect:** `user-scalable=no`, `maximum-scale=1`, or a layout that becomes unusable at 200–400% zoom.
**Why it fails:** it removes the primary adaptation mechanism for low-vision users, and it is the same failure as a broken 320px layout viewed from the other direction. (Safety floor.)
**Fix:** remove the restriction; fix the 320px layout, which fixes the zoom path at the same time.

## Unreserved media

**Detect:** images without `width`/`height` or `aspect-ratio`; embeds and ad slots that size themselves on arrival.
**Why it fails:** the page reflows when the bytes land, and the shift is proportionally largest on narrow screens where the image occupies most of the column. Users tap the wrong thing because the target moved.
**Fix:** declare dimensions or reserve the box for every asynchronous visual, and keep `sizes` in agreement with the real CSS layout width.

## The untested middle

**Detect:** a test matrix of "mobile" and "desktop"; no evidence anyone opened 768 or 1100.
**Why it fails:** the tablet range is where two-column layouts are most fragile and where nav patterns are most likely to be caught mid-transition.
**Fix:** 320 / 375 / 768 / 1024 / 1440 for every surface, with at least one task completed at 320 rather than observed.
