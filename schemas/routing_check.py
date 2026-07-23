#!/usr/bin/env python3
"""Draft-pack routing isolation: a pack's lifecycle status must have a real
operational consequence, not just be a label in metadata.yaml. This checks
that `skills/akos/SKILL.md`'s two routing sections agree with reality (every
stable pack is in the Stable catalog and nowhere in Experimental; every
draft pack is Experimental-only), and that no `status: stable` agent or
workflow depends on a draft pack.

Table membership is determined by LINE POSITION relative to the "###
Experimental" heading, not a whole-file substring search — SKILL.md has one
legitimate illustrative prose mention of a draft pack outside any table
("see `packs/ai-engineering/agent-security` for what one would look like"),
and a substring search would false-positive on it. Row-shaped lines
(a markdown table row naming a backtick-quoted domain/name pack id) are the
only thing counted as routing membership either way, which also excludes
that prose mention on its own (it isn't a table row).

Usage:
    python3 schemas/routing_check.py [--format text|json]

Exit codes (this command's own 0/1/2 convention, per docs/cli/exit-codes.md):
    0 - every stable/draft pack is where it should be
    1 - usage/setup error (SKILL.md or a pack directory not found)
    2 - a pack is misfiled, or a stable agent/workflow depends on a draft pack
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

PACK_ROW_RE = re.compile(r"^\|\s*`([a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*)`\s*\|")
EXPERIMENTAL_HEADING_RE = re.compile(r"^###\s+Experimental")
SUBSECTION_END_RE = re.compile(r"^##\s+")  # any top-level (##) heading ends the ### subsection
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
AGENT_PACK_LINK_RE = re.compile(r"\[([a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*)\]\(\.\./packs/")


def parse_skill_routing(skill_path: Path) -> tuple[set[str], set[str]]:
    """Returns (stable_ids, experimental_ids) — pack ids appearing as a table
    row in each section, bucketed by position relative to the Experimental
    heading, never by a whole-file text search."""
    lines = skill_path.read_text(encoding="utf-8").splitlines()
    stable_ids: set[str] = set()
    experimental_ids: set[str] = set()
    in_experimental = False
    for line in lines:
        if EXPERIMENTAL_HEADING_RE.match(line):
            in_experimental = True
            continue
        if in_experimental and SUBSECTION_END_RE.match(line):
            in_experimental = False
        m = PACK_ROW_RE.match(line)
        if not m:
            continue
        (experimental_ids if in_experimental else stable_ids).add(m.group(1))
    return stable_ids, experimental_ids


def load_pack_statuses(akos_home: Path) -> dict[str, str]:
    """{domain/name: status} for every non-personal pack."""
    statuses: dict[str, str] = {}
    for meta_path in sorted(akos_home.glob("packs/*/*/metadata.yaml")):
        if "personal" in meta_path.parts:
            continue
        domain, name = meta_path.parent.parent.name, meta_path.parent.name
        try:
            data = yaml_subset.load(meta_path)
        except yaml_subset.YamlSubsetError:
            data = {}
        status = data.get("status", "stable") if isinstance(data, dict) else "stable"
        statuses[f"{domain}/{name}"] = status
    return statuses


def load_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        data = yaml_subset.loads(m.group(1))
    except yaml_subset.YamlSubsetError:
        return {}
    return data if isinstance(data, dict) else {}


def agent_pack_ids(md_path: Path) -> set[str]:
    """Agent frontmatter has no `packs` field (per docs/contracts/agent.md) —
    packs are named as markdown links in the prose '## Packs to load'
    section instead. Extracts pack ids from links shaped like
    `[domain/name](../packs/domain/name/...)` within that section only."""
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"^##\s+Packs to load\s*$(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return set()
    return set(AGENT_PACK_LINK_RE.findall(m.group(1)))


def check_stable_routing(akos_home: Path | None = None) -> list[str]:
    """Returns human-readable error strings; empty means clean."""
    akos_home = akos_home or AKOS_HOME
    skill_path = akos_home / "skills" / "akos" / "SKILL.md"
    errors: list[str] = []

    statuses = load_pack_statuses(akos_home)
    stable_ids, experimental_ids = parse_skill_routing(skill_path)

    for pack_id, status in sorted(statuses.items()):
        if status == "stable":
            if pack_id not in stable_ids:
                errors.append(f"stable pack '{pack_id}' is missing from the Stable routing catalog in skills/akos/SKILL.md")
            if pack_id in experimental_ids:
                errors.append(f"stable pack '{pack_id}' incorrectly appears in the Experimental section too")
        elif status == "draft":
            if pack_id in stable_ids:
                errors.append(f"draft pack '{pack_id}' appears in the Stable routing catalog — must be Experimental-only")
            if pack_id not in experimental_ids:
                errors.append(f"draft pack '{pack_id}' is missing from the Experimental section in skills/akos/SKILL.md")

    for md_path in sorted((akos_home / "agents").glob("*.md")):
        fm = load_frontmatter(md_path)
        if fm.get("status", "stable") != "stable":
            continue
        for pack_id in agent_pack_ids(md_path):
            if statuses.get(pack_id) == "draft":
                errors.append(f"stable agent '{md_path.name}' depends on draft pack '{pack_id}'")

    for md_path in sorted((akos_home / "workflows").glob("*.md")):
        fm = load_frontmatter(md_path)
        if fm.get("status", "stable") != "stable":
            continue
        for pack_id in (fm.get("packs") or []):
            if statuses.get(pack_id) == "draft":
                errors.append(f"stable workflow '{md_path.name}' depends on draft pack '{pack_id}'")

    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    skill_path = AKOS_HOME / "skills" / "akos" / "SKILL.md"
    if not skill_path.is_file():
        print(f"error: {skill_path} not found", file=sys.stderr)
        return 1

    errors = check_stable_routing(AKOS_HOME)

    if args.format == "json":
        print(json.dumps({"errors": errors}, indent=2))
    else:
        for e in errors:
            print(f"\033[31m✗\033[0m {e}")
        if not errors:
            print("\033[32m✓\033[0m stable routing contains only stable packs; drafts are Experimental-only")
        else:
            print(f"\n{len(errors)} routing violation(s).")

    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
