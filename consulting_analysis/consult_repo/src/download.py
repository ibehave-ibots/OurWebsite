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
        DOWNLOAD_USR = os.getenv('DOWNLOAD_USR')
        DOWNLOAD_PWD = os.getenv('DOWNLOAD_PWD')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(DOWNLOAD_USR, DOWNLOAD_PWD))
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        load_dotenv()
        UPLOAD_USR = os.getenv('UPLOAD_USR')
        UPLOAD_PWD = os.getenv('UPLOAD_PWD')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(UPLOAD_USR, UPLOAD_PWD))
        fs.download("/", destination, recursive=True)
