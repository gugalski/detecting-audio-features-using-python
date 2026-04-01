from __future__ import annotations

from pathlib import Path

from loguru import logger

CACHE_DIR = Path("cache")


def clear_cache() -> None:
    """Delete all files and subdirectories from cache/ (except .gitkeep)."""
    if not CACHE_DIR.exists():
        logger.warning("Cache directory does not exist.")
        return

    files = [f for f in CACHE_DIR.rglob("*") if f.is_file() and f.name != ".gitkeep"]
    dirs = sorted(
        [d for d in CACHE_DIR.rglob("*") if d.is_dir()],
        reverse=True,  # deepest first
    )

    if not files and not dirs:
        logger.info("Cache is already empty.")
        return

    for f in files:
        f.unlink()
        logger.info("Deleted: {path}", path=f)

    for d in dirs:
        d.rmdir()
        logger.info("Removed directory: {path}", path=d)
