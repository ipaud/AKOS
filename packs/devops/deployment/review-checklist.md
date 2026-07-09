# Review Checklist — Deployment Pack

## High
- [ ] Progressive rollout (canary/rolling) used for non-trivial changes. (DP-E1)
- [ ] Schema migrations follow expand-contract, no breaking mid-rollout state. (DP-E2)
- [ ] Rollback tested periodically, not assumed. (DP-E3)

## Medium
- [ ] Post-deploy smoke tests verify critical paths. (DP-E4)
- [ ] Data migrations have a tested/documented reversal path. (DP-E5)

## Low
- [ ] High-risk deploys scheduled with an owner actively monitoring. (DP-E6)
