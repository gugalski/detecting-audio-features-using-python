from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf

from exceptions import AudioFileNotFoundError
from loader import resolve_files


def test_single_file(sine_wav):
    result = resolve_files(sine_wav)
    assert result == [sine_wav]


def test_directory(tmp_path, sample_rate):
    for name in ("a.wav", "b.wav", "c.wav"):
        sf.write(str(tmp_path / name), np.zeros(sample_rate, dtype=np.float32), sample_rate)
    result = resolve_files(tmp_path)
    assert len(result) == 3
    assert result == sorted(result)


def test_directory_recursive(tmp_path, sample_rate):
    sub = tmp_path / "sub"
    sub.mkdir()
    sf.write(str(tmp_path / "a.wav"), np.zeros(sample_rate, dtype=np.float32), sample_rate)
    sf.write(str(sub / "b.wav"), np.zeros(sample_rate, dtype=np.float32), sample_rate)
    result = resolve_files(tmp_path)
    assert len(result) == 2


def test_nonexistent_path_raises(tmp_path):
    with pytest.raises(AudioFileNotFoundError):
        resolve_files(tmp_path / "nonexistent.wav")


def test_empty_directory_returns_empty(tmp_path):
    result = resolve_files(tmp_path)
    assert result == []
