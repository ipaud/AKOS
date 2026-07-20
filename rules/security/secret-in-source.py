"""Detector for SECRET_IN_SOURCE.

Vendor-unique prefixes (AWS, GitHub, Slack, Stripe) match anywhere — near-zero
collision risk by construction, so those are Certain-confidence hits. The
generic KEY="..." catch-all additionally requires high entropy and a
denylist check, and skips fixture/doc/example paths, to keep the false-
positive rate down. A decodable JWT with a "service_role" claim escalates to
CRITICAL — that specific case is what SERVICE_ROLE_IN_CLIENT also checks for,
scoped to client-side paths.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _secret_utils import (  # noqa: E402
    VENDOR_PATTERNS, GENERIC_ASSIGNMENT_RE, JWT_RE,
    shannon_entropy, looks_like_placeholder, is_fixture_or_doc_path, decode_jwt_claims,
)

MIN_ENTROPY = 3.0


def run(files: list[Path]) -> list[dict]:
    findings = []
    for path in files:
        path_str = str(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for vendor, pattern in VENDOR_PATTERNS.items():
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                severity_override = "MEDIUM" if vendor == "stripe_test_key" else None
                findings.append({
                    "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                                  "snippet": f"{vendor} pattern matched"}],
                    "confidence_override": "Certain",
                    **({"severity_override": severity_override} if severity_override else {}),
                })

        for m in JWT_RE.finditer(text):
            claims = decode_jwt_claims(m.group(0))
            if not claims:
                continue
            role = claims.get("role")
            # anon/authenticated-role keys are DESIGNED to be public — safe
            # in a client bundle because RLS constrains what they can do.
            # Only service_role (which bypasses RLS entirely) is a secret.
            if role != "service_role":
                continue
            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                              "snippet": f"JWT with role={role!r}"}],
                "confidence_override": "Certain",
                "severity_override": "CRITICAL",
            })

        if is_fixture_or_doc_path(path_str):
            continue
        for m in GENERIC_ASSIGNMENT_RE.finditer(text):
            value = m.group(1)
            if looks_like_placeholder(value) or shannon_entropy(value) < MIN_ENTROPY:
                continue
            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                              "snippet": "high-entropy value assigned to a key/secret/token/password-like name"}],
            })
    return findings
