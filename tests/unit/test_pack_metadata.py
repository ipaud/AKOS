import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import pack_metadata  # noqa: E402


class TestDiscoverPackMetadataPaths(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.packs_dir = Path(self.tmp.name)

    def _write_pack(self, domain, name, text="schema_version: 1\n"):
        d = self.packs_dir / domain / name
        d.mkdir(parents=True)
        (d / "metadata.yaml").write_text(text)

    def test_finds_every_pack_metadata_file(self):
        self._write_pack("ux", "steve-krug")
        self._write_pack("security", "owasp-top-10")
        found = pack_metadata.discover_pack_metadata_paths(self.packs_dir)
        self.assertEqual(
            sorted(p.parent.name for p in found),
            ["owasp-top-10", "steve-krug"],
        )

    def test_excludes_the_personal_layer(self):
        self._write_pack("personal", "pau-avila")
        self._write_pack("ux", "steve-krug")
        found = pack_metadata.discover_pack_metadata_paths(self.packs_dir)
        self.assertEqual([p.parent.name for p in found], ["steve-krug"])

    def test_results_are_sorted(self):
        self._write_pack("ux", "zeta")
        self._write_pack("ux", "alpha")
        found = pack_metadata.discover_pack_metadata_paths(self.packs_dir)
        self.assertEqual([p.parent.name for p in found], ["alpha", "zeta"])

    def test_empty_directory_returns_no_paths(self):
        self.assertEqual(pack_metadata.discover_pack_metadata_paths(self.packs_dir), [])


class TestLoadPackMetadata(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.meta_path = Path(self.tmp.name) / "metadata.yaml"

    def test_valid_yaml_returns_data_and_no_error(self):
        self.meta_path.write_text("schema_version: 1\nstatus: draft\n")
        data, err = pack_metadata.load_pack_metadata(self.meta_path)
        self.assertIsNone(err)
        self.assertEqual(data["status"], "draft")

    def test_malformed_yaml_returns_none_and_an_error_message(self):
        self.meta_path.write_text("key: value\n  bad-indent: [unterminated\n")
        data, err = pack_metadata.load_pack_metadata(self.meta_path)
        self.assertIsNone(data)
        self.assertIsInstance(err, str)
        self.assertTrue(err)


if __name__ == "__main__":
    unittest.main()
