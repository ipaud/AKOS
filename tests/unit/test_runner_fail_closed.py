"""The rules runner must fail closed. A detector or registry that cannot run
is an operational error (status 'error', exit 1), never a finding and never a
clean pass — the failure mode where a broken security detector silently
reported the codebase clean. These build a throwaway AKOS_HOME with a temp
rules/ tree (patching runner.AKOS_HOME) so no real repo file is touched.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import runner  # noqa: E402  (rules/runner.py, on path via paths helper)

VALID_REGISTRY = """\
id: {rid}
title: A test rule
domain: testdomain
level: A
severity:
  default: {severity}
confidence: High
applies_to:
  target: project-source
  glob: ["**/*.txt"]
detector: rules/testdomain/{rid}.py
status: stable
"""


class RunnerFailClosedCase(unittest.TestCase):
    def setUp(self):
        self._home_tmp = tempfile.TemporaryDirectory()
        self._scan_tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._home_tmp.name)
        self.scan = Path(self._scan_tmp.name)
        (self.home / "rules").mkdir()
        # A file for detectors to "find".
        (self.scan / "a.txt").write_text("hello\n", encoding="utf-8")
        self._saved_home = runner.AKOS_HOME
        runner.AKOS_HOME = self.home

    def tearDown(self):
        runner.AKOS_HOME = self._saved_home
        self._home_tmp.cleanup()
        self._scan_tmp.cleanup()

    def _rule(self, rid: str, detector_body: str, *, severity: str = "MEDIUM",
              registry: str | None = None, write_detector: bool = True):
        dom = self.home / "rules" / "testdomain"
        dom.mkdir(parents=True, exist_ok=True)
        reg = registry if registry is not None else VALID_REGISTRY.format(rid=rid, severity=severity)
        (dom / f"{rid}.yaml").write_text(reg, encoding="utf-8")
        if write_detector:
            (dom / f"{rid}.py").write_text(detector_body, encoding="utf-8")

    # --- operational errors ---

    def test_rule_runner_returns_error_when_detector_crashes(self):
        self._rule("CRASHER", "def run(files):\n    raise RuntimeError('boom')\n")
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "detector" and e.rule_id == "CRASHER" for e in result.errors))
        self.assertEqual(result.findings, [])

    def test_rule_runner_returns_error_when_detector_file_is_missing(self):
        self._rule("NOFILE", "", write_detector=False)
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.rule_id == "NOFILE" for e in result.errors))

    def test_rule_runner_returns_error_when_detector_has_no_run_function(self):
        self._rule("NORUN", "x = 1  # no run()\n")
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any("run()" in e.message for e in result.errors))

    def test_rule_runner_returns_error_when_registry_is_invalid(self):
        # Missing the required `detector` key.
        bad = "id: BADREG\ntitle: x\ndomain: testdomain\nseverity:\n  default: LOW\n"
        self._rule("BADREG", "def run(files):\n    return []\n", registry=bad)
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "discovery" for e in result.errors))

    def test_discover_rules_raises_when_no_collector_and_registry_invalid(self):
        """The count-only caller (ci.yml) has no errors list, so it must fail
        loudly rather than silently discover fewer rules."""
        bad = "id: BADREG\ntitle: x\ndomain: testdomain\n:\n  : : :\n"
        self._rule("BADREG", "def run(files):\n    return []\n", registry=bad)
        with self.assertRaises(runner.RegistryError):
            runner.discover_rules()

    # --- exit-code contract ---

    def test_rule_runner_json_separates_findings_and_errors(self):
        self._rule("CRASHER", "def run(files):\n    raise RuntimeError('boom')\n")
        obj = runner._result_to_json(runner.scan(self.scan))
        self.assertEqual(obj["status"], "error")
        self.assertIn("findings", obj)
        self.assertIn("errors", obj)
        self.assertEqual(obj["findings"], [])
        self.assertTrue(obj["errors"])
        self.assertEqual(obj["summary"]["errors"], len(obj["errors"]))

    def test_rule_runner_error_exit_precedes_critical_finding_exit(self):
        # One rule emits a CRITICAL; another crashes. Errors win → exit 1.
        self._rule("GOODCRIT",
                   "def run(files):\n"
                   "    return [{'evidence': [{'path': str(files[0]), 'line_start': 1}],\n"
                   "             'severity_override': 'CRITICAL'}]\n")
        self._rule("CRASHER", "def run(files):\n    raise RuntimeError('boom')\n")
        self.assertEqual(runner.main([str(self.scan)]), 1)

    def test_rule_runner_clean_execution_still_returns_zero(self):
        self._rule("CLEAN", "def run(files):\n    return []\n")
        self.assertEqual(runner.main([str(self.scan)]), 0)

    def test_rule_runner_complete_critical_scan_returns_two(self):
        self._rule("GOODCRIT",
                   "def run(files):\n"
                   "    return [{'evidence': [{'path': str(files[0]), 'line_start': 1}],\n"
                   "             'severity_override': 'CRITICAL'}]\n")
        self.assertEqual(runner.main([str(self.scan)]), 2)

    def test_blocking_flag_gates_even_at_high_severity(self):
        """A HIGH finding a rule marks blocking gates to exit 2 (P0-4 signal)."""
        self._rule("HIGHBLOCK",
                   "def run(files):\n"
                   "    return [{'evidence': [{'path': str(files[0]), 'line_start': 1}],\n"
                   "             'severity_override': 'HIGH', 'blocking': True}]\n",
                   severity="HIGH")
        self.assertEqual(runner.main([str(self.scan)]), 2)

    def test_no_stable_rules_without_filter_is_setup_error(self):
        # Empty rules/ tree → cannot report a clean scan.
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "setup" for e in result.errors))


if __name__ == "__main__":
    unittest.main()
