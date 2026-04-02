#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKED = sorted(
    [
        "nitrogen/__init__.py",
        "nitrogen/constants.py",
        "nitrogen/contracts.py",
        "nitrogen/properties.py",
        "nitrogen/air_separation.py",
        "nitrogen/fixation.py",
        "nitrogen/storage.py",
        "nitrogen/safety.py",
        "nitrogen/screening.py",
        "nitrogen/extension_hooks.py",
        "nitrogen/domain_agriculture.py",
        "nitrogen/foundation.py",
        "tests/test_nitrogen_foundation.py",
        "tests/conftest.py",
        "README.md",
        "README_EN.md",
        "VERSION",
        "pyproject.toml",
        "CHANGELOG.md",
        "scripts/generate_signature.py",
        "scripts/verify_signature.py",
    ]
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main() -> None:
    m: dict = {"files": {}, "timestamp": "", "block_hash": ""}
    parts = []
    for rel in TRACKED:
        fp = ROOT / rel
        if not fp.exists():
            continue
        d = sha256_file(fp)
        m["files"][rel] = d
        parts.append(f"{rel}:{d}")
    m["timestamp"] = datetime.now(timezone.utc).isoformat()
    m["block_hash"] = hashlib.sha256("\n".join(parts).encode()).hexdigest()
    (ROOT / "SIGNATURE.sha256").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote SIGNATURE.sha256 ({len(m['files'])} files)")


if __name__ == "__main__":
    main()
