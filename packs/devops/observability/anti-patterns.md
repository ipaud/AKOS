# Anti-Patterns — Observability Pack

Named failure modes, how to spot them, and what to do instead. The last two are failures
of *adopting* this pack, which on a small stack is the likelier risk.

## The cardinality bomb

**Detect:** a user ID, email, raw URL containing an identifier, or request ID used as a
metric label or dimension.
**Why it fails:** every distinct combination of label values is a stored time series, so
one unbounded label multiplies cost without limit. It usually surfaces as a bill, not as an
error.
**Fix:** identity goes on spans and events, which are built for it; metric labels stay
small and enumerable. If the question is "which user", you wanted a trace. (OBS3, OBS13)

## The broken trace

**Detect:** traces that end at a service boundary, or a queue consumer whose work appears
as an unrelated root span. Each fragment looks healthy on its own.
**Why it fails:** the propagation gap is invisible until the incident where you need to
follow one request across the whole system, and then the data simply isn't there.
**Fix:** propagate standard context on every hop — including queues, scheduled work, and
background jobs — and verify end-to-end with an executed check rather than assuming the SDK
handled it. Use links where a direct parent-child relationship would be wrong. (OBS6,
OBS7, OBS8)

## The average

**Detect:** a latency dashboard showing means; an SLO defined on average response time.
**Why it fails:** averages hide the tail, and the tail is the part users experience. A
service with a good average and a bad p99 has a bad reputation and a green dashboard.
**Fix:** histograms, and percentiles chosen against what users notice. (OBS14)

## Logging as prose

**Detect:** `logger.info("User " + id + " did " + action + " in " + ms + "ms")`, later
parsed by a regular expression somebody maintains.
**Why it fails:** it cannot be aggregated, filtered, or sliced without parsing, and the
parser breaks the first time someone rewords the message.
**Fix:** structured fields. The message is a stable key; everything variable is an
attribute. (OBS18)

## The write-time aggregate

**Detect:** a counter incremented per event with no supporting detail; a nightly rollup
that replaces the raw records.
**Why it fails:** it answers exactly the question that was anticipated and no others. The
moment someone asks "which tenant drove that spike", the data to answer it was discarded
before it was stored.
**Fix:** aggregate at query time. Where write-time aggregation is genuinely necessary for
cost, say so explicitly and keep a sampled raw stream alongside. (OBS5, P3)

## The secret in the span

**Detect:** authorization headers captured wholesale, connection strings in exception
attributes, tokens in URLs, request bodies attached "for debugging".
**Why it fails:** telemetry leaves your system, lands in a third-party store with long
retention and broad team access, and is rarely covered by the same review as your database.
**Fix:** redact at the emitting boundary rather than trusting the backend to hide it;
select specific fields instead of whole payloads; inspect error objects before recording
them. (OBS31, OBS33, OBS35)

## Personal data by accident

**Detect:** emails and names as span attributes or log fields; telemetry absent from the
data inventory; a vendor that never went through processor review.
**Why it fails:** it is a personal-data store that nobody classified, with a retention
period nobody set, outside the deletion path.
**Fix:** pseudonymous identifiers by default; inventory what remains; treat the telemetry
vendor as the processor it is. (OBS32, and
[privacy PR31](../../security/privacy/engineering-rules.md))

## Uniform sampling

**Detect:** "we keep 1% of traces", applied evenly.
**Why it fails:** errors and slow requests are rare by definition, so uniform sampling
discards precisely the records the system was instrumented to capture. The 1% you kept is
1% of the boring ones.
**Fix:** keep anomalies at a much higher rate; sample the routine hard; decide after the
fact where the stack supports it. (OBS26, OBS27)

## The dashboard graveyard

**Detect:** dozens of dashboards, most last opened months ago; alerts routed to a channel
everyone mutes; metrics no query references.
**Why it fails:** it costs storage, review attention, and — worse — credibility, because a
wall of ignored signals teaches the team that signals are ignorable.
**Fix:** delete unopened dashboards and the instrumentation that fed only them. `error`
means a human should act; anything else is a different level. (OBS20, OBS30)

## Instrumentation as a follow-up ticket

**Detect:** a feature shipped with a "add logging" task in the backlog.
**Why it fails:** the ticket is done when it's convenient, which is never, and the code is
blind exactly when it first breaks — retrofitted under incident pressure by whoever is on
call.
**Fix:** instrumentation is part of the change, not after it, and the missing signal from
the last incident becomes an owned task. (OBS36, OBS37)

## The observability platform nobody needed

**Detect:** a collector, a tracing backend, and a sampling policy in front of one Next.js
app with two hundred users and no unanswered production questions.
**Why it fails:** it is a second system to operate, built against imagined load, measuring
things nobody asked about — while the actual first question ("which request did this user
hit?") would have been answered by an ID in a header.
**Fix:** platform logs, a request identifier returned to the client, error tracking with
release identifiers. Add tracing when correlation across services is genuinely the problem.
(OBS41, OBS42, OBS43, and the "do you need this pack yet" table in
[decision-framework.md](decision-framework.md))

## Instrumentation instead of reproduction

**Detect:** hours spent adding spans to chase a bug that reproduces locally in a minute.
**Why it fails:** observability is for what you *cannot* reproduce. Where you can, a
debugger is faster and more precise.
**Fix:** try to reproduce first. Reach for telemetry when the failure is
environment-specific, load-dependent, customer-specific, or intermittent.
([decision-framework](decision-framework.md), "when NOT to use this pack")
