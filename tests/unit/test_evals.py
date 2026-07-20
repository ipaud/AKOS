"""The review-output eval suite, and the property that makes it a suite.

Two Level C benchmark cases shipped unable to fail, because their assertion
was satisfied by their own prompt. These tests assert the equivalent
property here directly: every case must go red on a report that omits its
findings. A case that cannot fail is not a test, and it still counts toward
a passing run.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)
sys.path.insert(0, str(AKOS_HOME / "evals" / "runners"))
import grade  # noqa: E402


class TestCaseCorpus(unittest.TestCase):
    def test_cases_exist(self):
        self.assertTrue(grade.discover_cases(),
                        "no eval cases found — the guards below would cover nothing")

    def test_every_case_has_a_fixture(self):
        for case in grade.discover_cases():
            with self.subTest(case=case.name):
                fixture = case / "fixture"
                self.assertTrue(fixture.is_dir(), f"{case.name} has no fixture/")
                self.assertTrue(any(fixture.rglob("*")), f"{case.name}'s fixture is empty")

    def test_every_case_states_why_for_each_expectation(self):
        """A finding with no stated reason cannot be reviewed later, and is
        how a wrong case survives in a corpus indefinitely."""
        import yaml_subset
        for case in grade.discover_cases():
            spec = yaml_subset.load(case / "expected.yaml")
            for key in ("must_find", "must_not_find"):
                for entry in spec.get(key, []):
                    with self.subTest(case=case.name, entry=entry.get("id")):
                        self.assertTrue(entry.get("why", "").strip(),
                                        f"{case.name}/{key}/{entry.get('id')} has no why")


class TestEveryCaseCanFail(unittest.TestCase):
    """The load-bearing guard. If a case passes on an empty report, its
    assertions are satisfied by something other than the report's content."""

    def test_empty_report_fails_every_case(self):
        for case in grade.discover_cases():
            with self.subTest(case=case.name):
                result = grade.grade_case(case, "")
                if not result["found"] and not result["missed"]:
                    self.skipTest(f"{case.name} has no must_find entries")
                self.assertFalse(
                    result["passed"],
                    f"{case.name} passes on an empty report — its must_find entries are "
                    f"satisfied by something that is not the report")

    def test_a_report_naming_the_traps_fails(self):
        """The must_not_find half: a report that repeats the known false
        positives must be caught, not merely un-credited."""
        import yaml_subset
        for case in grade.discover_cases():
            spec = yaml_subset.load(case / "expected.yaml")
            traps = spec.get("must_not_find", [])
            if not traps:
                continue
            with self.subTest(case=case.name):
                # Build a report containing exactly the trap terms.
                terms = []
                for t in traps:
                    terms += t.get("match_all", []) + t.get("match_any", [])[:1]
                result = grade.grade_case(case, " ".join(terms))
                self.assertTrue(result["false_positives"],
                                f"{case.name} did not flag a report that names its traps")


class TestGraderMatching(unittest.TestCase):
    def test_match_all_requires_every_term(self):
        spec = {"match_all": ["api_token", "optional"]}
        self.assertTrue(grade.matches(grade.normalize("API_TOKEN is optional here"), spec))
        self.assertFalse(grade.matches(grade.normalize("API_TOKEN is required"), spec))

    def test_match_any_requires_at_least_one(self):
        spec = {"match_all": ["cache"], "match_any": ["permissive", "using (true)"]}
        self.assertTrue(grade.matches(grade.normalize("the cache policy is permissive"), spec))
        self.assertFalse(grade.matches(grade.normalize("the cache is fine"), spec))

    def test_matching_ignores_case_and_whitespace(self):
        spec = {"match_all": ["row level security"]}
        self.assertTrue(grade.matches(grade.normalize("ROW   LEVEL\nSECURITY"), spec))


class TestGraderExitCodes(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.report = Path(self._tmp.name) / "r.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_report_is_a_usage_error(self):
        self.assertEqual(grade.main(["--report", "/nonexistent/r.md", "--case", "optional-auth"]), 1)

    def test_omitting_case_is_a_usage_error_exiting_1_not_2(self):
        """--case is required because grading a report against a case whose
        fixture it never reviewed measures nothing. Exit 1, not argparse's
        default 2, which would be indistinguishable from a real regression."""
        self.report.write_text("anything")
        with self.assertRaises(SystemExit) as cm:
            grade.main(["--report", str(self.report)])
        self.assertEqual(cm.exception.code, 1)

    def test_unknown_case_is_a_usage_error_not_a_clean_pass(self):
        """A mistyped --case must not grade zero cases and exit 0."""
        self.report.write_text("anything")
        self.assertEqual(grade.main(["--report", str(self.report), "--case", "nope"]), 1)

    def test_failing_report_exits_2(self):
        self.report.write_text("nothing of substance")
        self.assertEqual(grade.main(["--report", str(self.report), "--case", "optional-auth"]), 2)


if __name__ == "__main__":
    unittest.main()
