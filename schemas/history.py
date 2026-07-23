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
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# The secret patterns live with the detector that owns them. Importing them
# rather than restating them here keeps one copy: a second set of regexes
# would drift from the first the moment either is updated.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rules" / "security"))
from _secret_utils import redact_secrets  # noqa: E402


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


GITIGNORE_ENTRY = ".akos/reviews/"
GITIGNORE_COMMENT = "# AKOS review reports — may quote secrets found during a review"


def ensure_gitignored(project_dir: Path) -> bool:
    """Make sure .akos/reviews/ is ignored. Returns True if it was added.

    `install-project` also does this, but a review can be recorded into a
    project that never ran it — which is exactly what happened on the first
    real end-to-end run, leaving the reports untracked and unprotected. The
    protection has to live where the file is written, not only where the
    project is scaffolded.

    Append-only, and never rewrites an existing .gitignore.
    """
    if not (project_dir / ".git").exists():
        return False  # not a git repo; nothing to ignore into
    gitignore = project_dir / ".gitignore"
    if gitignore.is_file():
        existing = gitignore.read_text(encoding="utf-8")
        if any(line.strip() == GITIGNORE_ENTRY for line in existing.splitlines()):
            return False
        prefix = "" if existing.endswith("\n") or not existing else "\n"
        gitignore.write_text(f"{existing}{prefix}\n{GITIGNORE_COMMENT}\n{GITIGNORE_ENTRY}\n",
                             encoding="utf-8")
    else:
        gitignore.write_text(f"{GITIGNORE_COMMENT}\n{GITIGNORE_ENTRY}\n", encoding="utf-8")
    return True


# How many fresh ids to try before giving up on a publish. A collision needs
# the same UTC second, the same type, AND the same 8 random hex chars, so one
# retry is already astronomically sufficient; the bound is a safety net, not a
# hot path.
MAX_ID_ATTEMPTS = 5


def make_review_id(review_type: str, timestamp: str) -> str:
    # A sortable, legible prefix (timestamp + type) plus stdlib entropy. The
    # timestamp alone is NOT the identity — two reviews of the same type in the
    # same second used to collide and the second overwrote the first. The
    # random suffix is what makes the id unique; no PID, no sub-second clock,
    # no external ULID dependency.
    safe_type = re.sub(r"[^a-zA-Z0-9_-]", "-", review_type)
    return f"{timestamp}-{safe_type}-{secrets.token_hex(4)}"


def cmd_record(args) -> int:
    project_dir = Path(args.dir).resolve()
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"error: report file not found: {report_path}", file=sys.stderr)
        return 1

    # Parse every structured argument BEFORE creating anything on disk. The
    # previous order wrote the directory and report.md first, so a malformed
    # --scores-json threw between the two writes and left a review that
    # `history list` skips (it requires metadata.json) — invisible, and a
    # fresh timestamp on every retry meant the orphans accumulated. The
    # caller assembling this JSON is an LLM following skills/akos-review,
    # so a malformed brace is the expected failure, not an edge case.
    try:
        scores = json.loads(args.scores_json) if args.scores_json else {}
    except json.JSONDecodeError as e:
        print(f"error: --scores-json is not valid JSON ({e}); nothing was written", file=sys.stderr)
        return 1
    try:
        packs = json.loads(args.packs_json) if args.packs_json else []
    except json.JSONDecodeError as e:
        print(f"error: --packs-json is not valid JSON ({e}); nothing was written", file=sys.stderr)
        return 1

    timestamp = args.timestamp  # injected by caller (bash `date`) — this module never calls
                                  # datetime.now() itself, since Date.now()-equivalents are
                                  # explicitly the one thing that must come from the caller
                                  # for reproducibility in any replay/resume context. It is a
                                  # sortable prefix, not the unique id — uniqueness is added here.

    # Redact at write time, not at display time. A security review is
    # required to quote the credential it found — the report format demands
    # concrete evidence — so this file is exactly where secrets accumulate,
    # and it lands in the consuming project where it may well get committed.
    # Once written, unredacting is not an option available to anyone.
    report_text, redacted = redact_secrets(report_path.read_text(encoding="utf-8"))
    report_json = json.dumps({"decision": args.decision, "scores": scores}, indent=2)

    reviews = reviews_dir(project_dir)
    reviews.mkdir(parents=True, exist_ok=True)

    # Atomic, no-clobber publish. Stage the three files in a sibling temp dir,
    # verify all three exist and re-parse, then os.rename onto the final id —
    # atomic within one filesystem (the temp dir is a sibling). A PUBLISHED
    # review dir is non-empty, so os.rename onto it fails and it is never
    # overwritten; on that collision we regenerate the id and retry. A crash
    # mid-write leaves only the temp dir, which is removed — never a partial
    # final review. Uniqueness comes from the random id + the atomic rename,
    # not a check-then-create race, so concurrent records all survive.
    published = False
    review_id = ""
    final_dir = reviews
    last_err: Exception | None = None
    for _ in range(MAX_ID_ATTEMPTS):
        review_id = make_review_id(args.type, timestamp)
        final_dir = reviews / review_id
        staging = Path(tempfile.mkdtemp(prefix=".tmp-review-", dir=reviews))
        try:
            metadata = {
                "review_id": review_id,
                "type": args.type,
                "timestamp": timestamp,
                "profile": args.profile,
                "decision": args.decision,
                **git_info(project_dir),
                "packs_loaded": packs,
            }
            (staging / "report.md").write_text(report_text, encoding="utf-8")
            (staging / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            (staging / "report.json").write_text(report_json, encoding="utf-8")
            for name in ("report.md", "metadata.json", "report.json"):
                if not (staging / name).is_file():
                    raise OSError(f"staged file missing: {name}")
            json.loads((staging / "metadata.json").read_text(encoding="utf-8"))
            json.loads((staging / "report.json").read_text(encoding="utf-8"))
            os.rename(staging, final_dir)  # atomic; fails if final_dir is a non-empty published review
            published = True
            break
        except OSError as e:
            shutil.rmtree(staging, ignore_errors=True)
            if final_dir.exists():
                last_err = e
                continue  # id collision — a published review must never be overwritten
            print(f"error: could not record review ({e}); nothing was published", file=sys.stderr)
            return 1
        except Exception as e:  # noqa: BLE001 - any failure must leave no partial review
            shutil.rmtree(staging, ignore_errors=True)
            print(f"error: could not record review ({e}); nothing was published", file=sys.stderr)
            return 1

    if not published:
        print(f"error: could not allocate a unique review id after {MAX_ID_ATTEMPTS} attempts "
              f"({last_err}); nothing was published", file=sys.stderr)
        return 1

    if ensure_gitignored(project_dir):
        print(f"  added {GITIGNORE_ENTRY} to .gitignore (reports can quote what they find)")

    print(f"recorded {review_id} in {final_dir}")
    if redacted:
        # Say so. A redaction the caller never learns about is the same
        # class of defect as no redaction: the reviewer keeps believing the
        # stored report is a faithful copy of what they wrote.
        print(f"  redacted before writing: {', '.join(redacted)} "
              f"(the finding text is kept; only the credential value is replaced)")
    return 0


STAGING_PREFIX = ".tmp-review-"

# The three files a published review must have, exactly as `cmd_record`
# stages and verifies them before the atomic rename. Any published directory
# missing one, or holding one that doesn't parse, is corrupt — visibly
# reported as such, never silently treated as either clean or absent.
REQUIRED_FILES = ("report.md", "metadata.json", "report.json")


def _is_staging(entry: Path) -> bool:
    return entry.name.startswith(STAGING_PREFIX)


def _review_state(entry: Path) -> tuple[dict | None, str | None]:
    """Validate a published review directory.

    Returns (metadata, None) if the review is intact — all three required
    files present, both JSON files parse. Returns (None, reason) otherwise,
    naming exactly what's wrong so a corrupt review is reported, not hidden
    as if it didn't exist and not confused with a valid one.
    """
    for name in REQUIRED_FILES:
        if not (entry / name).is_file():
            return None, f"missing {name}"
    try:
        meta = json.loads((entry / "metadata.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return None, f"unreadable metadata.json ({e})"
    try:
        json.loads((entry / "report.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return None, f"unreadable report.json ({e})"
    return meta, None


def cmd_list(args) -> int:
    project_dir = Path(args.dir).resolve()
    d = reviews_dir(project_dir)
    if not d.exists():
        print("(no reviews recorded yet)")
        return 0
    for entry in sorted(d.iterdir()):
        if not entry.is_dir():
            continue
        # Skip the in-flight staging dirs a concurrent record may be writing;
        # they are not published reviews.
        if _is_staging(entry):
            continue
        meta, reason = _review_state(entry)
        if reason is not None:
            print(f"  {entry.name:<40} (corrupt: {reason})")
            continue
        print(f"  {entry.name:<40} {meta.get('decision', '?'):<16} profile={meta.get('profile', '?')}")
    return 0


class ReviewCorruptError(Exception):
    """A published review directory exists but fails its file/JSON contract —
    distinct from FileNotFoundError (the review id doesn't exist at all) so
    callers can report "corrupt" rather than the misleading "no such review"."""


def _load_review(project_dir: Path, review_id: str) -> tuple[dict, dict]:
    d = reviews_dir(project_dir) / review_id
    if not d.is_dir():
        raise FileNotFoundError(f"no such review: {review_id}")
    meta, reason = _review_state(d)
    if reason is not None:
        raise ReviewCorruptError(f"review {review_id} is corrupt: {reason}")
    report = json.loads((d / "report.json").read_text(encoding="utf-8"))
    return meta, report


def cmd_show(args) -> int:
    project_dir = Path(args.dir).resolve()
    try:
        meta, report = _load_review(project_dir, args.review_id)
    except FileNotFoundError:
        print(f"error: no such review: {args.review_id}", file=sys.stderr)
        return 1
    except ReviewCorruptError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: review {args.review_id} has corrupt JSON ({e})", file=sys.stderr)
        return 1
    print(json.dumps({**meta, **report}, indent=2))
    return 0


def cmd_latest(args) -> int:
    project_dir = Path(args.dir).resolve()
    d = reviews_dir(project_dir)
    if not d.exists():
        print("(no reviews recorded yet)")
        return 0
    entries = sorted((e for e in d.iterdir() if e.is_dir() and not _is_staging(e)), key=lambda e: e.name)
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
    except ReviewCorruptError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: a review being compared has corrupt JSON ({e})", file=sys.stderr)
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
    # Staging dirs are never candidates: they are not published reviews, and a
    # concurrent record's in-flight write must not be swept mid-publish.
    entries = sorted((e for e in d.iterdir() if e.is_dir() and not _is_staging(e)), key=lambda e: e.name)
    to_remove = entries[: max(0, len(entries) - args.keep)]

    # Name every review that would go. The scope of this command depends on
    # how many reviews happen to exist, which the caller has not seen — so
    # reporting only a count is not enough to consent to the deletion.
    if not to_remove:
        print(f"nothing to remove: {len(entries)} review(s) present, keeping {args.keep}")
        return 0

    # Decide whether this call deletes BEFORE labelling anything, so the
    # per-entry lines never say "removing" on a call that then refuses.
    will_delete = not args.dry_run and args.confirm_delete == len(to_remove)
    for e in to_remove:
        print(f"  removing: {e.name}" if will_delete else f"  would remove: {e.name}")

    if args.dry_run:
        print(f"dry run: {len(to_remove)} review(s) would be removed, "
              f"{len(entries) - len(to_remove)} kept. "
              f"Re-run with --confirm-delete {len(to_remove)} to apply.")
        return 0

    # .akos/reviews/ is frequently untracked in the consuming project, so a
    # delete here is usually unrecoverable. Require the caller to state the
    # count it saw, so a stale expectation fails instead of deleting.
    if args.confirm_delete is None:
        print(f"error: refusing to delete {len(to_remove)} review(s) without confirmation.\n"
              f"  Preview first:  history clean --dir {args.dir} --keep {args.keep} --dry-run\n"
              f"  Then apply:     history clean --dir {args.dir} --keep {args.keep} "
              f"--confirm-delete {len(to_remove)}", file=sys.stderr)
        return 1
    if args.confirm_delete != len(to_remove):
        print(f"error: --confirm-delete {args.confirm_delete} does not match the "
              f"{len(to_remove)} review(s) that would be removed. Re-run with --dry-run "
              f"to see the current set; the history changed since you last looked.",
              file=sys.stderr)
        return 1

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
    p_record.add_argument("--timestamp", required=True, help="Caller-supplied, e.g. from `date -u +%%Y%%m%%dT%%H%%M%%SZ`")

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

    p_clean = sub.add_parser("clean", help="delete old reviews (requires --dry-run first, then --confirm-delete N)")
    p_clean.add_argument("--dir", default=".")
    p_clean.add_argument("--keep", type=int, default=20,
                         help="how many of the newest reviews to keep (default: 20)")
    p_clean.add_argument("--dry-run", action="store_true",
                         help="list the reviews that would be removed and exit without deleting")
    p_clean.add_argument("--confirm-delete", type=int, default=None, metavar="N",
                         help="delete, asserting exactly N reviews will go (get N from --dry-run)")

    args = ap.parse_args(argv)
    return {
        "record": cmd_record, "list": cmd_list, "show": cmd_show,
        "latest": cmd_latest, "compare": cmd_compare, "clean": cmd_clean,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
