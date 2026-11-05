# Pack: Game Accessibility — Safe by Default, Measured on the Panel in Use

**Domain:** Games · **Authority:** Level 1 (Xbox Accessibility Guidelines, WCAG, ITU-R), with Level 2 and
AKOS positions marked · **Version:** 1.1.0

Operationalizes AKOS's accessibility floor for rendered games: photosensitive safety, control, reading,
colour, sound, motion, wall-clock pressure, difficulty, and settings. `ux/wcag` still governs page shells,
but keyboard walks and an accessibility tree mean little inside a framebuffer, so this pack brings five
walks of its own.

Independent distillation for personal engineering use. Not affiliated with or endorsed by Microsoft, the
W3C, the ITU, Valve, or the Game Accessibility Guidelines authors. See [references.md](references.md) for
the originals.

## What this pack refuses to contain

**Any verdict that a game "is accessible", and any pass without evidence from where it counts.** The
Xbox guidelines say they are not a compliance or legal checklist, and that caveat stands throughout. A
review here reports walks passed, on named surfaces, with labelled evidence, and known gaps.

Three things follow. A flash result from frames that were not played is not a result. A simulator
screenshot can fail legibility, never pass it. And a rule is never softened to fit an engine: a missing
feature is a recorded gap with an owner.

## When to load this pack

- Reviewing or building any game, on any engine.
- Adding screen flashes, shake, strobing, or fast cuts.
- Choosing fonts, palettes, button gestures, or a restricted look.
- Designing a game that runs on the wall clock.
- Preparing a build for real hardware, especially a one-off unit.

**When not to:** a web page, launcher, or form ([ux/wcag](../../ux/wcag/README.md)), or a legal
compliance question.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P19. Harm first, evidence location, owners and surfaces, few buttons, time away. |
| [engineering-rules.md](engineering-rules.md) | GAX1–GAX55, each tagged engine, game, or both; eight starred; separate Pinyol and FNK0104B mappings. |
| [decision-framework.md](decision-framework.md) | Owner test, surfaces, **the five walks**, what is floor, the flash-limit derivation, a tested frame check, text sizes, colour test, juice and time rulings. |
| [review-checklist.md](review-checklist.md) | By severity, per target, with reviewer discipline. |
| [anti-patterns.md](anti-patterns.md) | The warning screen as a fix, a quarter of a small screen, only a gesture reaches it, the pet that punished a hospital stay. |
| [scoring-rubric.md](scoring-rubric.md) | No flash evidence is INCOMPLETE; no device evidence caps at 79. |
| [heuristics.md](heuristics.md) | Defaults while deciding. |
| [prompt-fragments.md](prompt-fragments.md) | Build block, review lens, hardware sign-off. |
| [glossary.md](glossary.md) | Terms used precisely. |
| [references.md](references.md) | Sources, what was read, and what Level 1 covers here. |

## Core claim, one line

Take seizure risk out of the default, give every requirement an owner and a surface, measure on the panel
in use, and report what was actually seen where.

## The floor

Eight starred rules, CRITICAL in every profile. Five are seizure risk (GAX1 to GAX5). Three restate the
constitution for rendered games: the primary task can be completed and nothing traps the player (GAX9),
essential text has readable contrast (GAX20), and no single-channel cue blocks the primary task (GAX25).
Remapping, text size, subtitles, difficulty, absence, and narration are not floor, and the framework says
why.

**Screen narration is a known limit.** The constitution's screen-reader test cannot be met inside a
framebuffer without speech output, so this pack treats it as a declared gap rather than a floor block.

## Related packs

[ux/wcag](../../ux/wcag/README.md) · [ux/apple-hig](../../ux/apple-hig/README.md) ·
[mobile/touch-ergonomics](../../mobile/touch-ergonomics/README.md) ·
[ux/laws-of-ux](../../ux/laws-of-ux/README.md)
