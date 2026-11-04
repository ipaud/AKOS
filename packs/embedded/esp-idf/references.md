# References — ESP-IDF Pack

Attribution only. Nothing here is copied from these sources; the pack is an original operational
distillation, organized by the AKOS file contract rather than by the guide's structure.

## Primary sources (Level 1 — platform owner)

- **ESP-IDF Programming Guide (ESP32-S3, v5.4.2)** — Espressif Systems.
  https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/
- **ESP-IDF source tree v5.4.2 (Kconfig defaults and component source)** — Espressif Systems.
  https://github.com/espressif/esp-idf/tree/v5.4.2

## Baseline

**ESP-IDF v5.4.2.** Pinyol's CI builds in `espressif/idf:v5.4.2`, and its `sdkconfig` records
`CONFIG_IDF_INIT_VERSION="5.4.2"`. The pages were read at that version, not at `latest`, so paths and
behaviour here may lag newer releases. A MicroPython build uses whatever version that
release requires, which this pack did not establish.

## What Level 1 covers here, and what it does not

**Covers:** documented behaviour of the chip, bootloader, and ESP-IDF: memory capabilities, DMA
constraints, cache behaviour during flash operations, FreeRTOS SMP rules, watchdogs, rollback states,
Secure Boot, Flash Encryption, and eFuse effects. Espressif is the platform owner, on the same basis
as Apple HIG on Apple platforms. Its authority holds on its own platform only.

**Does not cover:**

- **Any runtime figure for a particular board.** Those come from that board, and a measurement there
  overrides the guide's prior for that case (P1).
- **Frame-budget practice for games.** Espressif documents timers and tasks, not how a game spends a
  frame. IDF64 is synthesis.
- **What a given-away device needs.** Espressif documents rollback and health checks; IDF46–IDF50
  and the wider reading of P8 are synthesis, informed by the projects below. IDF38, IDF39, and IDF43
  are synthesis as well.
- **Application-file updates.** ESP-IDF's OTA guarantees do not reach them. Level 1 supports only
  the statement of what is not covered.
- **MicroPython.** Its behaviour belongs to [embedded/micropython](../micropython/README.md).
- **Flash endurance.** The FatFs, wear levelling, and NVS pages read state no erase-cycle figure, so
  this pack gives none. It comes from the flash part's datasheet.

## Pages read

All at v5.4.2 under `/esp32s3/`, fetched on 2026-11-04. Fetches returned machine summaries, not raw
text, so claims a rule depends on were re-checked against the `.rst` files and Kconfig of a local
v5.4.2 tree where marked †.

- `api-guides/`: `performance/speed.html`, `performance/ram-usage.html`, `external-ram.html` †,
  `memory-types.html`, `fatal-errors.html`, `bootloader.html`, `core_dump.html`,
  `usb-serial-jtag-console.html`.
- `api-reference/system/`: `wdts.html` †, `ota.html` †, `freertos.html`, `mem_alloc.html` †,
  `power_management.html`.
- `api-reference/system/freertos_idf.html`: **first 100,000 of 377,303 characters only**, which held
  the SMP sections used here.
- `api-reference/kconfig.html`: **first 100,000 of 563,055 characters only**. Other defaults were read
  from Kconfig files in the local tree †.
- `api-reference/storage/`: `fatfs.html`, `wear-levelling.html`, `nvs_flash.html`.
- `api-reference/peripherals/`: `spi_master.html`, `spi_flash/spi_flash_concurrency.html` †.
- `api-reference/network/esp_now.html`: read; no rule depends on it.
- `security/`: `security.html`, `secure-boot-v2.html`, `flash-encryption.html`,
  `security-features-enablement-workflows.html`.

Source read in the local tree: `components/esp_system/Kconfig`, the ESP32-S3 `Kconfig.system`,
`components/wear_levelling/Kconfig` and `WL_Flash.cpp`, `components/bootloader/Kconfig.projbuild`,
`components/bootloader_support/src/esp32s3/secure_boot_secure_features.c`,
`components/app_update/esp_ota_ops.c`, `components/fatfs/src/ff.c`, and
`components/soc/esp32s3/include/soc/soc_caps.h`.

## Pages not read, or not usable

- `api-guides/freertos-smp.html`: at v5.4.2 only a notice that the page moved; `freertos_idf.html`
  replaced it.
- The `latest` documentation tree: not read, because the baseline is v5.4.2.
- The remainder of `freertos_idf.html` and `kconfig.html`, beyond the limits above.
- `api-reference/peripherals/sdmmc_host.html`: not read. The source text has no DMA statement, so
  Pinyol's claim about SDMMC DMA and PSRAM stands as that project's measurement only.
- NVS Encryption, partition tables, the eFuse manager, and the ESP32-S3 Technical Reference Manual and
  datasheet: not read.
- Any stock MicroPython partition table or build configuration: not read.

## Where sources disagree

Recorded so nobody rediscovers these. Kconfig, being what builds, was preferred over prose.

- **Wear levelling.** The page gives 512-byte sectors in performance mode as the default. Kconfig at
  v5.4.2 defaults to 4096, and offers a mode only at 512, defaulting to safety.
- **Interrupt watchdog timeout.** The page says the default rises with PSRAM. Kconfig gives 300 ms here;
  the higher value applies only to the original ESP32.
- **Secure Boot and USB.** Page text covers USB-OTG in ROM and says nothing of USB-Serial-JTAG. On
  this chip's boards with no free UART that gap matters, so IDF56 sends it to the sacrificial board.

## Project evidence

Rules were checked against real ESP32-S3 firmware: Pinyol, which is public, and two private MicroPython
games by the same maintainer. That reading is not a source and carries no authority. Findings about
those projects stay in those projects: a pack states rules, never the state of a codebase.

## Related AKOS packs

[embedded/micropython](../micropython/README.md) ·
[security/nist-ssdf](../../security/nist-ssdf/README.md) ·
[devops/deployment](../../devops/deployment/README.md) ·
[performance/browser-rendering](../../performance/browser-rendering/README.md)
(frame-budget arithmetic only)
