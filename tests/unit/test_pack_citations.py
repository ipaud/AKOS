"""Rule codes cited inside a pack must exist in that pack.

A pack citing `MD14` when only MD1-MD12 exist is silently wrong: nothing
parses it, no link breaks, and a reader following the citation finds nothing.
Found by checking rather than by reading — one instance across 54 packs, in
`ux/material-design`, where the intended principle was MD12.

Low yield today. Kept because the cost is one test and packs keep being
added: the next miscitation is written by someone who cannot see this one.
"""

import re
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)

# `- **MD12 — ...` or `- MD12. ...` — how principles and engineering rules
# declare a code at the start of their bullet.
DEFINITION_RE = re.compile(r"^[-#\s]*\**([A-Z]{2,4}\d+)\b", re.MULTILINE)
CITATION_RE = re.compile(r"\b([A-Z]{2,4})(\d+)\b")


def codes_defined_by(pack: Path) -> set[str]:
    defined: set[str] = set()
    for name in ("principles.md", "engineering-rules.md"):
        f = pack / name
        if f.is_file():
            defined |= set(DEFINITION_RE.findall(f.read_text(encoding="utf-8")))
    return defined


class TestPackCitationsResolve(unittest.TestCase):
    def test_every_cited_code_exists_in_its_pack(self):
        for pack in sorted(AKOS_HOME.joinpath("packs").glob("*/*/")):
            defined = codes_defined_by(pack)
            if not defined:
                continue
            # Only check prefixes this pack actually owns; a pack may cite
            # another pack's codes, and those live elsewhere by design.
            prefixes = {re.match(r"([A-Z]+)", c).group(1) for c in defined}
            for f in sorted(pack.glob("*.md")):
                text = f.read_text(encoding="utf-8")
                for m in CITATION_RE.finditer(text):
                    if m.group(1) not in prefixes or m.group(0) in defined:
                        continue
                    with self.subTest(pack=pack.name, file=f.name, code=m.group(0)):
                        self.fail(
                            f"{pack.parent.name}/{pack.name}/{f.name} cites {m.group(0)}, "
                            f"which this pack never defines")

    def test_the_checker_finds_something_to_check(self):
        """Guards the guard: if the definition pattern stops matching, the
        test above passes by covering nothing."""
        total = sum(len(codes_defined_by(p)) for p in AKOS_HOME.joinpath("packs").glob("*/*/"))
        self.assertGreater(total, 500, "expected hundreds of declared rule codes across the corpus")


if __name__ == "__main__":
    unittest.main()
