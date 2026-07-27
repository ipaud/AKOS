# Decision Framework — Observability Pack

The choices this domain presents, and how to settle each one. The first section is the
most important, because the usual failure here is building a telemetry platform for a
system that needed a request identifier.

## Do you need this pack yet?

| Situation | Answer |
|---|---|
| Local prototype, no users | **No.** `console.log` and the platform's own logs. Adding a tracing stack now is the waste this pack warns about. |
| Deployed, one app, managed platform, few users | **Barely.** OBS41–OBS43: platform logs, a request identifier returned to the client, error tracking with release identifiers. Stop there. |
| Deployed, real users, one backend + a database | **Partly.** Add structured logs with trace-ish correlation, latency histograms on the slow endpoints, and an error budget's worth of signal ([sre](../sre/README.md)). |
| More than one service, or async work, or "it's slow but only sometimes" | **Yes.** This is where distributed tracing stops being ceremony and starts being the only way to answer the question. |
| A per-customer complaint you cannot reproduce | **Yes, urgently.** High-cardinality attributes on spans are the thing that answers it. |

The honest trigger is **"we could not answer a question about production"**, not a
headcount or an architecture diagram. If that has never happened, instrument the boundaries
(OBS11) and come back.

## Which signal for the question

| The question | Signal |
|---|---|
| Why was *this one* request slow? | Trace |
| Are requests generally slower than last week? | Metric (histogram) |
| What did the system do at 14:32? | Log |
| Which customers are affected? | Span/event attributes, sliced |
| Did this start with the last deploy? | Any signal, filtered by build identifier (OBS24) |
| Are we within our reliability target? | SLO — [sre](../sre/README.md), measured *from* these signals |
| Is the page slow for real users? | [core-web-vitals](../../performance/core-web-vitals/README.md) |

Reaching for a metric to answer a "which one" question is the most common mistake, and it
usually ends with someone adding a user ID to a metric label (OBS3) and a surprising bill.

## Where does an attribute go?

```
Is the value from a small, enumerable set (status, method, region, plan tier)?
   → metric label is fine
Does it identify a specific request, user, tenant, or entity?
   → span or event attribute, never a metric label
Is it a secret, credential, or token?
   → nowhere (OBS31)
Is it personal data?
   → pseudonymize, or inventory it and give it a retention period (OBS32)
Does it cross a service boundary and get read downstream?
   → baggage, and only if downstream genuinely needs it (OBS34)
```

## How much to sample

Start at 100% and reduce when volume forces it, not before — an early-stage system rarely
produces enough telemetry to matter, and sampling introduces a class of confusion ("the
trace isn't there") that costs more than the storage.

When reducing:

1. **Keep every error and every slow request.** These are the reason the data exists.
2. **Keep rare paths at a higher rate** than the hot path — the hot path is well-sampled at
   any rate.
3. **Sample the routine successes hard.** They are interchangeable in aggregate.
4. **Decide after the fact where you can** (tail-based), because the interesting property
   of a request is often only known once it finishes.
5. **Write the strategy down** (OBS26). An undocumented sampling policy makes every
   absence ambiguous.

## Build or buy

| Option | Choose when | Cost accepted |
|---|---|---|
| Platform-native (managed logs, error tracking) | Default for small stacks | Limited correlation, weak cross-service story |
| Vendor backend + vendor-neutral instrumentation | Real traffic, small team | Bill scales with cardinality — read OBS13 and OBS28 first |
| Vendor backend + a collector you run | Redaction, tail sampling, or multi-destination needed | One more thing to operate |
| Self-hosted stack | Data residency or scale genuinely requires it | You now operate a database that is bigger than your app |

Instrument with a vendor-neutral API regardless (OBS40). The instrumentation is the
expensive part and the backend is the swappable part; coupling them makes a migration into
a re-instrumentation.

## Profile modulation

- **Prototype** — skip the pack. Platform logs only.
- **Startup MVP** — OBS41–OBS43 plus the two starred rules. Structured logs, request
  identifier, error tracking, and never a secret or unpseudonymized personal data in
  telemetry.
- **Production** — the full checklist, with propagation verified end-to-end by an executed
  check (OBS7) and a written sampling and retention policy.
- **Enterprise** — plus telemetry as a governed data flow: the vendor is a processor,
  retention is set per signal, and the deletion path reaches it (OBS32).

## When NOT to use this pack

- **Before there is production traffic.** Instrumentation designed against imagined load
  measures the wrong things.
- **To answer a question a log line already answers.** The tracing stack is not the
  starting point; it is what you reach for when correlation across services is the problem.
- **As a substitute for reproducing a bug locally.** Observability is for what you cannot
  reproduce. When you can, that is faster.
- **For evaluating model or agent output** — non-deterministic quality needs
  [agent-evals](../../ai-engineering/agent-evals/README.md), not a latency histogram.
- **To set reliability targets.** That is [sre](../sre/README.md). This pack tells you what
  to measure with; that one tells you what "good enough" is.

## Related packs

| Question | Pack |
|---|---|
| What is our reliability target, and who gets paged? | [devops/sre](../sre/README.md) |
| How do we roll this out and roll it back? | [devops/deployment](../deployment/README.md) |
| What gates a merge? | [devops/ci-cd](../ci-cd/README.md) |
| May this field leave our system? | [security/privacy](../../security/privacy/README.md) |
| Is the page fast for real users? | [performance/core-web-vitals](../../performance/core-web-vitals/README.md) |
