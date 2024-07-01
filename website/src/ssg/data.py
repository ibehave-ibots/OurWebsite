from typing import Any
from pathlib import Path, PurePosixPath
from collections import defaultdict
from .utils import load_yaml


def extract_global_data(base_path: Path) -> dict[str, Any]:
    def extract_recursive(path: Path) -> Any:
        path = Path(path)
        collections = {}
        for item in path.iterdir():
            if item.is_dir():
                collections[item.stem] = extract_recursive(item)
            else:
                if '.yaml' in item.name:
                    data = load_yaml(item.read_text())
                    if item.name == '.yaml':
                        collections.update(data)  # Merge directly if filanme only '.yaml'
                    else:
                        collections[item.stem] = data
                else:
                    collections[item.stem] = str(PurePosixPath(item.relative_to(base_path)))
        return collections

    return extract_recursive(base_path)
