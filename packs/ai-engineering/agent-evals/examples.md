# Examples — Agent Evals Pack

Invented cases, plus one real worked assessment of this repository's own eval harness. Fabricated scenarios are marked as such; the `benchmarks/` assessment describes code that exists in this repo and is deliberately honest about what it does not do.

## Worked example: AKOS's own `benchmarks/` harness

This repository ships a real eval harness at [`benchmarks/`](../../../benchmarks/README.md), driven by [`benchmarks/runners/run.py`](../../../benchmarks/runners/run.py), with 21 cases listed in [`manifest.yaml`](../../../benchmarks/manifest.yaml) and its methodology written up in [`docs/benchmarks/overview.md`](../../../docs/benchmarks/overview.md). It is worth reading as a worked example rather than a hypothetical, because it gets several of this pack's hardest rules right and has a set of real, nameable gaps — which is the realistic state of most eval suites, and a more useful calibration target than either a strawman or an ideal.

**What it is:** each case is a synthetic mini-project under `cases/<id>/fixture/` plus an `expected.yaml` declaring `must_detect` and `must_not_detect`. The harness runs the real rules engine (`rules/`) against the fixture and diffs actual findings against expected ones, matching on rule ID, path, and line number within a tolerance of three. Nineteen cases are deterministic (the rules engine's Level A/B rule classes); two exercise a Level C LLM-assisted path through a deterministic offline mock provider.

### What it gets right

- **Positive and negative cases for every rule (AEE6).** Every Level A/B rule has at least one true-positive case *and* at least one realistic near-miss that must not fire — a suppressed policy, an anon-role JWT rather than a service-role one, a guarded destructive statement, a project that never adopted the up/down migration convention. This is the discipline most suites skip, and it is the one that catches false-positive drift, which positive cases structurally cannot.
- **Every case verified by deliberate sabotage (AEE70).** The "Adding a case" procedure in `benchmarks/README.md` ends by requiring the author to break the detector and confirm the case fails, and states that every case in the suite was verified this way. That is AE17 implemented as process rather than as intention, and it is rare.
- **The harness has been debugged as a component in its own right (AEE74).** `docs/benchmarks/overview.md` records two bugs found during construction, both in the harness rather than in any detector. The first is the canonical vacuous-pass failure: `expected.yaml` fixture paths were resolved relative to `benchmarks/` instead of the case's own directory, so every true-positive case failed while every true-negative case passed *for the wrong reason*. The write-up names the asymmetric failure pattern as the diagnostic clue, which is exactly the right reading. The second — a mock provider whose canned responses paraphrased their own trigger words, so `must_mention` failed on a correct match — is a grader defect, not a system defect, and it is recorded as one.
- **The corpus is stated with every number (AEE72, AEE73).** Both the README and the runner's own printed output state that recall and precision are computed only over the curated `must_detect`/`must_not_detect` corpus, and that this is a regression guard rather than a claim about detection rates on arbitrary real code. The runner prints that caveat on the line directly below the figures, which is where it belongs — a caveat one file away from a number does not travel with it.
- **No baseline to drift, by construction (AE14, AEE55).** `benchmarks/README.md` states plainly that no `--update-baseline` flag exists because there is no stored baseline: every run recomputes recall and precision fresh against the manifest's cases. This sidesteps the single most damaging habit in this pack's anti-pattern list by removing the mechanism rather than by asking people to resist it. It also accepts a tradeoff, noted below.
- **Gaps are stated, not implied (AEE15, AEE71).** `PACK_EXPIRED` is the one rule in `rules/` with no benchmark case, and both the README and the overview say so, name the reason (fixturing "AKOS's own repo root" would need the harness to monkeypatch `AKOS_HOME`), and point at the unit test that covers it instead. The runner reports how many cases a `--domain` filter excluded rather than silently narrowing the denominator.
- **Weak grading is labeled weak (AE6).** The Level C path checks `must_mention` phrases against the provider's response by lowercase substring match. The README says outright that this is not a rigorous grading method and exists to prove the plumbing works end to end. Its results are also excluded from the recall/precision arithmetic, which is the correct call — pooling a substring match with a line-accurate detector match would produce one number meaning two different things.
- **Fixtures are synthetic (AEE8).** The case-authoring instructions require invented content and forbid real secrets or real project code, which matters for a suite whose own subject includes secret detection.
- **Reports are regenerated, not committed (AEE76).** `report.md` / `report.json` are gitignored, so nobody reads a stale artifact as current.

### What it does not do

Stated plainly, because overclaiming an eval suite is the failure this pack exists to prevent.

- **It evaluates a deterministic detector, not an agent.** This is the largest and most important qualification. `benchmarks/` measures whether the rules engine still finds what it used to find in a fixture. It does not measure any agent's behavior, and most of this pack's agent-specific dimensions do not currently apply to it. Reading it as "AKOS has agent evals" would be wrong; it has a rules-engine regression suite, which is a different and also valuable thing.
- **No trajectory evals (AEE14).** Nothing observes a path. There is no notion of steps taken, no assertion about route, no repeated-call detection — because the thing under test has no trajectory. The moment anything agentic enters the suite, this stops being a non-applicable row and becomes a real gap.
- **No LLM-as-judge (AEE17, AEE22).** The Level C path is substring matching, which is closer to an exact-match grader than to a judge, and the default provider is a deterministic offline mock. No grader in the suite has been calibrated against human labels, because no grader in the suite exercises judgment. Level C proves plumbing; it does not grade quality, and the README says as much.
- **No pairwise comparison (AEE26).** Nothing compares two versions' outputs against each other. Every case is an absolute must / must-not check.
- **No cost, latency, or tool-call metrics (AEE40–AEE45).** The runner records pass/fail and finding counts. It does not record tokens, wall-clock, or call counts, so a change that preserved detection while doubling runtime would pass unremarked. For a deterministic Python rules engine that is a low-stakes gap; for anything model-backed it would not be.
- **No groundedness or hallucination metric (AEE29–AEE34).** Not applicable to a pattern-matching detector, and genuinely applicable the moment a real Level C provider gates anything.
- **No task completion, recovery, or failure injection (AEE35, AEE46–AEE50).** There is no end-to-end task, so there is nothing to complete and nothing to recover from. No case injects a tool error, a permission failure, or an unresolvable dead end.
- **No numeric regression threshold and no trend (AEE51, AEE52).** Gating is per-case pass/fail with exit code 2 on any failure — a strict and defensible policy, stricter in fact than a percentage bar. But because nothing is stored between runs, recall and precision cannot be tracked over time. The design that removes baseline-drift risk also removes the ability to see slow degradation, and that is a real tradeoff rather than a free win. If Level C ever runs against a non-deterministic provider, per-case pass/fail at one run per case will stop being adequate and a stored trend will start being necessary.
- **No held-out set or contamination discipline (AEE7, AEE64–AEE69).** Every case is used for iteration; no portion is held out. Again this is close to vacuous for a deterministic detector — a regex cannot memorize — and becomes load-bearing the instant a model is in the loop.
- **Its Level A/B/C axis is not this pack's altitude axis.** The suite's levels classify *rules* by detection method (deterministic vs. LLM-assisted). This pack's altitudes classify *evals* by scope (unit / tool-call / trajectory / end-to-end). They are orthogonal, and the shared word "level" invites conflating them. In this pack's terms, all 21 cases sit at the unit altitude.
- **21 cases is a small corpus.** The suite says so about itself, repeatedly and without being asked, which is the honest handling. It remains small.

**The summary judgment:** `benchmarks/` demonstrates the procedural half of this pack unusually well — negative cases, sabotage verification, stated corpus, stated gaps, no baseline flag, weak graders labeled weak — and none of the agent-specific half, because it was never built for it. The right way to extend it is not to bolt a judge onto the existing cases, but to add a second suite at a different altitude with its own graders and its own honest statement of what it measures.

## The three-example proof (AE1, AE2) — invented

An engineer changes an agent's system prompt to be more explicit about citing sources, runs four of their own recent queries before and after, and reports that citations are "much better now." The change ships.

Three weeks later a support ticket surfaces the actual effect: the agent now cites a source for nearly every claim, including claims it inferred rather than retrieved, because the prompt rewarded citation presence rather than citation validity. On the four demo queries — all of which had good retrieval results — this was invisible, since a valid citation happened to be available for every claim.

After: the four queries become the first four cases in a suite, joined by sixteen drawn from logged production queries, six of which return little or no retrieval. Groundedness is scored separately from correctness (AE7), and the case class that matters most is added explicitly: queries whose answer is *absent* from the retrieved context, where the expected behavior is to say so. The prompt change is re-run against the suite. Correctness is flat; groundedness drops eleven points. The change is reverted and rewritten to reward *attributable* claims rather than cited ones.

The generalizable point: the demonstration was not insufficiently large. It was incapable of coming out against the change.

## All-green steps, failed task (AE8, AEE35–AEE38) — invented

A scheduling agent's dashboard shows tool-selection accuracy at 96%, argument validity at 98%, and per-step plausibility (judged) at 94%. Leadership reads this as a healthy system. Users report that it "usually doesn't actually book the meeting."

The tasks take nine to fourteen steps. At 95% per step, a twelve-step task completes about 54% of the time even with perfect independence — and the steps are not independent, since a wrong calendar lookup early makes every downstream step wrong-but-plausible, so each one still grades well individually.

After: one metric goes above all the others — *does a calendar event exist, with the right attendees, in the right slot, after the run*. Checked against the calendar API, never against the agent's closing message, which had been saying "I've booked that for you" in most of the failing runs (AEE38). Completion comes in at 61%. The step metrics stay on the dashboard, relabeled as diagnostics, and immediately earn their keep: broken down by failing case, they locate the problem in a single tool's timezone handling within a day.

## The convenient baseline (AE14, AEE54, AEE55) — invented

A team's eval harness has an `--update-baseline` flag, added early because the corpus was changing weekly and re-recording was genuinely necessary. The corpus stabilized months ago; the flag stayed.

A model version bump lands two days before a release. The suite goes red: completion drops from 78% to 74%. The engineer runs the suite again, gets 75%, concludes it is "mostly noise plus a slightly different model," runs `--update-baseline`, and ships. No decision is recorded, because from the outside nothing happened — a command ran and CI went green.

Four releases later someone asks why completion is 71% when the number "has always been around 78%." Reconstructing the history takes an afternoon and finds three separate quiet re-records, none malicious, each individually defensible, cumulatively a seven-point regression nobody ever agreed to.

After, three changes, all procedural rather than clever:

1. The flag is deleted (AEE55). Updating a baseline now requires editing a committed file, which requires a diff, which requires a reviewer.
2. The baseline file records version, corpus revision, grader version, and run count alongside the number (AEE53), so "is this comparison even valid" is answerable without archaeology.
3. The suite is run twice against the *same* version to establish a noise floor — ±1.5 points, which retroactively makes the original four-point drop clearly a real regression rather than noise (AEE52). The threshold is set at a maximum 2-point drop and committed before the next change (AEE51).

The rule this illustrates: the fix for a moving baseline is never "be more careful." It is removing the path of least resistance, because under deadline pressure the path of least resistance is what decides.

## The flaky case that ate the suite (AE12, AEE59–AEE63) — invented

A suite of forty cases has six that fail intermittently — a judge grading borderline outputs inconsistently, plus two cases hitting a live API with variable latency. Everyone knows which six. The habit that develops is rational at every step: red suite → check whether the failures are "the usual ones" → if yes, re-run → green → merge.

A genuine regression arrives inside a batch where four of the usual six also failed. It is re-run. It passes on the second run, because the regression only affected 40% of runs on that case. It ships.

After: the two live-API cases are pinned to recorded responses, removing avoidable non-determinism before any of it is blamed on the model (AEE62). Each case now runs five times and reports a pass rate rather than a boolean (AEE59), which converts three of the remaining four from "flaky" into "83% — below the 95% bar, therefore failing," a far more useful statement. The last one has a genuinely ambiguous rubric criterion; the criterion is given behavioral anchors and the case stabilizes. Per-case pass rate is tracked automatically, so flakiness gets flagged by the tracker rather than remembered by people who are generous to cases they wrote (AEE60).

The report now distinguishes three things it used to collapse into one: failed, flaky-and-known, and re-run-to-green (AEE63). The third turns out to be the category that had been doing the damage.

## Contamination via the agent's own memory (AE13, AEE64) — invented

A coding agent's eval suite includes a case: "find the cause of the intermittent failure in `test_orders.py`." It passed reliably for two months, then started failing after an unrelated refactor to how sessions initialize.

Nothing about the agent's diagnostic capability changed. What changed is that the agent had been reading a project memory file containing a note from an earlier debugging session — "the intermittent test failure traces to a stale fixture in `test_orders.py`" — and the case had been measuring its ability to read that note. The refactor stopped loading memory files during eval runs, and the case immediately revealed what it had actually been measuring all along.

After: eval cases run cold, with no memory files and no carried session state (AEE64). The case's pass rate falls from 100% to 45%, which is the real number and always was. A held-out set is established (AEE7) so the next instance is caught by divergence rather than by an accidental refactor two months later.

The uncomfortable part worth sitting with: the contamination made the suite report a capability the system did not have, for two months, with no signal of any kind. Contamination does not look like a failure. It looks like success.
