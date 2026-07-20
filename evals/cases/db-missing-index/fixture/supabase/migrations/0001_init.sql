create table public.budgets (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations,
  client_id uuid not null references public.clients,
  total numeric not null default 0,
  created_at timestamptz not null default now()
);

alter table public.budgets enable row level security;

create policy budgets_org on public.budgets
  for all to authenticated
  using (organization_id = auth_org_id());

-- Only client_id is indexed.
create index budgets_client_idx on public.budgets (client_id);
