# Glossary — MicroPython Pack

Terms this pack uses precisely. Several are used loosely elsewhere; the entry says which sense is
meant here.

- **HOST** — any run on a development machine: CPython suite, unix port, or simulator, even one
  that models the board's timings. Never evidence for BOARD.
- **BOARD** — a run on the target hardware, on stated firmware and commit, with the result recorded.
- **HUMAN** — a BOARD result that needs a person: real buttons, or pulling the power.
- **Not verified** — the honest result of a `[BOARD]` or `[HUMAN]` item with no record. It is not a
  pass, and not a failure.
- **Portable core** — code that runs unchanged on CPython and MicroPython, imports no platform,
  and is checked on both after every change. A position, not a coincidence.
- **Gate** — one automatic check a change must pass. Here: compile with `mpy-cross`, import under
  MicroPython, execute under MicroPython.
- **Unix port** — MicroPython built for a desktop OS. Same language, but a POSIX filesystem, a
  different heap, and its own epoch rules. It finds missing modules, and not much about the board.
- **Heap** — on esp32 there are two: Python's, managed by the collector, and ESP-IDF's, used by
  WiFi, Bluetooth, and drivers. The word alone is ambiguous here.
- **Split heap** — this port starts with a small Python heap and adds regions on demand, so
  `gc.mem_free()` can include memory not yet added to the heap.
- **Fragmentation** — free memory divided into pieces too small for the request. Shows as
  `MemoryError` with plenty reported free.
- **Largest free block** — the biggest single allocation possible right now. Shown as "max free
  sz" in `micropython.mem_info()`.
- **Collection** — one run of the garbage collector. It stops all Python code while it runs.
  **Pause** means its measured duration on the board.
- **Hot path** — code that runs every frame, sample, or tick, including short timer callbacks.
- **Frame budget** — the time a frame may take, set by the project. This pack sets none.
- **Hard handler** — runs in true interrupt context, with the heap locked. Cannot allocate.
  Available on some ports. Not available from Python on esp32 for pins or timers.
- **Soft callback** — queued by the scheduler and run between bytecodes. May allocate. Delayed by
  anything that keeps the interpreter away, which is why it is blind during a stall.
- **Stall** — any period when the interpreter runs no scheduled work: a collection, a blocking C
  call, native code.
- **Scheduler queue** — the finite list of pending soft callbacks, depth 8 on esp32 at v1.28.
- **Ring buffer** — a fixed circular buffer with one writer per index. The default way to pass
  values from a handler to the main loop.
- **Atomic replace** — swapping a file so that a reader, or a reboot, sees either the old content
  or the new, never neither. Provided by LittleFS rename. Not provided by FAT.
- **Slot** — one of two alternating saved copies. **Torn slot** — one left incomplete by an
  interrupted write. Finding one is normal, and the other slot exists for it.
- **Integrity check** — a CRC or similar. Detects accidental damage. Says nothing about who wrote
  the file.
- **Authentication** — proof of origin, needing a secret or a signature. A CRC is not this.
- **Reset test** — interrupting a write with a reset issued by software. The storage stays
  powered, and a reset from a soft callback lands only between bytecodes. Useful, and limited.
- **Power cut** — real removal of power during a write. The only thing this pack calls by that
  name.
- **`.mpy`** — precompiled bytecode tied to a format version. Compatibility is checked at load.
- **Frozen code** — bytecode built into the firmware image and run from flash. Changing it means
  a firmware flash.
- **Stand-in** — a local module supplying a name MicroPython lacks. It may do nothing at all,
  and that is a choice to record.
- **Shadowing** — a same-named module on the path taking priority over an extensible built-in.
- **Half-period limit** — `ticks_diff` is only valid for values less than half a tick period
  apart. About 6.2 days for `ticks_ms` on esp32.
- **Recovery path** — code reached after repeated failure, which depends on as little as possible
  of what it repairs.
