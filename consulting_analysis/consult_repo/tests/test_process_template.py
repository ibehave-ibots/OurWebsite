import pytest
from src import TemplateDocumentProcessor
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path

@pytest.fixture
def reports(download_raw):
    template_doc = TemplateDocumentProcessor()
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls(str(download_raw))
    return reports


def test_process_return_template(reports):
    assert any(Path(report).stem == 'consulting_session_template' for report in reports)

def test_process_return_scholar_for_template(download_raw):
    ...

    