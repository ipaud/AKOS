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
    return name.strip('"').lower()


def schema_of(name: str) -> str:
    """Schema part of a possibly-qualified name; 'public' when unqualified."""
    name = name.strip().strip('"')
    return name.split(".")[0].strip('"').lower() if "." in name else "public"


# Schemas PostgREST exposes by default. RLS is what constrains access through
# the API, so a table outside these is not reachable that way and does not
# need a policy — protecting it with REVOKE, or simply by not exposing the
# schema, is a valid and often stronger choice.
#
# The previous pattern only stripped a literal `public.` prefix, so
# `CREATE TABLE IF NOT EXISTS private.app_secrets` matched the table name as
# `private`. On the first real repository this ran against, that produced a
# CRITICAL against a secrets table that was in a non-exposed schema *and*
# carried `REVOKE ALL ... FROM PUBLIC, anon, authenticated, service_role` —
# stronger than the RLS it was accused of lacking.
API_EXPOSED_SCHEMAS = {"public"}

_QUALIFIED = r'("?[\w$]+"?(?:\."?[\w$]+"?)?)'
TABLE_CREATE_RE = re.compile(
    rf"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?{_QUALIFIED}",
    re.IGNORECASE,
)
RLS_ENABLE_RE = re.compile(
    rf"ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?{_QUALIFIED}\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY",
    re.IGNORECASE,
)
