from __future__ import annotations

from pathlib import Path


class AudioFeaturesError(Exception):
    """Base exception for the project."""

    def __init__(self, message: str, *, context: dict | None = None) -> None:
        super().__init__(message)
        self.context: dict = context or {}

    def __str__(self) -> str:
        base = super().__str__()
        if self.context:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{base} [{ctx}]"
        return base


class AudioIOError(AudioFeaturesError):
    """I/O errors for audio files."""


class AudioFileNotFoundError(AudioIOError):
    """Requested audio file does not exist."""

    def __init__(self, path: Path) -> None:
        super().__init__(f"Audio file not found: {path}", context={"path": str(path)})
        self.path = path


class AudioFormatError(AudioIOError):
    """Unsupported or corrupted audio file format."""

    def __init__(self, path: Path, *, reason: str) -> None:
        super().__init__(
            f"Invalid audio format: {path}",
            context={"path": str(path), "reason": reason},
        )


class AudioValidationError(AudioFeaturesError):
    """Audio data does not meet requirements (empty signal, NaN, wrong dtype)."""

    def __init__(self, message: str, *, path: Path | None = None) -> None:
        super().__init__(message, context={"path": str(path)} if path else None)


class FeatureExtractionError(AudioFeaturesError):
    """General error during feature extraction."""


class FeatureComputationError(FeatureExtractionError):
    """Numerical error during feature computation."""

    def __init__(self, feature_name: str, *, cause: Exception) -> None:
        super().__init__(
            f"Failed to compute feature '{feature_name}'",
            context={"feature": feature_name, "cause": str(cause)},
        )
        self.__cause__ = cause


class ExportError(AudioFeaturesError):
    """Error during result export."""
