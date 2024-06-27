from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload  
from src import WordDocumentProcessor
from src import count_types_of_sessions, count_num_unique_scholars, count_num_occurrances_of_word

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

    n_unique_scholars = count_num_unique_scholars(processed_text)

    n_python = count_num_occurrances_of_word(processed_text, word='python')
    print(n_python)


    

if __name__ == "__main__":
    main()