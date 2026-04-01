from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger

import cache_manager
import extractors
import loader
import output
from exceptions import AudioFeaturesError

FEATURE_TYPES = [
    "mfcc",
    "egemaps",
    "spectral",
    "chroma",
    "rms",
]


def _configure_logger() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        ),
        level="INFO",
        colorize=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract audio features from WAV files (16 kHz)."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to a WAV file or directory containing WAV files.",
    )
    parser.add_argument(
        "--type",
        choices=FEATURE_TYPES,
        help=f"Feature type to extract. Available: {', '.join(FEATURE_TYPES)}.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cache"),
        help="Directory to save results (default: cache). Omit to print to stdout.",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Delete all files in the cache/ directory.",
    )
    return parser.parse_args()


def main() -> None:
    _configure_logger()
    args = parse_args()

    if args.clear_cache:
        confirm = input("Are you sure you want to clear the cache? [y/N] ").strip().lower()
        if confirm == "y":
            cache_manager.clear_cache()
        else:
            logger.info("Aborted.")
        return

    if not args.input or not args.type:
        logger.error("--input and --type are required for feature extraction.")
        sys.exit(1)

    try:
        files = loader.resolve_files(args.input)
    except AudioFeaturesError as exc:
        logger.error("{exc}", exc=exc)
        sys.exit(1)

    if not files:
        logger.warning("No WAV files found.")
        return

    results = []
    for f in files:
        try:
            features = extractors.extract(args.type, f)
            results.append({"file": f, "features": features})
            logger.info("Processed: {path}", path=f)
        except AudioFeaturesError as exc:
            logger.error("Skipped {path}: {exc}", path=f, exc=exc)

    try:
        output.write(results, args.output, args.type)
    except AudioFeaturesError as exc:
        logger.error("{exc}", exc=exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
