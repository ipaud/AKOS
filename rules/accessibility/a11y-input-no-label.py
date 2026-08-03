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

Shares its tag-scanning helpers with A11Y_SELECT_NO_LABEL via
schemas/a11y_dom_utils.py — same heuristic shape, same false-positive and
false-negative fixes already learned against a real corpus. See that
module's docstring before changing either detector's matching logic.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "schemas"))
from a11y_dom_utils import (  # noqa: E402
    has_id_bound_label,
    has_nonempty_aria_name,
    has_wrapping_label,
    mask_source_comments,
    tag_span,
)
from io_utils import read_text_file  # noqa: E402

# Case-SENSITIVE on the tag name, deliberately. JSX capitalises components to
# distinguish them from HTML elements, so `<Input>` is a React component whose
# label almost always comes from the wrapper that renders it (`<Field label=…>`),
# while `<input>` is the element this rule is actually about. With IGNORECASE,
# 110 of 122 findings on a real design-system codebase pointed at components —
# and buried the 12 genuine `<input>` elements underneath them.
INPUT_OPEN_RE = re.compile(r"<input\b")
SKIP_TYPES = {"hidden", "submit", "button", "reset", "image"}
TYPE_RE = re.compile(r'type\s*=\s*["\']?(\w+)', re.IGNORECASE)


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        text = read_text_file(path)
        text = mask_source_comments(text, include_js=path.suffix.lower() != ".html")

        for m in INPUT_OPEN_RE.finditer(text):
            end = tag_span(text, m.start())
            if end is None:
                continue
            tag = text[m.start():end]
            type_m = TYPE_RE.search(tag)
            if type_m and type_m.group(1).lower() in SKIP_TYPES:
                continue
            if has_nonempty_aria_name(tag):
                continue
            if has_id_bound_label(text, tag):
                continue
            if has_wrapping_label(text, m.start(), m.end()):
                continue

            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "evidence": [{"path": str(path), "line_start": line, "line_end": line,
                              "snippet": tag[:100].replace("\n", " ")}],
            })
    return findings
