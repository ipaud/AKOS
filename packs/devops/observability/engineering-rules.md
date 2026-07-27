# Engineering Rules — Observability Pack

Checkable in the artifact. `★` marks the two rules that are safety-floor business: what
telemetry may carry is a data-protection decision, not an engineering preference
([security/privacy](../../security/privacy/README.md)). Everything else is Level 2
practice — strong defaults, not a floor. Parenthetical codes cite the principle in
[principles.md](principles.md).

## Choosing the signal

- OBS1. Each new signal states the question it answers before it is added. A metric that
  no query or alert consumes is not shipped. (P12)
- OBS2. "Why was *this* request slow" is answered by a trace, "is it usually slow" by a
  metric, "what happened at this point" by a log. Instrumentation that answers the wrong
  question is a finding even when it works. (P5)
- OBS3. Per-request identity — user, tenant, order, build, feature flag — goes on spans
  and events, never on metric labels. (P9, P10)
- OBS4. One richly-attributed record per unit of work is preferred to several thin log
  lines that must be reassembled to reconstruct one operation. (P7)
- OBS5. Aggregation happens at query time. Write-time pre-aggregation is justified
  explicitly, and only where the raw form is genuinely unaffordable. (P3)

## Tracing

- OBS6. Trace context propagates across every hop: HTTP, RPC, queues, background jobs,
  scheduled work, and third-party calls that support it. Standard propagation headers are
  used rather than a bespoke correlation header. (P6)
- OBS7. Propagation is verified end-to-end by an executed check — one request producing one
  connected trace across services — not assumed from the SDK being installed. (P6)
- OBS8. Async and queued work continues the originating trace, via a link where a direct
  parent-child relationship would be wrong. (P6)
- OBS9. Span names are low-cardinality and describe the operation (`GET /orders/{id}`, not
  `GET /orders/12345`). Identifiers go in attributes. (P9, P13)
- OBS10. Every span that can fail records its status and, on failure, the error type and
  message as attributes rather than only in a log elsewhere. (P8)
- OBS11. Spans wrap boundaries first — inbound handler, outbound call, database query,
  queue publish and consume. Internal spans are added where a boundary span proved
  insufficient, not preemptively. (P15)
- OBS12. Span attributes carry the dimensions a future question would slice by: tenant,
  plan, region, build, feature-flag state, cache hit, retry count. (P10)

## Metrics

- OBS13. Metric attribute sets are bounded and the bound is known — every attribute has an
  enumerable, small value range. An unbounded attribute on a metric is a defect, not a
  tuning issue. (P9)
- OBS14. Latency is recorded as a histogram, not an average. An average latency hides
  exactly the tail that users experience. (P5)
- OBS15. Service-level instrumentation covers request rate, error rate, and duration;
  resource-level covers utilization, saturation, and errors. Which of the two applies is
  stated per component. (P5)
- OBS16. Where the stack supports it, metrics link to example traces so a spike leads
  directly to a representative request. (P8)
- OBS17. Counters and histograms are never reset or re-created per request; instrument
  handles are created once at module scope. (P12)

## Logs

- OBS18. Logs are structured — machine-parseable fields, not interpolated prose that must
  be parsed with a regular expression later. (P7, P13)
- OBS19. Every log record emitted inside a traced operation carries the trace and span
  identifiers. (P8)
- OBS20. Log levels have stated meanings, and `error` is reserved for something a human
  should act on. A log level that fires on expected conditions trains everyone to ignore
  it. (P12)
- OBS21. Logging inside a hot loop or per-item within a batch is bounded — sampled,
  aggregated, or moved to a span attribute. (P11, P12)

## Naming and resource identity

- OBS22. Standard semantic-convention attribute names are used where one exists; local
  names are invented only for genuinely domain-specific fields, and are then used
  consistently everywhere. (P13)
- OBS23. Every telemetry-producing process identifies its service name, version, and
  deployment environment, so signals can be filtered to one deploy. (P13)
- OBS24. The build or release identifier is present on telemetry, making "did this start
  with the last deploy" a query rather than a guess. (P13, P16)
- OBS25. One concept keeps one field name across services. A field spelled two ways cannot
  be aggregated at all. (P13)

## Cost control

- OBS26. Sampling reduces what is *kept*, never what is *recorded*, and the strategy is
  written down. (P11)
- OBS27. Errors, slow requests, and rare code paths are retained at a higher rate than
  routine successes. Uniform sampling that discards anomalies is a finding. (P11)
- OBS28. Every signal has a stated retention period, set deliberately rather than left at
  a vendor default. (P12)
- OBS29. Telemetry volume and spend are themselves monitored, with an alert before the
  bill rather than after it. (P12)
- OBS30. Dashboards and alerts nobody has opened in a quarter are deleted, along with the
  instrumentation that existed only to feed them. (P12)

## What telemetry may carry

- OBS31 ★. No credential, token, session identifier, API key, or authorization header is
  ever recorded as an attribute, a log field, or part of a URL. Redaction happens at the
  emitting boundary, not by trusting the backend to hide it. (P14)
- OBS32 ★. Personal data in telemetry is treated as personal data: inventoried, given a
  lawful basis and a retention period, and covered by the deletion path — the telemetry
  vendor is a processor like any other. Prefer a pseudonymous identifier to a name or
  address. (P14, [privacy PR15/PR31](../../security/privacy/engineering-rules.md))
- OBS33. Full request and response bodies are not captured by default; where a payload is
  needed, specific fields are selected rather than the whole object. (P14)
- OBS34. Propagated baggage carries only what downstream services need for routing or
  correlation, and never a secret or personal data — it crosses process and often
  organizational boundaries. (P14)
- OBS35. Error objects are inspected before being recorded wholesale; exception payloads
  routinely contain the query, the arguments, and the connection string. (P14, OBS31)

## Working with it

- OBS36. A new user-facing feature ships with the instrumentation needed to debug it, in
  the same change. (P4)
- OBS37. After an incident, the missing signal is added as part of the follow-up — the
  question that could not be answered becomes an instrumentation task with an owner. (P2)
- OBS38. Debugging starts from the user-visible symptom and narrows by dimension; a fix
  applied without isolating which dimension differed is recorded as unverified. (P16)
- OBS39. Instrumentation is exercised in a non-production environment before it is relied
  on, including the failure paths — a span that is never emitted on error is discovered
  during the incident otherwise. (P4)
- OBS40. Vendor coupling is bounded: instrumentation uses a vendor-neutral API so the
  backend can change without re-instrumenting the application. (P12)

## Small-stack mapping

Most of this pack assumes you operate services. A Prototype or MVP on a managed platform
does not, and should not pretend otherwise — see
[decision-framework.md](decision-framework.md) for when to skip this pack entirely.

- OBS41. On a managed platform, start with what it already emits — platform request logs,
  function logs, database logs, and browser error reporting — before adding a collector or
  an agent. Most early questions are answerable there. (P15)
- OBS42. Even with no tracing stack, a request identifier is generated at the edge, logged
  by every layer that handles the request, and returned to the client so a user report maps
  to server records. This is the cheapest useful observability there is. (P6, P8)
- OBS43. Error tracking with release identifiers and source maps precedes distributed
  tracing on a small stack: it answers "what is broken and since which deploy" for a
  fraction of the effort. (P15, OBS24)
- OBS44. Browser-side user-experience measurement stays in
  [performance/core-web-vitals](../../performance/core-web-vitals/README.md); this pack
  covers the server side of the same request. (P5)
