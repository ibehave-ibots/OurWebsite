from typing import Any
from pathlib import Path
from collections import defaultdict
from .utils import load_yaml


def extract_data(base_path: Path) -> dict[str, Any]:
    base_path = Path(base_path)
    collections = defaultdict(dict)
    for path in base_path.glob('*.yaml'):
        data = load_yaml(path.read_text())
        collections[path.stem] = data
    for path in base_path.glob('*/*.yaml'):
        data = load_yaml(path.read_text())
        collections[path.parent.stem][path.stem] = data
    for path in base_path.glob('*/*'):
        if path.is_dir():
            raise NotImplementedError("only single-nested collectoins are currently supported, sorry.")
    return dict(collections)


