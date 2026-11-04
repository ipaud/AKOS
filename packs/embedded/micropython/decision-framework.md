# Decision Framework — MicroPython Pack

The choices this domain presents, and how to settle each one.

## What can this evidence prove?

Find the claim, read across. Evidence to the left of what a claim needs does not support it.

| Claim | Reading | CPython suite | Unix port | Board | Person with board |
|---|---|---|---|---|---|
| Game logic is right | flags | **proves** | proves | proves | |
| Syntax and imports work on MicroPython | flags | no | **proves** | proves | |
| A code path runs on MicroPython | flags | no | partly | **proves** | |
| Frame time, collection pause, free heap | flags | no | no | **proves** | |
| Handler timing, lost events from a driven pin | flags | no | no | **proves** | |
| Filesystem behaviour | flags | no | no (it is POSIX there) | **proves** | |
| Reset recovery | flags | no | no | **proves** | |
| Real buttons under load | flags | no | no | no | **proves** |
| Power-cut survival | flags | no | no | no | **proves** |

The unix port shares the language, not the conditions: its files are POSIX and its heap is
unlike the board's. A simulator counts as the CPython column, whatever it models.

## The CPython trap table

Where a host run stays green and the board does not. Check this on every core change (MPY34).

| Trap | On CPython | On MicroPython (esp32 port) | Board-safe form |
|---|---|---|---|
| Large integers | no visible cost | outside ±2**30 is a heap object | keep hot values small; `array` for stores |
| Array overflow | raises | truncates silently: 257 in `'b'` becomes 1 | range-check before storing |
| Float width | 64-bit | 32-bit `[source]`; timestamps lose seconds | integers for anything time-like |
| `time.time()` | float, epoch 1970 | integer, epoch 2000 | never assume; use the platform clock |
| `os.replace`, `os.fsync`, `os.makedirs` | present | absent | see MPY36, MPY37 |
| `os.rename` onto a file | replaces atomically | depends on the driver `[source]` | see MPY37 |
| `except FileNotFoundError` | matches | plain `OSError` with `errno` | compare `errno.ENOENT` |
| `typing`, `dataclasses`, `__future__` | present | absent `[AKOS]`, measured on v1.28 | local stand-ins, MPY33 |
| Missing functions | present | `random.sample`, `time.monotonic` absent `[AKOS]`, measured | shadow module; found only by running |
| Class keyword arguments | work | compile, then fail at run time `[AKOS]`, measured | `if TYPE_CHECKING:` around the class |
| `zlib.crc32` | fast | may be absent; a Python loop costs seconds `[AKOS]` | `binascii.crc32`, loud fallback |
| `__del__` | runs | never called on user classes | `with`, or an explicit close |
| `with` in an unfinished generator | closes | `__exit__` not called | finish the generator, or close by hand |
| `json.dumps(bytes)` | raises `TypeError` | returns a string | validate before encoding |
| `struct.pack` argument count | raises | unchecked | test the round trip |
| `str.ljust`, step slices | work | absent, or `NotImplementedError` | pad by hand; no step slices |
| Resizing under a `memoryview` | `BufferError` | can corrupt the runtime | never resize |
| Recursion | about 1000 frames | 16 KB task stack `[source]` | bound and measure, MPY35 |
| Collection pause | invisible | hundreds of ms on a large heap `[AKOS]` | MPY14 to MPY17 |
| Memory per object | invisible | measured or unknown | MPY13 |

## When is collection allowed to run?

Pick one policy per project and write it down (MPY14). Measure first: time `gc.collect()` on the
board at the busiest scene.

| Worst measured pause | Policy |
|---|---|
| Well under a frame | The documentation's advice fits: frequent explicit collects, each one short. |
| About a frame or more | Collect at named pauses only: load, scene change, idle, sleep. Remove it from the loop. |
| Many frames | As above, plus reduce live objects and allocation rate. Size audio rings past the pause (MPY17), and treat automatic collection as an event that will reach the player. |

**What about the documentation's "collect often"?** It is sound on the heap it was written for,
and collecting often keeps each pass cheap only when little has been allocated. The two projects
found that on a heap of several megabytes the pass itself is expensive, so the advice flips for
the frame loop. Both positions hold, and the board decides which applies. `[AKOS]`

## How is this input captured?

| Must it survive a stall? | Mechanism | Limit |
|---|---|---|
| No, a late or missed event is harmless | Poll in the main loop | Lost if shorter than a frame |
| Should survive normal frames | Timer callback filling a preallocated queue | Runs only when the interpreter does; stops during a collection or blocking call |
| Must survive any stall | Hardware counter reconciled in the main loop | Tells you an edge happened, not when; two presses inside one stall may read as one |

On esp32, every Python callback is scheduled, so the first two rows share the same blind spot. A
hard handler is not an available fourth row at v1.28 and v1.29 `[source]`.

## Where does a save live?

| Option | When | Cost |
|---|---|---|
| Internal flash, LittleFS, two slots | Default. Power-failure resilience is the point. | Slow writes; a large save can stall play. |
| Card, FAT, two slots, with a LittleFS copy at pauses | Saves too slow for flash, and a stated loss window is acceptable | FAT is not power-fail tolerant, and a damaged volume can take the art with it. |
| Card only | Never, for state that matters | Card is removable, and FAT is exposed. |

Whichever is chosen, MPY36 and MPY38 hold, and the decision is recorded (MPY42). The two reference
projects chose differently, on the same board, and both are defensible.

Replacing the file, by filesystem:

```
LittleFS   write aside, close, os.rename onto target           one step, confirm by smoke test
FAT        write aside, close, os.rename                       driver unlinks, then renames
Two slots  overwrite the older slot in place                   no rename at all; CRC finds a torn slot
```

## Source, bytecode, or frozen?

| Form | Use when | Trade-off |
|---|---|---|
| `.py` on the filesystem | Early development | Compiled on import, in RAM; slowest boot |
| `.mpy` on the filesystem | Default for a deployed game | Tied to the compiler version (MPY48); loaded into RAM; replaceable file by file |
| Frozen in firmware | Stable code, small heap, or a shipped device | Runs from flash, saves RAM; each change means a firmware flash, and a file-based update cannot touch it |

On a board with megabytes of PSRAM, the RAM saving may be small, so check whether the real goal
is boot time, or stopping code changes.

## Which pack owns this?

| Question | Pack |
|---|---|
| Heap, collection, handlers, Python timing, file writes from Python, `machine.WDT` | here |
| DMA, IRAM, flash cache, partition layout, secure boot, encryption, eFuses | [esp-idf](../esp-idf/README.md) |
| What a binary's watchdogs do; installing updates, by partition or by file | [esp-idf](../esp-idf/README.md) |
| Evidence rules | both; they agree |
| How much of each test level | [testing-pyramid](../../testing/testing-pyramid/README.md) |

## Profile modulation

- **Prototype** — floor items only if it stores anything a person would miss. Board numbers can
  wait, and the record says they are missing.
- **Startup MVP** — floor, plus a collection policy, a measured worst frame, and the dual gate.
- **Game Dev** — as MVP, plus input under load and real power removal before anyone else plays it.
- **Production** — full checklist, every `[BOARD]` and `[HUMAN]` item recorded against a commit.
- **Enterprise** — plus crash and watchdog decisions reviewed per unit, and pinned toolchains.

The safety floor is the same in all of them.

## When NOT to use this pack

- **Nothing runs on a microcontroller.** It adds nothing to CPython alone.
- **The question is about the chip.** Use [esp-idf](../esp-idf/README.md).
- **A review with no board in reach wants a verdict on runtime behaviour.** Report what reading
  can flag, say what run would settle it, and stop there.
- **You need an API signature.** Read the documentation.
