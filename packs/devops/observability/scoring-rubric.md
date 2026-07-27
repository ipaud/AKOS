# Scoring Rubric — Observability Pack

Feeds the maintainability and release dimensions
([scoring/maintainability-score.md](../../../scoring/maintainability-score.md),
[scoring/overall-score.md](../../../scoring/overall-score.md)). Reliability *targets* score
under [devops/sre](../sre/README.md) — this rubric measures whether the signals exist to
meet them.

The two data-protection findings below are the safety floor arriving through this pack;
score them here **or** in [security/privacy](../../security/privacy/README.md), not both.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Credential, token, session identifier, or authorization header recorded in telemetry | −40 (CRITICAL) |
| Personal data in telemetry with no inventory entry, retention period, or deletion path | −25 (CRITICAL) |
| Unbounded attribute used as a metric label (user ID, raw URL with identifiers) | −10 (HIGH) |
| Trace context does not propagate across a hop that exists (queue, background job, service call) | −10 (HIGH) |
| Full request or response bodies captured by default | −10 (HIGH) |
| Error objects recorded wholesale without inspection | −10 (HIGH) |
| Uniform sampling that discards errors and slow requests at the same rate as successes | −10 (HIGH) |
| Latency reported as an average rather than a distribution | −6 (MEDIUM) |
| Logs unstructured — interpolated prose requiring a parser | −6 (MEDIUM) |
| No trace/span identifiers in log records emitted inside traced operations | −6 (MEDIUM) |
| Propagation asserted but never verified end-to-end by an executed check | −6 (MEDIUM) |
| No build or release identifier on telemetry | −6 (MEDIUM) |
| Boundaries (inbound, outbound, database, queue) not instrumented | −6 (MEDIUM) |
| Write-time pre-aggregation with no stated justification | −4 (MEDIUM) |
| Signals emitted that no query or alert consumes | −4 (MEDIUM) |
| No stated retention period for a signal | −4 (MEDIUM) |
| Local attribute names where a standard convention exists; one concept spelled two ways | −4 (MEDIUM) |
| High-cardinality span names (identifiers in the name) | −4 (MEDIUM) |
| Instrumentation shipped separately from the feature it debugs | −4 (MEDIUM) |
| Failure paths of the instrumentation never exercised | −4 (MEDIUM) |
| Telemetry spend unmonitored | −2 (LOW) |
| Unused dashboards and their feeding instrumentation retained | −2 (LOW) |
| Instrumentation coupled to one vendor's API | −2 (LOW) |
| `error` level used for expected conditions | −2 (LOW) |

## Caps and floors

- Any CRITICAL: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md).
- **Scored against the stack actually in use.** A managed-platform MVP is scored on
  OBS41–OBS43 (platform logs, request identifier returned to the client, error tracking
  with release identifiers). Deducting it for having no distributed tracing is a rubric
  error, not a finding — see the "do you need this pack yet" table in
  [decision-framework.md](decision-framework.md).
- **Prototype profile: `n/a`.** Except the two CRITICAL rows, which are the floor and never
  modulate.
- Building a collector-and-tracing stack for a single-service app with no unanswered
  production question is reported as over-engineering under
  [architecture/philosophy-of-software-design](../../architecture/philosophy-of-software-design/README.md),
  not rewarded here.

## Anchors

- **95** — boundaries instrumented, propagation verified by an executed check, identity on
  spans and never on metric labels, anomaly-biased sampling written down, retention set per
  signal, nothing secret or unpseudonymized leaving the system.
- **85** — solid; MEDIUM gaps (missing build identifier, some unstructured logs) scheduled.
- **72** — the signals exist but do not connect: traces break at a boundary, logs carry no
  trace identifiers, debugging means three tools and a guess.
- **60** — production questions are answered by reading code and redeploying with new
  logging. This is what "we're flying blind" measures.
- **≤ 40** — telemetry is a data-protection liability: secrets or unclassified personal
  data are leaving the system.
