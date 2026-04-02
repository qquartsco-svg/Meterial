from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .engine_ref_adapter import run_engine_ref_payload


def _load(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input json must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Carbon composite readiness assessment")
    parser.add_argument("--input-json", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    out = run_engine_ref_payload(_load(args.input_json))
    if args.json:
        print(json.dumps(out, ensure_ascii=True))
    else:
        print(f"[{out['engine_ref']}] verdict={out['verdict']} omega={out['omega']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

