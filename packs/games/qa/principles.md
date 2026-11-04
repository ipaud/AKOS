# Principles — Game QA Pack

Durable rules for deciding whether a game is verifiably shippable. The `GMQ*` codes in
[engineering-rules.md](engineering-rules.md) derive from these. Where a principle is AKOS's
own synthesis rather than the position of the Level 2 source, it says so; see
[references.md](references.md) for what the source does and does not cover.

## What this pack will and won't claim

- **P1 — A run proves only what it exercised.** A passing script is evidence about the
  inputs it pressed, the states it passed through, and the frames it looked at. It says
  nothing about the rest of the game. "The tests pass" is a sentence about the tests until
  someone states what they walked.
- **P2 — Losing the player's progress is this domain's data loss.** A softlock and a
  destroyed save both take away hours the player already spent. A softlock can look like
  nothing at all on a screenshot, and it is still critical. This extends the data-integrity
  floor to games; the source ranks defects in core mechanics highest and notes a broken
  mechanic can stop a game being finished, and the word "softlock" is AKOS's, not its.
- **P3 — Taste is not a test result.** Whether a game is fun, whether the pixels are
  beautiful, whether a choice has weight, whether an ending pays off: none of these is
  checkable from an artifact. An agent may flag one for a human. It never scores one.

## Evidence

- **P4 — Every claim has a rung and a place.** The rung is how strong the evidence is. The
  place is HOST or BOARD. A simulator that copies the target's timings, draw code, and lost
  presses is still HOST: it models what was already measured and cannot discover anything
  new about the hardware. (AKOS synthesis, taken from how the owner's release checklists
  actually work.)
- **P5 — A game that passes but draws nothing is not done.** Logic tests see state, and the
  player sees pixels. Between the two sit the draw call that never ran, the sprite under the
  background, and the text past the screen edge. Something has to look at the frames.
- **P6 — Reading never proves a playthrough.** Static reading finds defects, and it can
  disprove a claim. It cannot establish that a game can be finished, saved, or heard. A
  review must separate what it ran from what it read.

## Determinism

- **P7 — Determinism makes the game its own oracle.** If the same inputs must give the same
  outcome, then any difference between two runs is a defect, and no hand-written expected
  value is needed. The syllabus is silent on this. It is **AKOS methodology verified against
  practice** in the owner's projects, not a source's position. See
  [references.md](references.md) for exactly what each project does.
- **P8 — A hash sees only what it hashes.** Two identical framebuffer hashes say the
  hashed frames matched. They say nothing about state that was never drawn. A digest of
  seventeen fields says nothing about the eighteenth. The coverage of the oracle is part of
  the claim.
- **P9 — In a deterministic run, an intermittent failure is a finding.** On the web a flaky
  test has a browser, a network, and a scheduler to blame. Here nothing else is meant to
  vary, so a retry that passes has discovered nondeterminism and then hidden it.

## Progression

- **P10 — Completable is not softlock-free.** A path from start to goal shows that a game
  can be finished once, along that path. A softlock lives on a different path: somewhere
  the player can reach, from which the goal no longer can be. The useful check runs in both
  directions: everything reachable going forward must either reach the goal going backward
  or be a declared loss. (The idea is from the literature, not the Level 2 source; it is
  recorded in references.md as an idea and is not the basis of a rule.)
- **P11 — Reachability is proven on the real rules, and never by luck.** A cheap model of
  the game answers a question about the model. A required step that arrives only on a good
  roll is not reachable; it is likely. One seed reaching it proves that seed.

## State and data

- **P12 — What the game shows is a promise about what the game uses.** A displayed number, a
  hint, a stat: each is a claim the player acts on. The source treats the gap between shown
  and used values as a primary testing objective, and it applies to hidden parameters too,
  which the player can only feel.
- **P13 — A save is untrusted input from the past.** It may be torn by a power cut, written
  by an old version, too new for this one, or edited by hand. A checksum detects damage and
  authenticates nothing, because anyone able to edit the file can recompute it.
- **P14 — Time is an input, and the least reliable one.** On a game that lives on real days,
  the clock can be absent, wrong, moved, or restarted at its epoch. Tests that wait for real
  days do not exist in practice, so a game with a real calendar is tested on a fake one or
  not at all.
- **P15 — Content is data with a structure, and structure can be checked without judging
  it.** A story is a graph; a level is a set of references; a language file is a parallel
  copy of another. Whether a knot is reachable is a fact. Whether the knot is any good is
  P3. (AKOS synthesis on top of the source's level-testing and mechanics scope.)

## Targets

- **P16 — Budgets belong to a target.** There is no universal frame rate and no universal
  screen. One game runs at 60 fps on a handheld and another redraws in hundreds of
  milliseconds on a board, and both can be right. Performance measured on a desktop says
  almost nothing about either.
- **P17 — Text is layout, in every language.** A translation is a new string with a new
  length, new letters, and possibly a new word order around its variables. The screen has
  to be seen in each language, not assumed from the source one.
- **P18 — Every check must be runnable by one person.** A rule that assumes a QA department
  is a rule nobody runs. The source describes a studio's division of labour; this pack
  keeps the defect classes and drops the org chart. Where a human is truly needed, the rule
  says so, and says it can stay open rather than be guessed.

## Scope

This pack covers what makes a game verifiably shippable: progression and softlocks, saves,
game state and displayed values, levels, input edge cases, localised text, determinism as a
test oracle, long-running time, campaign bots, frame-budget regression, and a short
mechanical audio section. It is engine-agnostic; specifics live in two labelled mapping
sections of the engineering rules.

It does not cover balance (reserved for a later pack; a simulation harness appears only as a
QA technique), game accessibility (`games/accessibility`), web testing
([testing/playwright](../../testing/playwright/README.md)), pixel-art or audio doctrine, or
any judgement of craft (P3).
