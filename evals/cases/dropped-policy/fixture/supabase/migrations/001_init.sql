CREATE TABLE public.cache (id uuid PRIMARY KEY, data jsonb NOT NULL);
ALTER TABLE public.cache ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Cache writable" ON public.cache
  FOR INSERT TO authenticated WITH CHECK (true);

CREATE TABLE public.audit_log (id uuid PRIMARY KEY, actor uuid, action text);
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Audit readable by anyone" ON public.audit_log
  FOR SELECT TO authenticated USING (true);
