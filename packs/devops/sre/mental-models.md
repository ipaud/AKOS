# Mental Models — SRE Pack

- **SLI → SLO → error budget chain:** an SLI (Service Level Indicator, e.g. "% of requests under 200ms") is measured; an SLO (Service Level Objective, e.g. "99.9% of requests under 200ms") sets the target; the error budget (0.1% in this example) is the amount of failure allowed before it's spent.
- **Alert on symptoms, not causes:** page a human for "users are experiencing errors" (a symptom, SLO-based), not "CPU is at 80%" (a cause that may or may not actually be hurting users) — cause-based alerting produces noise; symptom-based alerting produces signal.
- **Toil as the enemy of engineering time:** repetitive, manual, automatable operational work that scales linearly with system size — SRE practice actively works to eliminate it, not just tolerate it.
- **Blameless postmortems:** incident review focused on systemic/process causes, not individual fault — the psychological safety this creates is what makes people report near-misses honestly instead of hiding them.
