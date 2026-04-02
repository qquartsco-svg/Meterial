#!/usr/bin/env python3
"""Generate SHA-256 integrity manifest for all tracked source files."""
import hashlib
import pathlib
import json
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIG_FILE = ROOT / "SIGNATURE.sha256"

TRACKED_GLOBS = [
    "chemical_reaction/**/*.py",
    "tests/**/*.py",
    "scripts/*.py",
    "pyproject.toml",
    "VERSION",
    "README.md",
    "README_EN.md",
    "CHANGELOG.md",
    "BLOCKCHAIN_INFO.md",
    "BLOCKCHAIN_INFO_EN.md",
    "PHAM_BLOCKCHAIN_LOG.md",
    "docs/*.md",
]


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def generate():
    manifest: dict = {}
    for pattern in TRACKED_GLOBS:
        for p in sorted(ROOT.glob(pattern)):
            if p.is_file():
                rel = p.relative_to(ROOT)
                manifest[str(rel)] = _sha256(p)

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prev_hash = ""
    if SIG_FILE.exists():
        prev_hash = hashlib.sha256(SIG_FILE.read_bytes()).hexdigest()

    payload = {
        "schema": "chemical_reaction_integrity_v1",
        "timestamp_utc": timestamp,
        "previous_manifest_hash": prev_hash,
        "file_count": len(manifest),
        "files": manifest,
    }

    manifest_json = json.dumps(payload, indent=2, ensure_ascii=False)
    block_hash = hashlib.sha256(manifest_json.encode()).hexdigest()
    payload["block_hash"] = block_hash

    final_json = json.dumps(payload, indent=2, ensure_ascii=False)
    SIG_FILE.write_text(final_json + "\n", encoding="utf-8")
    print(f"[OK] Wrote {SIG_FILE}")
    print(f"     Files tracked : {len(manifest)}")
    print(f"     Block hash    : {block_hash}")
    print(f"     Timestamp     : {timestamp}")


if __name__ == "__main__":
    generate()
