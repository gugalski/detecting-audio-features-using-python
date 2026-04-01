from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import numpy.typing as npt
from loguru import logger

from exceptions import AudioValidationError, FeatureComputationError


def extract(
    file_path: Path,
    *,
    n_mfcc: int = 13,
    sr: int = 16000,
) -> dict[str, float]:
    """
    Extract MFCC coefficients from a WAV file.

    Parameters
    ----------
    file_path : Path
        Path to the WAV file (16 kHz, mono).
    n_mfcc : int, optional
        Number of MFCC coefficients. Default: 13.
    sr : int, optional
        Target sample rate. Default: 16000.

    Returns
    -------
    dict[str, float]
        Mean and std for each coefficient (keys: mfcc_1_mean, mfcc_1_std, …).

    Raises
    ------
    AudioValidationError
        If the signal is empty or contains NaN/Inf values.
    FeatureComputationError
        If the MFCC computation fails.
    """
    logger.debug("Loading: {path}", path=file_path)
    y: npt.NDArray[np.float32]
    y, _ = librosa.load(str(file_path), sr=sr, mono=True, dtype=np.float32)

    _validate_signal(y, path=file_path)

    try:
        mfcc: npt.NDArray[np.float32] = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    except Exception as exc:
        raise FeatureComputationError("mfcc", cause=exc) from exc

    logger.debug("Extracted {n} MFCC coefficients", n=n_mfcc)

    means = {f"mfcc_{i + 1}_mean": float(np.mean(mfcc[i])) for i in range(n_mfcc)}
    stds = {f"mfcc_{i + 1}_std": float(np.std(mfcc[i])) for i in range(n_mfcc)}
    return means | stds


def _validate_signal(signal: npt.NDArray[np.float32], *, path: Path) -> None:
    if signal.size == 0:
        raise AudioValidationError("Signal is empty (size 0).", path=path)
    if not np.isfinite(signal).all():
        raise AudioValidationError("Signal contains NaN or Inf values.", path=path)
