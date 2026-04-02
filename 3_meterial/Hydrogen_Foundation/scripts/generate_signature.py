#!/usr/bin/env python3
"""Generate SIGNATURE.sha256 manifest for Hydrogen_Foundation."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKED_FILES = sorted(
    [
        "hydrogen/__init__.py",
        "hydrogen/constants.py",
        "hydrogen/contracts.py",
        "hydrogen/properties.py",
        "hydrogen/production.py",
        "hydrogen/storage.py",
        "hydrogen/fuel_cell.py",
        "hydrogen/safety.py",
        "hydrogen/screening.py",
        "hydrogen/extension_hooks.py",
        "hydrogen/foundation.py",
        "hydrogen/domain_space.py",
        "hydrogen/domain_grid.py",
        "hydrogen/domain_transport.py",
        "tests/test_hydrogen_foundation.py",
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    manifest: dict = {"files": {}, "timestamp": "", "block_hash": ""}
    payload_parts = []
    for rel in TRACKED_FILES:
        fp = ROOT / rel
        if not fp.exists():
            print(f"  SKIP (missing): {rel}")
            continue
        digest = sha256_file(fp)
        manifest["files"][rel] = digest
        payload_parts.append(f"{rel}:{digest}")

    manifest["timestamp"] = datetime.now(timezone.utc).isoformat()
    block_payload = "\n".join(payload_parts)
    manifest["block_hash"] = hashlib.sha256(block_payload.encode()).hexdigest()

    out = ROOT / "SIGNATURE.sha256"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {out}")
    print(f"  Tracked: {len(manifest['files'])} files")
    print(f"  Block hash: {manifest['block_hash'][:16]}…")


if __name__ == "__main__":
    main()
