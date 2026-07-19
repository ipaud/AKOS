# Review Checklist — Responsive Web Pack

Binary checks, ordered by severity. Used by [mobile-reviewer](../../../agents/mobile-reviewer.md). Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items and block in every reasoning profile ([constitution](../../../core/constitution.md) Articles 2 and 9).

Reviewing responsive behaviour means driving the page, not viewing it. The critical block requires a browser at 320px with something focused — a screenshot cannot produce most of these findings.

## Critical (blocks in every profile)

- [ ] ★ No document-level horizontal scrolling at 320px: `scrollWidth <= clientWidth`. (RWE3)
- [ ] ★ No content requires scrolling in both axes to be read or operated. (RW3, WCAG 1.4.10)
- [ ] ★ Zoom is not suppressed: no `user-scalable=no`, no `maximum-scale` below 5. (RWE2, WCAG 1.4.4)
- [ ] ★ Every value the user must read while operating a control is visible at 320px with that control focused. (RW8)
- [ ] ★ No interactive control sits inside a horizontal scroll region whose identity column is unpinned. (RWE19)
- [ ] ★ Every surface is fully operable at 320px — no clipped controls, no unreachable capability, no dialog exceeding the viewport without internal scroll. (RWE8)
- [ ] ★ Fluid font sizes include a `rem`-relative term; no viewport-unit-only preferred values. (RWE21, WCAG 1.4.4)
- [ ] ★ DOM order matches the intended reading order at the narrowest width; focus order does not contradict visual order. (RWE34, WCAG 1.3.2/2.4.3)
- [ ] Editable tables wider than the narrowest viewport restructure rather than scroll. (RWE31)
- [ ] `overflow-x: hidden` does not appear on `html` or `body`. (RWE4)

## High

- [ ] Every horizontal scroll region passes the full gate: exempt content type, pinned identity column, focusable and named container, visible scroll affordance. (RW7, RWE15–RWE18)
- [ ] Restructured narrow views preserve every capability of the wide view — same fields editable, same actions, same validation. (RWE32)
- [ ] Every breakpoint-conditional `display: none` has either an alternative route at that width or a recorded desktop-only decision. (RWE33)
- [ ] No fixed `width`/`min-width` above 320px on elements in normal flow. (RWE5)
- [ ] Flex and grid children containing text or scroll regions set `min-width: 0`. (RWE6)
- [ ] No `100vh`/`min-height: 100vh` on containers holding controls that must stay reachable. (RWE36)
- [ ] Dialogs, sheets, and drawers cap height in `dvh`/`svh`, scroll internally, and set `overscroll-behavior: contain`. (RWE37)
- [ ] Edge-anchored surfaces pad against `env(safe-area-inset-*)`, with `viewport-fit=cover` set. (RWE1, RWE39)
- [ ] At 320px, primary content begins above the fold and the page header renders in at most 2 rows. (RWE41, RWE42)
- [ ] Reusable components adapt via `@container`; no width-based media queries inside them. (RWE26, RWE27)
- [ ] Every image declares `width`/`height` or an `aspect-ratio`; embeds and ad slots reserve their space. (RWE46, RWE50)
- [ ] No truncation of money, dates, identifiers, or names on a surface where the user acts on them. (RWE35)
- [ ] The surface was exercised at 320 / 375 / 768 / 1024 / 1440, and one primary task was completed at 320. (RWE51)

## Medium

- [ ] Breakpoints are named tokens describing the layout change, not devices, and are declared once. (RWE9, RWE10)
- [ ] Breakpoint values use `em`/`rem`. (RWE13)
- [ ] At most 5 page-level breakpoints; no width range where two rules conflict or none applies. (RWE11, RWE14)
- [ ] Media queries build upward with `min-width`; any `max-width` query is annotated. (RWE12)
- [ ] Type and spacing steps are fluid tokens defined once, not per-component `clamp()` calls. (RWE20)
- [ ] No fluid value swings more than 2× between its min and max. (RWE22)
- [ ] Body-copy measure is constrained in `ch` (45–75 target). (RWE23)
- [ ] Body text is ≥ 16px effective at every width; no breakpoint reduces it. (RWE24)
- [ ] Section spacing compresses on narrow screens. (RWE25)
- [ ] Container-relative sizing uses `cqi`/`cqw` rather than `vw` inside containers. (RWE28)
- [ ] The stacked layout is the default and the wide layout the enhancement, where container-query support matters. (RWE30)
- [ ] More than two primary actions in a cluster collapse into a menu or sticky bar rather than wrapping. (RWE43)
- [ ] Per-record fields shown at 320px were chosen by importance and listed, not produced by truncation. (RWE44)
- [ ] `srcset` + `sizes` match the real CSS layout width at each breakpoint. (RWE47)
- [ ] Art direction uses `<picture>` with `media`, not CSS background swaps. (RWE48)
- [ ] The LCP image is eager with `fetchpriority="high"`; below-fold media is lazy. (RWE49)
- [ ] Long unbroken strings are wrapped or truncated with the full value reachable. (RWE7)
- [ ] No meaning or action depends on `:hover` at any width. (RWE45, and [touch-ergonomics](../touch-ergonomics/review-checklist.md))

## Low

- [ ] Container query thresholds are documented per component in terms of what changes. (RWE29)
- [ ] Fixed and sticky bars leave a usable content area at 320×568; overlapping bars are collapsed, not stacked. (RWE40)
- [ ] Full-height scrollable panes keep their primary action reachable without relying on collapsed browser chrome. (RWE38)
- [ ] Vertical rhythm and gutters are intentional at 320, not inherited desktop values. (RW13)

## Process

- [ ] Automated checks assert no document-level horizontal overflow at every tested width. (RWE52)
- [ ] Every new `overflow-x` in this diff names the exemption it claims, in the code. (RW7)
- [ ] Any responsive pattern reused from elsewhere had its preconditions restated and checked against this case — especially read-only → editable. (RW10)
- [ ] The rung of the reflow/restructure ladder this design stopped at is recorded, with the reason. (RW9)
- [ ] Tested with real worst-case content: longest label, largest number, longest translated string. (RW13)
