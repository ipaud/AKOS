# Anti-Patterns — Game QA Pack

Named failure modes, how to spot them, and what to do instead. The examples are invented.

## Green and blank

**Detect:** every script passes, and nobody has opened a frame. No `shot` lines, no reviewed
images, the title screen never seen.
**Why it fails:** logic tests see state. A sprite drawn under the background and a menu
rendered in black on black both pass.
**Fix:** capture every screen with text and look at each one. (GMQ38)

## The teleporting playthrough

**Detect:** a script called "full game" that starts at chapter nine, or sets `boss.hp = 1`, or
forces the score before the last match.
**Why it fails:** the evidence ends at the jump. Everything before it, and the fight it
skipped, is unproven, however green the line looks.
**Fix:** keep the shortcut for speed, mark it, and claim only what comes after. Have one run
from a new game to an ending on real input. (GMQ4, GMQ12)

## The completable softlock

**Detect:** "the level can be finished" backed by one route; no test of what happens after
the player uses the only key on the wrong door.
**Why it fails:** finishing proves one path exists. A softlock is a different path, one
the player takes by mistake and cannot undo.
**Fix:** check reachable states backwards from the goal, and drive the losing and retry paths.
(GMQ1, GMQ34)

## The cheaper model

**Detect:** a level validator with its own idea of jump height, trusted as proof that every
level is winnable.
**Why it fails:** it answers a question about the model. When the real physics differ by a
pixel, the validator passes a level nobody can finish.
**Fix:** use it as a fast filter, then play the level on the real rules. (GMQ1)

## The lucky path

**Detect:** a required item that comes from a random drop; a story beat behind a chance event;
one seed in the test suite.
**Why it fails:** the suite proved that seed. Some players will never get the roll.
**Fix:** a fixed trigger, or a guaranteed return of the missed chance. (GMQ3)

## Retry to green

**Detect:** a retry count on the headless suite; a test marked flaky; "just rerun it".
**Why it fails:** in a deterministic run nothing is meant to vary, so a pass on the second try
has found nondeterminism and thrown the finding away.
**Fix:** zero retries, and treat any intermittent result as a defect. (GMQ5, GMQ10)

## The hash that sees everything

**Detect:** "frames identical, so the state is identical"; a digest of a few fields described
as proving the whole game.
**Why it fails:** a framebuffer hash cannot see a value that is never drawn: an enemy's hidden
timer can differ for an hour before it shows.
**Fix:** state what the hash covers, and add a state digest or assertions for undrawn state.
(GMQ7)

## The silent blessing

**Detect:** a commit that changes a golden digest with no reason; a CI step that updates
baselines; a test whose expected value was pasted from its own failure.
**Why it fails:** the oracle now certifies whatever the code did today.
**Fix:** a changed baseline is a behaviour change: review it, approve it, record why. (GMQ8)

## HOST promoted to BOARD

**Detect:** a release note saying "tested on hardware" where only the simulator ran; one
ticked column for both; "runs at 60 fps" with a laptop behind it.
**Why it fails:** the same screen can take two milliseconds on a desktop and hundreds on the
board. The claim carries the target's name and none of the target's evidence.
**Fix:** two columns, each with date and build. A simulator with board timings is HOST.
(GMQ14, GMQ46)

## The CRC as a lock

**Detect:** decoded save fields used directly because "the checksum passed"; a count from the
save allocated without a bound.
**Why it fails:** a CRC detects accident, not intent. Anyone who edits the save can recompute
it, and a hostile number can exhaust memory at boot.
**Fix:** validate types, ranges, and sizes before use. (GMQ21)

## Latest schema only

**Detect:** migration tests built by hand from memory; a version nobody can load; a test that
only checks that loading raised no error.
**Why it fails:** the first player to update loses their game, and the failure arrives after
release, on the only copy.
**Fix:** a fixture from each shipped version, loaded and played on. (GMQ20)

## The save that grows

**Detect:** lists appended and never trimmed; save size only ever measured on a short run; no
stated limit.
**Why it fails:** nothing fails for months, and then every save fails at once, late in the
game, when the player has the most to lose.
**Fix:** weigh the save at the end of the longest run, against a stated limit. (GMQ23)

## The epoch birthday

**Detect:** a character decades old on the first network sync; a world frozen until the clock
catches up; time spent off that counts wildly wrong.
**Why it fails:** with no battery the chip's clock restarts at its epoch on every power-up,
and the game trusted it.
**Fix:** settle the clock before any state exists, and resume from the last save and a floor.
(GMQ25, GMQ26)

## Waiting for real days

**Detect:** a test plan that says "leave it running for a week"; a calendar feature checked by
changing the laptop's date; a real sleep in a test.
**Why it fails:** nobody runs it twice, so nothing about a long game ever gets regression
tested.
**Fix:** a fake clock through the real update path. (GMQ29, GMQ30)

## The silent fallback

**Detect:** a mood with no portrait that shows the neutral face, a language with no file that
reads the source language, a missing sound logged and skipped.
**Why it fails:** the game looks fine, so no test fails, and the content is simply gone.
**Fix:** make the missing thing fail the run, or lint for it. (GMQ33, GMQ41, GMQ42)

## One language reviewed

**Detect:** screenshots only in the source language; the font checked against the UI strings
but not the story; a bad divert in a language no script loads.
**Why it fails:** each translation has its own lengths, letters, and targets. A defect in an
unloaded language passes every test run in the others.
**Fix:** run and review each language; lint all language files together. (GMQ38, GMQ39, GMQ42)

## Assumed 60 fps

**Detect:** a frame budget of 16.7 ms on a game nobody measured; a world size or resolution
taken from another project.
**Why it fails:** the budget belongs to a target. On one board a hundreds-of-milliseconds
redraw is normal, while on another target it would be a disaster.
**Fix:** measure on each target and declare its budgets. (GMQ45)

## Scoring taste

**Detect:** a finding that says the ending feels unearned, the palette is weak, the pacing
drags; a deduction attached to any of them.
**Why it fails:** it cannot be checked, cannot be refuted, and displaces work on what can.
**Fix:** flag it for a human, with no severity and no score. (P3)

## The QA department rule

**Detect:** a plan that calls for a device lab, a localisation team, or a test matrix
signed off by leads, on a one-person project.
**Why it fails:** nobody will run it, and the checklist decays into fiction.
**Fix:** one script, one bot, one list of what is left for a person to do. (P18)
