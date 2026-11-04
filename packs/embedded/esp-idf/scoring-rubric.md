# Scoring Rubric — ESP-IDF Pack

Feeds the security, performance, and maintainability dimensions
([core/scoring-model.md](../../../core/scoring-model.md)). This rubric refuses to do one thing: let a
review reach a high score by reading code about behaviour only hardware can show.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| eFuse procedure with no dry run, or no written recovery path | −40 (CRITICAL) |
| Update to a device out of reach without rehearsal, health check, rollback, or diagnosis | −40 (CRITICAL) |
| Signing key in a repository, image, device, CI, or log, or with no backup | −40 (CRITICAL) |
| Development-mode encryption or insecure options on a device leaving the owner's hands | −40 (CRITICAL) |
| A power cut during save, update, or rollback can lose the last good state | −40 (CRITICAL) |
| RAM-saving swap of flash-driver or ISR-path code with no board run | −15 (HIGH) |
| File-based update without signed manifest, repeatable steps, or a protected update layer | −15 (HIGH) |
| ROM download choice not matched to a recovery path | −40 (CRITICAL) |
| A hang needs a person to recover, on a device its owner holds | −15 (HIGH) |
| No OTA test with the production bootloader, or no slot guard | −15 (HIGH) |
| Confirmation before a meaningful self-test | −15 (HIGH) |
| Watchdog behaviour undecided, or assumed to reset | −15 (HIGH) |
| IRAM-flagged ISR with flash-resident code or data | −15 (HIGH) |
| DMA buffer misuse, or a buffer touched while in flight | −15 (HIGH) |
| Unsynchronised state across cores | −15 (HIGH) |
| Allocation failure unhandled on a runtime path | −10 (HIGH) |
| No internal RAM floor in CI | −10 (HIGH) |
| Brownout detector off, or low-battery save not above it | −10 (HIGH) |
| Update-channel dependency with no stated lifetime | −10 (HIGH) |
| Placement or timing claim with no measurement and not labelled as such | −6 (MEDIUM) |
| Measurement with no board or build context | −6 (MEDIUM) |
| No largest-block or low-watermark reporting | −6 (MEDIUM) |
| Stack sizes not from high-water marks; no overflow detection | −6 (MEDIUM) |
| A panic leaves no readable evidence; reset reason not recorded | −6 (MEDIUM) |
| Atomicity assumed on FAT | −6 (MEDIUM) |
| ESP-IDF or runtime version unpinned | −6 (MEDIUM) |
| Anti-rollback undecided | −4 (MEDIUM) |
| Tasks with no explicit core, priority, or reason | −4 (MEDIUM) |
| Non-default options with no stated reason | −2 (LOW) |
| Flash write rate unbounded | −2 (LOW) |
| Frame cost read from a locked frame time | −2 (LOW) |

## Caps and floors

- **Any CRITICAL: score ≤ 59 (Blocked band)**, per
  [core/scoring-model.md](../../../core/scoring-model.md). An irreversible mistake does not average
  out against good code elsewhere.
- **Static-only cap: 80.** A review with no recorded board runs reports `score (static)`, capped at
  80, and lists every `[board]` rule as **not verified**. It may not claim pass on any of them.
  An unverified `[board]` rule is not itself a deduction; the cap accounts for it.
- **A board result from another model does not lift the cap** (IDF2).
- **No deduction may rest on an invented number**, and none on a figure from another board.
- A CRITICAL that is recorded as a known gap and blocks release in the project's own report still
  counts. Honest paperwork helps the owner; it does not make the device safe.

## `n/a` conditions

- **The whole rubric is `n/a`** for anything not on this chip family, including desktop and WASM
  builds of the same project.
- **Groups marked C only are `n/a` under MicroPython** (decision framework); score those under
  [embedded/micropython](../micropython/README.md) and never twice.
- **eFuse rows are `n/a`** where no burn is planned and the unit stays a development board. Say so,
  and do not score that as secured.
- **OTA rows are `n/a`** where a device has no over-the-air path, and the file-based rows are `n/a`
  where it uses only partitions, and the reverse.
- **Out-of-reach rows are `n/a`** only while the device stays with its owner and no handover is planned.
- **`n/a` under Prototype** for everything except floor rows on a board you would mind losing.

## Reading the score

| Score | Meaning |
|---|---|
| 90–100 | Board runs recorded, floor clean, decisions written down. |
| 80–89 | Sound; some `[board]` work outstanding or medium gaps. A static review tops out here. |
| 60–79 | Works, but relies on defaults nobody chose. |
| ≤ 59 | Blocked: something irreversible or unrecoverable is exposed. |
