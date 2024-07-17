from __future__ import annotations

import shutil
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from typing import Any, Dict, Type, _GenericAlias, GenericAlias, get_args, get_origin

import yaml
from pydantic import BaseModel

from . import schema
from .funs import DATA_PATH, check_for_validation_errors, load


def find_the_dict(annotation: Any) -> None | _GenericAlias:
    if not isinstance(annotation, (_GenericAlias, GenericAlias)):
        print(f'1: {annotation}')
        return None
    if get_origin(annotation) is dict:
        return annotation
    for arg in get_args(annotation):
        if find_the_dict(arg) is not None:
            return arg



def _validate_entry(base_model: BaseModel, key: str, data: dict[str, BaseModel]) -> None:
    """Prepares schema for checking and makes sure data to be entered is of the correct type."""
    base_model.model_rebuild()
    field = base_model.model_fields[key]
    dict_annotation = find_the_dict(field.annotation)
    if dict_annotation is None:
        print(field.annotation)
        raise TypeError(f"Look, you've got us a dict.  We've got {dict_annotation} here.")
    key_type, value_type = get_args(dict_annotation)

    if not isinstance(data, dict):
        raise TypeError(f'data has to be of type dict. Not {type(data)}')
    for key, value in data.items():
        if type(key) != key_type:
            raise TypeError(f'Expected {key_type}. Got {key} of type {type(key)} instead')
        if type(value) != value_type:
            raise TypeError(f'Expected {value_type}. Got {value} of type {type(value)} instead')        
    return None


def _pydantic_to_yaml(data: BaseModel | dict[str, BaseModel]) -> str:
    to_yaml = lambda d: yaml.dump(d, Dumper=yaml.Dumper)
    if isinstance(data, BaseModel):
        return to_yaml(data.model_dump(mode='json'))
    else:
        return to_yaml({k: m.model_dump(mode='json') for k, m in data.items()})
        

def _copy_db_to_tempdir(data_path: Path = DATA_PATH) -> Path:
    temp_dir = Path(TemporaryDirectory(prefix='dbcheck').name)
    shutil.copytree(data_path, temp_dir, dirs_exist_ok=True)
    return temp_dir


def update_all(key: str, data: dict[str, BaseModel], base_model: Type[BaseModel] = schema.Data, data_path: Path = DATA_PATH):
    _validate_entry(base_model=base_model, key=key, data=data)

    # Write the data
    temp_dir = _copy_db_to_tempdir()
    single_file_mode = temp_dir.joinpath(key).with_suffix('.yaml').exists()
    if single_file_mode:
        yaml_text = _pydantic_to_yaml(data=data)
        temp_dir.joinpath(key).with_suffix('.yaml').write_text(yaml_text)
    else:
        yaml_texts = {key: _pydantic_to_yaml(value) for key, value in data.items()}
        field_path = temp_dir.joinpath(key)
        field_path.mkdir(parents=True, exist_ok=True)
        for path in field_path.glob('*.yaml'):
            path.unlink()
        for k, yaml_text in yaml_texts.items():
            field_path.joinpath(k).with_suffix('.yaml').write_text(yaml_text)
    
    # Validate the data (Round-trip test)
    assert getattr(load(temp_dir), key) == data

    # Copy the new data over to the original database
    shutil.copytree(temp_dir, data_path, dirs_exist_ok=True)
    check_for_validation_errors(data_path) # Validate that the data still loads after copying
    

