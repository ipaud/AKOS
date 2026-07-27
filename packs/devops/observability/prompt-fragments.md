# Prompt Fragments — Observability Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first — in
most tasks the build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
OBSERVABILITY CONSTRAINTS (Level 2 practice, except the two floor rules at the end):

Before adding a signal
- Say which question it answers. A metric no query or alert consumes doesn't ship.
- Trace answers "why was THIS request slow". Metric answers "is it usually slow". Log
  answers "what happened at this point". Using the wrong one is a defect even when it works.
- Aggregate at query time. Write-time aggregation throws away the questions nobody has
  asked yet.

Where attributes go
- Per-request identity (user, tenant, order, build, feature flag) → span/event attributes.
- NEVER on metric labels: every distinct combination is a stored series, and one unbounded
  label multiplies cost without limit. If you want "which user", you want a trace.
- Metric labels are small enumerable sets only (status, method, region, plan tier).

Tracing
- Propagate standard trace context on EVERY hop: HTTP, RPC, queues, background jobs,
  scheduled work. Verify end-to-end with an executed check; don't assume the SDK did it.
- Async work continues the originating trace, or links to it.
- Span names are low-cardinality: "GET /orders/{id}", never "GET /orders/12345".
- Failing spans record status and error type.
- Instrument boundaries first: inbound, outbound, database, queue.

Metrics and logs
- Latency is a histogram. An average hides the tail users actually experience.
- Logs are structured fields, never interpolated prose parsed by regex later.
- Log records inside a traced operation carry trace and span IDs.
- Service name, version, environment, and build ID on everything — "did this start with
  the last deploy" should be a filter, not a guess.

Cost
- Sampling reduces what is KEPT, never what is recorded. Keep every error and slow request;
  sample routine successes hard. Uniform sampling discards exactly the anomalies you
  instrumented for.
- Every signal gets a deliberate retention period.

FLOOR (never waived, any profile):
- No credential, token, session ID, API key, or authorization header in any attribute, log
  field, or URL. Redact at the emitting boundary.
- Personal data in telemetry IS personal data: pseudonymize by default, inventory what
  remains, set retention, cover it in the deletion path. The telemetry vendor is a
  processor. Don't capture full request/response bodies by default; inspect error objects
  before recording them — payloads routinely carry queries, arguments, connection strings.
```

## Fragment: small-stack block (managed platform, few users)

```text
This project runs on a managed platform with modest traffic. Do NOT propose a collector,
a tracing backend, or a sampling policy. Do this instead:

1. Use what the platform already emits: request logs, function logs, database logs.
2. Generate a request identifier at the edge, log it in every layer that handles the
   request, and return it to the client so a user report maps to server records.
3. Add error tracking with release identifiers and source maps — it answers "what is broken
   and since which deploy" for a fraction of the effort of tracing.
4. Keep browser-side user-experience measurement in the core-web-vitals pack, not here.

The two floor rules still apply in full: no secrets in telemetry, and personal data in
telemetry is personal data.

Revisit when there is more than one service, async work, or a customer-specific problem
that cannot be reproduced.
```

## Fragment: review lens

```text
Review this code against the AKOS observability pack (devops/observability).

Report findings citing rule codes (OBS1–OBS44). Only two are CRITICAL, and both are data
protection rather than observability: secrets in telemetry (OBS31), and unclassified
personal data in telemetry (OBS32). Everything else is HIGH or below.

Score against the stack actually in use. If this is a managed-platform app with modest
traffic, check OBS41–OBS43 and do NOT report the absence of distributed tracing — that is a
rubric error, not a finding.

Prioritize: secrets and personal data in telemetry, then unbounded metric labels, then
broken trace propagation, then uniform sampling that discards anomalies, then averages
instead of histograms, then unstructured logs.

For each finding: the rule code, file and line, the question that becomes unanswerable (or
the data that leaks), and the smallest fix.
```

## Fragment: incident follow-up

```text
An incident just closed. Answer these before the follow-up ticket is written:

1. What question could we not answer from existing telemetry?
2. Which signal would have answered it — trace, metric, or log?
3. Which dimension would we have sliced by? Is that attribute recorded today?
4. Did we know which deploy it started with? If not, why is the build ID missing?
5. Was the fix verified by isolating the differing dimension, or applied on a hunch?

Turn (1) into an instrumentation task with an owner. That question is the only reliably
correct backlog this domain produces.
```

## One-liner (for tight token budgets)

```text
Observability floor: every signal names the question it answers; trace for "this one",
metric for "in general", log for "at this point"; identity on spans, NEVER on metric labels
(cardinality is the cost model); propagate trace context on every hop including queues and
verify it with an executed check; low-cardinality span names; histograms not averages;
structured logs carrying trace IDs; service name, version and build ID on everything;
sampling keeps errors and slow requests and drops routine successes; deliberate retention.
Hard floor: no secrets in telemetry, and personal data in telemetry is personal data.
Small managed stack? Platform logs + a request ID returned to the client + error tracking
with release IDs — nothing more.
```
