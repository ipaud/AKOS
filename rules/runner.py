#!/usr/bin/env python3
"""Discovers and runs AKOS's executable rules against a target directory.

Rules are filesystem-discovered — rules/<domain>/<id>.yaml + a sibling
<id>.py — never a hand-maintained central index. This mirrors how packs/
already works, and avoids recreating the exact drift risk doctor.sh's
routing-table guard exists to catch for the pack index.

Usage:
    python3 rules/runner.py <target-dir> [--rule ID ...] [--domain D ...]
                            [--target project-source|akos-packs|all]
                            [--profile NAME] [--format text|json]

Exit codes: 0 clean (no open CRITICAL), 1 setup error, 2 an open CRITICAL
finding exists. Only CRITICAL gates — the one severity core/review-pipeline.md
itself says "always blocks, every profile."
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

DEFAULT_IGNORE_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", "__pycache__", ".venv"}

SUPPRESS_RE = re.compile(r"akos:allow\s+([A-Z0-9_]+)")


class Rule:
    def __init__(self, yaml_path: Path, data: dict):
        self.yaml_path = yaml_path
        self.id = data["id"]
        self.title = data.get("title", self.id)
        self.domain = data.get("domain", yaml_path.parent.name)
        self.level = data.get("level", "A")
        self.confidence = data.get("confidence", "Moderate")
        self.severity_default = data.get("severity", {}).get("default", "MEDIUM")
        self.severity_profiles = data.get("severity", {}).get("profiles", {})
        self.related_packs = data.get("related_packs", [])
        self.applies_to = data.get("applies_to", {})
        self.target = self.applies_to.get("target", "project-source")
        self.globs = self.applies_to.get("glob", ["**/*"])
        self.detector_path = AKOS_HOME / data["detector"]
        self.recommendation = data.get("recommendation", "")
        self.status = data.get("status", "stable")

    def severity_for_profile(self, profile: str | None) -> str:
        if profile and profile in self.severity_profiles:
            return self.severity_profiles[profile]
        return self.severity_default


def discover_rules(domain_filter=None, rule_filter=None) -> list[Rule]:
    rules = []
    for yaml_path in sorted((AKOS_HOME / "rules").glob("*/*.yaml")):
        data = yaml_subset.load(yaml_path)
        rule = Rule(yaml_path, data)
        if rule_filter and rule.id not in rule_filter:
            continue
        if domain_filter and rule.domain not in domain_filter:
            continue
        if rule.status != "stable":
            continue
        rules.append(rule)
    return rules


def collect_files(target_dir: Path, globs: list[str]) -> list[Path]:
    files = []
    seen = set()
    for pattern in globs:
        for p in target_dir.glob(pattern):
            if not p.is_file():
                continue
            if any(part in DEFAULT_IGNORE_DIRS for part in p.parts):
                continue
            if p in seen:
                continue
            seen.add(p)
            files.append(p)
    return sorted(files)


def load_detector(rule: Rule):
    spec = importlib.util.spec_from_file_location(f"akos_rule_{rule.id}", rule.detector_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUPPRESS_WINDOW = 5  # lines to look back from the evidence line


def is_suppressed(finding: dict, rule_id: str, file_lines_cache: dict) -> bool:
    for ev in finding.get("evidence", []):
        path = Path(ev["path"])
        if path not in file_lines_cache:
            try:
                file_lines_cache[path] = path.read_text(encoding="utf-8", errors="replace").split("\n")
            except OSError:
                file_lines_cache[path] = []
        lines = file_lines_cache[path]
        end = ev.get("line_start", 1)
        # A suppression comment usually sits on the statement's opening line
        # (e.g. CREATE POLICY ... -- akos:allow X), not necessarily on the
        # exact evidence line further down the same statement — check a
        # small backward window rather than only the one line.
        start = max(0, end - SUPPRESS_WINDOW)
        for ln in lines[start:end]:
            m = SUPPRESS_RE.search(ln)
            if m and m.group(1) == rule_id:
                return True
    return False


def run_rules(target_dir: Path, rules: list[Rule], profile: str | None) -> list[dict]:
    all_findings = []
    file_lines_cache: dict = {}
    for rule in rules:
        scan_dir = AKOS_HOME if rule.target == "akos-packs" else target_dir
        files = collect_files(scan_dir, rule.globs)
        if not files:
            continue
        try:
            module = load_detector(rule)
            raw_findings = module.run(files)
        except Exception as e:  # noqa: BLE001 - a broken detector must not crash the whole run
            all_findings.append({
                "rule_id": rule.id, "title": rule.title, "domain": rule.domain,
                "level": rule.level, "severity": "MEDIUM", "confidence": "Low",
                "evidence": [], "recommendation": f"Detector error: {e}",
            })
            continue

        for f in raw_findings:
            if is_suppressed(f, rule.id, file_lines_cache):
                continue
            severity = f.get("severity_override") or rule.severity_for_profile(profile)
            finding = {
                "rule_id": rule.id,
                "title": rule.title,
                "domain": rule.domain,
                "level": rule.level,
                "severity": severity,
                "confidence": f.get("confidence_override", rule.confidence),
                "evidence": f.get("evidence", []),
                "recommendation": f.get("detail", rule.recommendation),
            }
            all_findings.append(finding)
    return all_findings


def print_text(findings: list[dict]):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    c_red, c_yellow, c_reset, c_bold = "\033[31m", "\033[33m", "\033[0m", "\033[1m"
    glyph = {"CRITICAL": f"{c_red}✗{c_reset}", "HIGH": f"{c_red}!{c_reset}", "MEDIUM": f"{c_yellow}!{c_reset}", "LOW": "·"}
    for f in sorted(findings, key=lambda x: order.get(x["severity"], 9)):
        loc = ""
        if f["evidence"]:
            ev = f["evidence"][0]
            loc = f" — {ev['path']}:{ev.get('line_start', '?')}"
        print(f"{glyph.get(f['severity'], '?')} [{f['severity']}] {f['rule_id']}{loc}")
        print(f"    {f['title']}")
        if f["recommendation"]:
            print(f"    Fix: {f['recommendation']}")
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    summary = "  ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9)))
    print(f"\n{c_bold}Summary{c_reset}  {summary or 'no findings'}  ({len(findings)} total)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target_dir", nargs="?", default=".", help="Directory to scan (project-source rules)")
    ap.add_argument("--rule", action="append", help="Only run this rule id (repeatable)")
    ap.add_argument("--domain", action="append", help="Only run rules in this domain (repeatable)")
    ap.add_argument("--profile", help="Reasoning profile — affects severity mapping")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    target_dir = Path(args.target_dir).resolve()
    if not target_dir.is_dir():
        print(f"error: not a directory: {target_dir}", file=sys.stderr)
        return 1

    rules = discover_rules(domain_filter=set(args.domain) if args.domain else None,
                            rule_filter=set(args.rule) if args.rule else None)

    # A filter that selects no rule must not report a clean scan. `--rule
    # SUPABASE_RLS_DISABLE` (one character short) used to print "no findings"
    # and exit 0, so an agent would report the codebase clean having run
    # nothing. Name the unmatched IDs rather than the empty result.
    if args.rule or args.domain:
        if not rules:
            requested = ", ".join(sorted(set(args.rule or []) | set(args.domain or [])))
            print(f"error: no rule matches the filter ({requested}). "
                  f"List available rules with 'akos rules list'.", file=sys.stderr)
            return 1
        selected_ids = {r.id for r in rules}
        unmatched = sorted(set(args.rule or []) - selected_ids)
        if unmatched:
            print(f"error: no such rule: {', '.join(unmatched)}. "
                  f"List available rules with 'akos rules list'.", file=sys.stderr)
            return 1

    findings = run_rules(target_dir, rules, args.profile)

    if args.format == "json":
        import json
        print(json.dumps(findings, indent=2))
    else:
        print_text(findings)

    if any(f["severity"] == "CRITICAL" for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
