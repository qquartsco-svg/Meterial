#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(*args: str) -> None:
    print(f"\n[run] {' '.join(args)}")
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    py = sys.executable
    run(py, "-m", "pytest", "tests", "-q")
    run(py, "scripts/verify_package_identity.py")
    run(py, "scripts/verify_signature.py")
    run(py, "scripts/cleanup_generated.py")
    print("\n[OK] release_check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
