# Scoring Rubric — Game QA Pack

Drives [agents/game-runtime-reviewer](../../../agents/game-runtime-reviewer.md), which fills
the Performance and Testing scores. Accessibility in games scores under its own pack, never
twice.

Two things this rubric deliberately refuses to do: score taste, and score a claim nobody ran.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| A softlock or progression blocker on the main path | −25 (CRITICAL) |
| Save data lost or corrupted, or an interrupted write that can cost the last good save | −25 (CRITICAL) |
| A shipped save version that no longer loads, or no evidence that it does | −25 (CRITICAL) |
| A version confirmed with no proof its own save reopens | −25 (CRITICAL) |
| No evidence at all that the game can be finished | −25 (CRITICAL) |
| A softlock off the main path | −10 (HIGH) |
| HOST evidence presented as BOARD | −10 (HIGH) |
| No run from a new game to an ending on real input | −10 (HIGH) |
| A required step that depends on a draw | −10 (HIGH) |
| A shown value differing from the used value | −10 (HIGH) |
| A determinism break in a replay or netplay path; replay not exact | −10 (HIGH) |
| A retry or quarantine on a deterministic suite | −10 (HIGH) |
| Decoded save data used without validation | −10 (HIGH) |
| A message from another device used without validation, or able to stop the game | −10 (HIGH) |
| A failed save the player cannot see | −10 (HIGH) |
| A frame budget missed, measured on the real target | −10 (HIGH) |
| A long-running game with an untested clock: fallback, moved clock, or absence | −10 (HIGH) |
| A scene with no way back and no exit of its own, or a hang on losing an input | −10 (HIGH) |
| A required gate that fails on a clean checkout | −10 (HIGH) |
| Saves across volumes with no stated survivor, moved before confirmation, or lost to a rollback | −10 (HIGH) |
| A simulator, bot, or playthrough that cannot fail, or a claim no gate asserts | −10 (HIGH) |
| A shipped chapter or mode no run reaches | −4 (MEDIUM) |
| A scene that leaves only by its own timer | −4 (MEDIUM) |
| Lockstep play with no build check or no divergence detection | −4 (MEDIUM) |
| A text screen with no screenshot review | −4 (MEDIUM) |
| Text cut at an edge, or a language not rendered | −4 (MEDIUM) |
| A hash claimed for more than it covers | −4 (MEDIUM) |
| A baseline changed with no recorded decision | −4 (MEDIUM) |
| Save size never measured over the lifespan | −4 (MEDIUM) |
| No per-target budget declared | −4 (MEDIUM) |
| Story graph, variables, or language files unlinted, or a silent fallback in content | −4 (MEDIUM) |
| Input edges untested | −4 (MEDIUM) |
| A test waiting on wall-clock time | −4 (MEDIUM) |
| A fix on a save or update path with no independent walk of its cut points | −4 (MEDIUM) |
| Bots that do not repeat under the same seed | −4 (MEDIUM) |
| Internal names on screen | −1 (LOW) |
| Audio level drift between files; no stated voice rule | −1 (LOW) |
| Teaching order or difficulty direction unchecked | −1 (LOW) |
| No first-divergence report | −1 (LOW) |

These are the defaults of [core/scoring-model.md](../../../core/scoring-model.md).

## Caps and floors

- **Any CRITICAL:** Blocked band, score ≤ 59.
- **No run at all: score ≤ 59, labelled `not run`.** A review resting only on reading the code
  (rung 0) cannot exceed this, however clean the code looks. Static reading never proves a
  playthrough (P6).
- **Runs reported but none reviewed:** if no output, log, or screenshot was seen, the
  reviewer treats them as not run.
- **HOST only, on a release decision: score ≤ 79** while any BOARD row that the release depends
  on is open. The game may be well tested and it is still not proven on its target. Nothing
  rated [needs board] or [needs human] may be counted as passed from a host run or from static
  reading.
- **An unrun Critical row is `not run`, not an open CRITICAL.** It keeps the release decision open
  and does not cap the score at 59 by itself, unless nothing ran at all.
- **One root cause, one deduction.** A defect in shared engine code is deducted in the engine's
  review; a game's review lists it with its owner and deducts it only if the game could avoid it.
  A root cause seen by two packs is one finding in the summary, and counts once in each pack's own
  scale; scales are never added.
- **The sum and the anchors can disagree.** Report the sum, floored at 0, name the nearest anchor,
  and below 40 compare severity counts across reviews, not the number.
- **`n/a` for GMQ20 and GMQ52** before anything has shipped: no released save version, no update
  path. The review says so. Shipped means a unit left its owner's hands, or an update channel
  reaches one.
- **`n/a` for GMQ54** with no link between devices, and for GMQ55 when play is not in lockstep.
- **`n/a` for the long-running rules** (GMQ25–GMQ30) when the game has no real-time element.
- **`n/a` for the save rules** (GMQ19–GMQ24) when the game keeps nothing between sessions.
- **`n/a` for the bot rules** (GMQ31, GMQ32) when a script can enumerate every route.
- **`n/a` for the narrative rules** (GMQ40–GMQ44, each where its data is absent), for audio
  (GMQ47–GMQ50) when the game is silent, and for language rules when one language ships.
- **`n/a` for the determinism rules** (GMQ6–GMQ9) when a game is declared not deterministic;
  the declaration itself is checked by GMQ5.
- **`n/a` under Prototype**, except the floor.
- **No deduction may rest on taste.** Fun, pacing, voice, the weight of choices, the payoff of
  the ending, the look of the art, the sound of the music. A finding of that kind is not
  scored at all. This is the most important line in the rubric.
- **Balance is not scored.** GMQ44 checks direction, never values.

## Anchors

- **95** — a finishing run and a backward check on the real rules; every shipped save version
  plays on; reset-tested saves on the target; exact replay; a bad-player bot; every text screen
  reviewed in every language; HOST and BOARD complete and separate.
- **85** — sound on HOST and BOARD, MEDIUM gaps scheduled.
- **79** — thoroughly tested on HOST, with BOARD rows still open.
- **72** — scripts reach most of the game, but with forced state and few screenshots reviewed.
- **59** — not run, or a CRITICAL open.
- **≤ 40** — saves or progression are known to fail, or the report claims things nobody ran.
