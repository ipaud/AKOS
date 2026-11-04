# Prompt Fragments — MicroPython Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first: in most
tasks the build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
MICROPYTHON CONSTRAINTS (Level 1 on documented behaviour; [AKOS] items are synthesis from two
real games, not MicroPython's position):

Evidence
- A claim about timing, heap, or latency needs a number from the board: value, firmware,
  commit, scene, sample count. Without one, write "unmeasured".
- HOST never counts for BOARD. A simulator is HOST. Reading code flags risk, never clears it.

Memory and collection
- Nothing allocates in the frame loop unless measured and accepted. Preallocate; readinto();
  memoryview for slices that only feed a call. Check with heap_lock around one real pass.
- Free memory is not allocatable memory: report the largest block and BOTH heaps.
- State where gc.collect() may run: load, scene change, idle. Never in the frame loop or input
  path without a board number. Audio rings must outlast the worst measured pause.

Handlers
- On esp32 every Python callback is scheduled, not a true interrupt. It cannot run during a
  collection, a blocking C call, or native code. Pin.irq has no hard option.
- Do what cannot wait, store into a preallocated slot, leave. No objects, no print, no files.
- Input that must survive a stall is counted by hardware (machine.Counter) and reconciled in
  the main loop.
- alloc_emergency_exception_buf(100). Shared multi-value state goes through a ring buffer.

Portable core
- The core imports no platform and takes time as an argument.
- After every core change: CPython suite AND MicroPython gate. Import is not execution: run
  save, load, and rare paths.
- Ticks only via ticks_diff/ticks_add. Timestamps never pass through float().

Saves (floor)
- Never overwrite the only complete state. Two copies, CRC, counter, newest valid wins.
- os.replace and os.fsync do not exist. LittleFS rename replaces in one step: do not remove
  first. FAT rename unlinks then renames. Confirm with a smoke test on that filesystem.
- A card is untrusted: bound the size, validate structure, range and scale BEFORE expanding
  anything. A CRC is not authentication. Nothing on a card may execute.
- Any failed copy, MemoryError included, falls through to the other copy.

Chip-level questions (DMA, secure boot, OTA, partitions) belong to embedded/esp-idf.
```

## Fragment: review lens

```text
Review this code against the AKOS MicroPython pack (embedded/micropython).

Two rules bind the review itself:

1. NAME THE EVIDENCE. Every finding about behaviour says read, HOST, BOARD, or HUMAN. Reading may
   raise a risk and may never close one. Items tagged [BOARD] or [HUMAN] with no record are
   "not verified", with the run that would settle it. Never write "looks fine" about timing,
   heap, input, or power loss.
2. REPORT THE METHOD, NOT THE CONCLUSION. Write "15 resets from a timer", not "survives power
   cuts". A reset from a Timer on esp32 runs between bytecodes and cannot land inside a C write,
   and the storage stays powered.

Only four findings are CRITICAL, all floor: a save that overwrites the only complete state
(MPY36), no fall-through to a second copy (MPY38), card data used before validation or a CRC
trusted as origin (MPY39), anything on a card that can execute (MPY40).

Then in order: runtime claims with no board record, one-runtime core changes, gc.collect() in
the loop, work or objects in handlers, shared read-modify-write, must-not-lose input on a Python
callback, assumed rename behaviour, silent save failure, crashes that end at the prompt.

Apply the rubric caps: no board record at all, 69 at most; no real power removal or no
real-button test, 79 at most.

For each finding: rule code, file and line, evidence level, and the smallest fix.
```

## Fragment: portable-core gate

```text
This change touches code that runs on CPython and MicroPython. Before calling it done:

1. CPython suite passes.
2. mpy-cross, at the firmware's version, compiles every module.
3. MicroPython at the firmware's version imports every module, with local stand-ins on the path.
4. Check the diff against the trap table: float width, large integers, os.replace, os.fsync,
   except FileNotFoundError, class keyword arguments, __del__, step slices, struct arity,
   ticks arithmetic, timestamps through float().
5. New stdlib calls are executed under MicroPython, not only imported. A missing function
   fails when the line runs.
6. If it touches save, load, or heap-heavy data: run it on the board, and record the numbers.

Report each step as done or not done. Step 6 not done means "not verified on hardware".
```

## Fragment: save-path check

```text
Review this save path. Walk through every step and answer for each: if power goes now, what is
the newest complete state on disk?

- Which filesystem, and what does rename do there? Is that proved by a test on that volume?
- Is there any instant with no complete state? An os.remove before os.rename is such an instant
  unless a second valid copy exists.
- On load: is size bounded before reading? Are structure, range, and scale validated before any
  expansion? Does a failure of any kind, MemoryError included, reach the other copy?
- If both copies fail to read, does it stop rather than create a new game over them?
- How was survival tested? Name the method. Only real power removal during a write counts as a
  power-cut test.
```

## One-liner (for tight token budgets)

```text
MicroPython: a board claim needs a board number; HOST never counts for BOARD, and reading only
flags risk. No allocation in the frame loop; report largest block and both heaps; state where
gc.collect() may run, never in the loop without a measurement. On esp32 all Python callbacks are
scheduled and blind during stalls, so must-not-lose input is counted by hardware. Handlers store
and leave. Core: no platform imports, checked on both runtimes every change, and import is not
execution. Saves: never overwrite the only good state, two copies, name the filesystem's rename
behaviour, validate card data before use, CRC is not authentication, nothing on a card executes.
A reset is not a power cut.
```
