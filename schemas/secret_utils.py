"""Shared secret-detection and redaction helpers.

Used by the SECRET_IN_SOURCE and SERVICE_ROLE_IN_CLIENT detectors, by
A11Y_INPUT_NO_LABEL for comment-masking, and by schemas/history.py to redact
credentials before a review report is written to a consuming project's
.akos/reviews/. Lives in schemas/ — a neutral module both rules/ and
schemas/ import — rather than under rules/security/, since it is not itself
a rule: no registry YAML, never discovered by the runner's glob.
"""

from __future__ import annotations

import base64
import json
import math
import re
from pathlib import Path, PurePosixPath

DENYLIST_SUBSTRINGS = [
    "changeme", "placeholder", "your-api-key", "your_api_key", "example",
    "dummy", "akos_test", "xxxxxxxx", "insert-key-here", "replace-me",
    "<key>", "sk_test_000",
]

OPENSSH_PRIVATE_KEY_BEGIN = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
OPENSSH_PRIVATE_KEY_END = "-----END " + "OPENSSH PRIVATE KEY-----"

PRIVATE_KEY_FAMILIES = {
    "rsa_private_key": "RSA " + "PRIVATE KEY",
    "ec_private_key": "EC " + "PRIVATE KEY",
    "pkcs8_private_key": "PRIVATE " + "KEY",
}


def _private_key_pattern(family: str) -> re.Pattern:
    begin = "-----BEGIN " + family + "-----"
    end = "-----END " + family + "-----"
    return re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)


VENDOR_PATTERNS = {
    "openssh_private_key": re.compile(
        re.escape(OPENSSH_PRIVATE_KEY_BEGIN)
        + r".*?"
        + re.escape(OPENSSH_PRIVATE_KEY_END),
        re.DOTALL,
    ),
    **{
        label: _private_key_pattern(family)
        for label, family in PRIVATE_KEY_FAMILIES.items()
    },
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_fine_grained_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "stripe_live_key": re.compile(r"sk_live_[A-Za-z0-9]{16,}"),
    "stripe_test_key": re.compile(r"sk_test_[A-Za-z0-9]{16,}"),
}

# The keyword may be the *suffix* of a longer name (STRIPE_API_KEY, myApiKey,
# DB_PASSWORD) — that is the dominant naming convention, not the exception.
# A leading \b cannot express that: `_` is a word character, so \b never fires
# between `STRIPE_` and `API_KEY`, and every prefixed name sailed past this
# pattern while the benchmark stayed green. The optional [A-Za-z0-9_.-]* prefix
# closes that. Quoted values retain the broad source-language name matching.
# Unquoted values are deliberately limited to environment-style UPPER_SNAKE
# secret names and token characters: otherwise ordinary references such as
# ``const token = options.apiToken`` look indistinguishable from literals.
# Placeholder and entropy gates below provide a second precision boundary.
GENERIC_ASSIGNMENT_RE = re.compile(
    r"""(?x)
    (?:
        (?:
            (?P<key_quote>['"])
            (?i:
                [A-Za-z0-9_.-]*
                (?:api[_-]?key|secret|token|password|service_role[_-]?key)\b
            )
            (?P=key_quote)
          |
            (?i:
                [A-Za-z0-9_.-]*
                (?:api[_-]?key|secret|token|password|service_role[_-]?key)\b
            )
        )
        \s*[:=]\s*
        (?P<quote>['"])
        (?P<quoted_value>[^'"\r\n]{16,})
        (?P=quote)
      |
        (?m:^[ \t]*(?:(?:export|ENV)[ \t]+)?)
        (?<![A-Za-z0-9_])
        (?:(?:[A-Z][A-Z0-9]*_)+)?
        (?:API_KEY|SECRET|TOKEN|PASSWORD|SERVICE_ROLE_KEY)\b
        \s*[:=]\s*
        (?P<unquoted_value>[A-Za-z0-9_+/=.-]{12,})
        (?=$|[\s,;#}\])>])
    )
    """
)
GENERIC_ASSIGNMENT_MIN_ENTROPY = 3.0

JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\b")
STANDALONE_QUOTED_RE = re.compile(
    r"""(?x)
    (?P<quote>['"])
    (?P<value>[A-Za-z0-9_+/=.-]{32,})
    (?P=quote)
    """
)
HEX_DIGEST_RE = re.compile(r"^[0-9a-fA-F]{32,}$")
SUBRESOURCE_INTEGRITY_RE = re.compile(
    r"^sha(?:1|256|384|512)-[A-Za-z0-9+/]+={0,2}$",
    re.IGNORECASE,
)
UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)
STANDALONE_MIN_ENTROPY = 4.0

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


def generic_assignment_value(
    match: re.Match,
) -> tuple[str, tuple[int, int], bool]:
    """Return value, exact span, and whether the unquoted syntax arm matched."""
    group_name = (
        "quoted_value"
        if match.group("quoted_value") is not None
        else "unquoted_value"
    )
    return (
        match.group(group_name),
        match.span(group_name),
        group_name == "unquoted_value",
    )


def is_generic_secret_assignment_value(
    value: str, *, unquoted: bool = False,
) -> bool:
    """Shared detector/history eligibility gate for generic assignments."""
    if (
        looks_like_placeholder(value)
        or shannon_entropy(value) < GENERIC_ASSIGNMENT_MIN_ENTROPY
    ):
        return False
    if unquoted and "." in value:
        return (
            any(char.islower() for char in value)
            and any(char.isupper() for char in value)
            and any(char.isdigit() for char in value)
        )
    return True


def spans_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def is_standalone_secret_candidate(value: str) -> bool:
    """Conservative entropy fallback for an opaque quoted literal.

    It intentionally excludes common non-secrets such as checksums and UUIDs
    and requires mixed character classes. Matches are advisory/non-blocking in
    the detector, but write-time redaction still removes them because copying a
    possible credential into review history has a much higher downside than
    asking the operator to inspect the original source.
    """
    if looks_like_placeholder(value):
        return False
    if JWT_RE.fullmatch(value):
        return False
    if (
        HEX_DIGEST_RE.fullmatch(value)
        or SUBRESOURCE_INTEGRITY_RE.fullmatch(value)
        or UUID_RE.fullmatch(value)
    ):
        return False
    if shannon_entropy(value) < STANDALONE_MIN_ENTROPY:
        return False
    return (
        any(ch.islower() for ch in value)
        and any(ch.isupper() for ch in value)
        and any(ch.isdigit() for ch in value)
    )


def iter_standalone_secret_matches(text: str, excluded_spans=()):
    """Yield quoted entropy candidates not already explained by stronger rules."""
    excluded = tuple(excluded_spans)
    for match in STANDALONE_QUOTED_RE.finditer(text):
        value_span = match.span("value")
        if any(spans_overlap(value_span, span) for span in excluded):
            continue
        if is_standalone_secret_candidate(match.group("value")):
            yield match


def classification_path(path, scan_root=None) -> str:
    """Path string to use for fixture/server-convention CLASSIFICATION.

    Relative to the scanned root whenever possible. Classifying the absolute
    path lets every ancestor directory ABOVE the project vote: a repo checked
    out under `/Users/bob/test/proj/` or `/tmp/fixtures/proj/` had all its
    real secrets downgraded to LOW because an ancestor segment happened to be
    named `test` or `fixtures`. Only segments inside the scanned tree may
    influence classification; the absolute path is still what gets read.
    """
    p = Path(path)
    if scan_root is None:
        return str(p)
    try:
        return str(p.resolve().relative_to(Path(scan_root).resolve()))
    except (ValueError, OSError):
        return str(p)


def is_fixture_or_doc_path(path_str: str) -> bool:
    """Match whole path SEGMENTS and filename markers, not arbitrary
    substrings — a naive substring check would skip real production files
    like `src/testUtils.ts` or anything under a directory that merely
    contains "test" as part of a longer name (e.g. a repo checked out into
    a path like `.../my-test-project/...`).

    Callers with a scan root must pass `classification_path(path, root)`
    rather than the raw absolute path — see that helper for why."""
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
        text = pattern.sub(lambda m, nm=name: _mark(nm), text)

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
        value, _, unquoted = generic_assignment_value(m)
        if not is_generic_secret_assignment_value(value, unquoted=unquoted):
            return m.group(0)
        return m.group(0).replace(value, _mark("high_entropy_assignment"))

    text = GENERIC_ASSIGNMENT_RE.sub(_assignment, text)

    def _standalone(match):
        value = match.group("value")
        if not is_standalone_secret_candidate(value):
            return match.group(0)
        return match.group(0).replace(value, _mark("standalone_high_entropy"))

    text = STANDALONE_QUOTED_RE.sub(_standalone, text)
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
