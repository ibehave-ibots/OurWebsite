from pathlib import Path
from dotenv import load_dotenv
import os
from webdav4.fsspec import WebdavFileSystem

load_dotenv()

def download_data():
    fs = connect_to_sciebo()
    fs.download("/", "raw_data", recursive=True)

def connect_to_sciebo():
    SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
    SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')
    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))
    return fs

def get_reports(input_dir):
    return [file for file in Path(input_dir).iterdir() if file.is_file()]
