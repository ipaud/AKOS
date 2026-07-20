"""Cross-file wiring that nothing else checks.

Every defect locked here was found by an audit, not by a test, because the
pieces are individually valid: an agent file with no route parses fine, a
detector nobody invokes still passes its own unit tests, and a hardcoded
profile path is a working path. Only the relationship is wrong, and prose
relationships drift silently.
"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)
AGENTS = sorted((AKOS_HOME / "agents").glob("*.md"))
REVIEW_SKILL = (AKOS_HOME / "skills/akos-review/SKILL.md").read_text()
BUILD_SKILL = (AKOS_HOME / "skills/akos/SKILL.md").read_text()


class TestEveryAgentIsReachable(unittest.TestCase):
    """`backend-reviewer` carried profile weights in all six profiles and
    appeared in no lens table, no workflow and no prompt — a registered
    reviewer nothing could route to. It had shipped that way since 1.0.0."""

    def test_every_agent_is_named_in_the_review_skill(self):
        for agent in AGENTS:
            with self.subTest(agent=agent.name):
                self.assertIn(
                    agent.name, REVIEW_SKILL,
                    f"{agent.name} is not mentioned in skills/akos-review/SKILL.md — "
                    f"either route it (as a numbered lens or an explicitly "
                    f"routed-from one) or delete the agent")

    def test_every_agent_with_a_profile_weight_exists(self):
        profiles = (AKOS_HOME / "core/reasoning-profiles.md").read_text()
        names = {a.stem for a in AGENTS}
        for row in re.finditer(r"^\|\s*([a-z-]+-reviewer)\s*\|", profiles, re.MULTILINE):
            with self.subTest(agent=row.group(1)):
                self.assertIn(row.group(1), names,
                              "reasoning-profiles.md weights an agent that does not exist")


class TestDeterministicRulesAreWired(unittest.TestCase):
    """rules/ shipped seven working detectors that no agent or skill
    referenced. The security lens was told to hunt for committed secrets by
    hand while SECRET_IN_SOURCE sat unused — and, holding only
    Read/Grep/Glob, it could not have run it even if told to."""

    def test_the_review_skill_invokes_the_rules_runner(self):
        self.assertIn("akos rules run", REVIEW_SKILL,
                      "no step in the review skill runs the deterministic detectors")

    def test_each_project_scoped_rule_reaches_a_lens(self):
        # PACK_EXPIRED targets AKOS's own packs, not a reviewed project, and
        # is wired into doctor.sh instead.
        wired = REVIEW_SKILL + "".join(a.read_text() for a in AGENTS)
        for yaml_path in sorted((AKOS_HOME / "rules").glob("*/*.yaml")):
            rule_id = next(
                (line.split(":", 1)[1].strip()
                 for line in yaml_path.read_text().splitlines()
                 if line.startswith("id:")), None)
            if rule_id in (None, "PACK_EXPIRED"):
                continue
            with self.subTest(rule=rule_id):
                self.assertIn(
                    rule_id, wired,
                    f"{rule_id} is never named in the review skill or any agent, "
                    f"so nothing consumes it")

    def test_reviewer_agents_have_no_bash(self):
        """The reason the orchestrator must run the detectors. If an agent
        ever gains Bash this assumption changes and step 3 should be
        revisited — so fail loudly rather than let it drift."""
        for agent in AGENTS:
            with self.subTest(agent=agent.name):
                m = re.search(r"^tools:\s*(.+)$", agent.read_text(), re.MULTILINE)
                self.assertIsNotNone(m, f"{agent.name} has no tools: line")
                self.assertNotIn("Bash", m.group(1))


class TestPersonalProfileIsNotHardcoded(unittest.TestCase):
    """1.4.0 decoupled personal profiles across skills, core and templates
    but missed agents/, where five 'Packs to load' entries still named
    pau-avila. A project running `akos profile use alice` got Alice's layer
    nowhere and Pau's in five lenses."""

    # The defect is a hardcoded *path*, not any mention of the name. Naming
    # pau-avila as the documented default is correct and matches how both
    # skills word it. Citations of specific numbered principles also stay:
    # a second profile would not share this one's numbering, so genericizing
    # them would misrepresent what is being cited — recorded as a scope
    # decision when profiles were decoupled.
    HARDCODED_PATH = re.compile(r"packs/personal/pau-avila/")
    CITATION = re.compile(r"pau-avila principle \d+")

    def test_no_agent_loads_a_hardcoded_personal_profile(self):
        for agent in AGENTS:
            with self.subTest(agent=agent.name):
                for i, line in enumerate(agent.read_text().splitlines(), 1):
                    if not self.HARDCODED_PATH.search(line) or self.CITATION.search(line):
                        continue
                    self.fail(
                        f"{agent.name}:{i} loads a hardcoded profile path outside a "
                        f"principle citation — use packs/personal/<personal_profile>/"
                        f"\n  {line.strip()}")

    def test_both_skills_use_the_generic_form(self):
        for name, text in (("akos", BUILD_SKILL), ("akos-review", REVIEW_SKILL)):
            with self.subTest(skill=name):
                self.assertIn("<personal_profile>", text)


if __name__ == "__main__":
    unittest.main()
