#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    ROOT / ".pytest_cache",
    ROOT / "tests" / "__pycache__",
    ROOT / "chemical_reaction" / "__pycache__",
]


def main() -> int:
    cleaned = 0
    for target in TARGETS:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            cleaned += 1
    print(f"cleaned={cleaned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
