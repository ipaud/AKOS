"""Rule-code prefixes should be owned by one pack, so a citation resolves.

A code like `AP1` is ambiguous when two packs each define their own `AP`
series — an agent emitting "AP1" can't be resolved to a single pack.
`test_pack_citations.py` only checks that a cited prefix is defined *within*
its owning pack, so a cross-pack collision passes it.

Fully renamespacing the existing collisions is a context-sensitive content
change (an external `CE1` reference must be read to know which pack it meant),
tracked separately. This test's job is to STOP THE BLEEDING: it freezes the
known collisions in a baseline and fails if a *new* one appears — a fifth pack
reusing a prefix, or a new pack colliding with an existing owner.

"Owns a prefix" = defines at least two codes with it in engineering-rules.md.
"""

import collections
import re
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent
CODE_RE = re.compile(r"\b([A-Z]{2,4}(?:-E)?)(\d+)\b")
OWNERSHIP_MIN_DEFINITIONS = 2

# Known, pre-existing collisions — tracked debt, to be resolved by a
# context-aware renamespace pass, NOT grown. Each entry is a prefix mapped to
# the set of packs that independently define a series under it. Adding a pack
# to any of these sets, or introducing a new colliding prefix, must fail this
# test rather than silently join the ambiguity.
KNOWN_COLLISIONS = {
    "AP": {"security/owasp-api-top-10", "ux/apple-hig"},
    "BE": {"performance/browser-rendering", "product/escaping-the-build-trap"},
    "CE": {"frontend/css", "product/continuous-discovery-habits"},
    "DP-E": {"architecture/design-patterns", "devops/deployment"},
    "OW": {"ai-engineering/agent-security", "security/owasp-top-10"},
    "ER": {"ux/don-norman", "ux/laws-of-ux", "ux/nielsen-norman-group", "ux/steve-krug"},
    "NR": {"ux/don-norman", "ux/laws-of-ux", "ux/nielsen-norman-group"},
    "NG": {"ux/laws-of-ux", "ux/nielsen-norman-group", "ux/universal-principles-of-design"},
    "WC": {"ux/refactoring-ui", "ux/wcag"},
}


def prefix_owners() -> dict:
    owners = collections.defaultdict(set)
    for md in AKOS_HOME.glob("packs/*/*/engineering-rules.md"):
        pack = f"{md.parent.parent.name}/{md.parent.name}"
        counts = collections.Counter(
            m.group(1) for m in CODE_RE.finditer(md.read_text(encoding="utf-8", errors="ignore")))
        for prefix, n in counts.items():
            if n >= OWNERSHIP_MIN_DEFINITIONS:
                owners[prefix].add(pack)
    return {p: v for p, v in owners.items() if len(v) > 1}


class TestPackPrefixUniqueness(unittest.TestCase):
    def test_no_new_prefix_collisions_beyond_the_known_baseline(self):
        current = prefix_owners()
        new = {p: sorted(packs) for p, packs in current.items()
               if p not in KNOWN_COLLISIONS or packs != KNOWN_COLLISIONS[p]}
        self.assertEqual(
            new, {},
            "New or grown rule-code prefix collision(s). A prefix must be owned by one pack "
            "so a citation resolves. Pick a distinct prefix, or if resolving known debt, update "
            "KNOWN_COLLISIONS:\n" + "\n".join(f"  {p}: {packs}" for p, packs in new.items()))

    def test_a_baseline_collision_that_gets_fixed_must_be_removed_from_the_baseline(self):
        # Guard against the baseline going stale in the lenient direction: if a
        # known collision is resolved, its KNOWN_COLLISIONS entry should be
        # deleted, not left to grandfather a prefix that is now clean.
        current = prefix_owners()
        stale = [p for p in KNOWN_COLLISIONS if p not in current]
        self.assertEqual(
            stale, [],
            f"These prefixes are no longer colliding — remove them from KNOWN_COLLISIONS: {stale}")


if __name__ == "__main__":
    unittest.main()
