# Heuristics — Deployment Pack

- A schema migration that both adds a new column and requires the old one removed in the same deploy → split into expand (add new, deploy, backfill) then contract (remove old, deploy) phases.
- No smoke test runs automatically after deploy → add one checking the top 2-3 critical endpoints before calling the release "done."
- Rollback procedure last tested "a while ago" → test it again before it's needed under pressure.
- A risky deploy going out at 5pm Friday with no one watching → reschedule or ensure an owner is actively monitoring through stabilization.
- 100% traffic cutover for a significant behavior change → consider canary/rolling instead, even if it adds a few minutes to the rollout.
