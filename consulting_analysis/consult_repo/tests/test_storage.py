from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import fsspec
from webdav4.fsspec import WebdavFileSystem
from fsspec.implementations.local import LocalFileSystem
from fsspec import filesystem
from pathlib import Path

from consulting_analysis.scripts.data_downloader import get_reports
from consulting_analysis.scripts.data_processor import create_consolidated_report


@dataclass
class Storage:
    fs_from: fsspec.AbstractFileSystem
    fs_to: str

    @classmethod
    def connect(cls, fs_from: fsspec.AbstractFileSystem, fs_to: str) -> Storage:
        return Storage(
            fs_from=fs_from,
            fs_to=fs_to
        )
    
    def list_files(self, path):
        return self.fs_from.ls(path)

    def push(self):
        Path.mkdir(Path(self.fs_to), exist_ok=True)
        self.fs_from.download("/", self.fs_to, recursive=True)

    def write_to(self, path: str, text: str):
        Path.mkdir(Path(self.fs_to), exist_ok=True)
        self.fs_from.write_text(path, text, encoding='utf-8')



def test_download_from_sciebo():
    load_dotenv()
    SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
    SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')
    fs_remote = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))

    repo = Storage.connect(
        fs_from = fs_remote,
        fs_to = 'raw_data/'
    )

    repo.push()

    fs_raw = LocalFileSystem()
    repo_raw = Storage.connect(
        fs_from=fs_raw,
        fs_to = 'processed/'
    )

    assert len(repo_raw.list_files('raw_data')) == 3

def test_process_read_from_raw():
    fs_raw = LocalFileSystem()
    fs_processed = 'processed_data/'
    repo = Storage.connect(
        fs_from=fs_raw,
        fs_to=fs_processed
    )

    reports = fs_raw.ls('raw_data/', detail=False)
    consolidated_report = create_consolidated_report(reports=reports)

    repo.write_to(fs_processed + 'consolidated_report.txt', consolidated_report)

    assert len(repo.list_files(fs_processed)) == 1
