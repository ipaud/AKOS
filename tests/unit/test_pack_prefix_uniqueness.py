"""Every rule-code prefix must be DEFINED by exactly one pack, so a citation
resolves.

A code like `AP1` is ambiguous if two packs each define their own `AP` series.
An audit found 9 prefixes flagged by a naive count, which split into two kinds:

- Genuine dual-definition (AP, BE, CE, DP-E) — two packs each defined a series.
  Resolved by renamespacing the pack with no external citations: apple-hig
  AP→AHE, escaping-the-build-trap BE→BTE, css CE→CSE, continuous-discovery
  CE→CDE, deployment DP/DP-E→DPL/DPL-E.
- Citation artifacts (OW, ER, NR, NG, WC) — one pack defines the series, others
  merely CITE it ("see Krug ER8", "extends OW1"). A count that treats citations
  as definitions false-positives here. Renaming would have been wrong.

The fix for the second kind is this test counting DEFINITIONS only. A definition
is a code at the start of a list item (`- OW1.`, `- **DP1 —**`); a citation is
the same code mid-sentence. With that distinction, every prefix now has exactly
one defining pack, so the baseline is empty — any collision is a real bug.
"""

import collections
import re
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent

# A DEFINITION: the code is the first token of a markdown list item, optionally
# bold, optionally starred — `- OW1.`, `- OW1 ★.`, `- **DP1 —**`, `## NG5`.
# NOT a citation like "see Krug ER8" or "(extends OW1)", where the code sits
# mid-line preceded by other words.
DEFINITION_RE = re.compile(r"^\s*(?:#+\s+|-\s+)\*{0,2}([A-Z]{2,4}(?:-E)?)(\d+)\b", re.MULTILINE)
OWNERSHIP_MIN_DEFINITIONS = 2

# Empty by construction: the 4 genuine collisions were renamed and the 5
# citation artifacts disappear under definition-aware counting. A non-empty
# result is a real regression — a new prefix defined by two packs.
KNOWN_COLLISIONS: dict = {}


def prefix_owners() -> dict:
    owners = collections.defaultdict(set)
    for md in AKOS_HOME.glob("packs/*/*/engineering-rules.md"):
        pack = f"{md.parent.parent.name}/{md.parent.name}"
        counts = collections.Counter(
            m.group(1) for m in DEFINITION_RE.finditer(md.read_text(encoding="utf-8", errors="ignore")))
        for prefix, n in counts.items():
            if n >= OWNERSHIP_MIN_DEFINITIONS:
                owners[prefix].add(pack)
    return {p: v for p, v in owners.items() if len(v) > 1}


class TestPackPrefixUniqueness(unittest.TestCase):
    def test_the_scan_finds_definitions(self):
        # Guard the guard: a broken DEFINITION_RE would make the collision
        # check vacuous. There must be many single-owner prefixes.
        owners = collections.defaultdict(set)
        for md in AKOS_HOME.glob("packs/*/*/engineering-rules.md"):
            pack = f"{md.parent.parent.name}/{md.parent.name}"
            for m in DEFINITION_RE.finditer(md.read_text(encoding="utf-8", errors="ignore")):
                owners[m.group(1)].add(pack)
        self.assertGreater(len(owners), 20, "definition regex found almost nothing — it is probably broken")

    def test_every_prefix_is_defined_by_exactly_one_pack(self):
        current = prefix_owners()
        collisions = {p: sorted(packs) for p, packs in current.items()
                      if KNOWN_COLLISIONS.get(p) != packs}
        self.assertEqual(
            collisions, {},
            "Rule-code prefix defined by more than one pack — a citation to it can't resolve. "
            "Rename one pack's series to a distinct prefix:\n"
            + "\n".join(f"  {p}: {packs}" for p, packs in collisions.items()))


if __name__ == "__main__":
    unittest.main()
