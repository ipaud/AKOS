# Pack: Coding Agents — The Discipline of the Edit

**Domain:** AI Engineering · **Authority:** Level 2 (industry authority — agent-computer interface research, grounded in this repository's own engineering record) · **Version:** 1.0.0

Operationalizes what an agent must actually do when it reads and modifies a real repository. The governing idea: **plausible is not correct.** A system that writes code by predicting what code should look like produces well-formed output whether or not it is right, which destroys the single cheapest error-detection signal software engineering ever had — the visible hesitation of a person who does not know. Nothing replaces that signal except execution. A coding task is therefore done only when a command has been run against the changed artifact and its real output and exit code have been read; a description of what should happen is a hypothesis, and an unchecked success claim is not a shortcut but a defect in the highest-leverage part of the deliverable.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the original — read it; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Any task where an agent will edit files in a real repository, rather than produce standalone code.
- Reviewing a change an agent made: the diff, the commits, the pull request, or the completion claim attached to it.
- A change that "should work" turned out not to, or a report claimed a state that was never verified.
- Before renaming, re-signaturing, or removing anything with more than one consumer.
- Writing or reviewing a bug fix, and deciding what evidence would demonstrate that it fixes anything.
- Deciding how to respond to a failing CI check or a review comment — and whether the response is fixing or silencing.
- Auditing a verification setup for checks that pass because they cannot fail.
- Designing a migration for a shared interface, a schema, a config key, or a persisted format.
- Setting the standard for what a commit, a commit message, and a PR description must contain.

## Scope boundary

This pack is the **process discipline of the edit itself** — how an agent orients, changes, verifies, and reports on a modification to a repository it does not own. It is deliberately narrow. What shape the surrounding system should be, and how it is bounded — termination conditions, budgets, error classification, escalation, idempotency — is [agent-foundations](../agent-foundations/README.md), which explicitly defers repository-editing discipline to this pack. What the agent can *see* while it works — retrieval timing, progressive disclosure, memory tiers, navigating a large repository instead of loading it — is [context-engineering](../context-engineering/README.md). Whether the design being implemented is any good is architecture, and lives in [packs/architecture](../../architecture/); what a codebase's test strategy should be is [packs/testing](../../testing/). This pack does not decide any of those; it decides whether the change that implements them was actually made and actually verified. And it lowers no safety floor: an edit satisfying every rule here can still introduce a vulnerability, break accessibility, or corrupt data, and a green test run is not a substitute for the reviews that catch those.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Why fluency destroys the uncertainty signal; the report as part of the artifact; the failing check as the cheapest form of the problem |
| [mental-models.md](mental-models.md) | The evidence ladder, the vacuous pass, the exit-code chain, the first-match trap, blast radius, the revert test, the claim ledger, green-as-goal vs. green-as-signal |
| [principles.md](principles.md) | CA1–CA18: always-true rules of the edit, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per phase — orientation, search, reading, conventions, scope, testing, evidence, migration, commits, review response |
| [engineering-rules.md](engineering-rules.md) | CAE1–CAE80: checkable in a diff, a commit history, a PR, a transcript, or a CI log |
| [decision-framework.md](decision-framework.md) | Is this done; edit or migration; rewrite or targeted edit; which convention wins; in this diff or not; fix the code or fix the test; how much verification this change needs |
| [anti-patterns.md](anti-patterns.md) | The plausible completion, the vacuous pass, the pipe-swallowed exit code, the first-match fix, the blind overwrite, the invented API, the suppressed check, the stale green |
| [review-checklist.md](review-checklist.md) | Binary pass/fail process review, severity-ordered, transcript-aware |
| [examples.md](examples.md) | Invented before → after cases, plus a real in-repo case study: AKOS's own v1.4.0 work and the eight bugs found only by executing |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents, plus an orientation worksheet and a verification trace |
| [scoring-rubric.md](scoring-rubric.md) | Edit-discipline scoring, 0–100, with a false record graded as a correctness defect |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Plausible is not correct — a coding task is done only when a command has been executed against the changed artifact and its real output and exit code have been read, and an unchecked success claim is itself a defect rather than a shortcut.

## Related packs

[agent-foundations](../agent-foundations/README.md) · [context-engineering](../context-engineering/README.md) · [tdd](../../testing/tdd/README.md) · [git](../../devops/git/README.md) · [martin-fowler-refactoring](../../architecture/martin-fowler-refactoring/README.md)
