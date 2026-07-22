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

Fail-closed. Findings and operational errors are separate results: a detector
or a registry that cannot run is an ExecutionError, never a finding, and never
a clean exit. Exit codes:

    0  ran completely, no blocking finding
    1  usage/setup error, or the scan was incomplete (bad registry, unloadable
       detector, detector with no run(), internal exception) — an incomplete
       scan cannot report "clean"
    2  ran completely and a blocking finding exists (CRITICAL, or a finding a
       rule explicitly marked blocking)

If findings and operational errors coexist, exit 1 wins: the scanner is
incomplete, so its "no CRITICAL" is not trustworthy.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
sys.path.insert(0, str(AKOS_HOME / "rules" / "security"))
import yaml_subset  # noqa: E402

DEFAULT_IGNORE_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", "__pycache__", ".venv"}

SUPPRESS_RE = re.compile(r"akos:allow\s+([A-Z0-9_]+)")


@dataclass(frozen=True)
class ExecutionError:
    """An operational failure that made the scan incomplete — distinct from a
    finding. Its presence forces status 'error' and exit 1."""
    phase: str            # "discovery" | "setup" | "detector" | "read"
    rule_id: str | None
    path: str | None
    message: str


@dataclass
class ScanResult:
    status: str           # "ok" | "findings" | "error"
    findings: list[dict] = field(default_factory=list)
    errors: list[ExecutionError] = field(default_factory=list)
    rules_discovered: int = 0
    rules_executed: int = 0


class RegistryError(Exception):
    """Raised by discover_rules when a registry is malformed and the caller did
    not pass an errors list to collect into — so a broken registry fails closed
    for count-only callers instead of silently shrinking the rule set."""


def _is_blocking(finding: dict) -> bool:
    """CRITICAL always blocks; a rule may also mark a specific finding blocking
    (e.g. a live vendor credential that defaults to HIGH)."""
    return finding.get("severity") == "CRITICAL" or bool(finding.get("blocking"))


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


def discover_rules(domain_filter=None, rule_filter=None, errors=None) -> list[Rule]:
    """Discover stable rules. A malformed registry, or one missing required
    keys, is an operational error — recorded in `errors` if a collector is
    passed, otherwise raised (RegistryError) so a count-only caller fails
    closed rather than quietly running fewer rules than it thinks."""
    rules = []
    for yaml_path in sorted((AKOS_HOME / "rules").glob("*/*.yaml")):
        rel = str(yaml_path.relative_to(AKOS_HOME))
        try:
            data = yaml_subset.load(yaml_path)
            rule = Rule(yaml_path, data)
        except (yaml_subset.YamlSubsetError, KeyError, ValueError, TypeError) as e:
            rule_id = None
            if isinstance(e, KeyError):
                # A KeyError here is a missing required registry field.
                msg = f"registry missing required field {e}"
            else:
                msg = f"unparseable/invalid registry: {e}"
            err = ExecutionError("discovery", rule_id, rel, msg)
            if errors is None:
                raise RegistryError(f"{rel}: {msg}") from e
            errors.append(err)
            continue
        if rule_filter and rule.id not in rule_filter:
            continue
        if domain_filter and rule.domain not in domain_filter:
            continue
        if rule.status != "stable":
            continue
        rules.append(rule)
    return rules


def collect_files(target_dir: Path, globs: list[str]) -> list[Path]:
    # Symlinks are skipped, and anything whose real location falls outside the
    # scanned tree is skipped too (glob on Python <=3.12 recurses through
    # symlinked directories). Without this, scanning an untrusted repository
    # that plants `link -> ~/.ssh/id_rsa` makes the secret detectors read the
    # host's private key — and a review report quotes the evidence it finds.
    root_resolved = target_dir.resolve()
    files = []
    seen = set()
    for pattern in globs:
        for p in target_dir.glob(pattern):
            if p.is_symlink() or not p.is_file():
                continue
            if any(part in DEFAULT_IGNORE_DIRS for part in p.parts):
                continue
            try:
                p.resolve().relative_to(root_resolved)
            except (ValueError, OSError):
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


def run_rules(target_dir: Path, rules: list[Rule], profile: str | None,
              errors=None) -> list[dict]:
    """Run each rule's detector. A detector that cannot run (missing file, no
    run(), or an exception) is an ExecutionError recorded in `errors` — it is
    never turned into a finding, so a broken security detector can never read
    as a clean pass. Severity is the rule/finding severity as-is: there is no
    path-based downgrade (a real credential under tests/ is still a real
    credential — see P0-4)."""
    if errors is None:
        errors = []
    all_findings = []
    file_lines_cache: dict = {}
    for rule in rules:
        scan_dir = AKOS_HOME if rule.target == "akos-packs" else target_dir
        files = collect_files(scan_dir, rule.globs)
        if not files:
            continue
        rel_detector = _rel_to_akos(rule.detector_path)
        try:
            if not rule.detector_path.exists():
                raise FileNotFoundError("detector file missing")
            module = load_detector(rule)
            if not hasattr(module, "run"):
                raise AttributeError("detector has no run() function")
            # Detectors that classify by path take the scan root so they can
            # judge the project-relative path, not the absolute one.
            if len(inspect.signature(module.run).parameters) >= 2:
                raw_findings = module.run(files, scan_dir)
            else:
                raw_findings = module.run(files)
        except Exception as e:  # noqa: BLE001 - captured as an operational error, not a finding
            errors.append(ExecutionError("detector", rule.id, rel_detector, str(e)))
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
                "blocking": bool(f.get("blocking")) or severity == "CRITICAL",
            }
            all_findings.append(finding)
    return all_findings


def _rel_to_akos(p: Path) -> str:
    try:
        return str(p.relative_to(AKOS_HOME))
    except ValueError:
        return str(p)


def scan(target_dir: Path, domain_filter=None, rule_filter=None,
         profile: str | None = None) -> ScanResult:
    """Full pipeline: discover → run → classify. Setup problems (a filter that
    matches nothing, an unknown rule id, or — with no filter — an empty rule
    set) are operational errors, so an incomplete run never reports clean."""
    errors: list[ExecutionError] = []
    rules = discover_rules(domain_filter=domain_filter, rule_filter=rule_filter, errors=errors)

    if rule_filter or domain_filter:
        if not rules:
            requested = ", ".join(sorted(set(rule_filter or set()) | set(domain_filter or set())))
            errors.append(ExecutionError("setup", None, None,
                                         f"no rule matches the filter ({requested})"))
        elif rule_filter:
            unmatched = sorted(set(rule_filter) - {r.id for r in rules})
            if unmatched:
                errors.append(ExecutionError("setup", None, None,
                                             f"no such rule: {', '.join(unmatched)}"))
    elif not rules:
        errors.append(ExecutionError("setup", None, None,
                                     "no stable rules discovered — cannot report a clean scan"))

    findings = run_rules(target_dir, rules, profile, errors=errors) if rules else []
    detector_error_rules = {e.rule_id for e in errors if e.phase == "detector" and e.rule_id}
    executed = len(rules) - len(detector_error_rules)

    if errors:
        status = "error"
    elif any(_is_blocking(f) for f in findings):
        status = "findings"
    else:
        status = "ok"
    return ScanResult(status=status, findings=findings, errors=errors,
                      rules_discovered=len(rules), rules_executed=executed)


def print_text(result: ScanResult):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    c_red, c_yellow, c_reset, c_bold = "\033[31m", "\033[33m", "\033[0m", "\033[1m"
    glyph = {"CRITICAL": f"{c_red}✗{c_reset}", "HIGH": f"{c_red}!{c_reset}", "MEDIUM": f"{c_yellow}!{c_reset}", "LOW": "·"}
    findings = result.findings
    for f in sorted(findings, key=lambda x: order.get(x["severity"], 9)):
        loc = ""
        if f["evidence"]:
            ev = f["evidence"][0]
            loc = f" — {ev['path']}:{ev.get('line_start', '?')}"
        block = " [blocking]" if _is_blocking(f) else ""
        print(f"{glyph.get(f['severity'], '?')} [{f['severity']}]{block} {f['rule_id']}{loc}")
        print(f"    {f['title']}")
        if f["recommendation"]:
            print(f"    Fix: {f['recommendation']}")

    if result.errors:
        # Operational errors are printed separately and never phrased as a
        # clean result — the scan did not finish.
        print(f"\n{c_bold}{c_red}Execution errors{c_reset}  "
              f"(the scan is INCOMPLETE — do not read this as clean):")
        for e in result.errors:
            where = e.rule_id or e.path or e.phase
            print(f"{c_red}✗{c_reset} [{e.phase}] {where}: {e.message}")

    counts: dict = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    sev_summary = "  ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9)))
    print(f"\n{c_bold}Summary{c_reset}  status: {result.status}  "
          f"rules discovered: {result.rules_discovered}  executed: {result.rules_executed}  "
          f"findings: {len(findings)}  errors: {len(result.errors)}")
    if findings:
        print(f"  {sev_summary}")


def _result_to_json(result: ScanResult) -> dict:
    return {
        "status": result.status,
        "summary": {
            "rules_discovered": result.rules_discovered,
            "rules_executed": result.rules_executed,
            "findings": len(result.findings),
            "errors": len(result.errors),
        },
        "findings": result.findings,
        "errors": [asdict(e) for e in result.errors],
    }


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

    try:
        result = scan(
            target_dir,
            domain_filter=set(args.domain) if args.domain else None,
            rule_filter=set(args.rule) if args.rule else None,
            profile=args.profile,
        )
    except RegistryError as e:
        # Belt-and-braces: scan() passes an errors collector, so this path is
        # only reached if a nested call raised. Fail closed either way.
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        import json
        print(json.dumps(_result_to_json(result), indent=2))
    else:
        print_text(result)

    # Errors beat findings: an incomplete scan is exit 1, even if a blocking
    # finding also surfaced. A complete scan with a blocking finding is exit 2.
    return {"error": 1, "findings": 2, "ok": 0}[result.status]


if __name__ == "__main__":
    raise SystemExit(main())
