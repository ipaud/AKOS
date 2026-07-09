# Anti-Patterns — Twelve-Factor App Pack

## Committed secrets

`.env` file with real production credentials committed to git "just for now." Fix: TF1 — secrets never in source control, ever, even temporarily.

## Snowflake environments

Dev uses SQLite, staging uses an old Postgres version, production uses a managed cloud Postgres with different extensions enabled — bugs appear only in production. Fix: TF7 — same backing service type everywhere.

## In-memory session state

Web app storing user sessions in process memory; horizontal scaling breaks (user's second request hits a different process with no session) and every deploy logs everyone out. Fix: TF3 — sessions in a shared backing store (Redis, DB).

## Snowflake deploy scripts

Migrations run via a developer's laptop with manually-exported environment variables, different from what the deployed app uses. Fix: TF9 — admin tasks run identically to the app itself.

## Self-managed logging

App writing to local log files with custom rotation logic, breaking when the container filesystem is ephemeral (logs vanish on restart). Fix: TF8 — stdout streaming, let the platform handle storage.

## Mutable releases

"Hotfixing" a running production release by editing files in place via SSH instead of building and deploying a new release. Fix: TF10 — releases are immutable; every change is a new release.

## God process holding everything

A single process handling web requests, background jobs, and scheduled tasks, scaled by giving it more CPU/RAM rather than splitting into separate scalable process types. Fix: TF5 — scale via the process model, split process types by workload.
