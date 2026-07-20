"""Shared test helper — resolves AKOS_HOME and puts every source directory
on sys.path, exactly once, however a test file is invoked (unittest
discovery, direct `python3 tests/unit/test_x.py`, or from a different cwd).
"""

from __future__ import annotations

import sys
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent.parent

for sub in ("schemas", "rules", "benchmarks"):
    p = str(AKOS_HOME / sub)
    if p not in sys.path:
        sys.path.insert(0, p)
