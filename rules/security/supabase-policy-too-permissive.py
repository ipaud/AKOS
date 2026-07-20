"""Detector for SUPABASE_POLICY_TOO_PERMISSIVE.

Default severity is HIGH, not CRITICAL, deliberately: an always-true policy
is sometimes correct (a public lookup/reference table — plans, countries).
The suppression comment (`-- akos:allow SUPABASE_POLICY_TOO_PERMISSIVE`) is
the intended escape hatch for those legitimate cases, rather than an
exception list baked into the detector.

Migration-order aware. A policy created in one migration and dropped in a
later one no longer exists, and reporting it is a false positive — which is
exactly what happened on the first real repository this ran against: two of
six findings named policies a later migration had already dropped, in a
project carrying 26 `DROP POLICY` statements. `SUPABASE_RLS_DISABLED`
already scanned all files together for the equivalent reason; this one did
not, and that asymmetry was the defect.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _sql_utils import mask_sql_comments, line_of_offset  # noqa: E402

ALWAYS_TRUE_RE = re.compile(r"(USING|WITH\s+CHECK)\s*\(\s*true\s*\)", re.IGNORECASE)

# Policy names may be double-quoted or bare; tables may be schema-qualified.
_NAME = r'(?:"([^"]+)"|([A-Za-z_][\w$]*))'
_TABLE = r'([A-Za-z_][\w$]*(?:\.[A-Za-z_][\w$]*)?)'
CREATE_POLICY_RE = re.compile(rf"CREATE\s+POLICY\s+{_NAME}\s+ON\s+{_TABLE}", re.IGNORECASE)
DROP_POLICY_RE = re.compile(
    rf"DROP\s+POLICY\s+(?:IF\s+EXISTS\s+)?{_NAME}\s+ON\s+{_TABLE}", re.IGNORECASE)


def _identity(m: re.Match) -> tuple[str, str]:
    """(policy name, table) — the pair Postgres treats as unique."""
    name = m.group(1) if m.group(1) is not None else m.group(2)
    return name, m.group(3).lower()


def run(files: list[Path]) -> list[dict]:
    # Migrations are timestamp-prefixed, so lexical order is apply order.
    # Walk every statement in that order and keep only the policies still
    # live at the end: a drop removes one, a later create brings it back.
    live: dict[tuple[str, str], dict] = {}

    for path in sorted(files):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        masked = mask_sql_comments(text)

        stmt_start = 0
        for m in re.finditer(r";", masked):
            stmt = masked[stmt_start : m.end()]

            drop_m = DROP_POLICY_RE.search(stmt)
            if drop_m:
                live.pop(_identity(drop_m), None)
                stmt_start = m.end()
                continue

            create_m = CREATE_POLICY_RE.search(stmt)
            if create_m:
                key = _identity(create_m)
                clause_m = ALWAYS_TRUE_RE.search(stmt)
                if clause_m:
                    abs_offset = stmt_start + clause_m.start()
                    live[key] = {
                        "evidence": [{
                            "path": str(path),
                            "line_start": line_of_offset(text, abs_offset),
                            "line_end": line_of_offset(text, abs_offset),
                            "snippet": clause_m.group(0),
                        }],
                    }
                else:
                    # Re-created without the always-true clause: whatever the
                    # earlier permissive version said no longer applies.
                    live.pop(key, None)

            stmt_start = m.end()

    return list(live.values())
