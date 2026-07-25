import importlib.util
import json
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402


AKOS_HOME = Path(paths.AKOS_HOME)
CI_WORKFLOW = AKOS_HOME / ".github" / "workflows" / "ci.yml"
SELF_SCAN_GATE = AKOS_HOME / "tests" / "ci" / "self_scan_gate.py"


def _load_gate():
    spec = importlib.util.spec_from_file_location("self_scan_gate", SELF_SCAN_GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCIWorkflowContract(unittest.TestCase):
    def test_quality_and_functional_jobs_are_separate(self):
        text = CI_WORKFLOW.read_text()
        self.assertRegex(text, r"(?m)^  quality:\s*$")
        self.assertRegex(text, r"(?m)^  functional:\s*$")

    def test_functional_matrix_covers_minimum_python_and_macos(self):
        text = CI_WORKFLOW.read_text()
        self.assertIn("ubuntu-latest", text)
        self.assertIn('"3.10"', text)
        self.assertIn("macos-latest", text)
        self.assertIn("5fda3b95a4ea91299a34e894583c3862153e4b97", text)

    def test_coverage_is_branch_aware_and_gates_at_80(self):
        config = (AKOS_HOME / ".coveragerc").read_text()
        requirements = (AKOS_HOME / "requirements-dev.txt").read_text()
        workflow = CI_WORKFLOW.read_text()

        self.assertRegex(config, r"(?m)^branch\s*=\s*True$")
        self.assertRegex(config, r"(?m)^fail_under\s*=\s*80$")
        self.assertIn("coverage==7.15.2", requirements)
        self.assertIn("coverage run", workflow)
        self.assertIn("coverage report", workflow)
        self.assertIn(
            "python3 tests/ci/run_integrations.py --coverage",
            workflow,
        )

    def test_dependabot_tracks_the_dev_requirement(self):
        config = (AKOS_HOME / ".github" / "dependabot.yml").read_text()
        self.assertIn('package-ecosystem: "pip"', config)
        self.assertRegex(
            config,
            r'(?s)package-ecosystem: "pip".*?directory: "/"'
            r'.*?interval: "weekly"',
        )


class TestSelfScanGate(unittest.TestCase):
    def _fake_akos(self, returncode, payload):
        tmp = tempfile.TemporaryDirectory()
        script = Path(tmp.name) / "akos"
        script.write_text(
            "#!/usr/bin/env python3\n"
            "import json, sys\n"
            f"print(json.dumps({payload!r}))\n"
            f"raise SystemExit({returncode})\n"
        )
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        self.addCleanup(tmp.cleanup)
        return script

    def test_accepts_complete_scan_with_blocking_findings(self):
        gate = _load_gate()
        akos = self._fake_akos(2, {
            "status": "findings",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{
                "severity": "CRITICAL",
                "rule_id": "SUPABASE_RLS_DISABLED",
                "evidence": [{
                    "path": (
                        "benchmarks/cases/supabase-rls-basic/"
                        "fixture/supabase/migrations/0001_init.sql"
                    ),
                }],
            }],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 0)

    def test_rejects_blocking_finding_outside_expected_fixtures(self):
        gate = _load_gate()
        akos = self._fake_akos(2, {
            "status": "findings",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{
                "severity": "CRITICAL",
                "evidence": [{"path": "rules/security/production.py"}],
            }],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_rejects_secret_even_inside_a_fixture_directory(self):
        gate = _load_gate()
        akos = self._fake_akos(2, {
            "status": "findings",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{
                "severity": "CRITICAL",
                "rule_id": "SECRET_IN_SOURCE",
                "evidence": [{
                    "path": (
                        "benchmarks/cases/supabase-rls-basic/"
                        "fixture/credential.py"
                    ),
                }],
            }],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_rejects_unknown_case_even_for_allowlisted_rule(self):
        gate = _load_gate()
        akos = self._fake_akos(2, {
            "status": "findings",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{
                "severity": "CRITICAL",
                "rule_id": "SUPABASE_RLS_DISABLED",
                "evidence": [{
                    "path": (
                        "benchmarks/cases/new-unreviewed-case/"
                        "fixture/schema.sql"
                    ),
                }],
            }],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_accepts_complete_clean_scan(self):
        gate = _load_gate()
        akos = self._fake_akos(0, {
            "status": "ok",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 0,
                "errors": 0,
            },
            "findings": [],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 0)

    def test_rejects_operational_exit_even_with_parseable_json(self):
        gate = _load_gate()
        akos = self._fake_akos(1, {
            "status": "error",
            "summary": {"rules_discovered": 8, "rules_executed": 7},
            "findings": [],
            "errors": [{"phase": "detector", "message": "boom"}],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_rejects_errors_hidden_behind_success_exit(self):
        gate = _load_gate()
        akos = self._fake_akos(0, {
            "status": "error",
            "summary": {"rules_discovered": 8, "rules_executed": 7},
            "findings": [],
            "errors": [{"phase": "detector", "message": "boom"}],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_rejects_incomplete_rule_execution_with_success_exit(self):
        gate = _load_gate()
        akos = self._fake_akos(0, {
            "status": "ok",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 7,
                "findings": 0,
                "errors": 0,
            },
            "findings": [],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_rejects_summary_counter_drift(self):
        gate = _load_gate()
        akos = self._fake_akos(0, {
            "status": "ok",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 2,
                "errors": 0,
            },
            "findings": [],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_exit_two_requires_a_blocking_finding(self):
        gate = _load_gate()
        akos = self._fake_akos(2, {
            "status": "findings",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{"severity": "MEDIUM", "blocking": False}],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)

    def test_exit_zero_rejects_a_blocking_finding(self):
        gate = _load_gate()
        akos = self._fake_akos(0, {
            "status": "ok",
            "summary": {
                "rules_discovered": 8,
                "rules_executed": 8,
                "findings": 1,
                "errors": 0,
            },
            "findings": [{"severity": "HIGH", "blocking": True}],
            "errors": [],
        })
        self.assertEqual(gate.main(["--akos-bin", str(akos), "--target", "."]), 1)


if __name__ == "__main__":
    unittest.main()
