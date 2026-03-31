from extractors import mfcc

_EXTRACTORS = {
    "mfcc": mfcc.extract,
}


def extract(feature_type: str, file_path: str) -> dict:
    return _EXTRACTORS[feature_type](file_path)
