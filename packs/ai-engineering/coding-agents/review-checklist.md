# Review Checklist — Coding Agents Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items — a false record of what was verified — and block in every reasoning profile.

Reviewing an agent's edit means reading the diff, the commit history, and where available the session transcript and the CI log — not the completion summary alone. A completion claim cannot be reviewed against the summary that makes it. Several checks below require the transcript or the log; those say so.

## Critical (blocks in every profile)

- [ ] ★ **Transcript check:** every claim of a verifiable state ("tests pass", "builds clean", "no other callers") is backed by a command that actually ran this session. (CA2, CAE52)
- [ ] ★ **Transcript check:** the exit code of each verification command was observed, and no nonzero exit was reported as success. (CA12, CAE53)
- [ ] ★ **Transcript check:** no verification was piped into another command that masks its status (`cmd | tail`, a wrapper whose last statement is an `echo`), or where one was, the failure was propagated explicitly. (CAE54)
- [ ] ★ Verification postdates the final edit; no green result from before a later change is being offered as this change's evidence. (CAE51, CAE57)
- [ ] ★ Every new or modified check was seen failing once on purpose before its passing result was trusted. (CA3, CAE41)
- [ ] ★ No file was written whose current contents were not read in this session. (CA6, CAE14)
- [ ] ★ Every external symbol used for the first time (function, flag, config key, package) was confirmed against the installed version, not recalled. (CA7, CAE33)
- [ ] ★ No failing check was resolved by suppressing it — no ignore directive, widened type, skipped test, file exclusion, raised threshold, or re-run-until-green — without a demonstrated false positive. (CA14, CAE77)
- [ ] ★ A shared interface change enumerated its consumers and follows a stated sequence; no commit leaves in-repo callers disagreeing with the definition. (CA10, CAE60–CAE62)

## High

- [ ] For a bug fix: the failure was reproduced and its output recorded *before* the change, and the identical reproduction was re-run and recorded after. (CA11, CAE38, CAE39)
- [ ] Every symbol renamed or changed in signature was searched repository-wide, and the enumerated result set is exhausted or each exception carries a stated reason. (CA5, CAE8, CAE11)
- [ ] The search covered non-code references — tests, fixtures, docs, config, string literals, re-exports. (CAE9, CAE10)
- [ ] The project's build ran to completion after the change and its exit code was checked. (CA13, CAE46)
- [ ] The project's type checker ran; no new type errors are present. (CAE47)
- [ ] The project's linter and formatter ran; no new violations were left for CI to surface. (CAE48)
- [ ] Verification used the project's own command (manifest, Makefile, CI config), not a hand-constructed equivalent. (CAE50)
- [ ] The full relevant test suite ran after the change, not only the test written for it. (CAE43)
- [ ] Any check that could not be run in this environment is named explicitly as unverified in the report. (CAE49, CAE59)
- [ ] The diff contains only changes the stated problem requires; no bundled refactor, cleanup, or unrelated rename. (CA9, CAE26)
- [ ] New code matches the surrounding conventions — naming, formatting, imports, error handling, test placement — including conventions the author would argue against. (CA8, CAE19–CAE21, CAE24)
- [ ] A test amended after failing was demonstrably the wrong party, and the reasoning is stated. (CAE44)
- [ ] Every commit leaves the repository in a state where the build and tests pass. (CA17, CAE67)
- [ ] No commit bundles work that could not be reverted alone without collateral damage. (CAE68)
- [ ] The pull request test plan lists the exact commands run and their real results, not intended coverage. (CA18, CAE74)
- [ ] Known gaps — untested paths, unverified checks, deferred work, ordering caveats — are stated in the description. (CAE75)
- [ ] A database migration ships with its reverse, or records why the change is irreversible. (CAE63)
- [ ] A destructive migration step is separated from the code change that stops using the dropped object, and lands after it. (CAE64)

## Medium

- [ ] Orientation preceded the first edit: build/test/lint entry points identified from the repository, target files located by search. (CA4, CAE1, CAE2)
- [ ] The project's contributor or agent-instruction files were read before the first edit, where they exist. (CAE3)
- [ ] Conventions and APIs were checked against the installed (pinned) version, not the latest published one. (CAE5)
- [ ] A search returning an unexpectedly small result set was re-run with a broader pattern before being trusted. (CAE12)
- [ ] A whole-file rewrite of an existing file states why a targeted edit was insufficient. (CAE16)
- [ ] Generated files, lockfiles, and vendored directories were regenerated rather than hand-edited. (CAE17)
- [ ] No new dependency was added where an existing one or the standard library already covered the need. (CAE22)
- [ ] No formatting-only changes appear on lines the change did not otherwise touch. (CAE23)
- [ ] Improvements noticed during the task were recorded as follow-up work rather than appended to the diff. (CAE27)
- [ ] A required refactor was landed as its own behavior-preserving change, not interleaved with the fix. (CAE28)
- [ ] Mechanical changes (renames, moves, formatting) are separated from semantic ones. (CA16, CAE29, CAE71)
- [ ] No debugging artifacts remain: temporary logging, commented-out experiments, scratch files, loosened checks. (CAE30)
- [ ] A behavior change outside the stated problem is stated explicitly rather than made silently. (CAE31)
- [ ] The reproduction was captured as a regression test where the project has a place for one. (CAE40)
- [ ] Every absence assertion ("nothing detected", "no error raised") is paired with a positive case proving the mechanism can fire. (CAE42)
- [ ] A skipped or quarantined test carries a stated reason and a condition for re-enabling. (CAE45)
- [ ] An unexpectedly clean first run was investigated rather than accepted. (CAE58)
- [ ] A change to a persisted or transmitted format states its compatibility direction. (CAE65)
- [ ] A renamed or removed config key keeps the old key working with a deprecation warning, or the project's policy permitting otherwise is cited. (CAE66)
- [ ] Commit messages state what changed and why, in the project's format. (CAE69)
- [ ] The staged set was inspected before committing; no scratch files, local config, or credentials were included. (CAE72)
- [ ] The description states why this approach, and what alternatives were rejected where a real choice existed. (CAE73)
- [ ] A suppression for a demonstrated false positive is narrow, in place, and commented with why the check is wrong here. (CAE78)
- [ ] A review comment was resolved by changing the code or by an explicit stated disagreement, not by restating the original reasoning. (CAE79)
- [ ] Verification commands were re-run after responding to review or CI feedback. (CAE80)

## Low

- [ ] The working tree's starting state was known — branch, cleanliness, foreign uncommitted changes. (CAE6)
- [ ] A materially different structure discovered mid-edit triggered a restated plan rather than silent improvisation. (CAE7)
- [ ] A symbol-aware lookup was preferred over plain text search where the language provides one. (CAE13)
- [ ] A file read early in a long session was re-read before a much later write. (CAE18)
- [ ] The project's formatter was run rather than its rules reproduced by hand. (CAE25)
- [ ] No new abstraction was introduced with exactly one caller and no stated second one. (CAE32)
- [ ] Package names were verified in the registry before being added to a manifest, with the resolved version recorded. (CAE36)
- [ ] CLI invocations were validated against the installed tool's interface. (CAE37)
- [ ] Empty command output was not read as success. (CAE56)
- [ ] Truncated output did not hide a failure summary; where truncation was necessary, the exit code was captured separately. (CAE55)
- [ ] A large change was split into a sequence of independently reviewable commits. (CAE70)

## Process

- [ ] The review inspected the diff, the commit history, and the transcript or CI log — not the completion summary alone.
- [ ] For each unbacked claim found, the review checked whether the underlying state is actually true, not only that the claim was unsupported.
- [ ] For each suppressed check found, the review traced what the check would have caught and whether the underlying defect is still present.
- [ ] For each interface change, the review independently enumerated consumers rather than accepting the author's count.
- [ ] Findings name the exact command to run or the exact line to change — never "verify this properly" without saying what to execute.
