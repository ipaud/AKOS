# Review Checklist — Game Accessibility Pack

Binary checks, each citing its rule. Eight items are CRITICAL. **Every finding names its owner (engine,
game, or both), its surface, and its evidence (HOST or DEVICE).** An item needing a person on hardware
stays `unverified` without one; it never passes on static reading (P4).

## Critical (blocks in every profile)

- [ ] Nothing over the area limit flashes more than three times in any second at default. (GAX1)
- [ ] Flashing area was judged against the limit for this panel and distance. (GAX2)
- [ ] The saturated-red test was run and passes. (GAX3)
- [ ] No oscillating regular pattern over 20 % of the screen, and no static one over 40 %; a static
      one at 20 to 40 % is a HIGH finding. (GAX4)
- [ ] All of the above hold with default options, with no credit for a toggle or warning. (GAX5)
- [ ] On each shipped surface, default input can start, complete, reach pause or exit, and leave
      every screen; no trap. (GAX9)
- [ ] Essential text and icons meet 4.5:1, or 3:1 large, on rendered pixels. (GAX20)
- [ ] No cue the primary task depends on is single-channel. (GAX25)

## High

- [ ] The flash result names tool, limit, route, and rate, over every displayed frame. (GAX6)
- [ ] A flash inventory exists and the route reaches each worst stacked moment. (GAX7)
- [ ] Every action has a plain press route, or a recorded exception. (GAX10)
- [ ] No required extended hold, rapid repeat, or chord without an alternative; holds under 3 s. (GAX11)
- [ ] Presses are not lost under deliberate load, measured on target hardware. (GAX12)
- [ ] One press gives one event, acknowledged at once. (GAX13)
- [ ] Remap exists where devices vary; prompts always match the active binding. (GAX14)
- [ ] Destructive actions show the loss, can be cancelled, and do not rely only on a hold. (GAX19)
- [ ] Smallest text is at least 1.06 mm on the panel, confirmed by a person. (GAX21)
- [ ] Meaningful colour pairs pass grayscale and simulated CVD review. (GAX26)
- [ ] Speech has subtitles naming the speaker; important sounds have an equivalent. (GAX27)
- [ ] Effects pass through one gate with a named cap and a zero setting. (GAX31)
- [ ] Absence alone causes no irreversible loss without a warned design decision. (GAX34)
- [ ] Settings are reachable before the first speech, loud sound, or heavy effect, and persist. (GAX39)
- [ ] Evidence is labelled; DEVICE-only items are signed. (GAX41)

## Medium

- [ ] Flashing sequences near the limit end within five seconds. (GAX8)
- [ ] Gameplay-critical touch, tilt, microphone, and speech have a digital alternative. (GAX15)
- [ ] Touch targets are measured in mm and meet the GAX16 size, act on release, and multi-point or
      path gestures have an alternative. (GAX16)
- [ ] The game pauses at any time, cutscenes included, offline, unless it runs on the wall clock
      (GAX35). (GAX17)
- [ ] Menus take one press per step, with visible focus and wrapping lists. (GAX18)
- [ ] Essential text scales to 200 %, or the gap is recorded with its owner. (GAX22)
- [ ] Text waits for a press, and each UI timer can be turned off, extended tenfold, or extended
      after a warning. (GAX24)
- [ ] Master mute exists; categories are independent where the game has them. (GAX28)
- [ ] Sound cues are distinct and audible on the actual output, never pan-only. (GAX29)
- [ ] HUD and reading text ignore camera shake, and text to read has no wave or tremble. (GAX32)
- [ ] The cost of absence is tested at a day, a week, and a month, and has a ceiling. (GAX35)
- [ ] Return gives one calm summary, and the first press cannot act. (GAX36)
- [ ] Objectives and controls are reviewable, and the most progress one failure can cost is
      recorded. (GAX38)

## Low

- [ ] Sentences are mixed case and left-aligned; subtitle lines fit 40 characters. (GAX23)
- [ ] Haptics and indicator lights can be turned off and carry nothing unique. (GAX30)
- [ ] Bob, sway, and menu backdrops can be turned off. (GAX33)
- [ ] The difficulty decision is recorded, with descriptive labels. (GAX37)
- [ ] A declaration states features, gaps, flash results, and sensitive content. (GAX40)

## Target: Pinyol

- [ ] `--check-flashes` ran on the real route, and its limits are stated. (GAX42)
- [ ] Area and red use every frame from per-tick `shot`, not `--video`. (GAX43)
- [ ] All the game's flashes read `reduce_flashing`; shake has the game's own option. (GAX44)
- [ ] Prompts follow `settings().buttons`, checked with a mapped run. (GAX45)
- [ ] Smallest `text()` is at least 7 px on Cirera; `shot` is treated as HOST. (GAX46)
- [ ] Text and shapes pass unfiltered; CVD was simulated offline. (GAX47)
- [ ] Volume categories are covered by the game or recorded as a gap, and rumble is gated by the
      game's own option. (GAX48)

## Target: FNK0104B

- [ ] Limits used are this panel's own. (GAX49)
- [ ] On every screen, going back, reaching a menu, and confirming each have a plain route. (GAX50)
- [ ] A button diagnostic with the console busy is recorded on the unit. (GAX51)
- [ ] Clock-forward absence tests are recorded. (GAX52)
- [ ] Flash rate uses measured redraw time; LED and backlight are inventoried. (GAX53)
- [ ] Sound-off walk is signed on the unit; no LED-only or mic-only cue. (GAX54)
- [ ] Contrast and icons are judged on the panel at each brightness. (GAX55)

## Reviewer discipline

1. **Assign the owner.** A finding without engine, game, or both goes back.
2. **Say where it was seen.** HOST or DEVICE, surface, build.
3. **Never write "accessible".** Report walks passed and gaps known (P19).
4. **Do not soften a rule to match a tool.** Record the gap (P7).

## Deferred, not checked here

- Page shell, launcher, forms → [ux/wcag](../../ux/wcag/README.md)
- Touch ergonomics in depth → [mobile/touch-ergonomics](../../mobile/touch-ergonomics/README.md)
- Save integrity and regression testing → the game QA pack in `packs/games/qa`
