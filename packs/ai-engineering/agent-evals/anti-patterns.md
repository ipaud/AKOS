# Anti-Patterns — Agent Evals Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers failures that make a suite report something *false* rather than merely incomplete; those are correctness defects in the measurement itself and are scored as such.

## The moving baseline

**Detect:** the baseline number changed in the same commit, or the same command, as a run that failed against it. Or the harness has an `--update-baseline` flag and the git history shows it being used after red runs.
**Why it fails:** it makes a regression disappear without anyone deciding to accept it, and it destroys every later comparison too — from that point on the bar is a number nobody vouched for, quietly re-derived from whatever shipped. The damage is not the one regression; it is that the suite has stopped being able to say no.
**Fix:** baseline changes become their own reviewed commit with a written justification (AEE54). Delete the convenience flag (AEE55). Accepted regressions get recorded as accepted, with the tradeoff, rather than absorbed (AEE56).

## The vacuous pass

**Detect:** a case has never been observed failing. Or: every positive case fails and every negative case passes after a harness change — the asymmetry is the tell, because a broken path match makes "must not detect" hold for the wrong reason.
**Why it fails:** the case occupies a slot in a coverage claim while testing nothing, and it is indistinguishable from a working case in every report. A suite of these produces a perfect score over a system nobody has measured.
**Fix:** verify each case by deliberately breaking what it tests and confirming it goes red (AEE70). Test the harness itself — path resolution, matching, skip logic — since a harness bug manufactures vacuous passes wholesale (AEE74).

## The contaminated benchmark

**Detect:** the score rises with no plausible capability mechanism behind it. A case passes in a warm session and fails cold. The iterated set improves while the held-out set is flat. Public-benchmark cases score far above private ones of similar difficulty.
**Why it fails:** the eval is measuring recall of an answer the system already had — from pretraining, from accumulated context, or from having been tuned against these exact cases — rather than the capability it claims to measure. The number is real and means something other than what it says.
**Fix:** run cold, with no memory or carried session state (AEE64). Maintain a held-out set never used for iteration and report it separately (AEE7, AEE67). Label cases drawn from public sources (AEE66). Record every change made in response to a specific case (AEE69).

## The self-approving judge

**Detect:** the grader is the same model, in the same context, that produced the output under test — or a judge that has never been calibrated against human labels, or one whose model version changed without re-calibration.
**Why it fails:** a model asked to grade its own answer in the same context is defending a position, not evaluating one. An uncalibrated judge emits numbers with an unknown error rate, which move for reasons unrelated to the agent — most reliably, length and stylistic self-similarity.
**Fix:** the judge is a separate instance with a clean context (AEE24), calibrated against human-labeled cases with the agreement rate recorded (AEE22), re-calibrated on any judge-model or rubric change (AEE23), and explicitly instructed not to reward length or confidence (AEE25).

## The three-example proof

**Detect:** an agent change proposed on the strength of a handful of outputs the author tried, chosen by the author, after making the change. Phrases like "it handles these much better now."
**Why it fails:** the evidence is selected twice — which prompts, and when to stop — so it cannot distinguish a real improvement from one that helped these inputs and hurt the ones nobody ran. It is also unfalsifiable: nothing about the demonstration could have come out against the change.
**Fix:** accept changes on a suite result against a stated baseline, not on demonstrations (AE1, AE2). The three examples are fine as a starting point — they become the first three cases.

## The bare percentage

**Detect:** a result reported as a number with no comparison, no corpus, or neither. "Completion is at 74%." "100% recall."
**Why it fails:** a figure alone is a function of corpus, grader, run count, and version, and moving any of them moves it. Reported without those, readers supply the most flattering interpretation available — usually that the corpus is large and the comparison favorable.
**Fix:** every metric ships with its baseline and its corpus in the same output (AEE9, AEE72), and any metric computed over a curated set says explicitly that it is a regression guard, not a population estimate (AEE73).

## The correctness-only suite

**Detect:** the suite grades quality and records nothing else. A change ships on a three-point quality gain with no statement of what it cost.
**Why it fails:** unmeasured dimensions drift, mechanically — every accepted change was accepted on the measured axes, so cost, latency, and tool-call count are free to move. The result is a system that gets steadily better and steadily more expensive, one individually justified change at a time.
**Fix:** record tokens, wall-clock, and tool-call count on every run (AEE40), report all four dimensions on every comparison (AEE41), and gate cost and latency with their own thresholds (AEE42).

## The all-green dashboard over a failing task

**Detect:** step-level metrics look strong — tool selection accuracy, argument validity, per-step plausibility — while users report the agent doesn't finish what they ask.
**Why it fails:** completion depends on the conjunction of every step being right *and* the sequence terminating on the actual goal. Twelve steps at 95% is a coin flip on the whole task, and every one of those steps reports green. A dashboard of parts cannot observe a failure of the whole.
**Fix:** measure completion directly, in externally checkable terms, as the headline metric (AEE35, AEE36). Never accept the agent's own claim of completion as the check (AEE38). Report per category so a category failing entirely isn't averaged away (AEE39).

## The happy-path golden set

**Detect:** every case in the suite is a well-formed request with a clean tool response and an achievable goal. No error injection, no near-misses, no cases where the right answer is "I can't."
**Why it fails:** it measures the system on the distribution where it was already known to work. Recovery rate is unmeasured, false-positive drift is unmeasured, and the behavior under absence — where confabulation lives — is unmeasured. The suite is green and the production failure modes are all outside it.
**Fix:** add negative cases where correct behavior is not to act (AEE6, AEE13), failure-injection cases graded on what happens next (AEE46–AEE50), and cases where the answer is genuinely absent from the provided context (AEE31).

## The retry-to-green suite

**Detect:** red runs are habitually re-run rather than investigated. Someone can name "the flaky ones." Per-case pass rates are not tracked.
**Why it fails:** re-running is behaviorally identical to ignoring, and it is applied uniformly — including to the one genuine regression in the batch. Each tolerated flaky case makes the next easier to tolerate, and past some threshold the suite is a ritual that costs CI minutes and gates nothing.
**Fix:** track per-case pass rate and let the tracker flag flakiness rather than memory (AEE60). Remove avoidable non-determinism first — seeds, timestamps, live network (AEE62). Fix, re-scope, or remove flaky cases with the removal recorded (AEE61), and distinguish "failed" from "re-run to green" in the report (AEE63).

## The threshold set after the fact

**Detect:** the pass bar appears in the same commit as the result it evaluates, or exists only as a shared understanding of what counts as a meaningful drop.
**Why it fails:** a bar chosen after seeing the number is a rationalization, and "that's within noise" is especially seductive because it is sometimes true. Without a stated variance figure nobody can tell the difference, so the argument is settled by whoever wants to ship.
**Fix:** declare the bar — floor, maximum drop, gated metrics — in a committed config before the run (AEE51), set outside the suite's measured run-to-run variance (AEE52).

## The exact-match trap

**Detect:** free-prose output graded by string equality or near-equality against a reference answer, producing failures on outputs that are correct but phrased differently.
**Why it fails:** it is brittle in precisely the direction language varies, so the suite fills with false failures — which trains everyone to discount reds, arriving at the same place as flakiness by a different road. It also quietly rewards outputs that mimic the reference's style over ones that are better.
**Fix:** exact match only where a canonical form exists — enums, IDs, numbers, structured fields (AEE19). For prose, use a rubric with behavioral anchors (AEE20) or pairwise comparison (AEE26).

## The pairwise score that became an absolute

**Detect:** a win rate reported or reused as a quality figure. "The new version scores 63."
**Why it fails:** pairwise says B beats A, which is compatible with both being poor. Converting it into an absolute claim smuggles in a quality assertion the method never supported, and it is invisible once the number is downstream of the comparison that produced it.
**Fix:** report pairwise as a win rate against a named opponent, always (AEE27). If an absolute claim is needed, a rubric or a deterministic criterion has to produce it.

## The frozen suite

**Detect:** the suite has been at or near 100% for several release cycles, no case has been added in months, and production failures keep arriving that no case describes.
**Why it fails:** a fixed corpus is a regression guard for known failures. It cannot discover a new one, so it converges on green while the real failure rate is set entirely by inputs it never contemplated — and the green reads as health.
**Fix:** every production failure a reviewer would have wanted caught becomes a case before the fix merges (AE16). Refresh cases on a stated cadence from recent real failures (AEE68). Treat a long-running 100% as a signal the cases are too easy.

## The uncontrolled comparison

**Detect:** the before-and-after run differed in more than the change under test — the corpus grew, the grader was updated, the run count changed, a dependency moved.
**Why it fails:** two variables moved and one delta came out; nothing in the result attributes it. This is the failure that most often precedes a moving baseline, because the honest response — re-run controlled — costs time the deadline doesn't have.
**Fix:** hold corpus revision, grader version, and run count fixed across a comparison, and state any difference that could not be held (AEE58). Record all of them in the baseline itself, not just the number (AEE53).
