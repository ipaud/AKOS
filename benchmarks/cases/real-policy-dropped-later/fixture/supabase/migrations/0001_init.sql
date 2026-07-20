create table cache (id uuid primary key, data jsonb not null);
alter table cache enable row level security;
create policy "Cache writable" on cache
  for insert to authenticated with check (true);
