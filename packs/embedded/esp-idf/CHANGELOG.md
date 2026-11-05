# Changelog — esp-idf

## [1.1.0] — 2026-11-05

### Calibrated against a third real audit

Third audit. Rubric rows for IDF37-IDF39 now apply to file-based updates, IDF39 has its row, and a hang out of reach is pointed at the out-of-reach row. IDF44 says a bench unit is not a second device. The prompt fragment no longer calls IDF11 and IDF42-IDF45 CRITICAL against the rubric.

## [1.0.0] — 2026-11-04

### Added

- First complete version, `status: draft`. Authority level 1 (Espressif, platform owner), review
  cadence 545 days (`review_after: 2028-05-02`). Baseline ESP-IDF v5.4.2, the version Pinyol builds.
  Cleared the source intake gate on a verified gap: outside `packs/embedded/`, `esp-idf`, `eFuse`,
  `PSRAM`, `task watchdog`, `secure boot`, `flash encryption`, and `brownout` returned zero files
  across the corpus, and `esp32` two: a personal project note and a project mapping in `games/qa`.
  The source is the platform owner's normative documentation and holds checkable positions, which
  is what separates this from reference.
- Principles P1–P17 and engineering rules IDF1–IDF64: evidence, memory, DMA, flash-cache safety,
  tasks, watchdogs, stacks, storage, OTA by partition, OTA by files, devices out of reach, Secure Boot
  and Flash Encryption, power, build, and frame budgets, plus one mapping onto three projects.

### The pack's organising decision: what it refuses to contain

**API reference, and any runtime number it did not get from a board.** The guide can be looked up, so
restating it fails the source intake gate. A number for someone else's board reads as a budget and
is not one. The line is enforced in the principles (P1, P2), by the `[board]` tag, by reviewer
discipline, by a scoring cap of 80 on static-only reviews, and by the *number laundering* anti-pattern.

Two further decisions organise the rest:

- **Measurement beats doctrine on the exact board,** and only there. Guidance is the prior.
- **Irreversibility is a floor.** eFuse procedures, signing keys, release-mode flags, and now updates
  to devices out of reach are CRITICAL when unrehearsed or without a way back.

### Other notable choices

- **The task watchdog default was verified:** warn and continue, confirmed in the page and in Kconfig.
  It became a rule, and with rollback's need for a reset it produced IDF38.
- **MicroPython split.** `embedded/micropython` owns heap, interrupts, filesystem, and runtime. This
  pack keeps chip and bootloader groups, which still bind under MicroPython, and C-only groups are
  `n/a` there.
- **File-based updates are a distinct mechanism.** Two MicroPython games were checked first: neither
  touches an app partition. The framework tables what `esp_ota_*` does and does not give them, and
  notes that Secure Boot never sees interpreted files.
- **Devices out of reach.** A device beyond a USB cable cannot be recovered by hand, so an update that
  stops the update channel is permanent unless the device can say why and undo it.
- **Calibrated against repeated audits.** IDF37 adds the data half of a self-test; IDF45 covers deletes
  and the order of an unfinished rollback.
- **Board models stay apart.** FNK0104N and FNK0104B figures are not interchangeable (IDF2).
- **No flash endurance figure.** The pages read state none, so the pack gives none.

### Known limits

- Two long pages were only partly read, and fetches were summaries; `references.md` lists both and
  which claims were re-checked against a local v5.4.2 tree.
- Stock MicroPython partition layouts were not verified.
- `engineering-rules.md` runs past the 200-line guidance because of its breadth and mapping table.
- Not yet linked from `graphs/knowledge-graph.md` or the routing table: out of scope for this change,
  and required before promotion.

### Scope boundary

Recorded against `packs/embedded/micropython` (heap, interrupts, filesystem, runtime),
`packs/security/nist-ssdf` (process and provenance), `packs/devops/deployment` (release discipline),
and `packs/performance/browser-rendering` (frame-budget arithmetic only).
`packs/architecture/philosophy-of-software-design` was considered and left out: nothing here turned on it.
