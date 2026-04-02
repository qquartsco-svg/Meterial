"""Ensure local package roots are importable in the chemistry hub copy."""

from __future__ import annotations

import sys
from pathlib import Path

_here = Path(__file__).resolve()
_project_root = _here.parents[1]

for _path in (
    _project_root,
    _project_root.parent.parent / "2_operational" / "60_APPLIED_LAYER" / "Battery_Dynamics_Engine",
    _project_root.parents[3] / "_staging" / "Battery_Dynamics_Engine",
):
    if _path.is_dir():
        _s = str(_path)
        if _s not in sys.path:
            sys.path.insert(0, _s)
