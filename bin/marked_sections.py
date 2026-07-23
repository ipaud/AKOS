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

Exit codes (the "new command" 0/1/2 scheme from docs/cli/exit-codes.md):
    0 — ran successfully, nothing to fail on
    1 — usage/file error (bad args, path is not a regular file, I/O error)
    2 — ran successfully, and found a problem (INVALID marker structure,
        a body containing a marker line, or a validate-all target that
        isn't safely writable)
"""

from __future__ import annotations

import argparse
import os
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


@dataclass
class MarkerState:
    status: str  # ABSENT | PRESENT | INVALID
    start_line: int | None = None  # 0-indexed, only set when status == PRESENT
    end_line: int | None = None
    reasons: tuple[str, ...] = ()  # only set when status == INVALID


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

    lines = text.splitlines()
    body_lines = lines[state.start_line + 1 : state.end_line]
    print("\n".join(body_lines))
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

    args = ap.parse_args(argv)
    if args.cmd == "write" and args.body == "-":
        args.body_file = "-"

    return {
        "check": cmd_check,
        "extract": cmd_extract,
        "write": cmd_write,
        "validate-all": cmd_validate_all,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
