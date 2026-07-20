"""Detector for SUPABASE_POLICY_TOO_PERMISSIVE.

Default severity is HIGH, not CRITICAL, deliberately: an always-true policy
is sometimes correct (a public lookup/reference table — plans, countries).
The suppression comment (`-- akos:allow SUPABASE_POLICY_TOO_PERMISSIVE`) is
the intended escape hatch for those legitimate cases, rather than an
exception list baked into the detector.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _sql_utils import mask_sql_comments, line_of_offset  # noqa: E402

POLICY_RE = re.compile(r"CREATE\s+POLICY\b", re.IGNORECASE)
ALWAYS_TRUE_RE = re.compile(r"(USING|WITH\s+CHECK)\s*\(\s*true\s*\)", re.IGNORECASE)


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        masked = mask_sql_comments(text)

        # Split on top-level ';' into statements, tracking each statement's
        # start offset in the original text so line numbers stay accurate.
        stmt_start = 0
        for m in re.finditer(r";", masked):
            stmt = masked[stmt_start : m.end()]
            if POLICY_RE.search(stmt):
                for clause_m in ALWAYS_TRUE_RE.finditer(stmt):
                    abs_offset = stmt_start + clause_m.start()
                    line = line_of_offset(text, abs_offset)
                    findings.append({
                        "evidence": [{
                            "path": str(path),
                            "line_start": line,
                            "line_end": line,
                            "snippet": clause_m.group(0),
                        }],
                    })
            stmt_start = m.end()
    return findings
