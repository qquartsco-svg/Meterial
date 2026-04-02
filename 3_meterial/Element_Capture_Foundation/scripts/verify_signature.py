from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SIGNATURE = ROOT / "SIGNATURE.sha256"


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not SIGNATURE.exists():
        print("[FAIL] SIGNATURE.sha256 not found")
        return 1

    passed = failed = missing = 0
    for line in SIGNATURE.read_text(encoding="utf-8").splitlines():
        if "  " not in line:
            continue
        expected, rel = line.split("  ", 1)
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING  {rel}")
            missing += 1
            continue
        actual = hash_file(path)
        if actual == expected:
            passed += 1
        else:
            print(f"FAILED   {rel}")
            failed += 1

    print(f"passed={passed} failed={failed} missing={missing}")
    return 0 if failed == 0 and missing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
