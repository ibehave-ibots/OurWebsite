from __future__ import annotations
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from webdav4.fsspec import WebdavFileSystem
import os

class DataDownload(ABC):
    @abstractmethod
    def download_raw_reports(self, destination: str) -> None:
        pass

    @abstractmethod
    def download_results(self, destination: str) -> None:
        pass

class ScieboDataDownload(DataDownload):
    def download_raw_reports(self, destination: str):
        load_dotenv()
        REPORT_USR = os.getenv('REPORT_USR')
        REPORT_PWD = os.getenv('REPORT_PWD')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(REPORT_USR, REPORT_PWD))
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        load_dotenv()
        RESULT_USR = os.getenv('REPORT_USR')
        RESULT_PWD = os.getenv('REPORT_PWD')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(RESULT_USR, RESULT_PWD))
        fs.download("/", destination, recursive=True)
