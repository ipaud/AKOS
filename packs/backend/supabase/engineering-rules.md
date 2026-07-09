# Engineering Rules — Supabase Pack

- SU1 ★. Every table with user-scoped or sensitive data has `ROW LEVEL SECURITY` enabled at creation time.
- SU2 ★. Explicit policies exist for SELECT/INSERT/UPDATE/DELETE as appropriate to the table's use — no table relies on "no policy means implicit access" as an intentional design (it means denial, but the intent should be explicit and documented).
- SU3 ★. `service_role` key is stored only in server-side environment variables (edge functions, server-side API routes), never in any client-shipped bundle or config.
- SU4. Policies reference `auth.uid()` (or equivalent) to scope rows to the requesting user; policies are not written as always-true placeholders "to make it work for now."
- SU5. RLS policies are tested with a script or test suite simulating multiple distinct authenticated users, not verified by inspection alone.
- SU6. Storage buckets are explicitly set public or private with a stated reason; private buckets have storage policies matching table-level RLS discipline.
- SU7. Edge functions used for service_role-requiring operations validate the caller's identity/authorization themselves (they don't inherit RLS automatically once using service_role).
- SU8. Auth session invalidation (logout, password change) is verified to actually revoke access, not just clear client-side state.
