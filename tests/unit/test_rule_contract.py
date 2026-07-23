"""Versioned rule-registry and suppression-policy contract tests."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import rule_schema  # noqa: E402
import runner  # noqa: E402


AKOS_HOME = Path(paths.AKOS_HOME)


class RuleRegistryContractCase(unittest.TestCase):
    def test_every_real_registry_satisfies_the_v1_contract(self):
        failures = {}
        for yaml_path in sorted((AKOS_HOME / "rules").glob("*/*.yaml")):
            errors = rule_schema.validate_rule_file(yaml_path, AKOS_HOME)
            if errors:
                failures[str(yaml_path.relative_to(AKOS_HOME))] = errors
        self.assertEqual(failures, {})

    def test_security_floor_rules_are_explicitly_non_suppressible(self):
        expected = {
            "SECRET_IN_SOURCE",
            "SERVICE_ROLE_IN_CLIENT",
            "SUPABASE_POLICY_TOO_PERMISSIVE",
            "SUPABASE_RLS_DISABLED",
        }
        actual = {
            rule.id
            for rule in runner.discover_rules(rule_filter=expected)
            if not rule.suppressible
        }
        self.assertEqual(actual, expected)


class SuppressionPolicyCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_secret_allow_comment_cannot_suppress_a_real_secret(self):
        token = "AKIA" + "ABCDEFGHIJKLMNOP"
        path = self.project / "src" / "config.ts"
        path.parent.mkdir(parents=True)
        path.write_text(
            f"// akos:allow SECRET_IN_SOURCE\nconst key = '{token}';\n",
            encoding="utf-8",
        )
        rule = runner.discover_rules(rule_filter={"SECRET_IN_SOURCE"})[0]
        findings = runner.run_rules(self.project, [rule], "Production")
        self.assertEqual(len(findings), 1)
        self.assertTrue(findings[0]["blocking"])

    def test_policy_allow_comment_cannot_suppress_a_permissive_rls_policy(self):
        path = self.project / "supabase" / "migrations" / "001.sql"
        path.parent.mkdir(parents=True)
        path.write_text(
            "-- akos:allow SUPABASE_POLICY_TOO_PERMISSIVE\n"
            "CREATE POLICY public_read ON plans FOR SELECT USING (true);\n",
            encoding="utf-8",
        )
        rule = runner.discover_rules(
            rule_filter={"SUPABASE_POLICY_TOO_PERMISSIVE"}
        )[0]
        findings = runner.run_rules(self.project, [rule], "Production")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "SUPABASE_POLICY_TOO_PERMISSIVE")

    def test_suppressible_defaults_true_for_legacy_registries(self):
        data = {
            "id": "DEFAULT_SUPPRESSION",
            "title": "Test",
            "domain": "testing",
            "level": "A",
            "severity": {"default": "MEDIUM"},
            "confidence": "High",
            "related_packs": [],
            "detector": "rules/testing/default-suppression.py",
            "applies_to": {"glob": ["**/*.txt"], "target": "project-source"},
            "recommendation": "Fix it.",
            "references": [],
            "version": 1,
            "status": "stable",
        }
        self.assertTrue(runner.Rule(Path("rule.yaml"), data).suppressible)


if __name__ == "__main__":
    unittest.main()
