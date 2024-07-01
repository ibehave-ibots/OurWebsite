from __future__ import annotations
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from webdav4.fsspec import WebdavFileSystem
import os



class RemoteDataUpload(ABC):
    @abstractmethod
    def connect(self) -> WebdavFileSystem:
        ...

class ScieboDataUpload(RemoteDataUpload):
    def connect(self) -> WebdavFileSystem:
        load_dotenv()
        SANGEE_RESULTS_USR = os.getenv('USR')
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_RESULTS_USR, ''))
        return fs