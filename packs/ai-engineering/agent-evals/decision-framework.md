# Decision Framework — Agent Evals Pack

Decision rules for evaluating an agent. Composes with [core/decision-framework.md](../../../core/decision-framework.md); scoring bands and severity anchors stay with [core/scoring-model.md](../../../core/scoring-model.md).

## Is this evidence, or is it a demonstration?

| What you were shown | Verdict |
|---|---|
| A handful of outputs the author chose, after the change | **Demonstration.** Ask for the suite. |
| A suite result with no baseline | **Incomplete.** Ask what it is being compared against. |
| A suite result vs. baseline, quality only | **Partial.** Ask for cost, latency, tool-call count. |
| A suite result vs. baseline on all four, single run per case | **Weak.** Ask for the run-to-run variance; the delta may be inside it. |
| A suite result vs. baseline, all four dimensions, multiple runs, corpus stated | **Evidence.** Now argue about the corpus. |

**Rule:** the question is never "do these outputs look better." It is "what would this comparison have shown if the change were useless." A design that cannot answer that is a demonstration wearing a suite's clothes.

## Which altitude does this failure need?

| The failure you're worried about | Altitude |
|---|---|
| A prompt instruction stopped being followed | **Unit** |
| The wrong tool gets picked, or picked with bad arguments | **Tool-call** |
| A tool gets called when it shouldn't be | **Tool-call**, negative case |
| The agent takes a bizarre or wasteful route to a right answer | **Trajectory** |
| The agent doesn't recover from a failing tool | **Trajectory**, with failure injection |
| The user doesn't get what they asked for | **End-to-end** |
| Cost or latency crept up | Any altitude — it is a dimension recorded on every run, not a case type |

**Rule:** pick the cheapest altitude that can actually observe the failure. A failure that only manifests across a whole task cannot be caught by a unit eval no matter how many unit evals you write.

## Which grader?

| The output is… | Grader | Watch for |
|---|---|---|
| An enum, ID, number, boolean, or structured field | **Deterministic / exact match** | Brittleness if the format is not truly canonical |
| Free text with named quality dimensions | **Rubric** | Levels without behavioral anchors — two graders will diverge |
| Open-ended, no reference answer exists | **LLM-as-judge** | Length bias, self-preference, drift when the judge model changes |
| Two candidates, and the question is which is better | **Pairwise** | Position bias; and that it yields no absolute quality claim |
| Verifiable by running something (a test, a compile, a schema validation) | **Deterministic**, via that check | Nothing — this is the best case, use it whenever available |

**Rule:** climb the ladder only as far as the output shape forces. Every rung up trades a known error rate for an unknown one.

## The suite went red. What happened?

Work the list in order; the order is what stops the convenient answer from being reached first.

1. **Is the case flaky?** Check its historical pass rate. If it sits between the bounds, this is a flakiness finding, not a regression finding — and the case gets fixed or removed, not re-run.
2. **Did the harness change?** A path resolution bug, a matching change, a new skip filter. Harness bugs produce failures and vacuous passes in the same run; the asymmetry between positive and negative cases is the usual clue.
3. **Did the corpus or grader change?** If so, this is not a comparison — one variable was supposed to move and two did. Re-run with only the change under test.
4. **Is it a real regression?** The change made the system worse. Fix the change.
5. **Is the case wrong?** The expected behavior encoded in the case no longer reflects the intended behavior. This is legitimate and it is the most dangerous branch on the list, because it is the one every regression wants to be mistaken for. It requires an explicit decision, a separate commit, and a reviewer who is not the author of the change that motivated it.

**Rule:** "the case is out of date" is a conclusion you may reach, never a hypothesis you may start from.

## May the baseline move?

| Situation | Answer |
|---|---|
| A change regressed the metric and the team wants to ship anyway | **No.** Record an accepted regression with its reason; the baseline stays. |
| The corpus grew, so the number is not comparable | **Yes** — as its own commit, stating the corpus revision, with the old and new numbers both recorded. |
| The grader was re-calibrated or the judge model changed | **Yes** — same conditions, and the re-calibration agreement rate is recorded with it. |
| The old baseline was measured wrong (harness bug, contaminated run) | **Yes** — and the bug is fixed and named in the commit. |
| It's Friday and CI is red | **No.** |

**Rule:** a baseline change is a decision with an author, a justification, and a reviewer. If it can happen as a side effect of running the suite, the mechanism is the finding — not the individual update.

## Is this contamination or noise?

| Signal | Reading |
|---|---|
| Iterated set improves, held-out set flat | **Contamination by iteration.** The suite has become a target. |
| Case passes warm, fails cold | **Context leakage.** The answer is in memory or an earlier turn. |
| Public-benchmark cases score far above private ones of similar difficulty | **Likely training-data leakage.** Label those cases and weight them accordingly. |
| Scores move without any change to the system | **Noise, harness drift, or a changed dependency** — check the harness before the model. |
| Score rises with no plausible capability mechanism behind it | **Contamination until proven otherwise.** |

**Rule:** noise is the last explanation to reach for, not the first. It is the one that requires no action, which is exactly why it is attractive.

## What does this pack score, and what doesn't it?

| The question | Where it belongs |
|---|---|
| Does this agent's behavior meet a measured bar across runs? | **Here.** |
| Does this deterministic code work? | [packs/testing/testing-pyramid](../../testing/testing-pyramid/README.md), [packs/testing/tdd](../../testing/tdd/README.md) |
| Did this release pass manual QA? | [packs/testing/qa-checklists](../../testing/qa-checklists/README.md) |
| How do I score an AKOS review 0–100? | [core/scoring-model.md](../../../core/scoring-model.md) |
| How sure should I be about this claim? | [core/confidence-model.md](../../../core/confidence-model.md) |
| Which agent architecture should this be? | [agent-foundations](../agent-foundations/README.md) |
| What should be in the agent's context? | [context-engineering](../context-engineering/README.md) |
| Are we building the right thing at all? | [packs/product/lean-startup](../../product/lean-startup/README.md) |

**Rule:** an eval answers "is this version better than that one at this task." It does not answer "is this task worth doing," and a suite improving while the product fails is a well-known and entirely coherent outcome.

## How much eval is enough for this change?

| Change | Minimum |
|---|---|
| A prompt wording tweak | Full suite, before and after, quality quad reported |
| A new tool added | New tool-call cases (positive, negative, failure-injected) before merge |
| A model version bump | Full suite plus judge re-calibration — the judge model may have moved too |
| A context/retrieval change | Groundedness metric explicitly, since that is the dimension most likely to move |
| A new user-facing task | At least one end-to-end case defining completion externally |
| A bug fix from production | The failing case added first, red, then the fix |

**Rule:** the size of the eval is set by which dimension the change can plausibly move, not by how big the diff is. A one-line prompt change can move every number in the suite.
