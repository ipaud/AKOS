# Review history

AKOS reviews are LLM-driven, not script-driven — a review is a Claude/Codex session reading packs and writing a Review Summary, not a program that runs deterministically. History capture has to bridge that: `akos history` is a thin, structured storage layer that the `akos-review` skill's own final step writes into, in the **consuming project's** `.akos/reviews/`, not in the AKOS repo.

## Why project-local, not AKOS-local

Same reasoning as `.akos/config.md`: review history is state about *a project*, not about AKOS itself. It travels with the project (or its `.gitignore`, per taste — see below), not with the knowledge system.

## Layout

```
.akos/reviews/<timestamp>-<type>/
  report.md       # the full Review Summary, verbatim
  report.json      # { decision, scores }
  metadata.json     # review_id, type, timestamp, profile, git commit/branch, packs_loaded
```

`<timestamp>` is UTC, `YYYYMMDDTHHMMSSZ` — computed by `bin/akos`'s bash wrapper at record time (`date -u +%Y%m%dT%H%M%SZ`), never by the Python module itself, so nothing in the history subsystem depends on wall-clock time except at the one point it's actually needed.

## Commands

```bash
akos history record --type <lens-or-full> --decision "<PASS|PASS WITH FIXES|BLOCKED>" \
  --profile <name> --report <path> [--scores-json '{"ux": 72, ...}'] [--packs-json '["ux/wcag", ...]']
akos history list
akos history show <review-id>
akos history latest
akos history compare <review-a> <review-b>
akos history clean [--keep N] --dry-run              # list what would go
akos history clean [--keep N] --confirm-delete N     # delete, asserting the count
```

All commands accept `--dir <project-path>` (default: current directory).

`clean` is the only destructive command here, so it does not act on a bare call. Its scope depends on how many reviews happen to exist past `--keep` — a number the caller has not seen — so it names every review it would remove and requires `--confirm-delete N` matching that count. If the count has changed since you previewed it, the call fails rather than deleting a different set. `.akos/reviews/` is usually untracked in a consuming project, which makes a wrong delete here unrecoverable.

## What `compare` actually diffs

`report.json` today holds `decision` and per-dimension `scores` — that's what `compare` diffs: the decision transition (`BLOCKED -> PASS WITH FIXES`) and a per-dimension score delta. It does **not** diff individual findings (resolved/new/persistent) — `report.json` doesn't structure findings separately from the Markdown prose in `report.md` today. That's a real, stated gap, not a silent one: a richer per-finding diff would need the Review Summary's Critical/High/Medium/Low sections to be machine-parseable, which they deliberately aren't (they're prose an LLM writes and reads, per the same reasoning that keeps agent bodies out of JSON Schema in `docs/contracts/agent.md`). Revisit if finding-level diffing becomes a real need.

## Local, not committed by default

`.akos/` is already gitignored defensively at the AKOS repo's own root (irrelevant there) — for a **consuming** project, whether to commit `.akos/reviews/` is that project's call. It's genuinely useful project history (a record of what got reviewed and when), so there's no AKOS-side opinion forcing it into or out of version control.
