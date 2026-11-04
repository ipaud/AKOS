# Engineering Rules — Game Accessibility Pack

Checkable in code, data, scripts, frame captures, measurements, and signed device tests. Each rule
names its owner: `[engine]`, `[game]` or `[both]`; reviewers keep or correct that tag per finding
(P5). `★` marks the eight floor rules, CRITICAL in every profile: five are seizure risk, three
restate the constitution's floor for rendered games. Nothing else here is floor.

Sizes are stated for the panel in use: density = screen width in pixels ÷ physical width in mm.
Worked panels are in [decision-framework.md](decision-framework.md). Every number comes from a page
read (see [references.md](references.md)) or is marked an AKOS derivation. Parenthetical codes cite
[principles.md](principles.md).

## Photosensitive safety

- GAX1 ★. [game] At default settings, nothing larger than the GAX2 limit flashes more than
  three times in any one-second window. A flash is a pair of opposing relative-luminance
  changes of 0.10 or more, with the darker state below 0.80. Repeating effects whose leading
  edges are at least 334 ms apart pass at any brightness or size. (P1)
- GAX2 ★. [game] The limit on concurrent flashing area is `0.006 × d²` (cm², for `d` in cm), the
  WCAG solid angle at viewing distance `d`. *AKOS derivation:* use `d` = 20 cm for a held device,
  and the WCAG reference rectangle (2.8 % of the frame) for a desktop or full-screen browser. With
  several surfaces, the tightest shipped limit applies. Shares quoted for television or console
  (25 %, about 20 %) do not relax this. (P2)
- GAX3 ★. [game] Red is tested separately at the same rate and area: a transition to or from
  a state with R/(R+G+B) ≥ 0.8 whose chromaticity moves more than 0.2 in CIE 1976 u'v'. It can
  fail with almost no luminance change, so a luminance-only check does not cover it. Xbox's
  older form, a change above 20 in (R−G−B)×320, also counts: if either flags, it fails. (P1)
- GAX4 ★. [game] No regular pattern (more than five light and dark pairs of evenly spaced stripes,
  with flash-sized luminance difference between adjacent bands) that oscillates, flickers, or
  reverses covers more than 20 % of the screen, the strictest of Xbox's "about 20 %" and BT.1702's
  25 % oscillating. A static one stays under BT.1702's 40 %; 20 to 40 % static is HIGH, never
  CRITICAL. Patterns flowing smoothly one way are exempt, per BT.1702. *AKOS reading:* art with
  uneven spacing or varied content, such as brick, shelves, or tile texture, is not a regular
  pattern, and sources give no angular limit, so line width alone neither triggers nor clears
  this rule. (P1)
- GAX5 ★. [both] GAX1 to GAX4 hold with every option at its default. A "reduce flashing" setting
  and a warning screen earn no credit towards them. (P1)
- GAX6. [both] A flash result names the tool, the limit it used, the route played, and the frame
  rate. It looks at every displayed frame, at the rate the target really displays them; half-rate
  video does not qualify. A candidate from fast scrolling is inspected, since pixel counters
  report motion as flashing. (P3)
- GAX7. [game] A written flash inventory exists: hit flashes, explosions, lightning, palette swaps,
  blinking, transitions, rapid cuts, attract and splash screens, screensavers, an LED, and
  backlight changes. The test route reaches the worst stacked moment of each. (P3)
- GAX8. [game] A flashing sequence near the limit stops within five seconds, even when
  compliant. Lower-intensity flashing is not continued indefinitely either; Xbox treats sustained
  flashing as a failure in its own right. (P1)

## Control

- GAX9 ★. [both] On every shipped surface, with default bindings and only that surface's standard
  input, a player can start the game, complete the primary task, reach pause or exit, and leave
  every screen. No state traps input. (P8)
- GAX10. [both] Every action has a route of plain presses: one button at a time, no timing window,
  no duration distinction. Long presses and chords are shortcuts over that route. Where a
  screen cannot offer it, the exception is recorded with the reason. On a device with very few
  buttons, one recorded project-level exception may cover a gesture used alike on every screen:
  it is then one MEDIUM finding, not a HIGH per screen. This is an AKOS synthesis of Xbox's
  simplified-control and alternative-input positions. (P9)
- GAX11. [game] Neither menus nor play require an extended hold, a rapid repeat, or a simultaneous
  press without an alternative or bypass. Any long press needed for navigation completes in
  under 3 seconds. Hold durations are named constants, one per gesture, and stated to the
  player. (P9)
- GAX12. [engine] Presses are captured while the game is busy: loading, saving, garbage collection,
  network. Evidence is sent presses against received presses, on the target hardware, with the
  machine loaded on purpose, on a stated route. Known limits of the mechanism are written down.
  AKOS position. (P10)
- GAX13. [engine] One press gives one event. A held button does not repeat unless a list is
  being scrolled, releasing after a long press does nothing further, and contact bounce adds
  nothing. Each accepted press is acknowledged at once on screen, by sound, or by light. AKOS
  position. (P10)
- GAX14. [both] Where input devices vary (keyboard, pad), every action can be remapped in the game,
  and at least one binding covers each. On fixed hardware, GAX10 replaces remapping, plus a
  swap of equivalent buttons where it costs nothing. Every on-screen prompt shows the binding
  and the device now active, never a fixed label. (P9, P6)
- GAX15. [game] Gameplay-critical touch, tilt, microphone, or speech input has a digital
  alternative with the same result. (P8)
- GAX16. [game] Where touch exists: targets are measured in mm (Xbox suggests 15 mm on phones;
  below that needs a reason, never below the floor in
  [touch-ergonomics](../../mobile/touch-ergonomics/README.md) at the panel's real density),
  activation is on release, and multi-point or path gestures have an alternative. (P6, P13)
- GAX17. [both] Single-player and local games pause at any time, including cutscenes, save and
  load screens excepted. Live networked play is exempt. (P8)
- GAX18. [game] Menus are operable by one press per step, in a logical order. The focus is always
  visible and never off screen, linear lists wrap, and a slider needs no held button. (P8)
- GAX19. [game] Actions that destroy saved data or cannot be undone show what will be lost and can
  be cancelled. Hold-to-confirm cannot be the only way to confirm. (P9)

## Reading

- GAX20 ★. [game] Text and icons the primary task needs meet 4.5:1 contrast, or 3:1 at large
  size (twice the GAX21 minimum). "Needs" means the player must read it to choose, to know state,
  or to avoid a loss, and always includes the focused item. Measure on rendered pixels, at the
  lowest-contrast part of a mixed background. Logotypes, pure decoration, and text repeated in
  an equal-contrast form nearby are exempt. Under 3:1 is CRITICAL; from 3:1 up to the target is
  HIGH, matching the accessibility agent's severity for an AA failure. (P12, P13)
- GAX21. [game] The smallest text in use has a glyph height of at least 1.06 mm on the target panel,
  aiming for 1.41 mm (*AKOS derivation* from Valve's 9 and 12 px at 1280×800 on a 7-inch panel,
  read at 30 cm). Icons that carry meaning are recognisable at that panel size, and text inside
  them meets the same minimum. Xbox's mobile default, 4.6 mm body height, is a further target;
  where a line-length budget cannot reach it, record that. Passing needs a person at the device
  (GAX41). (P13)
- GAX22. [both] Essential text scales to 200 % of its default without losing content, or the absence
  is a recorded gap with its owner. Screen magnifier features do not count. (P13, P7)
- GAX23. [game] Sentences are in mixed case and left-aligned for their language. Subtitle lines stay
  at 40 characters or fewer, two lines at most. A decorative font has a plain option if used for
  anything longer than a title. Fonts cover every shipped language. (P13)
- GAX24. [game] Text waits for a press unless it is short and repeated elsewhere. A time limit on
  reading or menus can be turned off, or extended to ten times its default, or be preceded by a
  warning that allows at least 20 seconds to extend with one action. Timers inside the challenge
  are exempt but listed. (P15)

## Channels

- GAX25 ★. [game] No cue that the primary task depends on lives in a single channel. A colour-only,
  sound-only, haptic-only, or LED-only cue that blocks completion is a floor failure. (P11)
- GAX26. [game] Colour pairs that carry meaning are listed, each with a second signifier (shape,
  pattern, label, position) or at least 3:1 luminance contrast. Evidence is a screenshot pass in
  grayscale and in simulated protan, deutan, and tritan vision. A display filter does not replace
  this. (P12)
- GAX27. [game] All speech the game needs understood has subtitles naming the speaker, on by default
  or set before any speech. Ambient speech, such as a radio playing behind play, needs an on-screen
  equivalent only where it carries story or instructions.
  Important sounds without a visual counterpart have captions or an on-screen equivalent, including
  direction where direction matters. (P11)
- GAX28. [both] Music, effects, ambience, and voice have independent volume or mute where the game
  has them, and a master mute always exists. (P11)
- GAX29. [game] Essential sound cues are distinct from each other and audible on the target's actual
  output at default volume. Panning is never the only carrier, since one speaker or one working ear
  loses it. (P11, P4)
- GAX30. [both] Haptics and indicator lights can be turned off, and carry nothing that is not also
  on screen. Haptics have adjustable strength if the hardware allows. (P11)

## Motion and juice

- GAX31. [game] Every shake, full-screen flash, hit-stop, and comparable effect goes through one
  gate, with a named cap in a constant and a scale the player can set to zero. Scattered literal
  calls fail. The cap has no sourced number; the requirement is that it exists and can be read.
  (P14)
- GAX32. [game] HUD, prompts, subtitles, and reading text do not move with camera shake, and text
  the player must read has no wave or tremble effect. (P14)
- GAX33. [game] Repetitive camera bob, sway, automatic camera movement, and animated backdrops behind
  menu text can be turned off, unless core to play. A 3D view has an adjustable field of view. (P14)

## Time away

AKOS positions, below the floor (P16); neither XAG nor Game Accessibility Guidelines covers absence.

- GAX34. [game] Where the game runs on the wall clock, absence alone never causes irreversible
  loss: no death, no lost save, no closed route that a return cannot recover, without a recorded
  design decision and a warning the player sees before starting. (P16)
- GAX35. [game] The cost of absence is known and bounded: a test advances the clock by a day, a
  week, and a month, and the result is recorded. A pause or care mode is reachable from the normal
  menus, and decay stops or levels off at a stated ceiling for the case with no time to set it. (P16)
- GAX36. [game] Return shows what happened, once, without blame or a flood of alerts. The first press
  on return cannot trigger an action. Lost or unknown time reads as unknown, never as neglect. (P16)

## Difficulty and recovery

- GAX37. [game] The difficulty and assist decision is recorded, either way. If options exist, labels
  describe the effect without mocking the player, and changing them keeps progress. Level 2 advice,
  never floor. (P17)
- GAX38. [game] Failure does not cost much progress, through regular saves. The current objective
  and controls can be reviewed at any time. (P17)

## Settings and disclosure

- GAX39. [both] Accessibility settings are reachable before the first speech, loud sound, or heavy
  effect, by a route that passes the walks, and they persist. (P18)
- GAX40. [game] A short declaration states what the game offers, what it lacks, flash results,
  sensitive content, and how to reach settings. "Accessible" is not a claim it may make. (P19)
- GAX41. [both] Evidence is labelled HOST or DEVICE. Text legibility, speaker audibility, button feel,
  and input capture are DEVICE-only, signed by a person with the date and build. A review
  without it reports those items as unverified. (P4)

## Pinyol mapping

Labelled target mapping for the Pinyol engine on the Cirera handheld (480×320, 3.5-inch panel about
74 mm wide, so 6.5 px/mm), the SDL desktop player, and the browser. Verified against
`pinyol-engine/pinyol` source and docs on 2026-11-04.

- GAX42. [game] `pinyol_headless --check-flashes` runs on a script reaching the GAX7 route. A pass
  means only: under 25 % of the whole screen, no red test, no pattern test (`src/flashcheck.c`,
  `platform/null/main.c`, limit fixed in code). It cannot show GAX2, GAX3, or GAX4. The Library
  robot's run is 600 ticks with no input, so it is not evidence either. (P3)
- GAX43. [game] GAX2 and GAX3 use every frame: a script of `tick 1` and `shot` lines, then the check in
  the decision framework. `--video` keeps every second frame and is not usable. (P3)
- GAX44. [game] Each flash of the game's own reads `settings().reduce_flashing`; only `juice.flash`
  obeys it unaided. `juice.shake`, `juice.trauma`, and `juice.kick` have no setting, so GAX31 needs
  the game's own option, kept with `store`. (P14)
- GAX45. [game] Prompts derive from `settings().buttons`, because the engine remaps before the game
  sees input and a fixed "press A" then lies. Check with `settings buttons BAC` and a `shot`. Only A, B,
  and C permute; a game needing more builds it on `input.map`. (P9)
- GAX46. [game] `text()` draws in native 480×320 pixels: on Cirera GAX21 means at least 7 px glyph
  height, aiming at 10. The 5 px faces (Tiny5, Micro 5, Bytesized) need `scale = 2`. A `shot` is HOST
  evidence only. (P13)
- GAX47. [game] `settings().colour` shifts the world only; `text()` and shapes stay unfiltered and must
  pass on their own. It is a daltonization filter, so `settings colour deutan` plus `shot` is a play
  test with the filter on, not a CVD simulation. Run GAX26 offline. (P12)
- GAX48. [game] Ajustes offers one master volume, so GAX28 falls to the game through `bus()` and at most
  three `menuitem` entries, or is a recorded gap. `rumble()` is gated by the game's own option. (P7)

## FNK0104B three-button mapping

Labelled target mapping for MicroPython games on a Freenove FNK0104B: 2.8-inch ILI9341, 240×320, about
43 × 57 mm upright, so 5.6 px/mm; REW, PLAY, FF; one small speaker; touch not required. On a small run of hand-built units, GAX41 is the only
legibility evidence: a board item stays open until a person signs it.

- GAX49. [game] Limits for this panel: 2.4 cm², about 10 % of the frame, for GAX2 at 20 cm; glyph height
  at least 6 px, aiming at 8, for GAX21. Xbox's 4.6 mm body height is about 26 px, roughly 18 characters
  across, so text games record this as a gap. Note a stock 8×8 font has a lowercase x-height near 5 px,
  below the minimum: it needs capitals, or a larger face, or a recorded gap. (P2, P13)
- GAX50. [game] Every gesture has a plain route. A reviewer lists each screen where a long press, a hold,
  or a chord is the only way to go back, reach a menu, or confirm, and each is a GAX10 finding. A hold
  confirming what cannot be undone needs a second route under GAX19. (P9)
- GAX51. [engine] GAX12 evidence is a button diagnostic run with the console busy, on the unit. Simulated
  taps with no loss are HOST evidence. Any limit, such as two taps of one button inside one block
  counting as one, is stated to the player. (P10)
- GAX52. [game] GAX34 to GAX36 are reviewed with the clock moved forward. A game on real days needs a
  recorded absence test covering its longest gap and any carer or pause feature. (P16)
- GAX53. [game] GAX6 uses the board's measured redraw time, not the simulator's rate. At a measured
  6 redraws a second or fewer the screen cannot exceed three flashes, which closes GAX1 for the panel
  only: the LED and backlight are checked apart. Screensavers, the LED, and backlight changes go in the
  GAX7 inventory. (P3)
- GAX54. [game] The sound-off walk is run on the unit: one small speaker, no panning. An LED or a
  microphone never stands alone, and that stays a test a person signs. (P11)
- GAX55. [game] Contrast and icons are judged on the panel at high, medium, and low brightness. A 1-bit
  icon passes contrast by construction; recognisability is a person's call, not a screenshot's. (P13, P4)
