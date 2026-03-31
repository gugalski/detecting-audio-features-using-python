# detecting-audio-features-using-python

CLI tool for extracting audio features from WAV files (16 kHz). Supports batch processing of entire directories or single files. Results can be printed to stdout or saved to the `cache/` directory.

## Features

Extracted feature sets:

- **MFCC** — Mel-frequency cepstral coefficients (via librosa)
- **eGeMAPS** — Extended Geneva Minimalistic Acoustic Parameter Set (via openSMILE)
- **Spectral features** — spectral centroid, bandwidth, rolloff, zero-crossing rate (via librosa)
- **Chroma** — chroma STFT (via librosa)
- **RMS energy** — root mean square energy (via librosa)

## Input

- Format: WAV, 16 kHz
- Source: single file or directory (e.g. `dataset/`)

## Usage

```bash
# Single file, print to stdout
python features.py --input dataset/sample.wav --type mfcc

# Entire directory, save results to cache/
python features.py --input dataset/ --type egemaps --output cache/
```

### `--type` — available feature types

| Value | Description |
|---|---|
| `mfcc` | Mel-frequency cepstral coefficients |
| `egemaps` | Extended Geneva Minimalistic Acoustic Parameter Set |
| `spectral` | Spectral centroid, bandwidth, rolloff, zero-crossing rate |
| `chroma` | Chroma STFT |
| `rms` | Root mean square energy |

Default: `mfcc`

## Setup

```bash
pip install -r requirements.txt
```

Requires openSMILE installed separately: https://audeering.github.io/opensmile/

## Directory Structure

```
dataset/    # place WAV recordings here (not tracked by git)
cache/      # extracted features saved here (not tracked by git)
```
