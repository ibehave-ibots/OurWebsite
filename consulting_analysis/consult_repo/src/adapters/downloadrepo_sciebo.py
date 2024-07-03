from .scieboexternal import load_report_credentials, load_result_credentials
from src.app import DataDownload
from webdav4.fsspec import WebdavFileSystem


class ScieboDataDownload(DataDownload):
    def download_reports(self, destination: str):
        credentials = load_report_credentials()
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(credentials.USR, credentials.PWD))
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        credentials = load_result_credentials()
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(credentials.USR, credentials.PWD))
        fs.download("/", destination, recursive=True)