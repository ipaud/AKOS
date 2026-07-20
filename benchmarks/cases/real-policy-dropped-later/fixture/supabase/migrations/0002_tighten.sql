-- The permissive insert policy was a mistake; only service_role writes here.
drop policy if exists "Cache writable" on cache;
revoke insert, update, delete on cache from authenticated, anon;
