# Pack: MicroPython — Python on a Board, Measured on the Board

**Domain:** Embedded · **Authority:** Level 1 (MicroPython documentation and source) · **Version:** 1.0.0 · **Status:** draft

Keeps Python honest on a microcontroller, with the ESP32-S3 port as the reference target: heap,
fragmentation and collection, allocation in hot paths, interrupt handlers, timing, bytecode,
filesystem behaviour on flash and SD, crash recovery, and a core shared with CPython.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the
MicroPython project. See [references.md](references.md) for the originals.

## What this pack refuses to contain

**An API reference.** Function signatures are one search away and hold no position.

**A claim about the board that was not taken on the board.** This is the organising decision.
Static reading can flag a risk, and a host test can prove logic. Neither can say how long a
collection takes, what is free on the heap, or whether a save survives a power cut. Rules that
need hardware carry `[BOARD]` or `[HUMAN]`, a review without that evidence reports **not verified**,
and the rubric caps the score, so no review passes a board from reading code. The pack also holds
no performance targets, because a target that travels between boards is folklore.

**Chip-level rules.** DMA, secure boot, flash encryption, watchdog behaviour inside the binary,
OTA partitions, and installing updates belong to [embedded/esp-idf](../esp-idf/README.md). That
pack also binds on a MicroPython project for those groups. This one owns everything that lives in
a Python file.

## Whose position is this?

Three marks run through the pack, so a reader always knows what they are trusting. Unmarked means
MicroPython's documentation. `[source]` means the documentation is silent and the fact was read in
MicroPython's source. `[AKOS]` means synthesis from two real games, which is not MicroPython's
position.

## When to load this pack

- Any Python that runs on a microcontroller, especially a game or anything with a frame budget.
- A core that must run on both CPython and MicroPython.
- Button, timer, or audio handling on a MicroPython board.
- A save system on flash or an SD card.
- Before calling a board build ready: the rubric and checklist say what evidence that takes.

**When not to:** CPython with no board target, the chip and bootloader layer, or game logic that
never touches the runtime. A portable core with no board target yet can use only the host gates.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P18. What counts as evidence, memory, handlers, the portable core, data integrity. |
| [engineering-rules.md](engineering-rules.md) | MPY1–MPY50, four starred, plus one labelled section of evidence from two projects. |
| [decision-framework.md](decision-framework.md) | What each kind of evidence can prove, **the CPython trap table**, when collection runs, input capture, where a save lives, source or bytecode or frozen. |
| [review-checklist.md](review-checklist.md) | By severity, with `[BOARD]` and `[HUMAN]` items that static reading cannot tick. |
| [anti-patterns.md](anti-patterns.md) | Green on the laptop, the reset that was called a power cut, the checksum that vouched for a stranger, collecting every frame. |
| [scoring-rubric.md](scoring-rubric.md) | Deductions, caps when board evidence is missing, `n/a` conditions. |
| [heuristics.md](heuristics.md) | Defaults while deciding. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, portable-core gate. |
| [glossary.md](glossary.md) | Terms used precisely, including soft callback, reset test, and power cut. |
| [references.md](references.md) | Sources, what Level 1 covers here, pages read, firmware versions. |

## Core claim, one line

A board tells the truth only to a measurement taken on the board, so a passing host suite proves
your logic and nothing about your heap.

## The four starred rules

All four are the data-integrity and security floor. **A save never overwrites the only complete
state** (MPY36). **Two copies, and a failed copy falls through to the other** (MPY38). **Data from
a card is validated before use, and a CRC is not proof of origin** (MPY39). **Nothing on a
removable card can execute** (MPY40).

## Related packs

[embedded/esp-idf](../esp-idf/README.md) · [testing/testing-pyramid](../../testing/testing-pyramid/README.md)
