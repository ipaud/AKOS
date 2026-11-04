# Principles — ESP-IDF Pack

Durable positions on how firmware must behave on ESP32-class chips, with the ESP32-S3 as the
reference target. This is not an API guide: anything an agent can look up stays in the
Programming Guide. The `IDF*` codes in [engineering-rules.md](engineering-rules.md) derive
from these. Principles marked *(AKOS synthesis)* are this pack's own position, not
Espressif's.

## What counts as evidence

- **P1 — On this exact board, a measurement beats doctrine.** Platform guidance on where data
  should live is a prior. A measurement on the board overrides it for that board and that
  case, and only there. The guide is cautious about PSRAM; one board measured tiles there at
  10–13% over internal RAM, and that settles that question on that board and nowhere else.
  *(AKOS synthesis)*
- **P2 — Static reading establishes structure, never a runtime number.** Configuration,
  placement, ordering, and error paths can be read from artifacts. Frame time, contention,
  stack depth, and power-cut survival cannot. A review states which of the two it did.
  *(AKOS synthesis)*
- **P3 — A default is the platform owner's starting point, not your design.** The task
  watchdog warns and carries on, rollback is off, anti-rollback is off. Each is reasonable
  for someone, and none was chosen for your product.
- **P4 — Level 1 covers documented platform behaviour, and stops there.** How the chip,
  bootloader, and ESP-IDF behave is Espressif's to state. How a game should spend a frame,
  or what a gift needs before it leaves the house, is not; that is synthesis and is labelled.

## What cannot be undone

- **P5 — An eFuse has no retry.** A burn is one-way, and some configuration options burn on
  first boot without anyone typing a burn command. The procedure is the safety mechanism:
  rehearsed on a board you are willing to lose, with the way back written first.
- **P6 — Secure Boot, Flash Encryption, and freshness are three separate properties.** Secure
  Boot says the image was signed. It hides nothing. Flash Encryption hides contents and does
  not prove who wrote them. Neither stops an older signed image. Secure Boot verifies the
  bootloader and the app image, so anything the app later interprets from a filesystem is
  outside what it verified.
- **P7 — A signing key is the device's future.** Lost, it ends updates. Leaked, it hands them
  to someone else. Neither can be fixed from a distance.
- **P8 — A device you cannot reach is an irreversible context.** When nobody can plug in a
  cable, every update carries the same risk as an eFuse: a mistake may have no way back. What
  a bad update needs in order to recover has to be on the device before it leaves.
  *(AKOS synthesis)*

## What must survive a power cut

- **P9 — Power can fail between any two instructions.** The last good state stays readable
  through a cut during a save, an update, or a rollback. This is the data-integrity floor and
  no budget trades against it.
- **P10 — Claim atomicity only where someone proved it.** NVS documents tolerance to power
  loss, and `otadata` documents two sectors for that purpose. The FAT page documents neither,
  so nothing is assumed of it. A property proven on one filesystem does not transfer to
  another.
- **P11 — A new version is unproven until it proves itself, and rollback needs a reset to
  fire.** Rollback restores code, not data, and only if something restarts the device. A
  version that hangs politely holds the device hostage until a person intervenes.
  *(the last clause is AKOS synthesis)*

## Memory, time, and the bus

- **P12 — Memory is a placement problem across three unequal regions.** Internal RAM is fast
  and scarce and is the only home for many system needs. PSRAM is large and slower, and it
  shares a cache with flash. Flash is read-mostly and may vanish during a write. Free bytes
  in total say little; the largest free block in the right region says what will succeed.
- **P13 — Whatever an interrupt or DMA engine touches has a location and a lifetime.** A
  handler that outlives the cache, or a buffer changed mid-transfer, fails intermittently and
  far from its cause.
- **P14 — A flash operation is a system event unless you arranged otherwise.** By default the
  caches go off, tasks stop, the other core waits, and non-IRAM interrupts are deferred.
  Execute-in-place from PSRAM changes that, which makes the arrangement a safety dependency
  rather than a tuning choice.
- **P15 — Two cores share one memory bus.** Single-core figures do not add up to a dual-core
  result. Contention exists only as a measurement.

## Detection

- **P16 — A watchdog does what it is configured to do, for what it watches.** By default that
  means printing a warning about idle tasks. Assuming more is a review error.
- **P17 — A fault nobody can read did not happen as far as anyone knows.** Fixed stacks fail
  silently, and a crash on a device in someone's home leaves nothing unless evidence was
  designed in.

## Scope

This pack covers firmware on ESP32-class chips under ESP-IDF, plus the chip and bootloader
layer beneath a MicroPython runtime on the same chips. Heap, interrupts, filesystem, and
runtime behaviour under MicroPython belong to
[embedded/micropython](../micropython/README.md). General C practice, drivers for specific
parts, and API reference are out of scope.
