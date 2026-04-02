"""Optional: sibling AOF / SIK on sys.path for integration tests."""

from __future__ import annotations

import sys
from pathlib import Path

_here = Path(__file__).resolve()
# .../Cooking_Process_Foundation/tests -> parents[1] == project root
_project_root = _here.parents[1]
# .../3_chemical/Cooking_Process_Foundation/tests -> parents[5] == 00_BRAIN
_brain_root = _here.parents[5]

for _pkg in (
    _project_root,
    _brain_root / "_staging" / "Cooking_Process_Foundation",
    _brain_root / "COOKing" / "Cooking_Process_Foundation",
):
    if _pkg.is_dir():
        s0 = str(_pkg)
        if s0 not in sys.path:
            sys.path.insert(0, s0)

for _base in (
    _brain_root / "_staging",
    _project_root.parent / "_staging",
    _brain_root,
):
    _aof = _base / "Anomalous_Observation_Foundation"
    if _aof.is_dir():
        s = str(_aof)
        if s not in sys.path:
            sys.path.insert(0, s)
        break

for _base in (_brain_root / "_staging", _project_root.parent / "_staging"):
    _sik = _base / "Sensory_Input_Kernel"
    if _sik.is_dir():
        s2 = str(_sik)
        if s2 not in sys.path:
            sys.path.insert(0, s2)
        break
