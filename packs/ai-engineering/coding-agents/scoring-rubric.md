# Scoring Rubric — Coding Agents Pack

Standalone 0–100 score for the process discipline behind a change made by an agent to a real repository — the edit, its verification, and its record. Not a dimension of the twelve-lens UI review pipeline (`core/review-pipeline.md` scores the product; this pack scores how the change to it was made). Scored against the diff, the commit history, and the session transcript or CI log. Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

One class of finding is scored as a correctness defect rather than a process concern: **a false record** — a completion claim, a green check, or a description that misrepresents what was verified. These are graded like a wrong calculation, because they do not merely fail to help, they actively suppress the verification that would have caught the underlying problem. Everything downstream acts on them.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Completion claim asserting a verifiable state with no command executed to support it (CA2, CAE52) | −25 (CRITICAL) |
| Nonzero exit code reported or treated as success (CA12, CAE53) | −25 (CRITICAL) |
| Verification's exit status masked by a pipe or wrapper, and the result reported as green (CAE54) | −25 (CRITICAL) |
| A check trusted without ever having been seen fail, where it is later shown it could not have failed (CA3, CAE41) | −25 (CRITICAL) |
| File written whose contents were never read, destroying unrecorded content (CA6, CAE14) | −25 (CRITICAL) |
| Failing check resolved by suppression, skip, exclusion, threshold change, or retry-until-green (CA14, CAE77) | −25 (CRITICAL) |
| Shared interface changed with consumers left unenumerated or unmigrated (CA10, CAE60–CAE62) | −25 (CRITICAL) |
| Call to a function, flag, config key, or package not verified to exist in the installed version (CA7, CAE33) | −25 (CRITICAL) |
| Green result reported that predates the final edit (CAE51, CAE57) | −10 (HIGH) |
| Bug fix with no reproduced failure before the change (CA11, CAE38) | −10 (HIGH) |
| Symbol changed without a repository-wide search; call sites left inconsistent (CA5, CAE8–CAE11) | −10 per missed site, cap −20 (HIGH) |
| Build, type check, or lint not run after the change, and not named as unverified (CA13, CAE46–CAE49) | −10 each, cap −20 (HIGH) |
| Verification run with a hand-built command instead of the project's own (CAE50) | −10 (HIGH) |
| Unrelated refactor, cleanup, or rename bundled into the diff (CA9, CAE26) | −10 (HIGH) |
| New code imposes a convention no neighbouring file uses (CA8, CAE19–CAE21) | −10 (HIGH) |
| Test amended to match the new code where the code was the wrong party (CAE44) | −10 (HIGH) |
| Commit that cannot be reverted alone, or that leaves the tree non-building (CA17, CAE67, CAE68) | −10 each (HIGH) |
| Test plan describes intended coverage instead of executed commands and real results (CA18, CAE74) | −10 (HIGH) |
| Known gap omitted from the description (CAE75) | −10 (HIGH) |
| Migration without a reverse, or a destructive step landed with the code change (CAE63, CAE64) | −10 each (HIGH) |
| Orientation skipped: entry points or target files discovered mid-edit (CA4, CAE1, CAE2) | −4 (MEDIUM) |
| Whole-file rewrite where a targeted edit would have served, unjustified (CAE15, CAE16) | −4 each (MEDIUM) |
| Generated file, lockfile, or vendored code hand-edited (CAE17) | −4 each (MEDIUM) |
| Dependency added where an existing one or the standard library covered the need (CAE22) | −4 (MEDIUM) |
| Formatting-only changes on lines the change did not otherwise touch (CAE23) | −4 per file, cap −16 (MEDIUM) |
| Debugging residue left in the diff — logging, commented experiments, scratch, loosened check (CAE30) | −4 each (MEDIUM) |
| Absence assertion with no paired positive case proving the mechanism can fire (CAE42) | −4 each (MEDIUM) |
| Behavior changed outside the stated problem without saying so (CAE31) | −4 each (MEDIUM) |
| Reproduction not captured as a regression test where the project has a place for one (CAE40) | −4 (MEDIUM) |
| Test skipped or quarantined with no stated reason and re-enabling condition (CAE45) | −4 each (MEDIUM) |
| Suppression for a false positive that is file-wide or rule-wide rather than narrow and commented (CAE78) | −4 each (MEDIUM) |
| Commit message describing effort rather than change (CAE69) | −4 each (MEDIUM) |
| Mechanical and semantic changes mixed in one commit (CA16, CAE29, CAE71) | −4 each (MEDIUM) |
| Review comment closed by restating the original reasoning without addressing the objection (CAE79) | −4 each (MEDIUM) |
| Verification not re-run after responding to review or CI feedback (CAE80) | −4 (MEDIUM) |
| Compatibility direction unstated on a persisted or transmitted format change (CAE65) | −4 (MEDIUM) |
| Working tree's starting state unknown before editing (CAE6) | −1, cap −5 (LOW) |
| Text search used where a symbol-aware lookup was available (CAE13) | −1 each, cap −5 (LOW) |
| Formatter's rules reproduced by hand instead of running it (CAE25) | −1 each, cap −5 (LOW) |
| New abstraction with exactly one caller and no stated second (CAE32) | −1 each, cap −5 (LOW) |
| Empty command output read as success (CAE56) | −1 each, cap −5 (LOW) |
| Large change landed as one commit where a reviewable sequence was available (CAE70) | −1 each, cap −5 (LOW) |

## Hard caps

- **Any open CRITICAL finding: score ≤ 59 (BLOCKED).** A change whose record misstates what was verified fails this dimension regardless of how good the code turns out to be — the defect is that nobody downstream can now tell.
- No verification command executed at all against the changed artifact, Production profile: **cap 39**. This is the pack's spine; a change with zero executed evidence has not been shown to do anything.
- Verification run but exit codes never observed (output read instead): **cap 69**.
- A bug fix with a passing after-state and no observed before-state: **cap 79**. A fix that never had a red is not demonstrated.
- Completion reported at uniform confidence with no distinction between executed and inferred, and no stated gaps (CA15, CAE59): **cap 84**.

## Modifiers

- Every claim in the report traceable to a named command with its real output quoted: **+5** (cap 100).
- Each new check demonstrably exercised in its failing direction before being trusted (broken, seen red, restored, seen green): **+5** (cap 100).
- The change's blast radius enumerated explicitly (consumer list) before the interface was touched: **+3**.
- Explicit "what was not verified" section present and non-empty where gaps genuinely exist: **+3**.
- A defect found *by* the agent's own verification during the work, and recorded rather than quietly fixed: **+2**. The point of running things is finding things; saying so is what makes the practice legible.
- Repeat finding from a previous review, unfixed without a recorded tradeoff: **double its deduction**.
- Finding fixed at the instance only, where a check, a lint rule, or a test could have prevented the class: **no credit** — the finding remains open.

## Interpretation anchors

- **95** — every claim carries the command that produced it; each new check was seen red before green; the diff is scoped to the stated problem and matches local convention; interface consumers were enumerated; the description names what was not verified. Remaining findings are hygiene.
- **85** — sound and genuinely verified; a cluster of MEDIUMs (a bundled cleanup, a stray formatting hunk, a commit message describing effort, a regression test not added) to schedule.
- **72** — the work was done and the checks were run, but the record is thin: no before-state on a fix, gaps unstated, build run without its exit code being read. Acceptable pre-production with fixes queued.
- **58** — the report says the tests pass and no test was run, or a lint failure went green by way of an ignore directive. BLOCKED until the actual state is established by execution and the mechanism that produced the false record is corrected — not just the one claim edited.
- **35** — a change delivered with no executed evidence of any kind: plausible code, a confident summary, nothing run. This is the failure the pack exists to name.
