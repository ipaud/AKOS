# Engineering Rules — ESP-IDF Pack

Checkable in artifacts: `sdkconfig`, partition tables, source, CI, procedures, logs. `★` marks
floor rules: irreversible operations, secrets, and data integrity. `[board]` marks a rule a
person must verify on real hardware; static reading cannot pass it (P2). `*(AKOS)*` marks the
pack's synthesis rather than an Espressif position. Parenthetical codes cite
[principles.md](principles.md). Which groups bind under MicroPython is in
[decision-framework.md](decision-framework.md).

Kconfig defaults quoted here were read from the ESP-IDF v5.4.2 source tree.

## Evidence

- IDF1. A finding about placement, timing, or throughput on a named board cites a measurement
  (file, section, date) or says "no measurement"; a documented prior is called a prior. (P1, P2)
- IDF2. A measurement records its board model, clocks, cache sizes, XIP state, firmware commit,
  and scene. Without those it is an anecdote, and a figure from one board model is never
  applied to another, even on the same chip. (P1)
- IDF3. Where guidance and a board measurement disagree, the measurement governs that board and
  case only, and the record names both. (P1)
- IDF4. No runtime number and no power-cut claim is accepted from static reading. A `[board]`
  rule with no recorded run reports "not verified", not pass. (P2)

## Memory placement

- IDF5. CI fails when the internal RAM left by statics falls below a stated floor read from the
  build's map, and the floor's reason sits beside the check. (P12)
- IDF6. The firmware reports free bytes, largest free block, and low watermark per capability,
  internal and PSRAM, at runtime. A budget on total free bytes is not a budget. (P12)
- IDF7. Every allocation on a runtime path checks for failure and has a defined outcome. A
  failed load does not become a permanent placeholder or a crash two calls later. (P12)
- IDF8. A per-frame path that walks or copies PSRAM data larger than the cache has a measured
  cost; the guide puts the fall to raw PSRAM speed at accesses over 32 KB, and such accesses
  also evict cached flash. `[board]` (P1, P12)
- IDF9. One core writing a PSRAM region while the other reads it at frame rate is accepted only
  on a measurement with both running. `[board]` (P15)
- IDF10. Moving code or data into IRAM or DRAM, resizing a cache, or switching XIP records the
  gain measured and the internal RAM spent. `[board]` (P1, P12)
- IDF11. An option that swaps flash-driver, heap, or ISR-path code to save RAM is not taken
  until a flash erase, a save, and an update have run on the board with a heap integrity check
  after each. A documented trade-off lists only what the documentation knows. `[board]`
  (P3, P9)

## DMA

- IDF12. DMA buffers are `MALLOC_CAP_DMA` or `DMA_ATTR`, 32-bit aligned, a multiple of 4 bytes
  long, and not on a stack. A hot path that relies on the driver's silent copy is a defect.
  `max_transfer_sz` is set explicitly: zero means 4092 bytes with DMA. (P13)
- IDF13. DMA descriptors are never in PSRAM. A PSRAM DMA buffer
  (`MALLOC_CAP_SPIRAM | MALLOC_CAP_DMA`) needs a bandwidth measurement with the CPU also on
  PSRAM. `[board]` (P13, P15)
- IDF14. A buffer and its transaction descriptor stay untouched until the result is collected.
  Code that overlaps DMA with the next frame states who owns each buffer at each moment, and
  polled transactions do not start while queued ones are outstanding. (P13)

## IRAM and flash-cache safety

- IDF15. An ISR registered with `ESP_INTR_FLAG_IRAM` keeps its whole closure in IRAM or DRAM,
  including callees, constants, and strings. An ISR without that flag does not run during a
  flash operation, so its events are lost unless the design tolerates that in writing. (P13, P14)
- IDF16. ISRs do not use `printf`, allocate, block, or use the FPU; they hand work to a task. (P13)
- IDF17. A relaxation that depends on `CONFIG_SPIRAM_XIP_FROM_PSRAM` holds only while the option
  is on in every shipped configuration. If XIP-off is a stated fallback, the ISR set stays safe
  under both. (P14)
- IDF18. `CONFIG_SPI_FLASH_AUTO_SUSPEND` is not enabled without confirmed chip support, nor with
  frequent interrupts such as LCD flush or radio: the guide excludes hard real-time use. (P14)

## Tasks and core affinity

- IDF19. Every long-lived task is created with an explicit core and priority and a stated reason.
  An unpinned `xTaskCreate` in real-time firmware is a finding. (P15)
- IDF20. Latency-critical work is placed against the system task table: the Wi-Fi driver runs at
  priority 23, on core 0 by default. Sharing that core while the radio is active is measured.
  `[board]` (P15)
- IDF21. Exclusion across cores uses mutexes or `portMUX` critical sections, never
  `vTaskSuspendAll` or disabled interrupts. Critical sections are short and make no FreeRTOS or
  blocking call. Tasks delete themselves rather than one running on the other core. (P15)
- IDF22. Work split across cores shares no unsynchronised mutable state and never calls into a
  single-threaded runtime. *(AKOS)* (P15)

## Watchdogs

- IDF23. The task watchdog's outcome is a recorded decision per build. By default it prints a
  warning and a backtrace and carries on (`CONFIG_ESP_TASK_WDT_PANIC` defaults to `n`, the
  timeout to 5 s). A design or review assuming it resets the chip is wrong. (P3, P16)
- IDF24. By default it watches the idle tasks, so a task blocked forever while idle still runs
  goes unseen. A task whose stall matters subscribes. (P16)
- IDF25. Long erases are reckoned with: they can trip the task watchdog, and with panic enabled
  an update would reset itself mid-erase. Timeout or erase strategy is set accordingly. (P16)
- IDF26. The interrupt watchdog and `CONFIG_BOOTLOADER_WDT_ENABLE` stay on. Raising a timeout is
  the last resort, after shortening the critical section or ISR. (P16)

## Stacks and faults

- IDF27. Stack sizes come from high-water marks at peak load plus a margin, logged in the running
  firmware. A reduction without a fresh figure is rejected. `[board]` (P17)
- IDF28. Overflow detection is on and is not treated as complete: neither the canary nor the
  watchpoint catches every overflow. Assertions are not disabled globally. (P17)
- IDF29. A panic leaves evidence readable without a debugger attached: a core dump, a stored
  log, or a screen. `CONFIG_ESP_SYSTEM_PANIC_SILENT_REBOOT` is not used in release. (P17)

## Storage integrity

- IDF30 ★. Persisted state is replaced so that a cut at any point leaves the last good copy
  readable: two generations with a checksum, the older overwritten, the reader taking the newest
  that validates. Overwriting the only copy is CRITICAL. (P9)
- IDF31. A save API that returns before data is durable bounds and states its window, flushes on
  every orderly exit (power-off, game end, low battery), and retries without touching the last
  good copy. (P9)
- IDF32. No filesystem operation is assumed atomic on FAT, whose page is silent on power loss. FAT
  on writable flash goes through wear levelling. With 4096-byte sectors a sector is erased then
  rewritten, so metadata shared by both generations, such as a directory sector, is a common
  point of failure. A claim that saves survive cuts needs a cut test. `[board]` *(AKOS)* (P10)
- IDF33. NVS holds small values and checks `nvs_commit()`. Erasing a partition on
  `ESP_ERR_NVS_NO_FREE_PAGES` is a data-loss decision, not a reflex. Large blobs go elsewhere. (P10)
- IDF34. Flash write rate is bounded by design, and any endurance figure comes from that flash
  part's datasheet. The platform pages read for this pack state none, so none is given. (P9)

## OTA through app partitions

- IDF35. An update writes only the inactive slot, and the boot selection changes only after
  `esp_ota_end` validates the image. Any failure leaves the running image selected. (P9)
- IDF36. `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE` is set before first deployment. It defaults to
  `n`, it lives in the bootloader, and OTA cannot update the bootloader. (P3, P11)
- IDF37. An image confirms itself only after a self-test of what the next update needs, done
  promptly, and of the data it writes: it reopens a fresh save first. Confirming first thing at
  startup defeats rollback. *(AKOS on the data half)* (P11)
- IDF38. An unconfirmed version that hangs reaches a reset with no person involved, through a
  timer or a watchdog set to reset. Rollback fires on a reset, and IDF23 means the default
  watchdog will not supply one. `[board]` *(AKOS)* (P11)
- IDF39 ★. Rollback restores code, not data. A version that writes a format its predecessor cannot
  read keeps the previous data until confirmed, on every volume that holds it: internal flash, a
  card, and any copy between them. *(AKOS)* (P9, P11)
- IDF40. OTA is tested on the board with the production bootloader binary: a valid image, a corrupt
  one, a reset before confirming. CI fails before the image outgrows its slot. `[board]` (P11)
- IDF41. Anti-rollback is a recorded decision. It burns eFuses, the field allows only 16
  increments, and without it any older signed image remains installable. (P5, P6)

## OTA through application files

For a design that replaces files on a filesystem and leaves the app partition alone. The
[decision framework](decision-framework.md) lists what ESP-IDF's OTA does not cover here.

- IDF42. The design states which ESP-IDF guarantees it does not inherit, and rebuilds each one
  it needs. None apply just because the chip offers them. (P6, P11)
- IDF43. The layer that installs, undoes, and reports updates cannot be changed by an update, and
  the device enforces this by path even when a signature is good. Once the device is out of reach
  that layer is as fixed as a bootloader, so it is kept small and tested as one. Its last path resets
  the chip, and never falls through to an interpreter prompt. *(AKOS)* (P8)
- IDF44. Every file is checked against a signed manifest before install, the signature covers the
  version, versions only rise, and a failed version is never retried. A key held on the device
  must not be able to sign for other devices: a shared symmetric key is limited to a recorded
  single-device case. TLS that does not authenticate the server is not authentication, and is
  acceptable only as a recorded deviation with the signature as the trust. No hand-written crypto
  primitives: HMAC built on the platform's SHA-256 is construction, not a hand-written primitive.
  (P6, P7)
- IDF45. Every install and rollback step can repeat after a cut, deletes included, and the swap
  primitive is proven on that filesystem and that board. A folder whose existence carries meaning
  is renamed aside before it is deleted. An unfinished rollback goes before a pending install.
  `[board]` *(AKOS)* (P9, P10)

## Devices out of reach

Devices given away or otherwise beyond a USB cable, updated over the air. All of it is AKOS
synthesis, anchored in Espressif's rollback and diagnostics guidance.

- IDF46 ★. Publishing to a device you cannot reach is treated as an irreversible action. The update
  first runs through the real path on a device of the same model, from the version actually in
  the field. `[board]` (P8)
- IDF47 ★. Health confirmation, automatic rollback, and a diagnosis path exist on the device before
  it leaves. Adding any of them later relies on the update path it was meant to protect. (P8)
- IDF48. Health includes the update channel. A version that cannot fetch the next update is not
  healthy, however long it plays: confirming it makes it permanent. (P8, P11)
- IDF49. Diagnosis works with no USB and no REPL, lives in the fixed layer, and shows what the
  recipient can relay: installed version, last check's outcome, last errors. A tool that needs a
  cable does not count for this device. (P8, P17)
- IDF50. Every dependency of the update channel has a stated lifetime and failure: URL, host, token,
  root certificate, signing key. A certificate or token that expires stops updates silently. (P7, P8)

## Secure Boot, Flash Encryption, and eFuses

- IDF51 ★. No procedure that burns eFuses runs without a written step list, a dry run on a
  sacrificial board of the same model, a recovery path for each step, a verified key backup, and
  `espefuse.py summary` saved before and after. This includes merely enabling an option whose first
  boot burns. A procedure missing any of these is CRITICAL. `[board]` (P5)
- IDF52 ★. Signing keys are never in a repository, an image, a device, CI, or a log, except a
  verification key under the recorded single-device case in IDF44. They are
  generated with a strong entropy source such as OpenSSL, not by the build, and backed up offline,
  with loss and compromise procedures written. Production signing happens off the build machine, or
  the exception is recorded. A CI key is throwaway and its images can never reach a device. (P7)
- IDF53 ★. Development and release are separate modes. Flash Encryption Development mode, labelled
  "NOT SECURE" in Kconfig, never ships on a device leaving the owner's hands; release uses Release
  mode with a per-device key. `CONFIG_SECURE_BOOT_INSECURE`, `CONFIG_SECURE_BOOT_ALLOW_JTAG`, and
  `CONFIG_SECURE_INSECURE_ALLOW_DL_MODE` are absent from the generated release `sdkconfig`. (P5, P6)
- IDF54. The threat each property answers is recorded. Secure Boot alone leaves flash readable
  and exposed to swap-after-check. Partitions not flagged `encrypted` stay readable, and NVS needs
  its own encryption. Secure Boot does not cover files interpreted from a filesystem, so a fixed
  layer counts as signed only if it is built into the signed image. (P6)
- IDF55. Order is planned: read-protected keys before Secure Boot, Flash Encryption before Secure
  Boot in the external workflow, `ENABLE_SECURITY_DOWNLOAD` last. Power stays uninterrupted, and the
  first-boot encryption pass never runs on a battery. (P5, P9)
- IDF56 ★. The ROM download choice is matched to the recovery path before burning: permanently
  disabled leaves OTA as the only way in. On a board with no usable UART, anything touching
  USB-Serial-JTAG is proven on the sacrificial board first; the Secure Boot page does not describe
  that interface. Burning `DIS_DOWNLOAD_MANUAL_ENCRYPT` means any reflash needs images encrypted on
  the host with a held key, so a recovery path relying on it needs that key backed up. `[board]` (P5)
- IDF57. The bootloader is signed with every key needed for the device's life before flashing, and
  unused digest slots are revoked. Aggressive revocation is not enabled without a record, since it
  can brick. Key revocation runs only after rollback has settled. (P5, P7)
- IDF58. Before a provisioning flash, the generated `sdkconfig`, both signature blocks, the
  partition offsets, and the exact printed flash command are checked against the reviewed plan. The
  Secure Boot bootloader limit is 64 KB, and partitions start at least 0x1000 past the table. (P5)

## Power and brownout

- IDF59. The brownout detector stays enabled, its level is a recorded choice, and a brownout reset
  counts as a power cut under IDF30. The levels are approximate and vary between chips. (P9)
- IDF60. The low-battery path finishes its save above the brownout level under real load, on
  filtered readings; the threshold comes from a measurement under load. `[board]` (P9)
- IDF61. Boot reads and records the reset reason, so brownouts, panics, and watchdog resets can be
  told apart and a boot loop can be seen. (P17)

## Build configuration

- IDF62. The ESP-IDF version is pinned identically in CI, local builds, and the release record; for
  a prebuilt runtime, the binary's version is recorded. Upgrades are re-measured, advisories are
  watched, and older-version apps are checked against the bootloader in the field. (P3)
- IDF63. Each non-default option in `sdkconfig.defaults` has a stated reason. Release builds come from
  a clean configuration, since an existing `sdkconfig` keeps old values. (P3)

## Frame budgets (AKOS synthesis)

Level 1 does not cover these: Espressif documents timers and tasks, not how a game spends a frame.

- IDF64. When presentation is locked to the panel, per-stage work counters report cost; a locked loop
  reports the panel's period. Tearing and deadline claims are measured on the panel. `[board]` (P2)
