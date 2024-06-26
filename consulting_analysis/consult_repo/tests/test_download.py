from fsspec.implementations.local import LocalFileSystem
import pytest
from src import ScieboDataDownload

@pytest.fixture
def download_raw(tmp_path):
    sciebo_download = ScieboDataDownload()
    destination = tmp_path / "raw_data"
    destination.mkdir(parents=True, exist_ok=True)
    return destination    

def test_download_raw_reports(download_raw):
    sciebo_download = ScieboDataDownload()
    sciebo_download.download_raw_reports(destination=str(download_raw))
    fs_raw = LocalFileSystem()
    assert len(fs_raw.ls(str(download_raw), detail=False)) == 3
