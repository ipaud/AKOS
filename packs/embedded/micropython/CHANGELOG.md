# Changelog — micropython

## [1.1.0] — 2026-11-05

### Calibrated against a third real audit

Third audit. MPY21 names BLE event callbacks as handlers. The rubric's row now matches MPY39 on files. The promised project-figures section is dropped: figures belong to projects, not to a public pack.

## [1.0.0] — 2026-11-04

### Added

- First complete version, status `draft`. Authority level 1 (MicroPython documentation and
  source), review cadence 545 days (`review_after: 2028-05-02`). Cleared the source intake gate
  on a verified gap: `gc.collect`, `littlefs`, `fragmentation`, `interrupt handler`, `watchdog`,
  and `bytecode` returned zero files outside `packs/embedded/`, and `micropython` two passing
  mentions.
- Principles P1–P18 and engineering rules MPY1–MPY50 across evidence, allocation, heap accounting,
  collection, interrupt handlers, time, the portable core, saves and files, crash recovery, and
  deployment, plus one labelled section of evidence from two real games.

### The pack's organising decision: what it refuses to contain

**Any claim about the board that was not taken on the board.** Static reading can flag a risk, and
a host test can prove logic. Neither can state a pause, a free-heap figure, or a survival result.
The line is enforced in five places:

- P1 and P2 in the principles.
- `[BOARD]` and `[HUMAN]` tags on rules, which reading reports as **not verified**.
- A reviewer-discipline rule requiring every behaviour finding to name its evidence.
- Rubric caps: 69 with no board record, 79 without real power removal or real-button testing.
- An anti-pattern, *passing a board from the armchair*.

It also refuses an API reference, because AKOS rejects references, performance targets, because a
target that travels between boards is folklore, and chip-level rules, which belong to
`embedded/esp-idf`.

### Other notable choices

- **Three provenance marks.** Unmarked is MicroPython's documented position, `[source]` is read
  in its source because the documentation is silent, and `[AKOS]` is synthesis. Level 1 does not
  extend to `[AKOS]` statements, and `references.md` says so.
- **Source was read because the documentation left gaps that decide outcomes.** Rename onto an
  existing file, and hard pin interrupts on esp32, are both undocumented for this port.
- **Soft callbacks on esp32 are the sharpest finding.** Every Python pin and timer callback is
  scheduled, so Python cannot see events during a stall (P8). MPY24 therefore requires a hardware
  counter for input that must not be lost.
- **MPY20 goes further than the documentation.** Soft callbacks may allocate; the pack keeps the
  hard-handler discipline there, marked `[AKOS]`.
- **Collection is a frame-budget event.** The documentation advises collecting often. That holds on
  the heap it describes, and reverses in the frame loop on a heap of megabytes. The decision
  framework says how to tell which case applies.
- **Only four rules are starred**, all data-integrity or security floor: MPY36, MPY38, MPY39,
  MPY40.
- **No flash-wear rule.** The documentation does not discuss it, and neither project measured it.
- **Two beliefs from the source projects were corrected rather than encoded.** "`os.rename` does
  not replace" is false for both drivers at v1.28 and v1.29. "15 cuts" was `machine.reset()` from a
  timer. Details in `references.md`. Both projects' files were left untouched.

### Scope boundary

Recorded against `packs/embedded/esp-idf`, which owns the chip, bootloader, watchdog configuration,
and update installation, and which also binds on MicroPython projects for those groups. The pack
keeps `machine.WDT` and the path from `main.py` to recovery, and points at IDF23–IDF26 and
IDF43–IDF45 rather than restating them. General test strategy stays with
`packs/testing/testing-pyramid`.
