from __future__ import annotations

from pathlib import Path

from loguru import logger

from exceptions import AudioFileNotFoundError


def resolve_files(input_path: Path) -> list[Path]:
    """
    Return a list of WAV files to process.

    Parameters
    ----------
    input_path : Path
        Path to a single WAV file or a directory.

    Returns
    -------
    list[Path]
        Sorted list of WAV file paths.

    Raises
    ------
    AudioFileNotFoundError
        If the given path does not exist.
    """
    if input_path.is_file():
        logger.debug("Single file mode: {path}", path=input_path)
        return [input_path]

    if input_path.is_dir():
        files = sorted(input_path.rglob("*.wav"))
        logger.debug("Found {n} WAV file(s) in {path}", n=len(files), path=input_path)
        return files

    raise AudioFileNotFoundError(input_path)
