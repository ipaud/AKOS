# Decision Framework — Responsive Web Pack

Decision rules for adaptation calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## The ladder: how far up do we climb?

Adaptation options, cheap to expensive. Stop at the first rung that preserves every read-while-acting pair and every capability:

1. **Rescale** — fluid type and spacing. Never sufficient alone.
2. **Reflow** — stack columns, drop the sidebar, reduce grid tracks.
3. **Recompose** — toolbar → menu, nav → drawer, filters → single control.
4. **Restructure** — different component, same data: table → per-record cards, wide form → stepper.
5. **Re-scope** — a different, smaller task at this size, with the full task explicitly available elsewhere.

**Rule:** record the rung you stopped at and why. "It scrolls sideways now" is not a rung — it is the absence of one. Rung 5 requires a written decision, because it is a product choice, not a layout choice.

## Reflow or restructure?

| Signal | Verdict |
|--------|---------|
| Content is read-only and stacking keeps each value with its label | Reflow |
| Cells contain inputs, toggles, or per-row actions | Restructure (assume this until disproven) |
| The identity column plus one data column fit together at the narrowest width | Reflow or gated scroll |
| The identity column cannot stay pinned alongside any data column | Restructure |
| Users compare *across* rows | Gated scroll with pinned identity — comparison needs the tabular form |
| Users act on *one* record at a time | Restructure to cards; the table shape was never the point |
| Values are money, dates, or identifiers the user decides on | Restructure; never truncate, never unanchor |
| Content is code, a diagram, or media of intrinsic aspect | Scroll — there is no row identity to lose |

When two signals conflict, interactivity wins. An editable surface that scrolls sideways is the defect this pack exists to prevent.

## The horizontal-scroll gate

Before adding `overflow-x`, all five must be true. Any failure sends you up the ladder instead.

1. **Exempt content type** — data table, code block, diagram, intrinsic-aspect media. Prose, forms, cards, and navigation never qualify.
2. **Region, not document** — the scroll is bounded inside a container; the page itself never scrolls horizontally at any width.
3. **Identity pinned** — the row's identifying column is sticky, opaque, and above the scrolled cells.
4. **Keyboard-operable and named** — `tabindex="0"`, `role="region"`, accessible name.
5. **No unanchored controls** — nothing interactive inside the scrolled area depends on a column that scrolls away.

Record which exemption was claimed in the code, next to the container. The next person changing that table needs the conditions, not just the class name.

## Media query or container query?

| The question you're answering | Tool |
|-------------------------------|------|
| How is the *page* composed at this width? | Media query |
| How much room does *this component* have? | Container query |
| Is this element in a sidebar, a modal, or the main column? | Container query — always |
| Does the device support hover / what pointer is it? | Media query (`hover`, `pointer`) |
| Reduced motion, colour scheme, contrast, print? | Media query (preference features) |
| Is the whole app in its compact navigation mode? | Media query — genuinely global |

**Default:** if the component could ever be placed somewhere else, it is a container query. A width-based media query inside a reusable component is a bet on placement that the component cannot verify.

## Where to put a breakpoint

Resize continuously and stop at the first width where the layout is *wrong* — a column too narrow to read, cards shaped like ribbons, a nav on two lines, a table whose identity column is about to lose its neighbour. Put the breakpoint there, name it after the change, express it in `em`.

Reject a proposed breakpoint if: it matches a device model rather than a symptom; it duplicates an existing one within ~4rem; or it exists to nudge a size that should be fluid. Past four or five page-level breakpoints, the fix is fluid tokens, not another query.

## Which viewport unit

| Requirement | Unit |
|-------------|------|
| Must never be clipped when browser chrome is visible | `svh` |
| A pane that should reflow as chrome collapses and returns | `dvh` |
| Deliberately fills the tallest state, clipping accepted | `lvh` |
| Anything containing a control that must stay reachable | not `vh` — `dvh` with an internal scroll region |
| Sizing relative to the component's own box | `cqi` / `cqw` |

**Default for panes, dialogs, and drawers:** `max-height: calc(100dvh - 2rem)`, internal scroll, `overscroll-behavior: contain`. This is the pattern to copy.

## Hide, collapse, or restructure

When something doesn't fit:

- **Collapse** — same capability, fewer pixels: overflow menu, accordion, expandable row, disclosure. First choice.
- **Restructure** — different presentation, same capability. Second choice.
- **Hide** — only when the capability is genuinely reachable another way at that width, or the surface is deliberately desktop-only. Requires an annotation in the same change.
- **Never** — hide because it didn't fit and nobody noticed. That is an unrecorded feature cut.

## Fluid or stepped

Fluid when the correct value varies smoothly with available space: type sizes, gaps, section padding, measure, image sizing. Stepped when the correct answer changes in kind: number of columns, nav pattern, table vs cards, drawer vs sidebar.

Two smells: a `clamp()` being tuned to stop a layout from breaking (needs a breakpoint), and a fifth breakpoint added to nudge a font size (needs fluid tokens).

## Priority when constraints collide

1. **Safety floor** — 320px operability, no 2D scrolling, zoom not suppressed, focus order matching visual order. Never traded.
2. **Read-while-acting pairs** — correctness on decision surfaces.
3. **Capability parity** — every task doable at every supported width.
4. **Layout stability** — reserved space for async content.
5. **Consistency with existing patterns** — genuinely valuable, and the first thing to give way when the case differs in kind.
6. **Visual polish** — last.

Consistency sitting below correctness is the point: "it matches our other tables" is an argument about rank 5 being used to overrule rank 2.

## When desktop-only is a legitimate answer

Rarely, and never by default. It requires: a named user population and context (an operations console used on a fixed workstation), a recorded decision with a date, and a graceful narrow-width state that *explains* rather than breaks — not a 2000px layout squeezed into a phone. Article 9 makes this a decision to record, not an assumption to inherit.
