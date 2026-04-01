from __future__ import annotations

from pathlib import Path

from loguru import logger

CACHE_DIR = Path("cache")


def clear_cache() -> None:
    """Delete all files from the cache/ directory (except .gitkeep)."""
    if not CACHE_DIR.exists():
        logger.warning("Cache directory does not exist.")
        return

    files = [f for f in CACHE_DIR.iterdir() if f.is_file() and f.name != ".gitkeep"]
    if not files:
        logger.info("Cache is already empty.")
        return

    for f in files:
        f.unlink()
        logger.info("Deleted: {path}", path=f)
