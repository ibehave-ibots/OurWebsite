from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload  
from src import WordDocumentProcessor
from src import count_types_of_sessions

def main():
    fs_raw = LocalFileSystem()

    if not fs_raw.exists('raw/', detail=False):
        sciebo_download = ScieboDataDownload()
        sciebo_download.download_raw_reports(destination='raw/')

    word_doc = WordDocumentProcessor()
    reports = fs_raw.ls('raw/', detail=False)
    processed_text = word_doc.process(reports)

    n_short = count_types_of_sessions(processed_text, type='short')
    n_hands = count_types_of_sessions(processed_text, type='hands-on')
    print(n_short)
    print(n_hands)

    

if __name__ == "__main__":
    main()