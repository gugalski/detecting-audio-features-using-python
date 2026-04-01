from __future__ import annotations

from pathlib import Path

import opensmile
from loguru import logger

from exceptions import FeatureComputationError

_smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)


def extract(file_path: Path) -> dict[str, float]:
    """
    Extract eGeMAPS v02 features from a WAV file using openSMILE.

    Parameters
    ----------
    file_path : Path
        Path to the WAV file (16 kHz, mono).

    Returns
    -------
    dict[str, float]
        Dictionary of eGeMAPS functional features (88 values).

    Raises
    ------
    FeatureComputationError
        If openSMILE processing fails.
    """
    logger.debug("Extracting eGeMAPS: {path}", path=file_path)
    try:
        df = _smile.process_file(str(file_path))
    except Exception as exc:
        raise FeatureComputationError("egemaps", cause=exc) from exc

    logger.debug("Extracted {n} eGeMAPS features", n=df.shape[1])
    return {col: float(df[col].iloc[0]) for col in df.columns}
