# Anti-Patterns — Coding Agents Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers failures that produce a *false record* — a claim, a green check, or a description that misrepresents the state of the work. Those are correctness defects and are scored as such, because they remove the very mechanism by which the next person would have caught the problem.

## The plausible completion

**Detect:** a report states a verifiable result — "all tests pass", "builds clean", "no other call sites" — and no corresponding command appears in the session, or the command appears but its output was never read.
**Why it fails:** the claim's entire function is to tell the reader they do not need to check. A false one does not merely fail to inform; it actively suppresses the verification that would have caught the defect. It is the highest-leverage bug the process can produce, and nothing downstream is positioned to catch it.
**Fix:** every claim of a verifiable state names the command that produced it and that command actually ran this session (CA2, CAE52). Claims without a backing command are deleted, not softened.

## The vacuous pass

**Detect:** a check passes on its very first run against code it was written to catch; a detector reports nothing on a corpus that should contain findings; every negative-case test passes while every positive-case test fails.
**Why it fails:** a check that cannot fail is indistinguishable from a check that passed legitimately, and it produces its false reassurance consistently, so nothing ever prompts a look. The asymmetric failure pattern is the giveaway: a broken matcher vacuously satisfies every "this must *not* be detected" assertion while failing every "this must be detected" one.
**Fix:** deliberately break the code or the fixture and confirm the check goes red before trusting its green (CA3, CAE41). Pair every absence assertion with a positive case proving the mechanism can fire at all (CAE42).

## The pipe-swallowed exit code

**Detect:** a verification is invoked inside a pipeline or a wrapper — `run-checks | tail -30`, a script whose last line is an `echo`, a function ending in a log statement — and its status is reported as success.
**Why it fails:** a pipeline's exit code is its last stage's. `tail` succeeds essentially always, including when the command feeding it failed catastrophically. The failure is silent, reproducible, and reads as a clean run: the output on screen even shows the error, while the status says zero.
**Fix:** never place a command between a check and the reading of its status. Capture the exit code directly, or set the shell to propagate pipeline failures, or inspect the per-stage status array (CAE54). Where output must be trimmed, capture the status separately first (CAE55).

## The first-match fix

**Detect:** a symbol was renamed or its signature changed, and the diff touches one call site; the search that would have enumerated the rest was never run, or was run and its results not exhausted.
**Why it fails:** it produces a repository that compiles and passes tests while containing two incompatible understandings of the same interface. The remaining call sites are in the places nobody searched — a test fixture, a config string, a re-export, a directory outside the one being worked in — and they fail at run time, far from the change.
**Fix:** enumerate every reference before the first edit and treat the enumeration as the change's scope (CA5, CAE8–CAE11). A search returning suspiciously few hits is re-run with a broader pattern before it is believed (CAE12).

## The blind overwrite

**Detect:** a file was written whose current contents were never read in this session; or a full-file write was used where a targeted edit would have served.
**Why it fails:** it is a deletion of unknown content reported as an edit. Whatever was there — a workaround, a comment explaining why the obvious approach fails, someone else's concurrent change — is gone with no record, and the operation succeeds silently either way. The asymmetry matters: a targeted edit against wrong assumptions *errors*; a full write against wrong assumptions *succeeds*.
**Fix:** read before writing, always, and prefer the targeted edit precisely because it fails loudly when the file is not what you think (CA6, CAE14–CAE16).

## The invented API

**Detect:** a call to a function, flag, config key, or package that does not exist in the installed version — usually well-named, idiomatic, and exactly what the library ought to provide.
**Why it fails:** the generative process produces the correct call and the plausible one identically, and the surrounding code gives no signal about which this is. Unlike a human's uncertainty, which shows, this arrives fully confident. It is caught by the type checker if you are lucky, at run time if you are not, and in a rarely-exercised branch if you are unlucky.
**Fix:** confirm every first-use external symbol against the installed source, type definitions, or `--help` before writing the call (CA7, CAE33–CAE37). If it cannot be confirmed, report the gap rather than filling it with the most plausible name.

## The imported style

**Detect:** a change introduces a naming scheme, error-handling pattern, test structure, or formatting convention that no neighbouring file uses — often a genuinely better one.
**Why it fails:** a codebase's conventions are load-bearing because they are uniform, not because they are optimal. A superior pattern in one file makes that file inconsistent with every other, costing every future reader more than the pattern saves. And the trade was made unilaterally by the party who does not pay for it.
**Fix:** take the convention from the nearest observed usage — the file, then the directory, then the project (CA8, CAE19–CAE21). Argue for a convention change as its own separate work; never implement the argument inside an unrelated fix (CAE24).

## The bundled refactor

**Detect:** a diff whose hunks cannot all be traced to the stated problem — a rename, a dead-branch removal, a formatting pass, or a clarity improvement riding alongside the actual fix.
**Why it fails:** it dilutes the diff's signal until review becomes approval-on-trust, and it welds the fix and the cleanup into a single fate. Reverting the fix during an incident now also reverts the cleanup, and reverting the cleanup is not possible at all.
**Fix:** one problem per change; improvements noticed along the way are recorded as follow-up work rather than appended (CA9, CAE26–CAE28). Where a fix genuinely requires a refactor, land the refactor first as its own behavior-preserving change.

## The unreproduced fix

**Detect:** a bug fix with no recorded failing state — no reproduction was run before the change, only a passing run after it.
**Why it fails:** without a red state there is no way to distinguish "fixed" from "the symptom moved", from "was never broken in the way described", from "the fix is inert and something unrelated changed". The change addresses the bug as described, and the description is frequently not the bug.
**Fix:** reproduce first and record the failure, apply the fix, re-run the identical reproduction and record the pass (CA11, CAE38–CAE39). Capture the reproduction as a regression test wherever the project has a place for one.

## The suppressed check

**Detect:** a failing lint rule, type error, or test went green through an ignore directive, a widened type, a skipped test, a file exclusion, a raised threshold, or a re-run until it passed.
**Why it fails:** the condition that produced the failure is untouched; only its visibility is gone. Worse, the mechanism that would have caught the next instance is now disabled, so the cost is paid repeatedly and by someone else. The failing check was the cheapest form the problem was ever going to take.
**Fix:** fix the cause (CA14, CAE77). Suppression is legitimate only for a demonstrated false positive, and then narrow, in place, and commented with why the check is wrong here (CAE78).

## The silent interface break

**Detect:** an exported signature, column, config key, or serialized format changed, with no enumeration of consumers and no migration sequence — often a small, clean-looking diff.
**Why it fails:** the size of the diff has no relationship to the blast radius. A one-character signature change with external consumers breaks every one of them, and if the consumers are outside the repository they cannot be fixed in the same commit at all, so there is no atomic version of this change.
**Fix:** count consumers before changing the shape; all-in-repo means one atomic commit, any-external means add-new, migrate, remove-old as separate steps (CA10, CAE60–CAE62). Persisted-data changes additionally carry a deploy ordering and a reverse migration (CAE63–CAE64).

## The sprawling commit

**Detect:** a commit that cannot be reverted alone without removing unrelated work or breaking the build; or a change landed as one commit large enough that review is approval by trust.
**Why it fails:** commit boundaries are only tested at the worst possible moment — during an incident, by someone who did not write the code. A commit bundling unrelated work cannot be selectively undone; a commit whose siblings it depends on cannot be checked out, which destroys bisection, the main reason history exists.
**Fix:** apply the revert test to every commit before landing it (CA17, CAE67–CAE68). Split mechanical changes from semantic ones so each is reviewable at the appropriate depth (CAE71).

## The marketing description

**Detect:** a pull request body that describes benefits, narrates effort, or restates the diff in prose, with a test plan describing what testing would cover rather than what was run — and no mention of any gap.
**Why it fails:** a reviewer already has the diff; what they cannot recover from it is why this approach, what was rejected, what was actually executed, and what was not. A description that omits the gaps because they weaken it is not a weaker description — it is a false one, and it misdirects scrutiny away from exactly the parts that need it.
**Fix:** state what changed, why this approach, the exact commands run with their real results, and what was not verified (CA18, CAE73–CAE76). The most useful line is usually the one admitting a gap.

## The stale green

**Detect:** verification was run, then an edit was made — a small cleanup, a comment, a rename while writing the summary — and the earlier green result is reported as the change's evidence.
**Why it fails:** the evidence describes a state of the repository that no longer exists. It is a true statement about a different artifact, which makes it harder to detect than an outright false one, and the edits made after verification are exactly the unreviewed, unhurried ones where a typo lands.
**Fix:** verification postdates the final edit (CAE51, CAE57). Any change made after the last green run — including one made in response to review — invalidates it and requires a re-run (CAE80).

## The confident unknown

**Detect:** a report presents a change at uniform confidence, with no distinction between what was executed and what was inferred, and no statement of what was left uncovered.
**Why it fails:** the reader has no way to discount any particular sentence, so they either trust all of it or none of it. Both are wrong, and the first is what usually happens. The unverified parts get the same credibility as the verified ones until one of them is wrong in production.
**Fix:** state what was run and what was not, and name each unverified aspect at the point where a reader would assume coverage (CA15, CAE59). Confidence is capped by the weakest link in the evidence, not set by how carefully the code was written.
