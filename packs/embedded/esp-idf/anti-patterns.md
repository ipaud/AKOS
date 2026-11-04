# Anti-Patterns — ESP-IDF Pack

Named failure modes, how to spot them, and what to do instead. The last three are failures of
*applying* this pack.

## The watchdog that was assumed to reset

**Detect:** a design or comment relying on the task watchdog to recover a hang, with
`CONFIG_ESP_TASK_WDT_PANIC` unset in the generated `sdkconfig`.
**Why it fails:** by default it prints and carries on, and it mainly watches idle tasks. The device
stays hung, with a tidy backtrace on a serial port nobody is reading.
**Fix:** decide per build, subscribe the tasks that matter, and handle long erases. (IDF23, IDF24,
IDF25)

## Rollback with nothing to trigger it

**Detect:** rollback enabled, or a trial counter in place, and no timer or armed watchdog while a
version is unconfirmed. A note saying a hang is caught "after three power cycles".
**Why it fails:** rollback fires on a reset. A version that hangs without crashing waits for someone
who does not know a reset is what it needs.
**Fix:** an automatic reset path while unconfirmed. (IDF38)

## Healthy because it did not crash

**Detect:** confirmation based only on uptime or play time, with no successful update check.
**Why it fails:** a version that plays well but has broken its own Wi-Fi or update path is confirmed,
and it is now the last version that device will ever run.
**Fix:** make the update channel part of health. (IDF37, IDF48)

## The fix that ships in the update that never arrives

**Detect:** a diagnostic screen in the backlog for after the device leaves; a doctor tool that runs
over `mpremote`; a production mode that blocks that tool.
**Why it fails:** when updates stop reaching a device, the update adding the diagnosis is exactly
what does not arrive. Nothing on the device can say why, and the cable is in another home.
**Fix:** diagnosis in the fixed layer before handover, readable with no cable. (IDF47, IDF49)

## Signed firmware running unsigned files

**Detect:** a plan that says Secure Boot protects the code, where the code is scripts or `.mpy` files
on a filesystem.
**Why it fails:** Secure Boot verifies the bootloader and the app image. Files that image later
interprets were never checked, so the lock is on the wrong door.
**Fix:** build the fixed layer into the signed image, and authenticate everything else separately.
(IDF42, IDF54)

## Borrowed guarantees

**Detect:** "OTA has rollback and validation" said of a design that renames files on a filesystem.
**Why it fails:** those guarantees belong to `esp_ota_*` and the bootloader. A file update inherits
none of them; it only shares the name.
**Fix:** list what it does not inherit, and rebuild what it needs. (IDF42, IDF45)

## One key to sign them all

**Detect:** a symmetric key on the device, the same across units; a key readable through ROM download
or a REPL.
**Why it fails:** the verifier can sign. Reading one device gives you every device with that key.
**Fix:** asymmetric signatures, or a recorded single-device exception. (IDF44)

## Testing the fuse on the only board

**Detect:** a provisioning plan with one board, or a "quick test" of Secure Boot on the final unit.
**Why it fails:** the first attempt at an irreversible procedure is the one most likely to be wrong,
and this one has no retry.
**Fix:** sacrificial board of the same model, deliberately broken, before the final one. (IDF51)

## The convenient recommended option

**Detect:** permanently disabling ROM download because the guide calls it the most secure, on a board
with no other way in and no proven OTA.
**Why it fails:** the recommendation assumes a recovery path you may not have.
**Fix:** match the choice to the recovery written down, and prove it. (IDF56)

## The RAM that cost the heap

**Detect:** an option that swaps flash-driver or ISR-path code taken on the strength of a `size`
report, with a note saying the board test is still to do.
**Why it fails:** the documented trade-off lists known costs. On one board the real cost was heap
corruption on every erase, and the affected builds could not update themselves.
**Fix:** erase, save, and update on the board first, with heap checks. (IDF11)

## The one good copy

**Detect:** `fopen(path, "wb")` over the only save; an OTA that erases the running slot; a rename
trusted on FAT with no test.
**Why it fails:** a cut during that write leaves nothing, and nothing warned anyone.
**Fix:** two generations with a checksum, and a cut test before claiming survival. (IDF30, IDF32)

## Rollback that forgets the data

**Detect:** a new version migrates the save, and the rollback path restores only code.
**Why it fails:** the old code meets a format it cannot read. The rollback worked and the save is gone.
**Fix:** keep prior data until confirmed, and restore it on rollback. (IDF39)

## The ISR that reads flash

**Detect:** `ESP_INTR_FLAG_IRAM` on a handler whose callee, constant, or format string lives in flash.
**Why it fails:** it works until a flash operation coincides, then crashes or reads garbage, rarely
and far from the cause.
**Fix:** keep the whole closure in IRAM or DRAM. (IDF15)

## Writing to the buffer on the wire

**Detect:** a buffer reused or refilled after `spi_device_queue_trans` and before the result returns.
**Why it fails:** the screen shows two frames at once, intermittently, in a way no log explains.
**Fix:** state who owns each buffer at each moment. (IDF14)

## Trusting the locked frame time

**Detect:** a "render" figure sitting at exactly the panel's period across wildly different scenes.
**Why it fails:** a loop locked to the panel measures the panel, so regressions stay invisible until
the frame misses.
**Fix:** per-stage work counters. (IDF64)

## Number laundering

**Detect:** a review quoting a figure from another project or board, or from the guide, as this
board's cost.
**Why it fails:** it looks like evidence and is not.
**Fix:** cite the board's own measurement or say there is none. (IDF1, IDF2)

## Passing a hardware rule from the code

**Detect:** a review marking power-cut survival, stack margin, or frame rate as passed with no run
recorded.
**Why it fails:** code can show what is intended, not what happened.
**Fix:** report "not verified" and say what run would settle it. (IDF4)

## Loading this pack for everything on the device

**Detect:** IRAM findings on a MicroPython game, or fuse findings on the WASM build.
**Why it fails:** it produces noise and buries the rules that do apply.
**Fix:** apply the group table first. ([decision-framework](decision-framework.md), "which rule
groups apply")
