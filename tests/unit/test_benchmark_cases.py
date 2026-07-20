"""The Level C cases were vacuous: their must_mention phrases sat in their
own prompt, the mock provider echoed the prompt back, and the assertion
checked that echo — so both passed with the fixture deleted entirely. The
defect was introduced by a fix that made canned responses repeat their
trigger phrases verbatim, which closed the loop it was meant to open.

These tests assert the property that was missing, not the symptom: a case
must FAIL when its fixture is removed. A case that cannot fail is not a
test, and the benchmark summary counts it toward a passing suite anyway.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import yaml_subset  # noqa: E402
from providers import mock  # noqa: E402

CASES_DIR = Path(paths.AKOS_HOME) / "benchmarks" / "cases"


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


if __name__ == "__main__":
    unittest.main()
