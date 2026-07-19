# Philosophy — Responsive Web

## Narrow first is a constraint order, not a starting width

"Mobile-first" is usually heard as an instruction about which stylesheet to write first. That reading is trivial and mostly harmless. The instruction that matters is about *when you are allowed to make decisions*: at 320 pixels there is room for one column, a handful of controls, and roughly one idea at a time, so every question about what actually matters has to be answered before anything else gets built. Widening the viewport afterwards is additive — more room, more simultaneity, more secondary detail — and additive work is easy.

Do it the other way and every narrow-screen decision becomes a negotiation about what to cut from something that already exists and already has stakeholders. Nobody cuts their own feature. So things get hidden, shrunk, ellipsized, or shoved into a horizontally scrolling box, and the layout technically renders at 320 while the interface no longer works there. Constraint order is the whole mechanism: the narrow case is the only viewport that forces prioritization, so it must be where prioritization happens.

## Squeezing is not adapting

There are two ways to make a wide layout fit a narrow screen. One is to decide what this screen is *for* at this size and build that. The other is to reduce everything proportionally until it fits — smaller type, tighter padding, truncated labels, a scroll container around the part that refused. The second one is cheap, produces a screenshot that looks fine in review, and is where almost all responsive defects live, because it never asks the question that would have caught them: at this width, what is the user actually doing, and what do they need in front of them while they do it?

Adaptation is editing. It changes what is shown, in what order, and sometimes in what form. Squeezing changes only the numbers.

## Layout is a promise about co-visibility

An interface makes an implicit claim: the things you need together are together. Scrolling breaks that claim in a specific, well-understood way vertically — users accept it, because vertical scroll preserves the horizontal relationships between a thing and its label. Horizontal scroll does not. It breaks rows apart, and it does so precisely at the moment a user is reading along one.

This is why sideways scrolling is not merely "less convenient" than reflowing, and why WCAG treats two-dimensional scrolling as a failure rather than a nuisance. When a row's identifying label leaves the screen while its editable cell remains, the interface has stopped answering the question "what am I changing?" — and it has stopped answering it at the exact instant the user commits. The most expensive responsive defects are all versions of this: the answer was on screen a second ago, and the act of reaching the control removed it.

## Components adapt to their container, not to the phone

For fifteen years the only signal available was the viewport, so components were written as though the viewport were their environment. It never was. A card is narrow because it sits in a sidebar, not because the visitor is on a phone; a table is cramped because a filter panel opened next to it. Media queries encode a guess about where a component will be placed, which means every component with a media query inside it is coupled to a layout it cannot see.

Container queries removed the excuse. The correct mental model is local: a component asks how much room *it* has and responds. Media queries remain right for exactly the thing they describe — page-level composition, and the environmental facts that genuinely are global. Everything else was always a container question wearing a viewport costume.

## The viewport is not a rectangle you can trust

`100vh` was designed as though the visible area were a fixed quantity. On phones it is not: browser chrome collapses and reappears as the user scrolls, the on-screen keyboard eats half the screen, a notch or a home indicator carves pieces out of the corners, and the safe rectangle is smaller than the layout rectangle. The `dvh`/`svh`/`lvh` family exists because the platform admitted there is no single answer — only "largest", "smallest", and "whatever it is right now".

The design consequence is a habit rather than a unit: never place a control at the exact bottom edge of a computed viewport height and assume it is reachable. Measure the constraint you actually mean.

## Precedent transfers only with its conditions

Teams converge on shared solutions — "our tables scroll horizontally on mobile, that's fine, we've done it five times". The precedent is usually real and usually was fine. What gets lost is the set of conditions under which it was fine: those tables were read-only, they were narrow enough that a row stayed mostly on screen, and being unable to see the label while scanning cost the user a glance rather than a mistake.

Change one of those conditions and the pattern inverts. A table whose cells are inputs is a different kind of object from a table that displays values, and the difference is invisible in a diff that only says "added `overflow-x-auto`, consistent with the other tables". Precedent is compressed reasoning; reusing it without decompressing it is how a team ships a defect that every individual reviewer would have caught.

## Testing is the only proof

Responsive behaviour is claimed constantly and verified rarely, because the developer's browser window is wide, the design file has three artboards, and the CI screenshot suite renders at one size. Nothing here is true until the layout has been opened at the widths where it changes and driven — not looked at. Opening a page at 320 shows you a screenshot; editing a value at 320 shows you the product.

## Where this philosophy stops

This lens is space and adaptation. Fingers, gestures, hover, and the virtual keyboard belong to [touch-ergonomics](../touch-ergonomics/philosophy.md); the normative accessibility floor belongs to [wcag](../../ux/wcag/philosophy.md). And nothing here overrides that floor: a layout that reflows beautifully but strands a control off-screen at 320 is a defect no matter how elegant the technique that produced it.
