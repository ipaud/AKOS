# Mental Models — CI/CD Pack

- **Fail fast, fail cheap:** order pipeline stages from cheapest/fastest to most expensive/slowest (lint → unit tests → build → integration tests → E2E → deploy) so failures are caught before expensive stages run.
- **Main is always releasable:** the continuous-integration invariant that makes "ship now" always a safe answer.
- **Pipeline as the single source of truth for "ready":** if it passes the pipeline, it's deployable — no separate manual "is this actually ready" gate duplicating what automation should verify.
- **Deployment vs release as separable concepts:** deploying code to production infrastructure and releasing it to users (via feature flags) can be decoupled — deploy continuously, release deliberately.
