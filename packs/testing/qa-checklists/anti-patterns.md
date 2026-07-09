# Anti-Patterns — QA Checklists Pack

- **Happy-path-only QA** — testing only the ideal flow (data present, fast network, standard input), missing the states/edge cases where most real bugs hide.
- **Untested empty states** — a list feature demoed and shipped with only pre-populated test data, the empty state never actually seen until a real new user hits it broken.
- **Guessed browser matrix** — QA time spent on IE11-equivalent legacy combinations nobody uses per analytics, while the actual top mobile browser combination goes untested.
- **Unstructured exploratory testing** — "click around for a bit" with no charter and no reproducible findings log, producing vague unreproducible bug reports.
- **No regression pass** — each release re-breaks a previously-fixed bug because nothing checks for its return.
