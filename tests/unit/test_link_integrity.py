"""Every relative markdown link across the prose surfaces must resolve.

Adding a pack trips four guards (17-file contract, routing-table membership,
schema validation, citation resolution). Renaming or deleting one tripped
NONE of them for inbound references: a pack's `related:` targets, an agent's
"Packs to load" list, a graph edge, a scoring "Inputs" block. This is that
guard — it walks every `[text](relative)` link and asserts the target exists,
so a rename that orphans a reference goes red instead of shipping a dead link.
"""

import re
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SEARCH_DIRS = ["core", "agents", "scoring", "graphs", "workflows", "packs",
               "docs", "prompts", "skills", "templates"]


def iter_links():
    for d in SEARCH_DIRS:
        for md in sorted((AKOS_HOME / d).rglob("*.md")):
            text = md.read_text(encoding="utf-8", errors="ignore")
            for m in LINK_RE.finditer(text):
                target = m.group(1).strip()
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                path_part = target.split("#", 1)[0].strip()
                if not path_part:
                    continue
                yield md, target, (md.parent / path_part).resolve()


class TestLinkIntegrity(unittest.TestCase):
    def test_the_scan_actually_finds_links(self):
        # Guard the guard: an empty walk would make every assertion vacuous.
        self.assertGreater(sum(1 for _ in iter_links()), 500)

    def test_all_relative_links_resolve(self):
        broken = [f"{md.relative_to(AKOS_HOME)} -> {target}"
                  for md, target, resolved in iter_links() if not resolved.exists()]
        self.assertEqual(broken, [], f"{len(broken)} broken relative link(s):\n" + "\n".join(broken))


if __name__ == "__main__":
    unittest.main()
