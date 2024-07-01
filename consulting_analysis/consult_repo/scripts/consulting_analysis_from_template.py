import os
from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload, TemplateDocumentProcessor  

def main():
    os.environ['DB_WRITEMODE'] = '1'
    fs_raw = LocalFileSystem()

    if not fs_raw.exists('raw/', detail=False):
        sciebo_download = ScieboDataDownload()
        sciebo_download.download_raw_reports(destination='raw/')

    template_doc = TemplateDocumentProcessor()
    reports = fs_raw.ls('raw/', detail=False)
    extracted_consultants = template_doc.process(reports_path=reports)
    consultants = extracted_consultants[1:]
    total_sessions = sum(consultant.num_total_sessions for consultant in consultants)
    num_short_sessions = sum(consultant.num_short_sessions for consultant in consultants)
    num_hands_on_sessions = sum(consultant.num_hands_on_sessions for consultant in consultants)
    num_unique_scholars = sum(consultant.num_unique_scholars for consultant in consultants)
    time_short_hrs = sum(consultant.time_short_hrs for consultant in consultants)
    time_hands_on_hrs = sum(consultant.time_hands_on_hrs for consultant in consultants)
    time_all_hrs = sum(consultant.time_all_hrs for consultant in consultants)
    content = " ".join(consultant.consolidated_content for consultant in consultants)
    
    num_python = content.lower().count('python')
    num_matlab = content.lower().count('matlab')



if __name__ == "__main__":
    main()