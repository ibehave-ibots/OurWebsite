from dotenv import load_dotenv
from src import DataUpload
from webdav4.fsspec import WebdavFileSystem
import os

class ScieboDataUpload(DataUpload):
    def connect(self) -> WebdavFileSystem:
        load_dotenv()
        RESULT_USR = os.getenv('RESULT_USR') or '' 
        RESULT_PWD = os.getenv('RESULT_PWD') or ''
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(RESULT_USR, RESULT_PWD))
        return fs