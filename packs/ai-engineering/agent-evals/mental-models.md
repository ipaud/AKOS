# Mental Models — Agent Evals Pack

Named models this pack contributes. Use them as diagnostic lenses while building, reading, or distrusting an eval suite.

## The four eval altitudes

Evals operate at four levels, and each catches a class of failure the others structurally cannot see.

| Altitude | Input → assertion | Catches | Cannot catch | Cost |
|---|---|---|---|---|
| **Unit eval** | One prompt → one response, graded | A broken instruction, a format violation, a regressed classification | Anything requiring more than one turn | Lowest |
| **Tool-call eval** | A situation → the call(s) made, graded on selection and arguments | Wrong tool chosen, malformed or hallucinated arguments, a required call skipped | Whether the sequence as a whole made sense | Low |
| **Trajectory eval** | A task → the full path taken, graded on route | Wandering, redundant calls, an unacceptable route to a correct answer, non-recovery from an error | Whether the user's task was actually served | High |
| **End-to-end eval** | A task → the final outcome, graded on completion | Did the thing get done | *Where* it went wrong | Highest |

The failure this model exists to prevent is a suite that lives entirely at one altitude and reports its coverage as though it lived at all four.

**Diagnostic:** name the altitude of every case in the suite and count them. An empty row is a blind spot with a name; report it rather than letting the aggregate imply it isn't there.

## The grader ladder

Grader types trade cost and brittleness against flexibility, in a fixed order.

| Grader | Good at | Fails at | Needs calibration |
|---|---|---|---|
| **Exact match / deterministic check** | Structured output, classifications, presence of a required field, a test that passes | Anything phrased more than one way — brittle in exactly the direction language is variable | No |
| **Rubric-based** | Structured partial credit across named criteria; making disagreement locatable | Criteria vague enough that two graders diverge | Between human graders |
| **LLM-as-judge** | Open-ended quality where no reference answer exists | Its own biases — length, verbosity, style match, self-preference | Yes, against human labels |
| **Pairwise comparison** | "Is B better than A" — the question changes usually ask | Absolute quality; a pair of two bad outputs still yields a winner | Position-bias control |

The ladder is not a quality ordering — a deterministic check, where one applies, beats a judge on every axis including trustworthiness. It is an escalation path: climb only as far as the output shape forces you to.

**Diagnostic:** for each case, ask whether the rung below would have worked. A judge grading something a schema check could have decided is spending money to add variance.

## The completion cliff

Step-level metrics and outcome metrics do not degrade together. A system can hold high tool-selection accuracy, high argument validity, and high per-step plausibility while its task completion rate falls off, because completion depends on the conjunction of every step being right *and* the sequence terminating on the actual goal. Twelve steps at 95% each is a coin flip on the whole task. This is why a dashboard of green step metrics is compatible with a system that mostly does not work, and why the completion number has to be measured directly rather than inferred from its parts.

**Diagnostic:** if step metrics are strong and users are unhappy, the missing measurement is completion, not a better step metric. Multiply the per-step rates and compare the product against the observed completion rate — a large gap means the steps aren't independent, which is itself the finding.

## The baseline as a contract

A baseline is not a stored number. It is an agreement that a specific number, produced by a specific corpus and grader at a specific version, is the thing future changes must beat. Its entire value comes from being harder to change than the code it guards. The moment a baseline can be updated as a convenience — a flag, a re-record, a "the old one was stale anyway" in the same commit as a failing run — it stops being a contract and becomes a mirror.

**Diagnostic:** ask how a baseline gets updated in this repo. If the answer names a command rather than a commit and a reviewer, the contract does not exist yet regardless of what the numbers say.

## The contamination gradient

An eval measures capability only to the extent its answers were not already available to the system. Leakage arrives by three routes of decreasing obviousness:

1. **Training-data leakage** — the case, or its answer, was in pretraining. Suspected when a public benchmark scores far above private ones of comparable difficulty.
2. **Context leakage** — the answer is in the agent's accumulated context: a memory file, a cached note, a prior turn of the same session. Suspected when a case passes in a warm session and fails cold.
3. **Iteration leakage** — the system was tuned against these cases until it fit them. Suspected when the iterated set improves and a held-out set doesn't.

All three yield the same observable: rising score, unchanged capability.

**Diagnostic:** run the suspect case in a fresh context with no memory, and run the held-out set. Two clean numbers that diverge from the headline number locate which route is active.

## The flakiness tax

A flaky case does not cost one case's worth of value. It taxes every case around it, because a suite whose reds are sometimes meaningless trains its readers to re-run rather than investigate — and a re-run is behaviorally identical to ignoring, applied uniformly to the real regressions in the same batch. The tax compounds: each tolerated flaky case makes the next one easier to tolerate, and there is a threshold past which the suite is a ritual.

**Diagnostic:** count how often anyone re-runs a red suite without investigating first. If the answer is "usually," the number of flaky cases is already past the point where the suite gates anything.

## Two populations, not two numbers

Comparing a change against a baseline on a non-deterministic system is comparing two distributions, not two values. One run per case gives one sample from each, and a difference between two samples is not a difference between two systems. The practical consequence is unglamorous: run each case several times, report a rate with its spread, and set the regression threshold outside the observed run-to-run variance rather than at whatever gap looks meaningful.

**Diagnostic:** run the *same* version twice through the whole suite and record the delta. That number is the noise floor. A regression threshold tighter than it will fire constantly; a claimed improvement smaller than it is not yet evidence of anything.

## The suite as a specification of "better"

Whatever the suite measures is what the system will be optimized toward, by every person making every subsequent change. This makes the suite a de facto specification — usually a more binding one than any written requirements doc, because it is the thing that says no. It also means the suite's gaps are specifications too: an unmeasured dimension is not neutral, it is permission for that dimension to degrade.

**Diagnostic:** read the suite as though it were the product requirements. If a stakeholder would be surprised by what it does and does not demand, the suite and the intent have diverged, and the suite will win.

## The vacuous pass

A case can pass for the wrong reason: a grader that matches anything, a path that resolves to nothing so a "must not detect" check trivially holds, an assertion comparing a value to itself. Vacuous passes cluster in negative cases, because there "nothing happened" is both the correct outcome and the signature of a broken check — the two are indistinguishable from the report alone. The only reliable detector is deliberate sabotage: break the thing, confirm the case notices.

**Diagnostic:** for any case never observed red, treat its coverage claim as unverified. A suite of cases where none has been seen to fail has an unknown relationship to the system it claims to measure.
