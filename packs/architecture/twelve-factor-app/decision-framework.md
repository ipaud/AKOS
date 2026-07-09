# Decision Framework — Twelve-Factor App Pack

## When the twelve factors fully apply

Any service deployed to a platform that restarts/scales/schedules processes automatically (containers, PaaS, serverless, k8s) benefits from all twelve factors essentially without exception — they're not optional style preferences in that context, they're what makes the platform's automation safe.

## When to relax a factor

- **Long-running stateful workers** (e.g. a video-encoding worker holding a large in-memory buffer) may hold transient in-process state during a single job — but must still be safely killable between jobs, and must not treat that state as durable.
- **Local scripts/one-off tools** with no deployment/scaling story don't need port binding or process-model concurrency — but config-from-environment (TF1) is still worth keeping, it's cheap and prevents credential leaks regardless of deployment target.
- **Monolithic legacy systems mid-migration** may not achieve full statelessness immediately — treat each factor as an incremental target, prioritizing config-externalization (TF1) and log-streaming (TF8) first since they're the cheapest, highest-leverage wins.

## Config strategy choice

Environment variables (TF1) are the baseline; for larger systems, a secrets manager (Vault, cloud provider secret store) injecting into the environment at deploy time is the natural evolution — the principle (config out of code, out of the repo) stays constant, the mechanism scales up.

## Dev/prod parity tradeoffs

Full parity (identical backing services, identical scale) is expensive for a small team; the pragmatic minimum is: same *type* of backing service (Postgres in dev, Postgres in prod — not SQLite in dev), and a short gap between commit and deploy (continuous deployment beats weekly release trains for parity purposes).
