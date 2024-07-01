from src import TemplateDocumentProcessor
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path

def test_process_return_template(download_raw):
    template_doc = TemplateDocumentProcessor()
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls(str(download_raw))
    assert any(Path(report).stem == 'consulting_session_template' for report in reports)
    