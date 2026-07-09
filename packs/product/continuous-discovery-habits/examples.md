# Examples — Continuous Discovery Habits Pack

## Story-based question vs. opinion question

Bad: "Would you use a feature that automatically categorizes your expenses?"
Good: "Tell me about the last time you had to categorize expenses — walk me through exactly what you did, step by step." Follow-ups drill into specific friction moments mentioned.

## Opportunity solution tree (compact)

```
Outcome: increase week-4 retention from 30% to 45%

Opportunity A: "I forget to log back in after the trial ends"
  Solution A1: re-engagement email sequence
  Solution A2: in-app reminder banner during trial
Opportunity B: "I can't tell if the tool is saving me time"
  Solution B1: weekly summary email showing time saved
  Solution B2: in-app dashboard widget
```

Two opportunities, two solutions each — visible exploration before any commitment.

## Assumption map (compact)

```
Solution: in-app dashboard widget showing "time saved"
- Desirability: will users care about this metric? [important, low evidence] ← TEST FIRST
- Usability: will they understand what "time saved" means without explanation? [important, medium evidence]
- Feasibility: can we compute "time saved" accurately from existing data? [important, high evidence — already prototyped]
- Viability: none identified (no cost/legal/business concern)
```

Test first: desirability — cheapest test is a static mockup shown in 5 interviews this week, asking "what does this number mean to you, and would it change what you do?"

## Weekly cadence in practice

Every Tuesday, 30 minutes: one customer interview (rotating who conducts it among PM/design/eng), findings added to the tree same day, 10-minute team sync Wednesday to discuss any new pattern. Sustained for 6 months = ~25 interviews, several strong patterns emerged that a single big study would have missed (seasonal usage shifts, a workaround habit only 3 unrelated customers mentioned but all in the same words).

## Fixing a solution-first tree

Before (single branch): `Outcome → "Build AI assistant" → [already building]`.
After team pushback: `Outcome → Opportunity: "hard to find the right report" → Solutions: (a) AI assistant, (b) better search, (c) saved-report templates` — AI assistant remains a candidate, now compared honestly against two cheaper alternatives.
