import numpy as np
import librosa


def extract(file_path: str, n_mfcc: int = 13, sr: int = 16000) -> dict:
    y, sr = librosa.load(file_path, sr=sr, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return {
        f"mfcc_{i+1}_mean": float(np.mean(mfcc[i]))
        for i in range(n_mfcc)
    } | {
        f"mfcc_{i+1}_std": float(np.std(mfcc[i]))
        for i in range(n_mfcc)
    }
