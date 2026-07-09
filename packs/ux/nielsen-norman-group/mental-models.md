# Mental Models — NN/g Pack

## The five usability attributes

Usability decomposes into: **learnability** (first-use success), **efficiency** (expert throughput), **memorability** (return-after-absence success), **errors** (rate + recoverability), **satisfaction** (subjective). Products weight these differently: a kiosk is all learnability; a pro tool is efficiency + memorability. Declare the weighting before judging.

## Heuristic evaluation as instrument

A small set of evaluators independently inspects the UI against the heuristics, then findings merge. Independence matters (evaluators anchor each other); multiplicity matters (each finds different problems); 3–5 evaluators hit diminishing returns. Solo AKOS adaptation: one agent runs the ten heuristics as separate passes rather than one blended read.

## Severity ratings

Rate each finding on frequency (rare ↔ common), impact (nuisance ↔ task failure), persistence (once ↔ every time). NN/g's 0–4 scale maps to AKOS severities: 4 catastrophe → CRITICAL, 3 major → HIGH, 2 minor → MEDIUM, 1 cosmetic → LOW, 0 not-a-problem → drop.

## Five users find most problems

Iterative testing with ~5 users per round exposes the large majority of discoverable problems in that design state; further users mostly re-find. Corollary: many small rounds across iterations beat one big study. (Same engine as Krug's testing habit.)

## Jakob's Law

Users' expectations are set by the aggregate of everything else they use. Your innovation budget is limited; spend it on your differentiator, not on reinventing list views. Quantified relatives live in [laws-of-ux](../laws-of-ux/mental-models.md).

## Information foraging & scent

Users follow "scent" — cues (link labels, headings, icons) predicting where the goal is. Strong scent → confident deep navigation; weak scent → pogo-sticking (click, back, click, back). Pogo-sticking observed in analytics/testing = scent failure, fix labels first (cf. [Krug](../steve-krug/heuristics.md) on depth-vs-breadth).

## Progressive disclosure

Show the core by default; reveal the advanced on request. Keeps H8 (minimalism) and H7 (power) from fighting. The disclosure control itself must be discoverable (H6) — hiding *everything* behind "Advanced" just relocates the problem.

## The evaluator effect

Different evaluators find different problems from the same session — inspection is sampling, not measurement. Practical: never treat one review pass (or one agent) as exhaustive; the checklist bounds the floor, not the ceiling.
