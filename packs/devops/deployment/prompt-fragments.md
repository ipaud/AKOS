# Prompt Fragments — Deployment Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply safe deployment practice (AKOS L2):
- Match rollout strategy to blast radius: trivial config/copy change →
  direct deploy; new feature or behavior change → canary (5-10% traffic,
  monitor, ramp) or rolling; infra/schema change or major rewrite →
  blue-green with an explicit cutover decision point.
- Never switch 100% of traffic instantly for a significant change.
- Schema changes stay backward-compatible with the currently-running
  application version. Old and new versions run simultaneously during
  rollout and both must work against the new schema.
- Sequence migrations expand-contract as separate deploys: add new →
  deploy → dual-write → backfill → move reads → deploy → drop old. Never
  add a NOT NULL column and drop its predecessor in one release.
- Destructive DDL (drop column/table, rename) ships only after zero
  remaining reads are confirmed over a full traffic cycle.
- Every data migration has a tested reversal path, or a written reason
  none can exist (e.g. genuinely one-way anonymization).
- Rollback is one automated action, exercised at least quarterly outside
  a real incident. An untested rollback is not a rollback.
- Automated post-deploy smoke tests assert the critical paths before the
  release is marked successful.
- High-risk deploys have a named owner monitoring through stabilization,
  in a window when the team is available — no Friday-evening schema
  changes without genuine 24/7 coverage.
```

## Fragment: review lens

```text
Review this release as a deployment reviewer:
1. Blast radius — how many users hit the change at once if it is bad, and
   does the rollout strategy match that exposure?
2. Mixed-version state — walk the moment old and new application versions
   both run against the new schema. Does either break?
3. Destructive operations — any DROP, RENAME, or added NOT NULL shipping
   in the same release as the code that stops using the old shape?
4. Reversibility — can this data migration be undone, and has the
   reversal actually been executed against realistic data?
5. Rollback — one action or improvisation? Time-to-restore? Last run?
6. Verification — what runs automatically after deploy to prove health,
   and which user-visible paths does it actually cover?
7. Ownership and timing — who watches, for how long, starting when?
Report against review-checklist.md by severity. An irreversible change or
a mid-rollout-breaking migration is HIGH regardless of feature value.
```

## Fragment: expand-contract migration plan

```text
Plan this schema/data change as an expand-contract sequence:
Deploy 1 (expand) — additive only: nullable or defaulted new column, new
  table, index built without blocking writes. Existing code unaffected.
Backfill — batched, resumable, rate-limited, safe to re-run, executed
  outside peak traffic.
Deploy 2 (migrate) — application dual-writes, then reads move to the new
  shape. The old shape stays populated and correct.
Deploy 3 (contract) — drop the old column/table only after logs or
  metrics confirm zero reads across a full traffic cycle.
For each step state: exact DDL/DML, whether it takes a blocking lock,
expected duration at production row count, and the reversal action.
Do not collapse steps into a single deploy to save time.
```

## Fragment: rollout and rollback plan

```text
Produce a rollout plan before this release ships:
- Strategy and rationale (canary percentage and ramp schedule, rolling
  batch size, or blue-green cutover point).
- Health signals watched during ramp, each with its abort threshold:
  error rate, p95/p99 latency, and one key business metric.
- Post-deploy smoke tests: the 2-3 critical paths asserted automatically.
- Rollback trigger condition, rollback command, expected time-to-restore.
- Named owner and the monitoring window through stabilization.
If any line cannot be filled in, the release is not ready to ship.
```

## One-liner (for tight token budgets)

```text
Deployment: rollout proportional to blast radius, never instant full
cutover for a significant change; expand-contract migrations that never
break the mixed-version state; destructive DDL only after zero reads are
confirmed; every migration reversible or explicitly not; one-action
rollback tested quarterly; automated post-deploy smoke tests; a named
owner watching through stabilization.
```
