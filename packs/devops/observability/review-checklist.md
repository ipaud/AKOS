# Review Checklist — Observability Pack

Binary checks, each citing its rule. Only the two data-protection items are CRITICAL —
they are the safety floor arriving through this pack, not an observability opinion.
Everything else is Level 2 practice.

## Critical (blocks in every profile)

- [ ] No credential, token, session identifier, API key, or authorization header appears
      in any attribute, log field, or URL. (OBS31)
- [ ] Personal data in telemetry is inventoried, pseudonymized where possible, given a
      retention period, and covered by the deletion path — the vendor is a
      processor. (OBS32)

## High

- [ ] No unbounded attribute (user ID, raw URL with identifiers, email) is used as a
      metric label. (OBS3, OBS13)
- [ ] Trace context propagates across every hop, including queues and background
      jobs. (OBS6)
- [ ] Propagation is verified end-to-end by an executed check, not assumed from the SDK
      being installed. (OBS7)
- [ ] Span names are low-cardinality; identifiers live in attributes. (OBS9)
- [ ] Latency is a histogram, not an average. (OBS14)
- [ ] Logs are structured fields, not interpolated prose. (OBS18)
- [ ] Log records inside a traced operation carry trace and span identifiers. (OBS19)
- [ ] Full request and response bodies are not captured by default. (OBS33)
- [ ] Baggage carries nothing secret or personal. (OBS34)
- [ ] Error objects are inspected before wholesale capture — payloads routinely contain
      queries, arguments, and connection strings. (OBS35)
- [ ] Sampling keeps errors, slow requests, and rare paths at a higher rate than routine
      successes. (OBS27)

## Medium

- [ ] Each signal states the question it answers; nothing is emitted that no query or alert
      consumes. (OBS1)
- [ ] The signal type matches the question — trace for "this one", metric for "in general",
      log for "at this point". (OBS2)
- [ ] One wide record per unit of work, rather than several thin lines to reassemble. (OBS4)
- [ ] Aggregation happens at query time unless write-time is explicitly justified. (OBS5)
- [ ] Async and queued work continues or links the originating trace. (OBS8)
- [ ] Failing spans record status and error type. (OBS10)
- [ ] Boundaries are instrumented first: inbound, outbound, database, queue. (OBS11)
- [ ] Span attributes carry the dimensions a future question would slice by. (OBS12)
- [ ] Rate/errors/duration for services, utilization/saturation/errors for resources, with
      which applies stated per component. (OBS15)
- [ ] Standard semantic-convention names are used where one exists. (OBS22)
- [ ] Service name, version, and environment identify every telemetry producer. (OBS23)
- [ ] The build or release identifier is present on telemetry. (OBS24)
- [ ] One concept, one field name, across services. (OBS25)
- [ ] Sampling reduces what is kept, never what is recorded, and is written down. (OBS26)
- [ ] Every signal has a deliberately set retention period. (OBS28)
- [ ] Instrumentation ships in the same change as the feature it debugs. (OBS36)
- [ ] Instrumentation was exercised, including failure paths, before being relied on. (OBS39)

## Low

- [ ] Metrics link to example traces where the stack supports it. (OBS16)
- [ ] Instrument handles are created once, not per request. (OBS17)
- [ ] Log levels have stated meanings and `error` means a human should act. (OBS20)
- [ ] Logging in hot loops and per-item in batches is bounded. (OBS21)
- [ ] Telemetry volume and spend are monitored with an alert before the bill. (OBS29)
- [ ] Unused dashboards, alerts, and their feeding instrumentation are deleted. (OBS30)
- [ ] Instrumentation uses a vendor-neutral API. (OBS40)

## Small stack (managed platform, few users)

Check these *instead of* most of the above — see
[decision-framework.md](decision-framework.md).

- [ ] Platform-native logs are being used before any collector or agent is added. (OBS41)
- [ ] A request identifier is generated at the edge, logged by every layer, and returned to
      the client. (OBS42)
- [ ] Error tracking with release identifiers and source maps exists. (OBS43)
- [ ] Browser-side user-experience measurement is routed to
      [core-web-vitals](../../performance/core-web-vitals/README.md), not duplicated
      here. (OBS44)

## Process

- [ ] After an incident, the signal that was missing became an instrumentation task with an
      owner. (OBS37)
- [ ] Fixes applied without isolating which dimension differed are recorded as
      unverified. (OBS38)
