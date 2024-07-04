from __future__ import annotations
from abc import ABC, abstractmethod
from webdav4.fsspec import WebdavFileSystem


class DataUpload(ABC):
    @abstractmethod
    def connect(self) -> WebdavFileSystem:
        ...