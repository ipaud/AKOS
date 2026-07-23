import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import validate as v  # noqa: E402


PACK_SCHEMA = v.load_schema("knowledge-pack")


class TestValidateInstance(unittest.TestCase):
    def test_minimal_valid_pack_has_no_errors(self):
        data = {
            "schema_version": 1,
            "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
            "tags": [], "sources": [{"title": "t", "url": "u"}], "related": [],
        }
        errors, warnings = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])
        # Recommended fields are absent -> warnings, not errors.
        self.assertTrue(warnings)

    def test_fully_populated_pack_has_no_warnings(self):
        data = {
            "schema_version": 1,
            "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
            "tags": [], "sources": [{"title": "t", "url": "u"}], "related": [],
            "id": "y/x", "status": "stable", "last_reviewed": "2026-01-01",
            "review_after": "2027-01-01", "maintainer": "core",
        }
        errors, warnings = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_required_field_is_an_error(self):
        data = {"domain": "y", "authority-level": 2, "version": "1.0.0", "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        fields = {e["field"] for e in errors}
        self.assertIn("name", fields)

    def test_bad_authority_level_type(self):
        data = {"name": "x", "domain": "y", "authority-level": "high", "version": "1.0.0",
                "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "authority-level" for e in errors))

    def _pack(self, **overrides):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": []}
        data.update(overrides)
        return data

    # The schema declared `minimum: 0, maximum: 4` on authority-level from the start,
    # but validate.py implemented neither keyword, so any out-of-range level validated
    # clean. Found by deliberately trying to break the validator rather than trusting
    # its green. These lock the bound in both directions, plus both boundaries.
    def test_authority_level_above_maximum_is_an_error(self):
        errors, _ = v.validate_instance(self._pack(**{"authority-level": 9}), PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "authority-level" and e["rule"] == "maximum" for e in errors))

    def test_authority_level_below_minimum_is_an_error(self):
        errors, _ = v.validate_instance(self._pack(**{"authority-level": -1}), PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "authority-level" and e["rule"] == "minimum" for e in errors))

    def test_authority_level_boundaries_are_valid(self):
        for level in (0, 4):
            errors, _ = v.validate_instance(self._pack(**{"authority-level": level}), PACK_SCHEMA)
            self.assertEqual([e for e in errors if e["field"] == "authority-level"], [],
                             f"authority-level {level} is in range and must validate clean")

    def test_bad_status_enum(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": [], "status": "not-a-status"}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "status" for e in errors))

    def test_bad_date_format(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": [], "last_reviewed": "2026-99-99"}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "last_reviewed" for e in errors))

    def test_bad_name_pattern(self):
        data = {"name": "Not Valid!", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "name" for e in errors))

    def test_sources_missing_url(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [{"title": "only title"}], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any("sources[0]" in e["field"] for e in errors))

    def test_source_with_org_instead_of_author_is_valid(self):
        # Real corpus fact: 3 packs use `org:` instead of `author:` in
        # sources — the schema deliberately doesn't require either.
        data = {"schema_version": 1, "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [{"title": "t", "org": "W3C", "url": "u"}], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])


class TestSchemaRegistry(unittest.TestCase):
    def test_schema_registry_resolves_v1(self):
        for kind, expected_path in (
            ("knowledge-pack", "v1/knowledge-pack.schema.json"),
            ("agent", "v1/agent.schema.json"),
            ("workflow", "v1/workflow.schema.json"),
        ):
            registry = json.loads(v.REGISTRY_PATH.read_text(encoding="utf-8"))
            self.assertEqual(registry["kinds"][kind]["schema_path"], expected_path)
            schema = v.load_schema(kind)
            self.assertEqual(schema["type"], "object")

    def test_legacy_schema_paths_do_not_drift(self):
        # The 3 schemas physically moved to schemas/v1/ (not aliased) — this
        # locks down that the OLD flat paths stay gone rather than silently
        # reappearing as a stale duplicate copy that could drift from v1/.
        for old_name in ("knowledge-pack.schema.json", "agent.schema.json", "workflow.schema.json"):
            self.assertFalse((paths.AKOS_HOME / "schemas" / old_name).exists(),
                              f"schemas/{old_name} should not exist — moved to schemas/v1/{old_name}")


def _valid_pack(**overrides) -> dict:
    data = {
        "schema_version": 1, "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
        "tags": [], "sources": [{"title": "t", "url": "u"}], "related": [],
    }
    data.update(overrides)
    return data


class TestSchemaStrictness(unittest.TestCase):
    def test_missing_schema_version_is_error(self):
        data = _valid_pack()
        del data["schema_version"]
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "schema_version" and e["rule"] == "required" for e in errors))

    def test_unknown_schema_version_is_error(self):
        errors, _ = v.validate_instance(_valid_pack(schema_version=99), PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "schema_version" and e["rule"] == "enum" for e in errors))

    def test_schema_version_wrong_type_is_error(self):
        errors, _ = v.validate_instance(_valid_pack(schema_version="1"), PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "schema_version" and e["rule"] == "type" for e in errors))

    def test_unknown_top_level_property_is_error(self):
        # The exact typo ("maintaner" for "maintainer") this whole hardening
        # pass is meant to catch — previously silently ignored.
        errors, _ = v.validate_instance(_valid_pack(maintaner="core"), PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "maintaner" and e["rule"] == "additionalProperties" for e in errors))

    def test_unknown_nested_source_property_is_error(self):
        data = _valid_pack(sources=[{"title": "t", "url": "u", "authro": "typo"}])
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["rule"] == "additionalProperties" and "sources[0]" in e["field"] for e in errors))

    def test_unknown_nested_profile_property_is_error(self):
        data = _valid_pack(profiles={"relevent": ["Production"]})  # typo: relevent
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["rule"] == "additionalProperties" and "profiles" in e["field"] for e in errors))


class TestPackSemantics(unittest.TestCase):
    def _meta_path(self, domain="ux", name="wcag") -> Path:
        return paths.AKOS_HOME / "packs" / domain / name / "metadata.yaml"

    def test_pack_path_metadata_mismatch_is_error(self):
        errors = v._check_pack_semantics({"domain": "wrong-domain", "name": "wcag"}, self._meta_path())
        self.assertTrue(any(e["field"] == "domain" for e in errors))

        errors = v._check_pack_semantics({"domain": "ux", "name": "wrong-name"}, self._meta_path())
        self.assertTrue(any(e["field"] == "name" for e in errors))

    def test_pack_id_mismatch_is_error(self):
        errors = v._check_pack_semantics({"id": "ux/wrong-id"}, self._meta_path())
        self.assertTrue(any(e["field"] == "id" for e in errors))

    def test_pack_id_matching_domain_name_is_valid(self):
        errors = v._check_pack_semantics({"domain": "ux", "name": "wcag", "id": "ux/wcag"}, self._meta_path())
        self.assertEqual(errors, [])

    def test_deprecated_pack_without_replacement_is_error(self):
        errors = v._check_pack_semantics({"deprecated": True}, self._meta_path())
        self.assertTrue(any(e["rule"] == "deprecated-requires-replacement" for e in errors))

    def test_deprecated_pack_with_replacement_is_valid(self):
        errors = v._check_pack_semantics({"deprecated": True, "replacement": "ux/other"}, self._meta_path())
        self.assertEqual(errors, [])


class TestValidateRealRepo(unittest.TestCase):
    def test_all_real_packs_validate_v1_strict(self):
        results = v.check_packs(PACK_SCHEMA)
        self.assertGreaterEqual(len(results), 40)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [], f"unexpected schema errors in real packs: {errors}")

    def test_all_real_agents_validate_v1_strict(self):
        schema = v.load_schema("agent")
        results = v.check_agents(schema)
        self.assertEqual(len(results), 13)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [])

    def test_all_real_workflows_have_frontmatter_and_validate_v1(self):
        # Inverts the pre-v1 contract: schema_version 1 requires frontmatter
        # to be present. All 9 real workflows were migrated to carry it
        # (id, description, agents, packs, profiles, status, maintainer).
        schema = v.load_schema("workflow")
        results = v.check_workflows(schema)
        self.assertEqual(len(results), 9)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [], f"unexpected schema errors in real workflows: {errors}")

    def test_workflow_without_frontmatter_is_error(self):
        tmp_workflow = paths.AKOS_HOME / "workflows" / "zz-test-no-frontmatter.md"
        tmp_workflow.write_text("# Workflow: Temp\n\nno frontmatter at all.\n", encoding="utf-8")
        try:
            schema = v.load_schema("workflow")
            results = v.check_workflows(schema)
            mine = next(r for r in results if r["file"].endswith("zz-test-no-frontmatter.md"))
            self.assertTrue(mine["errors"], "a workflow with no frontmatter at all must be a schema error now")
        finally:
            tmp_workflow.unlink()


if __name__ == "__main__":
    unittest.main()
