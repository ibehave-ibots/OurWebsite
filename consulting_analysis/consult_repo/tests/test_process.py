from __future__ import annotations
from abc import ABC, abstractmethod
from fsspec.implementations.local import LocalFileSystem
from docx import Document
from .test_download import ScieboDataDownload
import pytest


class DataProcessStrategy(ABC):
    @abstractmethod
    def process(self, reports: list) -> None:
        pass

class WordDocumentProcessor(DataProcessStrategy):

    def process(self, reports) -> str:
        session_reports = []
        for report in reports:
            session_report = self._get_report(report)
            session_reports.extend(session_report)

        consolidated_report = ' '.join(session_reports)
        return consolidated_report

    def _get_report(self, report):
        doc = Document(report)
        session_report = self._get_pages(doc)
        return session_report    
    
    def _get_pages(self, doc, pattern='___'):
        pages = []
        current_text = ""

        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if run._r.xpath('.//w:br[@w:type="page"]'):
                    if pattern in current_text:
                        pages.append(current_text.split(pattern)[0].strip())
                    else:
                        pages.append(current_text.strip())
                    current_text = ""
                else:
                    current_text += run.text + '\n'
        
        if current_text.strip():
            if pattern in current_text:
                pages.append(current_text.split(pattern)[0].strip())
            else:
                pages.append(current_text.strip())

        return pages


@pytest.fixture
def download_raw():
    sciebo_download = ScieboDataDownload()
    sciebo_download.download_raw_reports(destination='raw_data/')    

def test_process_string_is_not_empty(download_raw):
    word_doc = WordDocumentProcessor()
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls('raw_data/')

    assert len(word_doc.process(reports)) != 0