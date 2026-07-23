"""`.akos/config.md` lives in whatever repository the agent is working in,
including a cloned one, and skills/akos/SKILL.md tells the agent every
section of it is binding. So a project could lower the review profile,
add its own files to the agent's mandatory reading, and supply Notes
pre-authorized to override the agent's conclusions.

These lock the value checks. They do not — and cannot — test that an agent
actually runs the checker; that part is prose in SKILL.md, which is why the
skill labels it a mitigation rather than a control.
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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

    def test_missing_config_json_is_an_empty_list(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(
                config_check.main(
                    ["--dir", str(self.project), "--format", "json"]
                ),
                0,
            )
        self.assertEqual(json.loads(output.getvalue()), [])

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

    # --- Deployed flag: a closed yes/no value ---

    def test_deployed_accepts_only_yes_or_no(self):
        for good in ("yes", "no", "YES", "No"):
            with self.subTest(value=good):
                findings = self._check(f"## Project context\n- Deployed: {good}\n")
                self.assertNotIn("Deployed", self._fields(findings),
                                 f"{good!r} should be an accepted Deployed value")
        for bad in ("false-ish", "unknown", "no; rm -rf /", "maybe", "true"):
            with self.subTest(value=bad):
                findings = self._check(f"## Project context\n- Deployed: {bad}\n")
                self.assertIn("Deployed", self._fields(findings),
                              f"{bad!r} should be flagged as an ambiguous Deployed value")

    def test_duplicate_deployed_field_is_rejected(self):
        """Two declarations must not resolve silently by document order."""
        findings = self._check(
            "## Project context\n- Deployed: no\n- Deployed: yes\n")
        deployed = [f for f in findings if f["field"] == "Deployed"]
        self.assertTrue(deployed, "a duplicated Deployed field must be flagged")
        self.assertTrue(any(f["severity"] == "HIGH" for f in deployed))

    # --- Profile overrides: not authoritative from a repository ---

    def test_hostile_repo_config_cannot_override_security_minimums(self):
        """A repo-side profile override asking to switch off a security lens
        must surface as HIGH — the repo cannot rewrite the weight table."""
        findings = self._check(
            "## Profile overrides\n- security-reviewer: 0\n- accessibility-reviewer: 0\n")
        overrides = [f for f in findings if f["field"] == "Profile overrides"]
        self.assertTrue(overrides, "non-empty repo Profile overrides must be flagged")
        self.assertTrue(any(f["severity"] == "HIGH" for f in overrides))

    def test_empty_profile_overrides_section_is_clean(self):
        """Near-miss: the scaffolded template ships this section empty."""
        findings = self._check(
            "## Profile overrides\n\n## Packs to always load\n\n")
        self.assertNotIn("Profile overrides", self._fields(findings))

    def test_pack_path_escape_remains_critical(self):
        """The pre-existing traversal contract must survive the additions."""
        for entry in ("/etc/passwd", "../../elsewhere/notes", "./docs/x"):
            with self.subTest(entry=entry):
                findings = self._check(f"## Packs to always load\n\n- {entry}\n")
                self.assertIn("CRITICAL", {f["severity"] for f in findings})

    # --- Draft/deprecated packs: no self-authorization into always-load ---

    def _fake_akos_home_with_pack(self, domain: str, name: str, metadata_body: str) -> Path:
        home = self.project / "fake-akos-home"
        pack_dir = home / "packs" / domain / name
        pack_dir.mkdir(parents=True)
        (pack_dir / "metadata.yaml").write_text(metadata_body, encoding="utf-8")
        return home

    def test_config_always_load_rejects_draft_pack(self):
        home = self._fake_akos_home_with_pack(
            "ai-engineering", "some-draft-pack",
            "schema_version: 1\nname: some-draft-pack\ndomain: ai-engineering\n"
            "authority-level: 3\nversion: 1.0.0\ntags: []\nsources: []\nrelated: []\n"
            "status: draft\n",
        )
        findings = config_check.check_config(
            self._write("## Packs to always load\n\n- ai-engineering/some-draft-pack\n"),
            home,
        )
        self.assertTrue(any("draft" in f["message"] for f in findings),
                         f"expected a draft-pack finding, got {findings}")
        self.assertTrue(all(f["severity"] != "CRITICAL" for f in findings),
                         "a draft pack is advisory (MEDIUM), not a hard block")

    def test_config_always_load_rejects_deprecated_pack(self):
        home = self._fake_akos_home_with_pack(
            "ux", "old-pack",
            "schema_version: 1\nname: old-pack\ndomain: ux\nauthority-level: 3\n"
            "version: 1.0.0\ntags: []\nsources: []\nrelated: []\n"
            "status: deprecated\ndeprecated: true\nreplacement: ux/new-pack\n",
        )
        findings = config_check.check_config(
            self._write("## Packs to always load\n\n- ux/old-pack\n"),
            home,
        )
        self.assertTrue(any("deprecated" in f["message"] and "ux/new-pack" in f["message"] for f in findings),
                         f"expected a deprecated-pack finding naming the replacement, got {findings}")

    def test_config_always_load_accepts_stable_pack(self):
        home = self._fake_akos_home_with_pack(
            "ux", "stable-pack",
            "schema_version: 1\nname: stable-pack\ndomain: ux\nauthority-level: 3\n"
            "version: 1.0.0\ntags: []\nsources: []\nrelated: []\nstatus: stable\n",
        )
        findings = config_check.check_config(
            self._write("## Packs to always load\n\n- ux/stable-pack\n"),
            home,
        )
        self.assertEqual(findings, [])

    def test_no_allow_draft_packs_escape_hatch_exists(self):
        # The only sanctioned opt-in path is the current conversation's user
        # asking explicitly — never a field in this untrusted file. Locks
        # down that adding one wouldn't even do anything today.
        findings = self._check(
            "## Packs to always load\nallow_draft_packs: true\n\n- ux/wcag\n"
        )
        # allow_draft_packs is not a recognized pack-line shape at all under
        # PACK_LINE_RE/PACK_ENTRY_RE, so it either resolves to nothing or, if
        # ever matched, must never suppress the draft/deprecated findings for
        # real entries in the same section.
        self.assertNotIn("draft", " ".join(f["message"] for f in findings))


if __name__ == "__main__":
    unittest.main()
