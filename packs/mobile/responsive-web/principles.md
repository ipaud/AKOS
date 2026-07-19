# Principles — Responsive Web Pack

Durable rules of responsive layout. Violating one requires an explicit tradeoff statement. Each principle carries an operational corollary — the thing you do differently tomorrow because the principle is true.

## RW1 — Mobile-first is a constraint order, not a stylesheet order

The narrow viewport is the only one that forces prioritization, so it is where prioritization must happen. Building wide-first turns every narrow-screen decision into a negotiation about what to remove from something that already exists, and features are never removed by the people who built them — they are hidden, shrunk, or pushed into a scroll container.

**Corollary:** the first working version of any surface is built and demoed at 320px. If the first artifact is a desktop layout, the narrow layout is a demotion negotiation and will be reviewed as one.

## RW2 — 320 CSS pixels is a floor, not an edge case

Every surface is fully operable at 320px wide. This is simultaneously the small-phone width and the width a 1280px desktop page occupies at 400% zoom, so one design effort serves small screens and low-vision users at once. "Nobody uses a phone that small" misreads what the number is for.

**Corollary:** 320px enters the definition of done and the test matrix. A page-level horizontal scrollbar at 320 is a blocking defect, with no product-side exemption available.

## RW3 — Two-dimensional scrolling is a defect

Content must not require scrolling in both axes to be read or operated (WCAG SC 1.4.10). Vertical scroll preserves the horizontal relationship between a thing and its label; horizontal scroll destroys it, and destroys it exactly while the user is reading along a row.

**Corollary:** `overflow-x` is a reviewable event. Adding it requires naming the exempt content type and satisfying the scroll gate (RW7); adding it to `body` is never a fix, only a way to hide the element that overflowed.

## RW4 — Breakpoints come from the content, not from a device census

A breakpoint belongs where the layout stops working — where a column gets too narrow to read, where cards start looking like ribbons, where a nav no longer fits on one line. Naming breakpoints after hardware ties the CSS to a device population that changes every year and encodes an assumption that phone width and phone context are the same thing.

**Corollary:** breakpoint names describe the layout change (`--bp-two-column`, `--bp-nav-inline`), never a device. Adding a breakpoint requires stating the content symptom that justified it.

## RW5 — A component's environment is its container

Component-level adaptation responds to the space the component was given, not to the viewport. A card is narrow because it sits in a sidebar; a table is cramped because a filter panel opened. Media queries inside reusable components encode a guess about placement that the component cannot verify.

**Corollary:** any component that can appear in more than one layout context adapts via container queries. Media queries are reserved for page composition and for environmental facts that genuinely are global — pointer type, hover capability, user preferences, print.

## RW6 — Adaptation is continuous between breakpoints and discrete at them

Type and space scale smoothly across the range so the design is correct at every width, not at five of them. Arrangement changes discretely, because "half stacked" is not a layout. Using either mechanism for the other's job produces the two classic failures: a design that only looks right at exact breakpoints, or a design that never restructures because someone hoped `clamp()` would handle it.

**Corollary:** every type and spacing step in the scale is fluid; every arrangement change is a breakpoint. If a `clamp()` is being tuned to fix a layout that breaks, the fix is a breakpoint.

## RW7 — Horizontal scroll is a region-level exemption with conditions attached

Some content is destroyed by wrapping: data tables, code, diagrams, media of intrinsic aspect. These may scroll sideways within their own region — never the document — and only when the row identity is pinned, the container is keyboard-operable and labelled, the scrollability is visible, and nothing inside the scrolled area is an interactive control whose meaning depends on an unpinned column.

**Corollary:** a scrollable region ships with its sticky identity column, `tabindex="0"`, an accessible name, and a visible edge affordance in the same change. Any of them missing means the exemption was not earned.

## RW8 — Anything the user must read while acting must be visible while they act

Controls and their identifying context form a pair. Reaching the control must never be what removes the label. A price field whose product name has panned off-screen, a quantity input whose unit is three columns away, a confirm button whose amount scrolled past — each is a correctness defect on a decision surface, not a comfort issue.

**Corollary:** for every interactive cell or field, name the value the user reads while operating it and verify co-visibility at 320px with the caret in the control. Failure here outranks visual polish and outranks consistency with existing screens.

## RW9 — Reflow has a limit; past it, restructure

Reflow rearranges the same components. Restructuring replaces them with a different presentation of the same data — a table becoming per-record cards, a multi-column form becoming a stepper. Interactivity is the usual trigger: a wide read-only table can often reflow or scroll, while a wide *editable* table generally cannot, because editing requires co-visibility that stacking columns cannot preserve.

**Corollary:** when a layout stops preserving read-while-acting pairs under reflow, stop tuning the reflow. Record which rung of the ladder the design stopped at and why; "we made it scroll" is not a rung.

## RW10 — Precedent transfers only with its conditions

Reused patterns carry silent preconditions. "Our tables scroll on mobile" was accepted for tables that were read-only and near-viewport width; the same treatment on a wider table full of inputs is a different decision wearing the same diff. A difference in kind — read-only becoming editable, display becoming decision — voids the precedent entirely.

**Corollary:** before applying an existing responsive pattern, restate the conditions that made it acceptable and check each against this case. Record them next to the pattern so the next person inherits the reasoning rather than the shortcut.

## RW11 — Adaptation may not delete capability

Hiding an element at a breakpoint removes that capability for every user at that width. This is sometimes correct — but only when the same capability is reachable another way at that size, and the decision is recorded. `display: none` chosen because something didn't fit is not a responsive technique; it is an unrecorded feature cut.

**Corollary:** every breakpoint-conditional `display: none` is accompanied by either the alternative route at that width or a written decision that the capability is intentionally desktop-only. Reviewers treat an unannotated one as a missing feature.

## RW12 — Chrome must not outgrow content

Headers, toolbars, filter bars, and action clusters are written at widths where they cost a strip and rendered at widths where they cost the fold. A header that wraps to four rows at 320px has pushed the actual product below the first screen, and wrapping happens precisely because no decision was made about which action is primary.

**Corollary:** at 320px, primary content is visible before the first scroll, and clusters of more than two primary actions collapse into a menu or a sticky bar rather than wrapping. Count the header's rendered rows in review.

## RW13 — Density is designed per size, not inherited and truncated

How much is shown per record, and how strongly hierarchy is expressed, are decisions that should differ across widths. When desktop density is inherited unchanged, ellipsis makes the editing decisions — hiding whatever happens to be long rather than whatever is least important.

**Corollary:** for each size, list what is shown per record in importance order, and check that the surviving fields match. Truncation is acceptable only where the full value is reachable and the value isn't load-bearing for a decision — never for money, dates, identifiers, or names on an action surface.

## RW14 — The viewport is a range, not a number

The visible area changes as browser chrome collapses and returns, as the keyboard opens, and as notches and home indicators carve out corners inside the layout rectangle. `100vh` encodes an assumption the platform stopped making, which is why the `dvh`/`svh`/`lvh` family exists.

**Corollary:** never place an interactive element at the exact bottom of a computed viewport height. Choose the unit by the failure you're preventing — `svh` for "must never be clipped", `dvh` for panes that reflow with chrome — and pad against safe-area insets wherever the layout reaches a screen edge.

## RW15 — Reserved space is part of responsive layout

Media that arrives without declared dimensions reflows the page around it on arrival, and the shift is worst on narrow screens where images are proportionally larger. Layout stability is not a separate performance concern bolted on afterwards; it is whether the layout was fully described before the bytes landed.

**Corollary:** every image, video, embed, and async-loaded block declares its space up front — intrinsic `width`/`height`, `aspect-ratio`, or a reserved container — and `sizes` matches the real CSS width so the chosen source is the one the layout actually uses.

## RW16 — Responsive behaviour is tested, not asserted

Nothing here is true until the layout has been opened at the widths where it changes and *driven*. Looking at a screenshot proves the page renders; completing the task proves the page works. Most responsive defects are invisible in a static capture because they only appear once a control is focused, a menu is opened, or a value is typed.

**Corollary:** 320 / 375 / 768 / 1024 / 1440 are exercised for every surface, and at least one primary task is completed at 320 rather than observed. Automate the cheap half — assert no document-level horizontal overflow at each width — and do the expensive half by hand.
