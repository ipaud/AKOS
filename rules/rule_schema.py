"""Strict, versioned contract for ``rules/<domain>/<RULE_ID>.yaml`` registries.

The project intentionally uses a small YAML subset and the Python standard
library only. Keeping this validator beside the runner makes registry
validation available both during discovery and to authoring tests without
adding a JSON-Schema runtime dependency.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


RULE_SCHEMA_VERSION = 1
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
CONFIDENCE_LEVELS = {"Certain", "High", "Moderate", "Low"}
RULE_LEVELS = {"A", "B", "C"}
RULE_STATUSES = {"stable", "draft", "deprecated"}
RULE_TARGETS = {"project-source", "akos-packs"}
PROFILE_NAMES = {
    "Prototype",
    "Startup MVP",
    "Production",
    "Enterprise",
    "Game Dev",
    "Internal Tool",
}

REQUIRED_FIELDS = {
    "id",
    "title",
    "domain",
    "level",
    "severity",
    "confidence",
    "related_packs",
    "detector",
    "applies_to",
    "recommendation",
    "references",
    "version",
    "status",
}
OPTIONAL_FIELDS = {"suppressible"}
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS

_RULE_ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
_DOMAIN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class RuleContractError(ValueError):
    """A registry cannot be trusted by the rule engine."""


def _is_string_list(value) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def validate_rule_registry(data, *, source: Path | None = None) -> list[str]:
    """Return every contract violation in a parsed v1 rule registry."""
    errors: list[str] = []
    label = str(source) if source else "rule registry"

    if not isinstance(data, dict):
        return [f"{label}: root must be an object"]

    missing = sorted(REQUIRED_FIELDS - set(data))
    errors.extend(f"missing required field {field!r}" for field in missing)
    unknown = sorted(set(data) - ALLOWED_FIELDS)
    errors.extend(f"unknown field {field!r}" for field in unknown)

    rule_id = data.get("id")
    if not isinstance(rule_id, str) or not _RULE_ID_RE.fullmatch(rule_id):
        errors.append("'id' must match ^[A-Z][A-Z0-9_]*$")

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("'title' must be a non-empty string")

    domain = data.get("domain")
    if not isinstance(domain, str) or not _DOMAIN_RE.fullmatch(domain):
        errors.append("'domain' must be a lowercase kebab-case segment")

    if data.get("level") not in RULE_LEVELS:
        errors.append(f"'level' must be one of {sorted(RULE_LEVELS)}")
    if data.get("confidence") not in CONFIDENCE_LEVELS:
        errors.append(f"'confidence' must be one of {sorted(CONFIDENCE_LEVELS)}")
    if data.get("status") not in RULE_STATUSES:
        errors.append(f"'status' must be one of {sorted(RULE_STATUSES)}")
    if data.get("version") != RULE_SCHEMA_VERSION:
        errors.append(f"'version' must be integer {RULE_SCHEMA_VERSION}")

    severity = data.get("severity")
    if not isinstance(severity, dict):
        errors.append("'severity' must be an object")
    else:
        severity_unknown = sorted(set(severity) - {"default", "profiles"})
        errors.extend(f"unknown severity field {field!r}" for field in severity_unknown)
        if severity.get("default") not in SEVERITIES:
            errors.append(f"'severity.default' must be one of {sorted(SEVERITIES)}")
        profiles = severity.get("profiles", {})
        if not isinstance(profiles, dict):
            errors.append("'severity.profiles' must be an object")
        else:
            for profile, value in profiles.items():
                if profile not in PROFILE_NAMES:
                    errors.append(f"unknown severity profile {profile!r}")
                if value not in SEVERITIES:
                    errors.append(
                        f"severity for profile {profile!r} must be one of {sorted(SEVERITIES)}"
                    )

    applies_to = data.get("applies_to")
    if not isinstance(applies_to, dict):
        errors.append("'applies_to' must be an object")
    else:
        applies_unknown = sorted(set(applies_to) - {"glob", "target"})
        errors.extend(f"unknown applies_to field {field!r}" for field in applies_unknown)
        globs = applies_to.get("glob")
        if not _is_string_list(globs) or not globs:
            errors.append("'applies_to.glob' must be a non-empty string list")
        if applies_to.get("target") not in RULE_TARGETS:
            errors.append(f"'applies_to.target' must be one of {sorted(RULE_TARGETS)}")

    detector = data.get("detector")
    if (
        not isinstance(detector, str)
        or not detector.startswith("rules/")
        or not detector.endswith(".py")
        or ".." in Path(detector).parts
        or Path(detector).is_absolute()
    ):
        errors.append("'detector' must be a relative rules/**/*.py path with no traversal")

    if not _is_string_list(data.get("related_packs")):
        errors.append("'related_packs' must be a string list")
    if not _is_string_list(data.get("references")):
        errors.append("'references' must be a string list")
    recommendation = data.get("recommendation")
    if not isinstance(recommendation, str) or not recommendation.strip():
        errors.append("'recommendation' must be a non-empty string")
    if "suppressible" in data and not isinstance(data["suppressible"], bool):
        errors.append("'suppressible' must be boolean when present")

    return errors


def validate_rule_file(path: Path, akos_home: Path) -> list[str]:
    """Parse and validate one registry file for tests and authoring tools."""
    schemas_dir = akos_home / "schemas"
    if str(schemas_dir) not in sys.path:
        sys.path.insert(0, str(schemas_dir))
    import yaml_subset

    try:
        data = yaml_subset.load(path)
    except (OSError, yaml_subset.YamlSubsetError) as exc:
        return [f"could not parse registry: {exc}"]
    return validate_rule_registry(data, source=path)


def require_valid_rule_registry(data, *, source: Path | None = None) -> None:
    """Raise a single discovery error containing every contract violation."""
    errors = validate_rule_registry(data, source=source)
    if errors:
        raise RuleContractError("; ".join(errors))
