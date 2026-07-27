# Glossary — Observability Pack

Terms this pack uses precisely. Where a word collides with another pack's usage, the entry
says so.

- **Observability** — the ability to answer new questions about production without shipping
  new code. Contrasted with monitoring, which answers questions anticipated in advance.
- **Monitoring** — checking known conditions against known thresholds. Necessary, not
  sufficient, and not a lesser version of observability.
- **Signal** — a kind of telemetry. Traces, metrics, and logs are the three this pack
  covers; each answers a different question and none substitutes for another.
- **Trace** — the record of one request's path through a system, as a tree of spans.
- **Span** — one operation within a trace: a name, a start and end time, attributes,
  status, and a parent. `devops/git` and `domain-driven-design` use "span" in unrelated
  senses.
- **Span link** — a reference to another trace or span where a direct parent-child
  relationship would misrepresent the causality. The correct shape for batch and queue
  work.
- **Context propagation** — carrying trace identity across a process boundary so the
  downstream work joins the same trace. The part that breaks quietly.
- **Baggage** — key-value pairs propagated alongside trace context for downstream use.
  Crosses process and often organizational boundaries, so never carries secrets or personal
  data.
- **Attribute** — a key-value pair on a span, metric, or log record. Where dimensions live.
- **Resource attributes** — attributes describing the entity producing telemetry: service
  name, version, deployment environment.
- **Semantic conventions** — the standard names for common attributes, so telemetry from
  different services and libraries aggregates. Adopting them beats inventing local names.
- **Cardinality** — the number of distinct values a field takes. The cost model for
  metrics, and the value model for traces.
- **Dimensionality** — how many different fields are attached to a record. Wide records are
  what make slicing by an unanticipated dimension possible.
- **Wide event** — one richly-attributed record per unit of work, rather than several thin
  log lines that must be reassembled.
- **Histogram** — a distribution of values across buckets. What latency should be recorded
  as; an average is not a distribution.
- **Exemplar** — a link from an aggregated metric to a representative trace, so a spike
  leads to a specific request.
- **Head sampling** — deciding whether to keep a trace when it starts. Cheap, and blind to
  how the request turned out.
- **Tail sampling** — deciding after the request finishes, once you know it was slow or
  failed. More expensive, and keeps the records that matter.
- **Instrumentation** — the code that emits telemetry. The expensive half; the backend is
  the swappable half.
- **Collector** — a process that receives, processes, and forwards telemetry. Where
  redaction and tail sampling belong when you run one.
- **RED** — Rate, Errors, Duration. The service-level view.
- **USE** — Utilization, Saturation, Errors. The resource-level view.
- **Golden signals** — latency, traffic, errors, saturation. Belongs to the
  [sre](../sre/README.md) source; cited here for the boundary between the two packs.
- **SLO / error budget** — reliability targets. This pack supplies the measurement; the
  targets are [devops/sre](../sre/README.md).
- **Unknown unknowns** — failures nobody enumerated in advance. The class observability
  exists for. [philosophy-of-software-design](../../architecture/philosophy-of-software-design/glossary.md)
  uses the same phrase about code comprehension — related idea, different subject.
- **Core analysis loop** — start from the user-visible symptom, slice by dimension, find
  where behavior diverges from baseline, repeat. Narrowing rather than guessing.
