from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf

from exceptions import AudioValidationError
from extractors.mfcc import extract


def test_output_keys(sine_wav):
    result = extract(sine_wav)
    assert "mfcc_1_mean" in result
    assert "mfcc_1_std" in result
    assert "mfcc_13_mean" in result
    assert "mfcc_13_std" in result


def test_output_size_default(sine_wav):
    result = extract(sine_wav)
    assert len(result) == 26  # 13 means + 13 stds


@pytest.mark.parametrize("n_mfcc", [5, 13, 20])
def test_output_size_parametric(sine_wav, n_mfcc):
    result = extract(sine_wav, n_mfcc=n_mfcc)
    assert len(result) == n_mfcc * 2


def test_values_are_finite(sine_wav):
    result = extract(sine_wav)
    assert all(np.isfinite(v) for v in result.values())


def test_empty_signal_raises(tmp_path, sample_rate):
    path = tmp_path / "empty.wav"
    sf.write(str(path), np.array([], dtype=np.float32), sample_rate)
    with pytest.raises(AudioValidationError, match="empty"):
        extract(path)
