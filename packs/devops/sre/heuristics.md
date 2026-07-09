# Heuristics — SRE Pack

- An alert that's fired 20 times this month, dismissed 19 times as noise → either fix the underlying issue or delete the alert; it's training the on-call to ignore pages.
- No SLO defined for a critical service → symptom of "we'll notice if it's really broken" reactive operations; define one before the next incident, not after.
- A postmortem naming a specific person as the cause → rewrite toward the process/system gap that allowed the mistake to have impact.
- The same manual operational task performed weekly by a human → toil; script/automate it.
- An incident resolved by "someone remembered what to do" rather than a runbook → write the runbook now, while it's fresh.
