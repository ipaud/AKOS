# Engineering Rules — Responsive Web Pack

Checkable in the artifact. A reviewer verifies each against the code and the rendered page at the tested widths; violations are findings. Touch-target sizing, gesture, and keyboard-avoidance rules live in [touch-ergonomics](../touch-ergonomics/engineering-rules.md).

## Viewport and the 320 floor

- RWE1. The viewport meta is `width=device-width, initial-scale=1` — plus `viewport-fit=cover` when the layout reaches a screen edge.
- RWE2. Zoom is never suppressed: no `user-scalable=no`, no `maximum-scale` below 5. (Safety floor — WCAG 1.4.4.)
- RWE3. At a 320px viewport, `document.documentElement.scrollWidth <= document.documentElement.clientWidth`. Assert this in an automated test at every tested width.
- RWE4. `overflow-x: hidden` never appears on `html` or `body`. It suppresses the symptom, hides the overflowing element, and can break `position: sticky` descendants.
- RWE5. No element in normal flow declares a fixed `width` or `min-width` greater than 320px. Fixed widths belong to exempt scroll regions only (RWE16).
- RWE6. Flex and grid children that contain text or scroll regions set `min-width: 0` (or `min-inline-size: 0`); the default `auto` minimum size is the most common cause of unexplained page overflow.
- RWE7. Long unbroken strings — URLs, IDs, hashes, filenames — are constrained with `overflow-wrap: anywhere` or an explicit truncation with the full value reachable.
- RWE8. Every surface is fully operable at 320px: no capability is unreachable, no control is clipped, no dialog exceeds the viewport without an internal scroll region.

## Breakpoints

- RWE9. Breakpoints are declared once as named tokens and referenced everywhere; no ad-hoc pixel values scattered through components.
- RWE10. Breakpoint names describe the layout change, not a device (`--bp-two-column`, not `--bp-ipad`).
- RWE11. A surface uses at most 5 page-level breakpoints. More than that is a signal that fluid sizing is missing (RWE20).
- RWE12. Media queries use `min-width` and build upward; a `max-width` query is allowed only for genuinely wide-only behaviour and is annotated with why.
- RWE13. Breakpoint values are expressed in `em`/`rem` so they respond to the user's font size, not only to device width.
- RWE14. No layout gap between breakpoints: every width from 320 upward matches exactly one arrangement, with no range where two rules conflict or none applies.

## Horizontal overflow and scroll regions

- RWE15. Sideways scrolling exists only inside a bounded region and only for content destroyed by wrapping: data tables, code blocks, diagrams, media of intrinsic aspect. Prose, forms, cards, and navigation never qualify.
- RWE16. Every horizontal scroll region is keyboard-operable: `tabindex="0"`, `role="region"`, and an accessible name (`aria-label` or `aria-labelledby`). A scrollable box no keyboard user can scroll is an accessibility failure, not a layout choice.
- RWE17. Every horizontal scroll region pins its identifying column with `position: sticky; left: 0` (or `inset-inline-start: 0`), an opaque background, and a `z-index` above the scrolled cells. Sticky headers pin with `top: 0` on the same element where applicable.
- RWE18. Scrollability is visible without interaction: an edge shadow, a partially visible next column, or an explicit affordance. Never rely on a scrollbar that the platform hides.
- RWE19. No interactive control (input, select, checkbox, button) sits inside the scrolled area of a region whose identity column is not pinned. If pinning is not possible, the component must restructure (RWE23).

## Fluid type and spacing

- RWE20. Type and spacing steps are fluid across the range: `clamp(min, preferred, max)` per step, defined once as tokens.
- RWE21. Every fluid font-size includes a `rem`-relative term in its preferred value — `clamp(1rem, 0.92rem + 0.4vw, 1.25rem)`, never a viewport-unit-only preferred value, which stops responding to zoom and text resize. (Safety floor — WCAG 1.4.4.)
- RWE22. The ratio between a fluid value's min and max does not exceed 2×; larger swings need a breakpoint, not a steeper slope.
- RWE23. Body-copy measure is constrained in `ch` (target 45–75); at 320px, the column is the viewport minus gutters, not a fixed width.
- RWE24. Base body text renders at ≥ 16px effective at every width; no breakpoint reduces body copy below it.
- RWE25. Section and component spacing is fluid, so vertical rhythm compresses on small screens instead of leaving a 96px gap on a phone.

## Container queries and component adaptation

- RWE26. Any component that can appear in more than one layout context adapts via `@container`, not `@media`. The wrapper declares `container-type: inline-size` and a `container-name`.
- RWE27. Media queries inside reusable components are limited to environmental features — `prefers-reduced-motion`, `prefers-color-scheme`, `pointer`, `hover`, `print`. Width-based media queries inside a reusable component are findings.
- RWE28. Container-relative sizing inside a container uses `cqi`/`cqw` rather than `vw`, so the component scales with its box.
- RWE29. Container query thresholds are named per component in terms of what changes ("below this, the card stacks"), and documented alongside the component.
- RWE30. A container-query fallback exists where the component must render acceptably without support: the stacked (narrow) layout is the default, and the wide layout is the enhancement.

## Restructure thresholds

- RWE31. Any table whose cells contain interactive controls, and whose natural width exceeds the narrowest supported viewport, restructures below the breakpoint at which its identity column can no longer stay pinned alongside at least one data column. Stacked per-record cards or rows — not a scroll container.
- RWE32. Restructured views preserve every capability of the wide view: the same fields are editable, the same actions available, the same validation shown.
- RWE33. `display: none` conditional on a breakpoint is accompanied in the same change by either the alternative route to that capability at that width, or a code comment recording the deliberate desktop-only decision. Unannotated instances are findings.
- RWE34. Content order in the DOM matches the intended reading order at the narrowest width; `order`, `row-reverse`, and grid placement never produce a focus order that contradicts the visual order. (Safety floor — WCAG 1.3.2, 2.4.3.)
- RWE35. Truncation is used only where the full value is reachable (expansion, detail view, title on a non-hover-dependent surface) and never for money, dates, identifiers, or names on a surface where the user makes a decision.

## Viewport units, full-height layouts, safe areas

- RWE36. `100vh` is not used for any container holding an interactive element that must remain reachable; use `dvh` for panes that reflow with browser chrome and `svh` where content must never be clipped.
- RWE37. Dialogs, sheets, and drawers cap their height (e.g. `max-height: calc(100dvh - 2rem)`), scroll internally, and set `overscroll-behavior: contain` so the page behind does not scroll when the pane reaches its end.
- RWE38. Any full-height scrollable pane keeps its primary action reachable without relying on the browser chrome being collapsed.
- RWE39. Layouts that reach a screen edge pad against `env(safe-area-inset-*)` — bottom bars, fixed footers, full-bleed headers, and side-anchored drawers — with `viewport-fit=cover` set (RWE1).
- RWE40. Fixed or sticky bars are sized so that their combined height leaves the content area usable at 320×568; overlapping bars are collapsed, not stacked.

## Chrome and density budget

- RWE41. At 320px, primary content begins above the fold: chrome above it occupies no more than ~25% of viewport height.
- RWE42. At 320px, a page header renders in at most 2 rows. A header that wraps to 3+ rows is a finding against the action cluster, not against the CSS.
- RWE43. More than two primary actions in one cluster collapse into an overflow menu or a sticky action bar at narrow widths rather than wrapping.
- RWE44. Per-record density is defined per size: the fields shown at 320px are chosen by importance and listed, not produced by whatever survived truncation.
- RWE45. Interactive elements do not rely on `:hover` to reveal meaning or actions at any width; row actions are visible or reachable via an explicit control. (See [touch-ergonomics](../touch-ergonomics/engineering-rules.md).)

## Responsive images and media

- RWE46. Every `<img>` declares intrinsic `width` and `height` attributes (or the container declares `aspect-ratio`), and `max-width: 100%; height: auto` in CSS. (Protects CLS — see [core-web-vitals](../../performance/core-web-vitals/engineering-rules.md).)
- RWE47. Resolution switching uses `srcset` with `w` descriptors plus a `sizes` attribute whose values match the real CSS layout width at each breakpoint. A `sizes` value that disagrees with the layout ships the wrong file at every width.
- RWE48. Art direction — a different crop, aspect ratio, or subject framing per size — uses `<picture>` with `<source media="…">`, never CSS `background-image` swaps that lose the alt text and the preload scanner.
- RWE49. The largest above-the-fold image is eager with `fetchpriority="high"`; everything below the fold is `loading="lazy"`. Never lazy-load the LCP element.
- RWE50. Videos, iframes, embeds, and ad slots reserve their space with `aspect-ratio` or an explicitly sized container before they load.

## Testing

- RWE51. Every surface is exercised at 320 / 375 / 768 / 1024 / 1440 CSS px, and at least one primary task is *completed* (not observed) at 320.
- RWE52. Automated checks assert, at each tested width: no document-level horizontal overflow (RWE3), no element extending beyond the viewport's inline box, and — for surfaces with editable rows — that the identity element is in the viewport while a row control has focus.
