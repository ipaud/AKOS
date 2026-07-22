# CLI exit codes

## The 10 pre-existing commands — unchanged

`help, doctor, install-project, link-project, list-packs, list-agents, list-skills, show-profile, review, create-pack` keep their exact original behavior: `0` on success, `1` on the command's own validation failure (bad arguments, target already exists, unknown subdomain) or an unknown top-level command. No other exit code was ever used here, and this initiative doesn't change that — scripts already depending on this behavior keep working.

## The new commands — a documented 0/1/2 scheme

`validate`, `rules`, `benchmark`, `freshness`, `check-config`, `eval` (and `profile`, `history`, which don't have a meaningful "found a problem" state and just use 0/1 — `history record` returns `1` if it cannot publish atomically: a malformed `--scores-json`/`--packs-json`, a mid-write failure, or exhausting its id-collision retries; on any of these nothing is published and no partial review is left behind):

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
- `akos check-config [dir]` — `2` if the project's `.akos/config.md` has a disallowed value: a profile that is not one of the six, a `personal_profile` with path separators, a pack reference that escapes `packs/`, a `Deployed` value that is not exactly `yes`/`no` (or a duplicated `Deployed`), or a non-empty repo-side `Profile overrides` section (the check both SKILL.md files gate on); `1` on a setup error; `0` when the config is clean **or** absent (no config is not a failure). A `0` validates *form*, not trust — it does not make the repository config authoritative.
- `akos eval --report PATH` — `2` if the graded report fails an eval case; `1` on usage/setup error (missing `--report`/`--case`, unreadable file); `0` when it passes.

## Why not unify everything under one scheme

The 10 pre-existing commands' 0/1 behavior predates this initiative and nothing scripted against it should have to change. Extending that same binary scheme to the new commands would lose the "ran fine, but found a real problem" signal that makes these commands useful in CI (`ci.yml` gates on exactly this: `doctor.sh` at 0/1, everything else at 0/1/2).

## Bash tail-call discipline

Every new command's `cmd_<name>()` function in `bin/akos` is a literal tail-call to its Python script (e.g. `cmd_validate() { python3 "$AKOS_HOME/schemas/validate.py" "$@"; }`). Under `bin/akos`'s `set -euo pipefail`, this propagates the Python script's exit code for free — no special-casing needed. The one real gotcha: don't add post-processing after the Python call without `|| rc=$?; ...; exit "$rc"` guarding, or `set -e` silently discards the intended exit code the moment anything follows it.
