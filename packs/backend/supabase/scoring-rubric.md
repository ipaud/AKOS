# Scoring Rubric — Supabase Pack

| Finding | Deduction |
|---------|-----------|
| RLS disabled on a table with user/sensitive data (deployed) | −40 (CRITICAL) |
| service_role key present in client-shipped code | −40 (CRITICAL) |
| Always-true or missing policy on a sensitive table | −25 (CRITICAL) |
| Policies untested with real multi-user scenarios | −10 (HIGH) |
| Public bucket holding private content | −15 (HIGH) |
| Edge function using service_role without caller validation | −15 (HIGH) |
| Session not actually revoked on logout | −6 (MEDIUM) |

Hard cap: any CRITICAL finding → score ≤59 (Blocked), matching [core scoring model](../../../core/scoring-model.md).

Anchors: 95 RLS-complete, tested, no key leakage · 80 solid with a documentation gap · 65 RLS present but untested · ≤59 RLS gap or key leakage — BLOCKED for any deployed project.
