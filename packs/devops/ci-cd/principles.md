# Principles — CI/CD Pack

- **CD1** — Pipeline stages are ordered cheapest/fastest first (lint, typecheck, unit tests) before expensive/slow stages (build, E2E, deploy).
- **CD2** — A red pipeline blocks merge; main only ever contains commits that passed the full gate.
- **CD3** — Pipeline runtime is actively budgeted and optimized (parallelization, caching); a slow pipeline invites bypass under deadline pressure.
- **CD4** — Deployment is automated end-to-end from a passing pipeline — no manual deploy steps that can drift from what was tested.
- **CD5** — Deploys are decoupled from releases where feature flags are available: ship code continuously, expose it to users deliberately.
- **CD6** — Rollback is automated and fast (previous release re-deployable in minutes), not a manual multi-step recovery procedure improvised during an incident.
- **CD7** — Secrets used in CI (deploy keys, API tokens) are stored in the CI platform's secret manager, never in pipeline config files.
