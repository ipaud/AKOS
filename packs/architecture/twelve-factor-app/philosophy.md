# Philosophy — Twelve-Factor App Pack

## Portability and disposability as first-class design goals

Software-as-a-service apps live in an environment where they'll be run by an automated platform, scaled horizontally, restarted frequently, and deployed across dev/staging/production with different backing services. The twelve factors are the concrete engineering practices that make an app *survive* that environment gracefully instead of fighting it: no assumptions about a stable long-running process, no config baked into code, no reliance on local disk state.

## Config is not code

The methodology's most consequential single rule: configuration that varies between deployments (database URLs, API keys, feature flags) lives in the environment, not in the codebase. This isn't a security nicety — it's what makes the same build artifact deployable to dev, staging, and production without modification, which is itself what makes builds trustworthy and rollbacks safe.

## Processes are stateless and disposable

Treat every running process as replaceable at any moment — the platform may kill and restart it for scaling, deployment, or failure recovery. Any state that must survive belongs in a backing service (database, cache, object store), never in process memory or local disk. This single discipline is what makes horizontal scaling, rolling deploys, and crash recovery boring instead of terrifying.

## Dev/prod parity closes the "works on my machine" gap

Divergence between development and production environments — different backing services, different deploy processes, different time lags between writing code and running it in production — is where entire classes of bugs hide until the worst possible moment. The factors push toward keeping environments as similar as possible and shrinking the gap between commit and deploy.
