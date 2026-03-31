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
python main.py --input dataset/sample.wav

# Entire directory, save results to cache/
python main.py --input dataset/ --output cache/

# Choose feature set
python main.py --input dataset/ --features mfcc,egemaps,spectral
```

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
