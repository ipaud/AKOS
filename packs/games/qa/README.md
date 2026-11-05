# Pack: Game QA — Shippable Is What a Run Can Show

**Domain:** Games · **Authority:** Level 2 (ISTQB CT-GaMe), plus AKOS methodology labelled as such · **Version:** 1.1.0

Decides whether a game is **verifiably shippable**: can the player get stuck, can a save be
lost, does the game do what it shows, does the same input give the same result, does it hold
its budget on the real target. Engine-agnostic, and written for one developer rather than a
QA department.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
ISTQB or any studio named in the sources. See [references.md](references.md) for the
originals.

## What this pack refuses to contain

**Taste.** Not demoted to a lower weight: refused. Nothing here can be checked from an
artifact, so nothing here is scored. An agent may flag one of these for a human. It never
puts a number on it:

- **Pixel-art doctrine and audio doctrine**, both rejected at intake as taste. Audio survives
  only as a short mechanical section.
- **Pacing of emotional beats, voice, whether choices have weight, whether the ending pays
  off.** Structural checks on story data are in; craft stays out.
- **Whether the game is fun.** The Game Dev profile says feel is the product, and that is
  exactly why a checklist must not pretend to measure it.

**Balance** is also out, reserved for a later pack. A simulation harness may appear as a QA
technique, and GMQ44 checks that difficulty moves in its declared direction, never whether
the values are right.

**Claims with no run.** The line this pack keeps most carefully is between what was run and
what was read. A passing headless script proves only what it exercised; a game that passes
but draws nothing is not done; static reading never proves a playthrough; performance on the
real device cannot be claimed from a desktop run. The rubric caps any score reached with no
run at all.

## When to load this pack

- Before calling a game finished, or before a release candidate.
- Auditing an existing game, its save system, or its test suite.
- A game that lives on real days: a calendar, a pet, a campaign with dates.
- Adding saves, a migration, netplay, a language, or a long story.
- Deciding how to test a game at all.

**When not to:** a game jam prototype nobody will keep, where only the floor applies; a
question about whether the game is good; a web app, which belongs to
[testing/playwright](../../testing/playwright/README.md).

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P18. What a run proves, rungs and places, determinism, progression, saves as input, time as input, budgets per target. |
| [engineering-rules.md](engineering-rules.md) | GMQ1–GMQ55, then one labelled mapping section for Pinyol. Only three rules are starred. |
| [decision-framework.md](decision-framework.md) | **The evidence ladder**, which test closes which claim, severity, choosing an oracle, and the exact web-testing rules this pack overrides. |
| [review-checklist.md](review-checklist.md) | By severity, plus reviewer discipline: every finding names its rung and its place. |
| [anti-patterns.md](anti-patterns.md) | Green and blank, the teleporting playthrough, the completable softlock, retry to green, the CRC that sees everything, HOST promoted to BOARD, the epoch birthday. |
| [scoring-rubric.md](scoring-rubric.md) | Caps for no run at all and for HOST-only release claims; `n/a` conditions; no deduction on taste. |
| [heuristics.md](heuristics.md) | Defaults while deciding. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, release report template. |
| [glossary.md](glossary.md) | Terms used precisely, including collisions with web testing. |
| [references.md](references.md) | Sources, pages read and not read, what each project actually does, and what remains unverified. |

## Core claim, one line

A run proves only what it exercised, and every claim names its rung and whether it ran on
HOST or BOARD; a claim that cannot do either is not a QA result.

## The four starred rules

All four are the data-integrity floor applied to games: **no reachable state leaves the
required ending out of reach** (GMQ1), **an interrupted write never costs the last good
save** (GMQ19), **every shipped save version loads and plays on** (GMQ20), and **a new version
reopens its own save before it stays** (GMQ52). A softlock
can look cosmetic on a screenshot and is still critical.

## How far the authority goes

The Level 2 source supplies the defect classes: mechanics, game state and saves, graphics,
sound, levels, controllers, localisation. It is manual and 3D-leaning and says almost nothing
about automation, and nothing about determinism or replay. Determinism, campaign bots, and
long-running time are therefore **AKOS methodology verified against the owner's projects**,
and each rule that rests on that is labelled. Where no project does what a rule says, the
rule says **unverified**.

## Related packs

[testing/qa-checklists](../../testing/qa-checklists/README.md) ·
[testing/testing-pyramid](../../testing/testing-pyramid/README.md) ·
[testing/tdd](../../testing/tdd/README.md) · `games/accessibility` for accessibility in games ·
[agents/game-runtime-reviewer](../../../agents/game-runtime-reviewer.md) is the lens that
loads this pack.
