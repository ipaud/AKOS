# Glossary — ESP-IDF Pack

Terms this pack uses precisely.

- **Internal RAM** — on-chip SRAM, split into DRAM and IRAM uses. Fast, scarce, and available during
  flash operations.
- **PSRAM** — external RAM reached through a cache shared with flash. Inaccessible while that cache is
  off.
- **DRAM / IRAM** — internal memory for data and for instructions. IRAM growth shrinks the heap.
- **IROM / DROM** — code and constants mapped from flash through the cache.
- **DMA-capable** — memory a peripheral's DMA can reach directly: `MALLOC_CAP_DMA`, which excludes PSRAM
  unless combined with `MALLOC_CAP_SPIRAM`.
- **IRAM-safe ISR** — a handler flagged `ESP_INTR_FLAG_IRAM` whose whole closure is in internal memory,
  so it can run during flash operations.
- **XIP from PSRAM** — code and constants copied to PSRAM at startup and run from there, so flash
  operations no longer turn the cache off.
- **Largest free block** — the biggest single allocation that can succeed now. Distinct from total free.
- **Low watermark** — the least free memory ever, or the least stack ever unused.
- **Task watchdog (TWDT)** — checks that watched tasks run. Warns by default.
- **Interrupt watchdog (IWDT)** — checks that interrupts are serviced. Panics.
- **Brownout** — supply voltage below the detector's level. The chip resets, and storage sees a power cut.
- **Slot** — an app partition (`ota_0`, `ota_1`). Distinct from a *save slot* in game code.
- **`otadata`** — the two-sector partition recording which slot boots.
- **Rollback** — the bootloader returning to the previous slot after an unconfirmed image resets. In
  this pack also, explicitly labelled, the equivalent in a fixed layer.
- **Anti-rollback** — an eFuse-backed minimum version that stops older apps booting. Different from
  rollback, and nearly opposite in intent.
- **Pending verify** — the state of a new image on first boot, before it confirms itself.
- **Confirmation / health** — a version declaring itself good. In this pack, health includes the
  ability to fetch the next update.
- **App-partition OTA** — update through `esp_ota_*` into a slot, with the bootloader's guarantees.
- **File-based update** — replacing application files on a filesystem. Inherits none of those guarantees.
- **Fixed layer** — the code an update cannot change, which installs, undoes, and reports updates.
- **Manifest** — a signed list of a version's files and hashes.
- **eFuse** — a one-time programmable bit in the chip. No retry.
- **Secure Boot v2** — ROM and bootloader verification of RSA-PSS signatures on bootloader and app.
- **Flash Encryption** — transparent XTS-AES encryption of flash contents. Development mode allows
  reflashing and is labelled not secure; Release mode does not.
- **Secure Download Mode** — a restricted ROM download mode; distinct from permanently disabled.
- **Sacrificial board** — a board of the same model you are willing to lock or destroy.
- **Out of reach** — a device nobody can connect a cable to, typically given away. An irreversible
  context in this pack, not a location.
- **Prior** — platform guidance before a measurement exists.
- **`[board]`** — a rule needing a recorded run on real hardware.
- **TE** — the panel's tearing-effect signal, one pulse per scan on the boards measured.
