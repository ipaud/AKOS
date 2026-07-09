# Mental Models — Twelve-Factor App Pack

## Build, release, run

Three strictly separated stages: **build** (code → executable bundle, dependencies resolved), **release** (build + config → a specific, immutable, versioned release), **run** (release executed in the target environment). Config injected only at release time; a release is never mutated in place — a config change creates a new release. This separation is what makes rollback a simple "run the previous release," not a redeploy.

## Processes as cattle, not pets

A process is disposable: it can be started, killed, or restarted at any moment with no ceremony and no data loss, because nothing important lives only in it. This mental model directly enables horizontal scaling (add more identical processes) and resilient operations (crashed process → platform just restarts it).

## The environment, not the codebase, varies

The same build artifact runs unmodified across dev/staging/production; everything that differs between them (URLs, credentials, feature flags, resource limits) is environment configuration, injected at runtime, never baked into the artifact at build time.

## Backing services as attached resources

Databases, queues, caches, and third-party APIs are all "attached resources" accessed via a URL/credential in config — swappable without code changes (a local Postgres and a managed Postgres are interchangeable to the app; only the config differs).

## Logs as event streams, not files

An app never manages its own log file rotation or storage location — it writes a stream of events to stdout, and the execution environment captures, aggregates, and routes it. This keeps the app agnostic to logging infrastructure choices made independently by ops.
