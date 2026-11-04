# Anti-Patterns — MicroPython Pack

Named failure modes, how to spot them, and what to do instead. The examples are invented; real
project evidence stays in [engineering-rules.md](engineering-rules.md). The last two are failures
of *applying* this pack.

## Green on the laptop

**Detect:** a PR saying "tested" whose only record is a CPython run; a board checklist row filled
from a simulator; a core change with no MicroPython gate in the log.
**Why it fails:** the suite runs on 64-bit floats, a POSIX filesystem, and a heap with no pause.
The defects this domain produces cannot occur there.
**Fix:** run both gates, record HOST and BOARD apart, and say which claims are still unmeasured.
(MPY2, MPY31, MPY32)

## The module that imported fine

**Detect:** a port declared working because every module imports; a shim for missing modules
with no run of the code that calls them.
**Why it fails:** missing functions and some class-level failures surface only when the line
executes, which may be the first save, a rare minigame, or week three of a pet's life.
**Fix:** execute construction, save, load, and rare paths under MicroPython, then on the board.
(MPY32, MPY34)

## Collecting every frame

**Detect:** `gc.collect()` inside the main loop, a draw function, or an input handler, usually
added to stop a `MemoryError` or an old pause.
**Why it fails:** on a large heap each pass can cost many frames. The frame rate collapses and
presses arrive late, and the symptom gets blamed on the drawing.
**Fix:** take it out, measure a pass at the busiest scene, and move it to a named pause. (MPY14,
MPY15, MPY16)

## The heap that looked fine

**Detect:** diagnostics print only `gc.mem_free()`; a `MemoryError` or a WiFi failure occurs with
megabytes reported free.
**Why it fails:** the total hides fragmentation, and it says nothing about the ESP-IDF heap that
WiFi and drivers use.
**Fix:** report the largest free block and both heaps, at the scene with most in memory. (MPY6,
MPY12)

## The confident median

**Detect:** a performance note giving one average, from a bench that ran `gc.collect()` first.
**Why it fails:** collection and recompute spikes are what a player feels, and this bench was
built to miss them.
**Fix:** report median and worst, across real scenes, with collection left as it runs in play.
(MPY3)

## Work in the handler

**Detect:** a `Pin.irq` or `Timer` callback that decodes gestures, updates game state, formats a
log line, or opens a file.
**Why it fails:** the callback blocks everything behind it, the queue fills, and on a hard
port it fails outright. Filesystem code is not reentrant, so this can corrupt more than timing.
**Fix:** store the edge and the time in a preallocated slot, decode in the main loop. (MPY19,
MPY20)

## The timer that watches the stall

**Detect:** a design claiming no input is lost because a timer polls every few milliseconds.
**Why it fails:** on esp32 that timer is a scheduled callback. During a collection or a blocking
card read it does not run, so a tap inside the stall leaves no trace.
**Fix:** count edges in a hardware peripheral and reconcile, then test it with real buttons under
deliberate load. (MPY24, MPY26)

## Counting on both sides

**Detect:** `presses += 1` in a callback, and `presses = 0` or `presses -= 1` in the main loop.
**Why it fails:** read-modify-write is not atomic, so updates vanish, rarely enough to
pass every short test.
**Fix:** a ring buffer with one writer per index, or a short critical section. (MPY23)

## Trusting the comment about rename

**Detect:** a code comment stating what rename does, with no smoke test on the filesystem; an
`os.remove(target)` directly before `os.rename(temp, target)` on LittleFS.
**Why it fails:** behaviour varies by driver, and the documentation is silent. The belief that
rename cannot replace leads people to add a delete that opens the very window they wanted
closed.
**Fix:** test it on the real volume, then name the behaviour in the write path. (MPY37)

## The one good file

**Detect:** a save with a single path, written in place, or a settings file treated as disposable
that holds something a person would miss.
**Why it fails:** a cut during the write leaves nothing complete, and a CRC can only report the
loss.
**Fix:** two alternating copies, or write aside and swap. (MPY36, MPY38)

## The checksum that vouched for a stranger

**Detect:** a loader that treats a good CRC as permission to trust content; a stored count
driving a list expansion or a `range()` before any bounds check.
**Why it fails:** anyone with the card can edit the data and recompute the CRC. A forged
`rentals: 90000000` then exhausts memory or hangs the boot, and may do so at every boot.
**Fix:** bound the size, validate structure and scale before expanding, and fall through to
the other slot on any failure, `MemoryError` included. (MPY38, MPY39)

## The reset that was called a power cut

**Detect:** a record reading "survived N power cuts" where the method was `machine.reset()`,
especially from a `Timer`; a checklist row ticked on that basis.
**Why it fails:** the storage stayed powered, and on esp32 a timer callback runs between
bytecodes, so the reset cannot land inside a C write. The test only covers the gaps between
Python statements, and the reassuring number spreads through later documents.
**Fix:** rename it a reset test. Remove power for real, during the write, repeatedly, and count
that separately. (MPY44)

## The hang nobody catches

**Detect:** a shipped device with no watchdog and no record of why; a watchdog fed from a timer.
**Why it fails:** a hang is not an exception, so crash handling never sees it. A timer callback
keeps feeding while the main loop is stuck in Python, which hides the hang the watchdog exists to
catch.
**Fix:** decide and record it. Feed only after the main loop proves health, or list the gap.
(MPY46)

## Tested, but not what boots

**Detect:** release confidence from `mpremote run` or `mount`; a new `.mpy` built by whichever
`mpy-cross` was on the path; a deploy checked by file size.
**Why it fails:** the stored program may differ, bytecode may be incompatible, and a same-sized
file can hold different bytes.
**Fix:** pin the compiler, verify by hash, and validate from a reset. (MPY48, MPY49, MPY50)

## Passing a board from the armchair

**Detect:** a review that says frame rate, input, or power-cut survival "looks fine" with no
board record.
**Why it fails:** code shows intent, not behaviour, and that sentence is what stops anyone
running the test.
**Fix:** report **not verified**, name the run that would settle it, and apply the rubric's cap.
(MPY1, [scoring-rubric](scoring-rubric.md))

## Reviewing the chip from here

**Detect:** findings on DMA, secure boot, or partition tables raised under this pack, or Python
heap findings raised under [esp-idf](../esp-idf/README.md).
**Why it fails:** the rules live elsewhere, and a lens that covers everything covers nothing well.
**Fix:** use the ownership table in the [decision framework](decision-framework.md), "which pack
owns this".
