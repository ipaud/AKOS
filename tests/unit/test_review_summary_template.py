"""The Review Summary section set must be identical across its four copies.

The template is embedded verbatim in four places — the pipeline doc, the review
skill, the canonical agent, and the paste-prompt — with no include mechanism
(every consumer is an LLM reading one file in isolation, so the duplication is
load-bearing). It had already drifted: `## Coverage` was added to three copies
and not the fourth, so a reviewer on the prompt path produced a report missing
a whole section. This asserts the section HEADER set matches, which is the
invariant that matters — the prompt legitimately condenses the bodies (e.g. a
one-line Scores), so byte-identity is the wrong check; a dropped section is not.
"""

import re
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent

COPIES = [
    "core/review-pipeline.md",
    "skills/akos-review/SKILL.md",
    "agents/ux-reviewer.md",
    "prompts/run-full-review.md",
]

EXPECTED_SECTIONS = [
    "Context", "Strengths", "Critical Issues", "High Priority Fixes",
    "Medium Priority Fixes", "Low Priority Improvements", "Tradeoffs",
    "Relevant Knowledge Packs Used", "Coverage", "Scores",
    "Recommended Next Iteration", "Final Decision",
]

EXPECTED_SCORES = [
    "UX", "Accessibility", "Mobile", "Architecture", "Security",
    "Performance", "Product", "Maintainability", "Overall",
]


def sections_in_review_block(path: Path) -> list[str]:
    """Section headers inside the first fenced block that starts with the
    '# Review Summary' line."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    # Find the fenced block containing the Review Summary skeleton.
    for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.DOTALL):
        if "# Review Summary" in block:
            out = []
            for line in block.splitlines():
                m = re.match(r"^## (.+?)\s*$", line)
                if m:
                    # Normalise the prompt's condensed "Scores (…)" / "Final
                    # Decision — …" to the bare header.
                    name = m.group(1).split("(")[0].split("—")[0].strip()
                    out.append(name)
            return out
    return []


def scores_in_review_block(path: Path) -> list[str]:
    """Dimension labels inside the Review Summary's Scores section."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    for block in re.findall(r"```[a-z]*\n(.*?)```", text, re.DOTALL):
        if "# Review Summary" not in block:
            continue
        condensed = re.search(r"^## Scores \(([^)]+)\)", block, re.MULTILINE)
        if condensed:
            return [part.strip() for part in condensed.group(1).split("/")]
        scores = re.search(r"^## Scores\s*$(.*?)(?=^## |\Z)",
                           block, re.MULTILINE | re.DOTALL)
        if not scores:
            return []
        return [
            match.group(1).strip()
            for match in re.finditer(r"^-\s+([^:]+):", scores.group(1), re.MULTILINE)
        ]
    return []


class TestReviewSummaryTemplate(unittest.TestCase):
    def test_each_copy_has_exactly_the_canonical_sections_in_order(self):
        for rel in COPIES:
            with self.subTest(copy=rel):
                got = sections_in_review_block(AKOS_HOME / rel)
                self.assertEqual(
                    got, EXPECTED_SECTIONS,
                    f"{rel} Review Summary sections drifted from the canonical set")

    def test_all_four_copies_agree(self):
        section_sets = {rel: sections_in_review_block(AKOS_HOME / rel) for rel in COPIES}
        first = section_sets[COPIES[0]]
        for rel, got in section_sets.items():
            self.assertEqual(got, first, f"{rel} disagrees with {COPIES[0]}")

    def test_each_copy_has_the_canonical_score_dimensions(self):
        for rel in COPIES:
            with self.subTest(copy=rel):
                self.assertEqual(
                    scores_in_review_block(AKOS_HOME / rel),
                    EXPECTED_SCORES,
                    f"{rel} Scores dimensions drifted from the canonical set")


if __name__ == "__main__":
    unittest.main()
