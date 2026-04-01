# detecting-audio-features-using-python

CLI tool for extracting audio features from WAV files (16 kHz). Supports batch processing of entire directories or single files. Results are saved as CSV files (one per audio file) or printed to stdout.

> [!WARNING]
> This project extracts **aggregated (mean/std) features** — temporal information is collapsed into a fixed-size vector per file. This makes the output suitable for classical ML models (SVM, Random Forest, MLP) but **not** for recurrent neural networks (RNN, LSTM, GRU) or other architectures that require time-series input.

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
# Single file, save to cache/
python features.py --input dataset/sample.wav --type mfcc

# Entire directory, save to custom output directory
python features.py --input dataset/ --type egemaps --output results/

# Print to stdout instead of saving
python features.py --input dataset/sample.wav --type spectral --output -
```

### Arguments

| Argument | Required | Description |
|---|---|---|
| `--input` | yes | Path to a WAV file or directory |
| `--type` | yes | Feature type to extract (see table below) |
| `--output` | no | Output directory (default: `cache/`) |
| `--clear-cache` | no | Delete all files in `cache/` |

### `--type` — available feature types

| Value | Description |
|---|---|
| `mfcc` | Mel-frequency cepstral coefficients |
| `egemaps` | Extended Geneva Minimalistic Acoustic Parameter Set |
| `spectral` | Spectral centroid, bandwidth, rolloff, zero-crossing rate |
| `chroma` | Chroma STFT |
| `rms` | Root mean square energy |

### Cache management

```bash
# Delete all files in cache/
python features.py --clear-cache
```

## Output

Each audio file produces a separate CSV file named after the source recording (e.g. `sample.wav` → `cache/mfcc/sample.csv`). The first column is the filename (without extension), followed by feature values.

### Merging results into a single file

Use `compact_features.py` to combine all per-file CSVs from a directory into one `features.csv`:

```bash
# Merge all CSVs from cache/mfcc/ → cache/mfcc/features.csv
python compact_features.py --input cache/mfcc/

# Save to a custom path
python compact_features.py --input cache/mfcc/ --output dataset/mfcc_features.csv
```

| Argument | Required | Description |
|---|---|---|
| `--input` | yes | Directory containing CSV files to merge |
| `--output` | no | Output file path (default: `<input>/features.csv`) |

## Setup

```bash
pip3 install -r requirements.txt
```

Requires openSMILE installed separately: https://audeering.github.io/opensmile/

## Development

```bash
# Linting
python3 -m ruff check .

# Unit tests
python3 -m pytest

# Single test file
python3 -m pytest tests/unit/test_mfcc.py
```

## Directory Structure

```
dataset/    # place WAV recordings here (not tracked by git)
cache/      # extracted features saved here (not tracked by git)
```
