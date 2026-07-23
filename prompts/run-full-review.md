# Prompt: Run Full Review

Paste to run the complete twelve-step pipeline.

---

Load AKOS (see `~/DEV/AKOS/prompts/load-akos.md`) and run the full pre-release review pipeline (`~/DEV/AKOS/workflows/pre-release-review.md`) on [describe the target: feature / screen / release].

Run these twelve steps in order, each using its agent definition in `~/DEV/AKOS/agents/`, at the strictness dictated by the active reasoning profile's weight table:

1. Product clarity 2. UX clarity 3. Accessibility 4. Mobile/responsive 5. Copywriting 6. Frontend quality 7. Architecture 8. Security 9. Performance 10. Testing 11. Personal rules 12. Release readiness

Produce ONE aggregate Review Summary in the standard format:

```
# Review Summary
## Context
## Strengths
## Critical Issues
## High Priority Fixes
## Medium Priority Fixes
## Low Priority Improvements
## Tradeoffs
## Relevant Knowledge Packs Used
## Coverage
## Scores (UX / Accessibility / Mobile / Architecture / Security / Performance / Product / Maintainability / Overall)
## Recommended Next Iteration
## Final Decision — PASS / PASS WITH FIXES / BLOCKED
```

Before the security and other deterministic-detector lenses, run the executable
checks rather than grepping by hand: `akos rules run <project-dir>`. A detector
exists for secrets, RLS, permissive policies, service-role-in-client,
destructive migrations, and unlabelled inputs — a lens told to find those by eye
when a check exists is the reliability defect this step removes.

Final decision = the worst individual step's decision. Any open CRITICAL → BLOCKED. Skip steps the profile sets to weight 0, noting them as skipped-by-profile; steps 2, 3, 8 never drop below weight 1.
