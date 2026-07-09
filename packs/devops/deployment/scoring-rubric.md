# Scoring Rubric — Deployment Pack

| Finding | Deduction |
|---------|-----------|
| Breaking migration risked mid-rollout (no expand-contract) | −20 (CRITICAL) |
| No progressive rollout for a significant production change | −10 (HIGH) |
| Untested rollback mechanism | −10 (HIGH) |
| No post-deploy smoke verification | −6 (MEDIUM) |
| Irreversible data migration with no documented reason | −6 (MEDIUM) |
| High-risk deploy shipped with no active monitoring | −4 (MEDIUM) |

Anchors: 90 progressive rollout, tested rollback, expand-contract discipline · 75 solid with a gap · 60 instant cutovers common, rollback unverified · <50 breaking migrations risked, no verification at all.
