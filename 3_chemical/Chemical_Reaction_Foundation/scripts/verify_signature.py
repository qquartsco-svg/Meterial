#!/usr/bin/env python3
"""Verify file integrity against SIGNATURE.sha256 manifest."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIG_FILE = ROOT / "SIGNATURE.sha256"


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def verify() -> int:
    if not SIG_FILE.exists():
        print(f"[FAIL] Missing {SIG_FILE}")
        return 1
    data = json.loads(SIG_FILE.read_text(encoding="utf-8"))
    files = data.get("files", {})
    errors: list[str] = []
    for rel, expected in sorted(files.items()):
        p = ROOT / rel
        if not p.is_file():
            errors.append(f"missing: {rel}")
            continue
        actual = _sha256(p)
        if actual != expected:
            errors.append(f"mismatch: {rel}\n  expected {expected}\n  actual   {actual}")
    if errors:
        print("[FAIL] Signature verification failed:")
        for e in errors:
            print("  ", e)
        return 1
    print(f"[OK] All {len(files)} files match SIGNATURE.sha256")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
