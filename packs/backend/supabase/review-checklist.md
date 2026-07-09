# Review Checklist — Supabase Pack

Floor items (★) block beyond pure local Prototype.

## Critical ★
- [ ] RLS enabled on every table with user-scoped/sensitive data. (SU1)
- [ ] Explicit, correctly-scoped policies for every operation the table needs. (SU2)
- [ ] service_role key never present in client-shipped code. (SU3)

## High
- [ ] Policies reference `auth.uid()`/real scoping, not always-true placeholders. (SU4)
- [ ] Policies tested with multiple real authenticated identities. (SU5)
- [ ] Storage buckets explicitly public/private with matching policies. (SU6)

## Medium
- [ ] Edge functions using service_role validate caller identity themselves. (SU7)
- [ ] Logout/password-change actually revokes server-side session. (SU8)
