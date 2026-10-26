"""Heuristic for API routes whose shared auth hook is token-gated.

shortcut: detects same-file, same-line-condition patterns; upgrade to AST and
cross-module analysis when supporting additional framework registration shapes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "schemas"))
from io_utils import read_text_file  # noqa: E402
from secret_utils import mask_js_comments  # noqa: E402

API_ROUTE_CALL_RE = re.compile(r"\b(?:get|post|put|patch|delete|route)\s*\(", re.IGNORECASE)
TOKEN_GUARD_RE = re.compile(r"\bif\s*\([^\n)]*\bapiToken\b[^\n)]*\)\s*\{")
AUTH_HOOK_CALL_RE = re.compile(r"\baddHook\s*\(")


def _mask_strings(text: str) -> str:
    chars = list(text)
    index = 0
    while index < len(text):
        if text[index] not in "'\"`":
            index += 1
            continue
        quote = text[index]
        chars[index] = " "
        index += 1
        escaped = False
        while index < len(text):
            char = text[index]
            if char == "\n":
                if quote != "`":
                    break
            elif escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                chars[index] = " "
                index += 1
                break
            chars[index] = " "
            index += 1
    return "".join(chars)


def _has_api_route(text: str, code: str) -> bool:
    for match in API_ROUTE_CALL_RE.finditer(code):
        path = re.match(r"\s*(['\"`])\/api\/", text[match.end():])
        if path:
            return True
    return False


def _has_request_hook(body: str) -> bool:
    code = _mask_strings(body)
    for match in AUTH_HOOK_CALL_RE.finditer(code):
        name = re.match(r"\s*(['\"])onRequest\1\s*,", body[match.end():])
        if name:
            return True
    return False


def _guard_body(text: str, opening: int) -> str:
    depth = 1
    quote = None
    escaped = False
    for index in range(opening + 1, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"`":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[opening + 1:index]
    return ""


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        text = mask_js_comments(read_text_file(path))
        code = _mask_strings(text)
        if not _has_api_route(text, code):
            continue
        for match in TOKEN_GUARD_RE.finditer(code):
            opening = match.end() - 1
            if not _has_request_hook(_guard_body(text, opening)):
                continue
            line_number = code.count("\n", 0, match.start())
            findings.append({
                "evidence": [{
                    "path": str(path),
                    "line_start": line_number + 1,
                    "line_end": line_number + 1,
                    "snippet": "API request hook is registered only inside an apiToken condition",
                }],
            })
            break
    return findings
