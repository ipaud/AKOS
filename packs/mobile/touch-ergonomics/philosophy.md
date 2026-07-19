# Philosophy — Touch Ergonomics

## The finger is a different device, not a smaller mouse

A mouse reports a point. A finger reports an ellipse the size of a coin, from which the operating system guesses a point. That guess is drawn from a soft, deformable pad pressed at an angle by a hand in motion, often while walking, in one grip that the user did not choose ergonomically but chose because they were also holding something else. The resulting error is not noise around a good estimate; it is a systematic offset that varies with grip, angle, speed and which part of the screen is being reached for.

Everything else in this pack follows from taking that seriously. Target sizes are not a style choice; they are the width of the error distribution. Spacing is not visual rhythm; it is the margin that stops one error from landing on a neighbour. Placement is not composition; it is the geometry of an arc a thumb can sweep. Treating any of these as taste is how a design that looked correct in a desktop browser becomes unusable in a hand.

## Touch is commitment without aim

On a desktop the pointer sits somewhere, all the time, and the user aims before they commit. That resting position funds an entire vocabulary: hover previews, tooltips, hover-revealed controls, cursor changes that say "this is draggable", pointer-follows-focus behaviour that lets a user read an interface with the cursor. None of it exists on touch. The finger has no position until it lands, and landing *is* the click.

So there is no free look. Anything a desktop user discovers by hovering, a touch user must discover by committing — which means either the information was never needed, or it must be visible without any pointer at all. And because the first contact is already the action, mistakes are cheap to make and the interface owes the user a cheap way out: activation on release rather than press, an escape by sliding off before lifting, and undo rather than a dialog that taxes everyone to protect a rare slip.

## The hand covers the evidence

The pointer that clicks is attached to an arm that occludes. Roughly the area below and around the contact point — more of it for a right-handed user reaching left, more again on a large phone — is hidden by the hand at the exact moment the user needs to see whether anything happened. Feedback rendered under the thumb is feedback that did not happen. Tooltips that open downward, validation messages beneath the field being typed into, toasts anchored to the bottom where the thumb rests: each is a design decision made on a desktop where nothing was in the way.

## The keyboard is half the screen and half the contract

On a phone the text-entry surface is not a peripheral; it is a modal panel that eats most of the viewport, arrives without warning, and changes what the layout means. It is also the only place the interface gets to say what kind of value it wants. Markup chooses which keys the user is offered, which return key they get, whether autofill can spare them thirty taps — and, less obviously, which characters the code is about to receive. A field that asks for a decimal in a comma-locale is asking for a comma. If the parser was written assuming a dot, the interface has arranged its own data-loss bug and will commit it silently.

That is the shape of the worst defects in this domain: not "hard to tap" but "quietly wrong". A number that becomes zero, a delete that fires when the user aimed at edit, a warning the touch user never saw. Touch defects that only inconvenience are the mild ones.

## Documentation is not enforcement

Teams that get this right still ship it wrong, and the mechanism is consistent: the rule is known, written down, even explained with its consequence — and then two components bypass the shared primitive and reintroduce the defect. A rule lives in exactly one place, and it is not the doc. It is the field component, the button component, the token, the lint rule, the backstop stylesheet. If a developer can build a working input without going through the thing that enforces the floor, the floor is advisory, and advisory floors are the ones audits find.

This has a corollary that reviewers should internalize: finding a violation in a codebase whose own design system documents the rule is not evidence that the team didn't know. It is evidence that knowing was never the binding constraint.

## Touch is a capability, not a device class

The habit of inferring input from screen width was never accurate and is now actively wrong: laptops have touchscreens, tablets have trackpads and keyboards, phones connect mice, desktop browsers get resized to phone widths by developers who then declare the layout tested. The web platform exposes the actual question — can this device be touched, does it have a hover-capable pointer — and code that asks the actual question is both simpler and correct on hardware nobody anticipated.

The safe posture is asymmetric. Assume touch is possible and size for it; treat hover as a bonus that may never arrive. A 44px target costs a desktop user nothing. A hover-only control costs a touch user the feature.

## Where this philosophy stops

This lens covers the finger and the device. It does not cover how the layout reflows, how type scales, or where the breakpoints go — see [responsive-web](../responsive-web/philosophy.md). It does not decide whether the screen should exist or what the controls should say. And it never overrides the safety floor: a target that fails WCAG 2.5.8, a gesture with no single-pointer alternative, or meaning reachable only by hovering is an accessibility defect first and an ergonomics finding second.
