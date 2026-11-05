# Review Checklist — MicroPython Pack

Binary checks, each citing its rule, ordered by severity. Items tagged `[BOARD]` or `[HUMAN]`
pass only on a record from hardware. **Reading code never ticks them.** Without the record, mark
the item **not verified**, say what run would settle it, and apply the
[rubric's caps](scoring-rubric.md).

## Critical (blocks in every profile)

- [ ] No step of a save overwrites the only complete state. (MPY36)
- [ ] Two copies exist; a copy that fails to read, fails validation, or raises `MemoryError`
      falls through to the other; a read failure never starts a new game over old files. (MPY38)
- [ ] Data from a card or file is size-bounded, then validated for structure, range, and scale
      before use or expansion. No CRC is treated as proof of origin. (MPY39)
- [ ] Nothing on a removable card can execute: no path entry, no module, no `exec` or
      `eval`. (MPY40)

## High

- [ ] [BOARD] Timing, heap, and latency claims carry value, firmware, commit, load, and
      sample count. (MPY1)
- [ ] HOST and BOARD results are recorded apart, and no simulator result fills a BOARD
      entry. (MPY2)
- [ ] Every core change shows both the CPython suite and a MicroPython gate. (MPY31)
- [ ] [BOARD] Save, load, and rarely reached paths were executed on MicroPython, not only
      imported. (MPY32)
- [ ] No `gc.collect()` in the frame loop or input path without a board number. (MPY15)
- [ ] [BOARD] Worst collection pause was measured at real occupancy. (MPY16)
- [ ] [BOARD] Continuous consumers fed from Python outlast the worst measured stall. (MPY17)
- [ ] Handlers do bounded work: no loops, waits, `print`, or filesystem calls. (MPY19)
- [ ] Handlers create no objects, and bound methods are cached. (MPY20)
- [ ] Shared multi-value state goes through a ring buffer or a short critical section, and no
      read-modify-write is shared. (MPY23)
- [ ] [BOARD] Input that must survive a stall is captured by a hardware counter and reconciled
      in the main loop. (MPY24)
- [ ] [HUMAN] Real buttons were tested under deliberate load, with lost and doubled presses
      counted. (MPY26)
- [ ] The write path names its filesystem's replace behaviour, confirmed on that filesystem, and
      no `os.remove` precedes a rename on LittleFS without a second valid copy. (MPY37)
- [ ] [HUMAN] Any power-loss claim rests on real power removal during a write, and resets are
      reported as reset tests. (MPY44)
- [ ] A failed save is visible, and play continues. (MPY43)
- [ ] An uncaught exception ends in a logged reset, and repeated crashes reach recovery, not
      the prompt. (MPY45)
- [ ] `main.py` reaches recovery even when a game module fails to import. (MPY47)

## Medium

- [ ] [BOARD] Benchmarks report median and worst and say whether they collected first. (MPY3)
- [ ] [BOARD] One real frame pass ran under `heap_lock`, or its allocation is accepted in
      writing. (MPY4)
- [ ] Repeated buffers are created once; `readinto` and `memoryview` replace copies. (MPY5)
- [ ] Large permanent buffers are allocated early, after imports. (MPY6)
- [ ] Per-frame text is cached until its inputs change, or drawn from bytes. (MPY7)
- [ ] No hot path computes with integers outside ±2**30. (MPY8)
- [ ] Firmware routines replace Python loops, and a slow fallback announces itself. (MPY9)
- [ ] Large loads handle `MemoryError` by evicting, falling back, or trying the other save. (MPY11)
- [ ] [BOARD] Diagnostics show both heaps and the largest free block at peak occupancy. (MPY12)
- [ ] [BOARD] Data that grows has a measured per-item cost and a limit. (MPY13)
- [ ] Allowed and forbidden collection points are stated in one place. (MPY14)
- [ ] `gc.threshold` carries a recorded reason, and `gc.disable` has a guaranteed collect elsewhere.
      (MPY18)
- [ ] The emergency exception buffer is allocated, and handlers catch their own exceptions. (MPY21)
- [ ] Globals and dict keys used by handlers exist before interrupts start. (MPY22)
- [ ] `schedule()` failure is handled, and bouncing inputs are filtered before any callback. (MPY25)
- [ ] Ticks use `ticks_diff` and `ticks_add` only. (MPY27)
- [ ] No stored tick outlives half a period on a long-running device. (MPY28)
- [ ] Code runs with no wall clock, and timestamps never pass through `float()`. (MPY29)
- [ ] The core imports no platform, enforced by a check, and takes time as an argument. (MPY30)
- [ ] Core code avoids the trap table, or uses its board-safe form. (MPY34)
- [ ] [BOARD] Save size has a tested limit, and save time at that size is measured. (MPY41)
- [ ] Frequent saves on FAT are a recorded decision with a loss window and a LittleFS copy. (MPY42)
- [ ] The watchdog is a recorded decision, with its timeout above the worst stall, fed from the
      main loop, or the hang is a listed gap. (MPY46)
- [ ] `mpy-cross` is pinned, and `sys.implementation._mpy` is checked. (MPY48)
- [ ] Deployment is verified by hash, not size, with a recovery for a cut mid-deploy. (MPY49)
- [ ] [BOARD] Release validation ran from a reset through the stored `main.py`. (MPY50)

## Low

- [ ] Long native routines yield, and viper lengths are proved before pointer loops. (MPY10)
- [ ] Extended built-ins use the documented `sys.path` method, and no built-in is patched. (MPY33)
- [ ] [BOARD] Recursion in shared code has a measured bound. (MPY35)

## Reviewer discipline

Two rules, both aimed at this domain's specific failure:

1. **Say where the evidence was taken.** Every finding about behaviour names its evidence: read,
   HOST, BOARD, or HUMAN. Static reading may raise a risk at any severity, and may never close
   one (P1, P2).
2. **Say the method, not the conclusion.** Write "15 resets from a timer", not "survives power
   cuts". Reports carry claims forward; this keeps them from growing on the way (P15).

## Deferred, not checked here

- Chip, DMA, flash, secure boot, watchdog configuration, and update installation →
  [embedded/esp-idf](../esp-idf/README.md)
- Test balance and strategy → [testing/testing-pyramid](../../testing/testing-pyramid/README.md)
