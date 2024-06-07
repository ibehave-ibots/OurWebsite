from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Dict, NamedTuple, Tuple
from pprint import pprint
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

@dataclass(frozen=True)
class ResultDTO:
    short_name: str
    name: str
    value: float
    units: str
    display_units: str

@dataclass
class ConsultingResultRepo:
    _consulting_results: list[ConsultingResult] = field(repr=False)
    path: Path

    @classmethod
    def connect(cls, path, write_mode = False) -> ConsultingResultRepo:
        path = Path(path)
        results = []
        for file in path.glob('*.json'):
            result = ConsultingResult.model_validate_json(file.read_text())
            results.append(result)
        
        return ConsultingResultRepo(
            _consulting_results=results,
            path=path,
        )

    @requires_write_permission
    def clear_all(self) -> None: 
        self._consulting_results.clear()
            
    @requires_write_permission
    def put(self, short_name: str, name: str, value: float, units: str, display_units: str) -> None:
        result = ConsultingResult(
            short_name=short_name,
            name=name,
            value=value,
            units=units,
            display_units=display_units,
        )
        self._consulting_results.append(result)

    def list(self) -> list[ResultDTO]:
        results = []
        for result in self._consulting_results:
            r = self.get(result.short_name)
            results.append(r)
        return results

    def get(self, s_name: str) -> ResultDTO:
        for result in self._consulting_results:
            if s_name in result.short_name:
                return ResultDTO(
                    short_name=result.short_name,
                    name=result.name,
                    value=result.value,
                    units=result.units,
                    display_units=result.display_units

                )
    
    def to_dict(self) -> Dict[Any, Any]:
        return {
            'short_name': [result.short_name for result in self._consulting_results],
            'name': [result.name for result in self._consulting_results],
            'value': [result.value for result in self._consulting_results],
            'units': [result.units for result in self._consulting_results],
            'display_units': [result.display_units for result in self._consulting_results],
        }
        
    def save(self):
        path = Path(self.path)
        if path.exists():
            assert path.is_dir()
        
        path.mkdir(parents=True, exist_ok=True)
        for result in self._consulting_results:
            json_text = result.model_dump_json(indent=3)
            fname = result.short_name
            path.joinpath(f'{fname}.json').write_text(json_text)