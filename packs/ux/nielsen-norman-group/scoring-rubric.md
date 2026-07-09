# Scoring Rubric — NN/g Pack

Feeds [scoring/ux-score.md](../../../scoring/ux-score.md). Score per heuristic, then aggregate.

## Per-heuristic scoring

Each of H1–H10 starts at 10 points. Deduct per finding: CRITICAL −10 (zeroes the heuristic), HIGH −5, MEDIUM −2, LOW −0.5 (floor 0). Sum of the ten heuristics = the 0–100 pack score.

This structure localizes weakness: a report saying "H3: 2/10, everything else ≥8" is a diagnosis, not just a grade.

## Standard modifiers

- Roach motel present anywhere: total capped at 59 (Blocked band) regardless of other heuristics.
- Systematic pattern (same violation ≥4 places): count once at one severity higher, note the systemic fix (token/component), not 4 findings.
- Heuristic not applicable to the surface (e.g. H10 for a single-button utility): score it 10 and mark n/a — don't punish absence of need.

## Anchors

- **93** — a heuristic evaluation finds only polish; all ten ≥ 8.
- **82** — two or three heuristics with HIGH findings, cluster diagnosed, fixes sized.
- **74** — one heuristic near-zeroed (commonly H1 or H9 in MVPs) with the rest sound; shippable pre-PMF with the cluster scheduled.
- **58** — multiple zeroed heuristics or any roach motel; BLOCKED.
