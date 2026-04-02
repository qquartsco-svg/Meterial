from __future__ import annotations

import sys
from pathlib import Path


def import_sibling_package(package_name: str, folder_name: str):
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / folder_name
        if (candidate / package_name).is_dir():
            path = str(candidate)
            if path not in sys.path:
                sys.path.insert(0, path)
            return __import__(package_name, fromlist=["*"])
        candidate = parent / "_staging" / folder_name
        if (candidate / package_name).is_dir():
            path = str(candidate)
            if path not in sys.path:
                sys.path.insert(0, path)
            return __import__(package_name, fromlist=["*"])
    raise ImportError(f"Cannot resolve sibling package {package_name} in {folder_name}")
