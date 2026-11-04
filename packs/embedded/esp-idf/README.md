# Pack: ESP-IDF — Firmware That Survives Its Board, Its Battery, and Its Owner's Absence

**Domain:** Embedded · **Authority:** Level 1 (Espressif, platform owner) · **Version:** 1.0.0

Checkable positions on how firmware must behave on ESP32-class chips, with the ESP32-S3 as
reference and ESP-IDF v5.4.2 as baseline: memory placement, DMA, flash-cache safety, tasks,
watchdogs, stacks, storage integrity, OTA and rollback, Secure Boot, Flash Encryption, eFuses,
power, and build configuration.

Independent distillation; not affiliated with or endorsed by Espressif Systems. See
[references.md](references.md).

## What this pack refuses to contain

**API reference, and any runtime number it did not get from a board.** Espressif's guide can be
looked up, so restating it adds nothing. A figure for a board the reader does not have is worse
than none, because it reads like a budget. Every number here is a documented platform fact or
one project's measurement, labelled with that project and board. Rules that need real hardware
carry `[board]`, and a review from static reading alone cannot pass them.

Two lines hold everything else up:

- **Measurement beats doctrine on the exact board.** Platform guidance is the prior.
- **Irreversible operations and data integrity are a floor.** A procedure that can brick hardware
  without a dry run and a written way back is CRITICAL, and so is an update design that can lose
  the last good state.

## When to load this pack

- Firmware on an ESP32-class chip under ESP-IDF, especially real-time and memory-constrained work.
- Anything touching eFuses, signing keys, Secure Boot, or Flash Encryption. Load it before the
  procedure exists, not after.
- OTA design, by app partition or by application files.
- A device about to leave your hands, such as a gift, and still receive updates.
- **MicroPython on these chips, for the chip and bootloader groups below.**

**When not to:** anything that is not firmware on this chip family: other microcontrollers, desktop or
WASM builds of the same engine, and game logic above the hardware. For those parts of a project, a
passing review here means nothing.

## With MicroPython on top

MicroPython sits on ESP-IDF, so the chip underneath still behaves as this pack says.
[embedded/micropython](../micropython/README.md) owns heap, interrupts, filesystem, and runtime
rules, and this pack does not repeat them.

| Still binds under MicroPython | C firmware only |
|---|---|
| OTA partitions and rollback (IDF35–IDF41) | Memory placement (IDF5–IDF11) |
| File-based updates (IDF42–IDF45) | DMA in your own code (IDF12–IDF14) |
| Devices out of reach (IDF46–IDF50) | IRAM attributes and flash-cache safety (IDF15–IDF18) |
| Secure Boot, Flash Encryption, eFuses (IDF51–IDF58) | Tasks and core affinity (IDF19–IDF22) |
| Watchdogs (IDF23–IDF26) | Stacks and faults (IDF27–IDF29) |
| Brownout and power (IDF59–IDF61) | Storage code (IDF30–IDF34) |
| Evidence and version pinning (IDF1–IDF4, IDF62) | Frame budgets (IDF64) |

The full split and its reasons are in the [decision framework](decision-framework.md).

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P17: evidence, what cannot be undone, power cuts, memory and time, detection. |
| [engineering-rules.md](engineering-rules.md) | IDF1–IDF64. |
| [decision-framework.md](decision-framework.md) | Which groups bind, where data goes, the irreversibility gate, development versus release, what ESP-IDF's OTA does not cover. |
| [review-checklist.md](review-checklist.md) | By severity, with `[board]` items and reviewer discipline. |
| [anti-patterns.md](anti-patterns.md) | The fix that ships in the update that never arrives, the watchdog that was assumed to reset, and others. |
| [scoring-rubric.md](scoring-rubric.md) | Deductions, `n/a` conditions, and a cap for static-only reviews. |
| [heuristics.md](heuristics.md) | Defaults while deciding. |
| [prompt-fragments.md](prompt-fragments.md) | Build block, review lens, eFuse gate, handover gate. |
| [glossary.md](glossary.md) | Terms used precisely. |
| [references.md](references.md) | Baseline, pages read and not read, what Level 1 covers. |

## Core claim, one line

The chip tells you what is possible, the board tells you what is true, and anything you cannot undo
or reach gets proven before it happens.

## Level 1 and synthesis

Level 1 covers documented chip, bootloader, and ESP-IDF behaviour. Frame-budget practice, what a
given-away device needs, and hang recovery are AKOS synthesis, marked as such where they appear.

## Related packs

[embedded/micropython](../micropython/README.md) · [security/nist-ssdf](../../security/nist-ssdf/README.md)
for signing and supply chain · [devops/deployment](../../devops/deployment/README.md) for rollback as
a release discipline · [performance/browser-rendering](../../performance/browser-rendering/README.md)
shares only the frame-budget arithmetic; none of its mechanisms apply here.
