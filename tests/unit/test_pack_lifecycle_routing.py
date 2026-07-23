"""A pack's lifecycle status (`stable` / `draft` / `deprecated`) must have a
real operational consequence — before this, all 6 `ai-engineering/*` draft
packs sat in `skills/akos/SKILL.md`'s single routing table identically
formatted to the 48 stable packs, one even labeled "Safety floor."

These tests derive expectations by reading the REAL corpus's metadata.yaml
files at test time — never a hardcoded list of "the 6 draft packs" — so a
future promotion/demotion doesn't silently stale the test.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import routing_check as rc  # noqa: E402
import yaml_subset as y  # noqa: E402

AKOS_HOME = Path(paths.AKOS_HOME)


def _real_pack_statuses() -> dict:
    return rc.load_pack_statuses(AKOS_HOME)


class TestRoutingCheckAgainstRealCorpus(unittest.TestCase):
    def test_stable_routing_catalog_contains_only_stable_packs(self):
        errors = rc.check_stable_routing(AKOS_HOME)
        self.assertEqual(errors, [], f"real repo should have zero routing violations: {errors}")

    def test_draft_pack_is_absent_from_automatic_routing(self):
        statuses = _real_pack_statuses()
        draft_ids = {pid for pid, status in statuses.items() if status == "draft"}
        self.assertTrue(draft_ids, "expected at least one real draft pack to test against")
        stable_ids, experimental_ids = rc.parse_skill_routing(AKOS_HOME / "skills" / "akos" / "SKILL.md")
        for pid in draft_ids:
            self.assertNotIn(pid, stable_ids, f"draft pack {pid!r} must not be in the Stable routing catalog")
            self.assertIn(pid, experimental_ids, f"draft pack {pid!r} must be listed in the Experimental section")

    def test_knowledge_graph_may_reference_draft_without_becoming_routing(self):
        # graphs/knowledge-graph.md legitimately links several draft packs as
        # catalog cross-references — routing_check never scans graphs/ at
        # all, so this is satisfied by construction, not by an exception list.
        statuses = _real_pack_statuses()
        draft_ids = {pid for pid, status in statuses.items() if status == "draft"}
        graph_text = (AKOS_HOME / "graphs" / "knowledge-graph.md").read_text(encoding="utf-8")
        referenced = {pid for pid in draft_ids if pid in graph_text}
        self.assertTrue(referenced, "expected the knowledge graph to reference at least one draft pack")
        # The routing check result is unaffected by anything in graphs/.
        self.assertEqual(rc.check_stable_routing(AKOS_HOME), [])

    def test_explicit_user_opt_in_is_documented_as_the_only_draft_path(self):
        text = (AKOS_HOME / "skills" / "akos" / "SKILL.md").read_text(encoding="utf-8")
        experimental_idx = text.index("### Experimental packs")
        section = text[experimental_idx:experimental_idx + 800]
        self.assertIn("explicitly asks for it", section)
        self.assertIn("cannot self-authorize", section)
        self.assertIn("check-config", section)


class TestRoutingCheckSabotage(unittest.TestCase):
    """Builds a minimal synthetic AKOS_HOME so a deliberately-introduced
    violation can be asserted WITHOUT mutating the real repo."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        (self.home / "agents").mkdir()
        (self.home / "workflows").mkdir()
        (self.home / "skills" / "akos").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _write_pack(self, domain: str, name: str, status: str):
        d = self.home / "packs" / domain / name
        d.mkdir(parents=True)
        (d / "metadata.yaml").write_text(
            f"schema_version: 1\nname: {name}\ndomain: {domain}\nauthority-level: 3\n"
            f"version: 1.0.0\ntags: []\nsources: []\nrelated: []\nstatus: {status}\n",
            encoding="utf-8",
        )

    def _write_skill(self, stable_rows: str, experimental_rows: str):
        (self.home / "skills" / "akos" / "SKILL.md").write_text(
            "## 4. Route to packs\n\n"
            "| Pack | Reach for it when |\n|---|---|\n"
            f"{stable_rows}\n"
            "### Experimental packs (status: draft — read before routing here)\n\n"
            "| Pack | Reach for it when |\n|---|---|\n"
            f"{experimental_rows}\n"
            "## 5. Apply\n",
            encoding="utf-8",
        )

    def test_stable_agent_cannot_depend_on_draft_pack(self):
        self._write_pack("ux", "wcag", "stable")
        self._write_pack("ai-engineering", "agent-security", "draft")
        self._write_skill(
            "| `ux/wcag` | accessibility |\n",
            "| `ai-engineering/agent-security` | agent surface |\n",
        )
        (self.home / "agents" / "sneaky-reviewer.md").write_text(
            "---\nschema_version: 1\nname: akos-sneaky-reviewer\ndescription: x\ntools: Read\n---\n\n"
            "## Packs to load\n\n"
            "- [ai-engineering/agent-security](../packs/ai-engineering/agent-security/README.md)\n",
            encoding="utf-8",
        )
        errors = rc.check_stable_routing(self.home)
        self.assertTrue(any("sneaky-reviewer" in e and "agent-security" in e for e in errors), errors)

    def test_stable_workflow_cannot_depend_on_draft_pack(self):
        self._write_pack("ux", "wcag", "stable")
        self._write_pack("ai-engineering", "tool-design", "draft")
        self._write_skill(
            "| `ux/wcag` | accessibility |\n",
            "| `ai-engineering/tool-design` | tool design |\n",
        )
        (self.home / "workflows" / "sneaky-workflow.md").write_text(
            "---\nschema_version: 1\nid: sneaky-workflow\nstatus: stable\n"
            "packs: [ai-engineering/tool-design]\n---\n\n# Workflow: Sneaky\n",
            encoding="utf-8",
        )
        errors = rc.check_stable_routing(self.home)
        self.assertTrue(any("sneaky-workflow" in e and "tool-design" in e for e in errors), errors)

    def test_draft_pack_misfiled_into_stable_table_is_caught(self):
        self._write_pack("ai-engineering", "agent-evals", "draft")
        self._write_skill("| `ai-engineering/agent-evals` | sneaked into stable |\n", "")
        errors = rc.check_stable_routing(self.home)
        self.assertTrue(any("Stable routing catalog" in e for e in errors), errors)

    def test_stable_pack_missing_from_catalog_is_caught(self):
        self._write_pack("ux", "wcag", "stable")
        self._write_skill("", "")  # neither table lists it
        errors = rc.check_stable_routing(self.home)
        self.assertTrue(any("missing from the Stable routing catalog" in e for e in errors), errors)

    def test_clean_fixture_has_no_violations(self):
        self._write_pack("ux", "wcag", "stable")
        self._write_pack("ai-engineering", "agent-security", "draft")
        self._write_skill(
            "| `ux/wcag` | accessibility |\n",
            "| `ai-engineering/agent-security` | agent surface |\n",
        )
        self.assertEqual(rc.check_stable_routing(self.home), [])


class TestListPacksCLI(unittest.TestCase):
    """Exercises the real `bin/akos list-packs` CLI against the real repo
    (read-only — never mutates anything)."""

    def _run(self, *args):
        return subprocess.run(
            [str(AKOS_HOME / "bin" / "akos"), "list-packs", *args],
            capture_output=True, text=True,
        )

    def test_list_packs_default_hides_draft(self):
        draft_ids = {pid for pid, s in _real_pack_statuses().items() if s == "draft"}
        out = self._run().stdout
        for pid in draft_ids:
            self.assertNotIn(pid, out, f"default list-packs must not show draft pack {pid!r}")

    def test_draft_pack_is_visible_with_list_packs_all(self):
        draft_ids = {pid for pid, s in _real_pack_statuses().items() if s == "draft"}
        out = self._run("--all").stdout
        for pid in draft_ids:
            self.assertIn(pid, out, f"list-packs --all must show draft pack {pid!r}")

    def test_list_packs_status_filter_is_deterministic(self):
        first = self._run("--status", "draft").stdout
        second = self._run("--status", "draft").stdout
        self.assertEqual(first, second)
        self.assertNotEqual(first.strip(), "")


class TestCreatePackDraftWarning(unittest.TestCase):
    def test_create_pack_warns_that_draft_is_not_auto_routed(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            copy = tmp / "akos-copy"
            shutil.copytree(AKOS_HOME, copy, symlinks=True)
            proc = subprocess.run(
                [str(copy / "bin" / "akos"), "create-pack", "zz-test-domain/zz-test-pack"],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            combined = proc.stdout + proc.stderr
            self.assertIn("NOT be auto-routed", combined)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
