# Scoring Rubric — MicroPython Pack

Feeds the performance, maintainability, and overall dimensions
([scoring/performance-score.md](../../../scoring/performance-score.md),
[scoring/maintainability-score.md](../../../scoring/maintainability-score.md),
[scoring/overall-score.md](../../../scoring/overall-score.md)). Chip-level findings score under
[embedded/esp-idf](../esp-idf/README.md), never twice.

This rubric deliberately refuses one thing: it will not let a score stand in for a measurement.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| A step of a save overwrites the only complete state | −40 (CRITICAL) |
| No fall-through to a second copy, or a read failure starts a new game over old files | −40 (CRITICAL) |
| Data from a card used before validation, or a CRC treated as proof of origin | −40 (CRITICAL) |
| Anything on a removable card can execute | −40 (CRITICAL) |
| Runtime claim stated with no board evidence, or a HOST result filed as BOARD | −15 (HIGH) |
| Core change with only one runtime checked | −10 (HIGH) |
| `gc.collect()` in the frame loop or input path with no board number | −10 (HIGH) |
| Filesystem call, loop, or object creation in a handler | −10 (HIGH) |
| Shared read-modify-write, or unprotected multi-value state, with a handler | −10 (HIGH) |
| Must-not-lose input resting on a Python callback or polling alone | −10 (HIGH) |
| `os.remove` before rename on LittleFS with no second valid copy, or rename behaviour assumed | −10 (HIGH) |
| A software reset reported as a power cut | −10 (HIGH) |
| A failed save that nobody is told about | −10 (HIGH) |
| A crash that can end at the prompt, or an endless boot loop | −10 (HIGH) |
| No stated collection policy | −6 (MEDIUM) |
| Audio or other continuous consumer not sized against a measured stall | −6 (MEDIUM) |
| Ticks compared directly, or stored past half a period on a long-running device | −6 (MEDIUM) |
| Timestamps through `float()`, or a wall clock assumed present | −6 (MEDIUM) |
| Core imports a platform, or trap-table constructs without the board-safe form | −6 (MEDIUM) |
| `MemoryError` on a large load crashes instead of falling back | −6 (MEDIUM) |
| Slow Python loop silently replacing a firmware routine | −6 (MEDIUM) |
| Per-frame allocation neither removed nor accepted in writing | −4 (MEDIUM) |
| Diagnostics show one heap, or a total without the largest block | −4 (MEDIUM) |
| Handler globals created late, or `schedule()` failure unhandled | −4 (MEDIUM) |
| Frequent FAT saves with no recorded loss window | −4 (MEDIUM) |
| Watchdog not decided, or fed from a timer | −4 (MEDIUM) |
| `mpy-cross` not pinned, or deploy verified by size | −4 (MEDIUM) |
| Mean-only benchmark, or no worst-frame figure | −2 (LOW) |
| Unbounded recursion in shared code, or a patched built-in | −2 (LOW) |

## Caps and floors

These are the point of the rubric. Each cap applies regardless of the arithmetic.

- **Any CRITICAL:** score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md). All four are safety floor.
- **No board record at all, for code that runs on a board: score ≤ 69**, and the report says
  **not verified on hardware**. Reading code cannot earn Acceptable for runtime behaviour.
- **A save system with no real power removal: score ≤ 79.** Reset tests count for something and
  never reach Good on their own.
- **Button or timer input not tested with real hardware under load: score ≤ 79.**
- **Board records older than the commit under review, on anything they measured: score ≤ 79**,
  and the report names the commit they came from.
- **Not verified is not a deduction.** An unrun `[BOARD]` or `[HUMAN]` item costs no points and
  earns none. The caps carry its weight, and a confident finding still needs its evidence.
- **No deduction rests on a performance target.** A slow number is a finding only against that
  project's stated budget, because this pack states none.

## `n/a` conditions

- **`n/a` when nothing runs on MicroPython.** CPython alone scores `n/a`, not a low number.
- **Host-only portable core, with no board in the project yet:** portable-core rules are scored,
  everything needing the board is `n/a`, and the report says so.
- **`n/a` for save rules when nothing persists.**
- **`n/a` for handler rules when no callback is registered.**
- **`n/a` under Prototype,** except the floor items when the prototype stores anything a person
  would miss.

## Anchors

- **95** — floor clean; real power removal and real-button runs recorded against this commit;
  worst frame and worst pause measured; a stated collection policy; dual gate in every log.
- **85** — sound, with board evidence for the main risks, and MEDIUM gaps scheduled.
- **79** — the likely ceiling for honest, careful work whose hardware tests are incomplete.
- **69** — clean on reading, with no record from the board.
- **≤ 59** — a save can destroy the last good state, or a card can feed the game unchecked data.
