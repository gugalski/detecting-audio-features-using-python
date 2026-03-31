import os
from pathlib import Path


def resolve_files(input_path: str) -> list[str]:
    path = Path(input_path)
    if path.is_file():
        return [str(path)]
    if path.is_dir():
        return sorted(str(f) for f in path.rglob("*.wav"))
    raise FileNotFoundError(f"No such file or directory: {input_path}")
