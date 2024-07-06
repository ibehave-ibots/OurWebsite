from typing import Any, Dict
from pathlib import Path, PurePosixPath

import yaml 


def extract_global_data(base_path: Path | str) -> Dict[str, Any]:
    base_path = Path(base_path)

    return _extract_recursive(base_path, base_path)


def _process_file(item: Path, base_path: Path, collections: Dict[str, Any]) -> None:
    if item.name == '.yaml':  # Is only a YAML extension?  Read it and just stick the data onto the parent.
        data = yaml.load(item.read_text(), Loader=yaml.Loader)  
        collections.update(data)  
    elif '.yaml' in item.name:  # Has a YAML extension?  Read it and use the filename's id as the key.
        data = yaml.load(item.read_text(), Loader=yaml.Loader)  
        collections[item.stem] = data
    else:  # Not sure how to parse the file?  Then assign a relative filepath.
        collections[item.stem] = str(PurePosixPath(item.relative_to(base_path)))


def _extract_recursive(path: Path, base_path: Path) -> Dict[str, Any]:
    
    collections = {}
    for item in path.iterdir():
        if item.is_dir():
            collections[item.stem] = _extract_recursive(item, base_path)
        else:
            _process_file(item, base_path, collections)
    return collections

