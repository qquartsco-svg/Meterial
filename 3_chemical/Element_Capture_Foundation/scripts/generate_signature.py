from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "SIGNATURE.sha256"
SKIP_PARTS = {".git", ".pytest_cache", "__pycache__"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts) or path.name == "SIGNATURE.sha256"


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    lines: list[str] = []
    count = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{hash_file(path)}  {rel}")
        count += 1
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {count} entries -> {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
