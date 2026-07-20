-- The dynamic-loop fix must not become a blanket pass for any file that
-- contains such a loop: `forgotten` is created and never added to the array.
create table clients (id uuid primary key);
create table forgotten (id uuid primary key);

do $$
declare t text;
begin
  foreach t in array array['clients'] loop
    execute format('alter table %I enable row level security;', t);
  end loop;
end $$;
