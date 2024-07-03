from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
from dotenv import load_dotenv
from webdav4.fsspec import WebdavFileSystem
import os

class DataDownload(ABC):
    @abstractmethod
    def download_reports(self, destination: str) -> None:
        pass

    @abstractmethod
    def download_results(self, destination: str) -> None:
        pass

class ScieboDataDownload(DataDownload):
    def download_reports(self, destination: str):
        fs = self._get_file_system('report')
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        fs = self._get_file_system('result')
        fs.download("/", destination, recursive=True)

    def _get_file_system(self, type: Union['report': str, 'result': str]) -> WebdavFileSystem:
        load_dotenv()
        REPORT_USR = os.getenv('REPORT_USR') or ''
        REPORT_PWD = os.getenv('REPORT_PWD') or ''
        RESULT_USR = os.getenv('RESULT_USR') or ''
        RESULT_PWD = os.getenv('RESULT_PWD') or ''
        if type == 'report':
            return WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(REPORT_USR, REPORT_PWD))
        if type == 'result':
            return WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(RESULT_USR, RESULT_PWD))