from typing import Any
from pathlib import Path
from collections import defaultdict
from pprint import pprint
from yaml import load, Loader

def extract(base_path: Path) -> dict[str, Any]:
    collections = defaultdict(dict)
    for path in base_path.glob('*.yaml'):
        data = load(path.read_text(), Loader=Loader)
        collections[path.stem] = data
    for path in base_path.glob('*/*.yaml'):
        data = load(path.read_text(), Loader=Loader)
        collections[path.parent.stem][path.stem] = data
    for path in base_path.glob('*/*'):
        if path.is_dir():
            raise NotImplementedError("only single-nested collectoins are currently supported, sorry.")
    return dict(collections)


if __name__ == '__main__':
    pprint(extract())
    
