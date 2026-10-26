# Measure first-review activation

**Owner:** AKOS maintainer  
**Review date:** 26 October 2026

AKOS must help a solo developer complete an evidence-backed review in their
existing agent, without hidden telemetry or a facilitator repairing the setup.

## Primary job

As a solo developer using Codex or Claude Code, I need to review a real
repository or frontend flow against a stable standard so that I know what to
fix before I ship.

“Read some packs” is not the job. Activation requires one complete Review
Summary with evidence, severity-ranked findings, scores only where evidence
supports them, and a final decision.

## Baseline

The baseline is not yet measured. Do not convert the targets below into a claim
that onboarding already works. The first five-user study establishes the
baseline and records the observed failure points.

## Success threshold

Run the study with 5 solo developers who already use Codex or Claude Code —
the segment this study recruits from, and why, is decided in
[first-adopter-segment.md](first-adopter-segment.md):

- At least 4 of 5 complete a review without maintainer intervention.
- Median time from starting the install path to receiving the first complete
  Review Summary is 10 minutes or less.
- Every completed report cites inspected evidence and labels uninspected
  surfaces; a fast but fabricated report does not count.

## Study task

1. Give the participant the README and a repository they are allowed to review.
2. Let them choose the global-clone or plugin path without coaching.
3. Ask them to run either the full frontend/UI review or the full twelve-lens
   review, whichever matches the repository.
4. Start the timer when they receive the README. Stop when one complete Review
   Summary appears; stop the session at 30 minutes if they are still blocked.
5. Do not explain steps or repair setup. If they ask for help, answer with
   “What would you try next?” and record whether they recover without a hint.
6. Ask what blocked or confused them, then inspect the report against the
   completion criteria.

## Completion check

Count a session as complete only when report includes:

- Evidence locations and concrete failure modes for findings.
- Severity-ranked findings, with confidence grounded in inspected evidence.
- Coverage that names inspected and uninspected surfaces; no invented runtime
  checks.
- Scores only for dimensions the report supports, plus final decision.

A report that appears within 10 minutes but fails this check does not count as
completed. Record first blocker using one of these steps: `README/install`,
`agent restart`, `skill activation`, `target/profile setup`, `review run`,
`report completion`, or `report evidence`.

## Evidence without telemetry

Collect this baseline without telemetry:

- The facilitator records start/end times in a study note.
- The participant voluntarily shares the generated Review Summary and the
  command or prompt they used.
- The facilitator records install path, agent, completion, elapsed time and
  the first blocking step.
- Inspect repository evidence locally with participant permission; do not copy
  or retain repository files. If participant declines to share report, record
  completion as unverified.
- AKOS does not phone home, add analytics, read unrelated agent history or
  upload repository content.

Store only aggregate results in this document after the study. Keep raw notes
outside the repository if they identify a participant or contain project
content.

Use participant numbers only (`P1`–`P5`) in the result table. For each session,
record exact minutes, completion, blocker step, and whether report passed the
completion check. Do not put names, repository names, report text, or source
code in this file.

## Result table

Leave the observations blank until a real session happens.

| Participant | Agent | Install path | Completed | Minutes | First blocker |
|---|---|---|---|---:|---|
| 1 | — | — | — | — | — |
| 2 | — | — | — | — | — |
| 3 | — | — | — | — | — |
| 4 | — | — | — | — | — |
| 5 | — | — | — | — | — |
