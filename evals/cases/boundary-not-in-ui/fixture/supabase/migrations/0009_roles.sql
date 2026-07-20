-- The boundary the UI layer refers to. Same six capabilities, enforced where
-- a request cannot route around them.
alter table public.budgets enable row level security;

create policy budgets_financials on public.budgets
  for select to authenticated
  using (
    exists (
      select 1 from public.profiles p
      where p.id = auth.uid()
        and p.role in ('owner', 'admin')
    )
  );
