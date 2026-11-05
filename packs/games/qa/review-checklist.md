# Review Checklist — Game QA Pack

Binary checks, each citing its rule. Only four items are CRITICAL, all of them the
data-integrity floor applied to games. **A finding names its rung and its place**: what
evidence it rests on, and whether that evidence is HOST or BOARD (P4). An unrun item is
marked `not run`, never passed.

## Critical (blocks in every profile)

- [ ] A finishing run on the real rules shows no reachable state leaves the required ending
      out of reach, losing paths included. (GMQ1)
- [ ] An interrupted write cannot cost the last good save, shown by repeated resets during
      real saves on the target. (GMQ19)
- [ ] A new version saves and reopens that save before it is confirmed, and goes back if it opens
      nothing or only an older copy. (GMQ52)
- [ ] Every shipped save version has a fixture that loads and plays on. (GMQ20)

## High

- [ ] A release report keeps HOST and BOARD apart, each with a date and a build. (GMQ14)
- [ ] Every claim in the review states its rung and whether it ran. (GMQ13)
- [ ] One run goes from a new game to an ending on real input, with state-setting lines
      marked. (GMQ12)
- [ ] Required content has its order tested in both directions. (GMQ2)
- [ ] No required step depends on a draw. (GMQ3)
- [ ] Each listed ending is reached by a run. (GMQ4)
- [ ] From every reachable position the player can get back or lose. (GMQ34)
- [ ] Each shown value that claims an effect is asserted against the used value. (GMQ16)
- [ ] Replay twice gives an exact match. (GMQ6)
- [ ] Every source of nondeterminism can be pinned from a test. (GMQ5)
- [ ] The headless suite runs with zero retries and no quarantine. (GMQ10)
- [ ] Decoded save data is validated before use, with no trust placed in the CRC. (GMQ21)
- [ ] A save and load compares the whole state at each kind of save point. (GMQ22)
- [ ] A failed save is visible and stays due. (GMQ24)
- [ ] Each target's budget is declared from measurement, and none is assumed. (GMQ45)
- [ ] Performance claims come from the real target. (GMQ46)
- [ ] Every scene has a way back through the real controls, and a lost input device does not
      hang the game. (GMQ36)
- [ ] Messages from another device are bounded and validated, and a malformed one cannot stop the
      game. (GMQ54)
- [ ] Simulators and bots assert their outcome, fail when it fails, and run in CI. (GMQ56)

## High, long-running games only

- [ ] The clock source is named, and nothing assumes it survives a power cut. (GMQ25)
- [ ] Sync failure has a tested fallback that never lands on the epoch. (GMQ26)
- [ ] A clock moved either way has a test. (GMQ27)
- [ ] A long absence has a bounded, tested result. (GMQ28)
- [ ] Calendar gates are tested on the day before, the day, and the day after. (GMQ29)
- [ ] A whole life or campaign runs on a fake clock with shipped mode flags, and tick wrap is tested. (GMQ30)

## Medium

- [ ] Lockstep play exchanges a build identity and detects divergence. (GMQ55)
- [ ] Each hash states what it covers. (GMQ7)
- [ ] A baseline changes only by recorded decision. (GMQ8)
- [ ] Test waits count ticks or steps, not wall-clock time. (GMQ11)
- [ ] Checks needing hardware or a person are named and left open until done. (GMQ15)
- [ ] Conserved quantities are asserted throughout a whole run. (GMQ17)
- [ ] Save size stays under its limit across the lifespan, margin stated. (GMQ23)
- [ ] Seeded profiles, a bad one among them, walk the game at real input timing. (GMQ31)
- [ ] Same seed gives the same report. (GMQ32)
- [ ] Every reference in level and content data resolves; a missing asset fails the run.
      (GMQ33)
- [ ] Input edges have scripted tests. (GMQ35)
- [ ] Text cut at an edge is detected by rendering, per language, with deliberate cuts declared. (GMQ37)
- [ ] Every text screen was captured and looked at, per language. (GMQ38)
- [ ] Language tables match in keys and variables, and every letter has a glyph. (GMQ39)
- [ ] The story graph passes a lint across all language files. (GMQ40)
- [ ] Story variables are set and read, and tags resolve with no silent fallback. (GMQ41)
- [ ] Language files carry the same knots and variables, and no TODO remains. (GMQ42)
- [ ] Audio does not skip under load, checked on the target by a person. (GMQ50)

## Low

- [ ] Divergence reports name the first differing step. (GMQ9)
- [ ] No internal name reaches the screen. (GMQ18)
- [ ] A teaching step precedes the first challenge needing the mechanic. (GMQ43)
- [ ] Difficulty moves in its declared direction, or the dip is declared. (GMQ44)
- [ ] No sound file clips, and the mix does not clip. (GMQ47)
- [ ] Audio levels sit within the project's declared band. (GMQ48)
- [ ] The voice limit and who loses a voice are stated. (GMQ49)

## Reviewer discipline

1. **Say what ran.** Separate what you executed, what you read in a captured log, and what you
   only read in the source. An agent that cannot run anything reports evidence it was given
   and marks the rest unverified.
2. **Never promote a place.** A simulator result is HOST, whatever it simulates.
3. **Do not score taste.** Fun, pacing, voice, the weight of a choice, the payoff of an ending,
   the beauty of the art: flag for a human if worth saying, with no severity.
4. **Report engine and game separately.** A defect in shared engine code is one finding.

## Deferred, not checked here

- Accessibility in games → `games/accessibility`
- Balance → reserved for a later pack
- Firmware and memory on the chip → the `embedded` packs
- Sandbox and signing-key exposure → the security lens
