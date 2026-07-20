-- The permissive insert policy was a mistake; only service_role writes here.
DROP POLICY IF EXISTS "Cache writable" ON public.cache;
REVOKE INSERT, UPDATE, DELETE ON public.cache FROM authenticated, anon;
