#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT / "3_meterial"

REQUIRED_FILES = {
    HUB / "README.md",
    HUB / "ELEMENT_REGISTRY.md",
    HUB / "ELEMENT_FOUNDATION_TEMPLATE.md",
    HUB / "CHEMICAL_GOVERNANCE.md",
    HUB / "FOLDER_STRUCTURE.md",
    HUB / "CHEMICAL_HYGIENE_STATUS.md",
}

REQUIRED_DIRS = {
    HUB / "Chemical_Reaction_Foundation",
    HUB / "Hydrogen_Foundation",
    HUB / "Oxygen_Foundation",
    HUB / "Element_Capture_Foundation",
    HUB / "Battery_Dynamics_Engine",
    HUB / "Carbon_Composite_Stack",
}


def main() -> int:
    if not HUB.is_dir():
        print(f"[FAIL] missing hub directory: {HUB}")
        return 1

    missing = [str(path.relative_to(ROOT)) for path in sorted(REQUIRED_FILES | REQUIRED_DIRS) if not path.exists()]
    if missing:
        print("[FAIL] missing expected chemistry hub items:")
        for item in missing:
            print(f"  - {item}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
