import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import yaml_subset as y  # noqa: E402


class TestYamlSubsetRealCorpus(unittest.TestCase):
    """Every metadata.yaml in the real repo must parse and carry the 7
    universal fields — this is the exact check that caught the 4 packs
    using a multi-line tags: [...] format during M2."""

    def test_all_pack_metadata_parses(self):
        files = sorted((paths.AKOS_HOME / "packs").glob("*/*/metadata.yaml"))
        self.assertGreaterEqual(len(files), 40, "expected the real pack corpus, not an empty glob")
        for f in files:
            with self.subTest(pack=f):
                data = y.load(f)
                self.assertIsInstance(data, dict)
                for req in ("name", "domain", "authority-level", "version", "tags", "sources", "related"):
                    self.assertIn(req, data, f"{f} missing required field {req}")
                self.assertIsInstance(data["authority-level"], int)
                self.assertIsInstance(data["tags"], list)
                self.assertIsInstance(data["sources"], list)
                for src in data["sources"]:
                    self.assertIn("title", src)
                    self.assertIn("url", src)

    def test_personal_layer_has_no_metadata_yaml(self):
        self.assertFalse((paths.AKOS_HOME / "packs/personal/pau-avila/metadata.yaml").exists())


class TestYamlSubsetScalars(unittest.TestCase):
    def test_int_scalar(self):
        self.assertEqual(y.loads("x: 2\n"), {"x": 2})

    def test_bool_scalars(self):
        self.assertEqual(y.loads("a: true\nb: false\n"), {"a": True, "b": False})

    def test_null_scalars(self):
        for null_repr in ("null", "~"):
            self.assertIsNone(y.loads(f"x: {null_repr}\n")["x"])

    def test_version_string_not_coerced_to_float(self):
        # 1.0.0 must stay a string — this was a deliberate design decision,
        # not an accident, to avoid silent type surprises with dates/versions.
        self.assertEqual(y.loads("version: 1.0.0\n")["version"], "1.0.0")

    def test_quoted_string_with_internal_colon_space(self):
        data = y.loads('title: "Refactoring UI: Practical Steps"\n')
        self.assertEqual(data["title"], "Refactoring UI: Practical Steps")

    def test_url_with_double_slash_is_not_split_as_key_value(self):
        data = y.loads("url: https://example.com\n")
        self.assertEqual(data["url"], "https://example.com")

    def test_spaced_key_e_g_profile_name(self):
        data = y.loads("Game Dev: HIGH\n")
        self.assertEqual(data, {"Game Dev": "HIGH"})


class TestYamlSubsetFlowLists(unittest.TestCase):
    def test_inline_flow_list(self):
        self.assertEqual(y.loads("tags: [a, b, c]\n")["tags"], ["a", "b", "c"])

    def test_empty_flow_list(self):
        self.assertEqual(y.loads("tags: []\n")["tags"], [])

    def test_quoted_items_in_flow_list(self):
        data = y.loads('tags: ["a, b", c]\n')
        self.assertEqual(data["tags"], ["a, b", "c"])


class TestYamlSubsetNesting(unittest.TestCase):
    def test_list_of_maps(self):
        data = y.loads(
            "sources:\n"
            '  - title: "A"\n'
            "    url: http://a\n"
            '  - title: "B"\n'
            "    url: http://b\n"
        )
        self.assertEqual(data["sources"], [{"title": "A", "url": "http://a"}, {"title": "B", "url": "http://b"}])

    def test_two_level_nested_map(self):
        # The rule-registry shape: severity: {default: X, profiles: {A: Y}}
        data = y.loads(
            "severity:\n"
            "  default: CRITICAL\n"
            "  profiles:\n"
            "    Prototype: HIGH\n"
            "    Game Dev: HIGH\n"
        )
        self.assertEqual(data["severity"]["default"], "CRITICAL")
        self.assertEqual(data["severity"]["profiles"]["Game Dev"], "HIGH")

    def test_plain_scalar_list(self):
        data = y.loads("related:\n  - packs/ux/wcag\n  - packs/ux/steve-krug\n")
        self.assertEqual(data["related"], ["packs/ux/wcag", "packs/ux/steve-krug"])


class TestYamlSubsetRejections(unittest.TestCase):
    def test_block_scalar_rejected(self):
        with self.assertRaises(y.YamlSubsetError):
            y.loads("x: |\n  multi\n  line\n")

    def test_flow_mapping_rejected(self):
        with self.assertRaises(y.YamlSubsetError):
            y.loads("x: {a: b}\n")

    def test_anchor_rejected(self):
        with self.assertRaises(y.YamlSubsetError):
            y.loads("x: &anchor value\n")

    def test_tab_indentation_rejected(self):
        with self.assertRaises(y.YamlSubsetError):
            y.loads("x:\n\tkey: value\n")


if __name__ == "__main__":
    unittest.main()
