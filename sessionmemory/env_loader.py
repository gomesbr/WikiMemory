from __future__ import annotations

import os
from pathlib import Path


def load_project_env(start_path: Path | None = None) -> Path | None:
    start = (start_path or Path.cwd()).resolve()
    for directory in (start, *start.parents):
        candidate = directory / ".env"
        if not candidate.exists() or not candidate.is_file():
            continue
        for raw_line in candidate.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = _clean_value(value.strip())
        return candidate
    return None


def _clean_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
