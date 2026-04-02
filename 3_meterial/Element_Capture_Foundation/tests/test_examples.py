from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def _run(name: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(EXAMPLES / name)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def test_run_capture_demo() -> None:
    out = _run("run_capture_demo.py")
    assert "CO2 DAC" in out
    assert "H2 electrolysis proxy" in out


def test_run_spacecraft_resource_loop_demo() -> None:
    out = _run("run_spacecraft_resource_loop.py")
    assert "capture_possible=" in out
    assert "regeneration_closure_gain_0_1=" in out


def test_run_capture_orbit_endurance_demo() -> None:
    out = _run("run_capture_orbit_endurance_demo.py")
    assert "orbits_per_day=" in out
    assert "mission_feasible=" in out
