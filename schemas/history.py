#!/usr/bin/env python3
"""Review history — records and compares AKOS review runs in a CONSUMING
project's `.akos/reviews/`, not in the AKOS repo itself (the same locality
as `.akos/config.md`). Reviews are LLM-driven (the akos-review skill), not
script-driven, so history capture is a bridge: the skill's last step calls
`akos history record` with the assembled report/scores/decision, and this
module is what turns that into structured, diffable storage.

Usage:
    python3 schemas/history.py record --type TYPE --decision PASS|"PASS WITH FIXES"|BLOCKED
                                       --profile NAME --report PATH
                                       [--scores-json JSON] [--packs-json JSON] [--dir PROJECT_DIR]
    python3 schemas/history.py list [--dir PROJECT_DIR]
    python3 schemas/history.py show REVIEW_ID [--dir PROJECT_DIR]
    python3 schemas/history.py latest [--dir PROJECT_DIR]
    python3 schemas/history.py compare REVIEW_A REVIEW_B [--dir PROJECT_DIR]
    python3 schemas/history.py clean [--dir PROJECT_DIR] [--keep N]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def git_info(project_dir: Path) -> dict:
    def run(*args):
        try:
            proc = subprocess.run(
                ["git", *args], cwd=project_dir, capture_output=True, text=True, timeout=5
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        if proc.returncode != 0:
            # Must check the exit code, not just stdout: `git rev-parse HEAD`
            # on a repo with zero commits exits 128 but still echoes the
            # literal string "HEAD" to stdout — stdout alone reads as a
            # plausible (wrong) commit hash. Caught by actually running this
            # against a freshly `git init`'d, commit-less scratch repo.
            return None
        return proc.stdout.strip() or None

    commit = run("rev-parse", "HEAD")
    branch = run("branch", "--show-current")
    return {"commit": commit, "branch": branch}


def reviews_dir(project_dir: Path) -> Path:
    return project_dir / ".akos" / "reviews"


def make_review_id(review_type: str, timestamp: str) -> str:
    safe_type = re.sub(r"[^a-zA-Z0-9_-]", "-", review_type)
    return f"{timestamp}-{safe_type}"


def cmd_record(args) -> int:
    project_dir = Path(args.dir).resolve()
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"error: report file not found: {report_path}", file=sys.stderr)
        return 1

    timestamp = args.timestamp  # injected by caller (bash `date`) — this module never calls
                                  # datetime.now() itself, since Date.now()-equivalents are
                                  # explicitly the one thing that must come from the caller
                                  # for reproducibility in any replay/resume context.
    review_id = make_review_id(args.type, timestamp)
    out_dir = reviews_dir(project_dir) / review_id
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "report.md").write_text(report_path.read_text(encoding="utf-8"), encoding="utf-8")

    scores = json.loads(args.scores_json) if args.scores_json else {}
    packs = json.loads(args.packs_json) if args.packs_json else []

    metadata = {
        "review_id": review_id,
        "type": args.type,
        "timestamp": timestamp,
        "profile": args.profile,
        "decision": args.decision,
        **git_info(project_dir),
        "packs_loaded": packs,
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (out_dir / "report.json").write_text(json.dumps({"decision": args.decision, "scores": scores}, indent=2), encoding="utf-8")

    print(f"recorded {review_id} in {out_dir}")
    return 0


def cmd_list(args) -> int:
    project_dir = Path(args.dir).resolve()
    d = reviews_dir(project_dir)
    if not d.exists():
        print("(no reviews recorded yet)")
        return 0
    for entry in sorted(d.iterdir()):
        if not entry.is_dir():
            continue
        meta_path = entry / "metadata.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        print(f"  {entry.name:<40} {meta.get('decision', '?'):<16} profile={meta.get('profile', '?')}")
    return 0


def _load_review(project_dir: Path, review_id: str) -> tuple[dict, dict]:
    d = reviews_dir(project_dir) / review_id
    meta = json.loads((d / "metadata.json").read_text())
    report = json.loads((d / "report.json").read_text())
    return meta, report


def cmd_show(args) -> int:
    project_dir = Path(args.dir).resolve()
    try:
        meta, report = _load_review(project_dir, args.review_id)
    except FileNotFoundError:
        print(f"error: no such review: {args.review_id}", file=sys.stderr)
        return 1
    print(json.dumps({**meta, **report}, indent=2))
    return 0


def cmd_latest(args) -> int:
    project_dir = Path(args.dir).resolve()
    d = reviews_dir(project_dir)
    if not d.exists():
        print("(no reviews recorded yet)")
        return 0
    entries = sorted((e for e in d.iterdir() if e.is_dir()), key=lambda e: e.name)
    if not entries:
        print("(no reviews recorded yet)")
        return 0
    args.review_id = entries[-1].name
    return cmd_show(args)


def _finding_keys(report: dict) -> set:
    # Findings aren't separately itemized in report.json today (scores +
    # decision only) — comparison operates on what IS structured: decision
    # and per-dimension scores. A richer per-finding diff is future work,
    # not silently pretended to exist here.
    return set(report.get("scores", {}).keys())


def cmd_compare(args) -> int:
    project_dir = Path(args.dir).resolve()
    try:
        meta_a, report_a = _load_review(project_dir, args.review_a)
        meta_b, report_b = _load_review(project_dir, args.review_b)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    result = {
        "a": args.review_a, "b": args.review_b,
        "decision_change": f"{report_a.get('decision')} -> {report_b.get('decision')}",
        "score_deltas": {},
    }
    all_dims = _finding_keys(report_a) | _finding_keys(report_b)
    for dim in sorted(all_dims):
        sa = report_a.get("scores", {}).get(dim)
        sb = report_b.get("scores", {}).get(dim)
        if sa is None or sb is None:
            result["score_deltas"][dim] = {"a": sa, "b": sb, "delta": None}
        else:
            result["score_deltas"][dim] = {"a": sa, "b": sb, "delta": sb - sa}

    print(json.dumps(result, indent=2))
    return 0


def cmd_clean(args) -> int:
    project_dir = Path(args.dir).resolve()
    d = reviews_dir(project_dir)
    if not d.exists():
        print("(nothing to clean)")
        return 0
    entries = sorted((e for e in d.iterdir() if e.is_dir()), key=lambda e: e.name)
    to_remove = entries[: max(0, len(entries) - args.keep)]
    for e in to_remove:
        for f in e.iterdir():
            f.unlink()
        e.rmdir()
    print(f"removed {len(to_remove)} review(s), kept {len(entries) - len(to_remove)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_record = sub.add_parser("record")
    p_record.add_argument("--type", required=True)
    p_record.add_argument("--decision", required=True)
    p_record.add_argument("--profile", default="unknown")
    p_record.add_argument("--report", required=True)
    p_record.add_argument("--scores-json")
    p_record.add_argument("--packs-json")
    p_record.add_argument("--dir", default=".")
    p_record.add_argument("--timestamp", required=True, help="Caller-supplied, e.g. from `date -u +%Y%m%dT%H%M%SZ`")

    p_list = sub.add_parser("list")
    p_list.add_argument("--dir", default=".")

    p_show = sub.add_parser("show")
    p_show.add_argument("review_id")
    p_show.add_argument("--dir", default=".")

    p_latest = sub.add_parser("latest")
    p_latest.add_argument("--dir", default=".")

    p_compare = sub.add_parser("compare")
    p_compare.add_argument("review_a")
    p_compare.add_argument("review_b")
    p_compare.add_argument("--dir", default=".")

    p_clean = sub.add_parser("clean")
    p_clean.add_argument("--dir", default=".")
    p_clean.add_argument("--keep", type=int, default=20)

    args = ap.parse_args(argv)
    return {
        "record": cmd_record, "list": cmd_list, "show": cmd_show,
        "latest": cmd_latest, "compare": cmd_compare, "clean": cmd_clean,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
