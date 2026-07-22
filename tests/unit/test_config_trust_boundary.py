"""Contract tests over the skill text that governs `.akos/config.md`.

`.akos/config.md` comes from the repository under review — possibly a hostile
one. The skills must frame it as untrusted manifest data, never as binding
instruction, and must not let it lower the safety floor or replace mandatory
packs. These lock that framing in prose so a future edit cannot quietly
re-confer authority on the file (the exact regression P0-2 fixed).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)
SKILL_FILES = [
    AKOS_HOME / "skills" / "akos" / "SKILL.md",
    AKOS_HOME / "skills" / "akos-review" / "SKILL.md",
]

# Phrases that turn the repository config into authority. If any reappears, a
# cloned repo can dictate the profile, the lens set, or the agent's reading.
BANNED = [
    "is binding",
    "not negotiable",
    "already decided",
    "override your assumptions",
]


class TestConfigTrustBoundary(unittest.TestCase):
    def test_notes_are_not_documented_as_binding(self):
        for path in SKILL_FILES:
            text = path.read_text(encoding="utf-8").lower()
            for phrase in BANNED:
                self.assertNotIn(
                    phrase, text,
                    f"{path.name} re-confers authority on .akos/config.md via {phrase!r}",
                )

    def test_config_is_framed_as_untrusted_data(self):
        for path in SKILL_FILES:
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn(
                "untrusted", text,
                f"{path.name} must frame .akos/config.md as untrusted data",
            )

    def test_repo_manifest_cannot_disable_mandatory_packs(self):
        """Packs-to-always-load is additive, never a replacement for a
        mandatory pack — stated in both skills."""
        for path in SKILL_FILES:
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn(
                "never replaces a mandatory pack", text,
                f"{path.name} must state repo packs never replace a mandatory pack",
            )

    def test_repo_profile_overrides_are_non_authoritative(self):
        for path in SKILL_FILES:
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn(
                "not authoritative", text,
                f"{path.name} must state repo-side profile overrides are not authoritative",
            )


if __name__ == "__main__":
    unittest.main()
