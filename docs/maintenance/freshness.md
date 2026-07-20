# Pack freshness

A pack's `metadata.yaml` carries `last_reviewed` and `review_after` (added by the metadata migration — see `docs/contracts/knowledge-pack.md`). Freshness is the report over that field across every pack: is anything due for a re-read against its sources?

## Bands

| Band | Meaning |
|---|---|
| `fresh` | More than 90 days before `review_after` |
| `review-due-soon` | Within 90 days of `review_after` |
| `review-due` | Within 30 days of `review_after` |
| `expired` | Past `review_after` |
| `unknown` | No `review_after` set — not yet migrated, or hand-created without one |

## Core check is offline, by design

Nothing here does automated web verification of whether a source has actually changed. The check is purely a date comparison against `review_after`, which itself is either migration-computed (`last_reviewed` + an authority-level cadence: 18 months for L0–1 standards, 12 for L2, 9 for L3–4) or hand-set by a maintainer. A live "has this URL changed" checker is a plausible future extension, but it is not required for the core loop to work, and it would need to fail gracefully offline — freshness itself must never require network access.

## Commands

```bash
akos freshness                       # every pack, all bands
akos freshness --expired             # only expired
akos freshness --due-soon            # review-due-soon or worse
akos freshness --pack ux/wcag        # one pack
akos freshness --format json
akos freshness --fail-on expired     # exit 2 if anything is expired or worse — for CI
```

## Relationship to the PACK_EXPIRED rule

`rules/meta/pack-expired.py` is the same underlying date check, packaged as an executable rule (`akos rules run . --rule PACK_EXPIRED`) so it participates in `akos rules`' severity/exit-code machinery and is dual-wired directly into `doctor.sh`'s "Pack freshness" section. `akos freshness` is the richer report — full band spectrum, not just expired/not — for a maintainer actually working through what's due.

## What "due" means in practice

`review_after` passing doesn't mean the pack is wrong — it means nobody has confirmed it's still right in a while. The action is: re-read the pack's `principles.md` and `engineering-rules.md` against the sources in `references.md`, confirm nothing has materially changed, and bump `last_reviewed` (and recompute `review_after`) in `metadata.yaml`. If something *has* changed, update the pack content first, per `core/source-policy.md` — distill, don't copy.
