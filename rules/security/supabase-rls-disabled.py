"""Detector for SUPABASE_RLS_DISABLED.

Scans ALL matched .sql files TOGETHER (not file-by-file) — a table is
commonly CREATE TABLE'd in one migration and RLS-enabled in a later one,
so per-file scanning would false-positive on that normal multi-migration
pattern. Known blind spot, stated rather than silently accepted: this only
covers raw SQL migrations (Supabase's own default). Dynamic SQL
(EXECUTE format(...)) and ORM-DSL migrations (Prisma/Drizzle/knex) are
false negatives by design.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _sql_utils import TABLE_CREATE_RE, RLS_ENABLE_RE, mask_sql_comments, line_of_offset, normalize_table_name  # noqa: E402


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
            table = normalize_table_name(m.group(1))
            if table not in created:
                created[table] = (path, line_of_offset(text, m.start()))

        for m in RLS_ENABLE_RE.finditer(masked):
            rls_on.add(normalize_table_name(m.group(1)))

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
