"""Detector for SERVICE_ROLE_IN_CLIENT.

`applies_to.glob` already restricts scanning to conventional client-code
roots (src/, app/, pages/, client/). This detector additionally excludes
server-convention sub-paths within those roots (pages/api/**, **/server/**,
supabase/functions/**, *.server.ts, middleware.ts) that the glob alone can't
express cleanly.

Reuses SECRET_IN_SOURCE's JWT decoder: a decodable service_role JWT literal
under a client path is CRITICAL. The bare identifier/env-var name (e.g.
`process.env.SUPABASE_SERVICE_ROLE_KEY`) with no decodable key is HIGH — an
architectural smell (a server-only client factory imported into client code)
even if a bundler might tree-shake the actual value away. Checks source
files only, not bundle output — a secret that only reaches the bundle
through misconfiguration without appearing in any source file is a
different, more framework-specific analysis, out of scope here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "schemas"))
from io_utils import read_text_file  # noqa: E402
from secret_utils import JWT_RE, decode_jwt_claims, mask_js_comments, classification_path  # noqa: E402

SERVER_SOURCE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".mts", ".cts", ".mjs", ".cjs")
SERVICE_ROLE_RE = re.compile(r"service[_-]?role", re.IGNORECASE)


def _has_adjacent_parts(parts: tuple[str, ...], left: str, right: str) -> bool:
    return any(
        parts[index:index + 2] == (left, right)
        for index in range(len(parts) - 1)
    )


def is_server_convention_path(path: Path) -> bool:
    """Callers with a scan root must pass a path already relativized via
    classification_path. Only conventions that establish an actual server
    boundary are excluded: a generic ``src/api`` or ``src/functions`` folder
    can still be browser code, while an API ``route.*`` handler is server
    code regardless of whether the framework nests it under ``app``."""
    parts_lower = tuple(part.casefold() for part in path.parts)
    name_lower = path.name.casefold()

    if "server" in parts_lower:
        return True
    if ".server." in name_lower:
        return True
    if name_lower in {
        f"{stem}{suffix}"
        for stem in ("server", "middleware")
        for suffix in SERVER_SOURCE_SUFFIXES
    }:
        return True
    if _has_adjacent_parts(parts_lower, "pages", "api"):
        return True
    if (
        "api" in parts_lower
        and name_lower in {f"route{suffix}" for suffix in SERVER_SOURCE_SUFFIXES}
    ):
        return True
    return _has_adjacent_parts(parts_lower, "supabase", "functions")


def run(files: list[Path], scan_root: Path | None = None) -> list[dict]:
    findings = []
    for path in files:
        if is_server_convention_path(Path(classification_path(path, scan_root))):
            continue
        text = read_text_file(path)
        # A comment warning against putting a service_role key here is not a
        # service_role key being put here. Offsets are preserved, so line
        # numbers below stay correct.
        text = mask_js_comments(text)

        decodable_hit_lines = set()
        for m in JWT_RE.finditer(text):
            claims = decode_jwt_claims(m.group(0))
            if claims and claims.get("role") == "service_role":
                line = text.count("\n", 0, m.start()) + 1
                decodable_hit_lines.add(line)
                findings.append({
                    "evidence": [{"path": str(path), "line_start": line, "line_end": line,
                                  "snippet": "decodable service_role JWT literal under a client path"}],
                    "severity_override": "CRITICAL",
                    "confidence_override": "Certain",
                })

        for m in SERVICE_ROLE_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            if line in decodable_hit_lines:
                continue  # already reported as the stronger CRITICAL finding
            findings.append({
                "evidence": [{"path": str(path), "line_start": line, "line_end": line,
                              "snippet": "service_role identifier referenced in client-path code"}],
            })
    return findings
