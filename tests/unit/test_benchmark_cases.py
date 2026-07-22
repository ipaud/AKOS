"""The Level C cases were vacuous: their must_mention phrases sat in their
own prompt, the mock provider echoed the prompt back, and the assertion
checked that echo — so both passed with the fixture deleted entirely. The
defect was introduced by a fix that made canned responses repeat their
trigger phrases verbatim, which closed the loop it was meant to open.

These tests assert the property that was missing, not the symptom: a case
must FAIL when its fixture is removed. A case that cannot fail is not a
test, and the benchmark summary counts it toward a passing suite anyway.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import yaml_subset  # noqa: E402
import runner as rules_runner  # noqa: E402
from providers import mock  # noqa: E402

CASES_DIR = Path(paths.AKOS_HOME) / "benchmarks" / "cases"


def _load_bench_runner():
    path = Path(paths.AKOS_HOME) / "benchmarks" / "runners" / "run.py"
    spec = importlib.util.spec_from_file_location("bench_run", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _level_c_cases():
    for d in sorted(CASES_DIR.iterdir()):
        spec = d / "expected.yaml"
        if not spec.is_file():
            continue
        expected = yaml_subset.load(spec)
        if expected.get("level") == "C":
            yield d.name, expected, d


def _mock_response(prompt: str, fixture_dir: Path | None) -> str:
    parts = [prompt]
    if fixture_dir is not None:
        for f in sorted(fixture_dir.rglob("*")):
            if f.is_file():
                parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return mock.generate("\n".join(parts))


class TestLevelCCasesAreFalsifiable(unittest.TestCase):
    def test_there_is_at_least_one_level_c_case(self):
        self.assertTrue(list(_level_c_cases()),
                        "this file asserts a property of Level C cases; finding none means "
                        "the guard silently covers nothing")

    def test_each_case_passes_with_its_fixture(self):
        for name, expected, case_dir in _level_c_cases():
            with self.subTest(case=name):
                response = _mock_response(expected["prompt"], case_dir / "fixture")
                missing = [p for p in expected["must_mention"] if p.lower() not in response.lower()]
                self.assertEqual(missing, [], f"{name} should pass with its fixture present")

    def test_each_case_fails_without_its_fixture(self):
        """The load-bearing one. If this passes, the fixture is decorative
        and the case is asserting that the prompt contains what the prompt
        contains."""
        for name, expected, _ in _level_c_cases():
            with self.subTest(case=name):
                response = _mock_response(expected["prompt"], None)
                missing = [p for p in expected["must_mention"] if p.lower() not in response.lower()]
                self.assertNotEqual(
                    missing, [],
                    f"{name} passes with no fixture at all — its must_mention phrases are "
                    f"satisfied by the prompt alone, so the case cannot detect any regression")

    def test_no_must_mention_phrase_appears_in_its_own_prompt(self):
        """The mechanism behind the vacuous pass, asserted directly so the
        failure names the cause rather than the symptom."""
        for name, expected, _ in _level_c_cases():
            with self.subTest(case=name):
                prompt = expected["prompt"].lower()
                leaked = [p for p in expected["must_mention"] if p.lower() in prompt]
                self.assertEqual(
                    leaked, [],
                    f"{name}: must_mention {leaked} appears in the prompt, so the mock echoes "
                    f"it back and the assertion is circular")


class TestBenchmarkFailsClosed(unittest.TestCase):
    """A benchmark case must not be counted as passed when a rule it depends on
    did not actually execute (P0-3). Otherwise a broken detector reads as a
    green benchmark."""

    def test_benchmark_case_fails_when_required_rule_did_not_execute(self):
        bench = _load_bench_runner()
        # A real case with a real must_detect expectation.
        case_dir = CASES_DIR / "secret-vendor-key"
        expected = yaml_subset.load(case_dir / "expected.yaml")

        # Simulate the required rule failing to run: run_rules records an
        # ExecutionError and returns no findings.
        def broken_run_rules(target_dir, rules, profile=None, errors=None):
            if errors is not None:
                errors.append(rules_runner.ExecutionError(
                    "detector", "SECRET_IN_SOURCE", "rules/security/secret-in-source.py",
                    "simulated crash"))
            return []

        original = bench.rules_runner.run_rules
        bench.rules_runner.run_rules = broken_run_rules
        try:
            result = bench.run_deterministic_case(expected, case_dir)
        finally:
            bench.rules_runner.run_rules = original

        self.assertFalse(result["passed"],
                         "a case whose required rule did not execute must not pass")
        self.assertTrue(result["execution_errors"],
                        "the operational error must be surfaced in the case result")

    def test_benchmark_materialization_does_not_modify_source_fixture(self):
        """The versioned fixture keeps its placeholder; the credential-shaped
        value exists only in the throwaway temp copy (P0-4)."""
        bench = _load_bench_runner()
        src = CASES_DIR / "secret-vendor-key" / "fixture" / "src" / "config.ts"
        before = src.read_text(encoding="utf-8")
        self.assertIn("{{AKOS_TEST_AWS_ACCESS_KEY}}", before,
                      "the versioned fixture should hold a placeholder, not a real key")

        real_value = bench.SECRET_PLACEHOLDERS["{{AKOS_TEST_AWS_ACCESS_KEY}}"]
        with bench.materialized_case(CASES_DIR / "secret-vendor-key") as base:
            materialized = (base / "fixture" / "src" / "config.ts").read_text(encoding="utf-8")
            self.assertIn(real_value, materialized,
                          "the temp copy must carry the materialized real value")
            self.assertNotIn("{{AKOS_TEST_AWS_ACCESS_KEY}}", materialized)

        # The versioned source is untouched, and the temp copy is gone.
        self.assertEqual(src.read_text(encoding="utf-8"), before)
        self.assertNotIn(real_value, src.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
