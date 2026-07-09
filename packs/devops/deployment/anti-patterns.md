# Anti-Patterns — Deployment Pack

- **Big-bang cutover** — 100% instant traffic switch for a significant change, no canary, all-or-nothing risk.
- **Breaking migration in one deploy** — adding a NOT NULL column and removing the old one simultaneously, guaranteed to break if the deploy is even briefly mid-rollout with mixed application versions.
- **Untested rollback** — a rollback procedure that's never actually been run, discovered broken during a real incident when it's needed most.
- **Friday-evening risky deploy** — a major schema/infra change shipped right before everyone leaves for the weekend, no one watching when it breaks.
- **No post-deploy verification** — deploying and immediately moving on, discovering the release broke something only when a user reports it hours later.
