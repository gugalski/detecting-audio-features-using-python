from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf

from exceptions import AudioValidationError
from extractors.spectral import extract

EXPECTED_KEYS = {
    "spectral_centroid_mean", "spectral_centroid_std",
    "spectral_bandwidth_mean", "spectral_bandwidth_std",
    "spectral_rolloff_mean", "spectral_rolloff_std",
    "zcr_mean", "zcr_std",
}


def test_output_keys(sine_wav):
    result = extract(sine_wav)
    assert set(result.keys()) == EXPECTED_KEYS


def test_values_are_finite(sine_wav):
    result = extract(sine_wav)
    assert all(np.isfinite(v) for v in result.values())


def test_empty_signal_raises(tmp_path, sample_rate):
    path = tmp_path / "empty.wav"
    sf.write(str(path), np.array([], dtype=np.float32), sample_rate)
    with pytest.raises(AudioValidationError, match="empty"):
        extract(path)
