# Engineering Rules — Game QA Pack

Checkable in an artifact: code, data, a script, a log, a screenshot, a measurement. `★` marks
the four rules that are floor business, because breaking one loses the player's progress
(P2). Parenthetical codes cite the principle in [principles.md](principles.md).

Labels on a rule: **[AKOS methodology]** means the Level 2 source is silent and the rule was
verified against the owner's projects. **[AKOS synthesis]** means the rule is built on the
source's scope rather than stated by it. **[unverified]** means no project examined does
this yet. **[needs board]** and **[needs human]** mean a host run can never close it.
Unlabelled rules follow the source's defect classes. Numbers come from a page or file that
was read; any other number is the project's own to declare.

## Progression and endings

- GMQ1 ★. No state the player can reach leaves the game running with the required ending out
  of reach, losing paths and retries included. The evidence is a finishing player or solver
  on the real rules, through the real update path, plus a backward check wherever the space
  can be enumerated. A checker cheaper than the real rules is a filter, not this proof.
  [AKOS synthesis] (P2, P10, P11)
- GMQ2. Required keys, abilities, flags, and triggers have a tested order: each is reachable
  with what precedes it, and asserted unreachable without it. An untested negative is how a
  sequence break ships. (P10, P11)
- GMQ3. No required step depends on a draw. Its trigger is fixed, or a missed chance comes
  back, and a run under more than one seed or profile shows it. [AKOS methodology] (P11)
- GMQ4. The endings are listed in data or docs, and a run reaches each one. An ending reached
  only by forcing state counts as forced (GMQ12). (P1)

## Determinism as an oracle

All of this section is [AKOS methodology]: the source does not treat determinism or replay.

- GMQ5. Every source of nondeterminism is named and can be pinned from a test: random seed,
  wall clock, time zone, hash-table iteration order, number width, input timing. A source no
  test can pin is a finding. (P7)
- GMQ6. Replay is run: same build, same inputs, twice, comparing a per-frame or per-step
  record, exact match only. A deterministic software renderer at a fixed resolution matches
  to the pixel, with no tolerance. Where the target can drop frames, the run is repeated at a
  different draw or simulation step rate and the state must match: drawing that shares a random
  stream with the rules fails this, and so does a guard that a slow step trips. (P7)
- GMQ7. A report names what its hash covers: a framebuffer hash covers the pixels of the
  frames it hashed, and a state digest covers the listed fields at the sampled moments.
  Neither is claimed for more. Undrawn state needs a state digest or an assertion. (P8)
- GMQ8. A baseline changes only by recorded decision. A changed digest fails the gate, is
  reviewed as a behaviour change, and is updated with the approval and the reason. CI never
  refreshes a baseline by itself. (P7)
- GMQ9. A divergence report names the first differing frame or step, not only that two runs
  differ. [unverified: no project examined reports this; see references.md] (P7)
- GMQ10. A deterministic headless suite runs with zero retries, and has no quarantine. A
  second attempt that passes is a nondeterminism finding. (P9)
- GMQ11. Test waits count game ticks or steps on a controlled clock, never wall-clock time.
  (P7, P9)

## Playthrough and evidence

- GMQ12. The main safety net is a whole-game run from a new game to an ending through the
  real input path. Every line that sets state, jumps to a chapter, or forces a result is
  marked, and the claim starts after the last such line. (P1)
- GMQ56. A simulator, bot, or playthrough that only prints is not a gate. It asserts its expected
  outcome, exits non-zero when that fails, runs in CI, and fails when an input it depends on stops
  doing what it expects. A document claims only what such a gate asserts. [AKOS methodology] (P1)
- GMQ13. A review says, per claim, which rung of the
  [evidence ladder](decision-framework.md#the-evidence-ladder) it came from and whether it
  ran. A claim with no run says "not run". (P4, P6)
- GMQ14. A release report keeps HOST and BOARD apart, with a result, date, and build for
  each. A simulator with the target's timings or draw code is HOST. Netplay tested against a
  scripted peer is HOST; it needs two real devices. (P4)
- GMQ15. A check needing real hardware or a person is named as such and stays open until
  done: button feel, audible distortion, first-time comprehension, pulling the power.
  [needs board] [needs human] (P4, P18)

## Game state and displayed values

- GMQ16. Every displayed value that claims an effect is asserted against the value the rules
  use: a stat, a price, a hint that says what a point is worth. A change in a shown stat
  changes the outcome it claims to change. (P12)
- GMQ17. Conserved quantities are asserted throughout a whole run, not only at its end:
  stock, money, copies, dates, whatever the game must never break. [AKOS methodology] (P12)
- GMQ18. No internal name reaches the screen: enum values, flags, keys, ISO dates, tag names.
  The check scans the strings actually drawn against a list of internal tokens.
  [AKOS synthesis] (P5, P12)

## Saves

Skip this section only if the game keeps nothing between sessions.

- GMQ19 ★. An interrupted write never costs the last good save: atomic replace or alternating
  copies, and an unreadable copy never starts a new game over an old one. The claim covers
  every mutation on the path, deletes included, not only the final swap: anything other code
  trusts by its existence is renamed aside in one step before it is deleted. The test resets
  repeatedly during real saves on the target's real storage. [needs board] (P2, P13)
- GMQ20 ★. Every schema version ever shipped has a fixture, written by that version where
  possible, that loads and plays on. A save newer than the engine is refused, unchanged and
  set aside. (P2, P13)
- GMQ21. Decoded save data is validated before use: types, ranges, and sizes checked before
  anything is expanded or walked. A CRC detects damage and authenticates nothing, so passing
  it earns no trust, and a failed copy falls back to the other. (P13)
- GMQ22. A save and load compares the whole state, hidden parameters included, at each kind
  of save point the game has: checkpoint, station, autosave, manual. Position alone is not
  a round trip. (P12, P13)
- GMQ23. Save size stays under its slot limit across the whole lifespan, measured at the end
  of a long intensive run, with the margin stated. Unbounded lists are found here. (P13)
- GMQ24. A failed save is visible and stays due: the game keeps running, retries, and the
  player can find out it is not saving. (P2)
- GMQ51. Saves held in more than one place are branches, and each event states which survives:
  rollback, confirmation, a missing volume, a volume that cannot be written. A move between
  them happens after the version is confirmed, never before, and a folder says which version
  wrote it, so an interrupted move is finished or dropped by ownership, not by position. On one
  volume the same holds: the old version's last save stays aside until the new one is confirmed,
  and a rollback returns to it. [AKOS methodology] (P2, P13)
- GMQ52 ★. A new version is confirmed only after it saves and reopens that same save. Slots it
  cannot decode still count as a game, so opening nothing, or only an older copy, sends it
  back before anything is written. Time played and a reachable update channel prove neither.
  [AKOS methodology] (P2, P13)
- GMQ53. A fix on a save, update, or rollback path is not done until a review that did not
  write it has walked every interruption point against it. Its author's tests prove only the
  cases the author imagined. Each cut gets the next boot's behaviour and what could be lost.
  [AKOS methodology] (P1, P2)
- GMQ54. A message from another device is untrusted input, like a save. Size and nesting are
  bounded before parsing; type and range are checked before use, and sender and frame window
  wherever the transport has them. A malformed message cannot stop the game or grow its memory without limit. [AKOS methodology]
  (P2, P13)
- GMQ55. Lockstep play proves itself: both sides exchange a build identity before play, and a
  periodic state hash ends the match with a message when they diverge. Injecting a peer's inputs
  below the receive path shows nothing about that path. [AKOS methodology] (P1, P7)

## Long-running time

Applies to games that live on real days. Otherwise `n/a`. [AKOS methodology]

- GMQ25. The clock source is named in the code or docs, and nothing assumes a wall clock
  survives a power cut unless a battery-backed clock has been shown on the hardware. (P14)
- GMQ26. Sync failure has a defined and tested fallback: no network, bad password, no answer.
  The game resumes from the newest of the last save and a believable floor, never from the
  chip's epoch. (P14)
- GMQ27. A clock moved backwards neither advances nor freezes the game, and a correction
  forwards is not taken for time away. Both have a test. (P14)
- GMQ28. A long absence has a defined result: elapsed time capped, the catch-up bounded and
  shown on screen, the pending events summarised, and nothing dated in the future arriving.
  (P14)
- GMQ29. Calendar-gated content is tested on its exact boundary: the day before, the day,
  and the day after, in a fixed time zone. (P14)
- GMQ30. A whole life or campaign is simulated on a fake fixed clock, through the real update
  path with the same mode flags as a shipped build, never in real time. Tick counters that wrap are tested past the wrap. (P14)

## Campaign bots

Applies to games long enough that a script cannot enumerate the routes. [AKOS methodology]

- GMQ31. Seeded player profiles that differ on purpose, a bad one among them, walk the whole
  game through the real input timing, checking the invariants of GMQ17 as they go. A profile
  that stops making progress within a declared bound fails with its seed and its place.
  (P7, P11)
- GMQ32. Same seed, same report. The report is compared byte for byte, wall-clock lines
  apart. A bot that cannot repeat itself is a bug report nobody can reproduce. (P7)

## Levels

- GMQ33. Every reference in level and content data resolves: spawns, exits, triggers, doors,
  pictures, sounds. A missing asset fails the run instead of logging and continuing. (P15)
- GMQ34. From every position the player can reach, they can get back or lose; no ledge,
  geometry pocket, or out-of-bounds fall leaves them alive and stuck. Every open edge leads
  somewhere. (P10, P11)

## Input

- GMQ35. Input edges have scripted tests: buttons on the same tick, mashing, a hold across a
  scene change, a press during a busy spell, the shortest press, a long hold. One press is
  one action. (P1)
- GMQ36. Every scene has a way back through the real controls, and losing an input device or
  sensor pauses or informs instead of hanging. A scene that leaves only by its own timer strands
  nobody, and is a MEDIUM. (P2)

## Text

- GMQ37. Text cut at a screen edge or box is detected by rendering, in each language, by
  hooking the draw path or by comparing against the box. Reading the strings does not find
  it. A cut made on purpose, such as a tab peeking past the edge, is declared and tested, and
  the report lists it apart from defects. (P5, P17)
- GMQ38. Every screen with text is captured and looked at, in each language: inside its box,
  away from the edge, readable on what is under it. A run with no screenshots reviewed does
  not close this. (P5, P17)
- GMQ39. Language tables have the same keys and the same variables per key, every letter has
  a glyph in the font used, and an artificially lengthened pseudo-language is run to find
  overflow. Sentences are not assembled from fragments around a variable. (P17)

## Narrative and level data integrity

Structural only, and [AKOS synthesis]. These rules hold for any branching format; none says
whether the writing is good (P3).

- GMQ40. The story graph is linted: each knot is reachable from the entry set, which includes
  every knot named from game code; no divert target is missing, in any language file; each
  branch ends explicitly in a divert, an end, or a choice. (P15)
- GMQ41. Every story variable is both set and read, each gating variable is declared, and
  each mood or portrait tag resolves to an existing asset, with no silent fallback. (P15)
- GMQ42. All language files carry the same knots, variables, and conditions, and no TODO
  marker remains in shipped story data. (P15, P17)
- GMQ43. A teaching step precedes the first challenge that needs the mechanic, shown from the
  game's step order. Whether it teaches well is a human's call. (P15)
- GMQ44. Difficulty values move in their declared direction along the progression, or the
  dip is declared in data. This checks order only; whether the values are right is balance,
  out of scope. (P15)

## Frame and tick budgets

- GMQ45. Each target declares its own frame or redraw budget per screen class, from
  measurement. None is assumed: not 60 fps, not a resolution. (P16)
- GMQ46. A performance claim comes from the real target, same scene and same build setup as
  its baseline. A desktop number supports order and ratios only, and a regression is a
  comparison on one target. [needs board] (P4, P16)

## Audio (mechanical only)

- GMQ47. No sound file clips, and the mix does not clip with everything playing, measured on
  a dump where the engine offers one. The speaker at full volume is still [needs human].
  (P5)
- GMQ48. Levels are consistent across files within a band the project declares. The band is
  the project's own number. (P5)
- GMQ49. The voice limit and the rule for who loses a voice under pressure are stated, and
  sounds that must always be heard are protected by that rule. (P16)
- GMQ50. Audio does not skip or drop while the frame budget is under load. [needs board]
  [needs human] (P4, P16)

## Target mapping: Pinyol

Read in the source or docs; **measured** means run on 2026-11-04 on copies outside the repo.

| Rule | On Pinyol |
|---|---|
| GMQ5 | `math.random` starts from a fixed seed; `math.randomseed()` with no argument reads the machine's time. The Lua hash seed is fixed in `CMakeLists.txt`, so `pairs` order repeats. Numbers are 32-bit on every platform. |
| GMQ6 | `pinyol_headless --crc FILE` writes a CRC-32 of the framebuffer on every other frame; `ctest`'s `record_replay` compares two runs with `cmp`. **Measured:** identical on `plataformas`. |
| GMQ7 | `--crc` covers pixels only. **Measured:** a random global that is never drawn differed between two runs while all 31 CRCs matched. Use `expect_lua` for undrawn state. |
| GMQ8 | Whole-frame goldens exist for the renderer only: `tests/ppu_golden.txt`, updated with `ppu_golden_test --update`. No game-level baseline is committed. |
| GMQ9 | No report exists. `cmp` on two `--crc` files gives a line; twice that line is roughly the frame. |
| GMQ11, GMQ12 | Scripts count ticks (`tick`, `press`, `in`). `pinyol_sim --record` writes real input. `lua` lines are not input and are not recorded. |
| GMQ14 | `lib/lockstep` and `lib/rollback` are tested with a scripted peer (`link_from`), not on two boards (`docs/roadmap.md`). |
| GMQ19, GMQ21, GMQ23 | `store()` keeps two files with a generation and a CRC, 64 KB in all; `tests/store_test.py` covers cut, torn, and altered files on the host. On the console the file is written a second after the last `store`, and a pending save is flushed when the game exits. |
| GMQ20 | `content_version` exists for `pinyol@1` only. A `pinyol@2` game owns its own save version. |
| GMQ33 | `--strict-assets` fails only on pictures the run actually requested. A missing sound logs "continuing silent" and does not fail. |
| GMQ37–GMQ39 | `shot name` writes a frame; `_draw` runs headless only for a `shot`. `tools/strings_check.py` checks `strings.csv` keys and glyphs and `--pseudo` lengthens texts by 40%. It does not read `story/*.txt`. |
| GMQ40–GMQ42 | No knot lint exists. `lib/story.lua` rejects a missing target when it compiles a file, so a bad target in an unloaded language passes every other language's script (**measured**). Unknown knots fail only at `s:go`. A mood with no portrait falls back silently to the neutral one. |
| GMQ45, GMQ46 | The meter marks red past 16.7 ms; `-DBP_BENCH=play` measures on the board. `docs/measurements.md` says desktop figures give order and ratios, not console milliseconds. |
| GMQ47, GMQ49 | `--audio FILE.pcm` dumps the mix. The mixer has a soft knee near -3 dBFS. 12 effect voices; when all are busy a new sound takes the one-shot nearest its end; `sfx` offers `max` and `cooldown`, with no priority parameter. |
