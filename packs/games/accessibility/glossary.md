# Glossary — Game Accessibility Pack

Terms this pack uses precisely.

- **Flash** — a pair of opposing relative-luminance changes of 0.10 or more, the darker state below 0.80.
  Not the same as a *blink*, which is a slower attention device; a blink faster than three a second counts
  as a flash.
- **Red flash** — a pair of opposing transitions involving a saturated red. Tested apart from luminance.
- **Regular pattern** — repeated light and dark stripes or elements. Fine balanced noise and checkers under
  0.1 degree per side do not count for flashing.
- **Relative luminance** — WCAG's linearized sRGB weighted sum, 0 to 1.
- **Area limit** — the largest concurrent flashing area allowed above three flashes a second, as a solid
  angle converted to the panel in use.
- **Density** — screen pixels across divided by panel millimetres across.
- **Glyph height** — here, the height of the smallest letter in use, x-height where lowercase appears.
- **Body height** — Xbox's text measure, ascender to descender. Larger than glyph height.
- **Surface** — a shipped combination of panel and input: fixed device, desktop, web.
- **Owner** — who must fix a finding: engine, game, or both.
- **Walk** — a defined pass through a build: control, read, sound-off, colour, flash.
- **HOST evidence** — from a simulator, test suite, or screenshot on another machine.
- **DEVICE evidence** — from the target hardware, seen by a person, with date and build.
- **Plain press route** — a way to reach an action by single presses of one button at a time, with no
  timing window. `ux/` packs do not use this term.
- **Gesture** — any press whose meaning depends on duration or combination: long press, hold, chord.
- **Chord** — two buttons pressed together.
- **Primary task** — what a player must do to play the game through. Floor rules apply here.
- **Juice** — effects added for feel: shake, flash, hit-stop, squash, letter tremble.
- **Gate** — the single function all such effects pass through, with a cap and a player scale.
- **Wall-clock game** — one whose state moves in real time while nobody plays.
- **Absence** — time away from a wall-clock game, for any reason, planned or not.
- **Daltonization** — shifting colours to separate those a player confuses. A display filter, not a
  simulation of colour vision.
- **CVD** — colour vision deficiency: protan, deutan, tritan.
- **Assist** — an option lowering a demand of play, such as speed or timing. Advice, not floor.
- **Gap** — a known missing feature, recorded with its owner, the rule left unchanged.
- **Screen narration** — speech output of on-screen UI. A declared gap on targets lacking it.
