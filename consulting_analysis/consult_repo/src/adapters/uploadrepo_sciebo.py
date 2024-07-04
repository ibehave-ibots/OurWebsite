from dotenv import load_dotenv
from src import DataUpload
from src.external import load_result_credentials
from webdav4.fsspec import WebdavFileSystem

class ScieboResultsUpload(DataUpload):
    def connect(self) -> WebdavFileSystem:
        credentials = load_result_credentials()
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(credentials.USR, credentials.PWD))
        return fs