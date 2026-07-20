# Review-output evals

`benchmarks/` measures the deterministic rules engine. This measures the part that actually produces AKOS's output: **the review**.

Until this existed, nothing did. `packs/ai-engineering/agent-evals` scored that dimension at roughly 18/100 and was right to: AKOS assigned reviews a 0–100 score with no check that the score meant the same thing twice, and no way to tell whether a change to a pack, an agent file, or a skill made reviews better or worse.

## What it does

Each case is a small fixture — real code shapes, copied from repositories that were reviewed by hand — plus an `expected.yaml` naming:

- **`must_find`** — findings a competent review has to surface. Each was confirmed by reading the fixture, not assumed.
- **`must_not_find`** — findings a careless review wrongly reports. These are the traps, and they matter more than the `must_find` entries, because every one of them is a false positive that really happened.

```bash
akos eval --report path/to/review.md --case optional-auth
akos eval --report path/to/review.md --case optional-auth --format json
```

`--case` is **required**, not a filter. A report can only be graded against
the case whose fixture it actually reviewed. Grading it against the others
produces both halves of a wrong answer, and this was observed rather than
predicted: a real review of one project scored 0% recall against another
project's case — "missing" findings that describe a different codebase — and
tripped a trap because it happened to use the words.

Exit `0` every case met the threshold · `1` usage error · `2` at least one case below it.

## What it deliberately does not do

**It does not run a review.** It grades a report someone else produced — by an agent, by hand, or replayed out of a project's `.akos/reviews/`. Generating the review inside the grader would make the suite depend on a provider and on run-to-run variance, and there is no honest way to gate CI on that. Grading is deterministic; producing is not.

**It says nothing about a project that is not this case's fixture.** Three cases is a small corpus. A passing run means "did not regress on one known artifact", and that is the entire claim.

**It cannot tell reporting a finding from explaining why something is *not* a finding.** Both put the same words in the report. A review that correctly refutes a trap reads identically to one that falls for it — observed on a real report that discussed a false positive in order to dismiss it, and was marked as having committed it. Separating the two needs a judge, which needs its own calibration.

**It does not grade wording, structure, tone, or score accuracy.** Two reports can read completely differently and both pass. Matching is concept-based: a finding counts when every `match_all` term appears and at least one `match_any` term does, case-insensitive with whitespace collapsed. Exact-match grading on prose measures phrasing, not correctness.

**Extra findings are neither rewarded nor punished.** Only the listed traps count against a report. A review that finds something real and unlisted is not penalised — and is also not credited, because nobody has verified it.

## Threshold

Stated in `runners/grade.py` as constants, before any run:

```
REQUIRED_RECALL      = 1.0   # every must_find, no partial credit
MAX_FALSE_POSITIVES  = 0
```

Recall is all-or-nothing on purpose. Each `must_find` is a defect a hand-verified read confirmed is really in the fixture; a review that misses one is not "mostly right", it missed a real defect on a artifact where the answer is known.

**Never lower a threshold to make a run pass.** If a case is wrong, fix or delete the case and say why in the commit. A baseline moved to accommodate a regression stops being a baseline — see `packs/ai-engineering/agent-evals` (AE14, AEE55).

## Why this is not in CI

CI has no review reports to grade. A step that iterates the cases and finds
nothing to work on would report green while doing nothing — the same vacuous
pass that two Level C benchmark cases shipped with, and that this suite's own
`test_every_case_can_fail` exists to prevent.

What *is* in CI is `tests/unit/test_evals.py`, which covers the part CI can
honestly check: that the grader discriminates, that every case fails on an
empty report, and that a report naming the traps is caught. The suite itself
runs on demand, when you have a review to grade:

```bash
akos-review the fixture, then:
akos eval --report .akos/reviews/<id>/report.md --case <case-id>
```

## Adding a case

1. Find a real finding — or a real false positive — in an actual repository. **Do not invent one.** Every case here traces to a review run on a real project, and that is what keeps the corpus from only containing failure modes its author already had in mind.
2. Reduce it to the smallest fixture that still exhibits the shape.
3. Write `expected.yaml`. Two traps to avoid, both hit while building this suite:
   - **Generic terms.** A bare `notes` matched a `## Notes` heading in a report that never mentioned the table — the same generic-term bug the detectors had.
   - **Trap terms a correct report would use.** A `must_not_find` keyed on `shellcheck` + `cannot fail` fired on a report that correctly said the *other* step cannot fail and that shellcheck was fine. Matching is now proximity-bounded, which helps, but proximity cannot rescue a trap worded in phrases a right answer reaches for. Write traps in words only a wrong answer would use.

     This rule was written down and then violated in the very next case added: `a11y-wrapper-label`'s trap used `no accessible name`, which a correct report uses about a *different* input two paragraphs up, well inside the window. Rewritten to phrasings that assert the specific claim (`field has no label`, `both inputs are unlabelled`). Expect to get this wrong; test both directions and it surfaces immediately.
   - **Multi-line flow lists.** The YAML subset parser takes `[a, b, c]` on one line only. A wrapped list raises `malformed flow list`.
4. **Verify the case can fail.** Grade a report that omits the finding and confirm it goes red. A case that cannot fail is not a test — two Level C benchmark cases shipped in exactly that state.

## Known gaps, stated rather than left to be discovered

- **Ten cases across eight lenses** (security ×3, testing, release, accessibility, architecture, mobile, copy, frontend). Four lenses have no coverage: product, UX, performance, database. A green run says nothing about those.
- **No held-out set.** The cases were written by the same process that fixed the detectors they exercise. That is the contamination `agent-evals` warns about; it is bounded here because the fixtures come from real code the author did not write, but it is not eliminated.
- **No variance measurement, and it cannot be produced from inside a single session.** Measuring how far apart two reviews of the same fixture land requires the second one not to be informed by the first. An agent reviewing a fixture it reviewed an hour ago is not producing an independent sample, and a number derived that way would be contaminated in the flattering direction. This needs two separate sessions, or two different reviewers, and until then `core/scoring-model.md`'s "a 75 that means the same thing next month" stays an aspiration rather than a measured property. Stated here rather than satisfied with a number that looks like evidence.
- **Recall is measured; precision is not.** A report that lists thirty findings, one of which is correct, passes. Grading unlisted findings needs a judge, which needs its own calibration.
