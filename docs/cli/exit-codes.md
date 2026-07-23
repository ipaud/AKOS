# CLI exit codes

## Python 3.10+ precondition (applies to every command below except two)

`bin/akos`'s `main()` calls `require_python` before dispatching to any
subcommand, which exits `1` immediately (no mutation, no partial work) if a
valid Python 3.10+ interpreter can't be resolved. The two documented
exceptions are `help`/`-h`/`--help` (pure bash, no Python needed) and
`doctor` (the health check that must still run and *report* Python's
absence as a finding, not refuse to run because of it — see
`bin/akos-common.sh`). `install.sh` and `update.sh` apply the same
`require_python` gate before touching anything on disk.

## The 10 pre-existing commands — unchanged

`help, doctor, install-project, link-project, list-packs, list-agents, list-skills, show-profile, review, create-pack` keep their exact original behavior: `0` on success, `1` on the command's own validation failure (bad arguments, target already exists, unknown subdomain) or an unknown top-level command. No other exit code was ever used here, and this initiative doesn't change that — scripts already depending on this behavior keep working. `list-packs` gained `--all` and `--status stable|draft|deprecated` flags (default: stable-only); an unrecognized status value is a `1`, same "command's own validation failure" bucket as always.

## The new commands — a documented 0/1/2 scheme

`validate`, `rules`, `benchmark`, `freshness`, `check-config`, `routing-check`, `eval` (and `profile`, `history`, which don't have a meaningful "found a problem" state and just use 0/1 — `history record` returns `1` if it cannot publish atomically: a malformed `--scores-json`/`--packs-json`, a mid-write failure, or exhausting its id-collision retries; on any of these nothing is published and no partial review is left behind):

| Code | Meaning |
|---|---|
| `0` | Ran successfully, nothing to fail on (warnings are still allowed to print) |
| `1` | Usage/setup error — bad flag, target directory doesn't exist, manifest missing |
| `2` | Ran successfully, and found something the command considers a failure |

What "found something" means per command:

- `akos validate` — `2` if any schema **error** exists (or, with `--strict`, any **warning** too). Recommended-field warnings alone never trigger `2`.
- `akos rules run` — fail-closed, and it separates findings from operational errors. `0` = ran to completion with no blocking finding; `2` = ran to completion and a **blocking** finding exists (an open CRITICAL, or a finding a rule explicitly marked `blocking` — e.g. a live vendor credential that defaults to HIGH); `1` = the scan was **incomplete** (unparseable registry, unloadable detector, a detector with no `run()`, an internal exception) or a usage/setup error (bad directory, a `--rule` filter that matches nothing, an unknown rule id, or no stable rule discovered). If findings and operational errors coexist, `1` wins — an incomplete scan's "no CRITICAL" is not trustworthy. HIGH/MEDIUM/LOW findings that are not marked blocking print but don't gate. `--format json` returns an object `{status, summary, findings, errors}`, never a bare list, so a caller can tell an error from a finding.
- `akos benchmark run` — `2` if any case fails (a missed `must_detect` or an unexpected `must_not_detect` hit).
- `akos freshness --fail-on BAND` — `2` if any pack is at `BAND` or worse. Without `--fail-on`, always `0` (it's a report, not a gate, by default).
- `akos check-config [dir]` — `2` if the project's `.akos/config.md` has a disallowed value: a profile that is not one of the six, a `personal_profile` with path separators, a pack reference that escapes `packs/`, a `Deployed` value that is not exactly `yes`/`no` (or a duplicated `Deployed`), a non-empty repo-side `Profile overrides` section (the check both SKILL.md files gate on), or a `Packs to always load` entry that resolves to a `status: draft`/`deprecated` pack (advisory — draft content is readable, just not promised-stable; there is no config field that can override this); `1` on a setup error; `0` when the config is clean **or** absent (no config is not a failure). A `0` validates *form*, not trust — it does not make the repository config authoritative.
- `akos routing-check` — `2` if a `status: stable` pack is missing from (or a `status: draft` pack appears in) the Stable routing catalog in `skills/akos/SKILL.md`, a draft pack is missing from the Experimental section, or a `status: stable` agent/workflow depends on a draft pack; `1` if `skills/akos/SKILL.md` itself can't be found; `0` when routing is clean.
- `akos eval --report PATH` — `2` if the graded report fails an eval case; `1` on usage/setup error (missing `--report`/`--case`, unreadable file); `0` when it passes.

## Stable JSON contracts (v1.12)

JSON is a public per-command interface. These shapes are intentionally
different and are not normalized in v1.12:

| Command | Stable top-level JSON shape |
|---|---|
| `validate --format json` | array of `{file, errors, warnings}` |
| `rules run --format json` | object `{status, summary, findings, errors}` |
| `benchmark run --format json` | array of benchmark result objects |
| `freshness --format json` | array of pack freshness row objects |
| `check-config --format json` | array of config findings; exactly `[]` when config is absent |
| `routing-check --format json` | object `{errors}` |
| `eval --format json` | array containing the selected case result |
| `history show` | one merged metadata/report object |
| `history compare` | object `{a, b, decision_change, score_deltas}` |

Adding optional fields is compatible. Renaming/removing fields, changing a
top-level array into an object (or vice versa), or using a different shape for
the same command is a breaking change and requires a new documented contract
version. Human-readable output remains informational and is not parsed by CI.

## `update.sh`'s own contract (not a `bin/akos` subcommand, but load-bearing)

`0` only if: the concurrency lock was acquired, the personal-layer backup was created **and** immediately verified against the live source, the git pull either succeeded or failed for an already-warned reason (or the directory isn't a git repo — see below), the personal layer was verified unchanged or successfully restored, **and** the final `doctor.sh` run (which `update.sh` now actually invokes, not just suggests) exits `0`. `1` on: a lock already held, a failed or unverifiable backup, an unrecoverable restore failure, a failed `git pull`, a non-git checkout (nothing was updated automatically — this is not treated as a silent success), or a failing final `doctor.sh`. "Update complete and verified" and "personal layer preserved"/"restored" are only ever printed after the corresponding check has actually run — never assumed.

## Why not unify everything under one scheme

The 10 pre-existing commands' 0/1 behavior predates this initiative and nothing scripted against it should have to change. Extending that same binary scheme to the new commands would lose the "ran fine, but found a real problem" signal that makes these commands useful in CI (`ci.yml` gates on exactly this: `doctor.sh` at 0/1, everything else at 0/1/2).

## Bash tail-call discipline

Every new command's `cmd_<name>()` function in `bin/akos` is a literal tail-call to its Python script (e.g. `cmd_validate() { python3 "$AKOS_HOME/schemas/validate.py" "$@"; }`). Under `bin/akos`'s `set -euo pipefail`, this propagates the Python script's exit code for free — no special-casing needed. The one real gotcha: don't add post-processing after the Python call without `|| rc=$?; ...; exit "$rc"` guarding, or `set -e` silently discards the intended exit code the moment anything follows it.
