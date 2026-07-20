# Mental Models — Coding Agents Pack

Named models this pack contributes. Use them as diagnostic lenses while planning, making, verifying, or reviewing a change to a repository.

## The evidence ladder

Claims about a change sit at one of several rungs, and only the top two are evidence. Every rung below is a prediction wearing the grammar of a result.

| Rung | The claim rests on | What it actually establishes |
|---|---|---|
| **Described** | "This change makes the endpoint idempotent" | The intent of the author |
| **Written** | The code is on disk and reads correctly | Nothing about behavior |
| **Parsed** | It compiles / type-checks | The shapes agree; the logic is untested |
| **Executed** | A command ran and exited zero | This path did not crash under this input |
| **Asserted against a known failure** | The check was seen red, then green | The check can detect the thing it claims to detect |

**Diagnostic:** for every sentence in a completion report, name its rung. Any sentence at "described" or "written" phrased as a result is a false claim, not an optimistic one.

## The vacuous pass

A green result has two possible causes: the thing under test is correct, or the test cannot distinguish correct from incorrect. These are indistinguishable from the outside, and the second is self-perpetuating — a check that always passes never draws attention, so it accumulates trust in proportion to how long it has been broken. The signature is a suspiciously clean result: a whole suite green on first run, a detector that finds nothing on a corpus that should contain something, every negative case passing while every positive case fails.

**Diagnostic:** ask what specific breakage this check would catch, then cause that breakage and confirm it does. A check whose failure mode has never been observed is at best unmeasured and at worst inert.

## The exit-code chain

A command's status travels through exactly one channel, and that channel is easy to sever accidentally. A pipeline reports the status of its last stage, so `run-tests | tail -20` reports whether `tail` succeeded — which it essentially always does, including when the tests failed catastrophically. The same severance happens through a wrapper script that ends in an `echo`, a function whose last statement is a log line, a subshell whose result is discarded, and a command substitution used for its text.

**Diagnostic:** trace the path from the check that knows the answer to the place the answer is read. Count how many commands sit in between. Any command in that path that can succeed independently has broken the chain.

## The first-match trap

A search returns matches in an arbitrary order, and the first one carries no information about whether it is the only one. Acting on it produces a change that is locally complete and globally partial, and the resulting state is worse than not having started: the interface now has two meanings depending on which caller you read, and the inconsistency is invisible in the file that was edited.

**Diagnostic:** before editing any match, ask how many there are. If the number is unknown, the scope of the change is unknown, which means it is not ready to be made.

## The unread overwrite

Writing a file without reading it first is not a risky edit — it is a deletion of unknown content combined with an insertion, reported as an edit. Nothing about the operation reveals what was lost, which is why it never fails loudly and why the loss is usually discovered by someone else, later, with no obvious connection to the change that caused it. The asymmetry to hold: a targeted edit that assumes wrongly *errors*; a whole-file write that assumes wrongly *succeeds*.

**Diagnostic:** for any full-file write, ask what would happen if the file currently contained something unexpected. If the answer is "it would be silently gone", the operation needs to be a read plus a targeted edit.

## Blast radius

The set of things a change can break, which is almost never the set of files it touches. A private helper's radius is its module. An exported function's radius is every importer. A database column's radius includes every query, every serializer, every report, and every consumer reading the table directly. A config key's radius includes every environment where it is set. Radius is the property that decides whether a change is an edit or a migration, and it is determined by consumers, not by the size of the diff.

**Diagnostic:** name the consumers before naming the fix. If any consumer is outside the repository, the change cannot be atomic and must be staged as add-new, migrate, remove-old.

## The scope contract

Every task carries an implicit contract about what will change, and a diff either honors it or quietly renegotiates it. Opportunistic improvements are the renegotiation: each is individually defensible and collectively converts a reviewable fix into a change of unclear purpose. The cost is not aesthetic — a bundled change cannot be reverted selectively, so the fix and the cleanup share a fate that neither of them chose.

**Diagnostic:** for each hunk in the diff, name the sentence in the task that requires it. Any hunk without one is either scope creep or a discovered requirement that should be stated out loud.

## The revert test

The operational definition of a well-drawn commit: could this be reverted, alone, on a bad night, by someone who did not write it, without taking anything else with it and without breaking the build? It is a sharper question than "is this commit small" or "is this commit atomic", because it forces the two real failure modes into view — a commit that carries unrelated work, and a commit that depends on a sibling commit to build.

**Diagnostic:** for each commit, describe what reverting it alone would do. Collateral damage means it bundles too much; a broken tree means it was split too finely along the wrong seam.

## The convention gradient

In any file there is a local convention, in the directory a broader one, in the project a broader one still, and outside it a general community style. They frequently disagree. The rule for resolving the disagreement is proximity: the nearest observed convention wins, because that is the one the next reader of this file will expect. A community best practice imported into a file that does not use it is not an improvement; it is a discontinuity introduced at the point where continuity is most visible.

**Diagnostic:** before writing a line, find the nearest existing example of the same kind of line and match it. If none exists in the file, widen to the directory, then the project. Reach outside the project only when nothing inside it answers.

## The claim ledger

A pull request description is best read as a list of assertions, each of which is either backed by an executed command or is a bet. The reviewer's job is made possible or impossible by whether the ledger is honest: an accurate ledger tells them exactly which parts they need to check themselves, and an inflated one tells them nothing while appearing to tell them everything. The single most useful entry in a good ledger is the one that says what was *not* verified.

**Diagnostic:** read the description and mark each claim as executed, inferred, or unstated-gap. A description with no inferred claims and no stated gaps is usually not more rigorous — it is less honest.

## Green as a goal versus green as a signal

The same word describes two opposite orientations. As a signal, green means the checks ran and found nothing; the checks are instrumentation and their sensitivity is an asset. As a goal, green is the state to reach, and anything producing red is an obstacle — which makes suppression, skipping, and rule-loosening feel like progress rather than like disabling the smoke detector. The two are impossible to tell apart from the final state of the repository; they are visible only in how the red was resolved.

**Diagnostic:** for each check that went from red to green during the work, ask what changed. If the answer is "the check", not "the code", the orientation has inverted.
