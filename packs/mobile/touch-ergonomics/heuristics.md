# Heuristics — Touch Ergonomics Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Sizing

- **Design to 44, defend at 24.** 44×44 (or 48 on Material) is the number you build to. 24 is the number you cite when explaining why a legacy dense table isn't blocking release — and it comes with a spacing obligation, not a free pass.
- **Size the target, not the icon.** A 16px glyph in a 44px box is correct. A 44px glyph is a design decision you probably didn't want.
- **Padding beats overlays.** Growing the element's own box is visible in devtools, participates in layout, and can't silently overlap a sibling. Reach for a pseudo-element only when the layout truly can't absorb the size.
- **If you're adding an overlay, do the arithmetic first.** `gap ≥ F − (wA + wB)/2`. Two seconds of arithmetic prevents the class of bug where the delete button quietly annexes its neighbour.
- **Dense tables are the usual crime scene.** Row actions inherit desktop density from the first implementation and nobody re-measures. Audit every row-action cluster explicitly.
- **The close button is a real button.** It gets the floor too — often it's the only escape from the surface.

## Placement

- **Bottom third for the thing they'll do most.** If a screen has one obvious next action, it belongs where the thumb already rests.
- **Top-right corner is the worst pixel on a phone.** Nothing that matters lives there alone. Duplicate it or move it.
- **Never put delete next to save.** Adjacency plus imprecision plus commitment-on-contact is the whole recipe. Move the destructive action into an overflow, a second step, or a different region.
- **Walk the thumb path.** Trace from the resting position to the primary action. Every control crossed is a misfire candidate; a destructive one is a finding.
- **A long form needs the submit twice, or sticky.** An action that requires scrolling past a screenful of content to reach is an action that gets abandoned in the field.
- **Field-use screens are stricter.** Standing, one hand, gloves, sunlight: for these, the ergonomic target is the floor, not the goal.

## Hover and discoverability

- **If it appears on hover, it doesn't exist.** Row actions, edit pencils, drag handles, delete icons — all invisible on touch. Make them persistent on coarse pointers.
- **`title=` is not a UI.** It has never been reachable on touch and is inconsistent for keyboard and screen-reader users. If the content matters, it isn't a `title`.
- **Replace hover with one of three things:** visible text, an accessible name on an icon control, or a tap-to-open popover. Choose by whether the content is identity (name it), detail (disclose it), or decoration (delete it).
- **Warnings never live in tooltips.** If a user must act on it, it must be visible without a pointer. This is the version of the rule that costs money.

## Forms and the keyboard

- **Declare the keyboard on every field.** `type` for what it is, `inputmode` for what keys to show, `autocomplete` for autofill, `enterkeyhint` for the return key. Four attributes, thirty saved taps.
- **`inputmode="decimal"` for money, not `type="number"`.** You want the keypad without the spinner semantics, the sanitization, and the locale surprises.
- **`type="number"` is for quantities only.** Not phones, not cards, not postal codes, not PINs — those are strings that happen to contain digits.
- **16px on every form control, enforced in the primitive.** Below it, iOS Safari zooms on focus and the user is stranded. And when someone proposes `user-scalable=no` to fix it, that's a different, worse bug.
- **Assume the comma.** In a comma-locale the decimal keypad offers a comma and users use it. Write the parser for what the keyboard produces, not for what your dev machine produces.
- **Never `Number(x) || 0` on anything a user typed.** That line is how a blank or unparseable money field becomes a confident zero in the database.
- **Echo the number back.** Show the parsed, formatted value near the field. A misread separator becomes visible instead of being discovered in a total three screens later.
- **Prefer the native picker.** Custom dropdowns and date pickers must beat the platform one on touch to earn their existence, and they rarely do.

## Gestures and scrolling

- **Gesture plus button, always.** The gesture is for people who know it; the button is for everyone else and for conformance.
- **Stay off the edges.** The left, right, and bottom edge strips belong to the operating system. Custom drags anchored there fight the OS and lose.
- **`touch-action: manipulation` on tappables; `touch-action: none` almost never.** The second one is a custom-gesture tool that gets misused as a scroll fix and takes pinch-zoom down with it.
- **`overscroll-behavior: contain` on every sheet and drawer.** Otherwise the inner scroll reaches the end and the page starts moving — or the browser refreshes and eats the form.
- **Horizontal carousels need `overscroll-behavior-x: contain`.** Otherwise a hard swipe navigates back.
- **Lock the body when a sheet is open, and restore the scroll position on close.** The half-implemented version is worse than none.

## Feedback and recovery

- **Feedback goes above the finger.** Under it is under the hand.
- **Undo, not "are you sure".** A dialog interrupts everyone to protect the rare slip; undo protects the slip without the tax. (See [ux-writing](../../content/ux-writing/decision-framework.md) for the confirm/undo table.)
- **Put the undo where the thumb is.** An undo at the top of the screen on a phone is a theoretical undo.
- **If you must confirm, move the button.** Placing the confirming button where the finger just landed converts a double-tap into a destroyed record.
- **Fire on release.** Down-event activation makes every scroll start a potential misfire.

## Enforcement

- **Ask where the rule lives.** If the answer is "in the design system docs", the rule is not in force. Move it into the primitive, a token, a lint rule, or a backstop stylesheet.
- **Fix the class, not the instance.** After every touch finding, ask what stops the next component from reintroducing it. If nothing does, the fix isn't done.
- **Grep for the bypass.** Raw `<input>` outside the field primitive, width-based touch branches, `title=` on interactive elements, `Number(` on user input. Each grep is a five-second audit of a whole defect class.

## Testing

- **On a device, in one hand.** A narrow desktop window has a mouse, hover, a keyboard that never appears, and a hand that never covers the screen. It cannot find these defects.
- **Test with the keyboard open.** Half of the sticky-footer bugs exist only in that state.
- **Test in a comma-locale.** Switch the device language and re-enter every number.
- **Test one-handed reach on the tallest device you support**, not the one in your pocket.
- **Screenshot with a thumb overlay.** Compositing a hand silhouette over a screenshot finds occlusion problems faster than reasoning about them.
