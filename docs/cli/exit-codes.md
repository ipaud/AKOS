# CLI exit codes

## The 10 pre-existing commands — unchanged

`help, doctor, install-project, link-project, list-packs, list-agents, list-skills, show-profile, review, create-pack` keep their exact original behavior: `0` on success, `1` on the command's own validation failure (bad arguments, target already exists, unknown subdomain) or an unknown top-level command. No other exit code was ever used here, and this initiative doesn't change that — scripts already depending on this behavior keep working.

## The new commands — a documented 0/1/2 scheme

`validate`, `rules`, `benchmark`, `freshness` (and `profile`, `history`, which don't have a meaningful "found a problem" state and just use 0/1):

| Code | Meaning |
|---|---|
| `0` | Ran successfully, nothing to fail on (warnings are still allowed to print) |
| `1` | Usage/setup error — bad flag, target directory doesn't exist, manifest missing |
| `2` | Ran successfully, and found something the command considers a failure |

What "found something" means per command:

- `akos validate` — `2` if any schema **error** exists (or, with `--strict`, any **warning** too). Recommended-field warnings alone never trigger `2`.
- `akos rules run` — `2` only if an open **CRITICAL** finding exists — the one severity `core/review-pipeline.md` itself says "always blocks, every profile." HIGH/MEDIUM/LOW findings print but don't gate, since the rules runner doesn't necessarily know the caller's full reasoning-profile weight table the way an LLM-driven review does.
- `akos benchmark run` — `2` if any case fails (a missed `must_detect` or an unexpected `must_not_detect` hit).
- `akos freshness --fail-on BAND` — `2` if any pack is at `BAND` or worse. Without `--fail-on`, always `0` (it's a report, not a gate, by default).

## Why not unify everything under one scheme

The 10 pre-existing commands' 0/1 behavior predates this initiative and nothing scripted against it should have to change. Extending that same binary scheme to the new commands would lose the "ran fine, but found a real problem" signal that makes these commands useful in CI (`ci.yml` gates on exactly this: `doctor.sh` at 0/1, everything else at 0/1/2).

## Bash tail-call discipline

Every new command's `cmd_<name>()` function in `bin/akos` is a literal tail-call to its Python script (e.g. `cmd_validate() { python3 "$AKOS_HOME/schemas/validate.py" "$@"; }`). Under `bin/akos`'s `set -euo pipefail`, this propagates the Python script's exit code for free — no special-casing needed. The one real gotcha: don't add post-processing after the Python call without `|| rc=$?; ...; exit "$rc"` guarding, or `set -e` silently discards the intended exit code the moment anything follows it.
