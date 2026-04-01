from __future__ import annotations

import csv
import sys
from pathlib import Path

from loguru import logger

from exceptions import ExportError


def write(results: list[dict], output_dir: Path | None, feature_type: str) -> None:
    """
    Write feature extraction results to CSV or print to stdout.

    Each audio file produces one CSV row with the filename as the primary key.
    When saving to a directory, files are stored in a subdirectory named after
    the feature type (e.g. cache/mfcc/sample.csv).

    Parameters
    ----------
    results : list[dict]
        List of {"file": Path, "features": dict[str, float]} dicts.
    output_dir : Path | None
        Output directory. None means stdout.
    feature_type : str
        Feature type name, used as the subdirectory name.

    Raises
    ------
    ExportError
        If writing to a file fails.
    """
    if not results:
        return

    fieldnames = ["file"] + list(results[0]["features"].keys())

    if output_dir is None:
        _write_stdout(results, fieldnames)
    else:
        _write_files(results, fieldnames, output_dir / feature_type)


def _write_stdout(results: list[dict], fieldnames: list[str]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for r in results:
        writer.writerow({"file": Path(r["file"]).stem} | r["features"])


def _write_files(results: list[dict], fieldnames: list[str], output_dir: Path) -> None:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ExportError(f"Cannot create output directory: {output_dir}") from exc

    for r in results:
        name = Path(r["file"]).stem
        out_file = output_dir / f"{name}.csv"
        try:
            with out_file.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({"file": name} | r["features"])
        except OSError as exc:
            raise ExportError(f"Failed to write: {out_file}") from exc
        logger.info("Saved: {path}", path=out_file)
