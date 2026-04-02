#!/usr/bin/env python3
"""Verify file integrity against SIGNATURE.sha256 manifest."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    sig_path = ROOT / "SIGNATURE.sha256"
    if not sig_path.exists():
        print("ERROR: SIGNATURE.sha256 not found. Run generate_signature.py first.")
        return 1

    manifest = json.loads(sig_path.read_text())
    files = manifest.get("files", {})
    ok = 0
    fail = 0

    for rel, expected in files.items():
        fp = ROOT / rel
        if not fp.exists():
            print(f"  MISSING: {rel}")
            fail += 1
            continue
        actual = sha256_file(fp)
        if actual == expected:
            ok += 1
        else:
            print(f"  MISMATCH: {rel}")
            fail += 1

    print(f"\nVerified: {ok} OK, {fail} FAILED out of {len(files)} tracked files.")
    return 1 if fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
