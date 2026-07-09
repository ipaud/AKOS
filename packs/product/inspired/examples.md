# Examples — Inspired Pack

## Outcome statement vs. feature description

Bad: "Ship a redesigned onboarding flow."
Good: "Reduce day-1 onboarding drop-off from 42% to under 25%, by [target date]." The redesign is one candidate solution, not the goal itself.

## Four-risk discovery note (compact)

```
Idea: Let teams invite guests without a full account
- Value: 12 customer interviews, 9/12 said this blocks their trial → real pain
- Usability: clickable prototype tested with 5 users, 4/5 completed invite flow unaided
- Feasibility: eng spike (2 days) confirmed auth model supports scoped guest tokens
- Viability: legal confirmed guest data retention policy needs a 1-line ToS update
Decision: proceed to build, ToS update tracked as a dependency.
```

## Cheapest experiment first

Idea: "will customers pay for a premium analytics tier?" Instead of building it: a landing page describing the tier with a "Notify me" button, driven to existing customers via email — conversion rate measured before writing analytics code.

## Feature-factory backlog vs. outcome-driven backlog

Feature factory: `[ ] Add dark mode  [ ] Add CSV export  [ ] Redesign settings page]` — no stated why.
Outcome-driven: `Reduce support tickets about "can't find X" by 30% — candidate solutions: search redesign, settings reorg, in-app help. Discovery in progress.`

## Killing an idea (success case)

A proposed "AI writing assistant" feature: value-risk test (5 customer interviews + a Wizard-of-Oz prototype) shows users don't trust AI-generated text for this use case and prefer templates. Idea killed before any engineering work — discovery did its job.
