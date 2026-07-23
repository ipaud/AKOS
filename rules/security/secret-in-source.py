"""Detector for SECRET_IN_SOURCE.

Vendor-unique prefixes (AWS, GitHub, Slack, Stripe) match anywhere — near-zero
collision risk by construction, so those are Certain-confidence hits. The
generic KEY=value catch-all accepts quoted literals and conservative unquoted
token shapes, then requires high entropy and a denylist check to keep the
false-positive rate down. A decodable JWT with a
"service_role" claim escalates to CRITICAL — that specific case is what
SERVICE_ROLE_IN_CLIENT also checks for, scoped to client-side paths.

A realistic credential is dangerous wherever it lives: this detector does NOT
downgrade or suppress a finding for sitting under tests/, fixtures/, or docs/
(P0-4). A live vendor key or a service_role JWT is marked `blocking` so it
gates the exit code even from a test file. AKOS's own synthetic corpus stays
clean not by a path exception here, but by keeping realistic values out of
version control (materialized into a temp copy at scan time — see
`benchmarks/runners/run.py`). Genuinely-public values stay non-findings on
their own merits: an anon/authenticated JWT is skipped by role, an obvious
placeholder by the denylist, a low-entropy value by the entropy gate, and a
key already gitignored (i.e. not committed to source) by the gitignore check.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from io_utils import read_text_file  # noqa: E402
from _secret_utils import (  # noqa: E402
    VENDOR_PATTERNS, GENERIC_ASSIGNMENT_RE, JWT_RE,
    generic_assignment_value, is_generic_secret_assignment_value,
    decode_jwt_claims,
    gitignored_paths, iter_standalone_secret_matches, spans_overlap,
)


def run(files: list[Path], scan_root: Path | None = None) -> list[dict]:
    # This rule is about a secret "committed to source". A key in a gitignored
    # file is not committed — it is in the one place it belongs. Resolved once
    # for the whole batch; see gitignored_paths for why not per file.
    ignored = gitignored_paths([p.resolve() for p in files])

    findings = []
    for path in files:
        if str(path.resolve()) in ignored:
            continue
        path_str = str(path)
        text = read_text_file(path)

        stronger_spans: list[tuple[int, int]] = []
        for vendor, pattern in VENDOR_PATTERNS.items():
            for m in pattern.finditer(text):
                stronger_spans.append(m.span())
                line = text.count("\n", 0, m.start()) + 1
                # A Stripe *test* key is not a live credential — MEDIUM, and it
                # does not gate. Every other vendor prefix is a live secret:
                # HIGH by registry default and blocking, wherever it sits.
                is_test_key = vendor == "stripe_test_key"
                finding = {
                    "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                                  "snippet": f"{vendor} pattern matched"}],
                    "confidence_override": "Certain",
                }
                if is_test_key:
                    finding["severity_override"] = "MEDIUM"
                else:
                    finding["blocking"] = True
                findings.append(finding)

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
            stronger_spans.append(m.span())
            line = text.count("\n", 0, m.start()) + 1
            findings.append({
                "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                              "snippet": f"JWT with role={role!r}"}],
                "confidence_override": "Certain",
                "severity_override": "CRITICAL",
                "blocking": True,
            })

        for m in GENERIC_ASSIGNMENT_RE.finditer(text):
            value, value_span, unquoted = generic_assignment_value(m)
            if any(spans_overlap(value_span, span) for span in stronger_spans):
                continue
            if not is_generic_secret_assignment_value(
                value, unquoted=unquoted
            ):
                continue
            stronger_spans.append(value_span)
            line = text.count("\n", 0, m.start()) + 1
            # A high-entropy secret that cleared the placeholder and entropy
            # gates is high-confidence — block on it, in any path.
            findings.append({
                "evidence": [{"path": path_str, "line_start": line, "line_end": line,
                              "snippet": "high-entropy value assigned to a key/secret/token/password-like name"}],
                "blocking": True,
            })

        for m in iter_standalone_secret_matches(text, stronger_spans):
            line = text.count("\n", 0, m.start("value")) + 1
            findings.append({
                "evidence": [{
                    "path": str(path),
                    "line_start": line,
                    "line_end": line,
                    "snippet": "standalone high-entropy quoted literal",
                }],
                "confidence_override": "Moderate",
                "severity_override": "MEDIUM",
                "blocking": False,
            })
    return findings
