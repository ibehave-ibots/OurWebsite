from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Dict, NamedTuple, Tuple, TypedDict
from warnings import warn
from fsspec import filesystem
from pprint import pprint
import fsspec
from pydantic import BaseModel
import functools

def requires_write_permission(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        if not os.getenv('DB_WRITEMODE'):
            raise PermissionError("Write permission disabled")
        return fun(*args, **kwargs)
    return wrapper

class ConsultingResult(BaseModel):
    short_name: str
    name: str
    value: float
    units: str
    display_units: str


class ResultDict(TypedDict):
    short_name: str
    name: str
    value: float
    units: str
    display_units: str

@dataclass
class ConsultingResultRepo:
    _consulting_results: dict[str, ConsultingResult] = field(repr=False)
    path: fsspec.AbstractFileSystem

    @classmethod
    def connect(cls, path: fsspec.AbstractFileSystem) -> ConsultingResultRepo:
        results = {}      
        return ConsultingResultRepo(
            _consulting_results=results,
            path=path,
        )

    @requires_write_permission
    def clear(self) -> None: 
        self._consulting_results.clear()
    
    def remove(self, s_name: str) -> None:
        self._consulting_results.pop(s_name)
            
    @requires_write_permission
    def put(self, short_name: str, name: str, value: float, units: str, display_units: str) -> None:
        result = ConsultingResult(
            short_name=short_name,
            name=name,
            value=value,
            units=units,
            display_units=display_units,
        )
        self._consulting_results[result.short_name] = result

    def list(self) -> list[ResultDict]:
        results = []
        for result_short_name in self._consulting_results.keys():
            r = self.get(result_short_name)
            results.append(r)
        return results

    def get(self, s_name: str) -> ResultDict:
        results = self._consulting_results
        result: ResultDict = results[s_name].model_dump()
        return result
        
    def push(self):
        path = self.path
        for file in path.glob('*.json'):
            try:
                path.rm(file)
            except:
                warn(f"{file[:-5]} was not deleted")
                
        for result in self._consulting_results.values():
            json_text = result.model_dump_json(indent=3)
            fname = result.short_name
            with path.open(f'{fname}.json', 'w') as f:
                f.write(json_text)

    def pull(self):
        path = self.path
        results = {}
        for file in path.glob('*.json'):
            f = path.open(file, 'r')
            result = ConsultingResult.model_validate_json(f.read())
            results[result.short_name] = result
        self._consulting_results = results

    def clone_to(self, repo: ConsultingResultRepo):
        repo.clear()
        self.pull()
        for result in self.list():
            repo.put(**result)
        repo.push()
        