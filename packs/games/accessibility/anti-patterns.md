# Anti-Patterns — Game Accessibility Pack

Named failure modes, how to spot them, and what to do instead. The last group are failures of
*reviewing* this domain, which here are as dangerous as the defects.

## The warning screen as a fix

**Detect:** a boot screen about seizures, or a "reduce flashing" option, beside effects that exceed the
limit at default.
**Why it fails:** the people most at risk may not know they are, and a seizure outruns a settings menu.
**Fix:** bring the default below the limit, then keep the option for comfort. (GAX1, GAX5)

## A quarter of a small screen

**Detect:** a check, comment, or tool limit of 25 % or 20 % of the screen on a device held in the hand.
**Why it fails:** that number was written for televisions across a room. On a held panel it can allow
several times the WCAG angle.
**Fix:** compute the limit from panel size and distance, or keep flashing at three a second or fewer.
(GAX2)

## The combo strobe

**Detect:** each hit flash is fine alone; four hits in a second during a combo are not. Reviews read
`flash(3)` once and move on.
**Why it fails:** flashes stack in play, and the code never shows the stack.
**Fix:** rate-limit full-screen flashes globally, inventory the worst moment, test that route. (GAX1, GAX7)

## Red that passes

**Detect:** a pulsing red danger state on a dark screen, reported clean by a luminance-only tool.
**Why it fails:** people are more sensitive to red flashing, so red has its own test, and a change
too small to count as a general flash can fail it.
**Fix:** run the red test, desaturate, or slow it. (GAX3)

## Half the frames

**Detect:** flash analysis from a video or GIF at half rate, or from screenshots at intervals.
**Why it fails:** a one-frame flash, and a flicker that alternates every frame, are invisible at half rate.
**Fix:** capture every displayed frame. (GAX6)

## The idle-screen pass

**Detect:** an automated clean bill from a run with no input, sitting on a title screen.
**Why it fails:** the harm lives in the fight, the super, and the ending, not the title.
**Fix:** script the route to the worst moments. (GAX7)

## Only a gesture reaches it

**Detect:** BACK only on a long press, a menu only on a chord, a confirm only on a two-second hold.
**Why it fails:** the action disappears for anyone without that timing or two free fingers.
**Fix:** add a short-press route. Keep the gesture as a shortcut. (GAX10, GAX11, GAX19)

## The press that vanished

**Detect:** taps lost during saves or loads; players pressing twice; input read once per frame on a slow
device.
**Why it fails:** the player cannot tell ignored from slow, and effort is wasted exactly where it costs
most.
**Fix:** capture independent of the frame, acknowledge at once, test with the machine busy. (GAX12, GAX13)

## The prompt that lies

**Detect:** "Press A" on screen after the player has swapped buttons, or a keyboard letter on a console.
**Why it fails:** a remap that breaks the tutorial is worse than none.
**Fix:** derive every prompt from active bindings. (GAX14)

## Fine on my monitor

**Detect:** text approved from an enlarged screenshot; no note from the actual panel.
**Why it fails:** a monitor at 3× flatters 6-pixel letters that are a millimetre tall in the hand.
**Fix:** convert to mm, then have a person read it on the device. (GAX21, GAX41)

## The colour filter as the answer

**Detect:** "we have a colour-blind mode" with states that still differ only by hue.
**Why it fails:** filters shift colours; they do not add meaning, and may miss text and UI altogether.
**Fix:** a second signifier first; the filter is an extra. (GAX25, GAX26)

## Bass you cannot hear

**Detect:** a low rumble warns of danger; on a small speaker there is nothing. Panned footsteps on one
speaker.
**Why it fails:** the cue exists only on the developer's headphones.
**Fix:** listen on the target; add a visual counterpart. (GAX25, GAX29)

## Juice with no off switch

**Detect:** `shake(8)` literals across forty files; a shaking HUD; dialogue that trembles.
**Why it fails:** nothing can turn it down, and reading fails at the moment information matters.
**Fix:** one gate, a named cap, a player scale, a still HUD. (GAX31, GAX32)

## The pet that punished a hospital stay

**Detect:** two weeks away ends the game, or a return screen full of blame and alerts.
**Why it fails:** real life caused it, the player had no warning, and nothing can repair it.
**Fix:** bound the cost, offer a care mode, bring the player back gently. (GAX34, GAX35, GAX36)

## Calling it accessible

**Detect:** "fully accessible" in a store page, README, or review verdict.
**Why it fails:** no walk can show it, and the source says it is not a compliance checklist.
**Fix:** state walks passed, surface, evidence, and known gaps. (GAX40)

## Host evidence dressed as device evidence

**Detect:** a passing review of legibility, speaker cues, or button capture with only a simulator in the
log.
**Why it fails:** it claims something no one saw. On a one-off gift unit, no other tester will catch it.
**Fix:** mark it unverified until a person signs it on the device. (GAX41)

## Rules softened to fit the engine

**Detect:** "n/a: engine has no text scale"; a threshold quietly loosened to match a tool.
**Why it fails:** the gap disappears from view, so nobody closes it.
**Fix:** keep the rule, record the gap, name the owner. (P7)
