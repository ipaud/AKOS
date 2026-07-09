# Examples — Clean Architecture Pack

## Repository interface owned by the core

```ts
// domain/orders/orderRepository.ts (core — interface)
export interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<void>;
}

// domain/orders/placeOrder.ts (core — use case, no framework imports)
export async function placeOrder(repo: OrderRepository, input: PlaceOrderInput): Promise<Order> {
  const order = Order.create(input); // business rules live in the entity
  await repo.save(order);
  return order;
}

// infra/orders/sqlOrderRepository.ts (outer ring — implementation)
export class SqlOrderRepository implements OrderRepository {
  constructor(private db: Database) {}
  async findById(id: string) { /* SQL here */ }
  async save(order: Order) { /* SQL here */ }
}

// main.ts (composition root)
const repo = new SqlOrderRepository(db);
app.post('/orders', (req, res) => placeOrder(repo, req.body).then(o => res.json(o)));
```

Testing `placeOrder` uses an in-memory fake `OrderRepository` — zero database, zero HTTP.

## When to skip the ring (decision-framework applied)

A settings page with one text field and one save button: a direct `settingsService.save(value)` calling the ORM is honest and correct at Prototype/MVP scale — no repository interface needed until a second persistence backend or a real business rule appears.

## Retrofitting incrementally

Legacy Express app with SQL inline in route handlers. Week 1: extract `calculateShippingCost` (real business rule) into a pure function, tested standalone; route handler now calls it. Week 2: repeat for the next entangled rule. No rewrite, continuous improvement.
