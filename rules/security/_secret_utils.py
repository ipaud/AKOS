"""Shared helpers for SECRET_IN_SOURCE and SERVICE_ROLE_IN_CLIENT. Not a rule
itself — no registry YAML, never discovered by the runner's glob.
"""

from __future__ import annotations

import base64
import json
import math
import re
from pathlib import PurePosixPath

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
