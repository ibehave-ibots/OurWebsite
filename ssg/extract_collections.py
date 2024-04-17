from typing import Any
from pathlib import Path
from collections import defaultdict
from pprint import pprint
from yaml import load, Loader

def extract_collections() -> dict[str, Any]:
    collections = defaultdict(list)
    base_path = Path('collections')
    for path in base_path.glob('*.yaml'):
        yaml_data = load(path.read_text(), Loader=Loader)
        collections[path.stem] = yaml_data
    for path in base_path.glob('*/*.yaml'):
        data = {'id': path.stem}
        yaml_data = load(path.read_text(), Loader=Loader)
        data.update(yaml_data)
        collections[path.parent.stem].append(data)
    return dict(collections)


if __name__ == '__main__':
    pprint(extract_collections())
    
