# Prompt Fragments — Supabase Pack

```text
Apply Supabase security practice (AKOS L2 — floor-level for any deployed
project): enable RLS on every table with user-scoped/sensitive data at
creation time; write explicit, auth.uid()-scoped policies for every
needed operation; never allow service_role key into client-shipped code
— use it only server-side (edge functions/API routes) with caller
identity validated first; test policies with multiple real authenticated
users, not just SQL inspection; storage buckets explicitly public/private
with matching access rules.
```
