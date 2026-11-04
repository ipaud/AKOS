# Prompt Fragments — ESP-IDF Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first: in most tasks
one block is all that needs loading.

## Fragment: build-mode constraint block

```text
ESP-IDF CONSTRAINTS (Level 1 on documented chip and bootloader behaviour; board measurements
override it for that board; marked items are AKOS synthesis):

Scope first
- Not this chip family: stop, this pack does not apply.
- MicroPython on top: use the evidence, watchdog, OTA, secure boot, flash encryption, eFuse,
  and power groups. IRAM, DMA, tasks, stacks, and storage code are C-only.

Evidence
- Cite a measurement on this exact board model, or say "no measurement".
- Never state a runtime number from reading code. Never invent a flash endurance figure.

Memory (C)
- DMA and IRAM-safe ISR data live in internal RAM. DMA descriptors never in PSRAM.
- Budget on the largest free block, not total free. CI guards an internal RAM floor.
- Hot PSRAM paths and cross-core PSRAM sharing need a board measurement.
- Options swapping flash-driver or ISR code need erase, save, and update run on the board.

Concurrency (C)
- Explicit core and priority on every long-lived task. portMUX or mutexes across cores.
- Buffers in flight stay untouched until collected. ISRs hand off; no printf, malloc, or float.

Watchdogs
- The task watchdog WARNS by default. It does not reset. Decide per build.

Integrity (floor)
- A power cut at any point leaves the last good state readable.
- Updates go to the inactive slot, selected only after validation; rollback on before deployment.
- Rollback restores code, not data. An unconfirmed version needs an automatic reset path.

Irreversible (floor)
- No eFuse step without written steps, a sacrificial board, per-step recovery, a key backup.
- Keys never in repo, image, device, CI, or logs. Release mode for anything leaving your hands.
```

## Fragment: review lens

```text
Review this firmware against the AKOS ESP-IDF pack (embedded/esp-idf).

Rules binding the review:

1. Apply the group table first. Under MicroPython, C-only groups are not findings here.
2. Name the board model. Figures from another model do not apply.
3. Every placement or timing finding cites a measurement or says "no measurement".
4. [board] rules with no recorded run report NOT VERIFIED, never pass. A static review is capped
   at 80 and must list them, with the run that would settle each.
5. Say when a rule is AKOS synthesis rather than Espressif's position.
6. Never run or casually suggest a command that burns an eFuse.

CRITICAL: an eFuse procedure lacking dry run or written recovery (IDF51); ROM download not matched
to recovery (IDF56); key exposure (IDF52); development mode or insecure options leaving the owner's
hands (IDF53); possible loss of the last good state (IDF30, IDF35, IDF39); an unproven RAM-saving
swap (IDF11); unprotected file-based updates (IDF42-IDF45); an out-of-reach device without health,
rollback, and diagnosis (IDF46-IDF49).

Then: watchdog assumptions, confirmation timing, ISR closures, DMA ownership, cross-core state.

For each finding: rule code, file and line, board model, measurement or "none", smallest fix.
```

## Fragment: eFuse gate

```text
This step burns eFuses or enables an option that burns them on first boot. It cannot be undone.
Stop unless every answer is yes:

1. Is every step written, in order, with exact commands?
2. Has it run on a sacrificial board of the SAME MODEL, then been deliberately broken?
3. Does each step name the recovery that remains after it?
4. Is the signing key backed up, and has the backup been restored once?
5. Is state saved first: espefuse summary, flash image, partition table?
6. Is the generated sdkconfig checked, and both signature blocks, and the flash command?
7. Is power guaranteed, not a battery?
8. Does the ROM download choice leave the recovery in point 3 possible?

Any "no": do not proceed. Report which, and what would make it yes. Do not run the step yourself.
```

## Fragment: handover gate

```text
This device is leaving, and will take updates where no cable can reach it. An update it cannot
recover from is permanent. Before it goes:

1. Which update mechanism does the code really use: app partitions or files? If files, which
   ESP-IDF guarantees does it not inherit, and what replaces each?
2. Is the update layer unchangeable by an update, enforced on the device?
3. Does health confirmation include fetching the next update?
4. Does a version that HANGS roll back with no person doing anything?
5. Can the recipient see version, last check, and last errors with no cable?
6. Does the key on the device fail to sign for any other device?
7. What in the update channel expires, and when?
8. Was the update path rehearsed on the same model, from the version going out?

Then, for every update published afterwards: rehearse from the version in the field first.
```

## One-liner (for tight token budgets)

```text
ESP-IDF floor: on this chip family only (MicroPython: chip, OTA, security, watchdog, and power groups
still bind). A measurement on this exact board beats guidance; cite one or say none; hardware claims
without a run are NOT VERIFIED. Task watchdog warns, it does not reset. A power cut must leave the last
good state. Rollback needs a reset and restores code only. Nothing burns an eFuse without a sacrificial
board and written recovery. Keys never in repo, image, device, or CI. A device out of reach needs
health (including the update channel), automatic rollback, and cable-free diagnosis before it leaves.
```
