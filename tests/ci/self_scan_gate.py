#!/usr/bin/env python3
"""Run the AKOS self-scan while preserving its three-state exit contract."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


EXPECTED_BLOCKING_FIXTURES = {
    "SUPABASE_RLS_DISABLED": (
        (
            "benchmarks", "cases", "supabase-rls-basic", "fixture",
            "supabase", "migrations", "0001_init.sql",
        ),
        (
            "benchmarks", "cases", "real-rls-dynamic-loop-gap", "fixture",
            "supabase", "migrations", "0002_rls.sql",
        ),
        (
            "benchmarks", "cases", "real-destructive-in-comment", "fixture",
            "supabase", "migrations", "0034_normalize.sql",
        ),
        (
            "evals", "cases", "private-schema-secrets", "fixture",
            "supabase", "migrations", "001_private.sql",
        ),
    ),
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--akos-bin", default="bin/akos")
    parser.add_argument("--target", default=".")
    return parser


def _is_blocking(finding: object) -> bool:
    return (
        isinstance(finding, dict)
        and (
            finding.get("severity") == "CRITICAL"
            or finding.get("blocking") is True
        )
    )


def _is_expected_fixture_path(
    rule_id: object,
    path_value: object,
    target_root: Path,
) -> bool:
    prefixes = EXPECTED_BLOCKING_FIXTURES.get(rule_id)
    if prefixes is None:
        return False
    if not isinstance(path_value, str) or not path_value:
        return False
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = target_root / candidate
    try:
        relative = candidate.resolve(strict=False).relative_to(target_root)
    except (OSError, ValueError):
        return False
    parts = relative.parts
    return parts in prefixes


def _is_expected_fixture_finding(finding: object, target_root: Path) -> bool:
    if not isinstance(finding, dict):
        return False
    rule_id = finding.get("rule_id")
    evidence = finding.get("evidence")
    return (
        isinstance(evidence, list)
        and bool(evidence)
        and all(
            isinstance(item, dict)
            and _is_expected_fixture_path(
                rule_id,
                item.get("path"),
                target_root,
            )
            for item in evidence
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        target_root = Path(args.target).resolve(strict=True)
    except OSError as exc:
        print(f"self-scan target cannot be resolved: {exc}", file=sys.stderr)
        return 1
    proc = subprocess.run(
        [args.akos_bin, "rules", "run", args.target, "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")

    try:
        payload = json.loads(proc.stdout)
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"self-scan returned invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("self-scan JSON must be an object", file=sys.stderr)
        return 1

    expected_status = {0: "ok", 2: "findings"}.get(proc.returncode)
    if expected_status is None:
        print(
            f"self-scan was operationally incomplete (exit {proc.returncode})",
            file=sys.stderr,
        )
        return 1

    status = payload.get("status")
    errors = payload.get("errors")
    findings = payload.get("findings")
    summary = payload.get("summary")
    if (
        status != expected_status
        or not isinstance(errors, list)
        or errors
        or not isinstance(findings, list)
    ):
        print(
            "self-scan exit/JSON contract mismatch: "
            f"exit={proc.returncode} status={status!r} "
            f"findings={findings!r} errors={errors!r}",
            file=sys.stderr,
        )
        return 1
    if not isinstance(summary, dict):
        print("self-scan JSON has no summary object", file=sys.stderr)
        return 1
    counters = {
        name: summary.get(name)
        for name in ("rules_discovered", "rules_executed", "findings", "errors")
    }
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in counters.values()
    ):
        print(f"self-scan summary has invalid counters: {counters}", file=sys.stderr)
        return 1
    if (
        counters["rules_discovered"] == 0
        or counters["rules_discovered"] != counters["rules_executed"]
        or counters["findings"] != len(findings)
        or counters["errors"] != len(errors)
    ):
        print(
            f"self-scan summary is internally inconsistent: {counters}",
            file=sys.stderr,
        )
        return 1
    has_blocking = any(_is_blocking(finding) for finding in findings)
    if (proc.returncode == 2) != has_blocking:
        print(
            "self-scan blocking/exit contract mismatch: "
            f"exit={proc.returncode} has_blocking={has_blocking}",
            file=sys.stderr,
        )
        return 1
    unexpected_blocking = [
        finding
        for finding in findings
        if _is_blocking(finding)
        and not _is_expected_fixture_finding(finding, target_root)
    ]
    if unexpected_blocking:
        locations = [
            item.get("path")
            for finding in unexpected_blocking
            if isinstance(finding, dict)
            for item in finding.get("evidence", [])
            if isinstance(item, dict)
        ]
        print(
            "self-scan found blocking findings outside expected fixtures: "
            f"{locations or ['<missing evidence path>']}",
            file=sys.stderr,
        )
        return 1

    print(f"self-scan complete: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
