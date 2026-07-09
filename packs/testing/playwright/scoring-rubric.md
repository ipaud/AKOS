# Scoring Rubric — Playwright Pack

| Finding | Deduction |
|---------|-----------|
| Fixed sleep/waitForTimeout causing flakiness | −10 (HIGH) |
| Brittle CSS/XPath selectors throughout | −6 (MEDIUM) |
| Shared mutable state across tests | −10 (HIGH) |
| No trace/video capture on CI failure | −4 (MEDIUM) |
| Retry-until-green masking real flakiness | −6 (MEDIUM) |
| E2E suite covering excessive non-critical permutations | −2 (LOW) |

Anchors: 90 stable, resilient selectors, isolated tests · 75 solid with occasional flake · 60 frequent flakiness, brittle selectors · <50 unreliable suite, routinely ignored failures.
