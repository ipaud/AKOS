# Changelog — observability

## [1.0.0] — 2026-07-27

### Added

- First complete version. Authority level 2, review cadence 365 days
  (`review_after: 2027-07-27`). Cleared the source intake gate on a verified gap:
  `OpenTelemetry`, `distributed tracing`, `cardinality`, `semantic convention`,
  `RED method`, `USE method`, and `golden signal` all returned zero across the 57-pack
  corpus. `SLO` returned 111 hits and `error budget` 10 — all in `devops/sre` — which
  confirmed the boundary rather than an overlap: SRE owns the targets, this pack owns the
  signals they are measured from.
- Principles P1–P16 across what observability is, the signals, cost and cardinality, and
  discipline. The spine: observability answers questions nobody anticipated,
  pre-aggregation destroys those questions before they are asked, cardinality is the cost
  model and metrics are where it explodes, and instrumentation is part of the feature
  rather than a follow-up.
- Engineering rules OBS1–OBS44 across signal choice, tracing, metrics, logs, naming and
  resource identity, cost control, what telemetry may carry, working method, and a
  small-stack mapping.
- **Only two rules are starred, and neither is about observability.** OBS31 (no credential
  or token in telemetry) and OBS32 (personal data in telemetry is personal data —
  inventoried, pseudonymized, retained deliberately, reachable by the deletion path) are
  the safety floor arriving through this pack. Telemetry leaves the system into a third
  party's store with long retention and broad team access; the vendor is a processor like
  any other. The scoring rubric says to score those findings here **or** in
  `security/privacy`, never both.
- **A small-stack mapping (OBS41–OBS44) and a "do you need this pack yet" table.** Most of
  the domain assumes you operate services. A managed-platform MVP does not, and the pack
  says so first rather than in a footnote: platform logs, a request identifier generated at
  the edge and returned to the client, and error tracking with release identifiers answer
  most early questions. The corresponding anti-pattern — the observability platform nobody
  needed — is listed, and the scoring rubric refuses to deduct a small stack for having no
  distributed tracing, calling that a rubric error rather than a finding.
- Anti-patterns: the cardinality bomb, the broken trace, the average, logging as prose, the
  write-time aggregate, the secret in the span, personal data by accident, uniform
  sampling, the dashboard graveyard, instrumentation as a follow-up ticket, and two
  failures of adopting the pack — the platform nobody needed, and instrumentation used
  instead of reproducing a bug that reproduces locally in a minute.
- Prompt fragments include a dedicated small-stack block that explicitly tells an agent
  *not* to propose a collector, a tracing backend, or a sampling policy for a managed
  platform with modest traffic.

### Authority level: 2, not 1

The roadmap entry that queued this pack proposed Level 1 on the strength of the
OpenTelemetry specification. Reconsidered while writing, and recorded in
[references.md](references.md): OpenTelemetry is a CNCF project authoritative *about
itself* and broadly adopted, but not a normative standard in the sense of the IETF RFCs
behind `security/auth`, or of WCAG. The reasoning half of the pack — unknown-unknowns, wide
events, high cardinality as a feature, the narrowing debug loop — is book-derived, which is
Level 3 territory. Claiming Level 1 would lend book judgment the deference owed to
normative requirements. Level 2 matches the sibling `devops/sre`, which distills the Google
SRE book at the same level. W3C Trace Context genuinely is Level 1 and is cited as the
authority where this pack restates it.

### Scope boundary

Recorded against `packs/devops/sre` (targets, alerting, on-call, incident process),
`packs/devops/deployment` (rollout and rollback), `packs/security/privacy` (whether a field
may leave the system at all), `packs/performance/core-web-vitals` (the browser side of the
same request), and `packs/ai-engineering/agent-evals` (non-deterministic output quality,
which a latency histogram cannot measure).
