import os
from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload  
from src import TemplateDocumentProcessor

def main():
    os.environ['DB_WRITEMODE'] = '1'
    fs_raw = LocalFileSystem()

    if not fs_raw.exists('raw/', detail=False):
        sciebo_download = ScieboDataDownload()
        sciebo_download.download_raw_reports(destination='raw/')

    template_doc = TemplateDocumentProcessor()
    reports = fs_raw.ls('raw/', detail=False)
    extracted_consultants = template_doc.process(reports_path=reports)


if __name__ == "__main__":
    main()