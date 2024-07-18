from __future__ import annotations
from pathlib import Path
import shutil
from typing import Any

from yaml_dir_parser import load_dir

from .schema import Data
from pydantic import BaseModel

DATA_PATH = Path(__file__).parent.parent.parent / 'data'

def load(path: Path = DATA_PATH) -> Data:
    data_py: dict = load_dir(path)
    data = Data(**data_py)
    return data


def check_for_validation_errors(path: Path = DATA_PATH, verbose=False) -> None:
    """Raises error if there was a validation error.  Otherwise does nothing."""
    data = load_dir(path)
    if verbose:
        print('checking...', end='', flush=True)
    Data.model_validate(data)
    if verbose:
        print('...validated!')
    return None


def copy_to(target: Path, src: Path = DATA_PATH):
    shutil.copytree(src=src, dst=target, dirs_exist_ok=True)

    
if __name__ == '__main__':
    check_for_validation_errors(verbose=True)    
    