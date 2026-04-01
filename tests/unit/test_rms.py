from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf

from exceptions import AudioValidationError
from extractors.rms import extract


def test_output_keys(sine_wav):
    result = extract(sine_wav)
    assert set(result.keys()) == {"rms_mean", "rms_std"}


def test_values_are_finite(sine_wav):
    result = extract(sine_wav)
    assert all(np.isfinite(v) for v in result.values())


def test_silent_signal_rms_near_zero(silent_wav):
    result = extract(silent_wav)
    assert result["rms_mean"] < 1e-6


def test_empty_signal_raises(tmp_path, sample_rate):
    path = tmp_path / "empty.wav"
    sf.write(str(path), np.array([], dtype=np.float32), sample_rate)
    with pytest.raises(AudioValidationError, match="empty"):
        extract(path)
