from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SIGNATURE.sha256"

SIGNED_FILES = [
    "README.md",
    "README_EN.md",
    "CHANGELOG.md",
    "BLOCKCHAIN_INFO.md",
    "PHAM_BLOCKCHAIN_LOG.md",
    "pyproject.toml",
    "VERSION",
    "docs/VERSIONING_POLICY.md",
    "docs/VERSIONING_POLICY_EN.md",
    "examples/sample_payload.json",
    "carbon_composite_stack/__init__.py",
    "carbon_composite_stack/contracts.py",
    "carbon_composite_stack/material.py",
    "carbon_composite_stack/process.py",
    "carbon_composite_stack/circularity.py",
    "carbon_composite_stack/observer.py",
    "carbon_composite_stack/pipeline.py",
    "carbon_composite_stack/engine_ref_adapter.py",
    "carbon_composite_stack/cli.py",
    "tests/test_carbon_composite_stack.py",
    "tests/conftest.py",
    "scripts/verify_signature.py",
    "scripts/generate_signature.py",
]


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    lines = []
    for rel in SIGNED_FILES:
        target = ROOT / rel
        if not target.exists():
            raise FileNotFoundError(f"missing signed file: {rel}")
        lines.append(f"{sha256_of(target)}  {rel}")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"updated {MANIFEST.name} with {len(lines)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

