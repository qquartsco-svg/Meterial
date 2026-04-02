#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    sp = ROOT / "SIGNATURE.sha256"
    if not sp.exists():
        return 1
    m = json.loads(sp.read_text())
    fail = 0
    for rel, exp in m.get("files", {}).items():
        fp = ROOT / rel
        if not fp.exists() or sha256_file(fp) != exp:
            fail += 1
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
