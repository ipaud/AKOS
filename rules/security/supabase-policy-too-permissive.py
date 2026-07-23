"""Detector for SUPABASE_POLICY_TOO_PERMISSIVE.

Policy definitions are folded in lexical migration and statement order.
CREATE, ALTER, RENAME, DROP, and table removal all affect final state; a
trailing statement without a semicolon is processed as well.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from io_utils import read_text_file  # noqa: E402
from _sql_utils import (  # noqa: E402
    TABLE_DROP_RE,
    _dollar_tag_at,
    iter_sql_statements,
    line_of_offset,
    normalize_table_name,
    relation_names,
)


_IDENT = r'(?:"(?:[^"]|"")+"|[A-Za-z_][\w$]*)'
_TABLE = rf"({_IDENT}(?:\s*\.\s*{_IDENT})?)"
_POLICY = rf"({_IDENT})"

CREATE_POLICY_RE = re.compile(
    rf"^\s*CREATE\s+POLICY\s+{_POLICY}\s+ON\s+{_TABLE}(?=\s|;|$)",
    re.IGNORECASE,
)
ALTER_POLICY_RE = re.compile(
    rf"^\s*ALTER\s+POLICY\s+{_POLICY}\s+ON\s+{_TABLE}(?=\s|;|$)",
    re.IGNORECASE,
)
DROP_POLICY_RE = re.compile(
    rf"^\s*DROP\s+POLICY\s+(?:IF\s+EXISTS\s+)?{_POLICY}\s+ON\s+"
    rf"{_TABLE}(?=\s|;|$)",
    re.IGNORECASE,
)
RENAME_POLICY_RE = re.compile(
    rf"^\s*ALTER\s+POLICY\s+{_POLICY}\s+ON\s+{_TABLE}"
    rf"\s+RENAME\s+TO\s+{_POLICY}(?=\s|;|$)",
    re.IGNORECASE,
)

USING_RE = re.compile(r"\bUSING\s*\(", re.IGNORECASE)
WITH_CHECK_RE = re.compile(r"\bWITH\s+CHECK\s*\(", re.IGNORECASE)
TAUTOLOGY_RE = re.compile(r"(?:true|1\s*=\s*1)", re.IGNORECASE)
FALSE_RE = re.compile(r"(?:false|0\s*=\s*1|1\s*=\s*0)", re.IGNORECASE)

ALWAYS_FALSE = -1
UNKNOWN = 0
ALWAYS_TRUE = 1


class PolicyState(NamedTuple):
    using_finding: dict | None = None
    check_finding: dict | None = None

    @property
    def finding(self) -> dict | None:
        return self.using_finding or self.check_finding


def _policy_name(raw_name: str) -> str:
    raw_name = raw_name.strip()
    if raw_name.startswith('"') and raw_name.endswith('"'):
        value = raw_name[1:-1].replace('""', '"')
        if re.fullmatch(r"[a-z_][a-z0-9_$]*", value):
            return value
        return '"' + value.replace('"', '""') + '"'
    return raw_name.lower()


def _identity(match: re.Match) -> tuple[str, str]:
    return _policy_name(match.group(1)), normalize_table_name(match.group(2))


def _closing_parenthesis(text: str, opening_offset: int) -> int | None:
    depth = 0
    in_single = False
    in_double = False
    dollar_tag: str | None = None
    i = opening_offset
    while i < len(text):
        if dollar_tag is not None:
            if text.startswith(dollar_tag, i):
                i += len(dollar_tag)
                dollar_tag = None
            else:
                i += 1
            continue
        char = text[i]
        if in_single:
            if char == "'" and i + 1 < len(text) and text[i + 1] == "'":
                i += 2
                continue
            if char == "'":
                in_single = False
        elif in_double:
            if char == '"' and i + 1 < len(text) and text[i + 1] == '"':
                i += 2
                continue
            if char == '"':
                in_double = False
        else:
            tag = _dollar_tag_at(text, i)
            if tag is not None:
                dollar_tag = tag
                i += len(tag)
                continue
            if char == "'":
                in_single = True
            elif char == '"':
                in_double = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return None


def _without_redundant_parentheses(expression: str) -> str:
    value = expression.strip()
    while value.startswith("("):
        closing = _closing_parenthesis(value, 0)
        if closing != len(value) - 1:
            break
        value = value[1:-1].strip()
    return value


def _is_word_at(text: str, offset: int, word: str) -> bool:
    end = offset + len(word)
    if text[offset:end].lower() != word.lower():
        return False
    before = text[offset - 1] if offset else ""
    after = text[end] if end < len(text) else ""
    return not (
        (before and (before.isalnum() or before in "_$"))
        or (after and (after.isalnum() or after in "_$"))
    )


def _split_top_level(expression: str, operator: str) -> tuple[str, ...]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_single = False
    in_double = False
    dollar_tag: str | None = None
    i = 0
    while i < len(expression):
        if dollar_tag is not None:
            if expression.startswith(dollar_tag, i):
                i += len(dollar_tag)
                dollar_tag = None
            else:
                i += 1
            continue
        char = expression[i]
        if in_single:
            if char == "'" and i + 1 < len(expression) and expression[i + 1] == "'":
                i += 2
                continue
            if char == "'":
                in_single = False
        elif in_double:
            if char == '"' and i + 1 < len(expression) and expression[i + 1] == '"':
                i += 2
                continue
            if char == '"':
                in_double = False
        else:
            tag = _dollar_tag_at(expression, i)
            if tag is not None:
                dollar_tag = tag
                i += len(tag)
                continue
            if char == "'":
                in_single = True
            elif char == '"':
                in_double = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif depth == 0 and _is_word_at(expression, i, operator):
                parts.append(expression[start:i])
                i += len(operator)
                start = i
                continue
        i += 1
    if not parts:
        return (expression,)
    return (*parts, expression[start:])


def _boolean_value(expression: str, recursion_depth: int = 0) -> int:
    if recursion_depth > 64:
        return UNKNOWN
    value = _without_redundant_parentheses(expression)

    disjuncts = _split_top_level(value, "OR")
    if len(disjuncts) > 1:
        if any(not part.strip() for part in disjuncts):
            return UNKNOWN
        values = tuple(
            _boolean_value(part, recursion_depth + 1)
            for part in disjuncts
        )
        if ALWAYS_TRUE in values:
            return ALWAYS_TRUE
        return (
            ALWAYS_FALSE
            if all(item == ALWAYS_FALSE for item in values)
            else UNKNOWN
        )

    conjuncts = _split_top_level(value, "AND")
    if len(conjuncts) > 1:
        if any(not part.strip() for part in conjuncts):
            return UNKNOWN
        values = tuple(
            _boolean_value(part, recursion_depth + 1)
            for part in conjuncts
        )
        if ALWAYS_FALSE in values:
            return ALWAYS_FALSE
        return (
            ALWAYS_TRUE
            if all(item == ALWAYS_TRUE for item in values)
            else UNKNOWN
        )

    negated = re.match(r"(?is)^NOT\b(.*)$", value)
    if negated:
        inner = _boolean_value(negated.group(1), recursion_depth + 1)
        return -inner
    if TAUTOLOGY_RE.fullmatch(value):
        return ALWAYS_TRUE
    if FALSE_RE.fullmatch(value):
        return ALWAYS_FALSE
    return UNKNOWN


def _tautology_span(
    statement: str,
    clause_pattern: re.Pattern,
) -> tuple[int, int] | None:
    clause = clause_pattern.search(statement)
    if clause is None:
        return None
    opening_offset = clause.end() - 1
    closing_offset = _closing_parenthesis(statement, opening_offset)
    if closing_offset is None:
        return None
    expression = statement[opening_offset + 1:closing_offset]
    if _boolean_value(expression) != ALWAYS_TRUE:
        return None
    return clause.start(), closing_offset + 1


def _tautology_finding(
    path: Path,
    source_text: str,
    statement_offset: int,
    statement: str,
    clause_pattern: re.Pattern,
) -> dict | None:
    span = _tautology_span(statement, clause_pattern)
    if span is None:
        return None
    start, end = span
    absolute_offset = statement_offset + start
    return {
        "evidence": [{
            "path": str(path),
            "line_start": line_of_offset(source_text, absolute_offset),
            "line_end": line_of_offset(source_text, absolute_offset),
            "snippet": statement[start:end],
        }],
    }


def run(files: list[Path]) -> list[dict]:
    policies: dict[tuple[str, str], PolicyState] = {}

    for path in sorted(files):
        text = read_text_file(path)

        for statement_offset, statement in iter_sql_statements(text):
            drop_table = TABLE_DROP_RE.search(statement)
            if drop_table:
                dropped_tables = set(relation_names(drop_table.group(1)))
                policies = {
                    key: state
                    for key, state in policies.items()
                    if key[1] not in dropped_tables
                }
                continue

            drop_policy = DROP_POLICY_RE.search(statement)
            if drop_policy:
                key = _identity(drop_policy)
                policies = {
                    existing: state
                    for existing, state in policies.items()
                    if existing != key
                }
                continue

            rename = RENAME_POLICY_RE.search(statement)
            if rename:
                old_key = _identity(rename)
                new_key = (_policy_name(rename.group(3)), old_key[1])
                current = policies.get(old_key)
                if current is not None:
                    policies = {
                        **{
                            key: state
                            for key, state in policies.items()
                            if key != old_key
                        },
                        new_key: current,
                    }
                continue

            create = CREATE_POLICY_RE.search(statement)
            if create:
                policies = {
                    **policies,
                    _identity(create): PolicyState(
                        using_finding=_tautology_finding(
                            path,
                            text,
                            statement_offset,
                            statement,
                            USING_RE,
                        ),
                        check_finding=_tautology_finding(
                            path,
                            text,
                            statement_offset,
                            statement,
                            WITH_CHECK_RE,
                        ),
                    ),
                }
                continue

            alter = ALTER_POLICY_RE.search(statement)
            if alter:
                key = _identity(alter)
                current = policies.get(key, PolicyState())
                policies = {
                    **policies,
                    key: current._replace(
                        using_finding=(
                            _tautology_finding(
                                path,
                                text,
                                statement_offset,
                                statement,
                                USING_RE,
                            )
                            if USING_RE.search(statement)
                            else current.using_finding
                        ),
                        check_finding=(
                            _tautology_finding(
                                path,
                                text,
                                statement_offset,
                                statement,
                                WITH_CHECK_RE,
                            )
                            if WITH_CHECK_RE.search(statement)
                            else current.check_finding
                        ),
                    ),
                }

    return [
        finding
        for state in policies.values()
        if (finding := state.finding) is not None
    ]
