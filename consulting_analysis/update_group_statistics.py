from pathlib import Path
from scripts.data_processor import count_page_breaks
from scripts.data_downloader import download_data
from docx import Document


download_data()

reports = [file for file in Path('raw_data/').iterdir() if file.is_file()]
session_reports = []
for report in reports:
    doc = Document(report)
    num_session, session_report = count_page_breaks(doc)
    session_reports.extend(session_report)
