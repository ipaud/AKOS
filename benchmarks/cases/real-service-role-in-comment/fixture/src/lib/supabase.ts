/**
 * Only the publishable (anon) key belongs here — it is bundled into the
 * browser and is safe to expose. RLS is what actually protects the data.
 * A service_role key or a Postgres connection string must NEVER be a
 * VITE_* variable.
 */
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY,
);
