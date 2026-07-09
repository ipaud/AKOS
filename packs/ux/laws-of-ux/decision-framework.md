# Decision Framework — Laws of UX Pack

## Which law applies? (symptom router)

| Observed symptom | First law to check | Then |
|------------------|--------------------|------|
| Hesitation/dwell at a step | Hick (too many/ambiguous options) | Miller (carrying context?), scent ([NN/g](../nielsen-norman-group/mental-models.md)) |
| Misclicks, slow target acquisition | Fitts (size/distance) | Slip analysis ([Norman](../don-norman/mental-models.md)) |
| "How do I…?" on standard objects | Jakob (convention broken) | Signifiers (Norman) |
| Users forget/retype earlier info | Miller | H6 recognition (NN/g) |
| Form abandonment | Tesler (complexity dumped on user) + Goal-Gradient (no visible progress) | Krug form rules |
| Flow completed but users rate it poorly | Peak-End (bad ending/peak) | — |
| Feature exists, nobody remembers it | Serial Position (buried middle) + Von Restorff (no isolation) | — |
| Everything highlighted, nothing found | Von Restorff (spent budget) | Squint test (Krug) |
| Great demo feedback, bad task metrics | Aesthetic-Usability (masking) | Behavioral testing |
| Drop-off near flow end | Goal-Gradient (distance not shrinking visibly) | — |

## Tradeoff rulings within the pack

- **Hick vs capability (expert tools):** cut *presentation*, not capability — progressive disclosure, command palettes, good defaults. Stripping expert options to "simplify" fails Tesler honestly.
- **Fitts vs safety:** frequency dictates size/proximity *except* for destructive actions, where safety inverts the rule deliberately.
- **Jakob vs differentiation:** convention for the chrome, novelty for the core value. If the differentiator *is* an interaction pattern, budget onboarding + test it.
- **Peak-End vs the middle:** peaks/ends get disproportionate polish only after the middle clears the usability floor — sampling bias doesn't excuse a broken step 3.
- **Von Restorff budget allocation:** primary action gets the accent by default; a status/danger element may take it per-screen, in which case the primary falls back to size/position dominance.

## Evidence upgrade path

Laws are priors, not verdicts. When a law-based finding is contested:
1. Cheap check: analytics (dwell, drop-off, misclick heatmap) against the law's prediction.
2. Cheaper still: 3-user think-aloud on the disputed step ([Krug fragment](../steve-krug/prompt-fragments.md)).
3. The law loses gracefully: if measured behavior contradicts the prior, the measurement wins ([confidence model](../../../core/confidence-model.md)).
