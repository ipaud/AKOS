"""Detector for MIGRATION_NO_DOWN_FILE.

Supabase's own CLI-generated migrations are forward-only by default, with no
built-in up/down convention — flagging every migration in a project that
never adopted paired files would be 100% false positives, not signal. So:
first check whether the project's migrations directory contains ANY
*.down.sql (or a "-- Down" marker) at all; if none exist anywhere, this
returns zero findings — the project hasn't opted into the convention, and
there's nothing to check. Only once at least one paired file exists does it
flag *.up.sql / bare migration files lacking a counterpart.
"""

from __future__ import annotations

import re
from pathlib import Path

DOWN_MARKER_RE = re.compile(r"--\s*Down\b", re.IGNORECASE)


def is_down_file(path: Path, text: str) -> bool:
    name = path.name.lower()
    if ".down.sql" in name or name.endswith("_down.sql"):
        return True
    return bool(DOWN_MARKER_RE.search(text))


def expected_down_names(path: Path) -> list[str]:
    name = path.name
    candidates = []
    if name.endswith(".up.sql"):
        candidates.append(name[: -len(".up.sql")] + ".down.sql")
    elif name.endswith(".sql"):
        stem = name[: -len(".sql")]
        candidates.append(stem + ".down.sql")
        candidates.append(stem + "_down.sql")
    return candidates


def run(files: list[Path]) -> list[dict]:
    file_texts = {}
    for path in files:
        try:
            file_texts[path] = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            file_texts[path] = ""

    down_files = [p for p in files if is_down_file(p, file_texts[p])]
    if not down_files:
        return []  # project hasn't adopted the up/down convention — nothing to check

    findings = []
    for path in files:
        if path in down_files:
            continue
        siblings = {p.name for p in path.parent.iterdir()} if path.parent.exists() else set()
        if any(candidate in siblings for candidate in expected_down_names(path)):
            continue
        findings.append({
            "evidence": [{"path": str(path), "line_start": 1, "line_end": 1,
                          "snippet": f"no paired down-migration found for {path.name}"}],
        })
    return findings
