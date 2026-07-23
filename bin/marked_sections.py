#!/usr/bin/env python3
"""Single, shared parser/writer for AKOS:START/END managed sections.

Replaces two independent, first-match-only implementations that used to live
in `bin/akos`: `write_marked_section` (bash, `grep -nF ... | head -n1`) and
`cmd_profile_use`'s separate awk state machine. Both silently picked the
FIRST start/end pair even when the file held duplicates, multiple pairs, or
a one-sided marker — "succeeding" while quietly operating on the wrong
range, or on `cmd_profile_use`'s side, silently returning an empty section
that looked identical to "no section at all". This module makes malformed
marker structure a hard, reported failure instead.

Usage:
    python3 bin/marked_sections.py check <file>
    python3 bin/marked_sections.py extract <file>
    python3 bin/marked_sections.py write <file> (--body-file PATH | --body -)
    python3 bin/marked_sections.py validate-all <file> [<file> ...]
    python3 bin/marked_sections.py install-project <existing-project-dir> <four bodies>
    python3 bin/marked_sections.py set-personal-profile <project-dir> <name>

Exit codes (the "new command" 0/1/2 scheme from docs/cli/exit-codes.md):
    0 — ran successfully, nothing to fail on
    1 — usage/file error (bad args, path is not a regular file, I/O error)
    2 — ran successfully, and found a problem (INVALID marker structure,
        a body containing a marker line, or a validate-all target that
        isn't safely writable)
"""

from __future__ import annotations

import argparse
import errno
import fcntl
import os
import secrets
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

MARK_START = "<!-- AKOS:START -->"
MARK_END = "<!-- AKOS:END -->"

ABSENT = "ABSENT"
PRESENT = "PRESENT"
INVALID = "INVALID"


class NotARegularFileError(Exception):
    """The target path exists but is not a regular file (e.g. a directory)."""


class MarkerBodyError(Exception):
    """The body to be written itself contains a line matching a marker."""


class ProjectPathError(Exception):
    """A project root/child path is missing, escapes the root, or is a symlink."""


class ProjectWriteError(Exception):
    """A prepared multi-file write failed and rollback was attempted."""


@dataclass
class MarkerState:
    status: str  # ABSENT | PRESENT | INVALID
    start_line: int | None = None  # 0-indexed, only set when status == PRESENT
    end_line: int | None = None
    reasons: tuple[str, ...] = ()  # only set when status == INVALID


@dataclass(frozen=True)
class _PreparedWrite:
    path: Path
    relative_path: str
    content: str
    original_text: str
    mode: int
    existed: bool
    original_identity: tuple[int, int] | None
    event: str


@dataclass(frozen=True)
class _CompletedWrite:
    write: _PreparedWrite
    parent_fd: int
    leaf_name: str
    installed_identity: tuple[int, int]


@dataclass(frozen=True)
class _CreatedDirectory:
    parent_fd: int
    name: str
    directory_fd: int
    identity: tuple[int, int]


@dataclass(frozen=True)
class ProjectInstallResult:
    events: tuple[str, ...]
    gitignore_added: bool


PROJECT_MARKED_PATHS = (
    "CLAUDE.md",
    "AGENTS.md",
    ".cursor/rules/akos.mdc",
    ".akos/config.md",
)
GITIGNORE_PATH = ".gitignore"
GITIGNORE_ENTRY = ".akos/reviews/"
GITIGNORE_COMMENT = "# AKOS review reports — may quote secrets found during a review"
PROFILE_CONFIG_PATH = ".akos/config.md"


def _is_marker_line(line: str, marker: str) -> bool:
    # Stripped content must be EXACTLY the marker — a substring match (the
    # bash implementation's `grep -qF`) would false-positive on a line that
    # merely mentions the marker syntax inside prose or an attribute.
    return line.strip() == marker


def classify(text: str) -> MarkerState:
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if _is_marker_line(line, MARK_START)]
    ends = [i for i, line in enumerate(lines) if _is_marker_line(line, MARK_END)]

    if not starts and not ends:
        return MarkerState(status=ABSENT)

    if len(starts) == 1 and len(ends) == 1 and starts[0] < ends[0]:
        return MarkerState(status=PRESENT, start_line=starts[0], end_line=ends[0])

    reasons: list[str] = []
    if len(starts) > 1:
        reasons.append(f"multiple START markers found at lines {[i + 1 for i in starts]}")
    if len(ends) > 1:
        reasons.append(f"multiple END markers found at lines {[i + 1 for i in ends]}")
    if starts and not ends:
        reasons.append("START marker present with no END marker")
    if ends and not starts:
        reasons.append("END marker present with no START marker")
    if len(starts) == 1 and len(ends) == 1 and starts[0] > ends[0]:
        reasons.append(f"END marker (line {ends[0] + 1}) appears before START marker (line {starts[0] + 1})")
    if not reasons:
        reasons.append("ambiguous marker structure")
    return MarkerState(status=INVALID, reasons=tuple(reasons))


def _detect_style(text: str) -> tuple[str, bool]:
    """Returns (newline_style, has_trailing_newline)."""
    style = "\r\n" if "\r\n" in text else "\n"
    has_trailing_newline = text.endswith("\n")
    return style, has_trailing_newline


def _read_target_text(path: Path) -> str:
    """The file's text content, or "" if it does not exist yet — a missing
    file is a valid ABSENT target (safe to create), not an error.

    Reads with newline="" (no universal-newline translation) so a CRLF file's
    line endings survive into `text` for _detect_style to see. Path.read_text
    only grew a `newline` parameter in 3.13 — below this repo's 3.10 floor —
    so this opens the file explicitly instead of using that shortcut.
    """
    if not path.exists():
        return ""
    if not path.is_file():
        raise NotARegularFileError(f"{path} exists but is not a regular file")
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def _default_create_mode() -> int:
    # What a normal `> file` redirect would produce: 0o666 masked by the
    # process umask. os.umask() has no read-only form — set then restore.
    current = os.umask(0)
    os.umask(current)
    return 0o666 & ~current


def _atomic_write(path: Path, content: str, mode: int) -> None:
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        os.chmod(tmp_name, mode)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _resolve_project_root(project_root: Path) -> Path:
    try:
        resolved = project_root.resolve(strict=True)
    except OSError as e:
        raise ProjectPathError(
            f"{project_root} is not an existing project directory: {e}"
        ) from e
    if not resolved.is_dir():
        raise ProjectPathError(f"{project_root} is not an existing project directory")
    return resolved


def _safe_project_child(root: Path, relative_path: str) -> Path:
    rel = Path(relative_path)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise ProjectPathError(f"unsafe project-relative path: {relative_path!r}")

    current = root
    for index, part in enumerate(rel.parts):
        current = current / part
        if current.is_symlink():
            raise ProjectPathError(
                f"refusing child symlink under project root: {current}"
            )
        if current.exists():
            is_leaf = index == len(rel.parts) - 1
            if not is_leaf and not current.is_dir():
                raise ProjectPathError(
                    f"project path component is not a directory: {current}"
                )
            if is_leaf and not current.is_file():
                raise ProjectPathError(
                    f"project target is not a regular file: {current}"
                )
    return current


def _render_gitignore(text: str) -> tuple[str, bool]:
    relevant = [
        line.strip()
        for line in text.splitlines()
        if line.strip() in {GITIGNORE_ENTRY, f"!{GITIGNORE_ENTRY}"}
    ]
    if relevant and relevant[-1] == GITIGNORE_ENTRY:
        return text, False
    style, _ = _detect_style(text)
    if not text:
        return f"{GITIGNORE_COMMENT}{style}{GITIGNORE_ENTRY}{style}", True
    prefix = "" if text.endswith(("\n", "\r")) else style
    return (
        f"{text}{prefix}{style}{GITIGNORE_COMMENT}{style}"
        f"{GITIGNORE_ENTRY}{style}",
        True,
    )


def _identity(file_stat: os.stat_result) -> tuple[int, int]:
    return file_stat.st_dev, file_stat.st_ino


def _directory_open_flags() -> int:
    """Flags needed to anchor traversal without following a swapped parent."""
    if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        raise ProjectPathError(
            "this platform cannot provide no-follow directory handles"
        )
    return (
        os.O_RDONLY
        | os.O_DIRECTORY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
    )


def _open_directory_at(parent_fd: int, name: str) -> int:
    try:
        fd = os.open(name, _directory_open_flags(), dir_fd=parent_fd)
    except (NotImplementedError, TypeError) as exc:
        raise ProjectPathError(
            "this platform cannot provide fd-relative directory traversal"
        ) from exc
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise ProjectPathError(
                f"refusing non-directory or symlinked project parent: {name}"
            ) from exc
        raise
    if not stat.S_ISDIR(os.fstat(fd).st_mode):
        os.close(fd)
        raise ProjectPathError(f"project parent is not a directory: {name}")
    return fd


def _relative_parts(relative_path: str) -> tuple[str, ...]:
    rel = Path(relative_path)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise ProjectPathError(f"unsafe project-relative path: {relative_path!r}")
    return tuple(rel.parts)


def _open_parent_at(
    root_fd: int,
    relative_path: str,
    *,
    create: bool,
    created: list[_CreatedDirectory] | None = None,
) -> tuple[int | None, str]:
    parts = _relative_parts(relative_path)
    current_fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            try:
                next_fd = _open_directory_at(current_fd, part)
            except FileNotFoundError:
                if not create:
                    os.close(current_fd)
                    return None, parts[-1]
                try:
                    os.mkdir(part, dir_fd=current_fd)
                except (NotImplementedError, TypeError) as exc:
                    raise ProjectPathError(
                        "this platform cannot create project parents fd-relatively"
                    ) from exc
                next_fd = _open_directory_at(current_fd, part)
                if created is not None:
                    created.append(_CreatedDirectory(
                        parent_fd=os.dup(current_fd),
                        name=part,
                        directory_fd=os.dup(next_fd),
                        identity=_identity(os.fstat(next_fd)),
                    ))
            os.close(current_fd)
            current_fd = next_fd
        return current_fd, parts[-1]
    except BaseException:
        try:
            os.close(current_fd)
        except OSError:
            pass
        raise


def _read_leaf_at(
    parent_fd: int | None,
    leaf_name: str,
) -> tuple[str, int, bool, tuple[int, int] | None]:
    if parent_fd is None:
        return "", _default_create_mode(), False, None
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(leaf_name, flags, dir_fd=parent_fd)
    except FileNotFoundError:
        return "", _default_create_mode(), False, None
    except (NotImplementedError, TypeError) as exc:
        raise ProjectPathError(
            "this platform cannot read project files fd-relatively"
        ) from exc
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise ProjectPathError(
                f"refusing symlinked project target: {leaf_name}"
            ) from exc
        raise
    file_stat = os.fstat(fd)
    if not stat.S_ISREG(file_stat.st_mode):
        os.close(fd)
        raise ProjectPathError(f"project target is not a regular file: {leaf_name}")
    with os.fdopen(fd, "r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    return (
        text,
        stat.S_IMODE(file_stat.st_mode),
        True,
        _identity(file_stat),
    )


def _prepare_write_at(
    root_fd: int,
    root: Path,
    relative_path: str,
    content: str,
    event: str,
) -> _PreparedWrite:
    parent_fd, leaf_name = _open_parent_at(
        root_fd,
        relative_path,
        create=False,
    )
    try:
        original_text, mode, existed, original_identity = _read_leaf_at(
            parent_fd,
            leaf_name,
        )
    finally:
        if parent_fd is not None:
            os.close(parent_fd)
    return _PreparedWrite(
        path=root / relative_path,
        relative_path=relative_path,
        content=content,
        original_text=original_text,
        mode=mode,
        existed=existed,
        original_identity=original_identity,
        event=event,
    )


def _atomic_write_at(
    parent_fd: int,
    leaf_name: str,
    content: str,
    mode: int,
) -> tuple[int, int]:
    temp_name = ""
    temp_fd: int | None = None
    for _ in range(16):
        temp_name = f".{leaf_name}.{secrets.token_hex(8)}.tmp"
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
            raise ProjectWriteError(
                "this platform cannot create fd-relative temporary files"
            ) from exc
    if temp_fd is None:
        raise ProjectWriteError("could not allocate a unique temporary file")
    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fchmod(handle.fileno(), mode)
        temp_fd = None
        try:
            os.replace(
                temp_name,
                leaf_name,
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
            )
        except (NotImplementedError, TypeError) as exc:
            raise ProjectWriteError(
                "this platform cannot replace project files fd-relatively"
            ) from exc
        return _identity(os.stat(
            leaf_name,
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


def _rollback_writes(
    completed: list[_CompletedWrite],
    created_dirs: list[_CreatedDirectory],
) -> list[str]:
    errors: list[str] = []
    for completed_write in reversed(completed):
        write = completed_write.write
        try:
            current = os.stat(
                completed_write.leaf_name,
                dir_fd=completed_write.parent_fd,
                follow_symlinks=False,
            )
            if _identity(current) != completed_write.installed_identity:
                raise OSError("target changed after AKOS wrote it")
            if write.existed:
                _atomic_write_at(
                    completed_write.parent_fd,
                    completed_write.leaf_name,
                    write.original_text,
                    write.mode,
                )
            else:
                os.unlink(
                    completed_write.leaf_name,
                    dir_fd=completed_write.parent_fd,
                )
        except (OSError, ProjectPathError, ProjectWriteError) as e:
            errors.append(f"{write.path}: {e}")
    for directory in reversed(created_dirs):
        try:
            current = os.stat(
                directory.name,
                dir_fd=directory.parent_fd,
                follow_symlinks=False,
            )
            if _identity(current) != directory.identity:
                continue
            os.rmdir(directory.name, dir_fd=directory.parent_fd)
        except FileNotFoundError:
            pass
        except OSError:
            # A non-empty directory may predate a completed write in another
            # branch; never remove anything recursively during rollback.
            pass
    return errors


def _parent_still_anchored(
    root_fd: int,
    relative_path: str,
    expected_parent_fd: int,
) -> bool:
    current_parent_fd, _ = _open_parent_at(
        root_fd,
        relative_path,
        create=False,
    )
    if current_parent_fd is None:
        return False
    try:
        return _identity(os.fstat(current_parent_fd)) == _identity(
            os.fstat(expected_parent_fd)
        )
    finally:
        os.close(current_parent_fd)


def _commit_writes(root_fd: int, writes: list[_PreparedWrite]) -> None:
    created_dirs: list[_CreatedDirectory] = []
    completed: list[_CompletedWrite] = []
    open_parent_fds: list[int] = []
    try:
        for write in writes:
            if write.content == write.original_text:
                continue
            parent_fd, leaf_name = _open_parent_at(
                root_fd,
                write.relative_path,
                create=True,
                created=created_dirs,
            )
            assert parent_fd is not None
            open_parent_fds.append(parent_fd)
            current_text, _, current_existed, current_identity = _read_leaf_at(
                parent_fd,
                leaf_name,
            )
            if (
                current_existed != write.existed
                or current_identity != write.original_identity
                or current_text != write.original_text
            ):
                raise ProjectPathError(
                    f"project target changed during installation: {write.path}"
                )
            installed_identity = _atomic_write_at(
                parent_fd,
                leaf_name,
                write.content,
                write.mode,
            )
            completed.append(_CompletedWrite(
                write=write,
                parent_fd=parent_fd,
                leaf_name=leaf_name,
                installed_identity=installed_identity,
            ))
            if not _parent_still_anchored(
                root_fd,
                write.relative_path,
                parent_fd,
            ):
                raise ProjectPathError(
                    f"project parent changed during installation: {write.path.parent}"
                )
    except (OSError, ProjectPathError, ProjectWriteError) as e:
        rollback_errors = _rollback_writes(completed, created_dirs)
        suffix = (
            f"; rollback also failed for: {', '.join(rollback_errors)}"
            if rollback_errors
            else "; all completed writes were rolled back"
        )
        raise ProjectWriteError(f"project installation write failed: {e}{suffix}") from e
    finally:
        for parent_fd in open_parent_fds:
            try:
                os.close(parent_fd)
            except OSError:
                pass
        for directory in created_dirs:
            for fd in (directory.parent_fd, directory.directory_fd):
                try:
                    os.close(fd)
                except OSError:
                    pass


def install_project_files(
    project_root: Path, marked_bodies: dict[str, str]
) -> ProjectInstallResult:
    """Prepare every project mutation, then apply it as a reversible batch.

    The caller may name the project root through a symlink; that explicit root
    is resolved once. No path component beneath it may be a symlink, including
    the four managed files, their parents, or `.gitignore`.
    """
    if set(marked_bodies) != set(PROJECT_MARKED_PATHS):
        raise ValueError(
            "install_project_files requires exactly the four AKOS managed paths"
        )
    root = _resolve_project_root(Path(project_root))
    # Retain the path-level preflight for clear diagnostics, then anchor every
    # read/write/rollback beneath one no-follow root descriptor.
    targets = {
        relative: _safe_project_child(root, relative)
        for relative in (*PROJECT_MARKED_PATHS, GITIGNORE_PATH)
    }
    root_fd = os.open(root, _directory_open_flags())
    try:
        try:
            fcntl.flock(root_fd, fcntl.LOCK_EX)
        except OSError as exc:
            raise ProjectPathError(
                f"could not lock project root for installation: {exc}"
            ) from exc
        writes: list[_PreparedWrite] = []
        events: list[str] = []
        for relative in PROJECT_MARKED_PATHS:
            parent_fd, leaf_name = _open_parent_at(
                root_fd,
                relative,
                create=False,
            )
            try:
                original, _, _, _ = _read_leaf_at(parent_fd, leaf_name)
            finally:
                if parent_fd is not None:
                    os.close(parent_fd)
            path = targets[relative]
            state = classify(original)
            if state.status == INVALID:
                raise ValueError(
                    f"{path}: invalid marker structure ({'; '.join(state.reasons)})"
                )
            content = render_write(original, marked_bodies[relative])
            verb = {
                ABSENT: "created" if not original else "appended to",
                PRESENT: "updated",
            }[state.status]
            event = f"{verb} {path}"
            writes.append(_prepare_write_at(
                root_fd,
                root,
                relative,
                content,
                event,
            ))
            events.append(event)

        gitignore = targets[GITIGNORE_PATH]
        parent_fd, leaf_name = _open_parent_at(
            root_fd,
            GITIGNORE_PATH,
            create=False,
        )
        try:
            gitignore_text, _, _, _ = _read_leaf_at(parent_fd, leaf_name)
        finally:
            if parent_fd is not None:
                os.close(parent_fd)
        gitignore_content, gitignore_added = _render_gitignore(gitignore_text)
        if gitignore_added:
            event = f"added {GITIGNORE_ENTRY} to {gitignore}"
            writes.append(_prepare_write_at(
                root_fd,
                root,
                GITIGNORE_PATH,
                gitignore_content,
                event,
            ))
            events.append(event)

        _commit_writes(root_fd, writes)
        return ProjectInstallResult(tuple(events), gitignore_added)
    finally:
        os.close(root_fd)


def _managed_body(text: str, state: MarkerState) -> str:
    assert state.status == PRESENT
    lines = text.splitlines()
    return "\n".join(lines[state.start_line + 1 : state.end_line])


def _with_personal_profile(body: str, profile_name: str) -> str:
    lines = body.splitlines()
    replacement = f"personal_profile: {profile_name}"
    if any(line.startswith("personal_profile:") for line in lines):
        return "\n".join(
            replacement if line.startswith("personal_profile:") else line
            for line in lines
        )
    return "\n".join([
        *lines,
        "",
        "## Personal profile",
        replacement,
    ])


def set_project_personal_profile(
    project_root: Path,
    profile_name: str,
) -> Path:
    """Update the managed project config without following child symlinks."""
    root = _resolve_project_root(Path(project_root))
    target = _safe_project_child(root, PROFILE_CONFIG_PATH)
    root_fd = os.open(root, _directory_open_flags())
    try:
        try:
            fcntl.flock(root_fd, fcntl.LOCK_EX)
        except OSError as exc:
            raise ProjectPathError(
                f"could not lock project root for profile update: {exc}"
            ) from exc

        parent_fd, leaf_name = _open_parent_at(
            root_fd,
            PROFILE_CONFIG_PATH,
            create=False,
        )
        if parent_fd is None:
            raise ProjectPathError(f"project config parent does not exist: {target.parent}")
        try:
            original, mode, existed, original_identity = _read_leaf_at(
                parent_fd,
                leaf_name,
            )
        finally:
            os.close(parent_fd)
        if not existed or original_identity is None:
            raise ProjectPathError(f"project config does not exist: {target}")

        state = classify(original)
        if state.status != PRESENT:
            detail = (
                "; ".join(state.reasons)
                if state.reasons
                else f"no AKOS-managed section ({state.status})"
            )
            raise ValueError(f"{target}: {detail}")
        body = _with_personal_profile(_managed_body(original, state), profile_name)
        content = render_write(original, body)
        _commit_writes(root_fd, [_PreparedWrite(
            path=target,
            relative_path=PROFILE_CONFIG_PATH,
            content=content,
            original_text=original,
            mode=mode,
            existed=True,
            original_identity=original_identity,
            event=f"updated {target}",
        )])
        return target
    finally:
        os.close(root_fd)


def _check_body(body_lines: list[str]) -> None:
    for line in body_lines:
        if _is_marker_line(line, MARK_START) or _is_marker_line(line, MARK_END):
            raise MarkerBodyError(
                f"the body to write contains a line matching a marker ({line.strip()!r}) — refusing"
            )


def render_write(text: str, body: str) -> str:
    """Pure function: given the target file's current text and the new body,
    return the new full file text. Raises MarkerBodyError / ValueError on a
    body containing a marker line, or on an INVALID current structure."""
    state = classify(text)
    if state.status == INVALID:
        raise ValueError(f"refusing to write: current structure is invalid ({'; '.join(state.reasons)})")

    body_lines = body.splitlines()
    _check_body(body_lines)

    style, has_trailing_newline = _detect_style(text)
    block_lines = [MARK_START, *body_lines, MARK_END]

    if state.status == ABSENT:
        if not text:
            new_lines = block_lines
        else:
            existing_lines = text.splitlines()
            new_lines = [*existing_lines, "", *block_lines]
            has_trailing_newline = True  # the appended block always ends the file cleanly
    else:  # PRESENT
        lines = text.splitlines()
        new_lines = [*lines[: state.start_line], *block_lines, *lines[state.end_line + 1 :]]

    joined = style.join(new_lines)
    if has_trailing_newline or not text:
        joined += style
    return joined


def cmd_check(args) -> int:
    path = Path(args.file)
    try:
        text = _read_target_text(path)
    except NotARegularFileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"error: could not read {path}: {e}", file=sys.stderr)
        return 1

    state = classify(text)
    if state.status == PRESENT:
        print(f"PRESENT (lines {state.start_line + 1}-{state.end_line + 1})")
        return 0
    if state.status == ABSENT:
        print("ABSENT")
        return 0
    print("INVALID")
    for reason in state.reasons:
        print(f"  - {reason}")
    return 2


def cmd_extract(args) -> int:
    path = Path(args.file)
    try:
        text = _read_target_text(path)
    except NotARegularFileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"error: could not read {path}: {e}", file=sys.stderr)
        return 1

    state = classify(text)
    if state.status != PRESENT:
        print(f"error: no section to extract ({state.status})", file=sys.stderr)
        for reason in state.reasons:
            print(f"  - {reason}", file=sys.stderr)
        return 2

    print(_managed_body(text, state))
    return 0


def cmd_write(args) -> int:
    path = Path(args.file)
    if args.body_file == "-":
        body = sys.stdin.read()
    else:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as e:
            print(f"error: could not read body file {args.body_file}: {e}", file=sys.stderr)
            return 1

    try:
        text = _read_target_text(path)
    except NotARegularFileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"error: could not read {path}: {e}", file=sys.stderr)
        return 1

    state = classify(text)
    if state.status == INVALID:
        print(f"error: refusing to write — current structure of {path} is invalid:", file=sys.stderr)
        for reason in state.reasons:
            print(f"  - {reason}", file=sys.stderr)
        return 2

    try:
        new_text = render_write(text, body)
    except MarkerBodyError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    mode = path.stat().st_mode & 0o777 if path.is_file() else _default_create_mode()
    try:
        _atomic_write(path, new_text, mode)
    except OSError as e:
        print(f"error: could not write {path}: {e}", file=sys.stderr)
        return 1

    verb = {"ABSENT": "created" if not text else "appended to", "PRESENT": "updated"}[state.status]
    print(f"{verb} {path}")
    return 0


def cmd_validate_all(args) -> int:
    any_invalid = False
    for file_arg in args.files:
        path = Path(file_arg)
        try:
            text = _read_target_text(path)
        except NotARegularFileError as e:
            print(f"{path}: error: {e}")
            any_invalid = True
            continue
        except OSError as e:
            print(f"{path}: error: could not read: {e}")
            any_invalid = True
            continue
        state = classify(text)
        if state.status == INVALID:
            any_invalid = True
            print(f"{path}: INVALID")
            for reason in state.reasons:
                print(f"  - {reason}")
        else:
            print(f"{path}: {state.status}")
    return 2 if any_invalid else 0


def cmd_install_project(args) -> int:
    bodies = {
        "CLAUDE.md": args.claude_body,
        "AGENTS.md": args.agents_body,
        ".cursor/rules/akos.mdc": args.cursor_body,
        ".akos/config.md": args.config_body,
    }
    try:
        result = install_project_files(Path(args.project_dir), bodies)
    except ProjectPathError as e:
        print(f"error: unsafe project path: {e}", file=sys.stderr)
        return 1
    except ProjectWriteError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except (MarkerBodyError, ValueError) as e:
        print(f"error: ambiguous marker structure or invalid body: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"error: could not prepare project installation: {e}", file=sys.stderr)
        return 1

    for event in result.events:
        print(event)
    return 0


def cmd_set_personal_profile(args) -> int:
    try:
        path = set_project_personal_profile(
            Path(args.project_dir),
            args.profile_name,
        )
    except ProjectPathError as e:
        print(f"error: unsafe project path: {e}", file=sys.stderr)
        return 1
    except ProjectWriteError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"error: invalid AKOS-managed config: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"error: could not update project profile: {e}", file=sys.stderr)
        return 1
    print(f"updated {path}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check")
    p_check.add_argument("file")

    p_extract = sub.add_parser("extract")
    p_extract.add_argument("file")

    p_write = sub.add_parser("write")
    p_write.add_argument("file")
    body_group = p_write.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--body-file", metavar="PATH")
    body_group.add_argument("--body", choices=["-"], help="read the body from stdin")

    p_validate_all = sub.add_parser("validate-all")
    p_validate_all.add_argument("files", nargs="+")

    p_install = sub.add_parser("install-project")
    p_install.add_argument("project_dir")
    p_install.add_argument("--claude-body", required=True)
    p_install.add_argument("--agents-body", required=True)
    p_install.add_argument("--cursor-body", required=True)
    p_install.add_argument("--config-body", required=True)

    p_profile = sub.add_parser("set-personal-profile")
    p_profile.add_argument("project_dir")
    p_profile.add_argument("profile_name")

    args = ap.parse_args(argv)
    if args.cmd == "write" and args.body == "-":
        args.body_file = "-"

    return {
        "check": cmd_check,
        "extract": cmd_extract,
        "write": cmd_write,
        "validate-all": cmd_validate_all,
        "install-project": cmd_install_project,
        "set-personal-profile": cmd_set_personal_profile,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
