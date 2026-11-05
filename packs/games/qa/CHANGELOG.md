# Changelog — qa

## [1.2.0] — 2026-11-05

### Calibrated against a third real audit

Third audit, on a wall-clock pet with live updates. GMQ56 refuses a gate that cannot fail. GMQ51 covers rollback on one volume. GMQ6 includes the simulation step rate. GMQ54 fits transports with no sender. The rubric defines shipped, adds `n/a` for GMQ54 and GMQ55, floors the sum at 0, and says how a root cause counts across packs. The README now says four stars. The 1.0.0 entry promised a MicroPython mapping that does not exist: `embedded/micropython` covers that ground.

## [1.1.0] — 2026-11-05

### Calibrated against a second real audit

GMQ54 and GMQ55 cover messages from another device and lockstep proof. GMQ6 repeats a run at a second draw rate. GMQ36 separates a scene that leaves by its own timer. The rubric states how unrun Critical rows, engine defects, unshipped games, and a sum far from the anchors are treated.

## [1.0.0] — 2026-11-04

### Added

- First complete version. Authority level 2 (ISTQB CT-GaMe syllabus v1.0.1), review cadence 365
  days (`review_after: 2027-11-04`). Status `draft`.
- Principles P1–P18 and engineering rules GMQ1–GMQ50 across progression, determinism,
  playthrough and evidence, game state, saves, long-running time, campaign bots, levels, input,
  text, narrative data, frame budgets, and audio. One labelled mapping section holds every
  engine detail: Pinyol, and MicroPython board games.

### Calibrated against repeated audits of one real game

GMQ19 now covers every mutation, deletes included. New: GMQ51 (saves across volumes are branches, moved
after confirmation, owned by version), GMQ52 ★ (a version must reopen its own save before it stays),
and GMQ53 (save-path fixes need a review by someone who did not write them). Each came from a defect
that passed its author's tests.

### The pack's organising decision: what it refuses to contain

**Taste is refused, and claims with no run are capped.** Pixel-art doctrine and audio doctrine
were rejected at intake as taste. Pacing of emotional beats, voice, whether choices have weight,
and whether the ending pays off are refused on the same ground: an agent may flag them for a
human and never scores them. Balance is reserved for a later pack.

The second half of the decision is the evidence ladder. A passing headless script proves only
what it exercised; a game that passes but draws nothing is not done; static reading never proves
a playthrough; a simulator with board timings is still host evidence. The line is enforced in
five places:

- P1, P4, P5, and P6 in the principles.
- The evidence ladder in the decision framework, with each rung naming HOST or BOARD.
- GMQ13 and GMQ14, plus reviewer discipline in the checklist.
- A score cap: no run at all scores 59 at most, and a HOST-only release decision scores 79 at
  most.
- Anti-patterns, including *green and blank* and *HOST promoted to BOARD*.

### Other notable choices

- **Only three rules were starred at first; GMQ52 made it four.** GMQ1 (softlocks), GMQ19 (interrupted writes), and GMQ20
  (every shipped save version). Each is the data-integrity floor applied to games.
- **Determinism is labelled AKOS methodology.** The Level 2 source is silent on it, so the rules
  rest on what the owner's projects do, recorded exactly in `references.md`. Pinyol's `--crc` is
  a framebuffer hash, not a state hash. Private projects supply the state digest, the
  blessed baseline and state replay. GMQ9 stays labelled `unverified`, because no project reports a first divergent frame.
- **Peer desync detection was left out.** `lib/rollback.lua` and `lib/lockstep.lua` hold no state
  check, and no read source describes one, so it did not earn a rule.
- **The softlock source was corrected.** arXiv 2405.11347, named in the pack brief as softlock
  detection, is a paper on cooperative test agents and never mentions softlocks. The idea comes
  from Cooper and Bazzaz (FDG 2025), read and recorded instead, as an idea only.
- **No golden-frame policy is stated.** The one policy examined covers a state
  digest. Nothing examined supports a frame policy for a game.
- **Web-testing claims were checked one by one.** Two had nothing to override: no testing pack
  sets a pixel-diff tolerance or a coverage percentage. The position is stated anyway and the
  absence recorded in the decision framework.
- **Rules were cut to stay at fifty.** Several were folded together: level references now cover
  missing assets, and losing paths joined GMQ1.
- **Numbers the sources do not give are the project's own.** Audio bands and line-length budgets
  are declared per project and never set here.

### Scope boundary

Recorded against `packs/testing/qa-checklists`, `packs/testing/testing-pyramid`, and
`packs/testing/tdd` (kept for what they own, overridden where the decision framework says),
`packs/testing/playwright` (web only), `packs/performance/core-web-vitals` (replaced by
per-target budgets), `games/accessibility` (accessibility in games), and the `embedded` packs
(firmware and memory on the chip).
