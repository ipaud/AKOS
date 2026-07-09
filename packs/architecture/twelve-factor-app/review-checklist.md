# Review Checklist — Twelve-Factor App Pack

## Critical

- [ ] No secrets/credentials/environment-varying config committed to source control. (TF1)
- [ ] Processes hold no correctness-critical state beyond current request/job; state lives in a backing service. (TF3)

## High

- [ ] Dependencies fully declared with a lockfile; no reliance on pre-installed system packages. (TF2)
- [ ] Graceful shutdown (SIGTERM handling) implemented; startup time bounded and short. (TF6)
- [ ] Admin/one-off tasks run with the same codebase/config as the live app. (TF9)
- [ ] Logs written to stdout/stderr, not self-managed files. (TF8)

## Medium

- [ ] Dev environment uses the same backing-service type as production. (TF7)
- [ ] Scaling achieved via more processes, not heavier single processes. (TF5)
- [ ] Releases are immutable; config changes produce new releases. (TF10)

## Low

- [ ] App binds its own port rather than depending on runtime server injection. (TF4)
