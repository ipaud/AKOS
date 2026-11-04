# Principles — MicroPython Pack

Durable positions on Python running on a microcontroller, with the ESP32-S3 port as the
reference target. This is not an API guide: the documentation is one search away, and an agent
can read it. The `MPY*` codes in [engineering-rules.md](engineering-rules.md) derive from these.

**Provenance marks, used through the whole pack.** Unmarked statements restate the position of
MicroPython's documentation. `[source]` means the documentation is silent and the fact was read
in MicroPython's source at the tags listed in [references.md](references.md). `[AKOS]` means
synthesis from real projects: AKOS's own position, not MicroPython's.

## What counts as evidence

- **P1 — The board is the only witness for anything that happens on the board.** A statement
  about redraw time, a collection pause, free heap, or input latency needs a number taken on the
  hardware, with firmware and commit named. Reading code can flag a risk. It cannot clear one.
  `[AKOS]`
- **P2 — HOST never counts for BOARD.** A green CPython suite, a green unix-port run, and a
  simulator with a "board mode" all prove logic. None of them proves anything about the heap,
  the scheduler, a filesystem driver, or a pause. A simulator's numbers are the simulator's
  guess about the board. `[AKOS]`
- **P3 — A number in the documentation has a home, and it is not your board.** The documented
  collection cost is stated for the Pyboard, where a collection with little work takes about a
  millisecond. A heap of several megabytes on PSRAM has been measured two to three orders of
  magnitude above that. The documentation tells you the mechanism; only the board tells you the
  size. `[AKOS]`

## Memory

- **P4 — Allocation is a time cost before it is a space cost.** Creating or growing an object
  in a loop is slow on its own, and each allocation moves the next collection closer. Reuse of
  a preallocated buffer removes both costs at once.
- **P5 — Free memory is not allocatable memory.** A heap can report plenty free and still fail
  a large request, because what is free is in small pieces. On this port there are also two
  heaps: Python's, and the one ESP-IDF keeps for WiFi, Bluetooth and drivers. A healthy reading
  from one says nothing about the other.
- **P6 — Garbage collection is a frame-budget event, and the program owns when it happens.**
  Left alone, a collection lands wherever an allocation fails, which is usually the moment
  you least want it. The documentation's answer is to collect at chosen moments. On a large
  heap that answer has a price: a collection in the wrong place costs seconds of frames, so a
  project must state where collection is allowed and what it costs there. `[AKOS]` for the
  price, docs for the principle.

## Interrupt handlers

- **P7 — A handler does what cannot wait, and nothing else.** Short, bounded, predictable. No
  loops, no waiting, no slow I/O, no objects created. Everything else moves to the main loop.
  This is the sharpest position in the source, and it binds every button and timer in a game.
- **P8 — On the esp32 port, a Python callback is never a real interrupt handler.** Timer
  callbacks are soft by documented statement, and the pin handler only queues the callback
  `[source]`. A queued callback runs between bytecodes, so it cannot run during a collection, a
  blocking C call, or native code. Python therefore cannot observe an event that happens
  inside a stall. Only a peripheral that counts without Python can. `[AKOS]` for the conclusion.
- **P9 — What a handler shares with the main loop is a concurrency problem.** One element of a
  preallocated buffer is safe. Several related values are not, and a read-modify-write on either
  side is a race. Structure changes, such as adding a dict key, can crash a hard handler.

## The portable core

- **P10 — A portable core is a position, not an accident.** Code that must run on CPython and on
  MicroPython is a stated contract: it imports no platform, takes time as an argument, and
  is checked on both runtimes after every change. Skipping either check dissolves the contract
  quietly, because each runtime alone stays green. `[AKOS]`
- **P11 — CPython hides whole classes of board defect.** Integer width, float width, rename
  semantics, missing modules and functions, collection pauses, recursion depth, and memory per
  object are all invisible on a laptop. A host test passing proves nothing about the heap, and
  several of these fail only at run time, on a path nobody has executed yet. `[AKOS]`

## Data integrity

- **P12 — A power cut during a save leaves the previous good state.** This is the floor, not a
  feature. There must be no instant, in any step of a save, at which the last complete state
  has ceased to exist and the new one is not yet complete. `[AKOS]`
- **P13 — Atomicity belongs to the filesystem driver, not to the language.** What `os.rename`
  does to an existing file depends on the driver underneath, and the documentation does not say.
  FAT is not power-fail tolerant and the documentation says so; littlefs is built for it. A
  save design that does not name its filesystem has not been designed. `[AKOS]`, with `[source]`
  for the driver behaviour.
- **P14 — A file read from a card is untrusted input.** Anyone can take the card out and edit it.
  A CRC detects accidents, and anyone can recompute it, so a CRC is not authentication. Passing
  a checksum earns a file the right to be validated, nothing more. `[AKOS]`
- **P15 — A survival test must be able to land inside the write.** A reset that can only fire
  between Python statements never lands inside a C write, and a software reset leaves the
  storage powered. Neither is a power cut, and calling it one turns a strong-sounding number into
  false assurance. `[AKOS]`

## Time, crashes, deployment

- **P16 — A crash has to land somewhere.** On a device nobody will debug, the REPL prompt is a
  dead end. Every failure ends in a reset, a fallback, or a recovery screen, and whatever does
  the repairing is never delivered by what it repairs. `[AKOS]`
- **P17 — Time on a board is relative until proven otherwise.** Tick counters wrap, their
  differences are valid only inside half a period, and without a maintained RTC the wall clock
  may count from power-up. A board has no reason to know what day it is.
- **P18 — What was tested must be what boots.** Bytecode is tied to a compiler and firmware, a
  script run over USB leaves the stored program untouched, and state survives across tool
  invocations. Validation that skips the boot path validates something else. `[AKOS]`

## Scope

This pack covers Python on a microcontroller: heap, fragmentation and collection, allocation in
hot paths, interrupt handlers, timing, bytecode and frozen code, filesystem behaviour on internal
flash and SD, crash recovery, and keeping a core portable between CPython and MicroPython.

It does not cover the chip underneath. DMA placement, cache behaviour, secure boot, flash
encryption, eFuses, OTA partitions, and update installation, including updates made of files,
belong to [embedded/esp-idf](../esp-idf/README.md), as does what the binary's own watchdogs do.
That pack's IDF evidence rules bind here too. This pack owns the Python-facing side only:
`machine.WDT`, and the path from `main.py` to recovery. Test strategy in general belongs to
[testing/testing-pyramid](../../testing/testing-pyramid/README.md).
