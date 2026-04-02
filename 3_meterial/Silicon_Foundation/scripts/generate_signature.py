#!/usr/bin/env python3
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TRACKED = sorted([
    "silicon/__init__.py","silicon/constants.py","silicon/contracts.py","silicon/properties.py",
    "silicon/refining.py","silicon/device.py","silicon/screening.py","silicon/extension_hooks.py","silicon/foundation.py",
    "tests/test_silicon_foundation.py","tests/conftest.py","README.md","README_EN.md","VERSION","pyproject.toml","CHANGELOG.md",
    "scripts/generate_signature.py","scripts/verify_signature.py",
])
def sha(p: Path)->str:
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
if __name__=="__main__":
    m={"files":{},"timestamp":datetime.now(timezone.utc).isoformat(),"block_hash":""}; parts=[]
    for rel in TRACKED:
        fp=ROOT/rel
        if fp.exists():
            d=sha(fp); m["files"][rel]=d; parts.append(f"{rel}:{d}")
    m["block_hash"]=hashlib.sha256("\n".join(parts).encode()).hexdigest()
    (ROOT/"SIGNATURE.sha256").write_text(json.dumps(m,indent=2,ensure_ascii=False)+"\n")
    print(f"Wrote SIGNATURE.sha256 ({len(m['files'])} files)")
