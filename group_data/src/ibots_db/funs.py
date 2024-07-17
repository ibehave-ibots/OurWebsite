from __future__ import annotations
from pathlib import Path
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


def update_all(key: str, data: dict[str, BaseModel]):
    # check the key is an attribute of the Data schema. (Done)
    # check that the BaseModel given is the same type specified by the schema. (Done)
    
    # make a temporary directory to try out the update (Done)

    # try it in temp:
        # copy the existing database into the temporary directory (Done)
        # change all the data to yaml and write it in the correct place (key)
        # check that that the temporary db reads properly and is valid
    # try it in real:
        # change all the data to yaml and write it in the correct place (key)
        # check that that the real db reads properly and is valid

    ...


if __name__ == '__main__':
    check_for_validation_errors(verbose=True)    
    