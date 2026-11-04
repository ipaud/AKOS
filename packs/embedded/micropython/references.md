# References — MicroPython Pack

Attribution only. Nothing here is copied from these sources; the pack is an original operational
distillation, organized by the AKOS file contract rather than by any source's structure.

## Primary sources (Level 1 — platform owner)

- **MicroPython documentation** — MicroPython. https://docs.micropython.org/en/latest/
- **Maximising MicroPython speed** — MicroPython. https://docs.micropython.org/en/latest/reference/speed_python.html
- **MicroPython on microcontrollers** — MicroPython. https://docs.micropython.org/en/latest/reference/constrained.html
- **Writing interrupt handlers** — MicroPython. https://docs.micropython.org/en/latest/reference/isr_rules.html
- **MicroPython differences from CPython** — MicroPython. https://docs.micropython.org/en/latest/genrst/index.html
- **Working with filesystems** — MicroPython. https://docs.micropython.org/en/latest/reference/filesystem.html
- **MicroPython source tree, v1.28.0 and v1.29.0** — MicroPython. https://github.com/micropython/micropython

## Firmware versions

Evidence projects run MicroPython v1.28.0 and v1.29.0, port `ESP32_GENERIC_S3-SPIRAM_OCT`. The latest
release at the time of writing was v1.29.0. The documentation pages are the `latest` build as of
2026-11-04, which can run ahead of a release.

## What Level 1 covers here, and what it does not

MicroPython is the platform owner, on the same basis as other platform documentation at Level 1.
The level covers the documented behaviour of the runtime: the handler rules, heap and collection
mechanisms, the documented differences from CPython, filesystem statements, and the esp32 port's
stated limits. Those are marked by no mark at all.

It covers two more things only with a mark:

- **`[source]`** — where the documentation is silent, behaviour was read in the source at the tags
  below. That is the platform owner's own code, so Level 1 applies, but only at those tags. It is
  implementation, and it can change without notice. Re-check at each firmware upgrade.
- **`[AKOS]`** — synthesis from two real games. It is **not** Level 1, and it is not MicroPython's
  position. The projects are one owner's work on one board class. Treat those statements as
  verified practice, and measure them on your own board.

**Numbers.** The only collection figure in the documentation is about 1 ms on the Pyboard. It
does not describe a heap of megabytes on PSRAM, and this pack does not use it as such. Every
other figure is either from a page listed below, from source, or labelled as a project's own
record. The pack holds no performance targets.

**Silences that matter.** The documentation does not say what `os.rename` does to an existing
file, and does not discuss flash wear, the esp32 hard-interrupt situation for pins, or recursion
limits. The pack says so rather than filling those gaps with assumption. It offers no rule on
flash wear for that reason.

## Pages read, 2026-11-04

Each page was fetched through a tool that returns a model's summary, so the raw text of the
pages below was then downloaded and the claims the rules rest on were checked in it.

**Reference:** `reference/speed_python.html`, `reference/constrained.html`,
`reference/isr_rules.html`, `reference/mpyfiles.html`, `reference/manifest.html`,
`reference/filesystem.html`, `reference/mpremote.html`.

**Differences from CPython:** `genrst/index.html`, `genrst/core_language.html`,
`genrst/builtin_types.html`, `genrst/modules.html`. `genrst/syntax.html` and the per-version
`differences/` pages were not read.

**esp32:** `esp32/quickref.html`, `esp32/general.html`. The latter has almost nothing on memory,
and its specification list describes the original ESP32 rather than the S3.

**Library:** `library/gc.html`, `library/micropython.html`, `library/esp32.html`,
`library/machine.WDT.html`, `library/machine.Pin.html`, `library/machine.Counter.html`,
`library/machine.html` (the `disable_irq` and `reset_cause` entries), `library/time.html`,
`library/os.html`, `library/index.html`, `library/sys.html`, `library/binascii.html`,
`library/vfs.html`.

**Not read:** the `machine.Timer`, `machine.SDCard`, and `machine.I2S` library pages. Timer facts
come from `esp32/quickref.html`. All listed pages loaded; none failed.

## Source read, for `[source]` statements

At tag v1.28.0: `extmod/vfs_fat.c`, `extmod/vfs_lfsx.c`, `extmod/vfs.c`, `extmod/modos.c`,
`extmod/modtime.c`, `ports/esp32/machine_pin.c`, `ports/esp32/machine_timer.c`,
`ports/esp32/main.c`, `ports/esp32/mpconfigport.h`, `py/gc.c`, `py/mpconfig.h`.

At tag v1.29.0, re-checked: `extmod/vfs_fat.c` (FAT rename) and `ports/esp32/machine_pin.c`
(no `hard` argument). All other `[source]` statements are v1.28.0 only.

The LittleFS rename statement also rests on the littlefs project's own `README.md` and `lfs.h`
(rename is atomic through power loss; an existing destination of the same type is replaced), and
on a smoke test run on a real board. The MicroPython documentation notes reports of littlefs failing in certain situations.

## Real-project evidence

Rules were checked read-only against two private MicroPython games on one ESP32-S3 board class. That
reading is not a public source and carries no authority, and findings about those projects stay in them.

**Two corrections this reading produced.** Each is the pack's reason for a rule.

1. *"`os.rename` does not replace an existing file."* One project's code said this while its own
   updater relied on the opposite. At v1.28.0 and v1.29.0 both drivers replace: LittleFS in one
   step, FAT by unlinking and renaming. What is true is that `os.replace` does not exist. See MPY37.
2. *"Survived 15 power cuts during saves."* The record meant `machine.reset()` from a timer. That a
   timer-driven reset cannot land inside a C write is inferred from the scheduler documentation
   and the port source, not observed. See MPY44.

## Gap this pack closes

A grep of `packs/` on 2026-11-04, excluding `packs/embedded/`: `gc.collect`, `littlefs`,
`fragmentation`, `interrupt handler`, `watchdog`, and `bytecode` returned zero files. `micropython`
returned two passing mentions: one personal project note and one games rule. No pack held a
position on any of this.

## Related AKOS packs

[embedded/esp-idf](../esp-idf/README.md) ·
[testing/testing-pyramid](../../testing/testing-pyramid/README.md)
