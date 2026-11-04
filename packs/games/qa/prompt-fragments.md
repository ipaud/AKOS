# Prompt Fragments — Game QA Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first: in most
tasks the build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
GAME QA CONSTRAINTS (Level 2 for defect classes; determinism, bots and time are AKOS
methodology, labelled in the rules. This pack never judges taste, and neither should you):

Evidence
- A passing script proves only what it pressed. Static reading never proves a playthrough.
- A game that passes but draws nothing is not done: capture every text screen and LOOK at it.
- Every claim names its rung and its place. A simulator with board timings is still HOST.
- Performance on the real device can't be claimed from a desktop run.

Progression
- No reachable state may leave the required ending out of reach, losing paths included.
- Prove reachability on the real rules, never on a cheaper model and never by luck.
- Keep one run from a new game to an ending on real input. Mark every forced line.

Determinism
- Name and pin every source of variation: seed, clock, zone, hash order, number width, input
  timing.
- Replay twice, exact match. Zero retries: a pass on the second try is a finding.
- Wait on ticks, never on wall-clock time.
- State what a hash covers. Frame hashes do not see undrawn state.
- Change a baseline only by recorded decision.

Saves
- An interrupted write never costs the last good save. Test with resets on the real storage.
- Every shipped version has a fixture that loads and plays on.
- Validate decoded data before use. A CRC detects damage; it does not authenticate.
- Weigh the save at the end of the longest run.

Time, if the game lives on real days
- Name the clock. Assume no wall clock survives a power cut.
- Offline fallback from the last save and a floor, never the epoch.
- Test the clock moved both ways, a long absence, and exact calendar boundaries.
- Simulate a whole life on a fake fixed clock through the real update path.

Text and data
- Detect cut text by rendering, per language. No internal names on screen.
- Lint story data: reachable knots, no missing targets, variables set and read, tags resolve,
  language files match, no TODO. Structure only.

Targets
- Budgets are per target and measured. Never assume 60 fps or a resolution.

FLOOR: softlocks and lost saves are data loss, critical even when they look cosmetic.
```

## Fragment: review lens

```text
Review this game against the AKOS game QA pack (games/qa).

Three rules bind the review itself:

1. SAY WHAT RAN. Separate what was executed, what you saw in a captured log or screenshot, and
   what you only read. Anything else is "not run". A review with no run at all scores 59 at
   most.
2. NAME THE RUNG AND THE PLACE. Every finding says what evidence it rests on and whether that
   evidence is HOST or BOARD. Never promote a simulator to BOARD.
3. NEVER SCORE TASTE. Fun, pacing, voice, the weight of choices, the payoff of the ending, the
   look of the art, how the music sounds. Flag for a human if useful, with no severity. Balance
   is out too.

Only four findings are CRITICAL by rule: a softlock or blocker on the main path (GMQ1), an
interrupted write that can cost a save (GMQ19), a shipped save version that no longer loads
(GMQ20), and a version confirmed without reopening its own save (GMQ52). A softlock is critical even when it looks cosmetic.

Then in order: forced lines where a whole-game run was claimed, required steps that depend on
a draw, shown values differing from used ones, replay not exact, retries on a deterministic
suite, unvalidated saves, an untested clock, budgets not measured on the target.

Report engine and game separately: a defect in shared engine code is one finding.

For each finding: rule code, file and line or artifact, rung and place, the owner, and the
smallest fix.
```

## Fragment: release report

```text
Release report for <game> <version>, <date>, build <commit>.

| Check | HOST (result, date) | BOARD (result, date) | HUMAN (result, date) |
|---|---|---|---|
| Whole game, new game to each ending, real input | | | |
| Softlock evidence, method named | | — | |
| Replay twice, exact; what the hash covers | | — | — |
| Bots: profiles, seeds, invariants, same report | | | — |
| Every shipped save version plays on | | | — |
| Resets during real saves, count and size | — | | — |
| Save size at end of the longest run, limit | | — | — |
| Clock: fallback, moved, absence, boundaries | | | — |
| Text: cuts detected, screens looked at, per language | | | |
| Budget per screen class on this target | — | | — |
| Audio: no clipping, no skipping under load | | | |

Rules for this table:
- A HOST result never fills a BOARD cell. A simulator with board timings is HOST.
- An empty cell says "not run". "—" means the check does not apply in that place.
- Open items are listed, not hidden. Forced lines in any script are listed.
```

## Fragment: new-language or story change

```text
This change touches story data or a language. Before it ships:

1. Lint all language files together, not the one in use: same knots, variables, and conditions,
   no TODO.
2. Every knot reachable from the entry set, counting those named from game code. No missing
   target in ANY language file.
3. Every variable set and read; every tag resolves to an asset, with no silent fallback.
4. Every letter has a glyph in the font used, story text included.
5. Run each language and look at each text screen. Passing in one language says nothing about
   another.

Structure only. Do not comment on the writing unless asked, and never score it.
```

## One-liner (for tight token budgets)

```text
Game QA floor: a run proves only what it pressed; name each claim's rung and HOST or BOARD, and
say "not run" otherwise. No reachable state may lose the required ending, proven on the real
rules, not by luck. Replay twice exact, zero retries, wait on ticks, state what each hash
covers. Saves survive resets on real storage, every shipped version plays on, validate decoded
data since a CRC authenticates nothing. Real-day games: name the clock, assume it dies with
the power, test it moved, absent, and on exact boundaries, on a fake clock. Look at every text
screen in every language. Budgets are per target and measured. Never score taste or balance.
```
