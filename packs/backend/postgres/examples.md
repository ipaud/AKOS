# Examples — PostgreSQL Pack

## Safe NOT NULL migration on a large table

Bad: `ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';` (blocking rewrite on large tables in older Postgres versions, or blocking on any volatile default).
Good:

```sql
ALTER TABLE orders ADD COLUMN status TEXT; -- fast, nullable
UPDATE orders SET status = 'pending' WHERE status IS NULL; -- backfill in batches
ALTER TABLE orders ALTER COLUMN status SET NOT NULL; -- constrain after backfill
```

## Foreign key + index

```sql
ALTER TABLE orders ADD CONSTRAINT fk_orders_customer
  FOREIGN KEY (customer_id) REFERENCES customers(id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id); -- FK columns need an index too
```

## Partial index

```sql
CREATE INDEX idx_active_orders ON orders(created_at) WHERE deleted_at IS NULL;
```

## EXPLAIN ANALYZE diagnosis

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;
-- Seq Scan on orders (cost=0.00..1200.00 rows=1 ...) → missing index, add one
```
