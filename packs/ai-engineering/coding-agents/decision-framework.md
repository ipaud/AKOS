# Decision Framework — Coding Agents Pack

Decision rules for the edit itself. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Is this task done

Work down the ladder. The task is done at the first row whose answer is "yes" *and* whose evidence was produced in this session.

| Question | If no |
|---|---|
| Did a command run against the changed artifact? | Not done — everything so far is a prediction |
| Was its exit code read, and was it zero? | Not done — a readable log is not a result |
| Was it the project's own command (manifest, Makefile, CI config)? | Re-run the real one; a hand-built equivalent can differ in flags and scope |
| Did it run *after* the last edit? | Re-run; an edit after the last green invalidates it |
| For a bug fix: was the same reproduction seen failing first? | Not demonstrated — you have a change, not a fix |
| For a new check: was it seen failing once on purpose? | Not trusted — a check never red may be inert |
| Is every claim in the report backed by one of the above? | Delete the unbacked claims or mark them unverified |

**Rule:** "it should work" is a valid thing to think and never a valid thing to report. Whatever is left unverified at the end of this table is named as unverified, at the point in the report where a reader would otherwise assume it was covered.

## Edit, or migration

Count the consumers of the thing being changed.

| Consumers | This is | Sequence |
|---|---|---|
| One, private to the module | An **edit** | Change it |
| Several, all inside the repository | A **migration, atomic** | Definition and every caller in one commit; no intermediate broken state |
| Any outside the repository (published package, other service, external client) | A **migration, staged** | Add the new form → migrate consumers → remove the old form, as separate changes |
| Persisted data (column, serialized format, wire protocol) | A **migration, staged and deploy-ordered** | Additive change → deploy → stop reading the old → deploy → remove the old |
| Unknown | **Not ready** | Enumerate first; an unknown consumer count is an unknown blast radius |

**Rule:** the consumer count decides the shape of the work, not the size of the diff. A one-character change to an exported signature is a migration; a two-hundred-line rewrite of a private helper is an edit.

## Full-file write, targeted edit, or don't touch it

| Situation | Choice |
|---|---|
| Changing part of an existing file | **Targeted edit** against text you have read — it fails loudly if the file is not what you think |
| Creating a file that does not exist | **Write** — nothing to lose |
| Replacing an existing file wholesale | **Read it in full first**, then write, and state why a targeted edit was insufficient |
| The file is generated, vendored, or a lockfile | **Run the generator**; hand edits are reverted by the next regeneration |
| You have not read the file this session | **Read it first.** There is no fourth option |

**Rule:** prefer the operation that fails when your assumption is wrong. A targeted edit errors on a stale assumption; a whole-file write succeeds and deletes the evidence.

## Which convention wins

Resolve by proximity — nearest observed usage first.

1. **The same file.** If the file already does this kind of thing, match it exactly, including things you would do differently.
2. **The same directory.** For a new file, take naming, structure, and test placement from its siblings.
3. **The project.** A configured formatter, linter, or style file is authoritative; run it rather than reproducing its rules.
4. **The project's stated conventions.** Contributor docs and agent-instruction files, where they exist.
5. **The wider community.** Only when nothing inside the project answers the question.

**Rule:** a better pattern imported from outside into a file that does not use it is a discontinuity, not an improvement. If the project's convention is genuinely wrong, that is a separate, argued change — never a silent rider on unrelated work.

## In this diff, or not

For each hunk, ask which the task requires.

| The hunk | Verdict |
|---|---|
| Required by the stated problem | **In** |
| Required to make the required part work (an import, a type, a test) | **In** |
| A refactor the fix genuinely depends on | **Out of this diff — land it first**, as its own behavior-preserving change |
| An improvement noticed along the way | **Out** — record it as follow-up work |
| Formatting of lines the change did not otherwise touch | **Out** |
| Debug logging, scratch, a check loosened during investigation | **Out** — residue, not fix |
| A behavior change nobody asked for | **Out**, or **stated explicitly** if it turns out to be necessary |

**Rule:** every hunk should be traceable to a sentence in the task. A hunk with no such sentence is either scope creep or a discovered requirement that has not been stated out loud yet.

## Responding to a failing check

1. **Reproduce it locally** if it came from CI. A failure you have not seen is one you cannot diagnose.
2. **Determine what it is telling you.** A type error, a lint violation, and a failing test each name a specific condition in the code.
3. **Fix that condition.** This is the default and the answer in the large majority of cases.
4. **If you believe it is a false positive, demonstrate it** — explain why the condition the check names does not hold here. Belief is not demonstration.
5. **Only then suppress**, narrowly: one line or one symbol, in place, with a comment stating why the check is wrong here. Never a file exclusion, never a rule disabled globally, never a widened type standing in for an explanation.
6. **Re-run everything.** The change you just made is unverified.

**Never on this list:** re-running until it passes, marking a test skipped to get green, excluding the file from the checker, or raising the threshold that flagged it. Each converts a visible problem into an invisible one and removes the mechanism that would have caught the next instance.

## Fix the code or fix the test

When a test fails after a change, exactly one of them is wrong.

| Evidence | Conclusion |
|---|---|
| The test encodes the behavior the task asked you to change | **The test is stale** — update it, and say so explicitly in the description |
| The test encodes behavior nobody asked you to change | **The code is wrong** — the change caused a regression |
| The test's assertion never matched the code, and both are unchanged | **The test was always broken** — fix it separately, and check what else it was silently not testing |
| You are not sure | **Not ready to decide.** Read the test's intent and its history before touching either |

**Rule:** amending a test to match the code you just wrote is the single easiest way to convert a real regression into a green build. It is legitimate exactly when the task's requirements changed the expected behavior, and it is stated out loud when it happens.

## How much verification does this change need

| Change | Minimum evidence |
|---|---|
| Comment, docstring, or documentation only | Lint/format, if the project checks docs |
| Behavior-preserving refactor | Full test suite green before and after; build and type check |
| Bug fix | Reproduction red → fix → same reproduction green; regression test added; suite green |
| New feature | Tests for the new behavior, each seen red once; suite green; build, type check, lint |
| Interface change | Everything above, plus every enumerated consumer updated and the suite green |
| Migration touching persisted data | Everything above, plus the reverse migration exercised, and the deploy ordering stated |
| Dependency change | Everything above, plus the resolved version recorded and the build run from a clean install |

**Rule:** the evidence floor is set by the change's blast radius, not by its line count or by how confident it feels.
