CREATE POLICY "public_read" ON plans -- akos:allow SUPABASE_POLICY_TOO_PERMISSIVE
  FOR SELECT
  USING (true);
