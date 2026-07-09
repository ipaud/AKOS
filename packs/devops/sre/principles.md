# Principles — SRE Pack

- **SR1** — Every production service has defined SLIs and SLOs for its critical user journeys, not just "we'll know if it's down."
- **SR2** — Alerts fire on symptoms affecting users (error rate, latency SLO breach), not on every resource-utilization fluctuation.
- **SR3** — An error budget is tracked; when exhausted, feature velocity yields to stability work until it recovers.
- **SR4** — Every page-worthy alert is actionable — if a human receiving it at 3am can't do anything useful, it shouldn't page.
- **SR5** — Postmortems are blameless, focus on systemic causes, and produce concrete follow-up actions with owners.
- **SR6** — Toil (manual, repetitive, automatable ops work) is tracked and actively reduced, not accepted as a permanent cost of operations.
- **SR7** — Runbooks exist for known failure modes, reducing incident response to "follow the documented steps" rather than improvisation under pressure.
