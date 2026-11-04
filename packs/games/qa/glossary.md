# Glossary — Game QA Pack

Terms this pack uses precisely. Several collide with web testing; the entry says which sense
is meant here.

- **Softlock** — the game is still running, the player has neither won nor lost, and the
  required goal can no longer be reached. Distinct from a crash, and often invisible on a
  screenshot. The Level 2 source never uses the word.
- **Hardlock** — the game itself stops responding. Found by any run, unlike a softlock.
- **Progression blocker** — anything that stops a required step on the main path, softlock or
  not.
- **Reachable** — can be arrived at by a real player under the real rules from a new game.
  Not the same as "exists in the data".
- **Forward and backward reachability** — forward from the start gives everywhere a player can
  get to; backward from the goal gives everywhere the goal can still be reached from. A
  location in the first set and not the second, unless it is a declared loss, is a softlock.
- **Sink** — a place from which the player inevitably loses. A declared loss, not a softlock.
- **Game state** — the value of everything that describes the game at a moment, shown and
  hidden. The sense follows the Level 2 source.
- **Hidden parameter** — a value that affects play and is never shown. Testable only by reading
  state or by its effects.
- **Tick** — one step of the game's fixed update. The unit for waits in a test. Not a frame on
  a game that drops frames, and not a wall-clock interval.
- **Headless** — running the game with no window. Not the same as with no drawing: an engine
  may skip drawing in this mode, so headless pixels need asking for.
- **Determinism** — same build, same inputs, same outcome. A property a game has to be given,
  by pinning each source of variation.
- **Replay** — running recorded inputs again. As an oracle, it is compared against the first
  run or a baseline.
- **Oracle** — how a test decides pass or fail. Here, usually an earlier run of the game.
- **Framebuffer hash** — a hash of the pixels of a frame. Sees nothing undrawn.
- **State digest** — a hash of named state fields. Sees nothing unlisted.
- **Golden, baseline** — a stored result a later run must match. **Blessing** is accepting a new
  one on purpose, with a recorded reason.
- **First divergent frame** — the earliest frame or step at which two runs differ: where to
  start looking.
- **HOST** — any evidence not gathered on the real target, however faithful. A simulator with
  the target's timings is HOST.
- **BOARD** — evidence gathered on the real device the game ships to. The word comes from
  handheld and dev-board work; on another platform it means the shipped target.
- **Evidence ladder** — the rungs from reading to a person with the device, in
  [decision-framework.md](decision-framework.md). A **rung** is how strong a piece of evidence
  is, and a **place** is HOST or BOARD.
- **Whole-game run** — a run from a new game to an ending. On real input unless it says
  otherwise. Not an "E2E test" in the web sense: here it is the cheap layer.
- **Forced line** — a script line that sets state rather than pressing input. The claim starts
  after the last one.
- **Campaign bot** — a program that plays a whole game as a seeded profile, on the real input
  path, checking invariants as it goes.
- **Profile** — a bot's declared habits: how often it plays, what it does, how well. Distinct
  from an AKOS reasoning profile.
- **Perfect player** — a bot that knows the game, used to show it can be finished. Says nothing
  about how a person plays.
- **Invariant** — something that must hold at every step of a run, such as stock adding up.
- **Save slot, save version** — a slot is a place a save lives; a version is its format.
  **Migration** carries an old version into the current one.
- **Torn write** — a write interrupted partway, leaving a file neither old nor new.
- **Clock floor** — the earliest time the game will believe, so a clock restarted at its epoch
  is not taken as true.
- **Epoch** — the date a chip's clock restarts from with no battery.
- **Catch-up** — simulating the time a device was off, in bounded steps.
- **Knot** — a named place in a branching story, as in ink. **Divert** — a jump to one. **Entry
  set** — every place a story can begin, including those named from game code.
- **Frame budget** — the time a target allows to draw one frame or redraw one screen. Always
  per target and per screen class. On a board it may be a redraw budget in hundreds of
  milliseconds, with no fixed frame rate at all.
- **Pseudo-language** — source strings lengthened and accented by a tool, to expose overflow
  and missing glyphs without a translation.
