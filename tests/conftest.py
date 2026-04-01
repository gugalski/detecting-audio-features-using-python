from __future__ import annotations

import numpy as np
import pytest
import soundfile as sf


@pytest.fixture(scope="session")
def sample_rate() -> int:
    return 16000


@pytest.fixture
def sine_wav(tmp_path, sample_rate):
    """440 Hz sine wave, 2 seconds."""
    t = np.linspace(0.0, 2.0, sample_rate * 2, endpoint=False)
    signal = (np.sin(2 * np.pi * 440.0 * t) * 0.5).astype(np.float32)
    path = tmp_path / "sine.wav"
    sf.write(str(path), signal, sample_rate)
    return path


@pytest.fixture
def silent_wav(tmp_path, sample_rate):
    """Silent signal, 1 second."""
    signal = np.zeros(sample_rate, dtype=np.float32)
    path = tmp_path / "silent.wav"
    sf.write(str(path), signal, sample_rate)
    return path
