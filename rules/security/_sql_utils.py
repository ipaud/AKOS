"""Shared helpers for the SQL-scanning detectors. Not a rule itself — no
registry YAML, never discovered by the runner's glob.
"""

from __future__ import annotations

import re


def mask_sql_comments(text: str) -> str:
    """Replace comment characters with spaces of equal length, preserving
    byte offsets and line numbers, so line-number reporting stays accurate
    after masking. Handles `--` line comments and `/* */` block comments,
    respecting single-quoted string literals (so a `--` or `/*` inside a
    string value isn't mistaken for a comment start)."""
    out = []
    i = 0
    n = len(text)
    in_string = False
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == "'":
                if i + 1 < n and text[i + 1] == "'":
                    out.append(text[i + 1])
                    i += 2
                    continue
                in_string = False
            i += 1
            continue
        if c == "'":
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == "-" and i + 1 < n and text[i + 1] == "-":
            j = i
            while j < n and text[j] != "\n":
                out.append(" ")
                j += 1
            i = j
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            j = i
            while j < n - 1 and not (text[j] == "*" and text[j + 1] == "/"):
                out.append(" " if text[j] != "\n" else "\n")
                j += 1
            out.append("  ")
            i = j + 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def normalize_table_name(name: str) -> str:
    name = name.strip().strip('"')
    if "." in name:
        name = name.split(".")[-1]
    return name.lower()


TABLE_CREATE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?\"?(?:public\.)?\"?(\w+)\"?",
    re.IGNORECASE,
)
RLS_ENABLE_RE = re.compile(
    r"ALTER\s+TABLE\s+\"?(?:public\.)?\"?(\w+)\"?\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY",
    re.IGNORECASE,
)
