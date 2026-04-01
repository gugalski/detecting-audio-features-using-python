from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import numpy.typing as npt
from loguru import logger

from exceptions import AudioValidationError, FeatureComputationError


def extract(file_path: Path, *, sr: int = 16000) -> dict[str, float]:
    """
    Extract RMS energy features from a WAV file.

    Parameters
    ----------
    file_path : Path
        Path to the WAV file (16 kHz, mono).
    sr : int, optional
        Target sample rate. Default: 16000.

    Returns
    -------
    dict[str, float]
        Mean and std of RMS energy across frames.

    Raises
    ------
    AudioValidationError
        If the signal is empty or contains NaN/Inf values.
    FeatureComputationError
        If feature computation fails.
    """
    logger.debug("Extracting RMS energy: {path}", path=file_path)
    y: npt.NDArray[np.float32]
    y, _ = librosa.load(str(file_path), sr=sr, mono=True, dtype=np.float32)

    _validate_signal(y, path=file_path)

    try:
        rms = librosa.feature.rms(y=y)[0]
    except Exception as exc:
        raise FeatureComputationError("rms", cause=exc) from exc

    logger.debug("Extracted RMS energy features")

    return {
        "rms_mean": float(np.mean(rms)),
        "rms_std": float(np.std(rms)),
    }


def _validate_signal(signal: npt.NDArray[np.float32], *, path: Path) -> None:
    if signal.size == 0:
        raise AudioValidationError("Signal is empty (size 0).", path=path)
    if not np.isfinite(signal).all():
        raise AudioValidationError("Signal contains NaN or Inf values.", path=path)
