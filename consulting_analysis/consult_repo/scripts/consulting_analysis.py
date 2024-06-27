import os
from fsspec.implementations.local import LocalFileSystem
from src import ScieboDataDownload  
from src import WordDocumentProcessor
from src import count_types_of_sessions, count_num_unique_scholars, count_num_occurrances_of_word
from results_repo import ConsultingResultRepo

def main():
    os.environ['DB_WRITEMODE'] = '1'
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
    n_matlab = count_num_occurrances_of_word(processed_text, word='matlab')

    consulting_results = [
        n_short,
        n_hands,
        n_unique_scholars,
        n_python,
        n_matlab
    ]

    fs_local = LocalFileSystem()
    repo_local = ConsultingResultRepo.connect(fs_local)
    for consulting_result in consulting_results:
        repo_local.put(
            short_name=consulting_result.short_name,
            name=consulting_result.name,
            value=consulting_result.value,
            units=consulting_result.units,
            display_units=consulting_result.display_units
        )

    repo_local.push()


if __name__ == "__main__":
    main()