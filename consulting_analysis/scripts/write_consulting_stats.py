from results_repo import ConsultingResultRepo
from fsspec.implementations.local import LocalFileSystem
import os
import sys
from pathlib import Path

def main(input_path):
    os.environ['DB_WRITEMODE'] = '1'

    with open(input_path, 'r', encoding='utf-8') as f:
        consolidated_report = f.read().replace('\n', '')

    fs_local = LocalFileSystem()
    repo_local = ConsultingResultRepo.connect(fs_local)

    n_short = consolidated_report.lower().count('type: short')

    repo_local.put(
        short_name='n_sess',
        name='Total number of sessions',
        value=n_short,
        units='Session',
        display_units='Session'
    )

    repo_local.push()
    

if __name__ == "__main__":
    input_path = sys.argv[1]
    main(input_path)
