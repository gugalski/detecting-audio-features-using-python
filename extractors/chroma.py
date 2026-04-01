from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import numpy.typing as npt
from loguru import logger

from exceptions import AudioValidationError, FeatureComputationError


def extract(file_path: Path, *, sr: int = 16000, n_chroma: int = 12) -> dict[str, float]:
    """
    Extract chroma STFT features from a WAV file.

    Each of the 12 chroma bins is summarized as mean and std across frames.

    Parameters
    ----------
    file_path : Path
        Path to the WAV file (16 kHz, mono).
    sr : int, optional
        Target sample rate. Default: 16000.
    n_chroma : int, optional
        Number of chroma bins. Default: 12.

    Returns
    -------
    dict[str, float]
        Dictionary of chroma feature statistics.

    Raises
    ------
    AudioValidationError
        If the signal is empty or contains NaN/Inf values.
    FeatureComputationError
        If feature computation fails.
    """
    logger.debug("Extracting chroma features: {path}", path=file_path)
    y: npt.NDArray[np.float32]
    y, _ = librosa.load(str(file_path), sr=sr, mono=True, dtype=np.float32)

    _validate_signal(y, path=file_path)

    try:
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=n_chroma)
    except Exception as exc:
        raise FeatureComputationError("chroma", cause=exc) from exc

    logger.debug("Extracted {n} chroma bins", n=n_chroma)

    means = {f"chroma_{i + 1}_mean": float(np.mean(chroma[i])) for i in range(n_chroma)}
    stds = {f"chroma_{i + 1}_std": float(np.std(chroma[i])) for i in range(n_chroma)}
    return means | stds


def _validate_signal(signal: npt.NDArray[np.float32], *, path: Path) -> None:
    if signal.size == 0:
        raise AudioValidationError("Signal is empty (size 0).", path=path)
    if not np.isfinite(signal).all():
        raise AudioValidationError("Signal contains NaN or Inf values.", path=path)
