# Prompt Fragments — CI/CD Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply continuous delivery practice (AKOS L2):
- Order pipeline stages cheapest-first: lint → typecheck → unit tests →
  build → integration → E2E → deploy. A failure must surface before any
  expensive stage runs.
- Branch protection blocks merge on a red pipeline. main contains only
  commits that passed the full gate.
- Budget pipeline runtime and keep it under ~10-15 minutes. Parallelize
  independent jobs, shard test suites, cache dependencies and build
  output. A slow pipeline gets routed around under deadline pressure.
- Production deploy is triggered automatically from a passing pipeline on
  main, or by an explicit auditable trigger promoting that same verified
  artifact. Never rebuild the artifact at deploy time.
- Zero manual deploy steps. A "temporary" manual step is permanent risk.
- Rollback to the previous release is one automated command or button,
  exercised at least once outside a real incident.
- Decouple deploy from release with feature flags where available: ship
  code continuously, expose it to users deliberately.
- CI secrets (deploy keys, registry credentials, API tokens) live in the
  CI platform's secret manager — never in pipeline config or the repo.
- A red main is an incident: stop the line, revert or fix forward, do not
  stack new work on a broken build.
```

## Fragment: review lens

```text
Review this pipeline and delivery setup as a CI/CD reviewer:
1. Stage order — does anything slow or expensive run before lint,
   typecheck, and unit tests?
2. Gate — is branch protection actually enforcing the pipeline, or is the
   check optional, advisory, or bypassable?
3. Secrets — scan pipeline config for inline tokens, keys, credentials.
   Any hit is HIGH.
4. Artifact integrity — does the artifact that was tested deploy, or does
   deploy rebuild from source and ship something never verified?
5. Manual steps — list every human action between merge and production.
6. Rollback — one action or an improvised procedure? Last actually run?
7. Runtime — total wall-clock and the slowest stage. Is it fast enough
   that nobody is tempted to merge around it?
Report against review-checklist.md by severity, each finding naming the
specific pipeline file and the concrete change.
```

## Fragment: slow-pipeline triage

```text
Triage a pipeline that has grown too slow:
- Measure per-stage wall-clock time and rank stages by duration.
- For the slowest stage apply, in order: cache (dependencies, build
  output, test fixtures), parallelize (shard tests, run independent jobs
  concurrently), reorder (move it behind cheaper gates), scope (run only
  on changed paths).
- Never buy speed by deleting a gate or making a required check
  non-blocking.
- Re-measure after each change; stop when total runtime is in budget.
Output: current stage timings, the change per stage, projected runtime.
```

## Fragment: delivery rigor selection

```text
Select CI/CD rigor for this project's profile:
- Prototype — lint plus basic tests; manual deploy acceptable.
- MVP — full pipeline; automated deploy to staging; manual promote to
  production.
- Production — full pipeline; automated deploy to production from main;
  automated rollback.
- Enterprise — the above plus security scanning gates, staged rollout,
  and monitoring-triggered automatic rollback.
Choose continuous deployment (every merge auto-deploys) only when test
coverage, monitoring, and rollback speed already support it. Otherwise
choose continuous delivery (every merge is deployable; deploy is a
deliberate trigger). Decide on demonstrated readiness, not aspiration.
```

## One-liner (for tight token budgets)

```text
CI/CD: cheap stages first; red pipeline blocks merge; secrets only in the
CI secret manager; deploy the tested artifact automatically from a green
main with no manual steps; rollback is one tested command; keep runtime
under ~15min so nobody routes around the gate; a red main stops the line.
```
