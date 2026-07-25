"""Detector for A11Y_INPUT_NO_LABEL — deliberately Level B (heuristic), not A.

True label association is a tree-structural relationship (wrapping <label>,
for/id matching where either can be set via a variable, aria-labelledby
pointing elsewhere, or — very commonly in component libraries — the label
living in a sibling JSX subtree connected only through form-library context).
A regex over text cannot reliably resolve any of that. This produces both
false positives (correctly-labeled inputs via a wrapping custom component)
and false negatives (conditionally-rendered blocks, multi-line prop
spreads) at a real rate — which is exactly why this rule is capped at
MEDIUM severity and excluded from CRITICAL-only gating, regardless of the
active profile.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "schemas"))
from io_utils import read_text_file  # noqa: E402
from secret_utils import mask_js_comments  # noqa: E402

# Case-SENSITIVE on the tag name, deliberately. JSX capitalises components to
# distinguish them from HTML elements, so `<Input>` is a React component whose
# label almost always comes from the wrapper that renders it (`<Field label=…>`),
# while `<input>` is the element this rule is actually about. With IGNORECASE,
# 110 of 122 findings on a real design-system codebase pointed at components —
# and buried the 12 genuine `<input>` elements underneath them.
INPUT_OPEN_RE = re.compile(r"<input\b")
SKIP_TYPES = {"hidden", "submit", "button", "reset", "image"}
TYPE_RE = re.compile(r'type\s*=\s*["\']?(\w+)', re.IGNORECASE)
ID_RE = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
ARIA_NAME_RE = re.compile(
    r"""\baria-label(?:ledby)?\s*=\s*
        (?:
            "([^"]*)"
          | '([^']*)'
          | \{([^{}]*)\}
          | ([^\s>]+)
        )
    """,
    re.IGNORECASE | re.VERBOSE,
)
LABEL_FOR_TEMPLATE = r'<label\b[^>]*\b(?:for|htmlFor)\s*=\s*["\']{id}["\']'
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

SEARCH_WINDOW = 400  # chars of surrounding context to check for a wrapping <label>


def mask_source_comments(text: str, *, include_js: bool = True) -> str:
    """Mask JS/JSX and HTML comments without changing offsets or line numbers."""
    masked = mask_js_comments(text) if include_js else text

    def blank(match: re.Match) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return HTML_COMMENT_RE.sub(blank, masked)


def has_nonempty_aria_name(tag: str) -> bool:
    """Treat only a non-empty literal or a non-trivial expression as a name.

    A dynamic JSX expression cannot be resolved by this Level-B text detector,
    so it remains a sufficient signal. Explicit empty string literals are
    checkable and must not silence the rule.
    """
    for match in ARIA_NAME_RE.finditer(tag):
        double_quoted, single_quoted, expression, unquoted = match.groups()
        if double_quoted is not None:
            if double_quoted.strip():
                return True
            continue
        if single_quoted is not None:
            if single_quoted.strip():
                return True
            continue
        if expression is not None:
            value = expression.strip()
            if not value or re.fullmatch(r"""(?:"\s*"|'\s*'|`\s*`)""", value):
                continue
            return True
        if unquoted and unquoted.strip():
            return True
    return False


def input_tag_span(text: str, start: int) -> tuple[int, int] | None:
    """End offset of the <input ...> tag opened at `start`, brace-aware.

    A plain `[^>]*` scan cannot be used on JSX: `onChange={(e) => setQ(...)}`
    contains a `>` inside a prop expression, so the tag was truncated at the
    arrow and every attribute after it — very often the `aria-label` — went
    unseen. On the first real repository this ran against, 8 of 21 findings
    were correctly-labelled inputs missed exactly this way.

    Tracks brace depth and quote state, so `>` only closes the tag at depth 0
    outside a string.
    """
    depth = 0
    quote = None
    i = start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == ">" and depth == 0:
            return i + 1
        i += 1
    return None


def has_wrapping_label(text: str, tag_start: int, tag_end: int) -> bool:
    window_start = max(0, tag_start - SEARCH_WINDOW)
    window_end = min(len(text), tag_end + SEARCH_WINDOW)
    before = text[window_start:tag_start]
    after = text[tag_end:window_end]
    # A <label> opened before this input and not yet closed, or the input
    # is immediately followed by a closing </label> — a loose but useful
    # heuristic for the common "wrap the input in a label" pattern.
    if before.rfind("<label") > before.rfind("</label>") and "<label" in before:
        return True
    if "</label>" in after and "<label" not in after[: after.find("</label>")]:
        return True
    return False


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        text = read_text_file(path)
        text = mask_source_comments(text, include_js=path.suffix.lower() != ".html")

        for m in INPUT_OPEN_RE.finditer(text):
            end = input_tag_span(text, m.start())
            if end is None:
                continue
            tag = text[m.start():end]
            type_m = TYPE_RE.search(tag)
            if type_m and type_m.group(1).lower() in SKIP_TYPES:
                continue
            if has_nonempty_aria_name(tag):
                continue

            id_m = ID_RE.search(tag)
            if id_m:
                input_id = re.escape(id_m.group(1))
                if re.search(LABEL_FOR_TEMPLATE.format(id=input_id), text, re.IGNORECASE):
                    continue

            if has_wrapping_label(text, m.start(), m.end()):
                continue

            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "evidence": [{"path": str(path), "line_start": line, "line_end": line,
                              "snippet": tag[:100].replace("\n", " ")}],
            })
    return findings
