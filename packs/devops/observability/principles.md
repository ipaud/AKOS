# Principles — Observability Pack

Durable rules for instrumenting a system so it can be asked questions nobody anticipated.
[devops/sre](../sre/README.md) owns the *targets* — SLOs, error budgets, alerting,
incident response. This pack owns the *signals* those targets are measured from, and the
debugging that happens once an alert fires. The `OBS*` codes in
[engineering-rules.md](engineering-rules.md) derive from these.

## What observability is

- **P1 — Observability is the ability to answer new questions without shipping new
  code.** Monitoring answers questions you thought of in advance; observability handles
  the ones you didn't. The distinction is not a dashboard count — it is whether a novel
  hypothesis can be tested against data you already have.
- **P2 — The interesting failures are the ones nobody predicted.** Known failure modes get
  a check and an alert, and then they stop being interesting. What takes systems down is
  the combination nobody enumerated: this customer, on that plan, with this payload, after
  that deploy. Instrumentation is judged by whether it can isolate a combination.
- **P3 — Pre-aggregation destroys the questions you haven't asked yet.** A counter
  incremented at write time has already thrown away who, where, and with what. Aggregation
  is a query-time decision; doing it at write time trades tomorrow's unknown question for
  today's storage bill.
- **P4 — Instrumentation is part of the feature, not a follow-up.** Code shipped without
  it is code that cannot be debugged in production, and the moment it needs debugging is
  the worst moment to add it. "We'll add logging if it breaks" is a plan to be blind
  exactly once.

## The signals

- **P5 — Traces, metrics, and logs answer different questions and none replaces the
  others.** A trace shows where time went *in one request*. A metric shows the shape of
  *many* requests. A log records what happened *at one point*. Reaching for the wrong one
  is the most common instrumentation mistake — a metric cannot tell you why one customer's
  request was slow, and a trace cannot tell you whether it usually is.
- **P6 — One request should be one traceable story across every service it touches.**
  Trace context propagates or the trace is a collection of disconnected fragments, each of
  which looks fine. Propagation is the part that breaks quietly, at queue boundaries,
  background jobs, and third-party calls.
- **P7 — Attach context to a wide event rather than scattering it across narrow ones.**
  One richly-attributed record per unit of work beats ten thin log lines that must be
  reassembled by grep. The width is what makes slicing by an unanticipated dimension
  possible.
- **P8 — Correlation identifiers are the whole value of the signals together.** Trace and
  span identifiers in logs, exemplars from metrics to traces. Without those links a team
  has three disconnected tools and has to context-switch between them at 3am.

## Cost and cardinality

- **P9 — Cardinality is the cost model, and metrics are where it explodes.** Every
  distinct combination of attribute values on a metric is a stored series, so putting a
  user ID or a URL with an ID in it on a counter multiplies cost without bound. Traces and
  events tolerate high cardinality; metrics do not. Most surprise telemetry bills are this
  one mistake.
- **P10 — High cardinality is the point, in the place that supports it.** The fields that
  identify *which* request went wrong — user, tenant, build, region, feature flag — are the
  ones that make debugging possible. The rule is not "avoid high cardinality", it is "put
  it on events and traces, not on metric labels".
- **P11 — Sampling is how volume is controlled; dropping instrumentation is not.** Reduce
  what is *kept*, never what is *recorded*, and keep what is unusual: errors, slow
  requests, rare paths. Uniform sampling that discards the anomalies has optimized the
  bill by removing the reason the data existed.
- **P12 — A signal nobody has ever queried is a cost with no benefit.** Telemetry
  accumulates the same way code does. Retention, dimensions, and dashboards all deserve
  the same "what decision does this feed" question that a data column gets.

## Discipline

- **P13 — Naming conventions matter more here than almost anywhere else**, because
  telemetry is queried by people who did not write it, often under time pressure, and a
  field named three ways cannot be aggregated at all. Adopt the standard names before
  inventing local ones.
- **P14 — Telemetry crosses a trust boundary and carries whatever you put in it.** Request
  attributes, headers, error payloads, and propagated baggage all leave your system and
  land in a third party's store, usually with long retention and broad team access. This
  is a processor relationship and a personal-data decision, not just an engineering one —
  see [security/privacy](../../security/privacy/README.md).
- **P15 — Instrument the boundaries first.** Inbound requests, outbound calls, database
  queries, queue operations. Boundaries are where latency, failure, and blame actually
  live, and they cover most incidents at a fraction of the effort of instrumenting
  everything.
- **P16 — Debug by narrowing from a symptom, not by pattern-matching on a hunch.** Start
  from what the user experienced, slice by dimension, find where behavior diverges from the
  baseline, repeat. Intuition finds the causes you have seen before, which are by
  definition not the ones still taking you down.

## Scope

This pack covers instrumentation and the debugging it enables: signal choice, trace
propagation, attribute naming, cardinality, sampling, correlation, and what telemetry may
carry. It does not cover reliability targets, alerting policy, on-call, or incident
process ([devops/sre](../sre/README.md)), rollout mechanics
([devops/deployment](../deployment/README.md)), browser-side user-experience metrics
([performance/core-web-vitals](../../performance/core-web-vitals/README.md)), or evaluating
non-deterministic model output
([ai-engineering/agent-evals](../../ai-engineering/agent-evals/README.md)).
