"""Shared fail-closed input reading for executable rules."""

from __future__ import annotations

import errno
import stat
from pathlib import Path


def read_text_file(path: Path) -> str:
    """Read one detector input and deliberately propagate every ``OSError``.

    The runner converts the propagated error into
    ``ExecutionError(phase="read")``. Detectors must never turn an unreadable
    file into an omitted input and a potentially false clean result.
    """
    return path.read_text(encoding="utf-8", errors="replace")


def read_regular_text_file(path: Path) -> str:
    """Read an auxiliary input without following symlinks or special files."""
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        raise OSError(errno.ELOOP, "refusing symlinked detector input", str(path))
    if not stat.S_ISREG(mode):
        raise OSError(errno.EINVAL, "detector input is not a regular file", str(path))
    return read_text_file(path)
