from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGETS = [".pytest_cache", "__pycache__"]


def main() -> int:
    cleaned = 0
    for path in ROOT.rglob("*"):
        if path.name in TARGETS and path.exists():
            shutil.rmtree(path, ignore_errors=True)
            cleaned += 1
    print(f"cleaned={cleaned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
