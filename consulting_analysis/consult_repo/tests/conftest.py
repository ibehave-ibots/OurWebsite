import pytest
from src import ScieboDataDownload

@pytest.fixture
def download_raw(tmp_path):
    sciebo_download = ScieboDataDownload()
    destination = tmp_path / "raw_data"
    destination.mkdir(parents=True, exist_ok=True)
    sciebo_download.download_raw_reports(destination=str(destination))
    return destination    