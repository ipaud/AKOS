#!/usr/bin/env python3
"""Grade an AKOS review report against a case's expected findings.

What this measures, precisely: whether a review report **surfaced** the
findings a competent reviewer must surface on a known artifact, and whether
it **avoided** the ones a careless reviewer wrongly reports. Nothing else.

What it does NOT measure, so nobody reads more into a green run than is
there:

- Wording, structure, tone, or score accuracy. Two reports can differ
  entirely and both pass.
- Whether an unlisted finding is right or wrong. Extra findings are neither
  rewarded nor punished; only the listed traps count against a report.
- Anything about a review of a project that is not this case's fixture.
  A report is graded against one case, named explicitly, because that is the
  only pairing that means anything.
- The difference between reporting a finding and explaining why it is *not*
  a finding. Both put the same words in the report. A review that correctly
  refutes a trap reads to this grader exactly like one that falls for it —
  separating them needs a judge, which needs its own calibration.

It does not invoke a model. It grades a report someone already produced —
by an agent, by hand, or replayed from `.akos/reviews/`. That is deliberate:
generating the review inside the grader would make the suite depend on a
provider and on run-to-run variance, and there is no honest way to gate CI
on that. Grading is deterministic; producing is not.

Matching is concept-based, not exact-match. A finding counts as surfaced
when every term in `match_all` appears in the report, and at least one term
in `match_any` if that list is present. Case-insensitive, whitespace
collapsed. That tolerates rewording, which is the whole reason exact-match
graders are useless on prose.

Exit codes: 0 all cases met their threshold · 1 usage error · 2 at least one
case below threshold.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EVALS_HOME = Path(__file__).resolve().parent.parent
AKOS_HOME = EVALS_HOME.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

# Stated up front, in the code, not decided after seeing a result. A review
# that misses a must_find is not "mostly right": every listed finding is one
# a hand-verified read of the fixture confirmed is really there.
REQUIRED_RECALL = 1.0
MAX_FALSE_POSITIVES = 0


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


# Terms have to land near each other to count as one finding. Matching over
# the whole document made a phrase in one finding satisfy a spec about
# another: a report correctly saying "the sanity step cannot fail" and
# separately "shellcheck ... is fine as-is" tripped a trap whose terms were
# `shellcheck` + `cannot fail`, because both appeared somewhere. The window
# is about the length of one finding with its evidence, not a whole report:
# at 600 it spanned a 299-character report entirely and bought nothing.
#
# Proximity is not sufficient on its own. A trap whose terms are phrases a
# CORRECT report uses about a different finding will still collide, however
# tight the window — the fix for that is to write the trap in words only a
# wrong report would reach for. See masked-ci-step for a worked case.
PROXIMITY_WINDOW = 240


def matches(report: str, spec: dict) -> bool:
    """True when the report surfaces the concept this spec describes.

    Every match_all term, plus at least one match_any term if present, must
    occur inside one PROXIMITY_WINDOW-character span. Anchored on each
    occurrence of the first match_all term rather than on the first one only,
    so a term used once in passing does not shadow the real finding later.
    """
    all_terms = [normalize(x) for x in spec.get("match_all", [])]
    any_terms = [normalize(x) for x in spec.get("match_any", [])]
    if not all_terms:
        return any(a in report for a in any_terms) if any_terms else False

    anchor = all_terms[0]
    start = report.find(anchor)
    while start != -1:
        lo = max(0, start - PROXIMITY_WINDOW)
        window = report[lo:start + PROXIMITY_WINDOW]
        if all(term in window for term in all_terms[1:]) and (
                not any_terms or any(term in window for term in any_terms)):
            return True
        start = report.find(anchor, start + 1)
    return False


def grade_case(case_dir: Path, report_text: str) -> dict:
    expected = yaml_subset.load(case_dir / "expected.yaml")
    report = normalize(report_text)

    found, missed = [], []
    for spec in expected.get("must_find", []):
        (found if matches(report, spec) else missed).append(spec["id"])

    false_positives = [
        spec["id"] for spec in expected.get("must_not_find", [])
        if matches(report, spec)
    ]

    total = len(expected.get("must_find", []))
    recall = 1.0 if total == 0 else len(found) / total
    passed = recall >= REQUIRED_RECALL and len(false_positives) <= MAX_FALSE_POSITIVES

    return {
        "case_id": expected["case_id"],
        "lens": expected.get("lens"),
        "passed": passed,
        "recall": recall,
        "found": found,
        "missed": missed,
        "false_positives": false_positives,
    }


def discover_cases() -> list[Path]:
    return sorted(d for d in (EVALS_HOME / "cases").iterdir()
                  if (d / "expected.yaml").is_file())


def print_text(results: list[dict]) -> None:
    red, green, yellow, bold, reset = "\033[31m", "\033[32m", "\033[33m", "\033[1m", "\033[0m"
    for r in results:
        mark = f"{green}✓ pass{reset}" if r["passed"] else f"{red}✗ fail{reset}"
        print(f"{mark}  {r['case_id']} ({r['lens']}) — recall {r['recall']:.0%}")
        for miss in r["missed"]:
            print(f"    {red}missed{reset}: {miss} — the report never surfaced this")
        for fp in r["false_positives"]:
            print(f"    {yellow}false positive{reset}: {fp} — reported something the fixture disproves")

    passed = sum(1 for r in results if r["passed"])
    print(f"\n{bold}Summary{reset}  pass: {passed}  fail: {len(results) - passed}  ({len(results)} cases)")
    print(f"Threshold: recall ≥ {REQUIRED_RECALL:.0%}, false positives ≤ {MAX_FALSE_POSITIVES}. "
          f"Grades a report someone else produced — it does not run a review, "
          f"and says nothing about projects outside these fixtures.")


class _ArgumentParser(argparse.ArgumentParser):
    """argparse exits 2 on a usage error, which here collides with "2 means
    a case failed" — a caller, including CI, could not tell a mistyped flag
    from a genuine regression. Usage errors exit 1, per docs/cli/exit-codes.md.
    """

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        sys.exit(1)


def main(argv=None) -> int:
    ap = _ArgumentParser(description=__doc__)
    ap.add_argument("--report", required=True, help="path to the review report (Markdown)")
    ap.add_argument("--case", required=True,
                    help="the case whose fixture this report reviewed (required — see below)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    report_path = Path(args.report)
    if not report_path.is_file():
        print(f"error: report not found: {report_path}", file=sys.stderr)
        return 1
    report_text = report_path.read_text(encoding="utf-8")

    # --case is required, not a filter. A report can only be graded against
    # the case whose fixture it actually reviewed: grading it against the
    # others measures nothing, and produces both halves of a wrong answer —
    # `must_find` entries "missed" because they describe a different
    # codebase, and traps "hit" because the report happens to use the words.
    # Observed directly: a real review of one project scored 0% recall and
    # one false positive against another project's case.
    cases = discover_cases()
    known = {c.name for c in cases}
    if args.case not in known:
        print(f"error: no such case: {args.case}. Available: {', '.join(sorted(known))}",
              file=sys.stderr)
        return 1
    cases = [c for c in cases if c.name == args.case]

    results = [grade_case(c, report_text) for c in cases]

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_text(results)

    return 0 if all(r["passed"] for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())
