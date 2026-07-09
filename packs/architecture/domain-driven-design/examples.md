# Examples — DDD Pack

## Value object vs. primitive

Bad: `function createUser(email: string) { if (!email.includes('@')) throw ... }` repeated in five call sites with slightly different regexes.
Good: `class EmailAddress { constructor(value: string) { /* validated once */ } }` — used everywhere, validated once, immutable.

## Aggregate boundary

`Order` aggregate root owns `OrderLine[]` (must stay consistent: totals, stock reservation) but references `Customer` and `Product` only by ID — those are separate aggregates with their own consistency rules.

```ts
class Order {
  private lines: OrderLine[] = [];
  addLine(productId: ProductId, qty: number) {
    // invariant enforced here: stock check, max-lines check
  }
}
```

## Domain event

```ts
class OrderPlaced {
  constructor(readonly orderId: string, readonly placedAt: Date) {}
}
// Order aggregate emits OrderPlaced; a separate handler in the Fulfillment
// context reacts to it — no direct call from Order into Fulfillment code.
```

## Bounded context translation (anti-corruption layer)

```ts
// Legacy ERP returns { cust_no, cust_nm, bal_due }
function translateLegacyCustomer(erp: LegacyErpCustomer): Customer {
  return new Customer(new CustomerId(erp.cust_no), erp.cust_nm, Money.fromCents(erp.bal_due));
}
```

## Skipping tactical DDD appropriately

An internal "feature flags" admin panel: flags are simple key/value rows, no invariants beyond uniqueness. Plain CRUD service + repository, no aggregate/value-object ceremony — correctly scoped per DD9.
