"""Shared helpers for the SQL-scanning detectors.

This module deliberately implements only a small lexical SQL layer. It keeps
statement order and source offsets without pretending to be a PostgreSQL
parser; detector state machines build on top of these primitives.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from io_utils import read_regular_text_file  # noqa: E402


_DOLLAR_TAG_RE = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*)?\$")
_IDENT_PART = r'(?:"(?:[^"]|"")+"|[A-Za-z_][\w$]*)'
_QUALIFIED_NAME = rf"{_IDENT_PART}(?:\s*\.\s*{_IDENT_PART})?"
_QUALIFIED = rf"({_QUALIFIED_NAME})"
_RELATION_LIST = rf"({_QUALIFIED_NAME}(?:\s*,\s*{_QUALIFIED_NAME})*)"
_SCHEMA_LIST = rf"({_IDENT_PART}(?:\s*,\s*{_IDENT_PART})*)"


def _dollar_tag_at(text: str, offset: int) -> str | None:
    match = _DOLLAR_TAG_RE.match(text, offset)
    return match.group(0) if match else None


def _backslash_escapes_at(text: str, quote_offset: int) -> bool:
    """Whether a quote starts PostgreSQL E'...' or U&'...' syntax."""
    prefix_start = quote_offset
    if quote_offset >= 1 and text[quote_offset - 1] in "Ee":
        prefix_start = quote_offset - 1
    elif quote_offset >= 2 and text[quote_offset - 2:quote_offset].lower() == "u&":
        prefix_start = quote_offset - 2
    else:
        return False
    return (
        prefix_start == 0
        or not (
            text[prefix_start - 1].isalnum()
            or text[prefix_start - 1] in "_$"
        )
    )


def mask_sql_comments(text: str) -> str:
    """Mask SQL comments while preserving offsets and line numbers.

    Line and block comment markers inside single-quoted strings,
    double-quoted identifiers, and dollar-quoted bodies remain data.
    """
    out: list[str] = []
    i = 0
    in_single = False
    backslash_escapes = False
    in_double = False
    dollar_tag: str | None = None

    while i < len(text):
        if dollar_tag is not None:
            if text.startswith(dollar_tag, i):
                out.append(dollar_tag)
                i += len(dollar_tag)
                dollar_tag = None
            else:
                out.append(text[i])
                i += 1
            continue

        char = text[i]
        if in_single:
            out.append(char)
            if backslash_escapes and char == "\\" and i + 1 < len(text):
                out.append(text[i + 1])
                i += 2
                continue
            if char == "'":
                if i + 1 < len(text) and text[i + 1] == "'":
                    out.append(text[i + 1])
                    i += 2
                    continue
                in_single = False
                backslash_escapes = False
            i += 1
            continue

        if in_double:
            out.append(char)
            if char == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    out.append(text[i + 1])
                    i += 2
                    continue
                in_double = False
            i += 1
            continue

        tag = _dollar_tag_at(text, i)
        if tag is not None:
            out.append(tag)
            i += len(tag)
            dollar_tag = tag
            continue
        if char == "'":
            in_single = True
            backslash_escapes = _backslash_escapes_at(text, i)
            out.append(char)
            i += 1
            continue
        if char == '"':
            in_double = True
            out.append(char)
            i += 1
            continue
        if text.startswith("--", i):
            while i < len(text) and text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if text.startswith("/*", i):
            while i < len(text):
                if text.startswith("*/", i):
                    out.append("  ")
                    i += 2
                    break
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            continue
        out.append(char)
        i += 1

    return "".join(out)


def iter_sql_statements(text: str):
    """Yield ``(offset, masked_statement)`` including a final unterminated one."""
    masked = mask_sql_comments(text)
    start = 0
    i = 0
    in_single = False
    backslash_escapes = False
    in_double = False
    dollar_tag: str | None = None

    while i < len(masked):
        if dollar_tag is not None:
            if masked.startswith(dollar_tag, i):
                i += len(dollar_tag)
                dollar_tag = None
            else:
                i += 1
            continue

        char = masked[i]
        if in_single:
            if backslash_escapes and char == "\\" and i + 1 < len(masked):
                i += 2
                continue
            if char == "'":
                if i + 1 < len(masked) and masked[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
                backslash_escapes = False
            i += 1
            continue
        if in_double:
            if char == '"':
                if i + 1 < len(masked) and masked[i + 1] == '"':
                    i += 2
                    continue
                in_double = False
            i += 1
            continue

        tag = _dollar_tag_at(masked, i)
        if tag is not None:
            dollar_tag = tag
            i += len(tag)
            continue
        if char == "'":
            in_single = True
            backslash_escapes = _backslash_escapes_at(masked, i)
        elif char == '"':
            in_double = True
        elif char == ";":
            end = i + 1
            statement = masked[start:end]
            if statement.strip():
                yield start, statement
            start = end
        i += 1

    statement = masked[start:]
    if statement.strip():
        yield start, statement


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _identifier_parts(name: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_double = False
    i = 0
    while i < len(name):
        char = name[i]
        if char == '"':
            current.append(char)
            if in_double and i + 1 < len(name) and name[i + 1] == '"':
                current.append(name[i + 1])
                i += 2
                continue
            in_double = not in_double
        elif char == "." and not in_double:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    parts.append("".join(current).strip())
    return parts


def _canonical_identifier(part: str) -> str:
    part = part.strip()
    if part.startswith('"') and part.endswith('"'):
        value = part[1:-1].replace('""', '"')
    else:
        value = part
    if re.fullmatch(r"[a-z_][a-z0-9_$]*", value):
        return value
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_$]*", value) and not part.startswith('"'):
        return value.lower()
    return '"' + value.replace('"', '""') + '"'


def normalize_table_name(name: str) -> str:
    """Return a schema-qualified PostgreSQL relation identity."""
    parts = [_canonical_identifier(part) for part in _identifier_parts(name)]
    if len(parts) == 1:
        parts.insert(0, "public")
    return ".".join(parts)


def relation_names(raw_names: str) -> tuple[str, ...]:
    """Normalize a comma-separated list of relation names."""
    return tuple(
        normalize_table_name(match.group(0))
        for match in re.finditer(_QUALIFIED_NAME, raw_names)
    )


def schema_names(raw_names: str) -> tuple[str, ...]:
    """Normalize a comma-separated list of schema identifiers."""
    return tuple(
        _canonical_identifier(match.group(0))
        for match in re.finditer(_IDENT_PART, raw_names)
    )


def schema_of(name: str) -> str:
    """Return the schema component, with ``public`` for unqualified names."""
    parts = [_canonical_identifier(part) for part in _identifier_parts(name)]
    return parts[0] if len(parts) > 1 else "public"


def api_exposed_schemas(scan_root: Path | None) -> set[str]:
    """Read Supabase's local ``api.schemas`` with a safe public fallback."""
    schemas = {"public"}
    if scan_root is None:
        return schemas
    config_path = Path(scan_root) / "supabase" / "config.toml"
    if not config_path.exists() and not config_path.is_symlink():
        return schemas
    config = read_regular_text_file(config_path)

    api_section = re.search(
        r"(?ms)^\s*\[api\]\s*$([\s\S]*?)(?=^\s*\[[^\]]+\]\s*$|\Z)",
        config,
    )
    if not api_section:
        return schemas
    declared = re.search(
        r"(?ms)^\s*schemas\s*=\s*\[(.*?)\]",
        api_section.group(1),
    )
    if not declared:
        return schemas
    for double, single in re.findall(r'"((?:[^"\\]|\\.)*)"|\'([^\']*)\'', declared.group(1)):
        value = double or single
        if value:
            schemas.add(_canonical_identifier(value))
    return schemas


TABLE_CREATE_RE = re.compile(
    rf"^\s*CREATE\s+(?:UNLOGGED\s+)?TABLE\s+"
    rf"(?:IF\s+NOT\s+EXISTS\s+)?{_QUALIFIED}",
    re.IGNORECASE,
)
TABLE_CREATE_IF_NOT_EXISTS_RE = re.compile(
    r"^\s*CREATE\s+(?:UNLOGGED\s+)?TABLE\s+IF\s+NOT\s+EXISTS\b",
    re.IGNORECASE,
)
TABLE_DROP_RE = re.compile(
    rf"^\s*DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?{_RELATION_LIST}"
    r"(?:\s+(?:CASCADE|RESTRICT))?\s*;?\s*$",
    re.IGNORECASE,
)
RLS_ENABLE_RE = re.compile(
    rf"^\s*ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?{_QUALIFIED}"
    r"\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY\b",
    re.IGNORECASE,
)
RLS_DISABLE_RE = re.compile(
    rf"^\s*ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?{_QUALIFIED}"
    r"\s+DISABLE\s+ROW\s+LEVEL\s+SECURITY\b",
    re.IGNORECASE,
)


FOREACH_ARRAY_LOOP_RE = re.compile(
    r"\bFOREACH\s+([A-Za-z_][\w$]*)\s+IN\s+ARRAY\s+"
    r"ARRAY\s*\[(.*?)\]\s+LOOP\b(.*?)\bEND\s+LOOP\b",
    re.IGNORECASE | re.DOTALL,
)
RLS_FORMAT_VARIABLE_RE = re.compile(
    r"\bEXECUTE\s+FORMAT\s*\(\s*"
    r"'(?:''|[^'])*?\bALTER\s+TABLE\s+"
    r"(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?"
    r"(?:[A-Za-z_][\w$]*\s*\.\s*)?%I\s+"
    r"ENABLE\s+ROW\s+LEVEL\s+SECURITY\b(?:''|[^'])*'"
    r"\s*,\s*([A-Za-z_][\w$]*)\s*\)",
    re.IGNORECASE | re.DOTALL,
)
QUOTED_IDENT_RE = re.compile(r"'([A-Za-z_][\w$]*)'")
EXPLICIT_IDENT_ARRAY_RE = re.compile(
    r"\s*'[A-Za-z_][\w$]*'"
    r"(?:\s*,\s*'[A-Za-z_][\w$]*')*\s*",
    re.IGNORECASE | re.DOTALL,
)


def dynamically_rls_enabled_tables(masked_sql: str) -> set[str]:
    """Return tables linked to the variable of an explicit dynamic RLS loop.

    The FOREACH variable must be the sole value argument to the RLS format
    call. Ambiguous arrays and expressions fail safe rather than suppressing
    real CRITICAL findings.
    """
    enabled: set[str] = set()
    for loop in FOREACH_ARRAY_LOOP_RE.finditer(masked_sql):
        variable, raw_array, body = loop.groups()
        if not EXPLICIT_IDENT_ARRAY_RE.fullmatch(raw_array):
            continue
        format_variables = {
            match.group(1).lower()
            for match in RLS_FORMAT_VARIABLE_RE.finditer(body)
        }
        if format_variables != {variable.lower()}:
            continue
        enabled.update(
            normalize_table_name(name)
            for name in QUOTED_IDENT_RE.findall(raw_array)
        )
    return enabled


REVOKE_RE = re.compile(
    rf"^\s*REVOKE\s+(.+?)\s+ON\s+(?:TABLE\s+)?{_RELATION_LIST}"
    r"\s+FROM\s+(.+?)(?:\s+(?:CASCADE|RESTRICT))?\s*;?\s*$",
    re.IGNORECASE | re.DOTALL,
)
GRANT_RE = re.compile(
    rf"^\s*GRANT\s+(.+?)\s+ON\s+(?:TABLE\s+)?{_RELATION_LIST}"
    r"\s+TO\s+(.+?)(?:\s+WITH\s+GRANT\s+OPTION)?\s*;?\s*$",
    re.IGNORECASE | re.DOTALL,
)
REVOKE_ALL_TABLES_IN_SCHEMA_RE = re.compile(
    rf"^\s*REVOKE\s+(.+?)\s+ON\s+ALL\s+TABLES\s+IN\s+SCHEMA\s+"
    rf"{_SCHEMA_LIST}\s+FROM\s+(.+?)"
    r"(?:\s+(?:CASCADE|RESTRICT))?\s*;?\s*$",
    re.IGNORECASE | re.DOTALL,
)
GRANT_ALL_TABLES_IN_SCHEMA_RE = re.compile(
    rf"^\s*GRANT\s+(.+?)\s+ON\s+ALL\s+TABLES\s+IN\s+SCHEMA\s+"
    rf"{_SCHEMA_LIST}\s+TO\s+(.+?)"
    r"(?:\s+WITH\s+GRANT\s+OPTION)?\s*;?\s*$",
    re.IGNORECASE | re.DOTALL,
)
API_ROLES = frozenset({"anon", "authenticated", "public"})
ALL_TABLE_PRIVILEGES = frozenset({
    "delete",
    "insert",
    "maintain",
    "references",
    "select",
    "trigger",
    "truncate",
    "update",
})


def sql_roles(raw_roles: str) -> frozenset[str]:
    return frozenset(
        _canonical_identifier(role.strip())
        for role in raw_roles.split(",")
        if role.strip()
    )


def sql_privileges(raw_privileges: str) -> frozenset[str]:
    privileges = {
        re.sub(r"\s*\([^)]*\)\s*$", "", privilege.strip()).lower()
        for privilege in raw_privileges.split(",")
        if privilege.strip()
    }
    if "all" in privileges or "all privileges" in privileges:
        return ALL_TABLE_PRIVILEGES
    return frozenset(privileges)


def revoke_all_locked_tables(masked_sql: str) -> set[str]:
    """Compatibility helper for complete REVOKE-only snippets."""
    locked: dict[str, frozenset[str]] = {}
    for _, statement in iter_sql_statements(masked_sql):
        match = REVOKE_RE.search(statement)
        if not match or sql_privileges(match.group(1)) != ALL_TABLE_PRIVILEGES:
            continue
        roles = sql_roles(match.group(3))
        for table in relation_names(match.group(2)):
            locked[table] = locked.get(table, frozenset()) | roles
    return {table for table, roles in locked.items() if API_ROLES <= roles}
