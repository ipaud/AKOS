"""Detector for PACK_EXPIRED.

Unlike the other detectors, this scans AKOS's OWN packs/ (target:
akos-packs in the registry — the runner always points this rule at
AKOS_HOME regardless of whatever --target-dir was passed on the CLI),
not a consuming project's source. Severity never exceeds MEDIUM — a stale
review date means "due for a look," not "actively wrong." Dual-wired into
doctor.sh directly (same detector, not a reimplementation) since this is
repo self-maintenance a maintainer should see during a routine health
check, not just when explicitly running `akos rules`.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402


def run(files: list[Path]) -> list[dict]:
    findings = []
    today = date.today()
    for path in files:
        try:
            data = yaml_subset.load(path)
        except yaml_subset.YamlSubsetError:
            continue
        review_after = data.get("review_after")
        if not review_after:
            continue  # not yet migrated — freshness.md covers "unknown" separately
        try:
            due = date.fromisoformat(review_after)
        except ValueError:
            continue
        if due >= today:
            continue
        pack_id = data.get("id", str(path.parent.relative_to(AKOS_HOME / "packs")))
        findings.append({
            "evidence": [{"path": str(path), "line_start": 1, "line_end": 1,
                          "snippet": f"{pack_id}: review_after {review_after} has passed ({(today - due).days} days overdue)"}],
        })
    return findings
