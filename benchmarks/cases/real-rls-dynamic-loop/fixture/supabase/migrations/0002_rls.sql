-- Shape from a real production repository: RLS is enabled in a loop over an
-- explicit table array. Stronger than per-table DDL — a table added to the
-- list cannot be half-protected — and invisible to a scanner that only reads
-- literal ALTER TABLE statements.
create table clients (id uuid primary key, organization_id uuid not null);
create table contacts (id uuid primary key, organization_id uuid not null);

do $$
declare t text;
begin
  foreach t in array array['clients','contacts'] loop
    execute format('alter table %I enable row level security;', t);
  end loop;
end $$;
