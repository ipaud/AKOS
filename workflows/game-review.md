---
schema_version: 1
id: game-review
description: Auditing a game or game engine as a running system.
agents: [accessibility-reviewer, game-runtime-reviewer, security-reviewer]
packs: [games/accessibility, games/qa, embedded/esp-idf, embedded/micropython]
profiles: [Prototype, Game Dev, Production]
status: draft
maintainer: core
---

# Workflow: Game Review

Auditing a game or game engine as a running system. Draft: run it only when the user asks for it by name.

## Capture evidence first

Reviewers hold `Read, Grep, Glob` and cannot run anything, so the orchestrator does this before dispatching them.

1. Build the target and run its automated playthroughs. Keep the exact command, exit code and log of each one.
2. Capture a screenshot of every screen with text, plus any scene with flashing or heavy effects.
3. Compute what reviewers cannot: contrast of the main text pairs on rendered pixels, and a captured frame sequence for each flash candidate. Hand these over as measurements.
4. List what was not run, and which targets were not available. Real hardware counts as unavailable unless a measurement from it is in the repository or the user provides one. A simulator, even one with hardware timing, is host evidence.

Hand this block to every reviewer. If nothing could be run, say so and continue: a read-only review is valid, but it is capped by each rubric and cannot claim a playthrough passed.

## Agents (in order)

1. [accessibility-reviewer](../agents/accessibility-reviewer.md) — with [games/accessibility](../packs/games/accessibility/README.md) in place of `ux/wcag`, and that pack's walks in place of the keyboard and accessibility-tree walks. Floor-level.
2. [game-runtime-reviewer](../agents/game-runtime-reviewer.md) — progression, saves, determinism, frame budget. Loads [embedded/esp-idf](../packs/embedded/esp-idf/README.md) when firmware is in scope and [embedded/micropython](../packs/embedded/micropython/README.md) when the game runs on it.
3. [security-reviewer](../agents/security-reviewer.md) — only when the target has a sandbox for third-party code, network play, a store or web surface, or signed firmware. Otherwise report `n/a` with the reason.

Mobile, frontend, copy and web performance lenses do not apply to a rendered game. Say so in Coverage instead of skipping them silently. The product lens judges menus and flow, never core mechanics, per the Game Dev profile.

## Merge

Combine per-agent findings into one [unified Review Summary](../core/review-pipeline.md). Final decision = worst individual decision. A defect in shared engine code is reported once, against the engine.

- Severity: the pack checklist decides when it states one, and the agent's levels cover the rest. Scores: when several caps apply, the lowest binds, and name it.
- A dimension with no score keeps the run BLOCKED if a CRITICAL is open elsewhere, naming what was not verified.
- Firmware security is scored from the [esp-idf rubric](../packs/embedded/esp-idf/scoring-rubric.md) when it applies, because `scoring/security-score.md` has no embedded inputs.

## Profile adjustments

- **Prototype:** run accessibility at floor depth and the runtime checks for softlocks and save loss only.
- **Game Dev:** run all that apply, at the profile weights.
- **Production:** run all that apply at full depth, and require a real-hardware measurement for any performance claim.

## Exit criteria

Unified summary with severity-ranked findings, each naming its owner and evidence rung, plus the evidence block. INCOMPLETE if a lens that applies did not report. Taste, fun, balance and story quality are out of scope until a pack backs them.
