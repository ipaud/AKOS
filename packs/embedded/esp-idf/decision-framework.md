# Decision Framework — ESP-IDF Pack

The choices this domain presents, and how to settle each one.

## Which rule groups apply?

MicroPython on this chip does load this pack, for the groups marked below. What lives in a Python
file is [embedded/micropython](../micropython/README.md)'s. What lives in the chip, the bootloader,
or the flash layout stays here.

| Group | C on ESP-IDF | MicroPython on top | Why |
|---|---|---|---|
| Evidence, IDF1–IDF4 | Binds | Binds | Measurements do not transfer between boards. |
| Memory placement, IDF5–IDF11 | Binds | C only | Heap under MicroPython is the sibling's; the placement choices were made when the runtime was built. |
| DMA, IDF12–IDF14 | Binds | C only | Descriptor placement concerns your own code. A native module you write is C and comes back here. |
| IRAM, flash cache, IDF15–IDF18 | Binds | C only | Attributes exist only in C. |
| Tasks, IDF19–IDF22 | Binds | C only | The runtime owns its tasks. |
| Watchdogs, IDF23–IDF26 | Binds | **Binds** | They are chip and bootloader behaviour. Know what your binary was built with; the Python API is the sibling's. |
| Stacks, faults, IDF27–IDF29 | Binds | C only | Evidence of a crash still matters, through IDF49. |
| Storage code, IDF30–IDF34 | Binds | C only | Filesystem rules are the sibling's. The floor of P9 applies to both. |
| OTA partitions, IDF35–IDF41 | Binds | **Binds** | If the runtime is replaced through app partitions, these are the rules. If it is not, the answer to "how do we fix the runtime?" is a USB cable; say so. |
| File-based updates, IDF42–IDF45 | Binds if used | **Binds** | What ESP-IDF does not cover is a platform fact, whichever language installs the files. |
| Out of reach, IDF46–IDF50 | Binds | **Binds** | The device does not care what language failed. |
| Secure Boot, Flash Encryption, eFuses, IDF51–IDF58 | Binds | **Binds** | Same chip, same fuses, same irreversibility. |
| Brownout and power, IDF59–IDF61 | Binds | **Binds** | Hardware behaviour. |
| Build, IDF62–IDF63 | Binds | **IDF62 binds** | A prebuilt binary is a version to record. IDF63 returns once you build your own. |
| Frame budgets, IDF64 | Binds | C only | Runtime cost under MicroPython is the sibling's. |

**One catch for prebuilt runtimes:** rollback, Secure Boot, and Flash Encryption depend on how the
bootloader and image were built. On a stock binary those rules become questions about what it
already is, and changing the answer means building your own firmware. Read the partition table of the installed binary rather than assume it has OTA slots;
this pack did not verify any stock MicroPython layout.

## Where does this data live?

Applies to C firmware. Work down, and stop at the first measurement.

```
1. Does a DMA engine or an IRAM-safe ISR touch it?  → internal RAM, no debate (IDF12, IDF15)
2. Is there a measurement on THIS board?            → it decides (IDF1, IDF3)
3. Touched per pixel or per sample, under the cache size? → prior: internal
4. Large, read-mostly, walked in bursts?            → prior: PSRAM, then measure (IDF8)
5. Written by one core, read by the other, per frame? → measure before believing (IDF9)
6. Still no number?                                 → say "no measurement" (IDF4)
```

A prior is a place to start. The usual trap on this chip is not PSRAM being slow; it is internal RAM
running out and stopping the radio.

## Before anything irreversible

The gate for eFuse burns, key revocation, and publishing to devices out of reach. Any "no" stops
the procedure, and a procedure missing any of these is CRITICAL (IDF46, IDF51).

```
1. Is every step written, in order, with the exact command?
2. Has it run on a sacrificial board of the same MODEL, deliberately broken afterwards?
3. Does each step name what recovery remains after it?
4. Are keys backed up, and has the backup been restored once?
5. Was the state saved before (espefuse summary, flash image, partition table)?
6. Is power guaranteed? Not on a battery (IDF55).
7. Is the person doing this able to stop at any step and know what state it is in?
```

## Development or release?

| Concern | Development | Release |
|---|---|---|
| Flash Encryption | Development mode, on boards you own | Release mode, per-device key (IDF53) |
| ROM download | Enabled | Secure, or disabled only with OTA proven as sole recovery (IDF56) |
| JTAG | Open on unfused boards | Off; the `ALLOW_JTAG` option is absent |
| Signing key | Throwaway | Offline or remote, backed up (IDF52) |
| Task watchdog | Warn, for backtraces | Decided and recorded (IDF23) |
| Stack and heap checks | Stronger options on | Canary at least (IDF28) |
| Images | May never reach a customer | Built clean, verified before flash (IDF58, IDF63) |

Secure Boot has no separate development mode in the pages read. Once enabled, it stays on a board
for good, so a "test" enablement on a real device is a release decision.

## Warn or reset on a task watchdog timeout?

- A person is at the device and a backtrace is worth more than recovery: warn.
- Nobody will be there, or a stall costs more than a reboot: reset, with long erases handled
  (IDF25).
- A version is unconfirmed: reset, or use a timer, at least until it confirms (IDF38).

Record the choice. The default was chosen by nobody on your project.

## Which update mechanism?

Two different mechanisms carry the same name. A MicroPython game that updates its own files uses the
second one: its code never touches an app partition. The table says what each inherits.

| Guarantee | App partitions (`esp_ota_*`) | Application files on a filesystem |
|---|---|---|
| Image validated before selection | Yes, at `esp_ota_end` | **No.** Rebuild with per-file hashes (IDF44). |
| Signature check with Secure Boot | Yes, at update and every boot | **No.** Secure Boot never sees these files (IDF54). |
| Power-safe selection of what boots | Yes, two-sector `otadata` | **No.** State files in the fixed layer (IDF45). |
| Automatic rollback | Yes, if enabled in the bootloader | **No.** Trial counter in the fixed layer (IDF38). |
| Running code cannot be overwritten | Yes, conflict error | **No.** Files are replaced in place, so the fixed layer enforces it by path (IDF43). |
| Anti-rollback | eFuse-backed, apps only | **No.** A version file, which flash write access can change. |
| Flash Encryption | App partitions by default | Only if the data partition is flagged `encrypted`; runtime compatibility is unverified here. |
| Whole second copy of the code | Yes, a slot | Often no room, so updates are per file, which makes a mixed state possible (IDF45). |

**Unchanged in both:** the bootloader cannot be updated over the air. File updates cannot repair the
runtime or anything below it, so a fault there needs a partition update or a cable. Brownout and
hardware watchdog behaviour stay as they are.

**Choose files** when flash cannot hold a second copy, the code is interpreted, and the fixed layer
can stay small. **Choose partitions** when you build your own image and want the platform's
guarantees rather than a rewrite of them. Doing both is legitimate, and each needs its own rules.

## May this device leave your hands?

For a device given away, beyond USB, and updated over the air. All three must exist first, because
adding one later relies on the path it protects (IDF47).

1. **Health confirmation**, including that the next update can be fetched (IDF48).
2. **Automatic rollback**, including from a hang, with no knowledge expected of the recipient (IDF38).
3. **Diagnosis with no cable**, in the fixed layer, that the recipient can read out or photograph
   (IDF49).

Then, for each published update: same-model rehearsal from the version in the field (IDF46). And
keep the rehearsal's board. It is the only cable you still have.

## Apparent conflicts

| Apparent conflict | Resolution |
|---|---|
| Guide cautious on PSRAM, board measured it fine | The measurement governs that board and case (IDF3). |
| Guide says authenticate the TLS server; the runtime has no certificate store | A "should": deviation recorded, signature carries the trust (IDF44). |
| Guide suggests disabling ROM download for production; a project keeps Secure mode for recovery | Recovery wins if recorded and that mode is proven on the board (IDF56). |
| Saving RAM versus keeping flash-driver code | A board run decides, not a Kconfig help text (IDF11). |
| A watchdog would catch hangs, but one cannot be stopped for USB work | Keep development usable, and do not ship the conflict: arm it only in the production layer or use a timer (IDF38). |
| Security wants a key the recovery plan needs | Secrets stay protected, and recovery uses a signed path. If none exists, the device is not ready. |

## Profile modulation

- **Prototype** — floor rules on any board you would mind losing, plus IDF1–IDF4. Nothing burned.
- **Game Dev** — the same, plus budgets (IDF5, IDF6, IDF64) and storage integrity.
- **Production** — full checklist, every `[board]` rule run and recorded.
- **Given-away device** — Production, plus IDF42–IDF50, even for a single unit. One unit means no
  second chance, not less rigor.

## When NOT to use this pack

- **Another chip family.** Nothing here transfers by analogy.
- **MicroPython heap, interrupts, or filesystem questions.** Those belong to the
  [sibling pack](../micropython/README.md).
- **The desktop or WASM build of the same engine.** No PSRAM, no fuses.
- **Game design, or whether a game is fun.** Not firmware.
- **"What is the API for X?"** Look it up in the guide.
