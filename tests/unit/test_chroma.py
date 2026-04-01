from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf

from exceptions import AudioValidationError
from extractors.chroma import extract


def test_output_size_default(sine_wav):
    result = extract(sine_wav)
    assert len(result) == 24  # 12 means + 12 stds


@pytest.mark.parametrize("n_chroma", [6, 12])
def test_output_size_parametric(sine_wav, n_chroma):
    result = extract(sine_wav, n_chroma=n_chroma)
    assert len(result) == n_chroma * 2


def test_output_keys(sine_wav):
    result = extract(sine_wav)
    assert "chroma_1_mean" in result
    assert "chroma_12_std" in result


def test_values_are_finite(sine_wav):
    result = extract(sine_wav)
    assert all(np.isfinite(v) for v in result.values())


def test_empty_signal_raises(tmp_path, sample_rate):
    path = tmp_path / "empty.wav"
    sf.write(str(path), np.array([], dtype=np.float32), sample_rate)
    with pytest.raises(AudioValidationError, match="empty"):
        extract(path)
