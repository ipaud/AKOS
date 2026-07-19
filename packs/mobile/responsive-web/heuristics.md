# Heuristics — Responsive Web Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Starting a layout

- **Build the 320 version first and demo it.** Whatever survives that width is the feature; everything else is enhancement. Exception: none worth the trouble — a wide-first build always costs the narrow one.
- **Default to one column, then earn the second.** A second column has to justify itself with a real relationship between the two, not with available space.
- **Let the grid decide the breakpoint.** `grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr))` handles most card layouts with no media query at all. Reach for explicit breakpoints when the arrangement changes in kind, not in count.
- **Gutters before widths.** Decide the page's inline padding first; at 320 it's what stands between the content and the bezel.
- **If it fits at 320 and 1440, check 700 and 1100.** The in-between widths are where "responsive" designs are ugliest, and nobody opens them.

## Breakpoints

- **Resize until it looks wrong; put the breakpoint there.** Then name it after what changed.
- **Three or four is usually enough.** Five is a lot. Seven means fluid sizing is missing.
- **Never name a breakpoint after a device.** Hardware changes annually; "two columns fit here" doesn't.
- **Build up with `min-width`.** Downward overrides accumulate into a specificity fight that nobody wins.
- **Use `em` for breakpoint values** so a user who bumps their base font size gets the simpler layout they need.

## Type and spacing

- **`clamp()` every step of the scale, once, as tokens.** Per-component `clamp()` calls drift within a release.
- **Keep a `rem` term in the preferred value.** `clamp(1rem, 0.92rem + 0.4vw, 1.25rem)`. A pure `vw` preferred value ignores zoom, which is an accessibility failure, not a taste issue.
- **Cap the swing at 2×.** If a heading wants to go from 24px to 96px, that's two ranges with a breakpoint between them.
- **Measure in `ch`, not pixels.** 45–75ch reads well at every size; a fixed `max-width` in px reads well at one.
- **Compress vertical rhythm on small screens.** A section gap that's beautiful at 1440 is a blank screen at 320.
- **Never shrink body text at a breakpoint.** Small screens need more legibility, not less — the thing to reduce is quantity.

## Wide content and tables

- **Ask whether it's read-only before allowing scroll.** Read-only and narrowish → scroll is often fine. Editable → assume restructure until proven otherwise.
- **Pin the identity column the moment a table scrolls.** `position: sticky; left: 0` with an opaque background and a `z-index`. A scrolling table without it is a table you can't read.
- **Make the scroll container focusable and labelled.** `tabindex="0"` + `role="region"` + a name. Otherwise keyboard users simply cannot reach the content.
- **Show that it scrolls.** An edge shadow or a sliced-off next column. Hidden scrollbars mean the affordance has to be visual.
- **Below the pin threshold, become cards.** When the identity column plus one data column no longer fit together, stacking per record beats any amount of scrolling.
- **Cards keep every capability.** Same fields editable, same actions, same validation. A read-only "mobile view" of an editable table is a feature cut wearing a layout costume.
- **Code and diagrams may scroll freely.** They have no row identity to lose — this is the clean case of the exemption.

## Chrome and actions

- **Count the header's rows at 320.** Three is a warning; four means the content is below the fold.
- **Two primary actions maximum in a cluster.** The third goes into an overflow menu, or the cluster becomes a sticky bar.
- **A sticky action bar beats a wrapping header** whenever actions apply to the whole screen — it keeps them reachable and stops them eating the top of the page.
- **Filters collapse into a single "Filters" control on narrow screens,** with the active count on it. A filter row is chrome, and chrome is what buries content.
- **Breadcrumbs truncate from the middle,** keeping the first and current items — the ends are the ones that orient.

## Viewport, height, and edges

- **`dvh` for panes, `svh` for "must not be clipped", `lvh` almost never.**
- **Cap dialogs and scroll them internally:** `max-height: calc(100dvh - 2rem)` with `overscroll-behavior: contain`. This is the pattern; the failure is a dialog that grows past the screen and takes its confirm button with it.
- **Never put a control at the exact bottom of a computed viewport height.** Chrome reappears and it's gone.
- **Pad against safe-area insets on anything touching an edge**, and remember they're zero until `viewport-fit=cover` is set.
- **Assume the keyboard eats half the screen.** Anything the user must see while typing has to survive that. (Details in [touch-ergonomics](../touch-ergonomics/heuristics.md).)

## Media

- **Dimensions before bytes.** `width`/`height` attributes or `aspect-ratio` on every image, video, iframe, and ad slot — otherwise the page jumps when the network lands, worst on the smallest screens.
- **`sizes` must describe the real layout.** Writing `sizes="100vw"` for an image that's half-width in a sidebar downloads twice the bytes at every breakpoint.
- **Crop change → `<picture>`; density change → `srcset`.** A 16:9 hero that should be 4:5 on a phone is art direction, not resolution switching.
- **Never lazy-load the LCP image.** Eager plus `fetchpriority="high"`; everything below the fold lazy.
- **Prefer CSS `object-fit` over ad-hoc crops** when the aspect changes but the subject framing doesn't.

## Density

- **Rank the fields, then cut from the bottom.** If you can't rank them, the screen has no hierarchy and truncation will invent one.
- **Two fields drive most decisions.** Show those; disclose the rest.
- **Never truncate money, dates, names, or IDs on an action surface.** Wrap, reformat, or restructure — losing the last three digits of a price is not a visual compromise.
- **Secondary metadata goes behind disclosure, not behind ellipsis.** Ellipsis hides the long thing, not the unimportant one.

## Testing

- **320 / 375 / 768 / 1024 / 1440, every surface, every time.**
- **Complete a task, don't observe a screenshot.** Focus a control, open the menu, type a value, submit. Most defects are invisible until something has focus.
- **Zoom a desktop page to 400% instead of resizing** when you want to confirm the 1.4.10 path — it's the same 320px target from the other direction and it catches different bugs.
- **Automate the boring assertion:** no document-level horizontal overflow at each width. It's three lines and it catches the `min-width: 0` class of bug forever.
- **Test with real content lengths.** The longest product name, the largest number, the German translation. Lorem ipsum never overflows.
