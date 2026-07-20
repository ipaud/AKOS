"""Detector for DESTRUCTIVE_MIGRATION_NO_GUARD.

Regex for DROP TABLE / DROP COLUMN / TRUNCATE TABLE not preceded within a
few lines by a guard comment (rollback/destructive/guard/reviewed — a
broader set of words than the generic `akos:allow` suppression the runner
already checks universally; this is a rule-specific, slightly more
permissive convention on top of that).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "security"))
from _sql_utils import mask_sql_comments  # noqa: E402

DESTRUCTIVE_RE = re.compile(
    r"\b(DROP\s+TABLE|DROP\s+COLUMN|TRUNCATE\s+TABLE)\b",
    re.IGNORECASE,
)
GUARD_RE = re.compile(r"--.*\b(rollback|destructive|guard|reviewed|akos:allow)\b", re.IGNORECASE)

# A DROP COLUMN whose data was copied elsewhere in the statement immediately
# above is guarded by the strongest thing available — the data still exists.
# Requiring a *comment* and nothing else reported exactly that shape as
# unguarded on the first real repository this ran against, where an
# `INSERT INTO tros_invites SELECT id, invite_code FROM trossos` preceded the
# `ALTER TABLE trossos DROP COLUMN invite_code`: expand-contract, done right.
DROP_COLUMN_RE = re.compile(
    r"ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?([\w$.\"]+)[\s\S]*?DROP\s+COLUMN\s+(?:IF\s+EXISTS\s+)?([\w$\"]+)",
    re.IGNORECASE)
PRESERVING_RE = re.compile(r"\bINSERT\s+INTO\b[\s\S]*\bSELECT\b", re.IGNORECASE)


def _bare(name: str) -> str:
    return name.strip().strip('"').split(".")[-1].lower()


def preceding_statement(text: str, offset: int) -> str:
    """The SQL statement ending immediately before `offset`."""
    before = text[:offset]
    end = before.rfind(";")
    if end == -1:
        return ""
    start = before.rfind(";", 0, end)
    return before[start + 1 : end + 1]


def containing_statement(text: str, offset: int) -> tuple[str, int]:
    """The statement containing `offset`, and its start offset."""
    start = text.rfind(";", 0, offset) + 1
    end = text.find(";", offset)
    return text[start : (end + 1 if end != -1 else len(text))], start


def data_was_preserved(text: str, m: re.Match) -> bool:
    """True when the statement just above copies the column being dropped."""
    # The match points at "DROP COLUMN", not at the "ALTER TABLE" that names
    # the table — so work from the whole statement, not from the match offset.
    stmt, stmt_start = containing_statement(text, m.start())
    dc = DROP_COLUMN_RE.search(stmt)
    if not dc:
        return False
    table, column = _bare(dc.group(1)), _bare(dc.group(2))
    prev = preceding_statement(text, stmt_start)
    if not PRESERVING_RE.search(prev):
        return False
    low = prev.lower()
    # Both the source table and the column have to appear, so an unrelated
    # INSERT above a DROP does not count as preserving anything.
    return table in low and column in low


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
        # Search the masked copy: a comment documenting a planned `drop column`
        # is a plan, not a statement. Its siblings mask; this one did not.
        # Offsets are preserved, so `lines` and the guard scan stay aligned.
        masked = mask_sql_comments(text)

        for m in DESTRUCTIVE_RE.finditer(masked):
            line_no = text.count("\n", 0, m.start()) + 1
            if has_adjacent_guard(lines, line_no):
                continue
            if data_was_preserved(text, m):
                continue
            findings.append({
                "evidence": [{"path": str(path), "line_start": line_no, "line_end": line_no,
                              "snippet": m.group(0)}],
            })
    return findings
