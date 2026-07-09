# Examples — Supabase Pack

## RLS enabled + scoped policy

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own invoices"
  ON invoices FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own invoices"
  ON invoices FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

## Testing as two users

```ts
// as user A
const { data: aData } = await supabaseAsUserA.from('invoices').select();
// as user B
const { data: bData } = await supabaseAsUserB.from('invoices').select();
// assert: aData never contains B's rows and vice versa
```

## Edge function validating caller before service_role use

```ts
// supabase/functions/admin-refund/index.ts
const { data: { user } } = await supabaseClient.auth.getUser(req.headers.get('Authorization'));
if (!user || !(await isAdmin(user.id))) return new Response('Forbidden', { status: 403 });
// only now use the service_role client for the privileged operation
```

## Private storage with signed URL

```ts
const { data } = await supabase.storage.from('documents').createSignedUrl(path, 60); // 60s expiry
```
