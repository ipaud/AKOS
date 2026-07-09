# Anti-Patterns — SRE Pack

- **Alert fatigue** — dozens of low-signal alerts firing constantly, training the on-call to ignore pages, until a real one is missed among the noise.
- **Cause-based paging** — paging on "CPU > 80%" instead of "users are seeing errors," waking someone for a non-issue while missing user-impacting problems that don't correlate with the watched metric.
- **Blame-first postmortems** — incident reviews that identify "who broke it" instead of "what systemic gap allowed this," discouraging honest reporting of near-misses.
- **No SLO, reactive-only operations** — reliability work only happens after an outage, with no proactive target or budget guiding investment.
- **Tribal-knowledge incident response** — resolving incidents relies on one specific engineer's memory, with no runbook, creating a single point of failure in the response process itself.
