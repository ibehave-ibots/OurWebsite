from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload
from src import WordDocumentProcessor

import pytest


@pytest.fixture
def download_raw(tmp_path):
    sciebo_download = ScieboDataDownload()
    destination = tmp_path / "raw_data"
    destination.mkdir(parents=True, exist_ok=True)
    sciebo_download.download_raw_reports(destination=str(destination))
    return destination    


def test_process_string_is_not_empty(download_raw):
    word_doc = WordDocumentProcessor()
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls(str(download_raw))

    assert len(word_doc.process(reports)) != 0