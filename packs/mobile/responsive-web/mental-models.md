# Mental Models — Responsive Web Pack

Named models this pack contributes. Use them as diagnostic lenses while building and reviewing.

## The read-while-acting pair

For every control, name the value the user must read *while operating it* — the row's identity, the unit, the running total, the field it belongs to. That value and that control form a pair, and the pair must be co-visible at every supported width. Vertical scroll preserves pairs; horizontal scroll destroys them, because reaching the control is what moves the label away.

This is the pack's central check and the one that catches the expensive defects. A price input whose product name has panned off-screen is not "slightly awkward on mobile" — the user is editing an unlabelled number on a money surface.

**Diagnostic:** at 320px, put the caret in the control. Screenshot. Is the identifying value in the shot? If not, it is a finding regardless of how the layout got there.

## The reflow → restructure ladder

Adaptation has rungs, in increasing order of how much the component changes:

1. **Rescale** — same layout, fluid sizes. Free, and never sufficient on its own.
2. **Reflow** — same components, rearranged: columns stack, a sidebar drops below, a grid loses tracks. The default.
3. **Recompose** — same information, different arrangement of the same parts: a toolbar collapses into a menu, a nav becomes a drawer.
4. **Restructure** — a genuinely different component presenting the same data: a table becomes a list of per-record cards; a multi-column form becomes a stepper.
5. **Re-scope** — a different task at this size, with an explicit, recorded decision that the full task lives elsewhere.

The rungs are cheap-to-expensive, so teams stop climbing too early. The signal to climb past reflow is that reflow has stopped preserving pairs: if stacking cannot keep the identity next to the control, rearranging is not the answer — replacing the component is.

**Diagnostic:** name the rung the design stopped at, and the reason. "We reflowed" is only an answer if nothing was left behind.

## The 320 floor

320 CSS pixels is not the smallest phone; it is the width at which a 1280px-wide desktop page must remain fully usable when a low-vision user zooms to 400%. It is therefore a floor for two constituencies at once, and one design effort serves both.

Treat it as a hard boundary, not an aspiration: everything a user can do at 1440 they can do at 320, in some form, without two-dimensional scrolling. The exemptions are narrow and listed (see the scroll gate below).

**Diagnostic:** `document.documentElement.scrollWidth <= document.documentElement.clientWidth` at a 320px viewport. A page-level horizontal scrollbar at 320 is a defect with no acceptable justification — the exemptions apply to *regions*, never to the document.

## The container is the world

A component's environment is the box it was placed in. Its width comes from its parent, not from the device, and a component that reads the viewport is answering a question nobody asked it.

| Question | Right tool |
|----------|-----------|
| How should the *page* be composed? | Media query |
| How much room does *this component* have? | Container query |
| Is this a touch device / does it support hover? | Media query (interaction features) |
| Does the user prefer reduced motion / dark? | Media query (preference features) |
| Should this card be horizontal or stacked? | Container query — always |

**Diagnostic:** for every media query inside a reusable component, ask what it would do if the component were dropped into a 300px sidebar on a 1440px monitor. If the answer is wrong, it was a container query.

## The horizontal-scroll gate

Sideways scrolling is permitted only for content whose meaning is destroyed by wrapping — essentially: data tables, code blocks, and rendered diagrams or media of intrinsic aspect. It is permitted at the **region** level only, never the document, and only when all four conditions hold:

1. The row's identifying column is pinned (`position: sticky`) so pairs survive the scroll.
2. The scroll container is keyboard-operable: focusable, labelled, and announced as a region.
3. The scroll is discoverable — an edge shadow, a partial column, or explicit affordance.
4. No cell inside the scrolled area is an interactive control whose identity depends on an unpinned column.

Condition 4 is the one teams miss, and it is usually the one that converts an acceptable pattern into a defect. Fail any condition, and the answer is not "add a scrollbar" — it is climb the ladder to restructure.

## Chrome budget

Header, toolbars, filters, breadcrumbs, and action clusters are chrome; the thing the user came for is content. Chrome is written at desktop widths where it costs a strip, and it is measured in *rows* at 320 where it costs the fold. A four-row header on a phone means the user scrolls before seeing anything.

Budget it explicitly: at 320px, chrome above the primary content gets a bounded share of the viewport height, and clusters of primary actions collapse rather than wrap. Wrapping is not adaptation — it is the absence of a decision about which action is primary.

**Diagnostic:** at 320px, is any content visible before the first scroll? Count the header's rendered rows.

## Precedent's conditions

Every reused pattern carries invisible preconditions. Before applying one, restate the conditions under which it was accepted and check each against the new case. The recurring shape:

| Precedent | Silent condition | Where it breaks |
|-----------|-----------------|-----------------|
| "Tables scroll sideways here" | those tables were read-only and near-viewport-width | a wider table whose cells are inputs |
| "We hide this column on mobile" | the value was decorative | the value is now the identifier |
| "Dialogs are full-height" | content was short | content grew past the viewport |
| "Cards stack at `md`" | cards were placed full-width | a card now lives in a sidebar |

**Diagnostic:** when a review comment says "consistent with the rest of the app", ask which conditions made the rest of the app correct, and whether this instance has them. A *difference in kind* — read-only becoming editable, display becoming decision — voids the precedent entirely.

## The unreliable viewport

The visible area is a range, not a number. Browser chrome collapses on scroll; the keyboard steals height; notches and home indicators carve out corners that are inside the layout rectangle but outside the safe one.

- `lvh` — largest: the viewport with chrome hidden. Content sized to it is clipped when chrome returns.
- `svh` — smallest: safe for anything that must never be cut off.
- `dvh` — dynamic: tracks the current value; correct for scrollable panes, and it reflows as chrome moves.
- `env(safe-area-inset-*)` — the corners; needs `viewport-fit=cover` to be non-zero.

**Diagnostic:** for each full-height element, ask "what happens the moment browser chrome reappears?" Anything that answers "the button is under the address bar" is using the wrong unit.

## Fluid between, decided at

Breakpoints and fluid sizing solve different halves of the same problem. Fluid values (`clamp()`) handle the continuum *between* breakpoints so the design never looks stretched at 1100px or cramped at 700px. Breakpoints handle the discontinuities — the moments where the right answer is a different arrangement, not a different number.

Reaching for one where the other belongs produces the two classic failures: a design that only looks correct at five exact widths, or a design that never restructures because someone hoped `clamp()` would do it.

## Density is a variable

Information density — how much is shown per unit of space, and how strongly hierarchy is expressed — is a design choice that should differ by size, not a constant that survives by truncation. A wide screen can afford secondary metadata inline; a narrow one shows the two fields that drive the decision and puts the rest behind disclosure. The failure mode is inheriting desktop density and letting ellipsis do the editing, which lets the layout choose what to hide based on string length rather than importance.

**Diagnostic:** at 320, list what is shown per record and rank it by importance. If the ranking doesn't match what survived, ellipsis made the design decision.
