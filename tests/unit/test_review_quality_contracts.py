"""Cross-file contracts for review scoring, routing, examples, and onboarding."""

import re
import unittest
from pathlib import Path


AKOS_HOME = Path(__file__).resolve().parent.parent.parent


def read(rel_path: str) -> str:
    return (AKOS_HOME / rel_path).read_text(encoding="utf-8")


class TestMobileReviewContract(unittest.TestCase):
    def test_overall_score_has_the_profile_mobile_weights(self):
        overall = read("scoring/overall-score.md")
        row = re.search(r"^\|\s*Mobile\s*\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|",
                        overall, re.MULTILINE)
        self.assertIsNotNone(row, "Mobile is a scored dimension and needs an Overall weight row")
        self.assertEqual(
            [int(value.strip()) for value in row.groups()],
            [1, 2, 3, 2, 1, 1],
        )

    def test_mobile_reviewer_forbids_fabricated_runtime_measurements(self):
        reviewer = read("agents/mobile-reviewer.md")
        self.assertIn("Mobile score", reviewer)
        self.assertIn("`n/a`", reviewer)
        self.assertRegex(reviewer, r"(?i)rendered|runtime")
        self.assertRegex(reviewer, r"(?i)evidence|coverage")

    def test_full_frontend_route_and_startup_mvp_are_explicit(self):
        workflow = read("workflows/ui-screen-review.md")
        skill = read("skills/akos-review/SKILL.md")
        prompt = read("prompts/run-ux-review.md")
        self.assertRegex(workflow, r"profiles:\s*\[[^\]]*Startup MVP[^\]]*\]")
        self.assertIn("Startup MVP", workflow)
        self.assertRegex(skill, r"(?i)full frontend")
        self.assertRegex(prompt, r"(?i)full frontend")


class TestTouchParsingExample(unittest.TestCase):
    def test_parse_amount_example_rejects_trailing_junk_and_bad_grouping(self):
        framework = read("packs/mobile/touch-ergonomics/decision-framework.md")
        self.assertNotIn(r".replace(/[^\d.\-]/g, '')", framework)
        self.assertRegex(framework, r"parseAmount\(['\"]12oops['\"][^)]*\).*null")
        self.assertRegex(framework, r"parseAmount\(['\"]1,2,3['\"][^)]*\).*null")


class TestReadmeOnboardingContract(unittest.TestCase):
    def test_path_instructions_update_the_current_shell(self):
        readme = read("README.md")
        self.assertRegex(readme, r'(?m)^export PATH="\$HOME/bin:\$PATH"$')

    def test_codex_plugin_instructions_add_marketplace_and_plugin(self):
        readme = read("README.md")
        self.assertIn("codex plugin marketplace add ipaud/AKOS", readme)
        self.assertIn("codex plugin add akos@akos", readme)

    def test_product_activation_baseline_is_explicit_and_telemetry_free(self):
        artifact = AKOS_HOME / "docs/product/activation-baseline.md"
        self.assertTrue(artifact.is_file(), "the primary job and activation baseline need a durable artifact")
        text = artifact.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)solo.*(?:Codex|Claude)")
        self.assertRegex(text, r"(?i)baseline.*not (?:yet )?measured")
        self.assertRegex(text, r"(?i)4 (?:of|out of) 5")
        self.assertRegex(text, r"(?is)median.*?10 minutes")
        self.assertRegex(text, r"(?i)without telemetry|no telemetry")


if __name__ == "__main__":
    unittest.main()
