#!/usr/bin/env python3
"""Generate SHA-256 integrity manifest for the Meterial umbrella repository."""
import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIG_FILE = ROOT / "SIGNATURE.sha256"
EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
}
EXCLUDED_NAMES = {
    ".DS_Store",
    "SIGNATURE.sha256",
}


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def generate():
    manifest: dict = {}
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if rel.name in EXCLUDED_NAMES:
            continue
        manifest[str(rel)] = _sha256(p)

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prev_hash = ""
    if SIG_FILE.exists():
        prev_hash = hashlib.sha256(SIG_FILE.read_bytes()).hexdigest()

    payload = {
        "schema": "meterial_integrity_v2",
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
