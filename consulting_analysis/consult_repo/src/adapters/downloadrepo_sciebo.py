from dataclasses import dataclass
import os
from typing import Union
from dotenv import load_dotenv
from src.app import DataDownload
from webdav4.fsspec import WebdavFileSystem


@dataclass
class Credentials:
    USR: str
    PWD: str

def load_report_credentials() -> Credentials:
    load_dotenv()
    return Credentials(
        USR = os.getenv('REPORT_USR') or '',
        PWD = os.getenv('REPORT_PWD') or ''
    )

def load_result_credentials() -> Credentials:
    load_dotenv()
    return Credentials(
        USR = os.getenv('RESULT_USR') or '',
        PWD = os.getenv('RESULT_PWD') or ''
    )

class ScieboDataDownload(DataDownload):
    def download_reports(self, destination: str):
        credentials = load_report_credentials()
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(credentials.USR, credentials.PWD))
        fs.download("/", destination, recursive=True)

    def download_results(self, destination: str):
        credentials = load_result_credentials()
        fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(credentials.USR, credentials.PWD))
        fs.download("/", destination, recursive=True)