#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    cleaned = 0
    for target in ROOT.rglob("*"):
        if target.name in {"__pycache__", ".pytest_cache"} and target.exists():
            if target.is_dir():
                shutil.rmtree(target)
                cleaned += 1
        elif target.name == ".DS_Store" and target.exists():
            target.unlink()
            cleaned += 1
    print(f"cleaned={cleaned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
