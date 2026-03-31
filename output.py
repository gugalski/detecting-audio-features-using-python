import json
import os
from pathlib import Path


def write(file_path: str, features: dict, output_dir: str | None) -> None:
    name = Path(file_path).stem
    data = {"file": file_path, "features": features}

    if output_dir is None:
        print(json.dumps(data, indent=2))
    else:
        os.makedirs(output_dir, exist_ok=True)
        out_file = Path(output_dir) / f"{name}.json"
        with open(out_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved: {out_file}")
