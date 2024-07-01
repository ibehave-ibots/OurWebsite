from typing import Any
from pathlib import Path, PurePosixPath
from collections import defaultdict
from .utils import load_yaml


def extract_global_data(base_path: Path) -> dict[str, Any]:
    base_path = Path(base_path)
    collections = {}
    for path in base_path.glob('*.*'):
        if path.suffix == '.yaml':
            data = load_yaml(path.read_text())
            collections[path.stem] = data
        else:
            collections[path.stem] = str(PurePosixPath(path.relative_to(path.parent)))
    for path in base_path.glob('*/*.*'):
        if not path.parent.stem in collections:
            collections[path.parent.stem] = {}
        if path.suffix == '.yaml':
            data = load_yaml(path.read_text())
            collections[path.parent.stem][path.stem] = data
        else:
            collections[path.parent.stem][path.stem] = str(PurePosixPath(path.relative_to(path.parent.parent)))
    for path in base_path.glob('*/*/*.*'):
        if not path.parent.parent.stem in collections:
            collections[path.parent.parent.stem] = {}
        if not path.parent.stem in collections[path.parent.parent.stem]:
            collections[path.parent.parent.stem][path.parent.stem] = {}
        if path.suffix == '.yaml':
            data = load_yaml(path.read_text())
            collections[path.parent.parent.stem][path.parent.stem][path.stem] = data
        else:
            collections[path.parent.parent.stem][path.parent.stem][path.stem] = str(PurePosixPath(path.relative_to(path.parent.parent.parent)))
    for path in base_path.glob('*/*/*'):
        if path.is_dir():
            raise NotImplementedError("only single- and double-nested collections are currently supported, sorry.")
    return collections


