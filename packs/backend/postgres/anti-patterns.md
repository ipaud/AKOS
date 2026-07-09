# Anti-Patterns — PostgreSQL Pack

- **Application-only referential integrity** — relying on app code to never insert an orphaned foreign key, instead of a DB constraint; eventually violated by a bug, a script, or a manual fix.
- **Index-everything** — adding an index to every column "just in case," bloating writes and storage with no corresponding read benefit.
- **Blocking migration on a hot table** — running `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT ...` on a large live table during peak traffic, causing a multi-minute lock and an outage.
- **SELECT \*** in application queries — fetching all columns including large/unneeded ones (blobs, rarely-used JSON), wasting bandwidth and cache.
- **N+1 from the ORM** — lazy-loaded relations triggering one query per row in a loop, invisible in the code but visible in query logs.
- **No EXPLAIN before "optimizing"** — guessing at performance fixes (adding random indexes, restructuring queries) without checking the actual execution plan first.
