# Principles — Touch Ergonomics Pack

Durable rules of touch interaction. Each carries an **operational corollary** — the form the principle takes when it hits code. Violating one requires an explicit tradeoff statement.

## TE1 — The finger reports an area, not a point

Touch input is a contact ellipse resolved to a coordinate the user never sees and cannot adjust before committing. Precision is bounded by anatomy, not by care, so "the user should tap more carefully" is not an available fix. Interfaces absorb the error with size and spacing or they mis-fire.

**Corollary:** every interactive element is sized for the error, not for the icon inside it. If a control's visual box is smaller than the target floor, its hit area is enlarged deliberately and the enlargement is checked against its neighbours.

## TE2 — The hand occludes what it touches

The pointer is attached to an arm that covers a region around and below the contact point at exactly the moment feedback matters. Anything rendered there is not delivered, and the failure is invisible to anyone testing with a mouse.

**Corollary:** feedback for a touch appears above or beside the contact point, never underneath it. Validation messages, tooltips, and confirmations are positioned relative to the finger, not to the desktop convention.

## TE3 — Touch has no hover, and hover is not a channel

There is no resting pointer, so there is no free look. Hover states, hover reveals, `title` tooltips, and cursor-shape affordances carry nothing on a touch device. Hover may reinforce; it may never inform.

**Corollary:** no meaning, no control, and no warning exists only in a hover state. Anything currently delivered by hover is either made persistently visible, moved into an explicit disclosure the user can tap, or deleted because it was never needed.

## TE4 — First contact is commitment

There is no aim-then-click. The gesture that targets is the gesture that fires, which makes accidental activation structurally more likely than on a pointer device and makes recovery the interface's responsibility rather than the user's.

**Corollary:** actions fire on release, not on press, and remain abortable by sliding off before lifting. Consequential actions are recoverable — undo with a stated window beats a dialog, because a dialog taxes every user to catch a rare slip.

## TE5 — Target size is set by anatomy, and there are two numbers

The size at which people reliably hit things is a property of hands, not of visual density. Two numbers govern: the conformance floor (24×24 CSS px, WCAG 2.2 SC 2.5.8 AA, with documented exceptions) and the platform ergonomic target (44×44 pt on Apple platforms, 48×48 dp on Material). They are not interchangeable — the first is where an interface stops being defensible, the second is where it starts being good.

**Corollary:** design to 44/48. Use the 24px floor only where the layout genuinely cannot carry the larger box, satisfy an actual documented exception when you do, and record the decision. A primary or destructive action never rides on the floor.

## TE6 — Spacing is part of the target

A target's usable area ends where its neighbour's begins. Two adjacent 44px areas separated by 4px do not give the user 44px each; they give a contested band that resolves by paint order. Size and spacing are one rule, and the conformance floor's spacing exception says so explicitly: an undersized target qualifies only if its 24px circle does not intersect a neighbouring target's.

**Corollary:** hit areas must not overlap, ever. For adjacent controls with visual widths `wA` and `wB` and floor `F`, require `gap ≥ F − (wA + wB)/2`. Compute it; do not eyeball it. Overlap resolved by stacking order is a defect even when it currently resolves in the user's favour.

## TE7 — Reach across the screen is not uniform

A hand holding a phone can comfortably reach a limited arc. The bottom and inner regions are free; the top quarter costs a regrip; the far top corner opposite the grip is effectively out of service. Screen position therefore encodes cost, and on tall phones the gradient is steep enough to determine whether a flow is usable one-handed at all.

**Corollary:** the primary, most-repeated action lives in the bottom third. Nothing that is required to complete a task sits only in the far top corner. On a screen designed for use in the field — standing, one hand busy, device in the other — this is a functional requirement, not a preference.

## TE8 — Consequence should be inverse to reachability

The easiest place to hit is the worst place to put an irreversible action. Convenience and danger must not coincide, and the thumb's natural sweep toward the primary action should not pass over anything destructive on the way.

**Corollary:** destructive controls sit outside the natural thumb arc, are separated from the primary action by more than the minimum gap, and are never the immediate neighbour of a frequently-tapped control. Where the layout forces adjacency, the destructive action moves behind an explicit disclosure (overflow menu, second step) instead.

## TE9 — A gesture is an accelerator, never the only route

Swipes, long presses, pinches, and multi-finger actions are invisible, undiscoverable, and unavailable to people who cannot perform a path or hold multiple contacts. They are genuinely good as shortcuts for users who know them; they are a lockout as the sole path. WCAG 2.2 SC 2.5.1 makes the single-pointer alternative normative.

**Corollary:** every gesture-driven action also has a visible control that performs it with a single tap. Gestures never carry the only route to an action, and no gesture is required to *discover* that an action exists.

## TE10 — The virtual keyboard is part of the layout

The keyboard is a modal panel that arrives unannounced, occupies a large share of the viewport, and does not consistently resize the layout viewport across browsers. Any layout designed as if the visible area were stable is a layout that hides its own submit button the moment the user starts typing.

**Corollary:** fixed and sticky elements are verified with the keyboard open on a real device. Layouts use dynamic viewport units and, where precision is required, the visual-viewport API rather than assuming the initial viewport height persists.

## TE11 — The keyboard the user gets is the one the markup asked for

Which keys appear, which return key is offered, and whether autofill can complete the field are all decided by attributes. A field that omits them is not neutral — it has requested the generic alphabetic keyboard and declined autofill, and the user pays in taps.

**Corollary:** every input declares `type`, `inputmode` where it differs from the type's default, `autocomplete` with a real token, and `enterkeyhint` in multi-field forms. `inputmode` is presentation only: it changes the keyboard and restricts nothing, so validation is never delegated to it.

## TE12 — A string is not a number until it is parsed under a locale

Keyboards are localized. A decimal keypad in a comma-locale offers a comma, and users type it. `Number("12,50")` is `NaN`; `parseFloat("12,50")` is `12`; `Number("") || 0` is a confident zero. Every one of those is a wrong value that looks like a value, and on a money field that is data loss with a plausible face.

**Corollary:** parsing is explicit, locale-aware, and total: it returns either a number or an explicit failure, never a fallback zero. `type="number"` does not solve this — in a comma-locale the element's own sanitization can yield an empty value from input the user can see on screen. Where money or quantity is involved, the parsed interpretation is echoed back before it is committed.

## TE13 — Input capability is a device property, not a screen width

Laptops have touchscreens, tablets take trackpads, phones take mice, and desktop windows get narrowed to phone widths by developers. Width has never answered "can this be touched", and code that infers one from the other is wrong on hardware that already exists.

**Corollary:** sizing branches on `any-pointer: coarse` (can this be touched at all), hover enhancements branch on `hover: hover` (does the primary pointer hover), and neither branches on `max-width`. The asymmetry is deliberate: size for the coarsest possible pointer, treat hover as a bonus that may never arrive.

## TE14 — A rule components can bypass is not enforced

Teams ship known defects. The mechanism is not ignorance — it is that the rule lived in a document while the components lived in the codebase, and two of them were written without going through the shared primitive. Documentation records intent; it does not constrain behaviour.

**Corollary:** each rule in this pack has exactly one enforcement site — a primitive, a token, a lint rule, or a backstop stylesheet. A fix that corrects the instance without installing the constraint is scored as unfixed, because the next component will reintroduce it.

## TE15 — Touch errors are cheap to make, so recovery is a feature

Given imprecision, occlusion, commitment-on-contact and one-handed use in motion, mistaken taps are the expected case rather than the exceptional one. An interface that treats every mistake as a user failure will be experienced as hostile on a phone regardless of how it feels on a desktop.

**Corollary:** consequential actions are reversible by default, with the undo affordance rendered where the thumb already is and held long enough to survive the user noticing. Confirmation dialogs are reserved for the genuinely irreversible; when used, they place the confirming button away from the position the user just tapped.

## TE16 — The device is used in the world, not at a desk

Phones are used while standing, walking, in sunlight, in gloves, with a wet screen, with one hand holding something else, and by people whose grip is not steady. Every one of those widens the error distribution the rest of this pack budgets for, and none of them appear in a desktop browser at 1440px.

**Corollary:** for surfaces with a known field-use context, the ergonomic target is a minimum rather than a goal, primary actions are placed for one-handed reach, and the flow is tested on a real device held in one hand — not resized in a browser.
