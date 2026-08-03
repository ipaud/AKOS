"""Detector for A11Y_SELECT_NO_LABEL — deliberately Level B (heuristic), not A.

Same shape as A11Y_INPUT_NO_LABEL, and strictly worse when it fires: a
`<select>` with no name has no placeholder fallback at all, so an unlabeled
select has zero accessible name in any modality, where an unlabeled input at
least usually carries a placeholder giving a screen reader *something*. Split
into its own rule ID rather than folded into A11Y_INPUT_NO_LABEL — the tag
pattern, not just the tag name, differs (no `type=` attribute to skip
hidden/submit/button variants against), and a separate rule ID lets a reader
re-run exactly this check.

Found as a real gap, not designed speculatively: two independent AKOS review
runs on the same held-out repo (2026-07-31 and 2026-08-01) had the
accessibility lens confirm all five A11Y_INPUT_NO_LABEL leads, then
independently flag two unlabeled `<select>` elements the input-only pattern
could not catch. Shares its tag-scanning helpers with A11Y_INPUT_NO_LABEL via
schemas/a11y_dom_utils.py — see that module's docstring before changing
either detector's matching logic.
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

# Case-SENSITIVE on the tag name, for the same reason as A11Y_INPUT_NO_LABEL:
# `<Select>` (capitalised) is a React component whose label almost always
# comes from its wrapper, not the native `<select>` this rule targets.
SELECT_OPEN_RE = re.compile(r"<select\b")


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        text = read_text_file(path)
        text = mask_source_comments(text, include_js=path.suffix.lower() != ".html")

        for m in SELECT_OPEN_RE.finditer(text):
            end = tag_span(text, m.start())
            if end is None:
                continue
            tag = text[m.start():end]
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
