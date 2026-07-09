# Prompt Fragments — Deployment Pack

```text
Apply safe deployment practice (AKOS L2): use progressive rollout
(canary/rolling) for non-trivial changes, not instant full cutover;
schema migrations follow expand-contract (additive first, destructive
only after confirming zero remaining reads); rollback is a single
tested automated action; post-deploy smoke tests verify critical paths
before calling a release complete; high-risk deploys scheduled with
active monitoring, not fire-and-forget.
```
