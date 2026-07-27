# Heuristics — Observability Pack

Defaults with known exceptions. Use these while deciding what to instrument; the
[engineering rules](engineering-rules.md) apply once telemetry exists.

- **Don't build a telemetry platform for a system that needed a request identifier.**
  Generate one at the edge, log it everywhere, return it to the client. On a small stack
  that is most of the value for almost none of the cost.
- **Instrument the boundaries, then stop and see what's missing.** Inbound, outbound,
  database, queue. Most incidents live at a boundary, and instrumenting everything up front
  produces volume nobody queries.
- **If you're about to put an ID on a metric label, you wanted a span.** This single
  substitution prevents most surprise telemetry bills.
- **Ask "what dimension would I slice by at 3am?" and add that attribute now.** Tenant,
  plan, build, region, feature flag, retry count. Adding it later means the incident you're
  in still can't be answered.
- **Put the build identifier on everything.** "Did this start with the last deploy" is the
  single most-asked production question, and it should be a filter rather than a guess.
- **Log the pseudonym, never the person.** Correlation is what debugging needs; identity is
  what the privacy review objects to. You can have the first without the second.
- **Keep every error and every slow request, whatever the sample rate.** Sampling that
  discards the anomalies has optimized away the reason the data existed.
- **Start at 100% sampling and reduce under pressure.** Early systems rarely produce enough
  telemetry to matter, and "the trace isn't there" costs more confusion than the storage
  saved.
- **An average latency is a lie by construction.** Histogram or nothing — the tail is the
  part users experience.
- **A dashboard nobody opens is a cost, and so is the instrumentation feeding it.** Delete
  both. Telemetry accumulates exactly like code.
- **Write the instrumentation with the feature, in the same change.** Retrofitting it
  happens under incident pressure, by whoever is on call, which is the worst combination
  available.
- **Exercise the failure path before trusting it.** A span that is never emitted on error
  is discovered during the outage otherwise.
- **After every incident, name the question you couldn't answer.** That question is the next
  instrumentation task, and it is the only reliably-correct backlog this domain produces.
- **Debug by narrowing, not by guessing.** Symptom → slice by dimension → find where
  behavior diverges. Intuition finds causes you've seen before, which are by definition not
  the ones still taking you down.
- **Prefer a vendor-neutral API even if you're sure about the vendor.** Instrumentation is
  the expensive half; the backend is the swappable half.
