# Decision Framework — DDD Pack

## Full tactical DDD vs. simple CRUD

| Signal | Choice |
|--------|--------|
| Core subdomain, genuine business invariants, domain experts have strong opinions | Full tactical DDD (aggregates, value objects, events) |
| Supporting subdomain (settings, admin, notifications config) | Plain CRUD/service layer — skip tactical patterns |
| Generic subdomain available as a bought/OSS solution (auth, payments) | Buy/integrate; wrap with an anti-corruption layer, don't model it as core |
| Small team, early-stage product, domain still being discovered | Strategic DDD only (language, rough context boundaries); defer tactical patterns until the model stabilizes |

## Drawing bounded-context boundaries

1. List the distinct groups of domain experts/stakeholders and the vocabulary each uses.
2. Where the same word means genuinely different things to two groups, that's a context seam.
3. Where the same word means the same thing everywhere, that's inside one context.
4. Confirm with a context map: which contexts are upstream/downstream, where translation happens.
5. Service/deployment boundaries follow the context map — don't reverse this order.

## Aggregate boundary sizing

Start smaller than instinct suggests. Ask: what is the smallest set of objects that must be atomically consistent for this one invariant? That's the aggregate. Everything else references it by ID and accepts eventual consistency via domain events.

## When DDD is the wrong tool

Simple data-shuffling CRUD apps, admin tools, and thin API wrappers around a single table rarely have real domain complexity — strategic DDD's "shared language" habit is still free and useful; tactical DDD's ceremony is not worth paying for.
