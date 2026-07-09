# Anti-Patterns — Supabase Pack

## RLS disabled "for now"

A table created without RLS "to get the demo working," deployed to production still without it — every row in the table is readable/writable by anyone with the (publicly-shipped) anon key. The single most common and most severe Supabase-specific vulnerability.

## service_role key in client code

The service_role key (which bypasses RLS entirely) pasted into a frontend env var or mobile app config — equivalent to shipping database admin credentials to every user.

## Always-true policy

`CREATE POLICY "allow all" ON table FOR SELECT USING (true);` written to "make the RLS error go away" without actually implementing the intended scoping — RLS is technically enabled but provides zero protection.

## Untested policies

Policies written and reviewed by reading the SQL, never actually tested by querying as two different authenticated users — a subtle bug (wrong column compared, missing `auth.uid()` check) ships undetected.

## Public bucket by accident

A storage bucket created as public because that was the quickest path past a permissions error, holding user-private documents reachable by anyone with the URL.

## Client-side business logic bypassing RLS intent

A feature route that needs elevated access uses the service_role key directly in a Next.js API route without validating the calling user's identity/permission first — the edge function/API route becomes the new unguarded door.
