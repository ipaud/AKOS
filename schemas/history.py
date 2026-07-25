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
import errno
import fcntl
import json
import os
import re
import secrets
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Shared with the SECRET_IN_SOURCE/SERVICE_ROLE_IN_CLIENT detectors. Importing
# rather than restating the patterns here keeps one copy: a second set of
# regexes would drift from the first the moment either is updated.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from secret_utils import redact_secrets  # noqa: E402


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


class UnsafeHistoryPathError(Exception):
    """A history path crosses a symlink or has an unexpected filesystem type."""


@dataclass
class _HistoryHandles:
    root_fd: int
    akos_fd: int
    reviews_fd: int

    def close(self) -> None:
        for fd in (self.reviews_fd, self.akos_fd, self.root_fd):
            try:
                os.close(fd)
            except OSError:
                pass


@dataclass(frozen=True)
class _GitignoreChange:
    existed: bool
    original_text: str
    original_mode: int
    installed_identity: tuple[int, int]


def _lexists(path: Path) -> bool:
    """Like Path.exists(), but returns True for broken symlinks too."""
    return os.path.lexists(path)


def _identity(file_stat: os.stat_result) -> tuple[int, int]:
    return file_stat.st_dev, file_stat.st_ino


def _directory_open_flags() -> int:
    if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        raise UnsafeHistoryPathError(
            "this platform cannot provide no-follow directory handles"
        )
    return (
        os.O_RDONLY
        | os.O_DIRECTORY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
    )


def _open_directory_at(parent_fd: int, name: str, label: str) -> int:
    try:
        fd = os.open(name, _directory_open_flags(), dir_fd=parent_fd)
    except (NotImplementedError, TypeError) as exc:
        raise UnsafeHistoryPathError(
            "this platform cannot provide fd-relative directory traversal"
        ) from exc
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise UnsafeHistoryPathError(f"{label} is a symlink or not a directory") from exc
        raise
    if not stat.S_ISDIR(os.fstat(fd).st_mode):
        os.close(fd)
        raise UnsafeHistoryPathError(f"{label} is not a directory")
    return fd


def _open_or_create_directory_at(
    parent_fd: int,
    name: str,
    label: str,
    *,
    create: bool,
) -> int | None:
    try:
        return _open_directory_at(parent_fd, name, label)
    except FileNotFoundError:
        if not create:
            return None
        try:
            os.mkdir(name, dir_fd=parent_fd)
        except FileExistsError:
            pass
        except (NotImplementedError, TypeError) as exc:
            raise UnsafeHistoryPathError(
                "this platform cannot create history directories fd-relatively"
            ) from exc
        return _open_directory_at(parent_fd, name, label)


def _open_history_handles(
    project_dir: Path,
    *,
    create: bool,
) -> _HistoryHandles | None:
    try:
        root_fd = os.open(project_dir, _directory_open_flags())
    except (NotImplementedError, TypeError) as exc:
        raise UnsafeHistoryPathError(
            "this platform cannot anchor the project directory"
        ) from exc
    try:
        fcntl.flock(root_fd, fcntl.LOCK_EX)
    except OSError:
        os.close(root_fd)
        raise
    try:
        akos_fd = _open_or_create_directory_at(
            root_fd,
            ".akos",
            ".akos",
            create=create,
        )
        if akos_fd is None:
            os.close(root_fd)
            return None
        try:
            reviews_fd = _open_or_create_directory_at(
                akos_fd,
                "reviews",
                ".akos/reviews",
                create=create,
            )
            if reviews_fd is None:
                os.close(akos_fd)
                os.close(root_fd)
                return None
        except BaseException:
            os.close(akos_fd)
            raise
    except BaseException:
        try:
            os.close(root_fd)
        except OSError:
            pass
        raise
    return _HistoryHandles(root_fd, akos_fd, reviews_fd)


def _read_regular_text_at(
    parent_fd: int,
    name: str,
    *,
    missing_ok: bool = False,
) -> tuple[str, int, bool, tuple[int, int] | None]:
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(name, flags, dir_fd=parent_fd)
    except FileNotFoundError:
        if missing_ok:
            return "", _default_create_mode(), False, None
        raise
    except (NotImplementedError, TypeError) as exc:
        raise UnsafeHistoryPathError(
            "this platform cannot read history files fd-relatively"
        ) from exc
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise UnsafeHistoryPathError(f"{name} is a symlink") from exc
        raise
    file_stat = os.fstat(fd)
    if not stat.S_ISREG(file_stat.st_mode):
        os.close(fd)
        raise UnsafeHistoryPathError(f"{name} is not a regular file")
    with os.fdopen(fd, "r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    return (
        text,
        stat.S_IMODE(file_stat.st_mode),
        True,
        _identity(file_stat),
    )


def _default_create_mode() -> int:
    current = os.umask(0)
    os.umask(current)
    return 0o666 & ~current


def _atomic_write_at(
    parent_fd: int,
    name: str,
    content: str,
    mode: int,
) -> tuple[int, int]:
    temp_name = ""
    temp_fd: int | None = None
    for _ in range(16):
        temp_name = f".{name}.{secrets.token_hex(8)}.tmp"
        try:
            temp_fd = os.open(
                temp_name,
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
                | os.O_NOFOLLOW
                | getattr(os, "O_CLOEXEC", 0),
                mode,
                dir_fd=parent_fd,
            )
            break
        except FileExistsError:
            continue
        except (NotImplementedError, TypeError) as exc:
            raise UnsafeHistoryPathError(
                "this platform cannot create fd-relative temporary files"
            ) from exc
    if temp_fd is None:
        raise OSError("could not allocate a unique temporary file")
    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fchmod(handle.fileno(), mode)
        temp_fd = None
        os.replace(
            temp_name,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        return _identity(os.stat(
            name,
            dir_fd=parent_fd,
            follow_symlinks=False,
        ))
    except BaseException:
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except OSError:
                pass
        try:
            os.unlink(temp_name, dir_fd=parent_fd)
        except OSError:
            pass
        raise


def _git_repository_present(root_fd: int) -> bool:
    try:
        file_stat = os.stat(".git", dir_fd=root_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    return stat.S_ISDIR(file_stat.st_mode) or stat.S_ISREG(file_stat.st_mode)


def _render_gitignore(text: str) -> tuple[str, bool]:
    relevant = [
        line.strip()
        for line in text.splitlines()
        if line.strip() in {GITIGNORE_ENTRY, f"!{GITIGNORE_ENTRY}"}
    ]
    if relevant and relevant[-1] == GITIGNORE_ENTRY:
        return text, False
    if not text:
        return f"{GITIGNORE_COMMENT}\n{GITIGNORE_ENTRY}\n", True
    prefix = "" if text.endswith("\n") else "\n"
    return (
        f"{text}{prefix}\n{GITIGNORE_COMMENT}\n{GITIGNORE_ENTRY}\n",
        True,
    )


def _ensure_gitignored_at(root_fd: int) -> tuple[bool, _GitignoreChange | None]:
    if not _git_repository_present(root_fd):
        return False, None
    existing, mode, existed, _ = _read_regular_text_at(
        root_fd,
        ".gitignore",
        missing_ok=True,
    )
    rendered, changed = _render_gitignore(existing)
    if not changed:
        return False, None
    installed_identity = _atomic_write_at(
        root_fd,
        ".gitignore",
        rendered,
        mode,
    )
    return changed, _GitignoreChange(
        existed=existed,
        original_text=existing,
        original_mode=mode,
        installed_identity=installed_identity,
    )


def _rollback_gitignore_at(root_fd: int, change: _GitignoreChange | None) -> None:
    if change is None:
        return
    current = os.stat(".gitignore", dir_fd=root_fd, follow_symlinks=False)
    if _identity(current) != change.installed_identity:
        raise UnsafeHistoryPathError(
            ".gitignore changed after AKOS wrote it; refusing rollback"
        )
    if change.existed:
        _atomic_write_at(
            root_fd,
            ".gitignore",
            change.original_text,
            change.original_mode,
        )
    else:
        os.unlink(".gitignore", dir_fd=root_fd)


def _require_real_directory(path: Path, label: str) -> None:
    """Reject symlinks and non-directories without following either."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        raise UnsafeHistoryPathError(f"{label} does not exist") from None
    if stat.S_ISLNK(mode):
        raise UnsafeHistoryPathError(f"{label} is a symlink")
    if not stat.S_ISDIR(mode):
        raise UnsafeHistoryPathError(f"{label} is not a directory")


def _prepare_reviews_dir(project_dir: Path, *, create: bool) -> Path | None:
    """Return a symlink-free reviews directory, optionally creating it.

    Each component is inspected with lstat before use. Path.exists/is_dir
    follow symlinks, which is precisely what a repository-controlled
    `.akos/reviews` path must never do for writes or destructive operations.
    """
    akos_dir = project_dir / ".akos"
    reviews = reviews_dir(project_dir)

    if _lexists(akos_dir):
        _require_real_directory(akos_dir, ".akos")
    elif not create:
        return None
    else:
        try:
            akos_dir.mkdir()
        except FileExistsError:
            pass
        _require_real_directory(akos_dir, ".akos")

    if _lexists(reviews):
        _require_real_directory(reviews, ".akos/reviews")
    elif not create:
        return None
    else:
        try:
            reviews.mkdir()
        except FileExistsError:
            pass
        _require_real_directory(reviews, ".akos/reviews")
    return reviews


def _preflight_gitignore(project_dir: Path) -> None:
    """Reject a symlink or special-file .gitignore before record publishes."""
    if not (project_dir / ".git").exists():
        return
    gitignore = project_dir / ".gitignore"
    if not _lexists(gitignore):
        return
    mode = gitignore.lstat().st_mode
    if stat.S_ISLNK(mode):
        raise UnsafeHistoryPathError(".gitignore is a symlink")
    if not stat.S_ISREG(mode):
        raise UnsafeHistoryPathError(".gitignore is not a regular file")


def ensure_gitignored(project_dir: Path) -> bool:
    """Make sure .akos/reviews/ is ignored. Returns True if it was added.

    `install-project` also does this, but a review can be recorded into a
    project that never ran it — which is exactly what happened on the first
    real end-to-end run, leaving the reports untracked and unprotected. The
    protection has to live where the file is written, not only where the
    project is scaffolded.

    Append-only, and never rewrites an existing .gitignore.
    """
    root = Path(project_dir).resolve()
    try:
        root_fd = os.open(root, _directory_open_flags())
    except (OSError, UnsafeHistoryPathError):
        raise
    try:
        changed, _ = _ensure_gitignored_at(root_fd)
        return changed
    finally:
        os.close(root_fd)


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

    try:
        handles = _open_history_handles(project_dir, create=True)
    except (OSError, UnsafeHistoryPathError) as e:
        print(f"error: unsafe review history path ({e}); nothing was published", file=sys.stderr)
        return 1
    assert handles is not None

    # Every staging write, publish, cleanup, and .gitignore update is anchored
    # to descriptors opened with O_NOFOLLOW. Renaming `.akos` or `reviews`
    # during the operation cannot redirect any mutation into a symlink target.
    gitignore_added = False
    gitignore_change: _GitignoreChange | None = None
    published = False
    review_id = ""
    final_dir = reviews_dir(project_dir)
    last_err: Exception | None = None

    def rollback_gitignore() -> str | None:
        try:
            _rollback_gitignore_at(handles.root_fd, gitignore_change)
        except (OSError, UnsafeHistoryPathError) as exc:
            return str(exc)
        return None

    try:
        for _ in range(MAX_ID_ATTEMPTS):
            review_id = make_review_id(args.type, timestamp)
            final_dir = reviews_dir(project_dir) / review_id
            staging_name = ""
            staging_fd: int | None = None
            try:
                staging_name, staging_fd = _create_staging_directory_at(
                    handles.reviews_fd,
                    STAGING_PREFIX,
                )
                metadata = {
                    "review_id": review_id,
                    "type": args.type,
                    "timestamp": timestamp,
                    "profile": args.profile,
                    "decision": args.decision,
                    **git_info(project_dir),
                    "packs_loaded": packs,
                }
                _write_new_text_at(staging_fd, "report.md", report_text)
                _write_new_text_at(
                    staging_fd,
                    "metadata.json",
                    json.dumps(metadata, indent=2),
                )
                _write_new_text_at(staging_fd, "report.json", report_json)
                metadata_text, _, _, _ = _read_regular_text_at(
                    staging_fd,
                    "metadata.json",
                )
                report_json_text, _, _, _ = _read_regular_text_at(
                    staging_fd,
                    "report.json",
                )
                json.loads(metadata_text)
                json.loads(report_json_text)

                if gitignore_change is None:
                    gitignore_added, gitignore_change = _ensure_gitignored_at(
                        handles.root_fd
                    )

                os.rename(
                    staging_name,
                    review_id,
                    src_dir_fd=handles.reviews_fd,
                    dst_dir_fd=handles.reviews_fd,
                )
                published = True
                break
            except OSError as e:
                if staging_fd is not None:
                    os.close(staging_fd)
                    staging_fd = None
                if staging_name:
                    try:
                        _cleanup_staging_at(handles.reviews_fd, staging_name)
                    except OSError:
                        pass
                try:
                    os.stat(
                        review_id,
                        dir_fd=handles.reviews_fd,
                        follow_symlinks=False,
                    )
                except FileNotFoundError:
                    rollback_error = rollback_gitignore()
                    suffix = (
                        f"; .gitignore rollback also failed ({rollback_error})"
                        if rollback_error
                        else ""
                    )
                    print(
                        f"error: could not record review ({e}){suffix}; "
                        "nothing was published",
                        file=sys.stderr,
                    )
                    return 1
                last_err = e
                continue
            except Exception as e:  # noqa: BLE001 - any failure must leave no partial review
                if staging_fd is not None:
                    os.close(staging_fd)
                    staging_fd = None
                if staging_name:
                    try:
                        _cleanup_staging_at(handles.reviews_fd, staging_name)
                    except OSError:
                        pass
                rollback_error = rollback_gitignore()
                suffix = (
                    f"; .gitignore rollback also failed ({rollback_error})"
                    if rollback_error
                    else ""
                )
                print(
                    f"error: could not record review ({e}){suffix}; "
                    "nothing was published",
                    file=sys.stderr,
                )
                return 1
            finally:
                if staging_fd is not None:
                    os.close(staging_fd)

        if not published:
            rollback_error = rollback_gitignore()
            suffix = (
                f"; .gitignore rollback also failed ({rollback_error})"
                if rollback_error
                else ""
            )
            print(
                f"error: could not allocate a unique review id after "
                f"{MAX_ID_ATTEMPTS} attempts ({last_err}){suffix}; "
                "nothing was published",
                file=sys.stderr,
            )
            return 1
    finally:
        handles.close()

    if gitignore_added:
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


def _review_state_at(
    reviews_fd: int,
    entry_name: str,
) -> tuple[dict | None, str | None, tuple[int, int] | None]:
    try:
        entry_fd = _open_directory_at(
            reviews_fd,
            entry_name,
            f"review {entry_name}",
        )
    except (OSError, UnsafeHistoryPathError) as exc:
        return None, f"unreadable review entry ({exc})", None
    try:
        entry_identity = _identity(os.fstat(entry_fd))
        try:
            children = set(os.listdir(entry_fd))
        except OSError as exc:
            return None, f"unreadable review directory ({exc})", entry_identity
        missing = [name for name in REQUIRED_FILES if name not in children]
        if missing:
            return None, f"missing {missing[0]}", entry_identity
        unexpected = sorted(children - set(REQUIRED_FILES))
        if unexpected:
            return (
                None,
                f"unexpected content: {', '.join(unexpected)}",
                entry_identity,
            )
        texts: dict[str, str] = {}
        for name in REQUIRED_FILES:
            try:
                text, _, _, _ = _read_regular_text_at(entry_fd, name)
            except (OSError, UnsafeHistoryPathError) as exc:
                return None, f"unreadable {name} ({exc})", entry_identity
            texts = {**texts, name: text}
        try:
            metadata = json.loads(texts["metadata.json"])
        except json.JSONDecodeError as exc:
            return None, f"unreadable metadata.json ({exc})", entry_identity
        try:
            json.loads(texts["report.json"])
        except json.JSONDecodeError as exc:
            return None, f"unreadable report.json ({exc})", entry_identity
        return metadata, None, entry_identity
    finally:
        os.close(entry_fd)


def _create_staging_directory_at(
    reviews_fd: int,
    prefix: str,
) -> tuple[str, int]:
    for _ in range(16):
        name = f"{prefix}{secrets.token_hex(8)}"
        try:
            os.mkdir(name, mode=0o700, dir_fd=reviews_fd)
        except FileExistsError:
            continue
        except (NotImplementedError, TypeError) as exc:
            raise UnsafeHistoryPathError(
                "this platform cannot stage history fd-relatively"
            ) from exc
        try:
            return name, _open_directory_at(
                reviews_fd,
                name,
                f"staging directory {name}",
            )
        except BaseException:
            try:
                os.rmdir(name, dir_fd=reviews_fd)
            except OSError:
                pass
            raise
    raise OSError("could not allocate a unique staging directory")


def _write_new_text_at(parent_fd: int, name: str, text: str) -> None:
    fd = os.open(
        name,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0),
        _default_create_mode(),
        dir_fd=parent_fd,
    )
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _remove_review_directory_at(parent_fd: int, entry_name: str) -> None:
    entry_fd = _open_directory_at(
        parent_fd,
        entry_name,
        f"review {entry_name}",
    )
    try:
        for name in REQUIRED_FILES:
            try:
                os.unlink(name, dir_fd=entry_fd)
            except FileNotFoundError:
                pass
    finally:
        os.close(entry_fd)
    os.rmdir(entry_name, dir_fd=parent_fd)


def _cleanup_staging_at(parent_fd: int, entry_name: str) -> None:
    try:
        _remove_review_directory_at(parent_fd, entry_name)
    except FileNotFoundError:
        pass


def _review_state(entry: Path) -> tuple[dict | None, str | None]:
    """Validate a published review directory.

    Returns (metadata, None) if the review is intact — all three required
    files present, both JSON files parse. Returns (None, reason) otherwise,
    naming exactly what's wrong so a corrupt review is reported, not hidden
    as if it didn't exist and not confused with a valid one.
    """
    try:
        entry_mode = entry.lstat().st_mode
    except OSError as e:
        return None, f"unreadable review entry ({e})"
    if stat.S_ISLNK(entry_mode):
        return None, "review entry is a symlink"
    if not stat.S_ISDIR(entry_mode):
        return None, "review entry is not a directory"

    try:
        children = {child.name: child for child in entry.iterdir()}
    except OSError as e:
        return None, f"unreadable review directory ({e})"
    missing = [name for name in REQUIRED_FILES if name not in children]
    if missing:
        return None, f"missing {missing[0]}"
    unexpected = sorted(set(children) - set(REQUIRED_FILES))
    if unexpected:
        return None, f"unexpected content: {', '.join(unexpected)}"
    for name in REQUIRED_FILES:
        try:
            mode = children[name].lstat().st_mode
        except OSError as e:
            return None, f"unreadable {name} ({e})"
        if stat.S_ISLNK(mode):
            return None, f"{name} is a symlink"
        if not stat.S_ISREG(mode):
            return None, f"{name} is not a regular file"
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
    try:
        d = _prepare_reviews_dir(project_dir, create=False)
    except UnsafeHistoryPathError as e:
        print(f"error: unsafe review history path ({e})", file=sys.stderr)
        return 1
    if d is None:
        print("(no reviews recorded yet)")
        return 0
    for entry in sorted(d.iterdir()):
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
    if review_id in ("", ".", "..") or Path(review_id).name != review_id:
        raise FileNotFoundError(f"no such review: {review_id}")
    root = _prepare_reviews_dir(project_dir, create=False)
    if root is None:
        raise FileNotFoundError(f"no such review: {review_id}")
    d = root / review_id
    if not _lexists(d):
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
    except UnsafeHistoryPathError as e:
        print(f"error: unsafe review history path ({e})", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: review {args.review_id} has corrupt JSON ({e})", file=sys.stderr)
        return 1
    print(json.dumps({**meta, **report}, indent=2))
    return 0


def cmd_latest(args) -> int:
    project_dir = Path(args.dir).resolve()
    try:
        d = _prepare_reviews_dir(project_dir, create=False)
    except UnsafeHistoryPathError as e:
        print(f"error: unsafe review history path ({e})", file=sys.stderr)
        return 1
    if d is None:
        print("(no reviews recorded yet)")
        return 0
    entries = sorted((e for e in d.iterdir() if not _is_staging(e)), key=lambda e: e.name)
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
    except UnsafeHistoryPathError as e:
        print(f"error: unsafe review history path ({e})", file=sys.stderr)
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
    try:
        handles = _open_history_handles(project_dir, create=False)
    except (OSError, UnsafeHistoryPathError) as e:
        print(f"error: unsafe review history path ({e}); nothing was removed", file=sys.stderr)
        return 1
    if handles is None:
        print("(nothing to clean)")
        return 0
    try:
        # Staging dirs are never candidates: they are not published reviews,
        # and a concurrent record's in-flight write must not be swept.
        entries = sorted(
            name
            for name in os.listdir(handles.reviews_fd)
            if not name.startswith(STAGING_PREFIX)
        )
        snapshots: dict[str, tuple[int, int]] = {}

        # Preflight every published entry, including the retention window.
        for entry_name in entries:
            _, reason, entry_identity = _review_state_at(
                handles.reviews_fd,
                entry_name,
            )
            if reason is not None or entry_identity is None:
                print(
                    f"error: refusing to clean corrupt review {entry_name}: "
                    f"{reason}; nothing was removed",
                    file=sys.stderr,
                )
                return 1
            snapshots = {**snapshots, entry_name: entry_identity}

        to_remove = entries[: max(0, len(entries) - args.keep)]
        if not to_remove:
            print(
                f"nothing to remove: {len(entries)} review(s) present, "
                f"keeping {args.keep}"
            )
            return 0

        will_delete = not args.dry_run and args.confirm_delete == len(to_remove)
        for entry_name in to_remove:
            print(
                f"  removing: {entry_name}"
                if will_delete
                else f"  would remove: {entry_name}"
            )

        if args.dry_run:
            print(
                f"dry run: {len(to_remove)} review(s) would be removed, "
                f"{len(entries) - len(to_remove)} kept. "
                f"Re-run with --confirm-delete {len(to_remove)} to apply."
            )
            return 0

        if args.confirm_delete is None:
            print(
                f"error: refusing to delete {len(to_remove)} review(s) "
                "without confirmation.\n"
                f"  Preview first:  history clean --dir {args.dir} "
                f"--keep {args.keep} --dry-run\n"
                f"  Then apply:     history clean --dir {args.dir} "
                f"--keep {args.keep} --confirm-delete {len(to_remove)}",
                file=sys.stderr,
            )
            return 1
        if args.confirm_delete != len(to_remove):
            print(
                f"error: --confirm-delete {args.confirm_delete} does not "
                f"match the {len(to_remove)} review(s) that would be removed. "
                "Re-run with --dry-run to see the current set; the history "
                "changed since you last looked.",
                file=sys.stderr,
            )
            return 1

        # Validate the complete set again through the anchored descriptor.
        for entry_name in entries:
            _, reason, entry_identity = _review_state_at(
                handles.reviews_fd,
                entry_name,
            )
            if (
                reason is not None
                or entry_identity != snapshots[entry_name]
            ):
                print(
                    f"error: review {entry_name} changed during clean: "
                    f"{reason or 'directory identity changed'}; "
                    "nothing was removed",
                    file=sys.stderr,
                )
                return 1

        # Capture every deletion candidate in one private sibling directory
        # before unlinking anything. If capture fails, names already moved are
        # rolled back; after capture, all unlinks remain anchored even if
        # `.akos` or `reviews` is concurrently replaced by a symlink.
        quarantine_name, quarantine_fd = _create_staging_directory_at(
            handles.reviews_fd,
            f"{STAGING_PREFIX}clean-",
        )
        moved: list[str] = []
        try:
            try:
                for entry_name in to_remove:
                    current = os.stat(
                        entry_name,
                        dir_fd=handles.reviews_fd,
                        follow_symlinks=False,
                    )
                    if _identity(current) != snapshots[entry_name]:
                        raise UnsafeHistoryPathError(
                            f"review {entry_name} identity changed"
                        )
                    os.rename(
                        entry_name,
                        entry_name,
                        src_dir_fd=handles.reviews_fd,
                        dst_dir_fd=quarantine_fd,
                    )
                    captured = os.stat(
                        entry_name,
                        dir_fd=quarantine_fd,
                        follow_symlinks=False,
                    )
                    if _identity(captured) != snapshots[entry_name]:
                        raise UnsafeHistoryPathError(
                            f"review {entry_name} changed while being captured"
                        )
                    moved.append(entry_name)
            except (OSError, UnsafeHistoryPathError) as exc:
                rollback_errors: list[str] = []
                for entry_name in reversed(moved):
                    try:
                        os.rename(
                            entry_name,
                            entry_name,
                            src_dir_fd=quarantine_fd,
                            dst_dir_fd=handles.reviews_fd,
                        )
                    except OSError as rollback_exc:
                        rollback_errors.append(str(rollback_exc))
                suffix = (
                    f"; capture rollback also failed: {', '.join(rollback_errors)}"
                    if rollback_errors
                    else ""
                )
                print(
                    f"error: review history changed during clean ({exc})"
                    f"{suffix}; nothing was removed",
                    file=sys.stderr,
                )
                return 1

            for entry_name in moved:
                _remove_review_directory_at(quarantine_fd, entry_name)
        except (OSError, UnsafeHistoryPathError) as exc:
            print(
                f"error: could not clean review history ({exc})",
                file=sys.stderr,
            )
            return 1
        finally:
            os.close(quarantine_fd)
            try:
                os.rmdir(quarantine_name, dir_fd=handles.reviews_fd)
            except OSError:
                pass

        print(
            f"removed {len(to_remove)} review(s), "
            f"kept {len(entries) - len(to_remove)}"
        )
        return 0
    finally:
        handles.close()


class _ContractArgumentParser(argparse.ArgumentParser):
    """Keep argparse usage failures inside history's documented 0/1 contract."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def _nonnegative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a non-negative integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer")
    return parsed


def main(argv=None) -> int:
    ap = _ContractArgumentParser(description=__doc__)
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
    p_clean.add_argument("--keep", type=_nonnegative_int, default=20,
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
