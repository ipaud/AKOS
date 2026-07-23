#!/usr/bin/env python3
"""A micro JSON-Schema interpreter for AKOS's 3 contracts.

Implements only the keywords schemas/v1/{knowledge-pack,agent,workflow}.schema.json
actually use: type, required, properties, enum, pattern, format:date, items,
minLength, minimum, maximum, additionalProperties (enforced at every level a
schema declares it, not just the root), plus the AKOS-specific
x-akos-recommended (-> warning, never an error). This is deliberately not a
full JSON Schema engine — the schema files themselves stay standards-compliant
JSON Schema (any real `ajv`/`jsonschema` tool could validate against them
too), but AKOS's own tooling stays dependency-free rather than vendoring or
requiring the `jsonschema` package.

The current schema version for each contract kind is resolved through
schemas/registry.json, never a hardcoded path — see load_schema() below.

Usage:
    python3 schemas/validate.py [packs|agents|workflows|all] [--format text|json] [--strict]

Exit codes (this command's own convention — the 10 pre-existing `akos`
commands keep their unchanged 0/1 behavior):
    0 - clean (warnings allowed)
    1 - usage error
    2 - errors found (or, with --strict, warnings found)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

VALID_TARGETS = {"packs", "agents", "workflows", "all"}

REGISTRY_PATH = AKOS_HOME / "schemas" / "registry.json"
_TARGET_TO_KIND = {"packs": "knowledge-pack", "agents": "agent", "workflows": "workflow"}


def load_schema(kind: str) -> dict:
    """Resolve a schema's CURRENT version through the registry rather than a
    hardcoded path — the one place that knows "knowledge-pack means
    v1/knowledge-pack.schema.json today" so a future v2 is a registry edit,
    not a hunt through every call site."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    entry = registry["kinds"][kind]
    schema_path = AKOS_HOME / "schemas" / entry["schema_path"]
    return json.loads(schema_path.read_text(encoding="utf-8"))

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
AGENT_REQUIRED_HEADINGS = [
    "Purpose", "When to use", "Packs to load", "Review checklist",
    "Severity levels", "Scoring rubric", "Pre-report gate", "Refusal / limits", "Output format",
]

_TYPE_MAP = {
    "string": str, "integer": int, "number": (int, float),
    "boolean": bool, "array": list, "object": dict, "null": type(None),
}


# --- Micro JSON-Schema interpreter -------------------------------------------


def _check_type(value, types: list[str]) -> bool:
    for t in types:
        py_type = _TYPE_MAP.get(t)
        if py_type is None:
            continue
        if t == "integer" and isinstance(value, bool):
            continue  # bool is an int subclass in Python — exclude explicitly
        if isinstance(value, py_type):
            return True
    return False


def _validate_value(value, schema: dict, field_name: str) -> list[dict]:
    errors = []
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        if not _check_type(value, types):
            errors.append({"field": field_name, "message": f"value {value!r} is not type {t}", "rule": "type"})
            return errors

    if "enum" in schema and value not in schema["enum"]:
        errors.append({"field": field_name, "message": f"value {value!r} not in {schema['enum']}", "rule": "enum"})

    if "pattern" in schema and isinstance(value, str) and not re.match(schema["pattern"], value):
        errors.append({"field": field_name, "message": f"value {value!r} does not match pattern {schema['pattern']!r}", "rule": "pattern"})

    if schema.get("format") == "date" and isinstance(value, str):
        try:
            date.fromisoformat(value)
        except ValueError:
            errors.append({"field": field_name, "message": f"value {value!r} is not a valid ISO date (YYYY-MM-DD)", "rule": "format:date"})

    if "minLength" in schema and isinstance(value, str) and len(value) < schema["minLength"]:
        errors.append({"field": field_name, "message": f"length {len(value)} is below minLength {schema['minLength']}", "rule": "minLength"})

    # bool is a subclass of int in Python; exclude it so `true` is not range-checked as 1.
    is_number = isinstance(value, (int, float)) and not isinstance(value, bool)

    if "minimum" in schema and is_number and value < schema["minimum"]:
        errors.append({"field": field_name, "message": f"value {value!r} is below minimum {schema['minimum']}", "rule": "minimum"})

    if "maximum" in schema and is_number and value > schema["maximum"]:
        errors.append({"field": field_name, "message": f"value {value!r} is above maximum {schema['maximum']}", "rule": "maximum"})

    if isinstance(value, dict) and "properties" in schema:
        nested_errors, _ = validate_instance(value, schema)
        for e in nested_errors:
            e = dict(e)
            e["field"] = f"{field_name}.{e['field']}"
            errors.append(e)

    if isinstance(value, list) and "items" in schema:
        item_schema = schema["items"]
        for idx, item in enumerate(value):
            if isinstance(item, dict) and item_schema.get("type") == "object":
                sub_errors, _ = validate_instance(item, item_schema)
                for e in sub_errors:
                    e = dict(e)
                    e["field"] = f"{field_name}[{idx}].{e['field']}"
                    errors.append(e)
            else:
                errors.extend(_validate_value(item, item_schema, f"{field_name}[{idx}]"))

    return errors


def validate_instance(instance, schema: dict) -> tuple[list[dict], list[dict]]:
    """Return (errors, warnings) for one parsed YAML/frontmatter document."""
    errors: list[dict] = []
    warnings: list[dict] = []

    if schema.get("type") == "object" and not isinstance(instance, dict):
        errors.append({"field": "<root>", "message": f"expected object, got {type(instance).__name__}", "rule": "type"})
        return errors, warnings

    for req in schema.get("required", []):
        if req not in instance:
            errors.append({"field": req, "message": "required field is missing", "rule": "required"})

    for rec in schema.get("x-akos-recommended", []):
        if rec not in instance:
            warnings.append({"field": rec, "message": "recommended field missing", "rule": "x-akos-recommended"})

    properties = schema.get("properties", {})
    additional_allowed = schema.get("additionalProperties", True)
    for key, value in instance.items():
        prop_schema = properties.get(key)
        if prop_schema is None:
            if additional_allowed is False:
                errors.append({
                    "field": key,
                    "message": f"unknown property {key!r} is not declared in the schema (additionalProperties: false)",
                    "rule": "additionalProperties",
                })
            continue
        errors.extend(_validate_value(value, prop_schema, key))

    return errors, warnings


# --- Per-target file walks ----------------------------------------------------


def _check_pack_semantics(data: dict, meta_path: Path) -> list[dict]:
    """Cross-field checks the generic schema interpreter can't express (it
    only ever sees the parsed instance, never the file's own path) — a typo'd
    domain/name/id must not pass just because each field is independently
    well-typed, and a pack marked deprecated without saying what replaces it
    leaves nothing for a reader steered here to actually reach for."""
    errors: list[dict] = []
    dir_name = meta_path.parent.name
    dir_domain = meta_path.parent.parent.name

    if "domain" in data and data["domain"] != dir_domain:
        errors.append({
            "field": "domain",
            "message": f"domain {data['domain']!r} does not match the directory it lives under ({dir_domain!r})",
            "rule": "path-consistency",
        })
    if "name" in data and data["name"] != dir_name:
        errors.append({
            "field": "name",
            "message": f"name {data['name']!r} does not match its directory name ({dir_name!r})",
            "rule": "path-consistency",
        })
    if "id" in data:
        expected_id = f"{dir_domain}/{dir_name}"
        if data["id"] != expected_id:
            errors.append({
                "field": "id",
                "message": f"id {data['id']!r} does not match domain/name ({expected_id!r})",
                "rule": "path-consistency",
            })
    if data.get("deprecated") is True and not data.get("replacement"):
        errors.append({
            "field": "replacement",
            "message": "deprecated: true requires a replacement pack id — a deprecated pack must say what replaces it",
            "rule": "deprecated-requires-replacement",
        })
    return errors


def check_packs(schema: dict) -> list[dict]:
    results = []
    for meta_path in sorted((AKOS_HOME / "packs").glob("*/*/metadata.yaml")):
        if "personal" in meta_path.parts:
            continue
        rel = str(meta_path.relative_to(AKOS_HOME))
        try:
            data = yaml_subset.load(meta_path)
        except yaml_subset.YamlSubsetError as e:
            results.append({"file": rel, "errors": [{"field": "<parse>", "message": str(e), "rule": "parse"}], "warnings": []})
            continue
        errors, warnings = validate_instance(data, schema)
        if isinstance(data, dict):
            errors.extend(_check_pack_semantics(data, meta_path))
        results.append({"file": rel, "errors": errors, "warnings": warnings})
    return results


def check_agents(schema: dict) -> list[dict]:
    results = []
    for md_path in sorted((AKOS_HOME / "agents").glob("*.md")):
        rel = str(md_path.relative_to(AKOS_HOME))
        text = md_path.read_text(encoding="utf-8")
        errors: list[dict] = []
        warnings: list[dict] = []

        m = FRONTMATTER_RE.match(text)
        if not m:
            errors.append({"field": "<frontmatter>", "message": "no YAML frontmatter block found", "rule": "structure"})
        else:
            try:
                data = yaml_subset.loads(m.group(1))
            except yaml_subset.YamlSubsetError as e:
                errors.append({"field": "<frontmatter>", "message": str(e), "rule": "parse"})
                data = {}
            fm_errors, fm_warnings = validate_instance(data, schema)
            errors.extend(fm_errors)
            warnings.extend(fm_warnings)

        for heading in AGENT_REQUIRED_HEADINGS:
            if f"## {heading}" not in text:
                warnings.append({"field": f"section:{heading}", "message": f"canonical heading '## {heading}' not found", "rule": "heading-presence"})

        results.append({"file": rel, "errors": errors, "warnings": warnings})
    return results


def check_workflows(schema: dict) -> list[dict]:
    results = []
    for md_path in sorted((AKOS_HOME / "workflows").glob("*.md")):
        rel = str(md_path.relative_to(AKOS_HOME))
        text = md_path.read_text(encoding="utf-8")
        errors: list[dict] = []
        warnings: list[dict] = []

        m = FRONTMATTER_RE.match(text)
        if m:
            try:
                data = yaml_subset.loads(m.group(1))
                fm_errors, fm_warnings = validate_instance(data, schema)
                errors.extend(fm_errors)
                warnings.extend(fm_warnings)
            except yaml_subset.YamlSubsetError as e:
                errors.append({"field": "<frontmatter>", "message": str(e), "rule": "parse"})
        else:
            # schema_version 1 requires frontmatter to be present — a
            # workflow with none is now an error, not an informational skip.
            # (Pre-v1, no workflow had ever claimed to carry frontmatter, so
            # this was a valid no-op; all 9 real workflows carry it now.)
            errors.append({"field": "<frontmatter>", "message": "no YAML frontmatter block found — schema_version 1 requires it", "rule": "structure"})

        results.append({"file": rel, "errors": errors, "warnings": warnings})
    return results


# --- CLI ----------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="validate.py", description=__doc__)
    ap.add_argument("targets", nargs="*", help="packs, agents, workflows, or all (default: all)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures too")
    args = ap.parse_args(argv)

    targets = set(args.targets) or {"all"}
    bad = targets - VALID_TARGETS
    if bad:
        print(f"error: unknown target(s): {', '.join(sorted(bad))}. Valid: packs, agents, workflows, all", file=sys.stderr)
        return 1
    if "all" in targets:
        targets = {"packs", "agents", "workflows"}

    all_results: list[dict] = []
    if "packs" in targets:
        all_results += check_packs(load_schema(_TARGET_TO_KIND["packs"]))
    if "agents" in targets:
        all_results += check_agents(load_schema(_TARGET_TO_KIND["agents"]))
    if "workflows" in targets:
        all_results += check_workflows(load_schema(_TARGET_TO_KIND["workflows"]))

    total_errors = sum(len(r["errors"]) for r in all_results)
    total_warnings = sum(len(r["warnings"]) for r in all_results)

    if args.format == "json":
        print(json.dumps(all_results, indent=2))
    else:
        c_green, c_yellow, c_red, c_reset, c_bold = "\033[32m", "\033[33m", "\033[31m", "\033[0m", "\033[1m"
        for r in all_results:
            for e in r["errors"]:
                print(f"{c_red}✗{c_reset} {r['file']}: {e['field']} — {e['message']}")
            for w in r["warnings"]:
                print(f"{c_yellow}!{c_reset} {r['file']}: {w['field']} — {w['message']}")
        clean = sum(1 for r in all_results if not r["errors"] and not r["warnings"])
        print(
            f"\n{c_bold}Summary{c_reset}  {c_green}✓ {clean} clean{c_reset}  "
            f"{c_yellow}! {total_warnings} warnings{c_reset}  {c_red}✗ {total_errors} errors{c_reset}  "
            f"({len(all_results)} files checked)"
        )

    if total_errors > 0:
        return 2
    if args.strict and total_warnings > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
