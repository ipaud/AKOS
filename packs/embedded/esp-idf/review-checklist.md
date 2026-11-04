# Review Checklist — ESP-IDF Pack

Binary checks, each citing its rule, ordered by severity. Apply the group table in the
[decision framework](decision-framework.md) first: under MicroPython, groups marked C only are
skipped. `[board]` items need a recorded run on real hardware. From static reading alone they report
**not verified**, never pass (P2).

## Critical (blocks in every profile)

- [ ] Any eFuse procedure has written steps, a sacrificial-board dry run of the same model, per-step
      recovery, a verified key backup, and saved `espefuse.py summary` output. `[board]` (IDF51)
- [ ] The ROM download choice matches a written, proven recovery path. `[board]` (IDF56)
- [ ] Publishing to a device out of reach is treated as irreversible and was rehearsed on the same
      model from the version in the field. `[board]` (IDF46)
- [ ] Signing keys are absent from repositories, images, devices, CI, and logs, with a strong source,
      an offline backup, and written loss and compromise procedures; a CI key can never reach a
      device. (IDF52)
- [ ] Devices leaving the owner's hands use Flash Encryption Release mode where encryption is used,
      and the generated `sdkconfig` has no insecure options. (IDF53)
- [ ] A cut at any point leaves the last good persisted state readable. (IDF30)
- [ ] Data a new version rewrites is kept until confirmed, on every volume holding saves. (IDF39)
- [ ] Health confirmation, automatic rollback, and a diagnosis path exist before the device
      leaves. (IDF47)

## High

- [ ] Burn order is planned, power is guaranteed, and the first encryption pass is not on a
      battery. (IDF55)
- [ ] The bootloader is signed with all lifetime keys; aggressive revocation is off or recorded;
      revocation follows settled rollback. (IDF57)
- [ ] The generated `sdkconfig`, signature blocks, offsets, and flash command were checked before
      provisioning. (IDF58)
- [ ] The threat each property answers is recorded, including what stays readable and whether
      interpreted files are covered. (IDF54)
- [ ] A key held on a device cannot sign for other devices, unless a single-device case is
      recorded. (IDF44)
- [ ] A save that returns early bounds its window and flushes on every orderly exit. (IDF31)
- [ ] An update writes only the inactive slot and selects it only after validation. (IDF35)
- [ ] Rollback is enabled before first deployment. (IDF36)
- [ ] Options swapping flash-driver, heap, or ISR-path code ran erase, save, and update on the board
      with heap checks. `[board]` (IDF11)
- [ ] The design lists which ESP-IDF guarantees it does not inherit and rebuilds those it needs. (IDF42)
- [ ] The update layer cannot be changed by an update, enforced on the device, and its last path
      resets rather than reaching a prompt. (IDF43)
- [ ] Every file is checked against a signed manifest, the version is signed and only rises, and
      failed versions are not retried. (IDF44)
- [ ] Every install and rollback step repeats safely after a cut. `[board]` (IDF45)
- [ ] Health includes a successful update-channel check. (IDF48)
- [ ] Diagnosis works with no USB and no REPL, from the fixed layer. (IDF49)
- [ ] An unconfirmed version that hangs reaches a reset with no person involved. `[board]` (IDF38)

- [ ] Same hang check on a device its owner holds: IDF38 is High here rather than Critical. (IDF38)
- [ ] An image confirms only after a self-test of what the next update needs. (IDF37)
- [ ] OTA was tested on the board with the production bootloader, including corrupt images and a reset
      before confirming, and CI guards slot size. `[board]` (IDF40)
- [ ] The task watchdog outcome is a recorded decision per build. (IDF23)
- [ ] Tasks whose stall matters are subscribed to the watchdog. (IDF24)
- [ ] Long erases cannot trip a watchdog into resetting an update. (IDF25)
- [ ] IRAM-flagged ISRs keep their whole closure in IRAM or DRAM, and non-IRAM event loss is
      accepted in writing. (IDF15)
- [ ] XIP-dependent relaxations hold in every shipped configuration. (IDF17)
- [ ] DMA buffers are capable, aligned, not on a stack, and `max_transfer_sz` is explicit. (IDF12)
- [ ] DMA descriptors are not in PSRAM. (IDF13)
- [ ] Buffers in flight are untouched until collected. (IDF14)
- [ ] Cross-core exclusion uses mutexes or `portMUX`, with short critical sections. (IDF21)
- [ ] Split work shares no unsynchronised state and no single-threaded runtime. (IDF22)
- [ ] Every runtime allocation checks for failure and has a defined outcome. (IDF7)
- [ ] CI enforces an internal RAM floor. (IDF5)
- [ ] The brownout detector is on and a brownout counts as a power cut. (IDF59)
- [ ] The low-battery save completes above brownout under measured load. `[board]` (IDF60)
- [ ] Update-channel dependencies have stated lifetimes. (IDF50)

## Medium

- [ ] Findings on a named board cite a measurement or say there is none. (IDF1)
- [ ] Measurements record their board and build context. (IDF2)
- [ ] Board-versus-guidance disagreements record both sides. (IDF3)
- [ ] Runtime reports free, largest block, and low watermark per capability. (IDF6)
- [ ] Hot PSRAM paths beyond the cache have a measured cost. `[board]` (IDF8)
- [ ] Cross-core PSRAM sharing at frame rate has a measurement. `[board]` (IDF9)
- [ ] ISRs do not print, allocate, block, or use the FPU. (IDF16)
- [ ] Auto-suspend is off, or supported and clear of frequent interrupts. (IDF18)
- [ ] Long-lived tasks have explicit core and priority with a reason. (IDF19)
- [ ] Stack sizes come from high-water marks at peak load. `[board]` (IDF27)
- [ ] Overflow detection is on, and assertions are not disabled globally. (IDF28)
- [ ] A panic leaves evidence readable without a debugger. (IDF29)
- [ ] No atomicity is assumed of FAT, and survival claims rest on a cut test. `[board]` (IDF32)
- [ ] `nvs_commit()` is checked and erasing NVS is a deliberate decision. (IDF33)
- [ ] Anti-rollback is a recorded decision. (IDF41)
- [ ] Boot records the reset reason. (IDF61)
- [ ] The ESP-IDF or runtime version is pinned and recorded. (IDF62)

## Low

- [ ] IRAM, cache, and XIP changes record gain and cost. `[board]` (IDF10)
- [ ] Sharing the radio's core is measured. `[board]` (IDF20)
- [ ] The interrupt and bootloader watchdogs stay on. (IDF26)
- [ ] Flash write rate is bounded, with endurance from the part's datasheet. (IDF34)
- [ ] Non-default options have stated reasons, and release builds are clean. (IDF63)
- [ ] Frame cost comes from work counters when presentation is locked. `[board]` (IDF64)

## Reviewer discipline

1. **Apply the group table before anything else.** A C-only finding on a MicroPython project is not
   a finding from this pack.
2. **Name the board model.** Findings and figures for FNK0104N and FNK0104B do not cross (IDF2).
3. **Cite a measurement or say there is none** (IDF1). Do not invent a number, and never give a flash
   endurance figure from this pack.
4. **`[board]` without a run is "not verified".** List what run would settle it (IDF4).
5. **Say when you are citing synthesis.** Rules marked *(AKOS)* are not Level 1 and must not be
   presented as Espressif's position.
6. **Never run, suggest running casually, or paste a command that burns an eFuse in a review.** Point
   to the gate.

## Deferred, not checked here

- Heap, interrupts, filesystem, and runtime under MicroPython →
  [embedded/micropython](../micropython/README.md)
- Secure development process and provenance →
  [security/nist-ssdf](../../security/nist-ssdf/README.md)
- Release discipline around rollback → [devops/deployment](../../devops/deployment/README.md)
