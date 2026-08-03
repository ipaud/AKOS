"""Shared tag-scanning helpers for the accessible-name detectors.

Used by A11Y_INPUT_NO_LABEL and A11Y_SELECT_NO_LABEL — same Level-B text
heuristic (comment-masked regex, not a DOM parse), same false-positive and
false-negative shape, same fixes for the same real bugs (JSX `htmlFor` vs
HTML `for`, brace-aware tag-span scanning so a `>` inside a prop expression
doesn't truncate the tag, comment masking so a commented-out element isn't
flagged and a commented-out label doesn't suppress a real one). Extracted
here rather than duplicated per detector, because a bug fixed in one copy
and not the other is exactly the drift this shared module exists to
prevent — see the case-by-case comments below for what was already learned
against a real corpus and would otherwise need relearning per tag.

Lives in schemas/, not rules/accessibility/, for the same reason
secret_utils.py does: it is not itself a rule (no registry YAML, never
discovered by the runner's glob).
"""

from __future__ import annotations

import re

from secret_utils import mask_js_comments

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
ID_RE = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
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


def tag_span(text: str, start: int) -> tuple[int, int] | None:
    """End offset of the tag opened at `start`, brace-aware.

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
    # A <label> opened before this element and not yet closed, or the element
    # is immediately followed by a closing </label> — a loose but useful
    # heuristic for the common "wrap the field in a label" pattern.
    if before.rfind("<label") > before.rfind("</label>") and "<label" in before:
        return True
    if "</label>" in after and "<label" not in after[: after.find("</label>")]:
        return True
    return False


def has_id_bound_label(text: str, tag: str) -> bool:
    """True if the tag's `id` is targeted by a `<label for=/htmlFor=>` anywhere."""
    id_m = ID_RE.search(tag)
    if not id_m:
        return False
    input_id = re.escape(id_m.group(1))
    return bool(re.search(LABEL_FOR_TEMPLATE.format(id=input_id), text, re.IGNORECASE))
