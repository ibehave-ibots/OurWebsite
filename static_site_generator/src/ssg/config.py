from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, DirectoryPath


class Config(BaseModel):
    base_url: str = ''
    base_dir: DirectoryPath = DirectoryPath('.')
    global_data_loader: Literal['iBOTS_DB'] = 'iBOTS_DB'
    global_data_path: DirectoryPath = DirectoryPath('./data')
    


class GlobalDataLoader(ABC):

    @abstractmethod
    def load(self, path: Path) -> dict[str, Any]: ...


class IBOTSGlobalDataLoader(GlobalDataLoader):

    def load(self, path: Path) -> dict[str, Any]:
        import ibots_db
        data = ibots_db.load(path)
        return data.model_dump(mode='json')
    

@dataclass
class App:
    global_data_loader: GlobalDataLoader = field(default_factory=IBOTSGlobalDataLoader)

    @classmethod
    def from_config(cls, config: Config) -> App:
        if config.global_data_loader == 'iBOTS_DB':
            global_data_loader = IBOTSGlobalDataLoader()
        else:
            raise NotImplementedError()

        return App(
            global_data_loader=global_data_loader
        )
    