from fsspec.implementations.local import LocalFileSystem
from src import WordDocumentProcessor

def test_process_string_is_not_empty(download_raw):
    word_doc = WordDocumentProcessor()
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls(str(download_raw))

    assert len(word_doc.process(reports)) > 0