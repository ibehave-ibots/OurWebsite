from typing import Any
from pathlib import Path, PurePosixPath
from collections import defaultdict
from .utils import load_yaml


def extract_global_data(base_path: Path) -> dict[str, Any]:
    def extract_recursive(path: Path) -> Any:
        collections = {}
        for item in path.iterdir():
            if item.is_dir():
                collections[item.stem] = extract_recursive(item)
            else:
                if item.suffix == '.yaml':
                    data = load_yaml(item.read_text())
                    collections[item.stem] = data
                else:
                    collections[item.stem] = str(PurePosixPath(item.relative_to(base_path)))
        return collections

    return extract_recursive(base_path)
