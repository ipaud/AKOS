# Engineering Rules — Deployment Pack

- DP-E1. Production deploys use canary or rolling rollout for any change beyond a trivial fix (config tweak, copy change).
- DP-E2. Schema migrations follow expand-contract: additive changes deployed and backfilled before any destructive/breaking change is deployed separately.
- DP-E3. Rollback is a single automated action, tested at least quarterly outside of a real incident.
- DP-E4. Post-deploy automated smoke tests verify critical paths before a release is marked successful.
- DP-E5. Data migrations have a tested reversal path or an explicit documented reason none exists (e.g. genuinely one-way anonymization).
- DP-E6. High-risk deploys are scheduled with an assigned owner monitoring through stabilization, not fire-and-forget.
