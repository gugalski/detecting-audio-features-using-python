from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import numpy.typing as npt
from loguru import logger

from exceptions import AudioValidationError, FeatureComputationError


def extract(file_path: Path, *, sr: int = 16000) -> dict[str, float]:
    """
    Extract spectral features from a WAV file.

    Computed features: spectral centroid, bandwidth, rolloff, zero-crossing rate.
    Each feature is summarized as mean and std across frames.

    Parameters
    ----------
    file_path : Path
        Path to the WAV file (16 kHz, mono).
    sr : int, optional
        Target sample rate. Default: 16000.

    Returns
    -------
    dict[str, float]
        Dictionary of spectral feature statistics.

    Raises
    ------
    AudioValidationError
        If the signal is empty or contains NaN/Inf values.
    FeatureComputationError
        If feature computation fails.
    """
    logger.debug("Extracting spectral features: {path}", path=file_path)
    y: npt.NDArray[np.float32]
    y, _ = librosa.load(str(file_path), sr=sr, mono=True, dtype=np.float32)

    _validate_signal(y, path=file_path)

    try:
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        zcr = librosa.feature.zero_crossing_rate(y)[0]
    except Exception as exc:
        raise FeatureComputationError("spectral", cause=exc) from exc

    logger.debug("Extracted spectral features", )

    return {
        "spectral_centroid_mean": float(np.mean(centroid)),
        "spectral_centroid_std": float(np.std(centroid)),
        "spectral_bandwidth_mean": float(np.mean(bandwidth)),
        "spectral_bandwidth_std": float(np.std(bandwidth)),
        "spectral_rolloff_mean": float(np.mean(rolloff)),
        "spectral_rolloff_std": float(np.std(rolloff)),
        "zcr_mean": float(np.mean(zcr)),
        "zcr_std": float(np.std(zcr)),
    }


def _validate_signal(signal: npt.NDArray[np.float32], *, path: Path) -> None:
    if signal.size == 0:
        raise AudioValidationError("Signal is empty (size 0).", path=path)
    if not np.isfinite(signal).all():
        raise AudioValidationError("Signal contains NaN or Inf values.", path=path)
