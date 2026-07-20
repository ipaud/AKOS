"""Shared helpers for SECRET_IN_SOURCE and SERVICE_ROLE_IN_CLIENT. Not a rule
itself — no registry YAML, never discovered by the runner's glob.
"""

from __future__ import annotations

import base64
import json
import math
import re
from pathlib import Path, PurePosixPath

DENYLIST_SUBSTRINGS = [
    "changeme", "placeholder", "your-api-key", "your_api_key", "example",
    "dummy", "xxxxxxxx", "insert-key-here", "replace-me", "<key>", "sk_test_000",
]

VENDOR_PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "stripe_live_key": re.compile(r"sk_live_[A-Za-z0-9]{16,}"),
    "stripe_test_key": re.compile(r"sk_test_[A-Za-z0-9]{16,}"),
}

GENERIC_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    \b(?:api[_-]?key|secret|token|password|service_role[_-]?key)\b
    \s*[:=]\s*
    ['"]([^'"]{16,})['"]
    """
)

JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\b")

FIXTURE_DIR_SEGMENTS = {"test", "tests", "spec", "specs", "fixtures", "fixture", "__mocks__", "mocks"}
FIXTURE_FILENAME_MARKERS = (".example", ".sample", ".template")


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    length = len(s)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())


def looks_like_placeholder(value: str) -> bool:
    low = value.lower()
    return any(d in low for d in DENYLIST_SUBSTRINGS)


def is_fixture_or_doc_path(path_str: str) -> bool:
    """Match whole path SEGMENTS and filename markers, not arbitrary
    substrings — a naive substring check would skip real production files
    like `src/testUtils.ts` or anything under a directory that merely
    contains "test" as part of a longer name (e.g. a repo checked out into
    a path like `.../my-test-project/...`)."""
    p = PurePosixPath(path_str.replace("\\", "/"))
    parts_lower = {part.lower() for part in p.parts}
    if parts_lower & FIXTURE_DIR_SEGMENTS:
        return True
    name_lower = p.name.lower()
    if name_lower.endswith(".md"):
        return True
    return any(marker in name_lower for marker in FIXTURE_FILENAME_MARKERS)


def decode_jwt_claims(token: str) -> dict | None:
    """Structurally decode a JWT's payload — no signature verification, just
    base64url-decode the middle segment to inspect the 'role' claim."""
    parts = token.split(".")
    if len(parts) != 3:
        return None
    payload = parts[1]
    padding = "=" * (-len(payload) % 4)
    try:
        decoded = base64.urlsafe_b64decode(payload + padding)
        return json.loads(decoded)
    except (ValueError, json.JSONDecodeError):
        return None


def redact_secrets(text: str) -> tuple[str, list[str]]:
    """Replace anything that looks like a live credential with a labelled
    marker. Returns (redacted_text, labels_of_what_was_removed).

    Used when a review report is copied into a project's .akos/reviews/.
    A security review is *required* to quote the credential it found — the
    report format demands concrete evidence — so the audit trail is exactly
    where secrets accumulate, and it lands in a directory the consuming
    project may well commit. Redaction therefore happens at write time, not
    at display time: once the file exists, it is too late.

    Deliberately aggressive. A false positive costs a reviewer one redacted
    string they can still find in the source; a false negative pushes a live
    key to a remote. The asymmetry is not close, so this does not try to be
    clever about whether a match is 'really' a secret.
    """
    labels: list[str] = []

    def _mark(label: str) -> str:
        if label not in labels:
            labels.append(label)
        return f"[REDACTED:{label}]"

    for name, pattern in VENDOR_PATTERNS.items():
        text, n = pattern.subn(lambda m, nm=name: _mark(nm), text)
        if n == 0 and name in labels:
            labels.remove(name)

    # A JWT is only a secret when it carries service_role; anon and
    # authenticated keys are designed to be public and RLS constrains them.
    # Redacting those would strip evidence a reviewer legitimately needs.
    def _jwt(m):
        claims = decode_jwt_claims(m.group(0))
        if claims and claims.get("role") == "service_role":
            return _mark("service_role_jwt")
        return m.group(0)

    text = JWT_RE.sub(_jwt, text)

    def _assignment(m):
        value = m.group(1)
        if looks_like_placeholder(value) or shannon_entropy(value) < 3.0:
            return m.group(0)
        return m.group(0).replace(value, _mark("high_entropy_assignment"))

    text = GENERIC_ASSIGNMENT_RE.sub(_assignment, text)
    return text, labels


def gitignored_paths(paths: list) -> set:
    """Subset of `paths` that git ignores. Empty set if git is unavailable.

    This rule's title is "secret literal **committed to source**". A key in a
    gitignored `.env` is not committed — it is in the one place it is supposed
    to be. Reporting it CRITICAL is the false positive this exists to prevent,
    found on the first real repository this ran against, where a correctly
    stored `service_role` key in an ignored `.env` was flagged as a leak.

    One `git check-ignore --stdin` call for the whole batch rather than one
    per file: the per-file version made the scan cost a subprocess per source
    file, which is how a check like this quietly becomes too slow to keep on.
    """
    import subprocess
    from collections import defaultdict

    if not paths:
        return set()

    # check-ignore resolves against a repo, so group by the repo each path is
    # in. Paths outside any repo cannot be ignored and are skipped.
    by_root = defaultdict(list)
    for p in paths:
        root = _git_root(Path(p))
        if root is not None:
            by_root[root].append(Path(p))

    ignored = set()
    for root, group in by_root.items():
        try:
            proc = subprocess.run(
                ["git", "check-ignore", "--stdin"],
                cwd=root, input="\n".join(str(p) for p in group),
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        # Exit 0 = some paths ignored, 1 = none, other = error. Trust only
        # 0 and 1; anything else means the answer is unknown, and an unknown
        # must not silently read as "not ignored" for every file at once.
        if proc.returncode not in (0, 1):
            continue
        ignored.update(line.strip() for line in proc.stdout.splitlines() if line.strip())
    return ignored


def _git_root(path: Path):
    for parent in [path if path.is_dir() else path.parent, *path.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def mask_js_comments(text: str) -> str:
    """Blank out //, /* */ and JSX {/* */} comments, preserving byte offsets.

    Line and column numbers stay valid because every masked character is
    replaced by a space rather than removed — the same contract as
    _sql_utils.mask_sql_comments.

    Needed because a rule that greps for an identifier finds it in the comment
    warning against it. On a real repository, SERVICE_ROLE_IN_CLIENT flagged
    `src/lib/supabase.ts` for a comment reading "A service_role key ... must
    NEVER be a VITE_* variable" — the detector reported the warning as the
    defect.

    String literals are skipped so a `//` inside a URL is not treated as a
    comment.
    """
    out = list(text)
    i, n = 0, len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'`":
            quote = ch
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                out[i] = " "
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            while i < n and not (text[i] == "*" and i + 1 < n and text[i + 1] == "/"):
                if text[i] != "\n":
                    out[i] = " "
                i += 1
            for _ in range(2):
                if i < n:
                    out[i] = " "
                    i += 1
            continue
        i += 1
    return "".join(out)
