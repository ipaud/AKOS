"""Detector for SUPABASE_RLS_DISABLED.

Scans ALL matched .sql files TOGETHER (not file-by-file) — a table is
commonly CREATE TABLE'd in one migration and RLS-enabled in a later one,
so per-file scanning would false-positive on that normal multi-migration
pattern. Known blind spot, stated rather than silently accepted: this only
covers raw SQL migrations (Supabase's own default). Dynamic SQL
ORM-DSL migrations (Prisma/Drizzle/knex) are false negatives by design.
Dynamic SQL that enables RLS in a loop over an array literal IS understood —
it was producing false positives, not the false negatives the original note
predicted. Dynamic SQL whose table list cannot be read still degrades to a
false negative, which is the correct direction for a gating rule.

Only tables in an API-exposed schema are considered — see API_EXPOSED_SCHEMAS
in _sql_utils. A second known gap, stated rather than hidden: a table in
`public` protected by `REVOKE ALL` rather than by RLS is still reported. That
is a rarer shape than the non-exposed-schema case and needs grant tracking to
resolve properly, so it is left as a suppression-comment case for now.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _sql_utils import (  # noqa: E402
    TABLE_CREATE_RE, RLS_ENABLE_RE, API_EXPOSED_SCHEMAS,
    mask_sql_comments, line_of_offset, normalize_table_name, schema_of,
    dynamically_rls_enabled_tables,
)


def run(files: list[Path]) -> list[dict]:
    created: dict[str, tuple[Path, int]] = {}
    rls_on: set[str] = set()

    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        masked = mask_sql_comments(text)

        for m in TABLE_CREATE_RE.finditer(masked):
            # RLS constrains access *through the API*. A table in a schema
            # PostgREST does not expose is not reachable that way, so a
            # missing policy is not a finding — and is frequently the
            # deliberate, stronger choice for secrets.
            if schema_of(m.group(1)) not in API_EXPOSED_SCHEMAS:
                continue
            table = normalize_table_name(m.group(1))
            if table not in created:
                created[table] = (path, line_of_offset(text, m.start()))

        for m in RLS_ENABLE_RE.finditer(masked):
            rls_on.add(normalize_table_name(m.group(1)))

        # RLS enabled through `execute format(...)` over an array literal —
        # see dynamically_rls_enabled_tables for why this counts.
        rls_on |= dynamically_rls_enabled_tables(masked)

    findings = []
    for table, (path, line) in sorted(created.items()):
        if table in rls_on:
            continue
        findings.append({
            "evidence": [{
                "path": str(path),
                "line_start": line,
                "line_end": line,
                "snippet": f"CREATE TABLE {table} — no ALTER TABLE {table} ENABLE ROW LEVEL SECURITY found in this scan",
            }],
        })
    return findings
