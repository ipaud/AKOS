"""`.akos/config.md` lives in whatever repository the agent is working in,
including a cloned one, and skills/akos/SKILL.md tells the agent every
section of it is binding. So a project could lower the review profile,
add its own files to the agent's mandatory reading, and supply Notes
pre-authorized to override the agent's conclusions.

These lock the value checks. They do not — and cannot — test that an agent
actually runs the checker; that part is prose in SKILL.md, which is why the
skill labels it a mitigation rather than a control.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import config_check  # noqa: E402

AKOS_HOME = Path(paths.AKOS_HOME)


class TestConfigCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        (self.project / ".akos").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, body: str) -> Path:
        p = self.project / ".akos" / "config.md"
        p.write_text(body, encoding="utf-8")
        return p

    def _check(self, body: str):
        return config_check.check_config(self._write(body), AKOS_HOME)

    def _fields(self, findings):
        return {f["field"] for f in findings}

    def test_a_legitimate_config_is_clean(self):
        findings = self._check(
            "## Reasoning profile\nprofile: Production\n"
            "## Personal profile\npersonal_profile: pau-avila\n"
            "## Packs to always load\n\n- packs/ux/wcag\n- backend/supabase\n"
        )
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    def test_unknown_profile_is_flagged(self):
        findings = self._check("## Reasoning profile\nprofile: Prototype-NoSecurity\n")
        self.assertIn("profile", self._fields(findings))

    def test_every_real_profile_is_accepted(self):
        for name in config_check.VALID_PROFILES:
            with self.subTest(profile=name):
                findings = self._check(f"## Reasoning profile\nprofile: {name}\n")
                self.assertEqual(findings, [])

    def test_traversal_in_personal_profile_is_flagged(self):
        findings = self._check("## Personal profile\npersonal_profile: ../../../etc\n")
        self.assertIn("personal_profile", self._fields(findings))

    def test_project_relative_pack_path_is_critical(self):
        """The actual attack: a path the agent resolves against the project,
        loading attacker-authored prose as authoritative knowledge. An
        earlier version of this checker resolved it AKOS-relative and
        reported it as merely 'missing' — a MEDIUM for the thing the check
        exists to catch."""
        findings = self._check(
            "## Packs to always load\n\n- ./docs/architecture-notes\n")
        crit = [f for f in findings if f["severity"] == "CRITICAL"]
        self.assertTrue(crit, f"expected a CRITICAL, got {findings}")

    def test_absolute_and_parent_paths_are_critical(self):
        for entry in ("/etc/passwd", "../../elsewhere/notes", "~/notes"):
            with self.subTest(entry=entry):
                findings = self._check(f"## Packs to always load\n\n- {entry}\n")
                self.assertTrue([f for f in findings if f["severity"] == "CRITICAL"],
                                f"{entry} should be CRITICAL, got {findings}")

    def test_nonexistent_but_well_formed_pack_is_not_critical(self):
        """Shape and existence are different problems and must not collapse:
        a typo'd real pack is a MEDIUM, not an attack."""
        findings = self._check("## Packs to always load\n\n- packs/nonexistent/thing\n")
        self.assertTrue(findings)
        self.assertNotIn("CRITICAL", {f["severity"] for f in findings})

    def test_missing_config_is_not_an_error(self):
        self.assertEqual(config_check.main(["--dir", str(self.project)]), 0)

    def test_exit_code_is_2_on_findings(self):
        self._write("## Packs to always load\n\n- ./evil\n")
        self.assertEqual(config_check.main(["--dir", str(self.project)]), 2)

    def test_usage_error_exits_1_not_2(self):
        """argparse defaults to 2 on a bad flag, which collides with
        "2 means findings" — a caller could not tell a typo from a hostile
        config. docs/cli/exit-codes.md reserves 1 for usage errors."""
        with self.assertRaises(SystemExit) as cm:
            config_check.main(["--nosuchflag"])
        self.assertEqual(cm.exception.code, 1)

    def test_positional_and_flag_forms_agree(self):
        self._write("## Packs to always load\n\n- ./evil\n")
        self.assertEqual(config_check.main([str(self.project)]), 2)
        self.assertEqual(config_check.main(["--dir", str(self.project)]), 2)


if __name__ == "__main__":
    unittest.main()
