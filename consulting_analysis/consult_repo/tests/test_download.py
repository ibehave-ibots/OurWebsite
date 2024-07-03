from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload  

def test_download_reports(download_raw):
    sciebo_download = ScieboDataDownload()
    sciebo_download.download_reports(destination=str(download_raw))
    fs_raw = LocalFileSystem()
    assert len(fs_raw.ls(str(download_raw), detail=False)) > 0

def test_download_results(download_raw):
    sciebo_download = ScieboDataDownload()
    sciebo_download.download_results(destination=str(download_raw))
    fs_raw = LocalFileSystem()
    assert len(fs_raw.ls(str(download_raw), detail=False)) > 0