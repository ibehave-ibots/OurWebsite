from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
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
        fs = self._get_file_system('report')
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        fs = self._get_file_system('result')
        fs.download("/", destination, recursive=True)

    def _get_file_system(self, type: Union['report': str, 'result': str]) -> WebdavFileSystem:
        load_dotenv()
        REPORT_USR = os.getenv('REPORT_USR')
        REPORT_PWD = os.getenv('REPORT_PWD')
        RESULT_USR = os.getenv('REPORT_USR')
        RESULT_PWD = os.getenv('REPORT_PWD')
        if type == 'report':
            return WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(REPORT_USR, REPORT_PWD))
        if type == 'result':
            return WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(RESULT_USR, RESULT_PWD))