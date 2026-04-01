from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from extractors import chroma, egemaps, mfcc, rms, spectral

_EXTRACTORS: dict[str, Callable[[Path], dict[str, float]]] = {
    "mfcc": mfcc.extract,
    "egemaps": egemaps.extract,
    "spectral": spectral.extract,
    "chroma": chroma.extract,
    "rms": rms.extract,
}


def extract(feature_type: str, file_path: Path) -> dict[str, float]:
    """
    Extract features from an audio file using the specified extractor.

    Parameters
    ----------
    feature_type : str
        Feature type to extract (must be a key in _EXTRACTORS).
    file_path : Path
        Path to the WAV file.

    Returns
    -------
    dict[str, float]
        Dictionary of feature values.
    """
    return _EXTRACTORS[feature_type](file_path)
