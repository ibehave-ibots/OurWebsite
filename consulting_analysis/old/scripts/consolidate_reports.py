import os
import sys
from pathlib import Path
from data_downloader import download_data, get_reports
from data_processor import create_consolidated_report

def main(input_dir, output_file):
    download_data()
    reports = get_reports(input_dir)
    consolidated_report = create_consolidated_report(reports=reports)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(consolidated_report)


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    main(input_dir, output_file)
