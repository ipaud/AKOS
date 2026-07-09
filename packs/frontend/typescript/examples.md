# Examples — TypeScript Pack

## Discriminated union over boolean soup

Bad: `{ isLoading: boolean; isError: boolean; data?: T; error?: string }`
Good:

```ts
type State<T> =
  | { status: 'loading' }
  | { status: 'error'; error: string }
  | { status: 'success'; data: T };
```

## Schema validation at the boundary

```ts
const UserSchema = z.object({ id: z.string().uuid(), email: z.string().email() });
const user = UserSchema.parse(await response.json()); // typed AND validated
```

## Branded type for ID safety

```ts
type UserId = string & { __brand: 'UserId' };
type OrderId = string & { __brand: 'OrderId' };
function getUser(id: UserId) { /* ... */ }
// getUser(orderId) // compile error - can't accidentally swap IDs
```
