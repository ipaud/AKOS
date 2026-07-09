# Heuristics — CI/CD Pack

- Pipeline taking >10-15 minutes → identify the slowest stage, parallelize or cache it, or move it later in the sequence.
- A "temporary" manual deploy step still in place months later → automate it now, it's accumulating risk every release.
- Pipeline config containing a hardcoded API key/token → move to the CI platform's secret store immediately.
- A rollback that requires SSHing into a server and running commands from memory → automate it into a one-command/one-click action before the next incident.
- main red for more than a few minutes → treat as an incident (stop-the-line), don't let it linger while new work piles on top.
