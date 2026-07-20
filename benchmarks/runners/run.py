#!/usr/bin/env python3
"""AKOS benchmark harness. Runs the deterministic rules engine (Level A/B)
against every case's fixture/, diffs actual findings against
must_detect/must_not_detect, and reports recall/precision/false-positive
rate per rule. Optionally exercises a Level C (LLM-assisted) provider —
mock by default, deterministic, no network; real providers are opt-in and
never used by CI.

Usage:
    python3 benchmarks/runners/run.py [run] [--case ID ...] [--domain D ...]
                                      [--provider NAME] [--format text|json]
    python3 benchmarks/runners/run.py list

No silent caps: every case in manifest.yaml runs unless explicitly filtered
out, and the summary states exactly how many cases were skipped and why.

Exit codes: 0 all cases pass, 1 setup error, 2 at least one case failed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
sys.path.insert(0, str(AKOS_HOME / "rules"))
sys.path.insert(0, str(AKOS_HOME / "benchmarks"))
import yaml_subset  # noqa: E402
import runner as rules_runner  # noqa: E402  (rules/runner.py)

BENCH_HOME = AKOS_HOME / "benchmarks"
LINE_TOLERANCE = 3


def load_manifest() -> dict:
    return yaml_subset.load(BENCH_HOME / "manifest.yaml")


def load_case(case_entry: dict) -> tuple[dict, Path]:
    case_dir = BENCH_HOME / case_entry["path"]
    expected = yaml_subset.load(case_dir / "expected.yaml")
    return expected, case_dir


def run_deterministic_case(expected: dict, case_dir: Path) -> dict:
    fixture_dir = case_dir / "fixture"
    rule_ids = expected.get("rules_under_test", [])
    rules = rules_runner.discover_rules(rule_filter=set(rule_ids) if rule_ids else None)
    findings = rules_runner.run_rules(fixture_dir, rules, profile=None)

    must_detect = expected.get("must_detect", [])
    must_not_detect = expected.get("must_not_detect", [])

    def matches(finding: dict, spec: dict) -> bool:
        if finding["rule_id"] != spec["rule_id"]:
            return False
        ev = finding["evidence"][0] if finding["evidence"] else {}
        # spec["path"] in expected.yaml is relative to the CASE directory
        # (e.g. "fixture/supabase/migrations/0001.sql"), not to benchmarks/.
        spec_path = str((case_dir / spec["path"]).resolve()) if "path" in spec else None
        if spec_path and str(Path(ev.get("path", "")).resolve()) != spec_path:
            return False
        if "line" in spec and ev.get("line_start") is not None:
            if abs(ev["line_start"] - spec["line"]) > LINE_TOLERANCE:
                return False
        return True

    true_positives = []
    false_negatives = []
    for spec in must_detect:
        hit = next((f for f in findings if matches(f, spec)), None)
        (true_positives if hit else false_negatives).append(spec)

    false_positives = []
    for spec in must_not_detect:
        hit = next((f for f in findings if matches(f, spec)), None)
        if hit:
            false_positives.append(spec)

    passed = not false_negatives and not false_positives
    return {
        "true_positives": len(true_positives),
        "false_negatives": false_negatives,
        "false_positives": false_positives,
        "passed": passed,
        "actual_finding_count": len(findings),
    }


def run_level_c_case(expected: dict, case_dir: Path, provider_name: str) -> dict:
    try:
        provider_mod = __import__(f"providers.{provider_name}", fromlist=["generate"])
    except ImportError:
        return {"skipped": True, "reason": f"provider '{provider_name}' not found"}

    fixture_dir = case_dir / "fixture"
    prompt_parts = [expected.get("prompt", "")]
    for f in sorted(fixture_dir.rglob("*")):
        if f.is_file():
            prompt_parts.append(f.read_text(encoding="utf-8", errors="replace"))
    prompt = "\n".join(prompt_parts)

    try:
        response = provider_mod.generate(prompt)
    except Exception as e:  # noqa: BLE001
        return {"skipped": True, "reason": f"provider error: {e}"}

    must_mention = expected.get("must_mention", [])
    missing = [phrase for phrase in must_mention if phrase.lower() not in response.lower()]
    return {"skipped": False, "passed": not missing, "missing": missing, "response": response}


def run_case(case_id: str, case_entry: dict, provider_name: str) -> dict:
    expected, case_dir = load_case(case_entry)
    level = expected.get("level", "A")
    if level == "C":
        result = run_level_c_case(expected, case_dir, provider_name)
        result["level"] = "C"
    else:
        result = run_deterministic_case(expected, case_dir)
        result["level"] = level
    result["case_id"] = case_id
    result["domain"] = expected.get("domain", "unknown")
    return result


def print_text(results: list[dict]):
    c_green, c_red, c_yellow, c_reset, c_bold = "\033[32m", "\033[31m", "\033[33m", "\033[0m", "\033[1m"
    passed = 0
    failed = 0
    skipped = 0
    for r in results:
        if r.get("skipped"):
            skipped += 1
            print(f"{c_yellow}skip{c_reset}  {r['case_id']}: {r.get('reason', 'skipped')}")
            continue
        if r["passed"]:
            passed += 1
            print(f"{c_green}✓{c_reset} pass  {r['case_id']} (level {r['level']})")
        else:
            failed += 1
            print(f"{c_red}✗{c_reset} FAIL  {r['case_id']} (level {r['level']})")
            for fn in r.get("false_negatives", []):
                print(f"    missed: {fn['rule_id']} at {fn.get('path', '?')}")
            for fp in r.get("false_positives", []):
                print(f"    unexpected: {fp['rule_id']} at {fp.get('path', '?')}")
            for m in r.get("missing", []):
                print(f"    missing phrase: {m!r}")

    print(f"\n{c_bold}Summary{c_reset}  pass: {passed}  fail: {failed}  skipped: {skipped}  ({len(results)} cases)")

    # Recall/precision over deterministic (Level A/B) cases only — Level C
    # is graded pass/fail per case above, not pooled into this arithmetic.
    tp = sum(r.get("true_positives", 0) for r in results if not r.get("skipped") and r.get("level") in ("A", "B"))
    fn = sum(len(r.get("false_negatives", [])) for r in results if not r.get("skipped") and r.get("level") in ("A", "B"))
    fp = sum(len(r.get("false_positives", [])) for r in results if not r.get("skipped") and r.get("level") in ("A", "B"))
    if tp + fn > 0:
        recall = tp / (tp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        print(f"Level A/B — recall: {recall:.0%}  precision: {precision:.0%}  (tp={tp} fn={fn} fp={fp})")
        real = sum(1 for c in results if str(c.get("case_id", "")).startswith("real-"))
        print(f"Measured over this corpus only — a regression guard, not a claim about "
              f"real-world code. {real} of {len(results)} cases carry shapes taken from real "
              f"repositories; the rest are synthetic and were written alongside the detectors "
              f"they exercise. This number read 100% while every Level-A finding on three real "
              f"repositories was a false positive.")


def cmd_list(manifest: dict):
    for c in manifest["cases"]:
        print(f"  {c['id']:<40} {c['path']}")


def cmd_run(manifest: dict, case_filter, domain_filter, provider_name: str, fmt: str) -> int:
    # A --case that matches nothing must not report a clean run. `--case
    # <typo>` used to print "pass: 0 fail: 0 (0 cases)" and exit 0, which in
    # a CI matrix is a green gate that ran nothing.
    if case_filter:
        known = {c["id"] for c in manifest["cases"]}
        unknown = sorted(case_filter - known)
        if unknown:
            print(f"error: no such case: {', '.join(unknown)}. "
                  f"List cases with 'akos benchmark list'.", file=sys.stderr)
            return 1

    results = []
    skipped_by_filter = 0
    for c in manifest["cases"]:
        if case_filter and c["id"] not in case_filter:
            skipped_by_filter += 1
            continue
        expected, case_dir = load_case(c)
        if domain_filter and expected.get("domain") not in domain_filter:
            skipped_by_filter += 1
            continue
        results.append(run_case(c["id"], c, provider_name))

    if fmt == "json":
        import json
        print(json.dumps(results, indent=2, default=str))
    else:
        print_text(results)
        if skipped_by_filter:
            print(f"(+{skipped_by_filter} case(s) excluded by --domain filter)")

    if any((not r.get("skipped")) and (not r.get("passed", True)) for r in results):
        return 2
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", nargs="?", default="run", choices=["run", "list"])
    ap.add_argument("--case", action="append", help="Only this case id (repeatable)")
    ap.add_argument("--domain", action="append", help="Only cases in this domain (repeatable)")
    ap.add_argument("--provider", default="mock", help="Level C provider (default: mock)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    if not (BENCH_HOME / "manifest.yaml").exists():
        print("error: benchmarks/manifest.yaml not found", file=sys.stderr)
        return 1

    manifest = load_manifest()

    if args.action == "list":
        cmd_list(manifest)
        return 0

    return cmd_run(manifest, set(args.case) if args.case else None,
                    set(args.domain) if args.domain else None, args.provider, args.format)


if __name__ == "__main__":
    raise SystemExit(main())
