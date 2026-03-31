import argparse

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
        choices=FEATURE_TYPES,
        default="mfcc",
        help=f"Feature type to extract. Available: {', '.join(FEATURE_TYPES)}. Default: mfcc.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Directory to save results. If not set, results are printed to stdout.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Input:   {args.input}")
    print(f"Type:    {args.type}")
    print(f"Output:  {args.output or 'stdout'}")
    # TODO: implement feature extraction


if __name__ == "__main__":
    main()
