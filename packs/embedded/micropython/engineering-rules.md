# Engineering Rules — MicroPython Pack

Checkable in an artifact: code, a bench log, a test record. `★` marks the four rules that are
safety floor. Parenthetical codes cite the principle in [principles.md](principles.md).

`[BOARD]` means the rule can only be passed by a measurement on the hardware. `[HUMAN]` means it
also needs a person with the hardware in hand. Static reading of a rule with either tag reports
**not verified**, never pass. Provenance marks (`[source]`, `[AKOS]`) are defined in the
principles. Project figures sit in one labelled section at the end, so the rules stay valid for
any MicroPython project.

## Evidence

- MPY1. [BOARD] A claim about timing, heap, or latency states value, firmware version, commit,
  scene or load, and sample count. A claim without those is reported as unmeasured. `[AKOS]` (P1)
- MPY2. HOST and BOARD results are kept in separate columns or records, and a simulator result
  is HOST even when it models the board. No BOARD entry is filled from a HOST run. `[AKOS]` (P2)
- MPY3. [BOARD] A benchmark reports median and worst, not a mean, over enough passes to catch a
  spike, and says whether it collected first. A bench that calls `gc.collect()` before timing
  and then stops describes the best case. `[AKOS]` (P1, P6)

## Allocation

- MPY4. [BOARD] The per-frame path allocates nothing, or its allocation is measured and accepted
  in writing. Proved by running one real pass inside `micropython.heap_lock()`: any allocation
  raises `MemoryError` at the line responsible. `[AKOS]` for the method. (P4)
- MPY5. Buffers used repeatedly are created once and reused. `read()` in a loop becomes
  `readinto()`; a `bytearray` slice that only feeds a call becomes a `memoryview` slice. (P4)
- MPY6. Large permanent buffers are allocated early, after imports and a `gc.collect()`, and
  before anything has had a chance to fragment the heap. (P5)
- MPY7. Text built per frame by `+`, f-string, or `format` is cached until its inputs change, or
  drawn from bytes. Literals are written as one literal, not concatenated at run time. (P4)
- MPY8. No hot path computes with integers outside the small-int range of -2**30 to 2**30-1.
  Those are heap objects, and millisecond wall-clock values and CRC results land there. (P4)
- MPY9. Work a firmware routine can do is not done by a Python loop. A chain of fallbacks that
  ends in a Python loop announces the fallback, because a silent one costs seconds on the board
  and nothing on the host, where the fast routine exists. `[AKOS]` (P4, P11)
- MPY10. A native or viper routine that can outlast the frame budget calls `time.sleep(0)` at
  intervals, since scheduled callbacks do not run inside native code. Viper pointers have no
  bounds checks, so the caller proves the length before the loop. (P8)

## Heap accounting

- MPY11. A load that can exceed free memory treats `MemoryError` as an expected path: evict and
  retry, take the fallback asset, or try the other save. A bare crash is a finding. `[AKOS]` (P5)
- MPY12. [BOARD] Diagnostics report the Python heap and the ESP-IDF heap separately, at the
  scene with the highest occupancy. The Python side includes the largest free block
  (`micropython.mem_info()`, "max free sz" `[source]`), since `gc.mem_free()` alone is a total,
  and on this port it includes memory not yet added to the heap. (P5)
- MPY13. [BOARD] Data that grows with content or play time has a measured cost per item on the
  board, and a stated limit. A host `sys.getsizeof` is not that cost. `[AKOS]` (P1, P11)

## Collection

- MPY14. The project states in one place where `gc.collect()` is allowed (load, scene change,
  idle) and where it is forbidden. A collect with no entry in that statement is a finding.
  `[AKOS]` (P6)
- MPY15. No `gc.collect()` sits in the per-frame loop or the input path unless a board number in
  a comment or record shows it fits the budget. `[AKOS]` (P6)
- MPY16. [BOARD] The worst collection pause is measured at real occupancy, on the scene with the
  most live objects, and measured again when the heap grows materially. `[AKOS]` (P3, P6)
- MPY17. [BOARD] Automatic collection can still fire anywhere, so every continuous consumer fed
  from Python, such as an audio ring, holds more than the worst measured stall. The sizing
  cites that number. `[AKOS]` (P6)
- MPY18. `gc.threshold()` is set only with a recorded reason: it is a heuristic whose effect
  varies by application. `gc.disable()` needs a guaranteed collect elsewhere, because with
  automatic collection off a failed allocation does not collect first `[source]`. (P6)

## Interrupt handlers

- MPY19. A handler does bounded work: read the hardware, store into a preallocated slot, leave.
  No loops, no waiting, no `print`, no filesystem call, which is not reentrant. Bus access
  only with a measured duration. (P7)
- MPY20. A handler creates no objects: no floats, list appends, large integers, memoryview
  slices, or bound methods. Bound methods are cached in the constructor. Soft callbacks on esp32
  may allocate; AKOS keeps the rule there, since a 10 ms timer that allocates is a hot path and
  code moves between ports. `[AKOS]` for that extension. (P4, P7)
- MPY21. A program that registers callbacks calls
  `micropython.alloc_emergency_exception_buf(100)` early. Handlers catch their own exceptions,
  because an unhandled one disables the interrupt and never reaches the main loop. (P7)
- MPY22. Globals and dict keys a handler touches exist before interrupts start. Handlers write
  only values into existing slots and never add or delete keys. (P9)
- MPY23. Related values shared with a handler pass through a ring buffer, or a short
  `machine.disable_irq()` section whose state is restored. `n += 1` on a shared value in the
  main loop is a race and a finding. (P9)
- MPY24. [BOARD] Input that must survive a stall is captured by hardware, such as
  `machine.Counter` on PCNT with a filter, and reconciled in the main loop. A Python timer or
  pin callback does not qualify. `Pin.irq` has no `hard` parameter on esp32 at v1.28 and
  v1.29 `[source]`, and `hard=True` on `Timer` raises `ValueError`. `Counter.value()` may
  allocate, so it is read from the main loop. `[AKOS]` (P8)
- MPY25. The scheduler queue is finite: depth 8 on esp32 `[source]`. `micropython.schedule()`
  raises `RuntimeError` when it is full, so the call is guarded. The port's pin handler ignores
  the failed queueing and the edge is lost silently `[source]`, so a bouncing input is
  filtered before it reaches a callback. (P8)
- MPY26. [HUMAN] Input is accepted on a scripted run with real buttons and the system busy on
  purpose (collection, card read, save), counting pressed, received, lost, and doubled. A
  driven pin or a simulator is a HOST result. The known limit, such as two presses inside
  one stall, is written down. `[AKOS]` (P1, P8)

## Time

- MPY27. Tick values are compared and offset only through `ticks_diff` and `ticks_add`. Direct
  `+`, `-`, `<`, or `>` on a tick is a finding. (P17)
- MPY28. A stored tick is never compared after half a period. That is about 6.2 days on esp32,
  where `ticks_ms` wraps every 2**30 ms `[source]`; `ticks_add(0, -1)` confirms it. A device
  that stays on for weeks unwraps ticks into a monotonic count at one point. `[AKOS]` (P17)
- MPY29. Wall-clock time is treated as absent until set, and code handles a boot with no NTP
  or RTC. Timestamps stay integers and never pass through `float()`: the esp32 port uses 32-bit
  floats `[source]`, and the epoch is 2000 on embedded ports, not 1970. (P11, P17)

## Portable core

- MPY30. The core imports no platform module. A check fails the build if `machine`, `esp32`, or
  a platform package appears under it, and time arrives as an argument. `[AKOS]` (P10)
- MPY31. Every core change runs both the CPython suite and a MicroPython gate, at the firmware's
  version. The commit or log shows both. Either one alone is an incomplete run. `[AKOS]` (P10)
- MPY32. [BOARD] The gate goes past import. Compiling with `mpy-cross` catches syntax and importing
  catches missing modules, but missing functions and class-level failures appear at run time.
  So construction, save, load, and rarely reached paths are executed under MicroPython, and on
  the board before a release. `[AKOS]` (P11)
- MPY33. Missing standard modules ship as local stand-ins. A built-in is extended by a
  same-named module on the path, only for the modules the documentation lists as extensible, and
  the module reaches the built-in with the `sys.path` method rather than a `u`-prefixed name.
  Patching attributes of a built-in module is a finding. (P11)
- MPY34. Core code avoids the constructs in the trap table in
  [decision-framework.md](decision-framework.md), or carries the board-safe form. `[AKOS]` (P11)
- MPY35. Recursion in shared code has a bound shown on the board, measured with
  `micropython.stack_use()`. The main task has a 16 KB stack on esp32 `[source]`, against
  CPython's thousand frames. `[AKOS]` (P11)

## Saves and files

- MPY36 ★. A save never overwrites the only complete state. The new version is fully written
  and closed in a separate file or the older of two slots before the previous one stops
  being readable. `os.sync()` reaches FAT volumes only on this port `[source]`, so it cannot
  stand in for closing the file. (P12)
- MPY37. The write path names its filesystem's replace behaviour, confirmed by a smoke test on
  that filesystem. LittleFS replaces an existing file in one step on rename. The FAT driver
  unlinks the target, then renames, leaving an instant with no target `[source]`. `os.replace`
  and `os.fsync` do not exist, and a rename cannot cross filesystems. An `os.remove` before a
  rename on LittleFS throws away atomicity and is a finding unless a second valid copy exists.
  (P13)
- MPY38 ★. State lives in two copies with a monotonic counter and a CRC over header and body.
  Load takes the newest copy that passes every check. A copy that cannot be read, fails
  validation, or raises `MemoryError` falls through to the other. A read failure with no valid
  copy stops short of creating a new game over the old files. `[AKOS]` (P12, P14)
- MPY39 ★. Data from a card or file is validated before use: size bounded before reading,
  magic, version and length checked, then structure, ranges, and scale checked **before** any
  expansion or loop driven by a stored value. A CRC is never treated as proof of origin. (P14)
- MPY40 ★. Nothing on a removable card can execute. No card path on `sys.path`, no `.mpy` or
  `.py` loaded from it, no `exec` or `eval` of its content. `[AKOS]` (P14)
- MPY41. [BOARD] The save has a size budget enforced by a test at the late-game maximum, and the
  time of a save at that size is measured. A save long enough to drop input is moved
  out of the play path. `[AKOS]` (P1, P12)
- MPY42. Frequent saves on FAT are a recorded decision with a stated loss window and a bounded
  interval to a LittleFS copy, since the documentation places changing data on littlefs. (P13)
- MPY43. A failed save is visible. Play continues, and the screen or diagnostics say the game is
  not being saved. Silent loss is a floor failure. `[AKOS]` (P12)
- MPY44. [HUMAN] A power-loss claim rests on real removal of power during a write, repeated and
  counted, with the recovered state checked: CRC good, counter not regressed, at most the
  in-flight save lost. A reset issued by software is reported as a reset test, under that name,
  and a reset from a `Timer` callback cannot land inside a blocking C write. `[AKOS]` (P15)

## Crash recovery

- MPY45. An uncaught exception ends in a logged, size-bounded line and a reset, not the prompt.
  Repeated crashes soon after boot go to a recovery path, and a boot-time load failure cannot
  loop forever. `[AKOS]` (P16)
- MPY46. The watchdog is a recorded decision. If used, its timeout exceeds the worst measured
  stall (1 s is the esp32 minimum), it is fed from the main loop after a health check and never
  from a timer callback, and USB work accounts for it, since a running `WDT` cannot be
  stopped. If not used, the hang it would catch is listed as a known gap. What the binary's own
  watchdogs do is IDF23 to IDF26 in the sibling pack. `[AKOS]` (P16)
- MPY47. `main.py` stays small and imports the game inside a guard, so a broken module, a bad
  `.mpy`, or a failed import still reaches the recovery path. Recovery code does not import what
  it repairs. Updates and their boot layer follow IDF43 to IDF45 in
  [embedded/esp-idf](../esp-idf/README.md). `[AKOS]` (P16)

## Deployment

- MPY48. `mpy-cross` is pinned to the firmware. The build checks its version, and the board's
  `sys.implementation._mpy` is compared against what was built. Code with viper or native
  functions is compiled with the matching `-march`. (P18)
- MPY49. A deployment is verified by content hash, not size. `mpremote cp` writes in place with no
  atomic swap, so a cut mid-deploy has a documented recovery. `[AKOS]` (P18)
- MPY50. [BOARD] Release validation runs from a reset, through the stored `main.py`, on the
  deployed bytecode. `mpremote run` and `mount` do not test what boots, and `mpremote` no longer
  soft-resets by default, so earlier state can mask a fault. (P18)
