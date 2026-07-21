# Review Checklist — Deployment Pack

## High
- [ ] Progressive rollout (canary/rolling) used for non-trivial changes. (DPL-E1)
- [ ] Schema migrations follow expand-contract, no breaking mid-rollout state. (DPL-E2)
- [ ] Rollback tested periodically, not assumed. (DPL-E3)

## Medium
- [ ] Post-deploy smoke tests verify critical paths. (DPL-E4)
- [ ] Data migrations have a tested/documented reversal path. (DPL-E5)

## Low
- [ ] High-risk deploys scheduled with an owner actively monitoring. (DPL-E6)
