#!/usr/bin/env python3
"""Canonical pack metadata.yaml discovery and parsing.

CLI listing, freshness, routing-check, and validate each open-coded the same
"glob every non-personal pack's metadata.yaml, try to parse it" pair with
slightly different try/except shapes. One implementation here; callers keep
their own decision about how to react to a parse failure (validate surfaces
it as a finding, everything else falls back to an empty dict).
"""

from __future__ import annotations

from pathlib import Path

import yaml_subset


def discover_pack_metadata_paths(packs_dir: Path) -> list[Path]:
    """Every metadata.yaml under packs_dir, excluding the personal layer."""
    return [
        p for p in sorted(packs_dir.glob("*/*/metadata.yaml"))
        if "personal" not in p.parts
    ]


def load_pack_metadata(meta_path: Path) -> tuple[dict | None, str | None]:
    """Parse one metadata.yaml. Returns (data, None) or (None, error message)."""
    try:
        return yaml_subset.load(meta_path), None
    except yaml_subset.YamlSubsetError as e:
        return None, str(e)
