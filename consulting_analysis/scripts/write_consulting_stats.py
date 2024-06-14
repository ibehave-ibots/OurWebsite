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
    n_hands_on = consolidated_report.lower().count('type: hands')
    n_sess = consolidated_report.lower().count('type: short') + consolidated_report.lower().count('type: hands')
    tot_hrs = consolidated_report.lower().count('type: short')*0.45 + consolidated_report.lower().count('type: hands')*2.5


    repo_local.put(
        short_name='n_short',
        name='Total number of sessions',
        value=n_short,
        units='Session',
        display_units='Session'
    )

    repo_local.put(
        short_name='n_sess',
        name='Total number of sessions',
        value=n_sess,
        units='Session',
        display_units='Session'
    )

    repo_local.put(
        short_name='tot_hrs',
        name='Total hours of sessions',
        value=tot_hrs,
        units='Hour',
        display_units='Hrs'
    )

    repo_local.put(
        short_name='n_hands',
        name='Total number of hands-on',
        value=n_hands_on,
        units='Hour',
        display_units='Hrs'
    )


    repo_local.push()
    

if __name__ == "__main__":
    input_path = sys.argv[1]
    main(input_path)
