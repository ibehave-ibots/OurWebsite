from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload, TemplateDocumentProcessor
import yaml

def main():
    fs_raw = LocalFileSystem()
    if not fs_raw.exists('raw/', details=False):
        sciebo_download = ScieboDataDownload(destination='raw/')

    template_doc = TemplateDocumentProcessor()
    reports = fs_raw.ls('raw/', detail=False)
    extracted_consultants = template_doc.process(reports_path=reports)

    consultants = extracted_consultants[1:]
    num_short_sessions = sum(consultant.num_short_sessions for consultant in consultants)
    total_sessions = sum(consultant.num_total_sessions for consultant in consultants)
    num_unique_scholars = len(set().union(*[consultant.scholars for consultant in consultants]))

    consulting_stats = {
        'num_short_sessions': num_short_sessions,
        'total_sessions': total_sessions,
        'num_unique_scholars': num_unique_scholars
    }

    with open('consulting_statistics.yaml', 'w') as f:
        yaml.dump(consulting_stats, f)
        
if __name__ == '__main__':
    main()

