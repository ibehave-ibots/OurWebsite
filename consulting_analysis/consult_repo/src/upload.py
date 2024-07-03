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
        RESULT_USR = os.getenv('RESULT_USR') or '' 
        RESULT_PWD = os.getenv('RESULT_PWD') or ''
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(RESULT_USR, RESULT_PWD))
        return fs