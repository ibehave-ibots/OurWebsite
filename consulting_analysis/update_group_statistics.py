from pathlib import Path
from scripts.data_processor import count_page_breaks, create_consolidated_report
from scripts.data_downloader import download_data



download_data()
reports = [file for file in Path('raw_data/').iterdir() if file.is_file()]
consolidated_report = create_consolidated_report(reports=reports)
print(consolidated_report)