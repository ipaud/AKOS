# Philosophy — PostgreSQL Pack

The database is where correctness guarantees are cheapest to enforce and most expensive to retrofit — a constraint (foreign key, unique, check) written once in the schema prevents an entire class of bugs application code would otherwise need to defensively re-check everywhere, forever. Indexes are a deliberate tradeoff (write cost for read speed) that must match actual query patterns, not be added reflexively; an unindexed hot query and an over-indexed write-heavy table are both real, opposite failure modes this pack navigates between.
