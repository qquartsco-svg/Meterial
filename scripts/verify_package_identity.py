#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "chemical_reaction"

EXPECTED = {
    "__init__.py",
    "constants.py",
    "contracts.py",
    "species_and_bonds.py",
    "thermodynamics.py",
    "kinetics.py",
    "equilibrium.py",
    "electrochemistry.py",
    "screening.py",
    "foundation.py",
    "extension_hooks.py",
    "domain_battery.py",
    "domain_life_support.py",
    "domain_materials.py",
}


def main() -> int:
    if not PACKAGE.is_dir():
        print(f"[FAIL] missing package dir: {PACKAGE}")
        return 1
    actual = {p.name for p in PACKAGE.iterdir() if p.is_file()}
    missing = sorted(EXPECTED - actual)
    unexpected = sorted(name for name in actual - EXPECTED if name.endswith(".py"))
    if missing or unexpected:
        if missing:
            print("[FAIL] missing expected package files:")
            for item in missing:
                print(f"  - {item}")
        if unexpected:
            print("[FAIL] unexpected python files in package:")
            for item in unexpected:
                print(f"  - {item}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
