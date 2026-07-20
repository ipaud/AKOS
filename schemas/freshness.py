#!/usr/bin/env python3
"""Reports the review-freshness band of every AKOS pack, from metadata.yaml's
`review_after` field. The core check (past due or not) is the same logic
`rules/meta/pack-expired.py` uses for the executable-rule/CRITICAL-adjacent
path; this command reports the full spectrum, not just the expired band, and
never gates the exit code unless --fail-on asks it to.

Usage:
    python3 schemas/freshness.py [--expired] [--due-soon] [--pack DOMAIN/NAME]
                                 [--format text|json] [--fail-on BAND]

Bands: fresh, review-due-soon (within 90 days), review-due (within 30 days),
expired (past due), unknown (no review_after field — not yet migrated).

Exit codes: 0 normally. With --fail-on BAND, exits 2 if any pack is at that
band or worse (unknown < expired < review-due < review-due-soon < fresh is
the severity order, worst first). 1 on setup error.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

DUE_SOON_DAYS = 90
DUE_DAYS = 30

BAND_ORDER = ["fresh", "review-due-soon", "review-due", "expired", "unknown"]
# Lower number = worse. fresh=0 (best) ... unknown=4 (worst) would invert the
# "at least as bad as X" comparison below; define it the other way instead:
# higher number = worse, so "at least as bad as X" is a simple >= threshold.
BAND_SEVERITY = {b: i for i, b in enumerate(BAND_ORDER)}  # fresh=0 (best) ... unknown=4 (worst)


def band_for(review_after: str | None, today: date) -> tuple[str, int | None]:
    if not review_after:
        return "unknown", None
    try:
        due = date.fromisoformat(review_after)
    except ValueError:
        return "unknown", None
    delta = (due - today).days
    if delta < 0:
        return "expired", delta
    if delta <= DUE_DAYS:
        return "review-due", delta
    if delta <= DUE_SOON_DAYS:
        return "review-due-soon", delta
    return "fresh", delta


def collect(pack_filter: str | None) -> list[dict]:
    today = date.today()
    rows = []
    for meta_path in sorted((AKOS_HOME / "packs").glob("*/*/metadata.yaml")):
        if "personal" in meta_path.parts:
            continue
        rel = str(meta_path.parent.relative_to(AKOS_HOME / "packs"))
        if pack_filter and rel != pack_filter:
            continue
        try:
            data = yaml_subset.load(meta_path)
        except yaml_subset.YamlSubsetError:
            data = {}
        band, delta_days = band_for(data.get("review_after"), today)
        rows.append({
            "pack": data.get("id", rel),
            "band": band,
            "review_after": data.get("review_after"),
            "days": delta_days,
        })
    return rows


def print_text(rows: list[dict]):
    c_green, c_yellow, c_red, c_reset, c_bold = "\033[32m", "\033[33m", "\033[31m", "\033[0m", "\033[1m"
    glyph = {"fresh": f"{c_green}✓{c_reset}", "review-due-soon": f"{c_yellow}!{c_reset}",
             "review-due": f"{c_yellow}!{c_reset}", "expired": f"{c_red}✗{c_reset}", "unknown": "?"}
    counts = {b: 0 for b in BAND_ORDER}
    for r in sorted(rows, key=lambda r: BAND_SEVERITY[r["band"]], reverse=True):
        counts[r["band"]] += 1
        detail = f"review_after {r['review_after']}" if r["review_after"] else "no review_after set"
        if r["days"] is not None and r["band"] in ("expired", "review-due", "review-due-soon"):
            detail += f" ({abs(r['days'])} days {'overdue' if r['days'] < 0 else 'remaining'})"
        print(f"{glyph[r['band']]} {r['pack']:<40} {r['band']:<16} {detail}")
    print(f"\n{c_bold}Summary{c_reset}  " + "  ".join(f"{b}: {counts[b]}" for b in BAND_ORDER))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expired", action="store_true", help="Only show expired packs")
    ap.add_argument("--due-soon", action="store_true", help="Only show review-due-soon and worse")
    ap.add_argument("--pack", help="Only this pack, e.g. ux/wcag")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--fail-on", choices=BAND_ORDER, help="Exit 2 if any pack is at this band or worse")
    args = ap.parse_args(argv)

    rows = collect(args.pack)
    # A --pack that matches nothing must not read as "this pack is fine".
    # `--pack no/such --fail-on expired` used to exit 0 unconditionally,
    # which turns a typo in a CI invocation into a gate that never fires.
    if args.pack and not rows:
        print(f"error: no pack matches '{args.pack}'. List them with 'akos list-packs'.",
              file=sys.stderr)
        return 1

    if args.expired:
        rows = [r for r in rows if r["band"] == "expired"]
    elif args.due_soon:
        rows = [r for r in rows if BAND_SEVERITY[r["band"]] >= BAND_SEVERITY["review-due-soon"]]

    if args.format == "json":
        import json
        print(json.dumps(rows, indent=2))
    else:
        print_text(rows)

    if args.fail_on:
        threshold = BAND_SEVERITY[args.fail_on]
        if any(BAND_SEVERITY[r["band"]] >= threshold for r in rows):
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
