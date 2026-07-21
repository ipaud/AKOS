"""Every structured metadata source must appear in the pack's reading list.

`metadata.yaml`'s `sources[]` is the machine-readable primary-source list;
`references.md` is the human-readable full citation list. They are two
source-of-truth lists for the same fact, so they drift — an audit found a
handful where a `sources[]` title named a citation that did not appear in
`references.md` at all (a renamed or invented title). A structured source not
grounded in the reading list is exactly the fabrication risk this guards.

The check: each `sources[].title` must appear verbatim as a `- **title**`
bullet in `references.md`. `references.md` may list MORE (related reading is
fine); `sources[]` may not name something absent from it. Exact-match by
design — authors control both files, and forcing them to agree is the point.
"""

import re
import sys
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
import yaml_subset  # noqa: E402

BOLD_BULLET_RE = re.compile(r"^\s*-\s+\*\*(.+?)\*\*", re.MULTILINE)


def pack_metadata_files():
    # Personal packs have no metadata.yaml; domain packs do.
    return sorted(AKOS_HOME.glob("packs/*/*/metadata.yaml"))


def reference_titles(references_path: Path) -> set:
    if not references_path.exists():
        return set()
    text = references_path.read_text(encoding="utf-8", errors="ignore")
    return {m.group(1).strip() for m in BOLD_BULLET_RE.finditer(text)}


class TestSourcesReferencesIntegrity(unittest.TestCase):
    def test_the_scan_actually_finds_packs(self):
        self.assertGreater(len(pack_metadata_files()), 40)

    def test_every_metadata_source_appears_in_references(self):
        offenders = []
        for meta in pack_metadata_files():
            pack = f"{meta.parent.parent.name}/{meta.parent.name}"
            data = yaml_subset.load(meta)
            titles = [s.get("title", "").strip() for s in (data.get("sources") or [])
                      if isinstance(s, dict)]
            ref_titles = reference_titles(meta.parent / "references.md")
            for t in titles:
                if t and t not in ref_titles:
                    offenders.append(f"{pack}: sources title {t!r} not a bullet in references.md")
        self.assertEqual(
            offenders, [],
            "metadata sources[] not grounded in references.md:\n" + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
