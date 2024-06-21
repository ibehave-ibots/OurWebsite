from __future__ import annotations
from abc import ABC, abstractmethod
from fsspec.implementations.local import LocalFileSystem
from webdav4.fsspec import WebdavFileSystem
import os
from docx import Document


class DataProcessStrategy(ABC):
    @abstractmethod
    def process(self, reports: list) -> None:
        pass

class WordDocumentProcessor(DataProcessStrategy):
    def process(self, report):
        doc = Document(report)
        session_report = self.get_pages(doc)
        return session_report    
    
    def get_pages(self, doc, pattern='___'):
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

    def create_consolidated_report(self, reports):
        session_reports = []
        for report in reports:
            session_report = self.generate_report(report)
            session_reports.extend(session_report)

        consolidated_report = ' '.join(session_reports)
        return consolidated_report

