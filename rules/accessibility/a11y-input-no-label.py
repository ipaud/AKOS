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
from pathlib import Path

INPUT_TAG_RE = re.compile(r"<input\b[^>]*?/?>", re.IGNORECASE | re.DOTALL)
SKIP_TYPES = {"hidden", "submit", "button", "reset", "image"}
TYPE_RE = re.compile(r'type\s*=\s*["\']?(\w+)', re.IGNORECASE)
ID_RE = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
ARIA_LABEL_RE = re.compile(r"\baria-label(?:ledby)?\s*=", re.IGNORECASE)
LABEL_FOR_TEMPLATE = r'<label\b[^>]*\b(?:for|htmlFor)\s*=\s*["\']{id}["\']'

SEARCH_WINDOW = 400  # chars of surrounding context to check for a wrapping <label>


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
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for m in INPUT_TAG_RE.finditer(text):
            tag = m.group(0)
            type_m = TYPE_RE.search(tag)
            if type_m and type_m.group(1).lower() in SKIP_TYPES:
                continue
            if ARIA_LABEL_RE.search(tag):
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
