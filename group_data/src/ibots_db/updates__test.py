from __future__ import annotations
from textwrap import dedent

import pytest
from pydantic import BaseModel
import yaml

from .updates import _validate_entry, _pydantic_to_yaml


class City(BaseModel):
        name: str
        restaurants: dict[str, Restaurant]

class Restaurant(BaseModel):
    owner: str
    max_size: int


#### VALIDATE ENTRY

def test_get_args_returns_correct_annotation_for_tech():
    key = 'restaurants'
    data = {
        'rest_1': Restaurant(owner='Nick', max_size=25),
    }
    
    _validate_entry(City, key, data)
    # no error raised, we're happy!
    assert True


def test_is_matching_raises_keyerror_when_key_not_found_in_basemodel():
    key = 'restaurant'
    data = {
        'rest_1': Restaurant(owner='Nick', max_size=25),
    }

    with pytest.raises(KeyError):
        _validate_entry(City, key, data)
    
def test_raises_typeerror_when_data_type_does_not_match_field_type():
    key = 'restaurants'
    data = [
        Restaurant(owner='Nick', max_size=25),
    ]
    with pytest.raises(TypeError):
        _validate_entry(City, key, data)


def test_raises_typeerror_when_data_type_of_keys_does_not_match_field_type():
    key = 'restaurants'
    data = {
        1: Restaurant(owner='Nick', max_size=25),
    }
    with pytest.raises(TypeError):
        _validate_entry(City, key, data)

    
def test_raises_typeerror_when_data_type_of_values_does_not_match_field_type():
    key = 'restaurants'
    data = {
        'aa': dict(owner='Nick', max_size=25),
    }
    with pytest.raises(TypeError):
        _validate_entry(City, key, data)


#####  PYDANTIC_TO_YAML

def test_can_make_yaml_from_pydantic_model():
    
    data = Restaurant(owner='Sangee', max_size=200)
    orig_data = data.model_dump(mode='json')
    text = _pydantic_to_yaml(data)
    observed_data = yaml.load(text, yaml.Loader)
    assert orig_data == observed_data


def test_yamls_merges():
    class Sequence(BaseModel):
        first: int
        second: int

    data = {'a': Sequence(first=1, second=2), 'b': Sequence(first=10, second=20)}
    expected = dedent("""
        a:
          first: 1
          second: 2
        b:
          first: 10
          second: 20
    """.lstrip('\n'))
    observed = _pydantic_to_yaml(data)
    assert observed == expected
