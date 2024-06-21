from __future__ import annotations
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
from fsspec.implementations.local import LocalFileSystem
from webdav4.fsspec import WebdavFileSystem


class DataDownloadStrategy(ABC):
    @abstractmethod
    def download_raw_reports(self, destination: str) -> None:
        pass

    @abstractmethod
    def download_results(self, destination: str) -> None:
        pass

class ScieboDataDownload(DataDownloadStrategy):
    def download_raw_reports(self, destination: str):
        load_dotenv()
        SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
        SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        load_dotenv()
        SANGEE_RESULTS_USR = os.getenv('USR')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_RESULTS_USR, ''))
        fs.download("/", destination, recursive=True)


def test_download_raw_reports():
    sciebo_download = ScieboDataDownload()
    sciebo_download.download_raw_reports(destination='raw_data/')
    fs_raw = LocalFileSystem()
    assert len(fs_raw.ls('raw_data', detail=False)) == 3
