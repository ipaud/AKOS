# Examples — Coding Agents Pack

Bad → good, with the rule applied. The invented cases are fabricated for calibration. The final section is a **real, in-repo case study**: AKOS's own v1.4.0 quality-infrastructure work, inspectable with `git log` and in [CHANGELOG.md](../../../CHANGELOG.md)'s `[1.4.0]` entry.

## The plausible completion (CA1, CA2, CAE52)

An agent is asked to fix a failing date-parsing function. It reads the code, spots that the format string uses `DD` where the library expects `dd`, changes it, and reports:

> Fixed the format string. All tests now pass and the build is clean.

No test command appears anywhere in the session. The diagnosis was correct and the fix was correct — and the report is still a defect, because the same sentence would have been produced had the fix been wrong. It also happens to be false in a way nobody checks for a week: the same file had a second `DD` on line 84, in the export path, which the agent never searched for.

After: the agent runs the project's suite, reads the failure, and reports what actually happened.

```
$ npm test -- date-utils
  ✗ formats export filenames  (expected 2026-07-20, got 2026-DD-20)
  ✓ formats display dates
exit 1
```

Two occurrences, one fixed. The correction to the process is not "be more careful" — it is that the claim now cannot be written before the command that produces it.

## The pipe that swallowed the exit code (CA12, CAE54)

A CI wrapper script runs a validator over a large corpus and prints a summary:

```bash
run_validation() {
  python3 schemas/validate.py "$@" | tail -5
}
```

The output is right there on screen — errors and all — and the function returns `0` every time, because a pipeline's exit code is its last stage's, and `tail` succeeds essentially always. The wrapper reports success while displaying failures. Nothing about the terminal output looks wrong; the only thing that is wrong is the number nobody printed.

After, three options, any of which closes the chain:

```bash
# 1. Don't put anything between the check and its status.
run_validation() { python3 schemas/validate.py "$@"; }

# 2. Propagate the pipeline's real failure.
set -o pipefail

# 3. Capture the status before the pipe consumes it.
python3 schemas/validate.py "$@" > /tmp/out; status=$?
tail -5 /tmp/out; exit $status
```

The generalizable rule: **trace the path from the command that knows the answer to the place the answer is read, and count what sits in between.** Every command in that path that can succeed on its own has severed the chain.

## The first-match fix (CA5, CAE8–CAE12)

A `timeout_ms` option is renamed to `timeoutMs` for consistency with the rest of a config object. The agent greps, sees the definition and one call site, changes both, runs the unit tests, and gets green.

Three references were never found: a YAML deployment config that sets `timeout_ms` as a string key, a re-export in `index.ts` that aliases the option under an older name, and a snapshot fixture. The unit tests pass because none of them exercise config loading. The failure appears in staging, as a silent fallback to the default timeout — which is longer, so nothing errors, and the regression is measured in latency two weeks later.

After: the search runs before the first edit and is deliberately widened past code.

```
$ grep -rn "timeout_ms" --include='*' . | wc -l
7
```

Seven references, enumerated: definition, two call sites, one re-export alias, one YAML config, one fixture, one docs page. The change is finished when the list is exhausted, not when the first site compiles. A search returning one hit on an option expected to be widely used is treated as a *suspect pattern*, not as good news.

## The bundled refactor (CA9, CAE26–CAE29)

A one-line null-check fix arrives as a 340-line diff: the fix, a rename of `usr` to `user` throughout the module, extraction of two helpers, a formatting pass, and removal of a dead branch. Each change is individually defensible. The reviewer approves it in four minutes, because reviewing it properly would take an hour and the fix at the center is obviously right.

Three days later the fix needs reverting — the null case turns out to be a symptom of an upstream bug, and reverting is the fastest mitigation. Reverting takes the extracted helpers and the rename with it, breaking two files that were updated to use them in the interim.

After: four changes, landed in order. The behavior-preserving rename first. The helper extraction second. The null-check fix third — nine lines, reviewed in thirty seconds, revertable alone. The dead-branch removal and formatting fourth. Same total work, and the one piece that needed undoing could be undone.

## The suppressed check (CA14, CAE77, CAE78)

A type checker reports `Object is possibly 'undefined'` on a lookup result. The agent widens the type and moves on:

```ts
const config = registry.get(name) as Config;  // was: Config | undefined
```

Green. The condition the checker named — this lookup can return nothing — is untouched, and the mechanism that would have caught the next one is now gone for this call site. The undefined case fires in production on a name that was removed from the registry in an unrelated change.

After: the cause is fixed, and the check keeps working.

```ts
const config = registry.get(name);
if (!config) throw new UnknownConfigError(name);
```

The legitimate use of suppression is narrow and rare, and it looks like this — one line, in place, with the reason the check is wrong *here*:

```ts
// akos:allow SECRET_IN_SOURCE — anon key, public by design; RLS constrains it
const SUPABASE_ANON_KEY = "eyJhbGciOi...";
```

## The silent interface break (CA10, CAE60–CAE66)

A shared `formatCurrency(amount, currency)` gains a third parameter and the argument order changes to `formatCurrency(currency, amount, locale)`. All eleven in-repo callers are updated in the same commit, tests pass, and the change lands.

The package is published. Two other services import it. Both compile — the parameters are all strings — and both begin rendering `"USD 1.00"` where the amount used to be, with no error anywhere.

After: consumers are enumerated *first*, and the count outside the repository decides the shape of the work. Since external consumers cannot be updated in the same commit, there is no atomic version of this change:

1. Add `formatCurrencyWithLocale(currency, amount, locale)` alongside the existing function. Ship it. Nothing breaks.
2. Migrate the eleven in-repo callers. Mark the old function deprecated with a stated removal version.
3. After external consumers have migrated, remove the old function — a separate change, in a later release.

The rule that decides this is not diff size. A one-character change to an exported signature is a migration; a two-hundred-line rewrite of a private helper is an edit.

---

# In-repo case study: AKOS v1.4.0

The rest of this file is not invented. AKOS's v1.4.0 initiative shipped JSON schemas, a validation CLI, an executable rules engine with eight detectors, a 21-case benchmark harness, freshness reporting, review history, CI workflows, and 79 unit tests plus 4 integration scripts, across thirteen commits. It found and fixed a series of real bugs, and the reason it found them is the entire subject of this pack: **each component was executed against a real or constructed case before the next one was built on top of it.** Every one of these would have shipped broken had the work stopped at "the code looks right."

Inspect it with `git log --oneline`, `git show 32905fa`, `git show b9e0b93`, and [CHANGELOG.md](../../../CHANGELOG.md)'s `[1.4.0]` entry.

## The vacuous pass, in production (CA3, CAE41, CAE58)

`write_marked_section` is the helper `akos install-project` depends on for every rerun — it splices a managed block into a project's `CLAUDE.md`. On this machine's BSD `awk`, it **silently failed whenever it needed to replace an already-marked section**: `awk -v` cannot accept a multi-line value, so it exited nonzero with no output, and `set -e` aborted before the file was ever rewritten.

The detail that matters is how long it hid. A prior "rerun idempotency" check **had passed** — by coincidence. The target content hadn't changed between the two runs, so a silently-failed no-op was byte-for-byte indistinguishable from a successful rewrite. The check was structurally incapable of failing for the case it existed to cover, and it reported green with exactly the same appearance as a real pass.

Had the agent claimed success on the strength of that green: every user rerunning `install-project` after editing their config would have silently kept the old block, with the command reporting success. The fix was a portable `sed` line-range splice; the durable fix was `tests/integration/test_marker_replace.sh`, which runs `install-project` twice **with a real content change in between** — the one condition under which the original check could have failed.

## Five detector bugs, each caught by running it (CA1, CA11, CAE38, CAE42)

Commit `32905fa` added eight executable rule detectors. Five real bugs were found by testing each detector against a constructed fixture — a true positive *and* the realistic near-miss that should not fire — before moving to the next one:

| Bug | What would have shipped |
|---|---|
| Suppression only checked the **exact evidence line** | A guard comment on a `CREATE POLICY`'s own line failed to suppress a violation reported a few lines later in the same statement — so every correctly-suppressed policy still fired. Fixed with a backward window. |
| `A11Y_INPUT_NO_LABEL` matched only HTML's `for`, never JSX's `htmlFor` | **Every correctly-labeled React input** in every scanned project would have been a false positive. The detector would have looked like it was working — it produces findings — while being wrong on essentially all real input. |
| Fixture-path exclusion matched `"test"` as a **substring** rather than a path segment | Any file under a directory merely *containing* the letters "test" was silently skipped — including, during that very session, the scratch directory `/tmp/secret-test/`. A secrets detector that silently skips files is worse than no detector: it reports clean. |
| Anon-role Supabase JWTs flagged as secrets | Anon keys are designed to be public and constrained by RLS. Flagging them trains users to ignore the rule, which disables it for the `service_role` case that actually matters. Only a decodable `service_role` claim should fire. |
| `DESTRUCTIVE_MIGRATION_NO_GUARD`'s fixed 3-line guard window | A guard comment meant for one statement suppressed an **unrelated** destructive statement a few lines later — a `DROP` silently exempted by a comment that was never about it. |

Three of these five produce *green*, not red: the substring exclusion, the guard bleed, and the anon-key noise all end with a check reporting nothing wrong. None would have been caught by reading the regex. All were caught by running the detector against a case whose answer was known in advance.

## The inverted comparison, caught by an exit code (CA12, CAE53)

`akos freshness --fail-on` mapped band severities through a `reversed()` that read backwards from how the `>=` comparison consumed it — `unknown=0`, `fresh=4`. The effect: `--fail-on expired` matched **everything except `unknown`**, instead of only expired-or-worse.

It was caught by exactly one observation, recorded in `git show b765cd7`: the first real run against an all-fresh repository **exited 2 when it should have exited 0**. Nothing in the output text was wrong — the band report was correct and readable. The only wrong thing was the number, and reading the number is what found it. Had the run been evaluated by reading its output, the bug ships, and the weekly CI freshness workflow fails permanently on a healthy corpus until someone disables it.

## The benchmark harness whose failure pattern was the diagnosis (CA3, CAE42)

The 21-case benchmark harness (`b9e0b93`) resolved `expected.yaml`'s fixture paths relative to `benchmarks/` instead of the case's own directory. Every `must_detect` spec therefore pointed at a nonexistent path and could never match a real finding.

The failure pattern was itself diagnostic, and it is the clearest instance of the vacuous pass this repo produced: **every true-positive case failed while every true-negative case passed** — because a broken `match()` *vacuously satisfies* a `must_not_detect` assertion regardless of whether the underlying detector is even correct. Half the suite was green for the worst possible reason. This is why CAE42 requires every absence assertion to be paired with a positive case proving the mechanism can fire at all.

The same commit records the corresponding discipline, applied deliberately rather than discovered: the `SUPABASE_RLS_DISABLED` detector was **disabled on purpose**, the case re-run, the expected `FAIL` and exit 2 confirmed, the detector restored, and the suite re-run clean. That is CAE41 — proving the check can fail before trusting that it passed.

## The piped `tail` that masked the real exit code (CA12, CAE54)

Commit `748db87` introduced `akos validate` with a three-value exit convention (`0` clean / `1` usage error / `2` errors found), while the ten pre-existing commands kept their unchanged `0`/`1` behavior — backward compatibility held deliberately at the CLI boundary (CAE66's spirit, applied to a command-line interface).

Verifying that convention end-to-end through the `bin/akos` wrapper turned up the trap this pack names explicitly. The commit message records it plainly: the first test of the new exit codes was run through a piped `tail`, **which reported its own status rather than the validator's**. The check appeared to pass at every one of `0`, `1`, and `2`, because `tail` succeeds regardless. The real verification required making `cmd_validate` a tail call — the literal last statement in its function — so `set -e` propagates `validate.py`'s exit code untouched, and then re-running all three cases with nothing between the command and its status.

Had that first result been trusted: a validation CLI shipping with an exit convention that was never actually verified, wired into `doctor.sh` and into CI, where it would have reported clean forever.

## The test that was wrong, not the code (CAE44)

While writing the unit suite (`4925d34`), the `MIGRATION_NO_DOWN_FILE` test asserted 0 findings where 1 was expected. The tempting move — the one CAE44 exists to prevent — is to amend the assertion to 0 and take the green.

It was traced instead: **the test itself** omitted the down file from the list passed to `run()`, since `down_files` is computed from the `files` argument rather than from a directory scan. The test was fixed; the detector was confirmed correct all along. The decision rule from [decision-framework.md](decision-framework.md) applies directly — when a test fails after a change, exactly one of them is wrong, and deciding which requires reading the test's intent rather than reaching for whichever edit produces green fastest.

## Conventions matched rather than improved (CA8, CAE19, CAE24)

While testing the new YAML parser against the real corpus (`09f9c6b`), four packs were found using a multi-line `tags:` flow-list format that the other forty-four did not. Two responses were available: grow the parser to support a second flow-list syntax, or reformat the four outliers to the established convention.

The four files were reformatted. The parser stayed simple, and the corpus stayed uniform. This is CA8 running in the direction people forget — the majority convention won not because it was better in the abstract, but because forty-four files already spoke it and consistency is the property that was worth preserving.

The same commit records the orientation discipline that made the whole schema non-breaking by construction: the required-field set was chosen as "exactly the 7 already universal across all 48 pre-existing packs," and the CHANGELOG says how that was established — *confirmed by direct inspection, not assumed* (CA4, CAE1).

## What the honest description looked like (CA18, CAE75)

Commit `4c3e854` added the CI workflows. Its final two steps reference `tests/unit` and `tests/integration`, which did not exist until the *next* commit. The commit message says so:

> ...by the end of this session the workflow is fully coherent, but noting the ordering honestly here rather than pretending it's already runnable standalone.

That sentence weakens the commit. It is also the most useful sentence in it, because it is the one thing a reader could not have recovered from the diff, and it tells the next person exactly which claim not to rely on. CAE75 exists for this: a known gap stated is worth more than a description that reads cleanly.

> **The same commit also violates CAE52, four lines earlier.** It asserts that *"every individual command referenced (doctor.sh, validate.py, freshness.py, the rules sanity snippet, benchmark run.py) was already exercised directly and separately."* The rules sanity snippet was `python3 rules/runner.py list` — and `runner.py` has no `list` subcommand; it reads `list` as a directory to scan. That command **cannot ever have been exercised successfully.** What was actually verified was that the YAML parsed. The workflow then failed on its first three real runs on GitHub, and v1.4.0 shipped and stayed red for 2h15m.
>
> Keep both facts about this commit, because together they are the real lesson and neither is true alone. The same author, in the same message, stated one gap with unusual honesty and asserted a verification that had not happened — and the honest sentence is what made the message *read* trustworthy. **A commit message is not evidence. CAE52 applies to the message itself: if it names a command as run, that command has to have been run.** The follow-up fix commit then repeated the pattern, diagnosing the incident as "the workflows had never run on GitHub" without checking — they had run three times, and one `gh run list` would have said so.

## What the case study establishes

Six named bugs in this range — the BSD `awk` marker replacement, the narrow suppression window, the `htmlFor` blind spot, the substring path exclusion, the anon-key false positive, and the inverted freshness comparison — plus the benchmark path-resolution bug and the piped-`tail` trap. Not one was found by reading the code. Every one was found because a command was executed and its **real output and exit code** were read.

The pattern generalizes into this pack's spine and is worth stating as the case study's conclusion rather than as an aphorism: the bugs were not unusual, and the code was not careless. What distinguishes this range is that at no point was a component trusted on the strength of looking correct. The characteristic AKOS practice visible across these commits — *leave the project verifiable after each step, so the next step builds on something that was actually run* — is this repository's own observed working discipline, recorded here from its commit history. It is not attributable to any external source, and the broader question it opens (how an agent maintains that property across a long-running, multi-session effort) belongs to a future `long-running-agents` pack, deliberately out of scope here.
