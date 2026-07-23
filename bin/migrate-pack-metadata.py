#!/usr/bin/env python3
"""Idempotent, additive migration of packs/*/*/metadata.yaml to the extended
schema in schemas/v1/knowledge-pack.schema.json.

Never rewrites an existing line — only appends brand-new top-level keys at
EOF, so a hand-reviewed 48-file corpus doesn't get a noisy reformatting diff.
Explicitly skips packs/personal/* (it has no metadata.yaml by design).

Safe by default: without --apply, this only prints what WOULD change. Run
with --apply to actually write. Re-running is a no-op for any pack that
already has all the fields (idempotent).

Usage:
    python3 bin/migrate-pack-metadata.py [--apply] [--pack DOMAIN/NAME]
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset as y  # noqa: E402

CANONICAL_ORDER = ["schema_version", "id", "status", "last_reviewed", "review_after", "maintainer", "license", "deprecated"]
CADENCE_DAYS = {0: 545, 1: 545, 2: 365, 3: 270, 4: 270}  # 18mo / 18mo / 12mo / 9mo / 9mo

# Matches "## [1.0.0] — 2026-07-09" — the em-dash is literal in all 49 real
# CHANGELOG.md files; a plain-hyphen-only regex would silently match none of
# them. Accept a plain hyphen too, as a documented, lower-priority fallback.
CHANGELOG_DATE_RE = re.compile(r"^##\s*\[.+?\]\s*[—-]\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)


def top_level_keys(text: str) -> set[str]:
    """Cheap presence check — column-0 'key:' lines only, no full parse needed
    just to know which keys already exist."""
    return set(re.findall(r"(?m)^([A-Za-z_][\w-]*):", text))


def parse_changelog_date(changelog_path: Path) -> tuple[date, str]:
    if not changelog_path.exists():
        return date.today(), "fallback (no CHANGELOG.md found)"
    text = changelog_path.read_text(encoding="utf-8")
    m = CHANGELOG_DATE_RE.search(text)
    if not m:
        return date.today(), "fallback (no dated '## [x.y.z] — YYYY-MM-DD' entry found)"
    try:
        return date.fromisoformat(m.group(1)), "CHANGELOG.md"
    except ValueError:
        return date.today(), f"fallback (unparseable date '{m.group(1)}' in CHANGELOG.md)"


def build_missing_block(meta_path: Path, missing: list[str]) -> tuple[str, dict[str, str]]:
    data = y.load(meta_path)
    name = data.get("name", meta_path.parent.name)
    domain = data.get("domain", meta_path.parent.parent.name)
    authority = data.get("authority-level", 3)
    if not isinstance(authority, int):
        authority = 3

    last_reviewed, source = parse_changelog_date(meta_path.parent / "CHANGELOG.md")
    review_after = last_reviewed + timedelta(days=CADENCE_DAYS.get(authority, 365))

    values = {
        "schema_version": "1",
        "id": f"{domain}/{name}",
        "status": "stable",
        "last_reviewed": last_reviewed.isoformat(),
        "review_after": review_after.isoformat(),
        "maintainer": "core",
        "license": "MIT",
        "deprecated": "false",
    }
    lines = "".join(f"{k}: {values[k]}\n" for k in CANONICAL_ORDER if k in missing)
    return lines, {"date_source": source}


def atomic_append(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text + block, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes. Without this flag, dry-run only.")
    parser.add_argument("--pack", help="Only migrate one pack, e.g. ux/steve-krug")
    args = parser.parse_args()

    if args.pack:
        targets = [AKOS_HOME / "packs" / args.pack / "metadata.yaml"]
    else:
        targets = sorted((AKOS_HOME / "packs").glob("*/*/metadata.yaml"))

    skipped_personal = 0
    migrated = 0
    already_ok = 0
    warned_dates = 0

    for meta_path in targets:
        if "personal" in meta_path.parts:
            skipped_personal += 1
            continue
        if not meta_path.exists():
            print(f"MISSING: {meta_path}")
            continue

        text = meta_path.read_text(encoding="utf-8")
        existing = top_level_keys(text)
        missing = [k for k in CANONICAL_ORDER if k not in existing]

        rel = meta_path.relative_to(AKOS_HOME)
        if not missing:
            already_ok += 1
            continue

        block, info = build_missing_block(meta_path, missing)
        if info["date_source"].startswith("fallback"):
            warned_dates += 1
            print(f"WARN  {rel}: {info['date_source']}")

        if args.apply:
            atomic_append(meta_path, block)
            print(f"MIGRATED {rel}: added {missing} (last_reviewed source: {info['date_source']})")
        else:
            print(f"WOULD ADD to {rel}: {missing}")
            print("  " + block.replace("\n", "\n  ").rstrip())
        migrated += 1

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"\n[{mode}] migrated={migrated} already_ok={already_ok} "
          f"skipped_personal={skipped_personal} date_fallback_warnings={warned_dates}")
    if not args.apply and migrated:
        print("Re-run with --apply to write these changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
