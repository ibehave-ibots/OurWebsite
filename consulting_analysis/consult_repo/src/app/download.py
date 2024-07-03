from __future__ import annotations
from abc import ABC, abstractmethod


class DataDownload(ABC):
    @abstractmethod
    def download_reports(self, destination: str) -> None:
        pass

    @abstractmethod
    def download_results(self, destination: str) -> None:
        pass

