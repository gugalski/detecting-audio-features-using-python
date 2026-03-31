import argparse

import extractors
import loader
import output

FEATURE_TYPES = [
    "mfcc",
    "egemaps",
    "spectral",
    "chroma",
    "rms",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract audio features from WAV files (16 kHz)."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a WAV file or directory containing WAV files.",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=FEATURE_TYPES,
        help=f"Feature type to extract. Available: {', '.join(FEATURE_TYPES)}.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Directory to save results. If not set, results are printed to stdout.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    files = loader.resolve_files(args.input)

    if not files:
        print("No WAV files found.")
        return

    for file_path in files:
        features = extractors.extract(args.type, file_path)
        output.write(file_path, features, args.output)


if __name__ == "__main__":
    main()
