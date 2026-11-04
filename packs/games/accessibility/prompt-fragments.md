# Prompt Fragments — Game Accessibility Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first: in most tasks the
build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
GAME ACCESSIBILITY CONSTRAINTS (thresholds are for the screen in use; assume no resolution):

Floor, never waived
- At default settings nothing above the area limit flashes more than 3 times in any second.
  Flash = opposing relative-luminance changes of 0.10+, darker state under 0.80.
- Area limit = 0.006 x d^2 (cm2, d in cm; held device d = 20; monitor 2.8 % of frame).
  Never "25 % of the screen" on a held device.
- Test saturated red separately. No large regular stripe pattern.
- A toggle or warning earns no credit.
- Primary task completable on each shipped surface; no trap.
- Essential text 4.5:1 (3:1 large) on rendered pixels.
- No single-channel cue blocks the primary task.

Input
- Every action has a plain press route; long press and chords are shortcuts.
- No required extended hold, mash, or chord without an alternative. Destructive actions never
  rely only on a hold.
- Capture input while busy. One press, one event. Acknowledge at once.
- Prompts follow the active binding.

Reading and channels
- Density = screen px across / panel mm across. Smallest letter 1.06 mm, aim 1.41 mm.
- Text waits for a press. HUD and reading text stay still.
- Meaningful colour pairs: second signifier or 3:1. Check grayscale and simulated CVD.
- Sound never carries an essential cue alone; panning never carries it alone.

Juice
- One gate for shake and flash, a named cap, a player scale down to zero.

Wall clock (AKOS position, below the floor)
- Absence alone causes no irreversible loss. Bounded cost. A calm return, once.

Tag each decision engine, game, or both. If the engine lacks something, record the gap;
do not soften the rule. Never call the game "accessible".
```

## Fragment: review lens

```text
Review this game against the AKOS game accessibility pack (games/accessibility).

Rules that bind the review:
1. ASSIGN THE OWNER: engine, game, or both, on every finding.
2. SAY WHERE: surface, build, HOST or DEVICE evidence.
3. STATE THRESHOLDS for this panel: compute density and the flash limit first.
4. NEVER WRITE "accessible". Report walks passed and gaps known.
5. Do not soften a rule to fit a tool or engine. Record the gap.

Run the five walks: control, read, sound-off, colour, flash.
CRITICAL only: GAX1 to GAX5, GAX9, GAX20, GAX25.
No flash evidence on a route reaching the worst stacked moment: INCOMPLETE, not PASS.
Legibility, speaker audibility, button feel, and input capture need a person on the device.
Without that, say "unverified", state "host evidence only", and cap the score at 79.

For each finding: rule code, owner, surface, evidence, file or frame, the smallest fix.
```

## Fragment: hardware sign-off

```text
A person with the device, the build noted, signs each line:

- Read: every text screen at arm's length, at each brightness. Can you read it all?
- Icons: do you know what each one means, without being told?
- Sound off: finish the primary task muted.
- Sound on: at default volume, can you hear every cue on this speaker?
- Buttons: every action, then again with the machine busy. Count sent and received presses.
- One press one step; hold each button 10 seconds and release: nothing odd.
- Flash: anything uncomfortable, including LED and backlight?
- Time: leave it, come back. Was the return calm?

Anything not done stays unverified. A simulator run does not count for any line.
```

## One-liner (for tight token budgets)

```text
Game a11y: no flash above 3/s over 0.006 x d^2 cm2 (d = 20 held; 2.8 % of frame on a monitor), red
tested too, no big stripe pattern, default-safe with no credit for toggles or warnings. Primary task
completable, no trap, essential text 4.5:1, no single-channel block. Plain press route for every
action, capture input while busy. Text in mm on the real panel, judged by a person. Effects behind
one gate. Absence never irreversible. Tag owner, surface, evidence. Never say "accessible".
```
