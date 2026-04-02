#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKED = sorted([
    "lithium/__init__.py",
    "lithium/constants.py",
    "lithium/contracts.py",
    "lithium/properties.py",
    "lithium/extraction.py",
    "lithium/battery.py",
    "lithium/screening.py",
    "lithium/extension_hooks.py",
    "lithium/foundation.py",
    "tests/test_lithium_foundation.py",
    "tests/conftest.py",
    "README.md",
    "README_EN.md",
    "VERSION",
    "pyproject.toml",
    "CHANGELOG.md",
    "scripts/generate_signature.py",
    "scripts/verify_signature.py",
])

def sha256_file(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

if __name__ == "__main__":
    m = {"files": {}, "timestamp": datetime.now(timezone.utc).isoformat(), "block_hash": ""}
    parts = []
    for rel in TRACKED:
        fp = ROOT / rel
        if fp.exists():
            d = sha256_file(fp)
            m["files"][rel] = d
            parts.append(f"{rel}:{d}")
    m["block_hash"] = hashlib.sha256("\n".join(parts).encode()).hexdigest()
    (ROOT / "SIGNATURE.sha256").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote SIGNATURE.sha256 ({len(m['files'])} files)")
