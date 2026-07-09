# Scoring Rubric — CI/CD Pack

| Finding | Deduction |
|---------|-----------|
| Secrets committed in pipeline config | −25 (CRITICAL — also security) |
| No branch protection gating merges on pipeline pass | −15 (HIGH) |
| Manual/undocumented production deploy process | −10 (HIGH) |
| No tested rollback mechanism | −10 (HIGH) |
| Pipeline stages poorly ordered (slow stages before fast ones) | −4 (MEDIUM) |
| Excessive pipeline runtime with no caching | −4 (MEDIUM) |

Anchors: 90 fully automated, fast, gated, tested rollback · 75 solid with a gap · 60 manual deploy steps or slow ungated pipeline · <50 no real CI/CD discipline, secrets exposed.
