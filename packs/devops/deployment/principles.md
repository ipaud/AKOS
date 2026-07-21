# Principles — Deployment Pack

- **DPL1** — Deployments to production use a progressive rollout strategy (canary or rolling) proportional to risk, not a single instant full-traffic cutover for significant changes.
- **DPL2** — Database schema changes are backward-compatible with the previous application version during rollout (expand-contract pattern), so a mid-deploy state never breaks.
- **DPL3** — Rollback is tested and fast — a previous release can be restored in minutes, verified periodically, not assumed to work.
- **DPL4** — Deployment includes automated post-deploy health verification (smoke tests, key metric checks) before considering the release complete.
- **DPL5** — Data migrations are reversible or have a documented, tested reversal plan before running against production.
- **DPL6** — High-risk deployments (schema changes, infra changes, major feature launches) have a communicated deployment window and an assigned owner monitoring through stabilization.
