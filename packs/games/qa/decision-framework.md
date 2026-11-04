# Decision Framework — Game QA Pack

The choices this domain presents, and how to settle each one.

## The evidence ladder

Every claim sits on a rung, and every rung names its place. A claim is worth the rung it
reached, not the rung the author hoped for. This ladder is AKOS synthesis (P4, P6).

| Rung | Evidence | Place | Proves | Does not prove |
|---|---|---|---|---|
| 0 | Reading the code or data | none | A defect, or that a claim is false | That anything works |
| 1 | Logic tests of rules | HOST | A rule holds alone | That the rules connect |
| 2 | Headless script | HOST | The path it pressed | Any path it did not |
| 3 | Seeded whole-game run or bots | HOST | Whole routes, invariants along them | Hardware, feel, what is on screen |
| 4 | Rendered review: frames looked at, cuts detected; any simulator, board timings included | HOST | Layout and pixels on the host's draw path | Timing, memory, storage, or the panel |
| 5 | Automated run on the real device | BOARD | Timing, memory, storage, lost input | What a person hears, feels, or understands |
| 6 | A person with the real device | BOARD | Button feel, sound, first-time understanding | Anything not tried |

A simulator that copies the target's timings stays on rung 4: it replays measurements already
taken, so it cannot find what nobody has measured yet.

## Which rung closes which claim

| Claim | Lowest rung that closes it |
|---|---|
| A rule's value is right | 1 |
| The same input gives the same result | 2 (GMQ6) |
| The game can be finished; no reachable softlock | 3 (GMQ1, GMQ12) |
| Saves survive damage and old versions | 3 for logic (GMQ20, GMQ21) |
| Saves survive a real power cut | 5 (GMQ19) |
| Text fits, in every language | 4 (GMQ37, GMQ38) |
| Runs within budget | 5 (GMQ46) |
| Sound does not distort or skip | 6 (GMQ47, GMQ50) |
| Netplay holds between devices | 5 with two devices (GMQ14) |
| Someone new can start playing | 6 (GMQ15) |

If a game has no separate hardware target, BOARD means the slowest device you actually ship
to. If that device is not available, the claim stays open: it is not closed by a guess.

## Which test for which defect

| Defect | Cheapest check that finds it |
|---|---|
| Wrong rule value | Rule test, one per rule |
| Softlock in a puzzle or room graph | Forward and backward reachability on the real rules |
| Softlock in a long game | Finishing bot plus a stuck bound (GMQ31) |
| Sequence break | Negative assertion on the order (GMQ2) |
| Nondeterminism | Replay twice (GMQ6) |
| Lost save | Reset loop on the target (GMQ19) |
| Save bloat | Longest run, weigh the save (GMQ23) |
| Shown differs from used | Assertion across a stat change (GMQ16) |
| Invisible sprite, cut text | Screenshot review, render hook (GMQ37, GMQ38) |
| Orphan knot, dead variable | A small data lint (GMQ40, GMQ41) |
| Calendar bug | Fake clock on the boundary (GMQ29) |

## Severity

Aligned with [agents/game-runtime-reviewer](../../../agents/game-runtime-reviewer.md).

- **CRITICAL:** a softlock or progression blocker on the main path; save data lost or
  corrupted. This holds even when the screen looks fine (P2).
- **HIGH:** a softlock off the main path; a determinism break in a replay or netplay path; a
  frame budget missed on the real target; a shown value that differs from the used one.
- **MEDIUM:** no run reaches a shipped chapter or mode; a text screen with no screenshot
  review.
- **LOW:** level drift between audio files; test ergonomics.

Priority is a separate question. The source weighs how likely players are to meet a defect
against its impact, so a defect in the first session often comes first. That orders the
work. It does not lower severity.

## Choosing an oracle

| Situation | Use | Note |
|---|---|---|
| Deterministic game, software renderer, fixed resolution | Per-frame framebuffer hash, exact | Covers pixels only (GMQ7) |
| Logic core separate from rendering | State digest of named fields, exact | Covers listed fields only |
| Both are cheap | Both | They fail for different reasons |
| Rendering on a real GPU or differing drivers | State digest, plus reviewed screenshots | No pixel oracle is claimed |
| Game genuinely not deterministic | Invariants and profiles (GMQ17, GMQ31) | Say so; a replay oracle is not available |

Golden baselines: a digest is blessed once, on purpose, with the reason recorded (GMQ8). The
only written policy examined covers a state digest. Nothing examined supports
a golden-frame policy for a game, so this pack does not state one. Pinyol's frame goldens
cover its renderer.

## Do the long-running rules apply?

| The game... | Then |
|---|---|
| Ends each session, no real-time element | GMQ25–GMQ30 are `n/a` |
| Uses dates or a real day length | GMQ25–GMQ30 apply in full |
| Has no battery-backed clock | GMQ25 and GMQ26 are release blockers |
| Would take weeks to test in real time | GMQ30 is the only way it gets tested |

## Where this overrides the web testing packs

Each claim was checked against the pack. "No rule" means the pack contains nothing to
override, and the position is simply stated here.

| Web position | Where | Ruling for games |
|---|---|---|
| Auto-waiting locators, accessible selectors | `testing/playwright` PW1, PL2 | **Overridden.** There is no DOM. Wait on ticks (GMQ11). PL1's ban on fixed sleeps survives. |
| Flaky tests may be quarantined; traces on retry | `testing/testing-pyramid` TY4; `testing/playwright` PL4 | **Overridden** for deterministic headless runs: zero retries, no quarantine (GMQ10). PW5 and TP4 already point this way. |
| Unit-heavy suite; few E2E, each justified | `testing/testing-pyramid` TP1, TP3, TY3; `testing/playwright` PL5; the testing lens's "unit-heavy, not inverted" | **Overridden where a whole-game run is cheap:** it becomes the main safety net (GMQ12). An inverted shape is not a finding here. Rule tests stay. If a run is slow or needs hardware, the pyramid stands. |
| Pixel-diff tolerance | No rule in any testing pack | Nothing to override. Position: exact match on a deterministic software renderer at fixed resolution (GMQ6). |
| Core Web Vitals budgets | `performance/core-web-vitals`, including CV5 | **Replaced** by per-target frame and tick budgets (GMQ45). The Game Dev profile already weights frame budget. |
| Viewport and browser matrices | `testing/qa-checklists` QA4, QA-E4; `mobile/responsive-web` RWE3, RWE8 | **Replaced** by the list of shipped targets, each with a fixed screen. No analytics exist to weight it. |
| CRITICAL means floor or data loss | `core/review-pipeline.md` | **Extended, not overridden:** a softlock or progression blocker counts as data loss, even if it looks cosmetic. `testing/qa-checklists` defines no severity scale of its own. |
| Line coverage target | No percentage in any testing pack; `core/reasoning-profiles.md` only mentions one as something Prototype skips | Nothing to override. Position: coverage means states, routes, endings, and knots reached (GMQ1, GMQ4, GMQ40). |
| Tests assert behaviour, not internal state | `testing/tdd` TD-E4 | **Narrowed.** Rule tests keep it. Invariants and state digests read internal state on purpose (GMQ7, GMQ17). |
| Degraded network pass | `testing/qa-checklists` QA-E3 | Applies only to a game that uses a network; for a device-clock game it becomes GMQ26. |

TD-E1, QA-E2, QA-E5, and QA-E6 stand as written. A bug fixed in a game gets its regression as a
recorded replay where the engine allows one.

## Profile modulation

- **Prototype** — only the floor: GMQ1 on the main path if anyone else will play it, and
  GMQ19 if it saves.
- **Startup MVP** — the Critical and High checklist items.
- **Game Dev and Production** — the full checklist, HOST and BOARD apart, on every target that
  ships.
- **Enterprise** — the same, with the baselines' approvals kept as decision records.

## When NOT to use this pack

- **The question is whether the game is fun, fair, or moving.** Refused (P3). Flag it for a
  human and stop.
- **The question is balance.** Reserved for a later pack.
- **The question is accessibility.** `games/accessibility`; the safety floor still applies.
- **The surface is the game's website or store page.** Use the web packs.
- **A firmware or memory question on the chip.** The `embedded` packs own those.
