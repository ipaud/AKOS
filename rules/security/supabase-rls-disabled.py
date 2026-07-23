"""Detector for SUPABASE_RLS_DISABLED.

Raw SQL files are folded in lexical migration and statement order. The final
state wins: a later DISABLE, DROP/CREATE, or GRANT can undo an earlier secure
state. Dynamic RLS loops count only when their table array is explicit.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from io_utils import read_text_file  # noqa: E402
from _sql_utils import (  # noqa: E402
    API_ROLES,
    ALL_TABLE_PRIVILEGES,
    GRANT_ALL_TABLES_IN_SCHEMA_RE,
    GRANT_RE,
    REVOKE_ALL_TABLES_IN_SCHEMA_RE,
    REVOKE_RE,
    RLS_DISABLE_RE,
    RLS_ENABLE_RE,
    TABLE_CREATE_IF_NOT_EXISTS_RE,
    TABLE_CREATE_RE,
    TABLE_DROP_RE,
    api_exposed_schemas,
    dynamically_rls_enabled_tables,
    iter_sql_statements,
    line_of_offset,
    normalize_table_name,
    relation_names,
    schema_names,
    schema_of,
    sql_privileges,
    sql_roles,
)

API_DATA_PRIVILEGES = frozenset({"delete", "insert", "select", "update"})


class TableState(NamedTuple):
    create_path: Path
    create_line: int
    rls_enabled: bool = False
    revoked_all_roles: frozenset[str] = frozenset()
    granted_privileges: frozenset[tuple[str, str]] = frozenset()

    @property
    def api_locked(self) -> bool:
        granted_roles = {
            role
            for role, privilege in self.granted_privileges
            if privilege in API_DATA_PRIVILEGES
        }
        return all(
            role in self.revoked_all_roles and role not in granted_roles
            for role in API_ROLES
        )


def _updated(
    states: dict[str, TableState],
    table: str,
    **changes,
) -> dict[str, TableState]:
    current = states.get(table)
    if current is None:
        return states
    return {**states, table: current._replace(**changes)}


def _revoke(
    states: dict[str, TableState],
    tables: tuple[str, ...],
    roles: frozenset[str],
    privileges: frozenset[str],
) -> dict[str, TableState]:
    revoke_all = privileges == ALL_TABLE_PRIVILEGES
    result = states
    for table in tables:
        current = result.get(table)
        if current is None:
            continue
        result = {
            **result,
            table: current._replace(
                revoked_all_roles=(
                    current.revoked_all_roles | roles
                    if revoke_all
                    else current.revoked_all_roles
                ),
                granted_privileges=frozenset(
                    (role, privilege)
                    for role, privilege in current.granted_privileges
                    if role not in roles
                    or (not revoke_all and privilege not in privileges)
                ),
            ),
        }
    return result


def _grant(
    states: dict[str, TableState],
    tables: tuple[str, ...],
    roles: frozenset[str],
    privileges: frozenset[str],
) -> dict[str, TableState]:
    additions = frozenset(
        (role, privilege)
        for role in roles
        for privilege in privileges
    )
    result = states
    for table in tables:
        current = result.get(table)
        if current is not None:
            result = {
                **result,
                table: current._replace(
                    granted_privileges=current.granted_privileges | additions,
                ),
            }
    return result


def _tables_in_schemas(
    states: dict[str, TableState],
    schemas: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        table for table in states if schema_of(table) in schemas
    )


def run(files: list[Path], scan_root: Path | None = None) -> list[dict]:
    exposed_schemas = api_exposed_schemas(scan_root)
    states: dict[str, TableState] = {}

    for path in sorted(files):
        if path.suffix.lower() != ".sql":
            continue
        text = read_text_file(path)

        for statement_offset, statement in iter_sql_statements(text):
            create = TABLE_CREATE_RE.search(statement)
            if create:
                raw_table = create.group(1)
                table = normalize_table_name(raw_table)
                if schema_of(raw_table) in exposed_schemas:
                    if not (
                        TABLE_CREATE_IF_NOT_EXISTS_RE.search(statement)
                        and table in states
                    ):
                        states = {
                            **states,
                            table: TableState(
                                create_path=path,
                                create_line=line_of_offset(
                                    text, statement_offset + create.start(1)
                                ),
                            ),
                        }
                continue

            drop = TABLE_DROP_RE.search(statement)
            if drop:
                dropped = set(relation_names(drop.group(1)))
                states = {
                    name: state
                    for name, state in states.items()
                    if name not in dropped
                }
                continue

            enable = RLS_ENABLE_RE.search(statement)
            if enable:
                states = _updated(
                    states,
                    normalize_table_name(enable.group(1)),
                    rls_enabled=True,
                )
                continue

            disable = RLS_DISABLE_RE.search(statement)
            if disable:
                states = _updated(
                    states,
                    normalize_table_name(disable.group(1)),
                    rls_enabled=False,
                )
                continue

            dynamically_enabled = dynamically_rls_enabled_tables(statement)
            if dynamically_enabled:
                states = {
                    name: (
                        state._replace(rls_enabled=True)
                        if name in dynamically_enabled
                        else state
                    )
                    for name, state in states.items()
                }
                continue

            revoke = (
                REVOKE_ALL_TABLES_IN_SCHEMA_RE.search(statement)
                or REVOKE_RE.search(statement)
            )
            if revoke:
                privileges = sql_privileges(revoke.group(1))
                if REVOKE_ALL_TABLES_IN_SCHEMA_RE.fullmatch(statement):
                    revoked_tables = _tables_in_schemas(
                        states, schema_names(revoke.group(2))
                    )
                else:
                    revoked_tables = relation_names(revoke.group(2))
                roles = sql_roles(revoke.group(3))
                states = _revoke(
                    states, revoked_tables, roles, privileges
                )
                continue

            grant = (
                GRANT_ALL_TABLES_IN_SCHEMA_RE.search(statement)
                or GRANT_RE.search(statement)
            )
            if grant:
                privileges = sql_privileges(grant.group(1))
                if GRANT_ALL_TABLES_IN_SCHEMA_RE.fullmatch(statement):
                    granted_tables = _tables_in_schemas(
                        states, schema_names(grant.group(2))
                    )
                else:
                    granted_tables = relation_names(grant.group(2))
                roles = sql_roles(grant.group(3))
                states = _grant(
                    states, granted_tables, roles, privileges
                )

    findings = []
    for table, state in sorted(states.items()):
        if state.rls_enabled or state.api_locked:
            continue
        findings.append({
            "evidence": [{
                "path": str(state.create_path),
                "line_start": state.create_line,
                "line_end": state.create_line,
                "snippet": (
                    f"CREATE TABLE {table} — no ALTER TABLE {table} "
                    "ENABLE ROW LEVEL SECURITY found in this scan"
                ),
            }],
        })
    return findings
