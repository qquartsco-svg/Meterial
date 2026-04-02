from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run_step(label: str, command: list[str]) -> int:
    print(f"\n[{label}] {' '.join(command)}")
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode != 0:
        print(f"\n[FAIL] {label} failed")
        return completed.returncode
    return 0


def main() -> int:
    steps = [
        ("tests", [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short"]),
        ("examples", [sys.executable, "-m", "pytest", "tests/test_examples.py", "-q", "--tb=short"]),
        ("verify_signature", [sys.executable, "scripts/verify_signature.py"]),
        ("cleanup_generated", [sys.executable, "scripts/cleanup_generated.py"]),
    ]
    for label, command in steps:
        code = run_step(label, command)
        if code != 0:
            return code
    print("\n[OK] release_check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
