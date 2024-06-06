from pathlib import Path
from scripts.data_processor import count_page_breaks, read_reports
from scripts.data_downloader import download_data



download_data()
reports = [file for file in Path('raw_data/').iterdir() if file.is_file()]
session_reports_list = read_reports(reports=reports)