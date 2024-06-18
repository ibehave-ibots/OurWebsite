from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import fsspec
from webdav4.fsspec import WebdavFileSystem
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path


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

    def pull(self):
        Path.mkdir(Path(self.fs_to), exist_ok=True)
        self.fs_from.download("/", self.fs_to, recursive=True)



def test_download_from_sciebo():
    load_dotenv()
    SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
    SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')
    fs_remote = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))

    repo = Storage.connect(
        fs_from = fs_remote,
        fs_to = 'raw_data/'
    )

    repo.pull()

    fs_raw = LocalFileSystem()
    repo_raw = Storage.connect(
        fs_from=fs_raw,
        fs_to = 'processed/'
    )

    assert len(repo_raw.list_files('raw_data')) == 3

