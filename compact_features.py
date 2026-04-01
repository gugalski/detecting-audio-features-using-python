from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from loguru import logger


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


def merge_csv(input_dir: Path, output_file: Path) -> None:
    """
    Merge all CSV files from a directory into a single CSV file.

    Parameters
    ----------
    input_dir : Path
        Directory containing CSV files to merge.
    output_file : Path
        Path to the output CSV file.
    """
    files = sorted(input_dir.glob("*.csv"))
    if not files:
        logger.warning("No CSV files found in: {path}", path=input_dir)
        return

    logger.info("Found {n} CSV files in {path}", n=len(files), path=input_dir)

    rows: list[dict] = []
    fieldnames: list[str] | None = None

    for f in files:
        with f.open(newline="") as fh:
            reader = csv.DictReader(fh)
            if fieldnames is None:
                fieldnames = reader.fieldnames or []
            for row in reader:
                rows.append(row)

    if not rows or fieldnames is None:
        logger.warning("No data to merge.")
        return

    with output_file.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logger.info("Saved {n} rows to {path}", n=len(rows), path=output_file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge all CSV feature files from a directory into a single features.csv."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing CSV files to merge.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV file path. Default: <input>/features.csv.",
    )
    return parser.parse_args()


def main() -> None:
    _configure_logger()
    args = parse_args()

    if not args.input.is_dir():
        logger.error("Not a directory: {path}", path=args.input)
        sys.exit(1)

    output_file = args.output or args.input / "features.csv"
    merge_csv(args.input, output_file)


if __name__ == "__main__":
    main()
