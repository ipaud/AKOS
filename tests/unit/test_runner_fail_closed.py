"""The rules runner must fail closed. A detector or registry that cannot run
is an operational error (status 'error', exit 1), never a finding and never a
clean pass — the failure mode where a broken security detector silently
reported the codebase clean. These build a throwaway AKOS_HOME with a temp
rules/ tree (patching runner.AKOS_HOME) so no real repo file is touched.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
related_packs: []
applies_to:
  target: project-source
  glob: ["**/*.txt"]
detector: rules/testdomain/{rid}.py
recommendation: Fix the test finding.
references: []
version: 1
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

    def test_detector_returning_none_is_a_structured_error(self):
        self._rule("NONE", "def run(files):\n    return None\n")
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertEqual(result.findings, [])
        self.assertTrue(any(e.rule_id == "NONE" and e.phase == "detector"
                            for e in result.errors))

    def test_detector_generator_failing_after_yield_is_a_structured_error(self):
        self._rule(
            "LATE",
            "def run(files):\n"
            "    yield {'evidence': [{'path': str(files[0]), 'line_start': 1}]}\n"
            "    raise RuntimeError('late generator failure')\n",
        )
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertEqual(
            result.findings,
            [],
            "a partially-consumed detector result must not leak partial findings",
        )
        self.assertTrue(any(e.rule_id == "LATE" and "late generator failure" in e.message
                            for e in result.errors))

    def test_malformed_finding_is_a_structured_error(self):
        self._rule("MALFORMED", "def run(files):\n    return [{'evidence': 'not-a-list'}]\n")
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertEqual(result.findings, [])
        self.assertTrue(any(e.rule_id == "MALFORMED" and e.phase == "detector"
                            for e in result.errors))

    def test_rule_runner_returns_error_when_registry_is_invalid(self):
        # Missing the required `detector` key.
        bad = "id: BADREG\ntitle: x\ndomain: testdomain\nseverity:\n  default: LOW\n"
        self._rule("BADREG", "def run(files):\n    return []\n", registry=bad)
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "discovery" for e in result.errors))

    def test_unknown_registry_field_fails_closed(self):
        registry = VALID_REGISTRY.format(rid="TYPO", severity="MEDIUM") + "supressible: false\n"
        self._rule("TYPO", "def run(files):\n    return []\n", registry=registry)
        result = runner.scan(self.scan)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "discovery" and "supressible" in e.message
                            for e in result.errors))

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

    def test_read_error_is_reported_as_read_phase_and_exits_incomplete(self):
        self._rule("READER", "def run(files):\n"
                   "    return [{'evidence': [{'path': str(files[0]), 'line_start': 1}]}]\n")
        target = self.scan / "a.txt"
        original_open = Path.open

        def fail_target_open(path, *args, **kwargs):
            if path == target:
                raise PermissionError("simulated unreadable input")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", fail_target_open):
            result = runner.scan(self.scan)

        self.assertEqual(result.status, "error")
        self.assertEqual(result.findings, [])
        self.assertTrue(any(e.phase == "read" and e.path == str(target)
                            for e in result.errors))

    def test_suppression_context_read_error_cannot_be_swallowed(self):
        self._rule(
            "SUPPRESSION_READ",
            "def run(files):\n"
            "    return [{'evidence': [{'path': str(files[0]), 'line_start': 1}]}]\n",
        )
        target = self.scan / "a.txt"
        original_open = Path.open
        target_opens = 0

        def fail_second_target_open(path, *args, **kwargs):
            nonlocal target_opens
            if path == target:
                target_opens += 1
                if target_opens == 2:
                    raise PermissionError("simulated suppression reread failure")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", fail_second_target_open):
            result = runner.scan(self.scan)

        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "read" and e.path == str(target)
                            for e in result.errors))

    def test_default_limits_are_explicit_and_bounded(self):
        self.assertEqual(runner.DEFAULT_MAX_FILES, 10_000)
        self.assertEqual(runner.DEFAULT_MAX_FILE_BYTES, 2 * 1024 * 1024)
        self.assertEqual(runner.DEFAULT_MAX_TOTAL_BYTES, 100 * 1024 * 1024)

    def test_file_count_limit_fails_closed(self):
        self._rule("LIMITED", "def run(files):\n    return []\n")
        (self.scan / "b.txt").write_text("world\n", encoding="utf-8")
        limits = runner.ScanLimits(max_files=1, max_file_bytes=1024, max_total_bytes=2048)
        result = runner.scan(self.scan, limits=limits)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "setup" and "max files" in e.message.lower()
                            for e in result.errors))

    def test_per_file_limit_fails_closed(self):
        self._rule("LIMITED", "def run(files):\n    return []\n")
        limits = runner.ScanLimits(max_files=10, max_file_bytes=3, max_total_bytes=100)
        result = runner.scan(self.scan, limits=limits)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "setup" and e.path == str(self.scan / "a.txt")
                            for e in result.errors))

    def test_total_byte_limit_fails_closed(self):
        self._rule("LIMITED", "def run(files):\n    return []\n")
        (self.scan / "b.txt").write_text("world\n", encoding="utf-8")
        limits = runner.ScanLimits(max_files=10, max_file_bytes=100, max_total_bytes=10)
        result = runner.scan(self.scan, limits=limits)
        self.assertEqual(result.status, "error")
        self.assertTrue(any(e.phase == "setup" and "total byte" in e.message.lower()
                            for e in result.errors))

    def test_ignored_directories_are_pruned_before_descent(self):
        self._rule("PRUNED", "def run(files):\n    return []\n")
        ignored = self.scan / "node_modules"
        ignored.mkdir()
        for index in range(20):
            (ignored / f"dependency-{index}.txt").write_text("ignored\n", encoding="utf-8")

        scanned_directories = []
        real_scandir = os.scandir

        def recording_scandir(path):
            scanned_directories.append(Path(path))
            return real_scandir(path)

        limits = runner.ScanLimits(max_files=1, max_file_bytes=1024, max_total_bytes=1024)
        with mock.patch.object(runner.os, "scandir", side_effect=recording_scandir):
            result = runner.scan(self.scan, limits=limits)

        self.assertEqual(result.status, "ok")
        self.assertIn(self.scan, scanned_directories)
        self.assertNotIn(ignored, scanned_directories)

    def test_symlink_entries_count_toward_traversal_budget(self):
        self._rule("LINKS", "def run(files):\n    return []\n")
        (self.scan / "a.txt").unlink()
        outside = Path(self._scan_tmp.name).parent / "akos-runner-outside"
        for index in range(2):
            (self.scan / f"link-{index}.txt").symlink_to(outside)
        limits = runner.ScanLimits(
            max_files=1,
            max_file_bytes=1024,
            max_total_bytes=1024,
        )

        result = runner.scan(self.scan, limits=limits)

        self.assertEqual(result.status, "error")
        self.assertTrue(any("traversal" in error.message for error in result.errors))

    def test_suppression_directive_must_be_in_a_comment(self):
        target = self.scan / "a.txt"
        finding = {
            "evidence": [{
                "path": str(target),
                "line_start": 1,
                "line_end": 1,
            }]
        }
        target.write_text(
            "select 'akos:allow SUPPRESSION';\n",
            encoding="utf-8",
        )
        self.assertFalse(runner.is_suppressed(finding, "SUPPRESSION", {}))

        target.write_text(
            "-- akos:allow SUPPRESSION\nselect true;\n",
            encoding="utf-8",
        )
        finding["evidence"][0]["line_start"] = 2
        self.assertTrue(runner.is_suppressed(finding, "SUPPRESSION", {}))

    def test_target_filter_selects_only_requested_rule_surface(self):
        self._rule("PROJECT", "def run(files):\n    return []\n")
        registry = VALID_REGISTRY.format(rid="PACKS", severity="MEDIUM").replace(
            "target: project-source", "target: akos-packs"
        )
        self._rule("PACKS", "def run(files):\n    return []\n", registry=registry)
        project_rules = runner.discover_rules(target_filter={"project-source"})
        pack_rules = runner.discover_rules(target_filter={"akos-packs"})
        self.assertEqual([r.id for r in project_rules], ["PROJECT"])
        self.assertEqual([r.id for r in pack_rules], ["PACKS"])

    def test_usage_errors_exit_one_and_cli_limits_reject_zero(self):
        with self.assertRaises(SystemExit) as cm:
            runner.main([str(self.scan), "--max-files", "0"])
        self.assertEqual(cm.exception.code, 1)

    def test_cli_accepts_target_filter(self):
        self._rule("PROJECT", "def run(files):\n    return []\n")
        self.assertEqual(
            runner.main([str(self.scan), "--target", "project-source"]),
            0,
        )


if __name__ == "__main__":
    unittest.main()
