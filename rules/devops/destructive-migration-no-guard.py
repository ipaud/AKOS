"""Detector for DESTRUCTIVE_MIGRATION_NO_GUARD.

Regex for DROP TABLE / DROP COLUMN / TRUNCATE TABLE not preceded within a
few lines by a guard comment (rollback/destructive/guard/reviewed — a
broader set of words than the generic `akos:allow` suppression the runner
already checks universally; this is a rule-specific, slightly more
permissive convention on top of that).
"""

from __future__ import annotations

import re
from pathlib import Path

DESTRUCTIVE_RE = re.compile(
    r"\b(DROP\s+TABLE|DROP\s+COLUMN|TRUNCATE\s+TABLE)\b",
    re.IGNORECASE,
)
GUARD_RE = re.compile(r"--.*\b(rollback|destructive|guard|reviewed|akos:allow)\b", re.IGNORECASE)


def has_adjacent_guard(lines: list[str], line_no: int) -> bool:
    """A guard comment must be immediately adjacent to count — the same
    line, or the nearest non-blank line above (skipping blank-line padding
    only, never reaching past unrelated preceding statements). A wider
    fixed-size window would let a guard comment for one statement suppress
    an unrelated one a few lines later — a real bug this method exists to
    avoid; caught by testing two destructive statements a few lines apart,
    only one of them guarded."""
    if GUARD_RE.search(lines[line_no - 1]):
        return True
    i = line_no - 2
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    return i >= 0 and bool(GUARD_RE.search(lines[i]))


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.split("\n")

        for m in DESTRUCTIVE_RE.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            if has_adjacent_guard(lines, line_no):
                continue
            findings.append({
                "evidence": [{"path": str(path), "line_start": line_no, "line_end": line_no,
                              "snippet": m.group(0)}],
            })
    return findings
